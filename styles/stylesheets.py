"""
VERICOM DLP 3D Printer GUI - Stylesheets
모든 컴포넌트의 QSS 스타일 정의
동적 테마 지원을 위해 함수 형태로 제공
"""

from .colors import Colors


class Spacing:
    """간격 시스템"""
    XS = 4
    SM = 8
    MD = 12
    LG = 16
    XL = 20
    XXL = 24
    XXXL = 32


class Radius:
    """모서리 반경"""
    SM = 8
    MD = 12
    LG = 16
    XL = 20


# ============================================================
# 동적 스타일 함수들 (테마 변경 시 호출)
# ============================================================

def get_global_style():
    """글로벌 스타일"""
    return f"""
QMainWindow {{
    background-color: {Colors.BG_PRIMARY};
}}

QStackedWidget {{
    background-color: {Colors.BG_PRIMARY};
}}

QWidget {{
    font-family: "Pretendard", "Noto Sans KR", sans-serif;
}}

QLabel {{
    color: {Colors.TEXT_PRIMARY};
}}
"""

def get_tool_button_style():
    """도구 버튼 스타일"""
    return f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.LG}px;
    color: {Colors.NAVY};
    font-size: 16px;
    font-weight: 600;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
    border-color: {Colors.CYAN};
}}
"""

def get_tool_button_danger_style():
    """도구 버튼 위험 스타일"""
    return f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.RED};
    border-radius: {Radius.LG}px;
    color: {Colors.RED};
    font-size: 16px;
    font-weight: 600;
}}
QPushButton:pressed {{
    background-color: {Colors.RED_LIGHT};
}}
"""

def get_main_menu_button_style():
    """메인 메뉴 버튼 스타일"""
    return f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.XL}px;
    color: {Colors.NAVY};
    font-size: 20px;
    font-weight: 600;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
    border-color: {Colors.CYAN};
}}
"""

def get_back_button_style():
    """뒤로가기 버튼 스타일"""
    return f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.NAVY};
    border-radius: 10px;
    padding: 0px;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
}}
"""

def get_header_style():
    """헤더 스타일"""
    return f"""
QWidget#header {{
    background-color: {Colors.BG_PRIMARY};
    border-bottom: 1px solid {Colors.BORDER};
}}
"""

def get_header_title_style():
    """헤더 타이틀 스타일"""
    return f"""
QLabel {{
    color: {Colors.NAVY};
    font-size: 18px;
    font-weight: 600;
}}
"""

def get_dialog_style():
    """다이얼로그 스타일"""
    return f"""
QDialog {{
    background-color: {Colors.BG_PRIMARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.LG}px;
}}
"""

def get_dial_value_style():
    """다이얼 값 프레임 스타일"""
    return f"""
QFrame {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.CYAN};
    border-radius: {Radius.LG}px;
}}
"""

def get_dial_number_style():
    """다이얼 숫자 스타일"""
    return f"""
QLabel {{
    color: {Colors.NAVY};
    font-size: 42px;
    font-weight: 700;
    background-color: {Colors.BG_SECONDARY};
    border: none;
}}
"""

def get_dial_unit_style():
    """다이얼 단위 스타일"""
    return f"""
QLabel {{
    color: {Colors.TEXT_SECONDARY};
    font-size: 18px;
    background-color: {Colors.BG_SECONDARY};
    border: none;
}}
"""

def get_dial_label_style():
    """다이얼 라벨 스타일"""
    return f"""
QLabel {{
    color: {Colors.TEXT_SECONDARY};
    font-size: 16px;
    background-color: transparent;
}}
"""

def get_dial_cancel_style():
    """다이얼 취소 버튼 스타일"""
    return f"""
QPushButton {{
    background-color: {Colors.BG_PRIMARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.MD}px;
    color: {Colors.TEXT_SECONDARY};
    font-size: 16px;
    font-weight: 600;
    padding: 12px 24px;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
}}
"""

