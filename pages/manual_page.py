"""
VERICOM DLP 3D Printer GUI - Manual Control Page
"""

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QGridLayout, QDialog
)
from PySide6.QtCore import Signal, Qt

from pages.base_page import BasePage
from components.icon_button import ControlButton, HomeButton
from components.numeric_keypad import NumericKeypad
from styles.colors import Colors
from styles.fonts import Fonts
from styles.icons import Icons
from styles.stylesheets import (
    get_axis_panel_style, get_axis_title_style,
    get_distance_button_active_style, AXIS_VALUE_STYLE
)


class AxisControlPanel(QFrame):
    """축 제어 패널"""

    # 이동 시그널
    move_positive = Signal(float)  # 양의 방향 이동 (거리)
    move_negative = Signal(float)  # 음의 방향 이동 (거리)
    home_axis = Signal()           # 홈 위치로

    def __init__(self, axis_name: str, is_horizontal: bool = False,
                 default_distance: float = 1.0,
                 min_distance: float = 0.05, max_distance: float = 100.0,
                 show_speed: bool = False, default_speed: int = 10,
                 min_speed: int = 5, max_speed: int = 9999,
                 parent=None):
        super().__init__(parent)

        self._axis_name = axis_name
        self._is_horizontal = is_horizontal
        self._distance = default_distance
        self._min_distance = min_distance
        self._max_distance = max_distance
        self._show_speed = show_speed
        self._speed = default_speed
        self._min_speed = min_speed
        self._max_speed = max_speed

        self._setup_ui()

    def _setup_ui(self):
        """UI 구성"""
        self.setStyleSheet(get_axis_panel_style())

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(0)

        layout.addStretch(1)

        # 헤더 (축 이름 - 가운데 정렬)
        self.title_label = QLabel(self._axis_name)
        self.title_label.setStyleSheet(get_axis_title_style())
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        layout.addStretch(1)

        # 거리 입력 버튼 (클릭하면 NumericKeypad 열림)
        self.btn_distance = QPushButton(self._format_value(self._distance, "mm"))
        self.btn_distance.setFixedHeight(44)
        self.btn_distance.setCursor(Qt.PointingHandCursor)
        self.btn_distance.setStyleSheet(get_distance_button_active_style())
        self.btn_distance.clicked.connect(self._on_distance_click)
        layout.addWidget(self.btn_distance)

        # 속도 입력 버튼 (show_speed=True일 때만)
        if self._show_speed:
            self.btn_speed = QPushButton(f"{self._speed} mm/s")
            self.btn_speed.setFixedHeight(44)
            self.btn_speed.setCursor(Qt.PointingHandCursor)
            self.btn_speed.setStyleSheet(get_distance_button_active_style())
            self.btn_speed.clicked.connect(self._on_speed_click)
            layout.addWidget(self.btn_speed)

        layout.addStretch(1)

        # 제어 버튼들
        control_layout = QHBoxLayout()
        control_layout.setSpacing(12)
        control_layout.setAlignment(Qt.AlignCenter)

        # 홈 버튼
        self.btn_home = HomeButton(70, 28)
        self.btn_home.clicked.connect(self.home_axis.emit)

        # 방향 버튼들
        if self._is_horizontal:
            self.btn_negative = ControlButton(Icons.CHEVRON_LEFT, 70, 28)
            self.btn_positive = ControlButton(Icons.CHEVRON_RIGHT, 70, 28)
        else:
            self.btn_positive = ControlButton(Icons.CHEVRON_UP, 70, 28)
            self.btn_negative = ControlButton(Icons.CHEVRON_DOWN, 70, 28)

        self.btn_positive.clicked.connect(self._on_move_positive)
        self.btn_negative.clicked.connect(self._on_move_negative)

        control_layout.addWidget(self.btn_home)
        control_layout.addWidget(self.btn_positive)
        control_layout.addWidget(self.btn_negative)

        layout.addLayout(control_layout)

        layout.addStretch(1)

    def _format_value(self, value: float, unit: str) -> str:
        """값 표시 포맷"""
        if value == int(value):
            return f"{int(value)} {unit}"
        else:
            return f"{value:g} {unit}"

    def _on_distance_click(self):
        """거리 버튼 클릭 → NumericKeypad 열기"""
        keypad = NumericKeypad(
            title="Move Distance",
            value=self._distance,
            unit="mm",
            min_val=self._min_distance,
            max_val=self._max_distance,
            allow_decimal=True,
            parent=self.window()
        )
        if keypad.exec() == QDialog.Accepted:
            self._distance = keypad.get_value()
            self.btn_distance.setText(self._format_value(self._distance, "mm"))

    def _on_speed_click(self):
        """속도 버튼 클릭 → NumericKeypad 열기"""
        keypad = NumericKeypad(
            title="Move Speed",
            value=self._speed,
            unit="mm/s",
            min_val=self._min_speed,
            max_val=self._max_speed,
            allow_decimal=False,
            parent=self.window()
        )
        if keypad.exec() == QDialog.Accepted:
            self._speed = int(keypad.get_value())
            self.btn_speed.setText(f"{self._speed} mm/s")

    def _on_move_positive(self):
        """양의 방향 이동"""
        self.move_positive.emit(self._distance)

    def _on_move_negative(self):
        """음의 방향 이동"""
        self.move_negative.emit(self._distance)

    def get_distance(self) -> float:
        """현재 거리 반환"""
        return self._distance

    def get_speed(self) -> int:
        """현재 속도 반환 (mm/s)"""
        return self._speed

    def set_value(self, value: float):
        """현재 값 업데이트 (사용 안함)"""
        pass


