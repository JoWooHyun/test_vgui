"""
VERICOM DLP 3D Printer GUI - Kiosk Manager
키오스크 모드 관리 및 관리자 접근 제어
"""

from PySide6.QtCore import QObject, Signal, QEvent, Qt, QTimer


class KioskManager(QObject):
    """키오스크 모드 관리자 - 단축키 차단 및 관리자 접근"""

    admin_mode_changed = Signal(bool)  # 관리자 모드 변경 시그널

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self._initialized = True

        self._admin_mode = False
        self._enabled = True  # 키오스크 모드 활성화 여부

        # 로고 클릭 카운터
        self._logo_click_count = 0
        self._logo_click_timer = QTimer()
        self._logo_click_timer.setSingleShot(True)
        self._logo_click_timer.timeout.connect(self._reset_logo_clicks)

        # 관리자 모드 자동 해제 타이머 (5분)
        self._admin_timeout_timer = QTimer()
        self._admin_timeout_timer.setSingleShot(True)
        self._admin_timeout_timer.timeout.connect(self._auto_disable_admin)

    def eventFilter(self, obj, event):
        """이벤트 필터 - 단축키 차단"""
        if not self._enabled:
            return False

        if event.type() == QEvent.KeyPress:
            key = event.key()
            modifiers = event.modifiers()

            # Ctrl+Shift+F12 → 관리자 모드 토글
            if (modifiers == (Qt.ControlModifier | Qt.ShiftModifier) and
                key == Qt.Key_F12):
                self.toggle_admin_mode()
                print(f"[Kiosk] Ctrl+Shift+F12 → 관리자 모드: {self._admin_mode}")
                return True  # 이벤트 소비

            # 관리자 모드면 모든 키 허용
            if self._admin_mode:
                return False

            # 차단할 단축키들
            # Alt + F4, Alt + Tab, Alt + Escape
            if modifiers & Qt.AltModifier:
                if key in (Qt.Key_F4, Qt.Key_Tab, Qt.Key_Escape):
                    print(f"[Kiosk] 차단: Alt+{self._key_name(key)}")
                    return True

            # Escape 단독
            if key == Qt.Key_Escape and modifiers == Qt.NoModifier:
                print("[Kiosk] 차단: Escape")
                return True

            # F1-F12 (F12 제외 - 관리자 조합에 사용)
            if Qt.Key_F1 <= key <= Qt.Key_F11:
                print(f"[Kiosk] 차단: F{key - Qt.Key_F1 + 1}")
                return True

            # Windows/Super/Meta 키
            if key in (Qt.Key_Super_L, Qt.Key_Super_R, Qt.Key_Meta):
                print("[Kiosk] 차단: Windows/Super 키")
                return True

            # Ctrl+Alt+Delete (일부 시스템에서 캡처 가능)
            if (modifiers == (Qt.ControlModifier | Qt.AltModifier) and
                key == Qt.Key_Delete):
                print("[Kiosk] 차단: Ctrl+Alt+Delete")
                return True

        return False

    def _key_name(self, key):
        """키 이름 반환"""
        key_names = {
            Qt.Key_F4: "F4",
            Qt.Key_Tab: "Tab",
            Qt.Key_Escape: "Escape",
        }
        return key_names.get(key, f"Key({key})")

    def on_logo_clicked(self):
        """로고 클릭 처리 - 5번 연속 클릭 시 관리자 모드"""
        self._logo_click_count += 1

        # 3초 타이머 리셋
        self._logo_click_timer.stop()
        self._logo_click_timer.start(5000)

        print(f"[Kiosk] 로고 클릭: {self._logo_click_count}/5")

        if self._logo_click_count >= 5:
            self._logo_click_count = 0
            self._logo_click_timer.stop()
            self.toggle_admin_mode()

    def _reset_logo_clicks(self):
        """로고 클릭 카운터 리셋"""
        if self._logo_click_count > 0:
            print(f"[Kiosk] 로고 클릭 리셋 (5초 타임아웃)")
        self._logo_click_count = 0

    def toggle_admin_mode(self):
        """관리자 모드 토글"""
        self.set_admin_mode(not self._admin_mode)

    def set_admin_mode(self, enabled: bool):
        """관리자 모드 설정"""
        if self._admin_mode == enabled:
            return

        self._admin_mode = enabled

        if enabled:
            print("[Kiosk] 관리자 모드 활성화 (5분 후 자동 해제)")
            # 5분 후 자동 해제
            self._admin_timeout_timer.start(5 * 60 * 1000)
        else:
            print("[Kiosk] 관리자 모드 비활성화")
            self._admin_timeout_timer.stop()

        self.admin_mode_changed.emit(enabled)

    def _auto_disable_admin(self):
        """관리자 모드 자동 해제"""
        print("[Kiosk] 관리자 모드 자동 해제 (5분 타임아웃)")
        self.set_admin_mode(False)

    @property
    def is_admin_mode(self) -> bool:
        """관리자 모드 여부"""
        return self._admin_mode

    @property
    def is_enabled(self) -> bool:
        """키오스크 모드 활성화 여부"""
        return self._enabled

    def set_enabled(self, enabled: bool):
        """키오스크 모드 활성화/비활성화"""
        self._enabled = enabled
        print(f"[Kiosk] 키오스크 모드: {'활성화' if enabled else '비활성화'}")


# 전역 인스턴스 가져오기
def get_kiosk_manager() -> KioskManager:
    """키오스크 관리자 인스턴스 가져오기"""
    return KioskManager()