def get_dial_confirm_style():
    """다이얼 확인 버튼 스타일"""
    return f"""
QPushButton {{
    background-color: {Colors.NAVY};
    border: none;
    border-radius: {Radius.MD}px;
    color: {Colors.WHITE};
    font-size: 16px;
    font-weight: 600;
    padding: 12px 24px;
}}
QPushButton:pressed {{
    background-color: {Colors.NAVY_DARK};
}}
"""

def get_control_button_style():
    """컨트롤 버튼 스타일 (다이얼 +/- 버튼)"""
    return f"""
QPushButton {{
    background-color: {Colors.BG_PRIMARY};
    border: 2px solid {Colors.NAVY};
    border-radius: {Radius.LG}px;
    padding: 0px;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
}}
"""

# ============================================================
# 글로벌 스타일 (정적 - 하위 호환성)
# ============================================================

GLOBAL_STYLE = f"""
QMainWindow {{
    background-color: {Colors.BG_PRIMARY};
}}

QWidget {{
    font-family: "Pretendard", "Noto Sans KR", sans-serif;
}}

QLabel {{
    color: {Colors.TEXT_PRIMARY};
}}
"""


# ============================================================
# 헤더 스타일
# ============================================================

HEADER_STYLE = f"""
QWidget#header {{
    background-color: {Colors.BG_SECONDARY};
    border-bottom: 1px solid {Colors.BORDER};
}}
"""

HEADER_TITLE_STYLE = f"""
QLabel {{
    color: {Colors.NAVY};
    font-size: 18px;
    font-weight: 600;
}}
"""


# ============================================================
# 버튼 스타일
# ============================================================

# Primary Button (네이비 배경)
BUTTON_PRIMARY_STYLE = f"""
QPushButton {{
    background-color: {Colors.NAVY};
    border: none;
    border-radius: {Radius.MD}px;
    color: {Colors.WHITE};
    font-size: 16px;
    font-weight: 600;
    padding: 14px 24px;
    min-height: 50px;
}}
QPushButton:pressed {{
    background-color: {Colors.NAVY_DARK};
}}
QPushButton:disabled {{
    background-color: {Colors.BG_TERTIARY};
    color: {Colors.TEXT_DISABLED};
}}
"""

# Secondary Button (흰 배경, 테두리)
BUTTON_SECONDARY_STYLE = f"""
QPushButton {{
    background-color: {Colors.BG_PRIMARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.MD}px;
    color: {Colors.TEXT_PRIMARY};
    font-size: 16px;
    font-weight: 600;
    padding: 14px 24px;
    min-height: 50px;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
    border-color: {Colors.NAVY};
}}
QPushButton:disabled {{
    background-color: {Colors.BG_TERTIARY};
    color: {Colors.TEXT_DISABLED};
}}
"""

# Icon Button (회색 배경, 테두리)
BUTTON_ICON_STYLE = f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.LG}px;
    padding: 0px;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
    border-color: {Colors.NAVY};
}}
QPushButton:disabled {{
    background-color: {Colors.BG_TERTIARY};
    opacity: 0.6;
}}
"""

# Icon Button Active (시안 테두리)
BUTTON_ICON_ACTIVE_STYLE = f"""
QPushButton {{
    background-color: {Colors.CYAN_ALPHA_10};
    border: 2px solid {Colors.CYAN};
    border-radius: {Radius.LG}px;
    padding: 0px;
}}
QPushButton:pressed {{
    background-color: {Colors.CYAN_ALPHA_20};
}}
"""

# Danger Button (빨간색)
BUTTON_DANGER_STYLE = f"""
QPushButton {{
    background-color: {Colors.RED_LIGHT};
    border: 2px solid {Colors.RED};
    border-radius: {Radius.MD}px;
    color: {Colors.RED};
    font-size: 16px;
    font-weight: 600;
    padding: 14px 24px;
}}
QPushButton:pressed {{
    background-color: #FECACA;
}}
"""

# Stop Button (큰 빨간 버튼)
BUTTON_STOP_STYLE = f"""
QPushButton {{
    background-color: {Colors.RED_LIGHT};
    border: 2px solid {Colors.RED};
    border-radius: {Radius.MD}px;
    color: {Colors.RED};
    font-size: 14px;
    font-weight: 600;
}}
QPushButton:pressed {{
    background-color: #FECACA;
    border-color: {Colors.RED_DARK};
}}
"""

# Main Menu Button (큰 사각 버튼)
BUTTON_MAIN_MENU_STYLE = f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.XL}px;
    color: {Colors.NAVY};
    font-size: 20px;
    font-weight: 600;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
    border-color: {Colors.CYAN};
}}
"""

