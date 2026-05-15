"""
Test VGUI - Print Test Page
설정값 요약 + 레이어 수 입력 + Start 버튼
"""

from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QGridLayout,
    QWidget, QLabel, QPushButton
)
from PySide6.QtCore import Signal, Qt

from pages.base_page import BasePage
from components.numeric_keypad import NumericKeypad
from styles.colors import Colors
from styles.fonts import Fonts
from styles.stylesheets import Radius
from controllers.settings_manager import get_settings


class PrintTestPage(BasePage):
    """프린트 테스트 설정 및 시작 페이지"""

    start_test = Signal(dict)  # 파라미터 딕셔너리

    def __init__(self, parent=None):
        super().__init__("Print Test", show_back=True, parent=parent)
        self.settings = get_settings()
        self._total_layers = 10
        self._layer_height = 0.05
        self._bottom_layers = 3
        self._setup_content()

    def _setup_content(self):
        self.content_layout.setContentsMargins(20, 10, 20, 10)

        # 메인 영역 (좌: 설정 요약, 우: 레이어 설정)
        main_row = QHBoxLayout()
        main_row.setSpacing(20)

        # === 좌측: 현재 설정 요약 ===
        left_panel = QWidget()
        left_panel.setStyleSheet(f"""
            QWidget {{
                background-color: {Colors.BG_SECONDARY};
                border-radius: {Radius.LG}px;
            }}
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 15, 20, 15)
        left_layout.setSpacing(8)

        lbl_title = QLabel("Current Settings")
        lbl_title.setFont(Fonts.h3())
        lbl_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        left_layout.addWidget(lbl_title)

        # 설정값 그리드
        self.grid = QGridLayout()
        self.grid.setSpacing(6)
        self._labels = {}

        items = [
            ("Blade Speed", "blade_speed", "mm/s"),
            ("Dispense Dist", "y_dispense_dist", "mm"),
            ("Dispense Speed", "y_dispense_speed", "mm/s"),
            ("Dispense Delay", "y_dispense_delay", "s"),
            ("Leveling Cycles", "leveling_cycles", ""),
            ("Priming Pos", "priming_pos", "mm"),
        ]

        for i, (label, key, unit) in enumerate(items):
            lbl_name = QLabel(f"{label}:")
            lbl_name.setFont(Fonts.body())
            lbl_name.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; background: transparent;")
            self.grid.addWidget(lbl_name, i, 0)

            lbl_value = QLabel("--")
            lbl_value.setFont(Fonts.body())
            lbl_value.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent; font-weight: bold;")
            self.grid.addWidget(lbl_value, i, 1)

            if unit:
                lbl_unit = QLabel(unit)
                lbl_unit.setFont(Fonts.caption())
                lbl_unit.setStyleSheet(f"color: {Colors.TEXT_DISABLED}; background: transparent;")
                self.grid.addWidget(lbl_unit, i, 2)

            self._labels[key] = lbl_value

        left_layout.addLayout(self.grid)
        left_layout.addStretch()
        main_row.addWidget(left_panel, 3)

        # === 우측: 레이어 설정 + Start ===
        right_panel = QWidget()
        right_panel.setStyleSheet(f"""
            QWidget {{
                background-color: {Colors.BG_SECONDARY};
                border-radius: {Radius.LG}px;
            }}
        """)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(20, 15, 20, 15)
        right_layout.setSpacing(12)

        # 레이어 수
        row_layers = QHBoxLayout()
        lbl_layers = QLabel("Layers:")
        lbl_layers.setFont(Fonts.h3())
        lbl_layers.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        row_layers.addWidget(lbl_layers)

        self.lbl_layer_count = QLabel(str(self._total_layers))
        self.lbl_layer_count.setFont(Fonts.h2())
        self.lbl_layer_count.setAlignment(Qt.AlignCenter)
        self.lbl_layer_count.setStyleSheet(f"""
            color: {Colors.CYAN};
            background: transparent;
            font-weight: bold;
        """)
        self.lbl_layer_count.mousePressEvent = lambda e: self._edit_value("layers")
        row_layers.addWidget(self.lbl_layer_count)
        right_layout.addLayout(row_layers)

        # 레이어 높이
        row_height = QHBoxLayout()
        lbl_h = QLabel("Layer Height:")
        lbl_h.setFont(Fonts.h3())
        lbl_h.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        row_height.addWidget(lbl_h)

        self.lbl_layer_height = QLabel(f"{self._layer_height} mm")
        self.lbl_layer_height.setFont(Fonts.h2())
        self.lbl_layer_height.setAlignment(Qt.AlignCenter)
        self.lbl_layer_height.setStyleSheet(f"""
            color: {Colors.CYAN};
            background: transparent;
            font-weight: bold;
        """)
        self.lbl_layer_height.mousePressEvent = lambda e: self._edit_value("height")
        row_height.addWidget(self.lbl_layer_height)
        right_layout.addLayout(row_height)

        # 바닥 레이어 수
        row_bottom = QHBoxLayout()
        lbl_b = QLabel("Bottom Layers:")
        lbl_b.setFont(Fonts.h3())
        lbl_b.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        row_bottom.addWidget(lbl_b)

        self.lbl_bottom_layers = QLabel(str(self._bottom_layers))
        self.lbl_bottom_layers.setFont(Fonts.h2())
        self.lbl_bottom_layers.setAlignment(Qt.AlignCenter)
        self.lbl_bottom_layers.setStyleSheet(f"""
            color: {Colors.CYAN};
            background: transparent;
            font-weight: bold;
        """)
        self.lbl_bottom_layers.mousePressEvent = lambda e: self._edit_value("bottom")
        row_bottom.addWidget(self.lbl_bottom_layers)
        right_layout.addLayout(row_bottom)

        right_layout.addStretch()

        # Start 버튼
        self.btn_start = QPushButton("START")
        self.btn_start.setFixedHeight(60)
        self.btn_start.setFont(Fonts.h2())
        self.btn_start.setCursor(Qt.PointingHandCursor)
        self.btn_start.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.NAVY};
                border: none;
                border-radius: {Radius.LG}px;
                color: {Colors.WHITE};
                font-weight: bold;
            }}
            QPushButton:pressed {{
                background-color: {Colors.NAVY_LIGHT};
            }}
        """)
        self.btn_start.clicked.connect(self._on_start)
        right_layout.addWidget(self.btn_start)

        main_row.addWidget(right_panel, 2)
        self.content_layout.addLayout(main_row)

    def showEvent(self, event):
        """페이지 표시 시 설정값 갱신"""
        super().showEvent(event)
        self._refresh_settings()

    def _refresh_settings(self):
        """현재 설정값 표시"""
        preset = self.settings.get_selected_material_preset()
        if preset:
            self._labels["blade_speed"].setText(str(preset.blade_speed))
            self._labels["y_dispense_dist"].setText(str(preset.y_dispense_distance))
            self._labels["y_dispense_speed"].setText(str(preset.y_dispense_speed))
            self._labels["y_dispense_delay"].setText(str(preset.y_dispense_delay))
            self._labels["leveling_cycles"].setText(str(preset.leveling_cycles))

        priming = self.settings.get_y_priming_position()
        self._labels["priming_pos"].setText(f"{priming:.1f}")

    def _edit_value(self, which: str):
        """수치 편집 다이얼로그"""
        if which == "layers":
            keypad = NumericKeypad(
                title="Total Layers",
                current_value=self._total_layers,
                min_val=1, max_val=1000,
                is_integer=True,
                parent=self
            )
            if keypad.exec():
                self._total_layers = int(keypad.get_value())
                self.lbl_layer_count.setText(str(self._total_layers))
        elif which == "height":
            keypad = NumericKeypad(
                title="Layer Height (mm)",
                current_value=self._layer_height,
                min_val=0.01, max_val=1.0,
                is_integer=False,
                parent=self
            )
            if keypad.exec():
                self._layer_height = keypad.get_value()
                self.lbl_layer_height.setText(f"{self._layer_height} mm")
        elif which == "bottom":
            keypad = NumericKeypad(
                title="Bottom Layers",
                current_value=self._bottom_layers,
                min_val=0, max_val=20,
                is_integer=True,
                parent=self
            )
            if keypad.exec():
                self._bottom_layers = int(keypad.get_value())
                self.lbl_bottom_layers.setText(str(self._bottom_layers))

    def _on_start(self):
        """Start 버튼 클릭"""
        preset = self.settings.get_selected_material_preset()

        params = {
            'totalLayer': self._total_layers,
            'layerHeight': self._layer_height,
            'bottomLayerCount': self._bottom_layers,
            'bladeSpeed': preset.blade_speed * 60 if preset else 300,
            'bladeCycles': preset.blade_cycles if preset else 1,
            'levelingCycles': preset.leveling_cycles if preset else 1,
            'yDispenseDistance': preset.y_dispense_distance if preset else 1.0,
            'yDispenseSpeed': preset.y_dispense_speed * 60 if preset else 180,
            'yDispenseDelay': preset.y_dispense_delay if preset else 2.0,
        }

        self.start_test.emit(params)
