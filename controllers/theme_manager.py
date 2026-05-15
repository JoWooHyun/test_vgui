"""
VERICOM DLP 3D Printer GUI - Theme Manager
Manages dynamic theme switching (Light/Dark/High Contrast)
"""

from PySide6.QtCore import QObject, Signal
from controllers.settings_manager import SettingsManager
from styles.colors import Colors


class ThemeColors:
    """테마별 색상 정의"""

    # ========== Light Theme ==========
    LIGHT = {
        "name": "Light",
        # Core
        "NAVY": "#1E3A5F",           # Primary
        "NAVY_LIGHT": "#2D4A6F",
        "NAVY_DARK": "#152C4A",
        "CYAN": "#06B6D4",           # Accent
        "CYAN_LIGHT": "#67E8F9",     # Highlight
        "CYAN_DARK": "#0891B2",
        # Semantic
        "RED": "#DC2626",            # Danger
        "RED_LIGHT": "#FEE2E2",
        "RED_DARK": "#B91C1C",
        "TEAL": "#14B8A6",
        "TEAL_LIGHT": "#CCFBF1",
        "AMBER": "#F59E0B",          # Warning
        "AMBER_LIGHT": "#FEF3C7",
        "GREEN": "#16A34A",          # Success
        "GREEN_LIGHT": "#DCFCE7",
        # Neutral
        "WHITE": "#FFFFFF",
        "BG_PRIMARY": "#FFFFFF",
        "BG_SECONDARY": "#F3F6FA",
        "BG_TERTIARY": "#E5EAF0",
        "BORDER": "#CBD5E1",
        "BORDER_LIGHT": "#E2E8F0",
        "TEXT_PRIMARY": "#334155",
        "TEXT_SECONDARY": "#64748B",
        "TEXT_DISABLED": "#94A3B8",
        "TEXT_EMPHASIS": "#0F172A",
    }

    # ========== Dark Theme (산업용 메인) ==========
    DARK = {
        "name": "Dark",
        # Core
        "NAVY": "#3B82F6",           # Primary (밝은 블루)
        "NAVY_LIGHT": "#60A5FA",
        "NAVY_DARK": "#2563EB",
        "CYAN": "#22D3EE",           # Accent
        "CYAN_LIGHT": "#7DD3FC",     # Highlight
        "CYAN_DARK": "#06B6D4",
        # Semantic
        "RED": "#F87171",            # Danger
        "RED_LIGHT": "#450A0A",
        "RED_DARK": "#DC2626",
        "TEAL": "#2DD4BF",
        "TEAL_LIGHT": "#134E4A",
        "AMBER": "#FBBF24",          # Warning
        "AMBER_LIGHT": "#78350F",
        "GREEN": "#4ADE80",          # Success
        "GREEN_LIGHT": "#14532D",
        # Neutral
        "WHITE": "#FFFFFF",
        "BG_PRIMARY": "#121826",     # 어두운 배경
        "BG_SECONDARY": "#1E293B",   # 카드 배경
        "BG_TERTIARY": "#334155",    # 비활성 배경
        "BORDER": "#334155",
        "BORDER_LIGHT": "#1E293B",
        "TEXT_PRIMARY": "#E5E7EB",   # 밝은 텍스트
        "TEXT_SECONDARY": "#9CA3AF",
        "TEXT_DISABLED": "#6B7280",
        "TEXT_EMPHASIS": "#FFFFFF",
    }



class ThemeManager(QObject):
    """테마 관리자 - 싱글톤"""

    theme_changed = Signal(str)  # 테마 변경 시그널

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

        self._current_theme = "Light"
        self._themes = {
            "Light": ThemeColors.LIGHT,
            "Dark": ThemeColors.DARK,
        }

        # 저장된 테마 로드
        self._load_theme()

    def _load_theme(self):
        """저장된 테마 설정 로드 및 적용"""
        settings = SettingsManager()
        saved_theme = settings.get("theme", "Light")
        if saved_theme in self._themes:
            self._current_theme = saved_theme
            # Colors 클래스에 테마 적용
            Colors.apply_theme(self._themes[self._current_theme])

    def _save_theme(self):
        """현재 테마 설정 저장"""
        settings = SettingsManager()
        settings.set("theme", self._current_theme)

    @property
    def current_theme(self) -> str:
        """현재 테마 이름"""
        return self._current_theme

    @property
    def colors(self) -> dict:
        """현재 테마 색상"""
        return self._themes[self._current_theme]

    def get_color(self, name: str) -> str:
        """특정 색상 가져오기"""
        return self.colors.get(name, "#000000")

    def set_theme(self, theme_name: str):
        """테마 변경"""
        if theme_name in self._themes and theme_name != self._current_theme:
            self._current_theme = theme_name
            # Colors 클래스에 테마 적용
            Colors.apply_theme(self._themes[self._current_theme])
            self._save_theme()
            self.theme_changed.emit(theme_name)

    def get_available_themes(self) -> list:
        """사용 가능한 테마 목록"""
        return list(self._themes.keys())

    @classmethod
    def with_alpha(cls, hex_color: str, alpha: float) -> str:
        """HEX 컬러를 RGBA로 변환"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r}, {g}, {b}, {alpha})"


# 전역 인스턴스
_theme_manager = None

def get_theme_manager() -> ThemeManager:
    """테마 매니저 인스턴스 가져오기"""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
