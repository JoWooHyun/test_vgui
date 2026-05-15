"""
VERICOM DLP 3D Printer GUI - SVG Icons
Lucide-style outlined icons
"""

from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtCore import QByteArray, Qt

try:
    from .colors import Colors
except ImportError:
    from colors import Colors


class Icons:
    """SVG 아이콘 클래스"""
    
    # 기본 아이콘 색상
    DEFAULT_COLOR = Colors.NAVY
    
    # ========== Navigation Icons ==========
    
    ARROW_LEFT = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 12H5M12 19l-7-7 7-7"/>
    </svg>
    """
    
    ARROW_UP = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 19V5M5 12l7-7 7 7"/>
    </svg>
    """
    
    ARROW_DOWN = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 5v14M5 12l7 7 7-7"/>
    </svg>
    """
    
    # ========== Flip Icons ==========
    
    FLIP_HORIZONTAL = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 3v18"/>
        <path d="M16 7l4 5-4 5"/>
        <path d="M8 7l-4 5 4 5"/>
    </svg>
    """
    
    FLIP_VERTICAL = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 12h18"/>
        <path d="M7 8L12 4l5 4"/>
        <path d="M7 16l5 4 5-4"/>
    </svg>
    """
    
    # 이미지 파일 아이콘 (사진)
    IMAGE = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <circle cx="8.5" cy="8.5" r="1.5"/>
        <path d="M21 15l-5-5L5 21"/>
    </svg>
    """
    
    # Checker 패턴 아이콘
    PATTERN_CHECKER = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <rect x="3" y="3" width="9" height="9" fill="{color}" opacity="0.3"/>
        <rect x="12" y="12" width="9" height="9" fill="{color}" opacity="0.3"/>
        <line x1="12" y1="3" x2="12" y2="21"/>
        <line x1="3" y1="12" x2="21" y2="12"/>
    </svg>
    """

    # 로고 패턴 아이콘 (VERICOM V자 부메랑 스타일)
    PATTERN_LOGO = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <path d="M6 8 L12 16 L18 8" stroke-width="3"/>
    </svg>
    """
    
    CHEVRON_UP = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <polyline points="18 15 12 9 6 15"/>
    </svg>
    """
    
    CHEVRON_DOWN = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <polyline points="6 9 12 15 18 9"/>
    </svg>
    """
    
    CHEVRON_LEFT = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <polyline points="15 18 9 12 15 6"/>
    </svg>
    """
    
    CHEVRON_RIGHT = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <polyline points="9 18 15 12 9 6"/>
    </svg>
    """
    
    # ========== Action Icons ==========
    
    HOME = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/>
        <polyline points="9 22 9 12 15 12 15 22"/>
    </svg>
    """
    
    PLAY = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <polygon points="5 3 19 12 5 21 5 3"/>
    </svg>
    """
    
    PAUSE = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="6" y="4" width="4" height="16"/>
        <rect x="14" y="4" width="4" height="16"/>
    </svg>
    """
    
    STOP = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="6" y="6" width="12" height="12" rx="2"/>
    </svg>
    """
    
    STOP_CIRCLE = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <rect x="9" y="9" width="6" height="6" rx="1"/>
    </svg>
    """
    
    CHECK = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <polyline points="20 6 9 17 4 12"/>
    </svg>
    """
    
    X = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <line x1="18" y1="6" x2="6" y2="18"/>
        <line x1="6" y1="6" x2="18" y2="18"/>
    </svg>
    """
    
    PLUS = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="5" x2="12" y2="19"/>
        <line x1="5" y1="12" x2="19" y2="12"/>
    </svg>
    """
    
    MINUS = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <line x1="5" y1="12" x2="19" y2="12"/>
    </svg>
    """
    
    TRASH = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <polyline points="3 6 5 6 21 6"/>
        <path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>
        <line x1="10" y1="11" x2="10" y2="17"/>
        <line x1="14" y1="11" x2="14" y2="17"/>
    </svg>
    """
    
    # ========== Menu Icons ==========
    
    WRENCH = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>
    </svg>
    """
    
    SETTINGS = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" 
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="3"/>
        <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
    </svg>
    """
    
    LAYERS = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" 
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="2" y="6" width="20" height="4" rx="1"/>
        <rect x="4" y="10" width="16" height="4" rx="1"/>
        <rect x="6" y="14" width="12" height="4" rx="1"/>
    </svg>
    """
    
    MOVE = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" 
         stroke-linecap="round" stroke-linejoin="round">
        <polyline points="5 9 2 12 5 15"/>
        <polyline points="9 5 12 2 15 5"/>
        <polyline points="15 19 12 22 9 19"/>
        <polyline points="19 9 22 12 19 15"/>
        <line x1="2" y1="12" x2="22" y2="12"/>
        <line x1="12" y1="2" x2="12" y2="22"/>
    </svg>
    """
    
    SQUARE = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" 
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <rect x="7" y="7" width="10" height="10" rx="1"/>
    </svg>
    """
    
    SQUARE_HALF = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" 
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2"/>
        <line x1="3" y1="12" x2="21" y2="12"/>
    </svg>
    """
    
    BAR_CHART = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 20V10"/>
        <path d="M18 20V4"/>
        <path d="M6 20v-4"/>
        <line x1="4" y1="20" x2="20" y2="20"/>
    </svg>
    """
    
    # ========== Status Icons ==========
    
    FILE = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
        <polyline points="14 2 14 8 20 8"/>
    </svg>
    """
    
    FILE_TEXT = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
        <polyline points="14 2 14 8 20 8"/>
        <line x1="16" y1="13" x2="8" y2="13"/>
        <line x1="16" y1="17" x2="8" y2="17"/>
        <polyline points="10 9 9 9 8 9"/>
    </svg>
    """
    
    FOLDER_OPEN = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
        <line x1="9" y1="14" x2="15" y2="14"/>
    </svg>
    """
    
    EDIT = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5L17 3z"/>
    </svg>
    """
    
    CLOCK = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <polyline points="12 6 12 12 16 14"/>
    </svg>
    """
    
    HOURGLASS = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 22h14"/>
        <path d="M5 2h14"/>
        <path d="M17 22v-4.172a2 2 0 0 0-.586-1.414L12 12l-4.414 4.414A2 2 0 0 0 7 17.828V22"/>
        <path d="M7 2v4.172a2 2 0 0 0 .586 1.414L12 12l4.414-4.414A2 2 0 0 0 17 6.172V2"/>
    </svg>
    """
    
    INFO = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="16" x2="12" y2="12"/>
        <line x1="12" y1="8" x2="12.01" y2="8"/>
    </svg>
    """
    
    ALERT_CIRCLE = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <line x1="12" y1="8" x2="12" y2="12"/>
        <line x1="12" y1="16" x2="12.01" y2="16"/>
    </svg>
    """
    
    USB = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="10" cy="7" r="1"/>
        <circle cx="4" cy="20" r="1"/>
        <path d="M4.5 19.5L12 12l-3-3"/>
        <path d="M12 12v-2l4-4"/>
        <path d="M18 6l-2 2 2 2"/>
        <path d="M12 7v5"/>
    </svg>
    """
    
    # ========== System Icons ==========
    
    GLOBE = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <line x1="2" y1="12" x2="22" y2="12"/>
        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
    </svg>
    """
    
    MAIL = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" 
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="2" y="4" width="20" height="16" rx="2"/>
        <path d="M22 6l-10 7L2 6"/>
    </svg>
    """
    
    WIFI = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 12.55a11 11 0 0 1 14.08 0"/>
        <path d="M1.42 9a16 16 0 0 1 21.16 0"/>
        <path d="M8.53 16.11a6 6 0 0 1 6.95 0"/>
        <circle cx="12" cy="20" r="1"/>
    </svg>
    """

    # ========== Theme Icon ==========

    SUN = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="5"/>
        <line x1="12" y1="1" x2="12" y2="3"/>
        <line x1="12" y1="21" x2="12" y2="23"/>
        <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
        <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
        <line x1="1" y1="12" x2="3" y2="12"/>
        <line x1="21" y1="12" x2="23" y2="12"/>
        <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
        <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
    </svg>
    """

    MOON = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
    </svg>
    """

    CONTRAST = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"/>
        <path d="M12 2a10 10 0 0 1 0 20z" fill="{color}"/>
    </svg>
    """

    # ========== Calibration Icon ==========

    CALIBRATION = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="3"/>
        <path d="M12 2v4"/>
        <path d="M12 18v4"/>
        <path d="M2 12h4"/>
        <path d="M18 12h4"/>
        <path d="M4.93 4.93l2.83 2.83"/>
        <path d="M16.24 16.24l2.83 2.83"/>
        <path d="M4.93 19.07l2.83-2.83"/>
        <path d="M16.24 7.76l2.83-2.83"/>
    </svg>
    """

    # ========== Leveling Icons ==========

    LEVEL = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <line x1="2" y1="18" x2="22" y2="18"/>
        <path d="M12 6l-6 8h12z"/>
        <line x1="12" y1="10" x2="12" y2="14"/>
        <circle cx="12" cy="9" r="1" fill="{color}" stroke="none"/>
    </svg>
    """

    HOME_Z = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 19V5"/>
        <path d="M5 12l7-7 7 7"/>
        <text x="20" y="22" font-size="8" font-weight="bold" fill="{color}" stroke="none" font-family="Arial">Z</text>
    </svg>
    """

    HOME_X = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 12H5"/>
        <path d="M12 5l-7 7 7 7"/>
        <text x="18" y="22" font-size="8" font-weight="bold" fill="{color}" stroke="none" font-family="Arial">X</text>
    </svg>
    """

    X_MOVE = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 12h14"/>
        <path d="M15 8l4 4-4 4"/>
        <text x="1" y="22" font-size="8" font-weight="bold" fill="{color}" stroke="none" font-family="Arial">X</text>
        <text x="13" y="22" font-size="7" fill="{color}" stroke="none" font-family="Arial">75</text>
    </svg>
    """

    # ========== Priming Icons ==========

    PUMP_HOME = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="6" y="4" width="12" height="14" rx="2"/>
        <line x1="12" y1="18" x2="12" y2="22"/>
        <line x1="9" y1="22" x2="15" y2="22"/>
        <path d="M9 1h6"/>
        <path d="M12 1v3"/>
    </svg>
    """

    PUMP_FILL = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="6" y="8" width="12" height="14" rx="2"/>
        <line x1="12" y1="8" x2="12" y2="2"/>
        <path d="M8 5l4-3 4 3"/>
    </svg>
    """

    # ========== Print Info Icons ==========

    STACK = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2L2 7l10 5 10-5-10-5z"/>
        <path d="M2 17l10 5 10-5"/>
        <path d="M2 12l10 5 10-5"/>
    </svg>
    """

    TIMER = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="13" r="8"/>
        <path d="M12 9v4l2 2"/>
        <path d="M9 2h6"/>
        <path d="M12 2v2"/>
    </svg>
    """

    RULER = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M21.3 8.7L8.7 21.3c-1 1-2.5 1-3.4 0l-2.6-2.6c-1-1-1-2.5 0-3.4L15.3 2.7c1-1 2.5-1 3.4 0l2.6 2.6c1 1 1 2.5 0 3.4z"/>
        <path d="M7.5 10.5l2 2"/>
        <path d="M10.5 7.5l2 2"/>
        <path d="M13.5 4.5l2 2"/>
    </svg>
    """

    SUNRISE = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M17 18a5 5 0 0 0-10 0"/>
        <line x1="12" y1="9" x2="12" y2="2"/>
        <line x1="4.22" y1="10.22" x2="5.64" y2="11.64"/>
        <line x1="1" y1="18" x2="3" y2="18"/>
        <line x1="21" y1="18" x2="23" y2="18"/>
        <line x1="18.36" y1="11.64" x2="19.78" y2="10.22"/>
        <line x1="23" y1="22" x2="1" y2="22"/>
    </svg>
    """

    ZAP = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>
    </svg>
    """

    # 일반 레이어 노출 (위쪽 광선 + 레이어)
    EXPOSURE_NORMAL = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <line x1="12" y1="2" x2="12" y2="5"/>
        <line x1="6" y1="4" x2="7.5" y2="6"/>
        <line x1="18" y1="4" x2="16.5" y2="6"/>
        <line x1="4" y1="8" x2="6" y2="9"/>
        <line x1="20" y1="8" x2="18" y2="9"/>
        <path d="M5 13l7 4 7-4"/>
        <path d="M5 17l7 4 7-4"/>
    </svg>
    """

    # 바닥 레이어 노출 (레이어 + 바닥선)
    EXPOSURE_BOTTOM = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 8l7 4 7-4"/>
        <path d="M5 12l7 4 7-4"/>
        <line x1="3" y1="20" x2="21" y2="20"/>
        <line x1="6" y1="17" x2="6" y2="20"/>
        <line x1="12" y1="17" x2="12" y2="20"/>
        <line x1="18" y1="17" x2="18" y2="20"/>
    </svg>
    """

    # 바닥 레이어 개수 (층층이 쌓인 레이어 + 하단 강조)
    BOTTOM_LAYERS = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M5 6l7 3 7-3"/>
        <path d="M5 10l7 3 7-3"/>
        <path d="M5 14l7 3 7-3"/>
        <rect x="4" y="18" width="16" height="3" rx="1" fill="{color}" stroke="none"/>
    </svg>
    """

    # 블레이드 속도 (블레이드 + 화살표)
    BLADE_SPEED = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="2" y="10" width="20" height="4" rx="1"/>
        <path d="M18 6l4 4-4 4"/>
        <line x1="14" y1="10" x2="14" y2="14"/>
    </svg>
    """

    # 소재 (비커/플라스크)
    MATERIAL = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 3h6"/>
        <path d="M10 3v5.172a2 2 0 0 1-.586 1.414L5 14l1.5 6.5h11L19 14l-4.414-4.414A2 2 0 0 1 14 8.172V3"/>
        <path d="M7 17h10"/>
    </svg>
    """

    # LED 파워 (전구 + 광선)
    LED_POWER = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M9 18h6"/>
        <path d="M10 22h4"/>
        <path d="M12 2v2"/>
        <path d="M4.93 4.93l1.41 1.41"/>
        <path d="M19.07 4.93l-1.41 1.41"/>
        <path d="M2 12h2"/>
        <path d="M20 12h2"/>
        <path d="M15 14.5A3 3 0 0 0 9 14.5"/>
        <circle cx="12" cy="10" r="4"/>
    </svg>
    """

    # 레진 잔량 게이지 (배터리/레벨)
    RESIN_LEVEL = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <rect x="6" y="4" width="12" height="18" rx="2"/>
        <rect x="9" y="1" width="6" height="3" rx="1"/>
        <rect x="9" y="12" width="6" height="7" rx="1" fill="{color}" stroke="none"/>
    </svg>
    """

    # 주사기/토출 (syringe)
    SYRINGE = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M17 3l4 4"/>
        <path d="M19 5L7.5 16.5"/>
        <path d="M5.5 14.5L3 22l7.5-2.5"/>
        <path d="M9 11l4 4"/>
        <path d="M11 9l4 4"/>
    </svg>
    """

    # 토출 속도 (물방울 + 속도)
    DISPENSE_SPEED = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"/>
        <path d="M9 13l3-3 3 3"/>
    </svg>
    """

    # 대기 시간 (모래시계/일시정지)
    DELAY = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M6 2h12"/>
        <path d="M6 22h12"/>
        <path d="M7 2v4l5 6-5 6v4"/>
        <path d="M17 2v4l-5 6 5 6v4"/>
    </svg>
    """

    # 반복/사이클 (회전 화살표)
    CYCLE = """
    <svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 2v6h-6"/>
        <path d="M3 12a9 9 0 0 1 15-6.7L21 8"/>
        <path d="M3 22v-6h6"/>
        <path d="M21 12a9 9 0 0 1-15 6.7L3 16"/>
    </svg>
    """

    @staticmethod
    def get_pixmap(svg_template: str, size: int = 24,
                   color: str = None) -> QPixmap:
        """SVG 템플릿에서 QPixmap 생성"""
        if color is None:
            color = Icons.DEFAULT_COLOR
        
        svg_data = svg_template.format(color=color)
        
        renderer = QSvgRenderer(QByteArray(svg_data.encode()))
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        
        return pixmap
    
    @staticmethod
    def get_icon(svg_template: str, size: int = 24, 
                 color: str = None) -> QIcon:
        """SVG 템플릿에서 QIcon 생성"""
        pixmap = Icons.get_pixmap(svg_template, size, color)
        return QIcon(pixmap)
