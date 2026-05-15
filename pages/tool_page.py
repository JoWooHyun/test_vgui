"""
Test VGUI - Tool Page (Manual / Setting / Material)
"""

from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtCore import Signal

from pages.base_page import BasePage
from components.icon_button import ToolButton
from styles.icons import Icons


class ToolPage(BasePage):
    """도구 메뉴 (Manual, Setting, Material)"""

    go_manual = Signal()
    go_setting = Signal()
    go_material = Signal()

    BUTTON_SIZE = (200, 200)

    def __init__(self, parent=None):
        super().__init__("Tool", show_back=True, parent=parent)
        self._setup_content()

    def _setup_content(self):
        self.content_layout.addStretch(1)

        row = QHBoxLayout()
        row.setSpacing(20)
        row.addStretch()

        self.btn_manual = ToolButton("Manual", Icons.MOVE)
        self.btn_manual.setFixedSize(*self.BUTTON_SIZE)
        self.btn_manual.clicked.connect(self.go_manual.emit)
        row.addWidget(self.btn_manual)

        self.btn_setting = ToolButton("Setting", Icons.CALIBRATION)
        self.btn_setting.setFixedSize(*self.BUTTON_SIZE)
        self.btn_setting.clicked.connect(self.go_setting.emit)
        row.addWidget(self.btn_setting)

        self.btn_material = ToolButton("Material", Icons.MATERIAL)
        self.btn_material.setFixedSize(*self.BUTTON_SIZE)
        self.btn_material.clicked.connect(self.go_material.emit)
        row.addWidget(self.btn_material)

        row.addStretch()
        self.content_layout.addLayout(row)
        self.content_layout.addStretch(2)
