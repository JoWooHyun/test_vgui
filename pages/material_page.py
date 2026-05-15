"""
VERICOM DLP 3D Printer GUI - Material Preset Page
소재별 프린트 프리셋 관리 (추가/편집/삭제)
"""

from dataclasses import asdict
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QDialog, QLineEdit
)
from PySide6.QtCore import Signal, Qt

from pages.base_page import BasePage
from components.numeric_keypad import NumericKeypad
from styles.colors import Colors
from styles.fonts import Fonts
from styles.icons import Icons
from styles.stylesheets import Radius
from controllers.settings_manager import get_settings, MaterialPreset


class MaterialNameDialog(QDialog):
    """소재 이름 입력 다이얼로그"""

    def __init__(self, title: str = "New Material", current_name: str = "", parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.setFixedSize(350, 180)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.BG_PRIMARY};
                border: 2px solid {Colors.CYAN};
                border-radius: 16px;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # 제목
        lbl_title = QLabel(title)
        lbl_title.setFont(Fonts.h3())
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        layout.addWidget(lbl_title)

        # 이름 입력
        self.input = QLineEdit(current_name)
        self.input.setFixedHeight(44)
        self.input.setFont(Fonts.body())
        self.input.setPlaceholderText("Material name...")
        self.input.setStyleSheet(f"""
            QLineEdit {{
                background-color: {Colors.BG_SECONDARY};
                border: 2px solid {Colors.BORDER};
                border-radius: 8px;
                color: {Colors.TEXT_PRIMARY};
                padding: 0 12px;
            }}
            QLineEdit:focus {{
                border-color: {Colors.CYAN};
            }}
        """)
        layout.addWidget(self.input)

        # 버튼
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.setFixedSize(120, 44)
        btn_cancel.setFont(Fonts.body())
        btn_cancel.setCursor(Qt.PointingHandCursor)
        btn_cancel.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 8px;
            }}
            QPushButton:pressed {{ background-color: {Colors.BG_TERTIARY}; }}
        """)
        btn_cancel.clicked.connect(self.reject)

        btn_ok = QPushButton("OK")
        btn_ok.setFixedSize(120, 44)
        btn_ok.setFont(Fonts.body())
        btn_ok.setCursor(Qt.PointingHandCursor)
        btn_ok.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.CYAN};
                color: {Colors.WHITE};
                border: none;
                border-radius: 8px;
            }}
            QPushButton:pressed {{ background-color: {Colors.CYAN_DARK}; }}
        """)
        btn_ok.clicked.connect(self.accept)

        btn_layout.addWidget(btn_cancel)
        btn_layout.addWidget(btn_ok)
        layout.addLayout(btn_layout)

    def get_name(self) -> str:
        return self.input.text().strip()


class MaterialEditRow(QFrame):
    """소재 설정 편집 행"""

    value_changed = Signal()

    def __init__(self, label: str, value: float, unit: str,
                 min_val: float, max_val: float, step: float = 1.0,
                 allow_decimal: bool = False, parent=None):
        super().__init__(parent)

        self._value = value
        self._unit = unit
        self._min = min_val
        self._max = max_val
        self._label = label
        self._allow_decimal = allow_decimal

        self.setFixedHeight(36)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 6px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 10, 0)
        layout.setSpacing(8)

        self.lbl_label = QLabel(label)
        self.lbl_label.setFont(Fonts.body_small())
        self.lbl_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; background: transparent; border: none;")
        self.lbl_label.setFixedWidth(120)

        self.lbl_value = QLabel()
        self.lbl_value.setFont(Fonts.body_small())
        self.lbl_value.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.lbl_value.setStyleSheet(f"color: {Colors.CYAN}; background: transparent; border: none; font-weight: 600;")
        self._update_display()

        layout.addWidget(self.lbl_label)
        layout.addWidget(self.lbl_value, 1)

    def _update_display(self):
        if self._value == int(self._value):
            self.lbl_value.setText(f"{int(self._value)} {self._unit}")
        else:
            self.lbl_value.setText(f"{self._value:.1f} {self._unit}")

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            keypad = NumericKeypad(
                title=self._label,
                value=self._value,
                unit=self._unit,
                min_val=self._min,
                max_val=self._max,
                allow_decimal=self._allow_decimal,
                parent=self.window()
            )
            keypad.value_confirmed.connect(self._on_confirmed)
            keypad.exec()
        super().mousePressEvent(event)

    def _on_confirmed(self, value: float):
        self._value = value
        self._update_display()
        self.value_changed.emit()

    def get_value(self) -> float:
        return self._value

    def set_value(self, value: float):
        self._value = value
        self._update_display()