# Tool Button (도구 메뉴 버튼)
BUTTON_TOOL_STYLE = f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.LG}px;
    color: {Colors.NAVY};
    font-size: 16px;
    font-weight: 600;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
    border-color: {Colors.CYAN};
}}
"""

# Tool Button Danger (STOP 버튼용)
BUTTON_TOOL_DANGER_STYLE = f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.RED};
    border-radius: {Radius.LG}px;
    color: {Colors.RED};
    font-size: 16px;
    font-weight: 600;
}}
QPushButton:pressed {{
    background-color: {Colors.RED_LIGHT};
}}
"""

# Back Button (헤더용)
BUTTON_BACK_STYLE = f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.NAVY};
    border-radius: 10px;
    padding: 0px;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
}}
"""

# Distance Selector Button (거리 선택)
BUTTON_DISTANCE_STYLE = f"""
QPushButton {{
    background-color: {Colors.BG_PRIMARY};
    border: 2px solid {Colors.BORDER};
    border-radius: 10px;
    color: {Colors.TEXT_SECONDARY};
    font-size: 14px;
    font-weight: 600;
    padding: 10px;
}}
QPushButton:pressed {{
    border-color: {Colors.CYAN};
    color: {Colors.CYAN};
}}
"""

BUTTON_DISTANCE_ACTIVE_STYLE = f"""
QPushButton {{
    background-color: {Colors.CYAN_ALPHA_10};
    border: 2px solid {Colors.CYAN};
    border-radius: 10px;
    color: {Colors.CYAN};
    font-size: 14px;
    font-weight: 600;
    padding: 10px;
}}
"""

# Control Button (방향키 등)
def get_button_control_style():
    """방향 제어 버튼 스타일 (동적)"""
    return f"""
QPushButton {{
    background-color: {Colors.BG_PRIMARY};
    border: 2px solid {Colors.NAVY};
    border-radius: {Radius.LG}px;
    padding: 0px;
}}
QPushButton:pressed {{
    background-color: {Colors.NAVY_ALPHA_10};
}}
"""

BUTTON_CONTROL_STYLE = get_button_control_style()

# Home Button (홈 버튼 - 시안)
def get_button_home_style():
    """홈 버튼 스타일 (동적)"""
    return f"""
QPushButton {{
    background-color: {Colors.BG_PRIMARY};
    border: 2px solid {Colors.CYAN};
    border-radius: {Radius.LG}px;
    padding: 0px;
}}
QPushButton:pressed {{
    background-color: {Colors.CYAN_ALPHA_10};
}}
"""

BUTTON_HOME_STYLE = get_button_home_style()


def get_button_nav_style():
    """네비게이션 버튼 스타일 (동적)"""
    return f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.MD}px;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
}}
"""


# Nav Button (네비게이션) - 호환성을 위해 유지
BUTTON_NAV_STYLE = get_button_nav_style()

