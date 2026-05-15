"""
VERICOM DLP 3D Printer GUI - Number Dial Component
"""

from PySide6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QPushButton, QFrame
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from styles.colors import Colors
from styles.fonts import Fonts
from styles.icons import Icons
from styles.stylesheets import (
    get_dialog_style, get_dial_value_style, get_dial_number_style,
    get_dial_unit_style, get_dial_label_style, get_dial_cancel_style,
    get_dial_confirm_style, get_control_button_style,
    Spacing, Radius
)


class NumberDial(QDialog):
    """숫자 입력 다이얼 다이얼로그"""
    
    value_changed = Signal(float)
    
    def __init__(self, title: str = "값 설정", initial_value: float = 0,
                 unit: str = "", min_value: float = 0, max_value: float = 9999,
                 step: float = 1, decimals: int = 0, parent=None):
        super().__init__(parent)
        
        self._title = title
        self._value = initial_value
        self._unit = unit
        self._min_value = min_value
        self._max_value = max_value
        self._step = step
        self._decimals = decimals
        
        self.setWindowTitle(title)
        self.setFixedSize(400, 300)
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """UI 구성"""
        self.setStyleSheet(get_dialog_style())
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignCenter)
        
        # 라벨
        self.label = QLabel(self._title)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(get_dial_label_style())
        layout.addWidget(self.label)
        
        # 다이얼 컨테이너
        dial_container = QHBoxLayout()
        dial_container.setSpacing(20)
        dial_container.setAlignment(Qt.AlignCenter)
        
        # 마이너스 버튼
        self.btn_minus = QPushButton()
        self.btn_minus.setFixedSize(60, 60)
        self.btn_minus.setStyleSheet(get_control_button_style())
        self.btn_minus.setCursor(Qt.PointingHandCursor)
        self.btn_minus.setIcon(Icons.get_icon(Icons.MINUS, 24, Colors.NAVY))
        self.btn_minus.clicked.connect(self._decrease)
        
        # 값 표시 영역
        value_frame = QFrame()
        value_frame.setFixedSize(160, 80)
        value_frame.setStyleSheet(get_dial_value_style())

        value_layout = QHBoxLayout(value_frame)
        value_layout.setContentsMargins(10, 0, 10, 0)
        value_layout.setAlignment(Qt.AlignCenter)

        self.value_label = QLabel(self._format_value())
        self.value_label.setFont(Fonts.mono_display())
        self.value_label.setStyleSheet(get_dial_number_style())
        self.value_label.setAlignment(Qt.AlignCenter)

        self.unit_label = QLabel(self._unit)
        self.unit_label.setStyleSheet(get_dial_unit_style())
        self.unit_label.setAlignment(Qt.AlignCenter)
        
        value_layout.addWidget(self.value_label)
        if self._unit:
            value_layout.addWidget(self.unit_label)
        
        # 플러스 버튼
        self.btn_plus = QPushButton()
        self.btn_plus.setFixedSize(60, 60)
        self.btn_plus.setStyleSheet(get_control_button_style())
        self.btn_plus.setCursor(Qt.PointingHandCursor)
        self.btn_plus.setIcon(Icons.get_icon(Icons.PLUS, 24, Colors.NAVY))
        self.btn_plus.clicked.connect(self._increase)
        
        dial_container.addWidget(self.btn_minus)
        dial_container.addWidget(value_frame)
        dial_container.addWidget(self.btn_plus)
        
        layout.addLayout(dial_container)
        
        # 액션 버튼들
        action_layout = QHBoxLayout()
        action_layout.setSpacing(16)
        
        self.btn_cancel = QPushButton("Cancel")
        self.btn_cancel.setFixedSize(140, 50)
        self.btn_cancel.setStyleSheet(get_dial_cancel_style())
        self.btn_cancel.setCursor(Qt.PointingHandCursor)
        self.btn_cancel.setIcon(Icons.get_icon(Icons.X, 18, Colors.TEXT_SECONDARY))
        self.btn_cancel.clicked.connect(self.reject)

        self.btn_confirm = QPushButton("Confirm")
        self.btn_confirm.setFixedSize(140, 50)
        self.btn_confirm.setStyleSheet(get_dial_confirm_style())
        self.btn_confirm.setCursor(Qt.PointingHandCursor)
        self.btn_confirm.setIcon(Icons.get_icon(Icons.CHECK, 18, Colors.WHITE))
        self.btn_confirm.clicked.connect(self._confirm)
        
        action_layout.addWidget(self.btn_cancel)
        action_layout.addWidget(self.btn_confirm)
        
        layout.addLayout(action_layout)
    
    def _format_value(self) -> str:
        """값 포맷팅"""
        if self._decimals == 0:
            return str(int(self._value))
        else:
            return f"{self._value:.{self._decimals}f}"
    
    def _update_display(self):
        """디스플레이 업데이트"""
        self.value_label.setText(self._format_value())
    
    def _increase(self):
        """값 증가"""
        new_value = self._value + self._step
        if new_value <= self._max_value:
            self._value = new_value
            self._update_display()
    
    def _decrease(self):
        """값 감소"""
        new_value = self._value - self._step
        if new_value >= self._min_value:
            self._value = new_value
            self._update_display()
    
    def _confirm(self):
        """확인"""
        self.value_changed.emit(self._value)
        self.accept()
    
    def get_value(self) -> float:
        """현재 값 반환"""
        return self._value
    
    def set_value(self, value: float):
        """값 설정"""
        self._value = max(self._min_value, min(self._max_value, value))
        self._update_display()


class DistanceSelector(QWidget):
    """거리 선택 버튼 그룹"""
    
    distance_changed = Signal(float)
    
    def __init__(self, distances: list = None, default_index: int = 1, 
                 parent=None):
        super().__init__(parent)
        
        if distances is None:
            distances = [0.1, 1.0, 10.0]
        
        self._distances = distances
        self._selected_index = default_index
        self._buttons = []
        
        self._setup_ui()
    
    def _setup_ui(self):
        """UI 구성"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        for i, dist in enumerate(self._distances):
            # 정수면 정수로, 소수면 소수로 표시 (mm 단위 없음)
            if dist == int(dist):
                btn = QPushButton(f"{int(dist)}")
            else:
                btn = QPushButton(f"{dist}")
            btn.setFixedHeight(40)
            btn.setCursor(Qt.PointingHandCursor)
            btn.clicked.connect(lambda checked, idx=i: self._select(idx))

            self._buttons.append(btn)
            layout.addWidget(btn)
        
        self._update_styles()
    
    def _update_styles(self):
        """버튼 스타일 업데이트"""
        from styles.stylesheets import get_distance_button_style, get_distance_button_active_style

        for i, btn in enumerate(self._buttons):
            if i == self._selected_index:
                btn.setStyleSheet(get_distance_button_active_style())
            else:
                btn.setStyleSheet(get_distance_button_style())
    
    def _select(self, index: int):
        """거리 선택"""
        self._selected_index = index
        self._update_styles()
        self.distance_changed.emit(self._distances[index])
    
    def get_selected_distance(self) -> float:
        """선택된 거리 반환"""
        return self._distances[self._selected_index]
