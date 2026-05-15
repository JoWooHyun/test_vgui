"""
VERICOM DLP 3D Printer GUI - Font Settings
"""

from PySide6.QtGui import QFont


class Fonts:
    """폰트 설정 클래스"""
    
    # 기본 폰트 패밀리
    FAMILY = "Pretendard"
    FAMILY_FALLBACK = "Noto Sans KR"
    FAMILY_MONO = "SF Mono"
    FAMILY_MONO_FALLBACK = "Consolas"
    
    @staticmethod
    def _create_font(size: int, weight: QFont.Weight = QFont.Medium, 
                     family: str = None) -> QFont:
        """폰트 생성 헬퍼"""
        if family is None:
            family = Fonts.FAMILY
        font = QFont(family, size)
        font.setWeight(weight)
        return font
    
    @staticmethod
    def display() -> QFont:
        """다이얼 숫자용 (42px Bold)"""
        return Fonts._create_font(42, QFont.Bold)
    
    @staticmethod
    def h1() -> QFont:
        """큰 숫자, 메인 값 (24px Bold)"""
        return Fonts._create_font(24, QFont.Bold)
    
    @staticmethod
    def h2() -> QFont:
        """메인 버튼 레이블 (20px SemiBold)"""
        return Fonts._create_font(20, QFont.DemiBold)
    
    @staticmethod
    def h3() -> QFont:
        """페이지 타이틀 (18px SemiBold)"""
        return Fonts._create_font(18, QFont.DemiBold)
    
    @staticmethod
    def body() -> QFont:
        """일반 버튼, 본문 (16px Medium)"""
        return Fonts._create_font(16, QFont.Medium)
    
    @staticmethod
    def body_small() -> QFont:
        """보조 정보 (14px Medium)"""
        return Fonts._create_font(14, QFont.Medium)
    
    @staticmethod
    def caption() -> QFont:
        """힌트, 레이블 (12px Regular)"""
        return Fonts._create_font(12, QFont.Normal)
    
    @staticmethod
    def tiny() -> QFont:
        """아이콘 하단 레이블 (11px Medium)"""
        return Fonts._create_font(11, QFont.Medium)
    
    @staticmethod
    def mono(size: int = 14) -> QFont:
        """숫자 표시용 모노스페이스"""
        font = QFont(Fonts.FAMILY_MONO, size)
        font.setWeight(QFont.Bold)
        return font
    
    @staticmethod
    def mono_large() -> QFont:
        """큰 숫자용 모노스페이스 (24px)"""
        return Fonts.mono(24)
    
    @staticmethod
    def mono_display() -> QFont:
        """다이얼 숫자용 모노스페이스 (42px)"""
        return Fonts.mono(42)
