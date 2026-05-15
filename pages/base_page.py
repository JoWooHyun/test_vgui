"""
VERICOM DLP 3D Printer GUI - Base Page Class
"""

import os
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap

from components.header import Header
from styles.colors import Colors

# 로고 경로
LOGO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "VERICOM_LOGO.png")


class BasePage(QWidget):
    """모든 페이지의 기본 클래스"""
    
    # 페이지 전환 시그널
    go_back = Signal()
    go_home = Signal()
    
    def __init__(self, title: str = "", show_back: bool = True, parent=None):
        super().__init__(parent)
        
        self._title = title
        self._show_back = show_back
        
        self._setup_base_ui()
    
    def _setup_base_ui(self):
        """기본 UI 구조 설정"""
        self.setStyleSheet(f"background-color: {Colors.BG_PRIMARY};")
        
        # 메인 레이아웃
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        # 헤더
        self.header = Header(self._title, self._show_back, self)
        self.header.back_clicked.connect(self._on_back_clicked)
        self.main_layout.addWidget(self.header)
        
        # 콘텐츠 영역
        self.content = QWidget()
        self.content.setStyleSheet("background-color: transparent;")
        self.content_layout = QVBoxLayout(self.content)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(16)

        self.main_layout.addWidget(self.content, 1)

        # 우측 하단 로고
        footer_widget = QWidget()
        footer_widget.setFixedHeight(44)
        footer_widget.setStyleSheet("background-color: transparent;")

        footer_layout = QHBoxLayout(footer_widget)
        footer_layout.setContentsMargins(0, 0, 16, 8)

        footer_layout.addStretch()  # 좌측 여백

        # 소형 로고
        small_logo_label = QLabel()
        if os.path.exists(LOGO_PATH):
            pixmap = QPixmap(LOGO_PATH)
            scaled_pixmap = pixmap.scaledToWidth(88, Qt.SmoothTransformation)
            small_logo_label.setPixmap(scaled_pixmap)
        small_logo_label.setStyleSheet("background-color: transparent;")

        footer_layout.addWidget(small_logo_label)

        self.main_layout.addWidget(footer_widget)
    
    def _on_back_clicked(self):
        """뒤로가기 처리"""
        self.go_back.emit()
    
    def set_title(self, title: str):
        """타이틀 변경"""
        self._title = title
        self.header.set_title(title)
