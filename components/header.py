"""
VERICOM DLP 3D Printer GUI - Header Component
"""

from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap

from styles.colors import Colors
from styles.icons import Icons
from styles.stylesheets import (
    get_header_style, get_header_title_style, get_back_button_style
)


class Header(QWidget):
    """페이지 상단 헤더 컴포넌트"""
    
    # 시그널 정의
    back_clicked = Signal()
    
    def __init__(self, title: str = "", show_back: bool = True, 
                 parent=None):
        super().__init__(parent)
        self.setObjectName("header")
        self.setFixedHeight(56)
        
        self._title = title
        self._show_back = show_back
        
        self._setup_ui()
    
    def _setup_ui(self):
        """UI 구성"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        layout.setSpacing(16)

        # Back 버튼
        self.btn_back = QPushButton()
        self.btn_back.setFixedSize(40, 40)
        self.btn_back.setStyleSheet(get_back_button_style())
        self.btn_back.setCursor(Qt.PointingHandCursor)
        self.btn_back.clicked.connect(self.back_clicked.emit)

        # Back 아이콘 설정
        icon_pixmap = Icons.get_pixmap(Icons.ARROW_LEFT, 20, Colors.NAVY)
        self.btn_back.setIcon(Icons.get_icon(Icons.ARROW_LEFT, 20, Colors.NAVY))
        self.btn_back.setIconSize(icon_pixmap.size())

        if not self._show_back:
            self.btn_back.setVisible(False)

        # 타이틀
        self.title_label = QLabel(self._title)
        self.title_label.setStyleSheet(get_header_title_style())
        self.title_label.setAlignment(Qt.AlignCenter)

        # 우측 여백 (Back 버튼과 균형) - 투명 배경 (부모 배경색 상속)
        self.right_spacer = QWidget()
        self.right_spacer.setFixedSize(40, 40)
        self.right_spacer.setStyleSheet("background-color: transparent;")

        # 레이아웃 구성
        layout.addWidget(self.btn_back)
        layout.addWidget(self.title_label, 1)
        layout.addWidget(self.right_spacer)

        # 스타일 적용
        self.setStyleSheet(get_header_style())
    
    def set_title(self, title: str):
        """타이틀 변경"""
        self._title = title
        self.title_label.setText(title)
    
    def set_back_visible(self, visible: bool):
        """Back 버튼 표시/숨김"""
        self._show_back = visible
        self.btn_back.setVisible(visible)
        self.right_spacer.setVisible(visible)
