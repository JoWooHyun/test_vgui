"""
VERICOM DLP 3D Printer GUI - Numeric Keypad Component
터치스크린용 숫자 키패드 다이얼로그
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from styles.colors import Colors
from styles.fonts import Fonts


class NumericKeypad(QDialog):
    """터치스크린용 숫자 키패드 다이얼로그"""
    
    value_confirmed = Signal(float)
    
    def __init__(self, title: str = "값 입력", value: float = 0,
                 unit: str = "", min_val: float = 0, max_val: float = 9999,
                 allow_decimal: bool = False, parent=None):
        super().__init__(parent)
        
        self._title = title
        self._unit = unit
        self._min_val = min_val
        self._max_val = max_val
        self._allow_decimal = allow_decimal
        
        # 초기값을 문자열로 변환
        if allow_decimal:
            self._input_str = str(value) if value != int(value) else str(int(value))
        else:
            self._input_str = str(int(value))
        
        self.setWindowTitle(title)
        self.setFixedSize(350, 470)
        self.setModal(True)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """UI 구성"""
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {Colors.BG_PRIMARY};
                border: 2px solid {Colors.BORDER};
                border-radius: 16px;
            }}
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(16)
        
        # 타이틀
        lbl_title = QLabel(self._title)
        lbl_title.setFont(Fonts.h3())
        lbl_title.setAlignment(Qt.AlignCenter)
        lbl_title.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; background: transparent;")
        layout.addWidget(lbl_title)
        
        # 입력값 표시 영역
        self.display_frame = QFrame()
        self.display_frame.setFixedHeight(56)
        self.display_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 2px solid {Colors.CYAN};
                border-radius: 10px;
            }}
        """)
        
        display_layout = QHBoxLayout(self.display_frame)
        display_layout.setContentsMargins(16, 0, 16, 0)
        
        self.lbl_value = QLabel()
        self.lbl_value.setFont(QFont("Arial", 24, QFont.Bold))
        self.lbl_value.setAlignment(Qt.AlignCenter)
        self.lbl_value.setStyleSheet(f"color: {Colors.NAVY}; background-color: transparent; border: none;")
        self._update_display()
        
        display_layout.addWidget(self.lbl_value)
        
        layout.addWidget(self.display_frame)
        
        # 숫자 키패드 그리드
        grid_layout = QGridLayout()
        grid_layout.setHorizontalSpacing(8)
        grid_layout.setVerticalSpacing(24)
        
        # 숫자 버튼 스타일 (테마 연동)
        num_btn_style = f"""
            QPushButton {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.NAVY};
                border: 2px solid {Colors.NAVY};
                border-radius: 8px;
                font-size: 20px;
                font-weight: bold;
            }}
            QPushButton:pressed {{
                background-color: {Colors.BG_TERTIARY};
                border-color: {Colors.CYAN};
            }}
        """

        # Clear 버튼 스타일
        clear_btn_style = f"""
            QPushButton {{
                background-color: {Colors.RED};
                color: {Colors.WHITE};
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }}
            QPushButton:pressed {{
                background-color: #B71C1C;
            }}
        """
        
        # 숫자 버튼 1-9
        for i in range(1, 10):
            btn = QPushButton(str(i))
            btn.setFixedSize(70, 55)
            btn.setCursor(Qt.PointingHandCursor)
            btn.setStyleSheet(num_btn_style)
            btn.clicked.connect(lambda checked, num=i: self._append_digit(str(num)))
            
            row = (i - 1) // 3
            col = (i - 1) % 3
            grid_layout.addWidget(btn, row, col)
        
        # 4번째 줄: [C] [0] [.] 또는 [C]
        # Clear
        btn_clear = QPushButton("C")
        btn_clear.setFixedSize(70, 55)
        btn_clear.setCursor(Qt.PointingHandCursor)
        btn_clear.setStyleSheet(clear_btn_style)
        btn_clear.clicked.connect(self._clear)
        grid_layout.addWidget(btn_clear, 3, 0)
        
        # 0
        btn_zero = QPushButton("0")
        btn_zero.setFixedSize(70, 55)
        btn_zero.setCursor(Qt.PointingHandCursor)
        btn_zero.setStyleSheet(num_btn_style)
        btn_zero.clicked.connect(lambda: self._append_digit("0"))
        grid_layout.addWidget(btn_zero, 3, 1)
        
        # 소수점 버튼 (소수점 허용 시만 표시)
        if self._allow_decimal:
            btn_dot = QPushButton(".")
            btn_dot.setFixedSize(70, 55)
            btn_dot.setCursor(Qt.PointingHandCursor)
            btn_dot.setStyleSheet(num_btn_style)
            btn_dot.clicked.connect(lambda: self._append_digit("."))
            grid_layout.addWidget(btn_dot, 3, 2)
        
        # 그리드를 중앙 정렬
        grid_wrapper = QHBoxLayout()
        grid_wrapper.addStretch()
        grid_wrapper.addLayout(grid_layout)
        grid_wrapper.addStretch()
        
        layout.addLayout(grid_wrapper)
        
        layout.addSpacing(8)
        
        # 액션 버튼들
        action_layout = QHBoxLayout()
        action_layout.setSpacing(12)
        
        # Cancel 버튼
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setFixedSize(140, 50)
        self.btn_cancel.setFont(Fonts.body())
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.BG_SECONDARY};
                color: {Colors.TEXT_PRIMARY};
                border: 1px solid {Colors.BORDER};
                border-radius: 10px;
            }}
            QPushButton:pressed {{
                background-color: {Colors.BG_TERTIARY};
            }}
        """)
        self.btn_cancel.clicked.connect(self.reject)
        
        # Confirm 버튼
        self.btn_confirm = QPushButton("Confirm")
        self.btn_confirm.setFixedSize(140, 50)
        self.btn_confirm.setFont(Fonts.body())
        self.btn_confirm.setCursor(Qt.PointingHandCursor)
        self.btn_confirm.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.CYAN};
                color: {Colors.WHITE};
                border: none;
                border-radius: 10px;
            }}
            QPushButton:pressed {{
                background-color: {Colors.CYAN_DARK};
            }}
        """)
        self.btn_confirm.clicked.connect(self._confirm)
        
        action_layout.addWidget(self.btn_cancel)
        action_layout.addWidget(self.btn_confirm)
        
        layout.addLayout(action_layout)
    
    def _update_display(self):
        """디스플레이 업데이트"""
        display_text = self._input_str if self._input_str else "0"
        if self._unit:
            display_text += f" {self._unit}"
        self.lbl_value.setText(display_text)
    
    def _append_digit(self, digit: str):
        """숫자 추가"""
        # 소수점 중복 방지
        if digit == "." and "." in self._input_str:
            return
        
        # 앞에 0만 있는 경우 처리
        if self._input_str == "0" and digit != ".":
            self._input_str = digit
        else:
            self._input_str += digit
        
        self._update_display()
    
    def _clear(self):
        """전체 삭제"""
        self._input_str = ""
        self._update_display()
    
    def _confirm(self):
        """확인 - 값 검증 후 시그널 발생"""
        try:
            # 빈 값 처리
            if not self._input_str:
                value = 0
            else:
                value = float(self._input_str)
            
            # 범위 검증
            if value < self._min_val:
                value = self._min_val
                self._input_str = str(int(value)) if not self._allow_decimal else str(value)
                self._update_display()
                self._show_range_hint()
                return
            elif value > self._max_val:
                value = self._max_val
                self._input_str = str(int(value)) if not self._allow_decimal else str(value)
                self._update_display()
                self._show_range_hint()
                return
            
            self.value_confirmed.emit(value)
            self.accept()
            
        except ValueError:
            self._input_str = ""
            self._update_display()
    
    def _show_range_hint(self):
        """범위 힌트 표시 (테두리 빨간색으로)"""
        self.display_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 2px solid {Colors.RED};
                border-radius: 10px;
            }}
        """)
        # 1초 후 원래대로
        from PySide6.QtCore import QTimer
        QTimer.singleShot(1000, self._reset_display_style)
    
    def _reset_display_style(self):
        """디스플레이 스타일 원래대로"""
        self.display_frame.setStyleSheet(f"""
            QFrame {{
                background-color: {Colors.BG_SECONDARY};
                border: 2px solid {Colors.CYAN};
                border-radius: 10px;
            }}
        """)
    
    def get_value(self) -> float:
        """현재 값 반환"""
        try:
            return float(self._input_str) if self._input_str else 0
        except ValueError:
            return 0
