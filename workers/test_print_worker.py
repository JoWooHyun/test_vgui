"""
Test VGUI - Print Worker (DLP 제거, LED → 5초 대기)
기존 print_worker.py의 출력 시퀀스를 그대로 유지하되,
DLP/LED/이미지 관련 기능을 모두 제거.
"""

import time
from enum import Enum, auto
from typing import Optional, Dict, Any
from dataclasses import dataclass

from PySide6.QtCore import QThread, Signal, QMutex, QWaitCondition

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from controllers.motor_controller import MotorController
except ImportError:
    from ..controllers.motor_controller import MotorController


# LED 대체 대기 시간 (초)
LED_SUBSTITUTE_DELAY = 5.0


class PrintStatus(Enum):
    IDLE = auto()
    INITIALIZING = auto()
    LEVELING = auto()
    PRINTING = auto()
    PAUSED = auto()
    STOPPING = auto()
    COMPLETED = auto()
    ERROR = auto()


@dataclass
class PrintJob:
    total_layers: int = 100
    layer_height: float = 0.05
    bottom_layer_count: int = 3
    blade_speed: int = 300       # mm/min
    blade_cycles: int = 1
    leveling_cycles: int = 1
    y_dispense_distance: float = 1.0
    y_dispense_speed: int = 300
    y_dispense_delay: float = 2.0
    y_priming_position: float = 0.0


