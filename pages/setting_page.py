"""
VERICOM DLP 3D Printer GUI - Setting Page
LED Power 및 Blade 설정 페이지
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QDialog
)
from PySide6.QtCore import Signal, Qt

from pages.base_page import BasePage
from components.numeric_keypad import NumericKeypad
from components.icon_button import ControlButton, HomeButton

from styles.colors import Colors
from styles.fonts import Fonts
from styles.icons import Icons
from styles.stylesheets import (
    get_axis_panel_style, get_axis_title_style,
    get_distance_button_active_style, Radius
)


class LEDPowerPanel(QFrame):
    """LED Power 설정 패널"""

    power_changed = Signal(int)  # 파워 값 변경
    led_on = Signal(int)         # LED ON (파워 값 전달)
    led_off = Signal()           # LED OFF

    def __init__(self, parent=None):
        super().__init__(parent)

        self._power_value = 43   # 기본값 43% (440/1023 올림)
        self._is_on = False
        self._min_power = 9     # 최소 9% (91/1023 올림)
        self._max_power = 100   # 최대 100% (1023)

        self._setup_ui()

    def _setup_ui(self):
        """UI 구성"""
        self.setStyleSheet(get_axis_panel_style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # 타이틀 (border 없음)
        self.title_label = QLabel("LED SET")
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.NAVY};
                font-size: 18px;
                font-weight: 700;
                background-color: transparent;
                border: none;
            }}
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        layout.addStretch(3)

        # Power 라벨
        power_label = QLabel("Power")
        power_label.setAlignment(Qt.AlignCenter)
        power_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 14px;
                background-color: transparent;
                border: none;
            }}
        """)
        layout.addWidget(power_label)

        # 파워 값 표시 (클릭 가능)
        self.power_btn = QPushButton(f"{self._power_value}%")
        self.power_btn.setFixedSize(200, 80)
        self.power_btn.setCursor(Qt.PointingHandCursor)
        self.power_btn.setFont(Fonts.mono_display())
        self._update_power_btn_style()
        self.power_btn.clicked.connect(self._on_power_click)

        power_container = QHBoxLayout()
        power_container.addStretch()
        power_container.addWidget(self.power_btn)
        power_container.addStretch()
        layout.addLayout(power_container)

        layout.addStretch(3)

        # ON/OFF 토글 버튼
        self.btn_toggle = QPushButton("ON")
        self.btn_toggle.setFixedHeight(44)
        self.btn_toggle.setCursor(Qt.PointingHandCursor)
        self.btn_toggle.setFont(Fonts.h3())
        self.btn_toggle.clicked.connect(self._on_toggle_click)
        self._update_toggle_style()
        layout.addWidget(self.btn_toggle)

    def _update_power_btn_style(self):
        """파워 버튼 스타일 업데이트"""
        self.power_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_SECONDARY};
                border: 2px solid {Colors.CYAN};
                border-radius: {Radius.LG}px;
                color: {Colors.NAVY};
                font-size: 36px;
                font-weight: 700;
            }}
            QPushButton:pressed {{
                background-color: {Colors.BG_TERTIARY};
            }}
        """)

    def _update_toggle_style(self):
        """토글 버튼 스타일 업데이트"""
        if self._is_on:
            # LED가 켜진 상태 → OFF 버튼 (빨간색)
            self.btn_toggle.setText("OFF")
            self.btn_toggle.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.RED};
                    border: none;
                    border-radius: {Radius.MD}px;
                    color: {Colors.WHITE};
                    font-weight: 600;
                }}
                QPushButton:pressed {{
                    background-color: #B91C1C;
                }}
            """)
        else:
            # LED가 꺼진 상태 → ON 버튼 (흰 배경 + 테두리)
            self.btn_toggle.setText("ON")
            self.btn_toggle.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.BG_PRIMARY};
                    border: 2px solid {Colors.BORDER};
                    border-radius: {Radius.MD}px;
                    color: {Colors.TEXT_PRIMARY};
                    font-weight: 600;
                }}
                QPushButton:pressed {{
                    background-color: {Colors.BG_SECONDARY};
                }}
            """)

    def _on_power_click(self):
        """파워 값 클릭 - 키패드 열기"""
        keypad = NumericKeypad(
            title="LED Power",
            value=self._power_value,
            unit="%",
            min_val=self._min_power,
            max_val=self._max_power,
            allow_decimal=False,
            parent=self.window()
        )
        keypad.value_confirmed.connect(self._on_power_confirmed)
        keypad.exec()

    def _on_power_confirmed(self, value: float):
        """파워 값 확정"""
        self._power_value = int(value)
        self.power_btn.setText(f"{self._power_value}%")
        self.power_changed.emit(self._power_value)

    def _on_toggle_click(self):
        """ON/OFF 토글"""
        if self._is_on:
            # 현재 켜진 상태 → 끄기
            self._is_on = False
            self.led_off.emit()
        else:
            # 현재 꺼진 상태 → 켜기
            self._is_on = True
            self.led_on.emit(self._power_value)
        self._update_toggle_style()

    def get_power(self) -> int:
        """현재 파워 값 반환"""
        return self._power_value

    def set_power(self, value: int):
        """파워 값 설정"""
        self._power_value = max(self._min_power, min(self._max_power, value))
        self.power_btn.setText(f"{self._power_value}%")


class BladePanel(QFrame):
    """Blade 설정 패널"""

    speed_changed = Signal(int)    # 속도 변경
    blade_move = Signal()          # MOVE 버튼 클릭
    home_axis = Signal()           # 홈 이동

    def __init__(self, parent=None):
        super().__init__(parent)

        self._speed_value = 5   # 기본값 5 mm/s (리드스크류)
        self._min_speed = 1     # 최소 1 mm/s
        self._max_speed = 100   # 최대 100 mm/s

        self._setup_ui()

    def _setup_ui(self):
        """UI 구성"""
        self.setStyleSheet(get_axis_panel_style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        # 타이틀 (border 없음)
        self.title_label = QLabel("BLADE SET")
        self.title_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.NAVY};
                font-size: 18px;
                font-weight: 700;
                background-color: transparent;
                border: none;
            }}
        """)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        layout.addStretch(3)

        # Speed 라벨
        speed_label = QLabel("Speed")
        speed_label.setAlignment(Qt.AlignCenter)
        speed_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 14px;
                background-color: transparent;
                border: none;
            }}
        """)
        layout.addWidget(speed_label)

        # 속도 값 표시 (클릭 가능)
        self.speed_btn = QPushButton(f"{self._speed_value} mm/s")
        self.speed_btn.setFixedSize(200, 80)
        self.speed_btn.setCursor(Qt.PointingHandCursor)
        self.speed_btn.setFont(Fonts.mono_display())
        self._update_speed_btn_style()
        self.speed_btn.clicked.connect(self._on_speed_click)

        speed_container = QHBoxLayout()
        speed_container.addStretch()
        speed_container.addWidget(self.speed_btn)
        speed_container.addStretch()
        layout.addLayout(speed_container)

        layout.addStretch(3)

        # 제어 버튼들 (HOME, MOVE)
        control_layout = QHBoxLayout()
        control_layout.setSpacing(8)

        self.btn_home = QPushButton("HOME")
        self.btn_home.setFixedHeight(44)
        self.btn_home.setCursor(Qt.PointingHandCursor)
        self.btn_home.setFont(Fonts.h3())
        self.btn_home.setStyleSheet(self._get_action_btn_style())
        self.btn_home.clicked.connect(self.home_axis.emit)

        self.btn_move = QPushButton("MOVE")
        self.btn_move.setFixedHeight(44)
        self.btn_move.setCursor(Qt.PointingHandCursor)
        self.btn_move.setFont(Fonts.h3())
        self.btn_move.setStyleSheet(self._get_action_btn_style())
        self.btn_move.clicked.connect(self.blade_move.emit)

        control_layout.addWidget(self.btn_home)
        control_layout.addWidget(self.btn_move)

        layout.addLayout(control_layout)

    def _update_speed_btn_style(self):
        """속도 버튼 스타일 업데이트"""
        self.speed_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_SECONDARY};
                border: 2px solid {Colors.CYAN};
                border-radius: {Radius.LG}px;
                color: {Colors.NAVY};
                font-size: 28px;
                font-weight: 700;
            }}
            QPushButton:pressed {{
                background-color: {Colors.BG_TERTIARY};
            }}
        """)

    def _get_action_btn_style(self):
        """액션 버튼 스타일 반환"""
        return f"""
            QPushButton {{
                background-color: {Colors.BG_SECONDARY};
                border: 2px solid {Colors.BORDER};
                border-radius: {Radius.MD}px;
                color: {Colors.TEXT_PRIMARY};
                font-weight: 600;
            }}
            QPushButton:pressed {{
                background-color: {Colors.BG_TERTIARY};
            }}
        """

    def _on_speed_click(self):
        """속도 값 클릭 - 키패드 열기"""
        keypad = NumericKeypad(
            title="Blade Speed",
            value=self._speed_value,
            unit="mm/s",
            min_val=self._min_speed,
            max_val=self._max_speed,
            allow_decimal=False,
            parent=self.window()
        )
        keypad.value_confirmed.connect(self._on_speed_confirmed)
        keypad.exec()

    def _on_speed_confirmed(self, value: float):
        """속도 값 확정"""
        self._speed_value = int(value)
        self.speed_btn.setText(f"{self._speed_value} mm/s")
        self.speed_changed.emit(self._speed_value)

    def get_speed(self) -> int:
        """현재 속도 값 반환"""
        return self._speed_value

    def set_speed(self, value: int):
        """속도 값 설정"""
        self._speed_value = max(self._min_speed, min(self._max_speed, value))
        self.speed_btn.setText(f"{self._speed_value} mm/s")