# File Item Button
BUTTON_FILE_ITEM_STYLE = f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.MD}px;
    text-align: center;
}}
QPushButton:pressed {{
    border-color: {Colors.CYAN};
}}
"""

BUTTON_FILE_ITEM_SELECTED_STYLE = f"""
QPushButton {{
    background-color: {Colors.NAVY_ALPHA_10};
    border: 2px solid {Colors.NAVY};
    border-radius: {Radius.MD}px;
    text-align: center;
}}
"""

# Progress Action Button
BUTTON_PROGRESS_ACTION_STYLE = f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.LG}px;
    color: {Colors.TEXT_SECONDARY};
    font-size: 11px;
    font-weight: 600;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
}}
"""

BUTTON_PROGRESS_STOP_STYLE = f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.RED};
    border-radius: {Radius.LG}px;
    color: {Colors.RED};
    font-size: 11px;
    font-weight: 600;
}}
QPushButton:pressed {{
    background-color: {Colors.RED_LIGHT};
}}
"""

BUTTON_PROGRESS_PAUSE_STYLE = f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.CYAN};
    border-radius: {Radius.LG}px;
    color: {Colors.CYAN};
    font-size: 11px;
    font-weight: 600;
}}
QPushButton:pressed {{
    background-color: {Colors.CYAN_ALPHA_10};
}}
"""

# Dial Action Buttons
BUTTON_DIAL_CANCEL_STYLE = f"""
QPushButton {{
    background-color: {Colors.BG_PRIMARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.MD}px;
    color: {Colors.TEXT_SECONDARY};
    font-size: 16px;
    font-weight: 600;
    padding: 12px 24px;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
}}
"""

BUTTON_DIAL_CONFIRM_STYLE = f"""
QPushButton {{
    background-color: {Colors.NAVY};
    border: none;
    border-radius: {Radius.MD}px;
    color: {Colors.WHITE};
    font-size: 16px;
    font-weight: 600;
    padding: 12px 24px;
}}
QPushButton:pressed {{
    background-color: {Colors.NAVY_DARK};
}}
"""


# ============================================================
# 카드/패널 스타일 (동적 함수)
# ============================================================

def get_axis_panel_style():
    """축 패널 스타일 (동적)"""
    return f"""
QFrame {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.LG}px;
}}
"""

def get_axis_title_style():
    """축 타이틀 스타일 (동적)"""
    return f"""
QLabel {{
    color: {Colors.NAVY};
    font-size: 18px;
    font-weight: 700;
    background-color: transparent;
    border: none;
}}
"""

def get_stop_button_style():
    """정지 버튼 스타일 (동적)"""
    return f"""
QPushButton {{
    background-color: {Colors.RED_LIGHT};
    border: 2px solid {Colors.RED};
    border-radius: {Radius.MD}px;
    color: {Colors.RED};
    font-size: 14px;
    font-weight: 600;
}}
QPushButton:pressed {{
    background-color: #FECACA;
    border-color: {Colors.RED_DARK};
}}
"""

def get_distance_button_style():
    """거리 버튼 스타일 (동적)"""
    return f"""
QPushButton {{
    background-color: {Colors.BG_PRIMARY};
    border: 2px solid {Colors.BORDER};
    border-radius: 10px;
    color: {Colors.TEXT_SECONDARY};
    font-size: 14px;
    font-weight: 600;
    padding: 10px;
}}
QPushButton:pressed {{
    border-color: {Colors.CYAN};
    color: {Colors.CYAN};
}}
"""

def get_distance_button_active_style():
    """거리 버튼 활성 스타일 (동적)"""
    return f"""
QPushButton {{
    background-color: {Colors.CYAN_ALPHA_10};
    border: 2px solid {Colors.CYAN};
    border-radius: 10px;
    color: {Colors.CYAN};
    font-size: 14px;
    font-weight: 600;
    padding: 10px;
}}
"""

def get_icon_button_style():
    """아이콘 버튼 스타일 (동적)"""
    return f"""
QPushButton {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.LG}px;
    padding: 0px;
}}
QPushButton:pressed {{
    background-color: {Colors.BG_TERTIARY};
    border-color: {Colors.NAVY};
}}
QPushButton:disabled {{
    background-color: {Colors.BG_TERTIARY};
    opacity: 0.6;
}}
"""