class MaterialPage(BasePage):
    """소재 프리셋 관리 페이지"""

    def __init__(self, parent=None):
        super().__init__("Material", show_back=True, parent=parent)
        self._current_material_name = ""
        self._setup_content()
        self._load_materials()

    def _setup_content(self):
        """콘텐츠 구성: 좌측 소재 리스트 + 우측 편집 패널"""
        main_layout = QHBoxLayout()
        main_layout.setSpacing(20)

        # === 좌측: 소재 리스트 ===
        left_frame = QFrame()
        left_frame.setFixedWidth(240)
        left_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
        """)
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(12, 12, 12, 12)
        left_layout.setSpacing(8)

        # 리스트 타이틀
        lbl_list_title = QLabel("Presets")
        lbl_list_title.setFont(Fonts.h3())
        lbl_list_title.setAlignment(Qt.AlignCenter)
        lbl_list_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent; border: none;")
        left_layout.addWidget(lbl_list_title)

        # 스크롤 영역 (소재 버튼들)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet(f"""
            QScrollArea {{
                border: none;
                background: transparent;
            }}
            QWidget {{
                background: transparent;
            }}
        """)
        self._list_widget = QWidget()
        self._list_layout = QVBoxLayout(self._list_widget)
        self._list_layout.setContentsMargins(0, 0, 0, 0)
        self._list_layout.setSpacing(6)
        self._list_layout.addStretch()
        scroll.setWidget(self._list_widget)
        left_layout.addWidget(scroll, 1)

        # Add / Delete 버튼
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.btn_add = QPushButton("Add")
        self.btn_add.setFixedHeight(36)
        self.btn_add.setFont(Fonts.body_small())
        self.btn_add.setCursor(Qt.PointingHandCursor)
        self.btn_add.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.CYAN};
                color: {Colors.WHITE};
                border: none;
                border-radius: 6px;
            }}
            QPushButton:pressed {{ background-color: {Colors.CYAN_DARK}; }}
        """)
        self.btn_add.clicked.connect(self._on_add)

        self.btn_delete = QPushButton("Delete")
        self.btn_delete.setFixedHeight(36)
        self.btn_delete.setFont(Fonts.body_small())
        self.btn_delete.setCursor(Qt.PointingHandCursor)
        self.btn_delete.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_PRIMARY};
                color: {Colors.RED};
                border: 1px solid {Colors.RED};
                border-radius: 6px;
            }}
            QPushButton:pressed {{ background-color: {Colors.RED}; color: {Colors.WHITE}; }}
        """)
        self.btn_delete.clicked.connect(self._on_delete)

        btn_row.addWidget(self.btn_add)
        btn_row.addWidget(self.btn_delete)
        left_layout.addLayout(btn_row)

        # === 우측: 편집 패널 ===
        right_frame = QFrame()
        right_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 12px;
            }}
        """)
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(16, 16, 16, 16)
        right_layout.setSpacing(8)

        # 소재 이름 (클릭하여 변경)
        self.lbl_material_name = QPushButton("Select Material")
        self.lbl_material_name.setFixedHeight(40)
        self.lbl_material_name.setFont(Fonts.h3())
        self.lbl_material_name.setCursor(Qt.PointingHandCursor)
        self.lbl_material_name.setStyleSheet(f"""
            QPushButton {{
                color: {Colors.NAVY};
                background: transparent;
                border: none;
                border-bottom: 2px solid {Colors.CYAN};
            }}
            QPushButton:pressed {{ color: {Colors.CYAN}; }}
        """)
        self.lbl_material_name.clicked.connect(self._on_rename)
        right_layout.addWidget(self.lbl_material_name)

        right_layout.addSpacing(4)

        # 편집 행들
        self.row_blade_speed = MaterialEditRow("Blade Speed", 5, "mm/s", 1, 100)
        self.row_led_power = MaterialEditRow("LED Power", 43, "%", 9, 100)
        self.row_blade_cycles = MaterialEditRow("Blade Cycles", 1, "회", 1, 3)
        self.row_y_dispense = MaterialEditRow("Resin Dist.", 1.0, "mm", 0.1, 5.0, allow_decimal=True)
        self.row_y_speed = MaterialEditRow("Resin Speed", 3, "mm/s", 1, 15)
        self.row_y_delay = MaterialEditRow("Resin Delay", 5.0, "s", 0.5, 300.0, allow_decimal=True)
        self.row_leveling = MaterialEditRow("평탄화 횟수", 1, "회", 0, 5)

        self._edit_rows = [
            self.row_blade_speed, self.row_led_power, self.row_blade_cycles,
            self.row_y_dispense, self.row_y_speed, self.row_y_delay,
            self.row_leveling
        ]

        for row in self._edit_rows:
            row.value_changed.connect(self._on_value_changed)
            right_layout.addWidget(row)

        right_layout.addStretch()

        # 조립
        main_layout.addWidget(left_frame)
        main_layout.addWidget(right_frame, 1)

        self.content_layout.addLayout(main_layout)

    def _load_materials(self):
        """소재 목록 로드 및 UI 갱신"""
        settings = get_settings()
        materials = settings.get_materials()

        # 기존 버튼 제거
        while self._list_layout.count() > 1:  # stretch 유지
            item = self._list_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # 소재 버튼 추가
        for mat in materials:
            btn = QPushButton(mat.name)
            btn.setFixedHeight(40)
            btn.setFont(Fonts.body())
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, name=mat.name: self._select_material(name))
            self._list_layout.insertWidget(self._list_layout.count() - 1, btn)

        # 선택된 소재 표시
        selected = settings.get_selected_material()
        if selected:
            self._select_material(selected)
        elif materials:
            self._select_material(materials[0].name)

        self._update_list_styles()

    def _update_list_styles(self):
        """리스트 버튼 스타일 갱신"""
        for i in range(self._list_layout.count()):
            item = self._list_layout.itemAt(i)
            if item and item.widget() and isinstance(item.widget(), QPushButton):
                btn = item.widget()
                if btn.text() == self._current_material_name:
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {Colors.CYAN};
                            color: {Colors.WHITE};
                            border: none;
                            border-radius: 8px;
                            font-weight: 600;
                        }}
                    """)
                else:
                    btn.setStyleSheet(f"""
                        QPushButton {{
                            background-color: {Colors.BG_PRIMARY};
                            color: {Colors.TEXT_PRIMARY};
                            border: 1px solid {Colors.BORDER};
                            border-radius: 8px;
                        }}
                        QPushButton:pressed {{ background-color: {Colors.BG_TERTIARY}; }}
                    """)

    def _select_material(self, name: str):
        """소재 선택"""
        settings = get_settings()
        preset = settings.get_material_by_name(name)
        if not preset:
            return

        self._current_material_name = name
        settings.set_selected_material(name)

        # UI 갱신
        self.lbl_material_name.setText(name)
        self.row_blade_speed.set_value(preset.blade_speed)
        self.row_led_power.set_value(preset.led_power)
        self.row_blade_cycles.set_value(preset.blade_cycles)
        self.row_y_dispense.set_value(preset.y_dispense_distance)
        self.row_y_speed.set_value(preset.y_dispense_speed)
        self.row_y_delay.set_value(preset.y_dispense_delay)
        self.row_leveling.set_value(preset.leveling_cycles)

        self._update_list_styles()

    def _on_value_changed(self):
        """편집 값 변경 → 즉시 저장"""
        if not self._current_material_name:
            return

        preset = MaterialPreset(
            name=self._current_material_name,
            blade_speed=int(self.row_blade_speed.get_value()),
            led_power=int(self.row_led_power.get_value()),
            blade_cycles=int(self.row_blade_cycles.get_value()),
            y_dispense_distance=self.row_y_dispense.get_value(),
            y_dispense_speed=int(self.row_y_speed.get_value()),
            y_dispense_delay=self.row_y_delay.get_value(),
            leveling_cycles=int(self.row_leveling.get_value()),
        )
        get_settings().update_material(self._current_material_name, preset)

    def _on_add(self):
        """소재 추가"""
        dialog = MaterialNameDialog("New Material", "", self)
        if dialog.exec() == QDialog.Accepted:
            name = dialog.get_name()
            if name:
                get_settings().add_material(MaterialPreset(name=name))
                self._load_materials()
                self._select_material(name)

    def _on_delete(self):
        """소재 삭제"""
        if not self._current_material_name:
            return

        if get_settings().delete_material(self._current_material_name):
            self._current_material_name = ""
            self._load_materials()

    def _on_rename(self):
        """소재 이름 변경"""
        if not self._current_material_name:
            return

        dialog = MaterialNameDialog("Rename", self._current_material_name, self)
        if dialog.exec() == QDialog.Accepted:
            new_name = dialog.get_name()
            if new_name and new_name != self._current_material_name:
                settings = get_settings()
                preset = settings.get_material_by_name(self._current_material_name)
                if preset:
                    old_name = self._current_material_name
                    preset.name = new_name
                    settings.update_material(old_name, preset)
                    self._current_material_name = new_name
                    self._load_materials()