class YAxisPanel(QFrame):
    """Resin 프라이밍 패널

    플로우:
    1. PRIME 클릭 → G28 Y 홈잉 (빈 상태, 주사기 없이) → Y=0 절대 좌표 확보
    2. 주사기 장착 → 양방향 이동으로 플런저 위치 맞춤 + 레진 토출 확인
    3. OK 클릭 → 현재 위치 저장 (홈 기준 절대 좌표)

    출력 시: 저장된 위치에서 -방향(홈 방향)으로 토출
    → Y=0 도달 시 Klipper position_min이 이동 거부 → 레진 소진
    """

    move_positive = Signal(float)  # 홈 반대방향 (전진, +)
    move_negative = Signal(float)  # 홈 방향 (후진, -)
    home_axis = Signal()           # 홈 이동
    priming_started = Signal()     # 프라이밍 시작 (G28 Y 홈잉 요청)
    priming_done = Signal()        # 프라이밍 완료 (좌표 저장 요청)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_priming = False   # 프라이밍 모드 여부
        self._setup_ui()

    def _setup_ui(self):
        """UI 구성"""
        self.setStyleSheet(get_axis_panel_style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)

        layout.addStretch(1)

        # 타이틀
        self.title_label = QLabel("PRIMING")
        self.title_label.setStyleSheet(get_axis_title_style())
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        # 상태 라벨
        self.status_label = QLabel("")
        self.status_label.setStyleSheet(f"""
            QLabel {{
                color: {Colors.TEXT_SECONDARY};
                font-size: 12px;
                background-color: transparent;
                border: none;
            }}
        """)
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        layout.addStretch(1)

        # 거리 입력 버튼 (클릭하면 NumericKeypad 열림)
        self._distance = 1.0
        self.btn_distance = QPushButton("1 mm")
        self.btn_distance.setFixedHeight(44)
        self.btn_distance.setCursor(Qt.PointingHandCursor)
        self.btn_distance.setStyleSheet(get_distance_button_active_style())
        self.btn_distance.clicked.connect(self._on_distance_click)
        self.btn_distance.setEnabled(False)  # 프라이밍 모드에서만 활성화
        layout.addWidget(self.btn_distance)

        layout.addStretch(1)

        # 이동 버튼들 (UP, DOWN) - 프라이밍 모드에서만 활성화
        move_layout = QHBoxLayout()
        move_layout.setSpacing(12)
        move_layout.setAlignment(Qt.AlignCenter)

        self.btn_up = ControlButton(Icons.CHEVRON_UP, 70, 28)
        self.btn_up.clicked.connect(self._on_move_up)
        self.btn_up.setEnabled(False)

        self.btn_down = ControlButton(Icons.CHEVRON_DOWN, 70, 28)
        self.btn_down.clicked.connect(self._on_move_down)
        self.btn_down.setEnabled(False)

        move_layout.addWidget(self.btn_up)
        move_layout.addWidget(self.btn_down)
        layout.addLayout(move_layout)

        layout.addStretch(1)

        # PRIME / OK 버튼
        action_layout = QHBoxLayout()
        action_layout.setSpacing(8)

        self.btn_prime = QPushButton("PRIME")
        self.btn_prime.setFixedHeight(44)
        self.btn_prime.setCursor(Qt.PointingHandCursor)
        self.btn_prime.setFont(Fonts.h3())
        self.btn_prime.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_SECONDARY};
                border: 2px solid {Colors.BORDER};
                border-radius: {Radius.MD}px;
                color: {Colors.TEXT_PRIMARY};
                font-weight: 600;
            }}
            QPushButton:pressed {{
                background-color: {Colors.BG_TERTIARY};
            }}
        """)
        self.btn_prime.clicked.connect(self._on_prime_click)

        self.btn_ok = QPushButton("OK")
        self.btn_ok.setFixedHeight(44)
        self.btn_ok.setCursor(Qt.PointingHandCursor)
        self.btn_ok.setFont(Fonts.h3())
        self.btn_ok.setEnabled(False)
        self._update_ok_style()
        self.btn_ok.clicked.connect(self._on_ok_click)

        action_layout.addWidget(self.btn_prime)
        action_layout.addWidget(self.btn_ok)
        layout.addLayout(action_layout)

    def _update_ok_style(self):
        """OK 버튼 스타일 (활성/비활성)"""
        if self.btn_ok.isEnabled():
            self.btn_ok.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.CYAN};
                    border: none;
                    border-radius: {Radius.MD}px;
                    color: {Colors.WHITE};
                    font-weight: 600;
                }}
                QPushButton:pressed {{
                    background-color: #0891B2;
                }}
            """)
        else:
            self.btn_ok.setStyleSheet(f"""
                QPushButton {{
                    background-color: {Colors.BG_TERTIARY};
                    border: 2px solid {Colors.BORDER};
                    border-radius: {Radius.MD}px;
                    color: {Colors.TEXT_DISABLED};
                    font-weight: 600;
                }}
            """)

    def _on_prime_click(self):
        """PRIME 버튼 클릭 → G28 Y 홈잉 시작 (빈 상태에서 0점 확보)"""
        self._is_priming = True
        self.btn_prime.setEnabled(False)
        self.status_label.setText("Homing resin pump...")
        self.priming_started.emit()  # main.py에서 G28 Y 실행

    def on_homing_completed(self):
        """G28 Y 홈잉 완료 후 호출 (main.py에서 호출)

        홈잉 완료 → 주사기 장착 → 양방향 이동 가능"""
        self.status_label.setText("Mount syringe, adjust & test, then OK")
        self.btn_distance.setEnabled(True)
        self.btn_up.setEnabled(True)   # + 방향 (홈에서 멀어짐)
        self.btn_down.setEnabled(True)  # - 방향 (홈 쪽으로)
        self.btn_ok.setEnabled(True)
        self._update_ok_style()

    def _on_ok_click(self):
        """OK 버튼 클릭 → 프라이밍 완료, 좌표 저장 요청"""
        self._is_priming = False
        self.status_label.setText("Priming saved!")
        self.btn_distance.setEnabled(False)
        self.btn_up.setEnabled(False)
        self.btn_down.setEnabled(False)
        self.btn_ok.setEnabled(False)
        self.btn_prime.setEnabled(True)
        self._update_ok_style()
        self.priming_done.emit()

    def _on_distance_click(self):
        """거리 버튼 클릭 → NumericKeypad 열기"""
        keypad = NumericKeypad(
            title="Move Distance",
            value=self._distance,
            unit="mm",
            min_val=0.05,
            max_val=100.0,
            allow_decimal=True,
            parent=self.window()
        )
        if keypad.exec() == QDialog.Accepted:
            self._distance = keypad.get_value()
            if self._distance == int(self._distance):
                self.btn_distance.setText(f"{int(self._distance)} mm")
            else:
                self.btn_distance.setText(f"{self._distance:g} mm")

    def _on_move_up(self):
        """위로 이동 (홈 반대방향 = 양의 방향, 주사기 빼기)"""
        self.move_positive.emit(self._distance)

    def _on_move_down(self):
        """아래로 이동 (홈 방향 = 음의 방향, 레진 토출)"""
        self.move_negative.emit(self._distance)