def get_icon_button_active_style():
    """아이콘 버튼 활성 스타일 (동적)"""
    return f"""
QPushButton {{
    background-color: {Colors.CYAN_ALPHA_10};
    border: 2px solid {Colors.CYAN};
    border-radius: {Radius.LG}px;
    padding: 0px;
}}
QPushButton:pressed {{
    background-color: {Colors.CYAN_ALPHA_20};
}}
"""

# 하위 호환성을 위한 정적 상수 (동적 함수 호출)
CARD_STYLE = f"""
QWidget {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.LG}px;
}}
"""

AXIS_PANEL_STYLE = f"""
QFrame {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.LG}px;
}}
"""

INFO_ITEM_STYLE = f"""
QFrame {{
    background-color: {Colors.BG_SECONDARY};
    border-radius: {Radius.MD}px;
}}
"""

PREVIEW_AREA_STYLE = f"""
QFrame {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.BORDER};
    border-radius: {Radius.LG}px;
}}
"""


# ============================================================
# 프로그레스 바 스타일
# ============================================================

PROGRESS_BAR_STYLE = f"""
QProgressBar {{
    background-color: {Colors.BG_TERTIARY};
    border: none;
    border-radius: 10px;
    height: 36px;
    text-align: center;
    font-size: 14px;
    font-weight: 700;
    color: {Colors.WHITE};
}}
QProgressBar::chunk {{
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                                stop:0 {Colors.NAVY}, 
                                stop:1 {Colors.CYAN});
    border-radius: 10px;
}}
"""


# ============================================================
# 다이얼 스타일
# ============================================================

DIAL_VALUE_STYLE = f"""
QFrame {{
    background-color: {Colors.BG_SECONDARY};
    border: 2px solid {Colors.CYAN};
    border-radius: {Radius.LG}px;
}}
"""

DIAL_NUMBER_STYLE = f"""
QLabel {{
    color: {Colors.NAVY};
    font-size: 42px;
    font-weight: 700;
    background-color: {Colors.BG_SECONDARY};
    border: none;
}}
"""

DIAL_UNIT_STYLE = f"""
QLabel {{
    color: {Colors.TEXT_SECONDARY};
    font-size: 18px;
    background-color: {Colors.BG_SECONDARY};
    border: none;
}}
"""

DIAL_LABEL_STYLE = f"""
QLabel {{
    color: {Colors.TEXT_SECONDARY};
    font-size: 16px;
}}
"""


# ============================================================
# 정보 표시 스타일
# ============================================================

AXIS_TITLE_STYLE = f"""
QLabel {{
    color: {Colors.NAVY};
    font-size: 18px;
    font-weight: 700;
}}
"""

AXIS_VALUE_STYLE = f"""
QLabel {{
    color: {Colors.CYAN};
    font-size: 24px;
    font-weight: 700;
}}
"""

INFO_LABEL_STYLE = f"""
QLabel {{
    color: {Colors.TEXT_DISABLED};
    font-size: 11px;
}}
"""

INFO_VALUE_STYLE = f"""
QLabel {{
    color: {Colors.TEXT_PRIMARY};
    font-size: 14px;
    font-weight: 600;
}}
"""

FILE_NAME_STYLE = f"""
QLabel {{
    color: {Colors.TEXT_PRIMARY};
    font-size: 12px;
    font-weight: 500;
}}
"""


# ============================================================
# 다이얼로그 스타일
# ============================================================

DIALOG_STYLE = f"""
QDialog {{
    background-color: {Colors.BG_PRIMARY};
    border-radius: {Radius.LG}px;
}}
"""

DIALOG_TITLE_STYLE = f"""
QLabel {{
    color: {Colors.NAVY};
    font-size: 18px;
    font-weight: 600;
}}
"""

DIALOG_MESSAGE_STYLE = f"""
QLabel {{
    color: {Colors.TEXT_PRIMARY};
    font-size: 16px;
}}
"""
