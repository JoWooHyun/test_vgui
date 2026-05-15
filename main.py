#!/usr/bin/env python3
"""
Test VGUI - DLP 없이 모터만 동작하는 테스트용 GUI
VGUI와 동일한 구조, DLP/LED/이미지 관련 기능 제거

Version: 1.0
Resolution: 1024x600
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from controllers.theme_manager import get_theme_manager
_theme_init = get_theme_manager()

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QStackedWidget, QDialog,
    QVBoxLayout, QLabel, QPushButton
)
from PySide6.QtCore import Qt, QThread, Signal, QObject

from styles.colors import Colors
from styles.fonts import Fonts
from styles.stylesheets import get_global_style, Radius
from pages.main_page import MainPage
from pages.tool_page import ToolPage
from pages.manual_page import ManualPage
from pages.setting_page import SettingPage
from pages.material_page import MaterialPage
from pages.print_test_page import PrintTestPage
from pages.test_progress_page import TestProgressPage

from controllers.motor_controller import MotorController
from controllers.settings_manager import get_settings
from workers.test_print_worker import TestPrintWorker, PrintStatus

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600
MOONRAKER_URL = "http://localhost:7125"
SIMULATION_MODE = False


class SimpleAlert(QDialog):
    """간단한 알림 다이얼로그"""
    def __init__(self, message: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("알림")
        self.setFixedSize(300, 150)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.BG_PRIMARY};
                border: 2px solid {Colors.BORDER};
                border-radius: {Radius.LG}px;
            }}
        """)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 20)
        layout.setSpacing(20)

        lbl = QLabel(message)
        lbl.setFont(Fonts.h3())
        lbl.setAlignment(Qt.AlignCenter)
        lbl.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background-color: {Colors.BG_PRIMARY}; border: none;")
        layout.addWidget(lbl)

        btn_ok = QPushButton("OK")
        btn_ok.setFixedSize(100, 40)
        btn_ok.setCursor(Qt.PointingHandCursor)
        btn_ok.setFont(Fonts.body())
        btn_ok.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.NAVY};
                border: none;
                border-radius: {Radius.MD}px;
                color: {Colors.WHITE};
            }}
            QPushButton:pressed {{
                background-color: {Colors.NAVY_LIGHT};
            }}
        """)
        btn_ok.clicked.connect(self.accept)
        layout.addWidget(btn_ok, alignment=Qt.AlignCenter)


class MotorWorker(QObject):
    """모터 작업 백그라운드 워커"""
    finished = Signal()
    error = Signal(str)

    def __init__(self, motor, operation: str, **kwargs):
        super().__init__()
        self.motor = motor
        self.operation = operation
        self.kwargs = kwargs

    def run(self):
        try:
            if self.operation == "z_move":
                self.motor.z_move_relative(self.kwargs.get("distance", 0))
            elif self.operation == "z_home":
                self.motor.z_home()
            elif self.operation == "x_move":
                self.motor.x_move_relative(
                    self.kwargs.get("distance", 0),
                    speed=self.kwargs.get("speed", 300)
                )
            elif self.operation == "x_home":
                self.motor.x_home()
            elif self.operation == "y_move":
                self.motor.y_move_relative(self.kwargs.get("distance", 0))
            elif self.operation == "y_home":
                self.motor.y_home()
            elif self.operation == "y_reset_position":
                self.motor.y_reset_position()
        except Exception as e:
            self.error.emit(str(e))
        finally:
            self.finished.emit()


class MainWindow(QMainWindow):
    """메인 윈도우"""

    PAGE_MAIN = 0
    PAGE_TOOL = 1
    PAGE_MANUAL = 2
    PAGE_SETTING = 3
    PAGE_MATERIAL = 4
    PAGE_PRINT_TEST = 5
    PAGE_TEST_PROGRESS = 6

    def __init__(self, simulation: bool = True):
        super().__init__()
        self.setWindowTitle("Test VGUI - Motor Test v1.0")
        self.setFixedSize(SCREEN_WIDTH, SCREEN_HEIGHT)

        self.simulation = simulation

        # 모터 컨트롤러
        self.motor = MotorController(MOONRAKER_URL)
        if not self.simulation:
            self.motor.connect()
        print(f"[System] 하드웨어 초기화 (시뮬레이션: {self.simulation})")

        # 설정
        self.settings = get_settings()
        self.theme_manager = get_theme_manager()

        # 페이지
        self._setup_pages()
        self._connect_signals()
        self._apply_saved_settings()

        # 워커
        self.print_worker = None
        self._motor_threads = []

    def _setup_pages(self):
        self.stack = QStackedWidget()

        self.main_page = MainPage()
        self.tool_page = ToolPage()
        self.manual_page = ManualPage()
        self.setting_page = SettingPage()
        self.material_page = MaterialPage()
        self.print_test_page = PrintTestPage()
        self.test_progress_page = TestProgressPage()

        self.stack.addWidget(self.main_page)          # 0
        self.stack.addWidget(self.tool_page)           # 1
        self.stack.addWidget(self.manual_page)         # 2
        self.stack.addWidget(self.setting_page)        # 3
        self.stack.addWidget(self.material_page)       # 4
        self.stack.addWidget(self.print_test_page)     # 5
        self.stack.addWidget(self.test_progress_page)  # 6

        self.setCentralWidget(self.stack)

    def _apply_saved_settings(self):
        saved_blade_speed = self.settings.get_blade_speed()
        self.setting_page.set_blade_speed(saved_blade_speed)

        # LED power는 표시만 (DLP 없으므로 동작 안 함)
        saved_led_power = self.settings.get_led_power()
        self.setting_page.set_led_power(saved_led_power)

        print(f"[System] 설정 적용: Blade={saved_blade_speed}mm/s")

    def _connect_signals(self):
        # 메인
        self.main_page.go_tool.connect(lambda: self._go_to_page(self.PAGE_TOOL))
        self.main_page.go_print_test.connect(lambda: self._go_to_page(self.PAGE_PRINT_TEST))

        # 도구
        self.tool_page.go_back.connect(lambda: self._go_to_page(self.PAGE_MAIN))
        self.tool_page.go_manual.connect(lambda: self._go_to_page(self.PAGE_MANUAL))
        self.tool_page.go_setting.connect(lambda: self._go_to_page(self.PAGE_SETTING))
        self.tool_page.go_material.connect(lambda: self._go_to_page(self.PAGE_MATERIAL))

        # 매뉴얼
        self.manual_page.go_back.connect(lambda: self._go_to_page(self.PAGE_TOOL))
        self.manual_page.z_move.connect(self._move_z)
        self.manual_page.z_home.connect(self._home_z)
        self.manual_page.x_move.connect(self._move_x)
        self.manual_page.x_home.connect(self._home_x)
        self.manual_page.y_move.connect(self._manual_y_move)
        self.manual_page.y_home.connect(self._manual_y_home)

        # 설정
        self.setting_page.go_back.connect(lambda: self._go_to_page(self.PAGE_TOOL))
        self.setting_page.led_on.connect(self._setting_led_on)
        self.setting_page.led_off.connect(self._setting_led_off)
        self.setting_page.blade_home.connect(self._setting_blade_home)
        self.setting_page.blade_move.connect(self._setting_blade_move)
        self.setting_page.led_power_changed.connect(self._on_led_power_changed)
        self.setting_page.blade_speed_changed.connect(self._on_blade_speed_changed)
        self.setting_page.y_move.connect(self._setting_y_move)
        self.setting_page.y_home.connect(self._setting_y_home)
        self.setting_page.y_prime_start.connect(self._setting_y_prime_start)
        self.setting_page.y_prime_done.connect(self._setting_y_prime_done)

        # 소재
        self.material_page.go_back.connect(lambda: self._go_to_page(self.PAGE_TOOL))

        # 프린트 테스트
        self.print_test_page.go_back.connect(lambda: self._go_to_page(self.PAGE_MAIN))
        self.print_test_page.start_test.connect(self._on_start_test)

        # 테스트 진행
        self.test_progress_page.go_home.connect(lambda: self._go_to_page(self.PAGE_MAIN))
        self.test_progress_page.pause_requested.connect(self._on_pause)
        self.test_progress_page.resume_requested.connect(self._on_resume)
        self.test_progress_page.stop_requested.connect(self._on_stop)

    def _go_to_page(self, page_index: int):
        self.stack.setCurrentIndex(page_index)

    # ==================== 모터 제어 ====================

    def _start_motor_operation(self, operation: str, on_finished=None, **kwargs):
        thread = QThread()
        worker = MotorWorker(self.motor, operation, **kwargs)
        worker.moveToThread(thread)

        thread.started.connect(worker.run)
        worker.finished.connect(thread.quit)
        worker.error.connect(self._on_motor_error)
        thread.finished.connect(lambda: self._cleanup_thread(thread, worker))

        if on_finished:
            worker.finished.connect(on_finished)

        thread.start()

    def _cleanup_thread(self, thread, worker):
        if hasattr(self, '_motor_threads') and thread in self._motor_threads:
            self._motor_threads.remove(thread)
        worker.deleteLater()
        thread.deleteLater()

    def _on_motor_error(self, error_msg: str):
        print(f"[Motor] 오류: {error_msg}")

    def _move_z(self, distance: float):
        self._start_motor_operation("z_move", distance=distance)

    def _home_z(self):
        self._start_motor_operation("z_home")

    def _move_x(self, distance: float, speed: int = 600):
        self._start_motor_operation("x_move", distance=distance, speed=speed)

    def _home_x(self):
        self._start_motor_operation("x_home")

    def _manual_y_move(self, distance: float):
        self._start_motor_operation("y_move", distance=distance)

    def _manual_y_home(self):
        self._start_motor_operation("y_home")

    # ==================== Setting 제어 ====================

    def _setting_led_on(self, power_percent: int):
        print(f"[Setting] LED ON 요청 ({power_percent}%) - DLP 없음, 무시")

    def _setting_led_off(self):
        print("[Setting] LED OFF 요청 - DLP 없음, 무시")

    def _setting_blade_home(self):
        self.motor.x_home()

    def _setting_blade_move(self):
        _, x_pos = self.motor.get_position()
        blade_speed_mms = self.setting_page.get_blade_speed()
        blade_speed = blade_speed_mms * 60

        if x_pos > 70:
            self.motor.x_move_absolute(0, blade_speed)
        else:
            self.motor.x_move_absolute(140, blade_speed)

    def _setting_y_move(self, distance: float):
        self._start_motor_operation("y_move", distance=distance)

    def _setting_y_home(self):
        self._start_motor_operation("y_home")

    def _setting_y_prime_start(self):
        self._start_motor_operation(
            "y_home",
            on_finished=self.setting_page.y_panel.on_homing_completed
        )

    def _setting_y_prime_done(self):
        self.motor.get_position()
        y_pos = self.motor._y_position
        self.settings.set_y_priming_position(y_pos)
        print(f"[Setting] Priming Done - Y: {y_pos}mm")

    def _on_led_power_changed(self, power: int):
        self.settings.set_led_power(power)

    def _on_blade_speed_changed(self, speed: int):
        self.settings.set_blade_speed(speed)

    # ==================== 프린트 테스트 ====================

    def _on_start_test(self, params: dict):
        """테스트 프린트 시작"""
        print(f"[Test] 프린트 테스트 시작: {params}")

        # Klipper Y 위치 조회
        self.motor.get_position()
        klipper_y = self.motor._y_position
        saved_pos = self.settings.get_y_priming_position()
        priming_pos = klipper_y if klipper_y > 0 else saved_pos

        if priming_pos <= 0:
            alert = SimpleAlert("셋팅페이지에서 프라이밍을 설정하세요.", self)
            alert.exec()
            return

        # 진행 페이지로 이동
        total_layers = params.get('totalLayer', 10)
        self.test_progress_page.start_progress(total_layers)
        self._go_to_page(self.PAGE_TEST_PROGRESS)

        # 워커 생성
        self.print_worker = TestPrintWorker(
            motor=self.motor,
            parent=self
        )
        self.print_worker.simulation = self.simulation

        # 시그널 연결
        self.print_worker.progress_updated.connect(self._on_progress)
        self.print_worker.print_completed.connect(self._on_completed)
        self.print_worker.print_stopped.connect(self._on_stopped)
        self.print_worker.error_occurred.connect(self._on_error)
        self.print_worker.resin_empty.connect(self._on_resin_empty)

        # 시작
        self.print_worker.start_print(
            params=params,
            blade_speed=params.get('bladeSpeed', 300),
            leveling_cycles=params.get('levelingCycles', 1),
            blade_cycles=params.get('bladeCycles', 1),
            y_dispense_distance=params.get('yDispenseDistance', 1.0),
            y_dispense_speed=params.get('yDispenseSpeed', 180),
            y_dispense_delay=params.get('yDispenseDelay', 2.0),
            y_priming_position=priming_pos,
        )

    def _on_progress(self, current: int, total: int):
        self.test_progress_page.update_progress(current, total)

    def _on_completed(self):
        print("[Test] 완료!")
        self._save_y_position()
        self.test_progress_page.show_completed()

    def _on_stopped(self):
        print("[Test] 정지됨")
        self._save_y_position()
        self.test_progress_page.show_stopped()

    def _on_error(self, message: str):
        print(f"[Test] 오류: {message}")
        self.test_progress_page.show_error(message)

    def _on_resin_empty(self):
        print("[Test] Resin empty")
        if self.print_worker:
            self.print_worker.disable_y_dispensing()

    def _save_y_position(self):
        self.motor.get_position()
        y_pos = self.motor._y_position
        self.settings.set_y_priming_position(y_pos)
        print(f"[Test] Y position saved: {y_pos}mm")

    def _on_pause(self):
        if self.print_worker and self.print_worker.isRunning():
            self.print_worker.pause()

    def _on_resume(self):
        if self.print_worker and self.print_worker.isRunning():
            self.print_worker.resume()

    def _on_stop(self):
        if self.print_worker and self.print_worker.isRunning():
            self.print_worker.stop()
        else:
            self.test_progress_page.show_stopped()

    def closeEvent(self, event):
        print("[System] Test VGUI 종료")
        if self.print_worker and self.print_worker.isRunning():
            self.print_worker.stop()
            self.print_worker.wait(3000)
        event.accept()


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Test VGUI - Motor Test')
    parser.add_argument('--no-sim', action='store_true', help='실제 하드웨어 모드')
    parser.add_argument('--sim', action='store_true', help='시뮬레이션 모드')
    args = parser.parse_args()

    simulation = SIMULATION_MODE
    if args.no_sim:
        simulation = False
    elif args.sim:
        simulation = True

    print("=" * 50)
    print("Test VGUI - Motor Test v1.0")
    print(f"Hardware: {'Simulation' if simulation else 'Real'}")
    print("=" * 50)

    app = QApplication(sys.argv)
    app.setStyleSheet(get_global_style())

    window = MainWindow(simulation=simulation)
    window.show()

    print("[System] Test VGUI 시작")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
