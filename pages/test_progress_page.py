"""
Test VGUI - Test Progress Page
프린트 진행 상황 표시 + Stop/Pause/Resume
"""

import time as _time

from PySide6.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton
)
from PySide6.QtCore import Signal, Qt, QTimer

from pages.base_page import BasePage
from styles.colors import Colors
from styles.fonts import Fonts
from styles.stylesheets import Radius


class TestProgressPage(BasePage):
    """테스트 프린트 진행 페이지"""

    go_home = Signal()
    pause_requested = Signal()
    resume_requested = Signal()
    stop_requested = Signal()

    def __init__(self, parent=None):
        super().__init__("Print Test Progress", show_back=False, parent=parent)
        self._is_paused = False
        self._start_time = 0
        self._total_layers = 0
        self._current_layer = 0
        self._setup_content()

        # 경과 시간 타이머
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._update_elapsed)
        self._timer.setInterval(1000)

    def _setup_content(self):
        self.content_layout.setContentsMargins(30, 20, 30, 20)
        self.content_layout.setSpacing(15)

        # 상태 라벨
        self.lbl_status = QLabel("Initializing...")
        self.lbl_status.setFont(Fonts.h2())
        self.lbl_status.setAlignment(Qt.AlignCenter)
        self.lbl_status.setStyleSheet(f"color: {Colors.CYAN}; font-weight: bold;")
        self.content_layout.addWidget(self.lbl_status)

        # 레이어 진행
        self.lbl_layer = QLabel("Layer: 0 / 0")
        self.lbl_layer.setFont(Fonts.h1())
        self.lbl_layer.setAlignment(Qt.AlignCenter)
        self.lbl_layer.setStyleSheet(f"color: {Colors.TEXT_PRIMARY}; font-weight: bold;")
        self.content_layout.addWidget(self.lbl_layer)

        # 시간 정보 행
        time_row = QHBoxLayout()
        time_row.setSpacing(40)

        # 경과 시간
        elapsed_col = QVBoxLayout()
        lbl_elapsed_title = QLabel("Elapsed")
        lbl_elapsed_title.setFont(Fonts.caption())
        lbl_elapsed_title.setAlignment(Qt.AlignCenter)
        lbl_elapsed_title.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        elapsed_col.addWidget(lbl_elapsed_title)

        self.lbl_elapsed = QLabel("00:00:00")
        self.lbl_elapsed.setFont(Fonts.h2())
        self.lbl_elapsed.setAlignment(Qt.AlignCenter)
        self.lbl_elapsed.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        elapsed_col.addWidget(self.lbl_elapsed)
        time_row.addLayout(elapsed_col)

        # 예상 남은 시간
        remain_col = QVBoxLayout()
        lbl_remain_title = QLabel("Remaining")
        lbl_remain_title.setFont(Fonts.caption())
        lbl_remain_title.setAlignment(Qt.AlignCenter)
        lbl_remain_title.setStyleSheet(f"color: {Colors.TEXT_SECONDARY};")
        remain_col.addWidget(lbl_remain_title)

        self.lbl_remaining = QLabel("--:--:--")
        self.lbl_remaining.setFont(Fonts.h2())
        self.lbl_remaining.setAlignment(Qt.AlignCenter)
        self.lbl_remaining.setStyleSheet(f"color: {Colors.TEXT_PRIMARY};")
        remain_col.addWidget(self.lbl_remaining)
        time_row.addLayout(remain_col)

        self.content_layout.addLayout(time_row)
        self.content_layout.addStretch()

        # 버튼 행
        btn_row = QHBoxLayout()
        btn_row.setSpacing(20)

        # Pause/Resume 버튼
        self.btn_pause = QPushButton("PAUSE")
        self.btn_pause.setFixedSize(200, 55)
        self.btn_pause.setFont(Fonts.h3())
        self.btn_pause.setCursor(Qt.PointingHandCursor)
        self.btn_pause.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.AMBER};
                border: none;
                border-radius: {Radius.LG}px;
                color: {Colors.WHITE};
                font-weight: bold;
            }}
            QPushButton:pressed {{
                opacity: 0.8;
            }}
        """)
        self.btn_pause.clicked.connect(self._on_pause_resume)
        btn_row.addWidget(self.btn_pause)

        # Stop 버튼
        self.btn_stop = QPushButton("STOP")
        self.btn_stop.setFixedSize(200, 55)
        self.btn_stop.setFont(Fonts.h3())
        self.btn_stop.setCursor(Qt.PointingHandCursor)
        self.btn_stop.setStyleSheet(f"""
            QPushButton {{
                background-color: {Colors.RED};
                border: none;
                border-radius: {Radius.LG}px;
                color: {Colors.WHITE};
                font-weight: bold;
            }}
            QPushButton:pressed {{
                opacity: 0.8;
            }}
        """)
        self.btn_stop.clicked.connect(self.stop_requested.emit)
        btn_row.addWidget(self.btn_stop)

        # Home 버튼 (완료/정지 후에만 보임)
        self.btn_home = QPushButton("HOME")
        self.btn_home.setFixedSize(200, 55)
        self.btn_home.setFont(Fonts.h3())
        self.btn_home.setCursor(Qt.PointingHandCursor)
        self.btn_home.setStyleSheet(f"""
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
        self.btn_home.clicked.connect(self.go_home.emit)
        self.btn_home.hide()
        btn_row.addWidget(self.btn_home)

        self.content_layout.addLayout(btn_row)

    def start_progress(self, total_layers: int):
        """프린트 시작"""
        self._total_layers = total_layers
        self._current_layer = 0
        self._start_time = _time.monotonic()
        self._is_paused = False

        self.lbl_status.setText("Printing...")
        self.lbl_status.setStyleSheet(f"color: {Colors.CYAN}; font-weight: bold;")
        self.lbl_layer.setText(f"Layer: 0 / {total_layers}")
        self.lbl_elapsed.setText("00:00:00")
        self.lbl_remaining.setText("--:--:--")

        self.btn_pause.show()
        self.btn_pause.setText("PAUSE")
        self.btn_stop.show()
        self.btn_home.hide()

        self._timer.start()

    def update_progress(self, current: int, total: int):
        """진행 업데이트"""
        self._current_layer = current
        self._total_layers = total
        self.lbl_layer.setText(f"Layer: {current} / {total}")

        # 남은 시간 계산
        if current > 0:
            elapsed = _time.monotonic() - self._start_time
            per_layer = elapsed / current
            remaining = per_layer * (total - current)
            self.lbl_remaining.setText(self._format_time(remaining))

    def show_completed(self):
        """완료"""
        self._timer.stop()
        self.lbl_status.setText("COMPLETED")
        self.lbl_status.setStyleSheet(f"color: {Colors.GREEN}; font-weight: bold;")
        self.btn_pause.hide()
        self.btn_stop.hide()
        self.btn_home.show()

    def show_stopped(self):
        """정지됨"""
        self._timer.stop()
        self.lbl_status.setText("STOPPED")
        self.lbl_status.setStyleSheet(f"color: {Colors.RED}; font-weight: bold;")
        self.btn_pause.hide()
        self.btn_stop.hide()
        self.btn_home.show()

    def show_error(self, message: str):
        """에러"""
        self._timer.stop()
        self.lbl_status.setText(f"ERROR: {message}")
        self.lbl_status.setStyleSheet(f"color: {Colors.RED}; font-weight: bold;")
        self.btn_pause.hide()
        self.btn_stop.hide()
        self.btn_home.show()

    def _on_pause_resume(self):
        if self._is_paused:
            self._is_paused = False
            self.btn_pause.setText("PAUSE")
            self.lbl_status.setText("Printing...")
            self.lbl_status.setStyleSheet(f"color: {Colors.CYAN}; font-weight: bold;")
            self.resume_requested.emit()
        else:
            self._is_paused = True
            self.btn_pause.setText("RESUME")
            self.lbl_status.setText("PAUSED")
            self.lbl_status.setStyleSheet(f"color: {Colors.AMBER}; font-weight: bold;")
            self.pause_requested.emit()

    def _update_elapsed(self):
        elapsed = _time.monotonic() - self._start_time
        self.lbl_elapsed.setText(self._format_time(elapsed))

    @staticmethod
    def _format_time(seconds: float) -> str:
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