class ManualPage(BasePage):
    """수동 제어 페이지 (Z축 + X축 + Y축)"""

    # 모터 제어 시그널
    z_move = Signal(float)      # Z축 이동 (+ 상승, - 하강)
    z_home = Signal()           # Z축 홈

    x_move = Signal(float, int) # X축(블레이드) 이동 (거리, 속도 mm/min)
    x_home = Signal()           # X축 홈

    y_move = Signal(float)      # Y축(Resin Feeder) 이동
    y_home = Signal()           # Y축 홈

    def __init__(self, parent=None):
        super().__init__("Manual Control", show_back=True, parent=parent)
        self._setup_content()

    def _setup_content(self):
        """콘텐츠 구성"""
        # 3열 레이아웃
        panels_layout = QHBoxLayout()
        panels_layout.setSpacing(20)

        # Z축 패널
        self.z_panel = AxisControlPanel("Z Axis", is_horizontal=False)
        self.z_panel.move_positive.connect(lambda d: self.z_move.emit(d))
        self.z_panel.move_negative.connect(lambda d: self.z_move.emit(-d))
        self.z_panel.home_axis.connect(self.z_home.emit)

        # X축 패널 (블레이드) - 속도 설정 포함
        self.x_panel = AxisControlPanel("X Axis (Blade)", is_horizontal=True,
                                         show_speed=True, default_speed=10,
                                         min_speed=5, max_distance=140.0)
        self.x_panel.move_positive.connect(
            lambda d: self.x_move.emit(d, self.x_panel.get_speed() * 60))
        self.x_panel.move_negative.connect(
            lambda d: self.x_move.emit(-d, self.x_panel.get_speed() * 60))
        self.x_panel.home_axis.connect(self.x_home.emit)

        # Y축 패널 (Resin Feeder)
        self.y_panel = AxisControlPanel("Resin Feeder", is_horizontal=False)
        self.y_panel.move_positive.connect(lambda d: self.y_move.emit(d))
        self.y_panel.move_negative.connect(lambda d: self.y_move.emit(-d))
        self.y_panel.home_axis.connect(self.y_home.emit)

        panels_layout.addWidget(self.z_panel)
        panels_layout.addWidget(self.x_panel)
        panels_layout.addWidget(self.y_panel)

        self.content_layout.addLayout(panels_layout)

    def update_z_position(self, value: float):
        """Z축 위치 업데이트"""
        self.z_panel.set_value(value)

    def update_x_position(self, value: float):
        """X축 위치 업데이트"""
        self.x_panel.set_value(value)