class SettingPage(BasePage):
    """설정 페이지 (LED Power + Blade + Resin)"""

    # LED 시그널
    led_power_changed = Signal(int)
    led_on = Signal(int)  # 파워 값 전달
    led_off = Signal()

    # Blade 시그널
    blade_speed_changed = Signal(int)
    blade_move = Signal()  # MOVE 버튼 클릭
    blade_home = Signal()

    # Resin 시그널
    y_move = Signal(float)    # Resin pump 이동 (거리)
    y_home = Signal()         # Resin pump 홈
    y_prime_start = Signal()  # 프라이밍 시작 (홈 요청)
    y_prime_done = Signal()   # 프라이밍 완료 (좌표 저장 요청)

    def __init__(self, parent=None):
        super().__init__("Setting", show_back=True, parent=parent)
        self._setup_content()

    def _setup_content(self):
        """콘텐츠 구성"""
        # 3열 레이아웃
        panels_layout = QHBoxLayout()
        panels_layout.setSpacing(20)

        # LED Power 패널
        self.led_panel = LEDPowerPanel()
        self.led_panel.power_changed.connect(self.led_power_changed.emit)
        self.led_panel.led_on.connect(self.led_on.emit)
        self.led_panel.led_off.connect(self.led_off.emit)

        # Blade 패널
        self.blade_panel = BladePanel()
        self.blade_panel.speed_changed.connect(self.blade_speed_changed.emit)
        self.blade_panel.blade_move.connect(self.blade_move.emit)
        self.blade_panel.home_axis.connect(self.blade_home.emit)

        # Resin 프라이밍 패널
        self.y_panel = YAxisPanel()
        self.y_panel.move_positive.connect(lambda d: self.y_move.emit(d))
        self.y_panel.move_negative.connect(lambda d: self.y_move.emit(-d))
        self.y_panel.home_axis.connect(self.y_home.emit)
        self.y_panel.priming_started.connect(self.y_prime_start.emit)
        self.y_panel.priming_done.connect(self.y_prime_done.emit)

        panels_layout.addWidget(self.led_panel, 1)
        panels_layout.addWidget(self.blade_panel, 1)
        panels_layout.addWidget(self.y_panel, 1)

        self.content_layout.addLayout(panels_layout)

    def get_led_power(self) -> int:
        """LED 파워 값 반환"""
        return self.led_panel.get_power()

    def set_led_power(self, value: int):
        """LED 파워 값 설정"""
        self.led_panel.set_power(value)

    def get_blade_speed(self) -> int:
        """Blade 속도 값 반환"""
        return self.blade_panel.get_speed()

    def set_blade_speed(self, value: int):
        """Blade 속도 값 설정"""
        self.blade_panel.set_speed(value)

