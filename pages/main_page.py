"""
Test VGUI - Main Page (Tool / Print Test)
"""

import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap

from styles.colors import Colors
from styles.fonts import Fonts
from styles.icons import Icons
from components.icon_button import MainMenuButton

LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "VERICOM_LOGO.png")


class MainPage(QWidget):
    """메인 홈 페이지 (Tool / Print Test)"""

    go_tool = Signal()
    go_print_test = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # 상단 타이틀
        title_widget = QWidget()
        title_widget.setFixedHeight(80)
        title_widget.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
        title_layout = QVBoxLayout(title_widget)
        title_layout.setAlignment(Qt.AlignCenter)

        title_label = QLabel("MAZIC CERA - Test")
        title_label.setFont(Fonts.h3())
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {Colors.NAVY};")
        title_layout.addWidget(title_label)
        layout.addWidget(title_widget)

        # 메인 콘텐츠
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setAlignment(Qt.AlignCenter)
        content_layout.setSpacing(32)

        self.btn_tool = MainMenuButton("Tool", Icons.WRENCH)
        self.btn_tool.clicked.connect(self.go_tool.emit)

        self.btn_print_test = MainMenuButton("Print Test", Icons.LAYERS)
        self.btn_print_test.clicked.connect(self.go_print_test.emit)

        content_layout.addWidget(self.btn_tool)
        content_layout.addWidget(self.btn_print_test)
        layout.addWidget(content, 1)

        # 하단 로고
        footer_widget = QWidget()
        footer_widget.setFixedHeight(44)
        footer_widget.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 0, 16, 8)
        footer_layout.addStretch()

        logo_label = QLabel()
        if os.path.exists(LOGO_PATH):
            pixmap = QPixmap(LOGO_PATH)
            scaled_pixmap = pixmap.scaledToWidth(88, Qt.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
        footer_layout.addWidget(logo_label)
        layout.addWidget(footer_widget)