class TestPrintWorker(QThread):
    """
    테스트용 프린트 워커 - DLP 없이 모터만 동작
    LED ON/OFF → 5초 대기로 대체
    """

    status_changed = Signal(str)
    progress_updated = Signal(int, int)  # current, total
    layer_started = Signal(int)
    error_occurred = Signal(str)
    print_completed = Signal()
    print_stopped = Signal()
    resin_empty = Signal()

    def __init__(self, motor: Optional[MotorController] = None, parent=None):
        super().__init__(parent)

        self.motor = motor

        self._status = PrintStatus.IDLE
        self._is_paused = False
        self._is_stopped = False

        self._mutex = QMutex()
        self._pause_condition = QWaitCondition()
        self._resin_mutex = QMutex()
        self._resin_condition = QWaitCondition()

        self._y_position = 0.0
        self._y_dispensing_disabled = False
        self._y_resin_waiting = False

        self._job: Optional[PrintJob] = None

        self.simulation = False

    @property
    def status(self) -> PrintStatus:
        return self._status

    def _set_status(self, status: PrintStatus):
        self._status = status
        self.status_changed.emit(status.name)
        print(f"[TestPrintWorker] 상태: {status.name}")

    def start_print(self, params: Dict[str, Any],
                    blade_speed: int = 300,
                    leveling_cycles: int = 1,
                    blade_cycles: int = 1,
                    y_dispense_distance: float = 1.0,
                    y_dispense_speed: int = 300,
                    y_dispense_delay: float = 2.0,
                    y_priming_position: float = 0.0):
        if self.isRunning():
            print("[TestPrintWorker] 이미 실행 중")
            return

        self._job = PrintJob(
            total_layers=params.get('totalLayer', 100),
            layer_height=params.get('layerHeight', 0.05),
            bottom_layer_count=params.get('bottomLayerCount', 3),
            blade_speed=blade_speed,
            blade_cycles=blade_cycles,
            leveling_cycles=leveling_cycles,
            y_dispense_distance=y_dispense_distance,
            y_dispense_speed=y_dispense_speed,
            y_dispense_delay=y_dispense_delay,
            y_priming_position=y_priming_position,
        )

        self._is_paused = False
        self._is_stopped = False
        self._y_position = y_priming_position
        self._y_dispensing_disabled = False
        self._y_resin_waiting = False

        self.start()

    def pause(self):
        self._mutex.lock()
        self._is_paused = True
        self._mutex.unlock()
        self._set_status(PrintStatus.PAUSED)

    def resume(self):
        self._mutex.lock()
        self._is_paused = False
        self._pause_condition.wakeAll()
        self._mutex.unlock()
        self._set_status(PrintStatus.PRINTING)

    def stop(self):
        self._mutex.lock()
        self._is_stopped = True
        self._is_paused = False
        self._pause_condition.wakeAll()
        self._mutex.unlock()
        self._resin_mutex.lock()
        self._y_resin_waiting = False
        self._resin_condition.wakeAll()
        self._resin_mutex.unlock()
        self._set_status(PrintStatus.STOPPING)

    def disable_y_dispensing(self):
        self._y_dispensing_disabled = True
        self._resin_mutex.lock()
        self._y_resin_waiting = False
        self._resin_condition.wakeAll()
        self._resin_mutex.unlock()

    def stop_by_resin_empty(self):
        self._resin_mutex.lock()
        self._y_resin_waiting = False
        self._resin_condition.wakeAll()
        self._resin_mutex.unlock()
        self.stop()

    # ==================== 메인 루프 ====================

    def run(self):
        if not self._job:
            self.error_occurred.emit("프린트 작업이 없습니다")
            return
        try:
            self._run_print_sequence()
        except Exception as e:
            self._set_status(PrintStatus.ERROR)
            self.error_occurred.emit(str(e))
            print(f"[TestPrintWorker] 오류: {e}")
        finally:
            self._cleanup()

    def _run_print_sequence(self):
        job = self._job

        # 1. 초기화
        self._set_status(PrintStatus.INITIALIZING)
        print(f"[TestPrintWorker] 테스트 프린트 시작")
        print(f"  - 총 레이어: {job.total_layers}")
        print(f"  - 블레이드 속도: {job.blade_speed} mm/min")

        if not self.simulation:
            if self.motor:
                self.motor.connect()
                self.motor.klipper_clear_pause()

        # X축 홈 → 대기 위치 (X 먼저)
        if self._check_stopped():
            return
        if not self._motor_x_home():
            self.error_occurred.emit("X축 홈 이동 실패")
            self._is_stopped = True
            return
        if not self._motor_x_move(10, job.blade_speed):
            self.error_occurred.emit("X축 대기 위치(10mm) 이동 실패")
            self._is_stopped = True
            return

        # Z축 홈 → 0.1mm 이동
        if self._check_stopped():
            return
        if not self._motor_z_home():
            self.error_occurred.emit("Z축 홈 이동 실패")
            self._is_stopped = True
            return
        if not self._motor_z_move(0.1):
            self.error_occurred.emit("Z축 0.1mm 이동 실패")
            self._is_stopped = True
            return

        # Resin 위치
        print(f"[TestPrintWorker] Resin start position: {job.y_priming_position}mm")
        self._y_position = job.y_priming_position

        # 2. 첫 레진 토출 (고정값: 1mm, 3mm/s, 60초 대기)
        INITIAL_DISPENSE_DIST = -1.0
        INITIAL_DISPENSE_SPEED = 180  # mm/min (3mm/s)
        INITIAL_DISPENSE_DELAY = 30.0
        if not self._y_dispensing_disabled and self._y_position > 0:
            if self._check_stopped():
                return
            if not self._motor_y_move(INITIAL_DISPENSE_DIST, INITIAL_DISPENSE_SPEED):
                self.error_occurred.emit("초기 레진 토출 실패")
                self._is_stopped = True
                return
            self._y_position += INITIAL_DISPENSE_DIST
            print(f"[TestPrintWorker] Initial resin dispensed {INITIAL_DISPENSE_DIST}mm (pos: {self._y_position:.1f}mm)")
            wait_start = time.monotonic()
            while (time.monotonic() - wait_start) < INITIAL_DISPENSE_DELAY:
                if self._check_stopped():
                    return
                time.sleep(0.1)

        # 3. 레진 평탄화
        if job.leveling_cycles > 0:
            self._set_status(PrintStatus.LEVELING)
            if self._check_stopped():
                return
            self._run_leveling(job.leveling_cycles, job.blade_speed)

        # 4. 메인 프린팅 루프
        self._set_status(PrintStatus.PRINTING)
        total_layers = job.total_layers

        for layer_idx in range(total_layers):
            if self._check_stopped():
                break
            self._check_paused()
            if self._check_stopped():
                break

            self.layer_started.emit(layer_idx)
            self.progress_updated.emit(layer_idx + 1, total_layers)

            if not self._process_layer(layer_idx, job):
                break

        # 5. 완료 또는 정지
        if self._is_stopped:
            self._set_status(PrintStatus.STOPPING)
            self.print_stopped.emit()
        else:
            self._set_status(PrintStatus.COMPLETED)
            self.print_completed.emit()

    def _process_layer(self, layer_idx: int, job: PrintJob) -> bool:
        """
        레이어 처리 (기존 시퀀스 그대로, DLP만 제거)

        1. Z축 레이어 높이로 이동
        2. Resin 토출 + 대기
        3. X축 10→140 (평탄화)
        4. [LED ON → 5초 대기로 대체]
        5. Z축 리프트 (+5mm)
        6. X축 140→10 (복귀)
        """
        # Z축 위치
        z_position = (layer_idx + 1) * job.layer_height

        # 1. Z축 이동
        if not self._motor_z_move(z_position):
            self.error_occurred.emit(f"레이어 {layer_idx}: Z축 이동 실패")
            self._is_stopped = True
            return False

        # 2. Resin 토출
        if not self._y_dispensing_disabled and job.y_dispense_distance > 0:
            if self._y_position <= 0:
                print(f"[TestPrintWorker] Resin empty at {self._y_position}mm")
                self._y_resin_waiting = True
                self.resin_empty.emit()
                self._resin_mutex.lock()
                while self._y_resin_waiting and not self._is_stopped:
                    self._resin_condition.wait(self._resin_mutex, 1000)
                self._resin_mutex.unlock()
                if self._check_stopped():
                    return True

            if not self._y_dispensing_disabled:
                dispense_dist = -job.y_dispense_distance
                if not self._motor_y_move(dispense_dist, job.y_dispense_speed):
                    self.error_occurred.emit(f"Layer {layer_idx}: Resin dispense failed")
                    self._is_stopped = True
                    return False
                self._y_position += dispense_dist
                print(f"[TestPrintWorker] Resin dispensed {dispense_dist}mm (pos: {self._y_position:.1f}mm)")
                wait_start = time.monotonic()
                while (time.monotonic() - wait_start) < job.y_dispense_delay:
                    if self._check_stopped():
                        return False
                    time.sleep(0.1)

        # 3. X축 평탄화 (10→140)
        if not self._motor_x_move(140, job.blade_speed):
            self.error_occurred.emit(f"레이어 {layer_idx}: X축 평탄화 실패")
            self._is_stopped = True
            return False

        # 정지/일시정지 체크
        if self._check_stopped():
            return True
        self._check_paused()
        if self._check_stopped():
            return True

        # 4. LED ON 대체 → 5초 대기
        print(f"[TestPrintWorker] Layer {layer_idx}: LED 대기 {LED_SUBSTITUTE_DELAY}초")
        start = time.monotonic()
        while (time.monotonic() - start) < LED_SUBSTITUTE_DELAY:
            if self._check_stopped():
                return True
            time.sleep(0.1)

        # 정지/일시정지 체크
        if self._check_stopped():
            return True
        self._check_paused()
        if self._check_stopped():
            return True

        # 5. Z축 리프트 (+5mm)
        z_lift_position = z_position + 5.0
        if not self._motor_z_move(z_lift_position):
            self.error_occurred.emit(f"레이어 {layer_idx}: Z축 리프트 실패")
            self._is_stopped = True
            return False

        # 6. X축 복귀 (140→10, 빠른 속도)
        if not self._motor_x_move(10, 3000):
            self.error_occurred.emit(f"레이어 {layer_idx}: X축 복귀 실패")
            self._is_stopped = True
            return False

        return True

    # ==================== 모터 래퍼 ====================

    def _motor_z_home(self) -> bool:
        print("[TestPrintWorker] Z축 홈")
        if self.motor and not self.simulation:
            return self.motor.z_home()
        else:
            time.sleep(0.5)
            return True

    def _motor_x_home(self, force: bool = True) -> bool:
        print("[TestPrintWorker] X축 홈")
        if self.motor and not self.simulation:
            return self.motor.x_home(force=force)
        else:
            time.sleep(0.3)
            return True

    def _motor_z_move(self, position: float, speed: int = 300) -> bool:
        if self.motor and not self.simulation:
            return self.motor.z_move_absolute(position, speed)
        else:
            time.sleep(0.1)
            return True

    def _motor_x_move(self, position: float, speed: int = 300) -> bool:
        if self.motor and not self.simulation:
            return self.motor.x_move_absolute(position, speed)
        else:
            time.sleep(0.2)
            return True

    def _motor_y_move(self, distance: float, speed: int = 300) -> bool:
        if self.motor and not self.simulation:
            return self.motor.y_move_relative(distance, speed)
        else:
            time.sleep(0.1)
            return True

    # ==================== 유틸리티 ====================

    def _run_leveling(self, cycles: int, speed: int):
        print(f"[TestPrintWorker] 레진 평탄화 ({cycles}회)")
        if self.motor and not self.simulation:
            self.motor.leveling_cycle(cycles, speed)
        else:
            for i in range(cycles):
                if self._check_stopped():
                    return
                print(f"[TestPrintWorker] 평탄화 {i+1}/{cycles}")
                time.sleep(0.5)

    def _check_stopped(self) -> bool:
        self._mutex.lock()
        stopped = self._is_stopped
        self._mutex.unlock()
        return stopped

    def _check_paused(self):
        self._mutex.lock()
        if self._is_paused and not self._is_stopped:
            self._mutex.unlock()
            if self.motor and not self.simulation:
                self.motor.klipper_pause()
            self._mutex.lock()

            while self._is_paused and not self._is_stopped:
                self._pause_condition.wait(self._mutex, 1000)

            if not self._is_stopped:
                self._mutex.unlock()
                if self.motor and not self.simulation:
                    self.motor.klipper_resume()
                    time.sleep(2.0)
                self._mutex.lock()
        self._mutex.unlock()

    def _cleanup(self):
        print("[TestPrintWorker] 정리 중...")

        # Z축 현재 위치 유지, X축 홈 복귀
        self._motor_x_home()

        if self.motor and not self.simulation:
            self.motor.klipper_clear_pause()
            self.motor.klipper_cancel()

        self._set_status(PrintStatus.IDLE)
        print("[TestPrintWorker] 정리 완료")
