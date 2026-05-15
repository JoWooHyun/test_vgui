"""
VERICOM DLP 3D Printer - Motor Controller
Moonraker API를 통한 Z축/X축 모터 제어

실제 하드웨어 동작 코드 (dlp_simple_slideshow.py 기반)
"""

import requests
import time
from typing import Optional, Tuple
from dataclasses import dataclass


@dataclass
class MotorConfig:
    """모터 설정"""
    z_speed: int = 300          # Z축 이동 속도 (mm/min)
    x_speed: int = 300          # X축 이동 속도 (mm/min) - 리드스크류
    y_speed: int = 300          # Resin pump 이동 속도 (mm/min)
    x_min: float = 0.0          # X축 최소 위치 (mm)
    x_max: float = 140.0        # X축 최대 위치 (mm) - printer.cfg position_max
    z_min: float = 0.0          # Z축 최소 위치 (mm)
    z_max: float = 80.0         # Z축 최대 위치 (mm) - 실제 스펙
    y_min: float = 0.0          # Resin pump 최소 위치 (mm) - 홈 = resin empty
    y_max: float = 125.0        # Resin pump 최대 위치 (mm) - printer.cfg position_max
    drop_speed: int = 150       # Z축 하강 속도 (mm/min)


class MotorController:
    """
    Moonraker API를 통한 모터 제어 클래스

    Z축: 빌드 플레이트 상하 이동
    X축: 블레이드 수평 이동 (Top-Down DLP 특징)
    """

    def __init__(self, moonraker_url: str = "http://localhost:7125"):
        self.moonraker_url = moonraker_url.rstrip('/')
        self.config = MotorConfig()
        self._is_connected = False

        # 현재 위치 캐시
        self._z_position: float = 0.0
        self._x_position: float = 0.0
        self._y_position: float = 0.0

        # 홈잉 상태
        self._z_is_homed = False
        self._x_is_homed = False
        self._y_is_homed = False

        # 재시도 설정
        self._max_retries = 3
        self._retry_delay = 1.0  # 초

    # ==================== 연결 관리 ====================

    def connect(self) -> bool:
        """Moonraker 연결 확인"""
        try:
            response = requests.get(
                f"{self.moonraker_url}/printer/info",
                timeout=5
            )
            if response.status_code == 200:
                self._is_connected = True
                print("[Motor] Moonraker 연결됨")
                return True
        except requests.exceptions.RequestException as e:
            print(f"[Motor] 연결 실패: {e}")

        self._is_connected = False
        return False

    @property
    def is_connected(self) -> bool:
        return self._is_connected

    # ==================== G-code 전송 ====================

    def _ensure_connected(self) -> bool:
        """연결 상태 확인 및 필요시 재연결"""
        if self._is_connected:
            # 연결 상태 검증 (빠른 ping)
            try:
                response = requests.get(
                    f"{self.moonraker_url}/printer/info",
                    timeout=3
                )
                if response.status_code == 200:
                    return True
            except:
                pass

            # 연결 끊김 감지
            print("[Motor] 연결 끊김 감지 - 재연결 시도")
            self._is_connected = False

        # 재연결 시도
        return self.connect()

    def send_gcode(self, gcode: str, timeout: Optional[int] = None) -> bool:
        """
        G-code 명령 전송 (자동 재연결 및 재시도 포함)

        Args:
            gcode: G-code 문자열 (여러 줄 가능)
            timeout: 타임아웃 (초), None이면 명령에 따라 자동 결정

        Returns:
            성공 여부
        """
        # 타임아웃 자동 결정
        if timeout is None:
            if "G0" in gcode and "X" in gcode:
                timeout = 300  # X축 이동: 5분
            elif "G1" in gcode and "X" in gcode:
                timeout = 300
            elif "G1" in gcode and "Y" in gcode:
                timeout = 120  # Y축 이동: 2분
            elif "G28" in gcode:
                timeout = 120  # 홈잉: 120초
            elif "M400" in gcode:
                timeout = 300  # M400 대기: 5분
            else:
                timeout = 60   # 기본: 1분

        # 재시도 루프
        for attempt in range(self._max_retries):
            # 연결 확인
            if not self._ensure_connected():
                print(f"[Motor] 연결 실패 (시도 {attempt + 1}/{self._max_retries})")
                if attempt < self._max_retries - 1:
                    time.sleep(self._retry_delay)
                continue

            try:
                url = f"{self.moonraker_url}/printer/gcode/script"
                response = requests.post(
                    url,
                    json={"script": gcode},
                    timeout=timeout
                )

                if response.status_code == 200:
                    print(f"[Motor] G-code 전송: {gcode.replace(chr(10), ' | ')} (timeout={timeout}s)")
                    return True
                else:
                    print(f"[Motor] G-code 실패: {response.status_code}")
                    # 4xx 에러는 재시도 의미 없음
                    if 400 <= response.status_code < 500:
                        return False

            except requests.exceptions.ConnectionError as e:
                print(f"[Motor] 연결 오류 (시도 {attempt + 1}/{self._max_retries}): {e}")
                self._is_connected = False
            except requests.exceptions.Timeout as e:
                print(f"[Motor] 타임아웃 (시도 {attempt + 1}/{self._max_retries}): {e}")
            except requests.exceptions.RequestException as e:
                print(f"[Motor] G-code 전송 오류 (시도 {attempt + 1}/{self._max_retries}): {e}")

            # 재시도 전 대기
            if attempt < self._max_retries - 1:
                time.sleep(self._retry_delay)

        print(f"[Motor] G-code 전송 최종 실패: {gcode.replace(chr(10), ' | ')}")
        return False

    def wait_for_movement_complete(self, timeout: int = 300) -> bool:
        """모든 모터 움직임 완료 대기 (M400)"""
        print("[Motor] 모터 움직임 완료 대기 중...")

        for attempt in range(3):
            print(f"[Motor] M400 시도 {attempt + 1}/3")
            success = self.send_gcode("M400", timeout=timeout)
            if success:
                print("[Motor] M400 명령 전송 완료")
                time.sleep(0.5)
                print("[Motor] 모터 움직임 완전 완료")
                return True
            else:
                print(f"[Motor] M400 시도 {attempt + 1} 실패")
                time.sleep(1.0)

        print("[Motor] M400 명령 모든 시도 실패 - 고정 대기시간 사용")
        time.sleep(2.0)
        return False

    def wait_for_settle(self, wait_time_ms: int = 500) -> bool:
        """안정화 대기 (G4)"""
        if wait_time_ms > 0:
            return self.send_gcode(f"G4 P{wait_time_ms}", timeout=60)
        return True

    # ==================== Z축 제어 ====================

    def z_home(self) -> bool:
        """Z축 홈으로 이동"""
        print("[Motor] Z축 홈 이동 시작")
        success = self.send_gcode("G28 Z", timeout=120)
        if success:
            self._z_position = 0.0
            self._z_is_homed = True
            self.wait_for_movement_complete(timeout=120)
            print("[Motor] Z축 홈 이동 완료")
        return success

    def z_move_relative(self, distance: float, speed: Optional[int] = None) -> bool:
        """
        Z축 상대 이동

        Args:
            distance: 이동 거리 (양수: 위로, 음수: 아래로)
            speed: 이동 속도 (mm/min), None이면 기본값
        """
        speed = speed or self.config.z_speed

        # 목표 위치 계산 및 제한
        target_position = self._z_position + distance
        target_position = max(self.config.z_min, min(target_position, self.config.z_max))
        actual_distance = target_position - self._z_position

        if actual_distance == 0:
            print(f"[Motor] Z축 이미 한계 위치 ({self._z_position:.1f}mm) - 이동 생략")
            return True

        if abs(actual_distance) != abs(distance):
            print(f"[Motor] Z축 이동 제한: {distance}mm → {actual_distance:.1f}mm (범위: {self.config.z_min}~{self.config.z_max}mm)")

        gcode = f"G91\nG1 Z{actual_distance} F{speed}\nG90"
        print(f"[Motor] Z축 상대 이동: {actual_distance:.1f}mm @ {speed}mm/min")
        success = self.send_gcode(gcode)
        if success:
            self._z_position = target_position
            self.wait_for_movement_complete(timeout=120)
        return success

    def z_move_absolute(self, position: float, speed: Optional[int] = None) -> bool:
        """
        Z축 절대 위치로 이동

        Args:
            position: 목표 위치 (mm)
            speed: 이동 속도 (mm/min)
        """
        speed = speed or self.config.z_speed

        # 위치 제한
        original_position = position
        position = max(self.config.z_min, min(position, self.config.z_max))

        if position != original_position:
            print(f"[Motor] Z축 위치 제한: {original_position:.1f}mm → {position:.1f}mm (범위: {self.config.z_min}~{self.config.z_max}mm)")

        gcode = f"G90\nG0 Z{position:.3f} F{speed}"
        print(f"[Motor] Z축 절대 이동: {position:.3f}mm @ {speed}mm/min")
        success = self.send_gcode(gcode)
        if success:
            self._z_position = position
            self.wait_for_movement_complete(timeout=120)
            print(f"[Motor] Z축 절대 이동 완료: 현재 위치 {self._z_position:.3f}mm")
        return success

    def z_up(self, distance: float) -> bool:
        """Z축 위로 이동 (빌드 플레이트 상승)"""
        return self.z_move_relative(abs(distance))

    def z_down(self, distance: float) -> bool:
        """Z축 아래로 이동 (빌드 플레이트 하강)"""
        return self.z_move_relative(-abs(distance))

    # ==================== X축 (블레이드) 제어 ====================

    def x_home(self, force: bool = False) -> bool:
        """
        X축 홈으로 이동 (블레이드 원점)

        Args:
            force: (미사용) 항상 실제 홈잉 수행
        """
        print("[Motor] X축 홈 이동 시작")
        success = self.send_gcode("G28 X", timeout=120)
        if success:
            self._x_position = 0.0
            self._x_is_homed = True
            self.wait_for_movement_complete(timeout=120)
            print("[Motor] X축 홈 이동 완료")
        return success

    def x_move_relative(self, distance: float, speed: Optional[int] = None) -> bool:
        """
        X축 상대 이동

        Args:
            distance: 이동 거리 (양수: 오른쪽, 음수: 왼쪽)
            speed: 이동 속도 (mm/min)
        """
        speed = speed or self.config.x_speed

        # 목표 위치 계산 및 제한
        target_position = self._x_position + distance
        target_position = max(self.config.x_min, min(target_position, self.config.x_max))
        actual_distance = target_position - self._x_position

        if actual_distance == 0:
            print(f"[Motor] X축 이미 한계 위치 ({self._x_position:.1f}mm) - 이동 생략")
            return True

        if abs(actual_distance) != abs(distance):
            print(f"[Motor] X축 이동 제한: {distance}mm → {actual_distance:.1f}mm (범위: {self.config.x_min}~{self.config.x_max}mm)")

        gcode = f"G91\nG0 X{actual_distance} F{speed}\nG90"
        print(f"[Motor] X축 상대 이동: {actual_distance:.1f}mm @ {speed}mm/min")
        success = self.send_gcode(gcode, timeout=300)
        if success:
            self._x_position = target_position
            # 상대 이동 후에는 홈 상태를 알 수 없음 (절대 좌표 이동 전 홈잉 필요)
            self._x_is_homed = False
            self.wait_for_movement_complete(timeout=300)
        return success

    def x_move_absolute(self, position: float, speed: Optional[int] = None) -> bool:
        """
        X축 절대 위치로 이동

        Args:
            position: 목표 위치 (mm), 0~125
            speed: 이동 속도 (mm/min)
        """
        speed = speed or self.config.x_speed

        # 위치 제한
        original_position = position
        position = max(self.config.x_min, min(position, self.config.x_max))

        if position != original_position:
            print(f"[Motor] X축 위치 제한: {original_position:.1f}mm → {position:.1f}mm (범위: {self.config.x_min}~{self.config.x_max}mm)")

        # 예상 시간 계산
        distance = abs(position - self._x_position)
        expected_time = (distance / speed) * 60

        print(f"[Motor] X축 {position:.1f}mm 위치로 이동 시작")
        print(f"[Motor] 이동 거리: {distance:.1f}mm, 예상 소요시간: {expected_time:.1f}초")

        # 이동 명령 전송 (G90 절대좌표 + G1 이동)
        gcode = f"G90\nG1 X{position:.1f} F{speed}"
        print(f"[Motor] X축 G-code: {gcode.replace(chr(10), ' | ')}")
        success = self.send_gcode(gcode, timeout=300)

        if not success:
            # 절대 이동 실패 시 상대 이동으로 대체 시도
            print("[Motor] X축 절대 이동 실패 - 상대 이동으로 대체 시도")
            relative_distance = position - self._x_position
            gcode = f"G91\nG1 X{relative_distance:.1f} F{speed}\nG90"
            success = self.send_gcode(gcode, timeout=300)

        if success:
            self._x_position = position
            print(f"[Motor] X축 이동 명령 전송 성공: {self._x_position:.1f}mm")

            # 움직임 완료까지 대기
            print("[Motor] X축 이동 완료 대기 중...")
            move_complete = self.wait_for_movement_complete(timeout=300)

            if move_complete:
                print(f"[Motor] ✅ X축 {position:.1f}mm 이동 완전 완료!")
                return True
            else:
                print("[Motor] ⚠️ X축 이동 완료 신호 실패, 추가 대기")
                time.sleep(expected_time)
                print("[Motor] X축 이동 강제 완료 처리")
                return True
        else:
            print("[Motor] ❌ X축 이동 명령 전송 실패")
            return False

    def x_to_end(self, speed: Optional[int] = None) -> bool:
        """X축 끝점(125mm)으로 이동"""
        return self.x_move_absolute(self.config.x_max, speed)

    def x_to_home(self, speed: Optional[int] = None) -> bool:
        """X축 홈(0mm)으로 이동 (G0 이동, G28 아님)"""
        return self.x_move_absolute(0, speed)

    # ==================== Resin Pump 제어 ====================

    def y_reset_position(self) -> bool:
        """Resin pump 위치를 0으로 리셋"""
        print("[Motor] Resin pump position reset (SET_KINEMATIC_POSITION Y=0)")
        success = self.send_gcode("SET_KINEMATIC_POSITION Y=0", timeout=10)
        if success:
            self._y_position = 0.0
            print("[Motor] Resin pump position reset complete")
        return success

    def y_home(self) -> bool:
        """Resin pump 홈으로 이동"""
        print("[Motor] Resin pump homing...")
        success = self.send_gcode("G28 Y", timeout=120)
        if success:
            self._y_position = 0.0
            self._y_is_homed = True
            self.wait_for_movement_complete(timeout=120)
            print("[Motor] Resin pump homing complete")
        return success

    def y_move_relative(self, distance: float, speed: Optional[int] = None) -> bool:
        """
        Resin pump 상대 이동

        Args:
            distance: 이동 거리 (양수: 홈 반대방향, 음수: 홈 방향=토출)
            speed: 이동 속도 (mm/min), None이면 기본값
        """
        speed = speed or self.config.y_speed

        # 목표 위치 계산 및 제한
        target_position = self._y_position + distance
        target_position = max(self.config.y_min, min(target_position, self.config.y_max))
        actual_distance = target_position - self._y_position

        if actual_distance == 0:
            print(f"[Motor] Resin pump at limit ({self._y_position:.1f}mm) - skip")
            return True

        if abs(actual_distance) != abs(distance):
            print(f"[Motor] Resin pump clamped: {distance}mm → {actual_distance:.1f}mm (range: {self.config.y_min}~{self.config.y_max}mm)")

        gcode = f"G91\nG1 Y{actual_distance} F{speed}\nG90"
        print(f"[Motor] Resin pump move: {actual_distance:.1f}mm @ {speed}mm/min")
        success = self.send_gcode(gcode)
        if success:
            self._y_position = target_position
            self.wait_for_movement_complete(timeout=120)
        return success

    # ==================== 복합 동작 ====================

    def home_all(self) -> bool:
        """모든 축 홈으로 이동"""
        print("[Motor] 모든 축 홈 이동")
        return self.send_gcode("G28", timeout=100)

    def emergency_stop(self) -> bool:
        """
        비상 정지 (Klipper 셧다운)
        주의: 이 명령은 Klipper를 완전히 종료시킵니다.
        일반적인 정지에는 quickstop()을 사용하세요.
        """
        print("[Motor] 비상 정지! (Klipper 셧다운)")
        try:
            response = requests.post(
                f"{self.moonraker_url}/printer/emergency_stop",
                timeout=5
            )
            return response.status_code == 200
        except:
            return False

    def quickstop(self) -> bool:
        """
        현재 동작만 취소 (Klipper 유지)
        M410: Quickstop - 현재 이동을 즉시 취소하고 Klipper는 계속 실행
        """
        print("[Motor] Quickstop - 현재 동작 취소")
        return self.send_gcode("M410", timeout=5)

    def klipper_pause(self) -> bool:
        """Klipper에 일시정지 알림 (idle timeout 방지)"""
        print("[Motor] Klipper PAUSE")
        try:
            response = requests.post(
                f"{self.moonraker_url}/printer/gcode/script",
                json={"script": "PAUSE"},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def klipper_resume(self) -> bool:
        """Klipper에 재개 알림"""
        print("[Motor] Klipper RESUME")
        try:
            response = requests.post(
                f"{self.moonraker_url}/printer/gcode/script",
                json={"script": "RESUME"},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def klipper_cancel(self) -> bool:
        """Klipper에 프린트 취소 알림"""
        print("[Motor] Klipper CANCEL_PRINT")
        try:
            response = requests.post(
                f"{self.moonraker_url}/printer/gcode/script",
                json={"script": "CANCEL_PRINT"},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def klipper_clear_pause(self) -> bool:
        """Klipper 일시정지 상태 초기화 (새 프린트 시작 전 호출)"""
        print("[Motor] Klipper CLEAR_PAUSE")
        try:
            response = requests.post(
                f"{self.moonraker_url}/printer/gcode/script",
                json={"script": "CLEAR_PAUSE"},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def leveling_cycle(self, cycles: int = 1, speed: Optional[int] = None) -> bool:
        """
        레진 평탄화 사이클 (Z축은 이미 0.1mm 위치에 있다고 가정)

        Args:
            cycles: 왕복 횟수
            speed: 블레이드 속도

        Flow:
            1. X축 140 → 0 → 140 왕복 (N회)
            2. Z축 홈 복귀
        """
        if cycles <= 0:
            return True

        speed = speed or self.config.x_speed
        print("=" * 40)
        print(f"[Motor] 레진 평탄화 작업 시작 (왕복 {cycles}회)")
        print("=" * 40)

        # 1. X축 블레이드 왕복 동작
        for cycle in range(cycles):
            print(f"\n[Motor] --- 평탄화 {cycle + 1}/{cycles}회 ---")

            print("[Motor] X축 0mm → 140mm 이동")
            if not self.x_move_absolute(140, speed):
                print("[Motor] X축 140mm 이동 실패 - 평탄화 중단")
                return False

            time.sleep(0.2)

            print("[Motor] X축 140mm → 0mm 이동")
            if not self.x_move_absolute(0, speed):
                print("[Motor] X축 0mm 이동 실패 - 평탄화 중단")
                return False

            time.sleep(0.2)
            print(f"[Motor] 평탄화 {cycle + 1}회 완료")

        # 2. Z축 홈으로 복귀
        print("[Motor] Z축 홈으로 복귀")
        if not self.z_home():
            print("[Motor] Z축 홈 복귀 실패")
            return False
        print("[Motor] Z축 홈 복귀 완료")

        print("=" * 40)
        print("[Motor] 레진 평탄화 작업 완료")
        print("=" * 40)
        return True

    # ==================== 상태 조회 ====================

    def get_position(self) -> Tuple[float, float]:
        """
        현재 위치 조회

        Returns:
            (z_position, x_position)
        """
        try:
            response = requests.get(
                f"{self.moonraker_url}/printer/objects/query",
                params={"toolhead": "position"},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                pos = data.get('result', {}).get('status', {}).get('toolhead', {}).get('position', [0, 0, 0, 0])
                self._x_position = pos[0] if len(pos) > 0 else 0
                self._y_position = pos[1] if len(pos) > 1 else 0
                self._z_position = pos[2] if len(pos) > 2 else 0
        except:
            pass

        return (self._z_position, self._x_position)

    def get_printer_state(self) -> str:
        """프린터 상태 조회 (ready, printing, paused, error 등)"""
        try:
            response = requests.get(
                f"{self.moonraker_url}/printer/objects/query",
                params={"print_stats": "state"},
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                return data.get('result', {}).get('status', {}).get('print_stats', {}).get('state', 'unknown')
        except:
            pass
        return 'unknown'

    def get_klipper_state(self) -> str:
        """Klipper 자체 상태 조회 (ready, shutdown, error, startup 등)"""
        try:
            response = requests.get(
                f"{self.moonraker_url}/printer/info",
                timeout=5
            )
            if response.status_code == 200:
                data = response.json()
                state = data.get('result', {}).get('state', 'unknown')
                print(f"[Motor] Klipper 상태: {state}")
                return state
        except:
            pass
        return 'unknown'

    def firmware_restart(self) -> bool:
        """Klipper 펌웨어 재시작 (shutdown 복구용)"""
        print("[Motor] Klipper FIRMWARE_RESTART")
        try:
            response = requests.post(
                f"{self.moonraker_url}/printer/firmware_restart",
                timeout=30
            )
            if response.status_code == 200:
                # 재시작 후 ready 상태가 될 때까지 대기
                for _ in range(30):  # 최대 15초 대기
                    time.sleep(0.5)
                    state = self.get_klipper_state()
                    if state == "ready":
                        print("[Motor] Klipper 재시작 완료 (ready)")
                        return True
                print("[Motor] Klipper 재시작 타임아웃")
                return False
            return False
        except:
            return False


# 테스트용
if __name__ == "__main__":
    motor = MotorController("http://localhost:7125")

    if motor.connect():
        print("연결 성공!")
        z, x = motor.get_position()
        print(f"현재 위치: Z={z}mm, X={x}mm")
    else:
        print("연결 실패 - Moonraker가 실행 중인지 확인하세요")
