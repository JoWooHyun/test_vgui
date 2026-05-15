"""
VERICOM DLP 3D Printer - Time Formatter
시간 포맷 및 예상 시간 계산
"""

from datetime import datetime, timedelta
from typing import Tuple


class TimeFormatter:
    """시간 포맷 유틸리티 클래스"""

    @staticmethod
    def seconds_to_mmss(seconds: float) -> str:
        """
        초를 MM:SS 형식으로 변환

        Args:
            seconds: 초

        Returns:
            "MM:SS" 형식 문자열
        """
        seconds = max(0, int(seconds))
        minutes = seconds // 60
        secs = seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    @staticmethod
    def seconds_to_hhmmss(seconds: float) -> str:
        """
        초를 HH:MM:SS 형식으로 변환

        Args:
            seconds: 초

        Returns:
            "HH:MM:SS" 형식 문자열
        """
        seconds = max(0, int(seconds))
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"

    @staticmethod
    def seconds_to_readable(seconds: float) -> str:
        """
        초를 읽기 쉬운 형식으로 변환

        Args:
            seconds: 초

        Returns:
            "1h 23m" 또는 "45m 30s" 등의 형식
        """
        seconds = max(0, int(seconds))

        if seconds < 60:
            return f"{seconds}s"

        minutes = seconds // 60
        secs = seconds % 60

        if minutes < 60:
            if secs > 0:
                return f"{minutes}m {secs}s"
            return f"{minutes}m"

        hours = minutes // 60
        mins = minutes % 60

        if mins > 0:
            return f"{hours}h {mins}m"
        return f"{hours}h"

    @staticmethod
    def estimate_remaining_time(
        current_layer: int,
        total_layers: int,
        elapsed_seconds: float
    ) -> float:
        """
        남은 시간 예상

        Args:
            current_layer: 현재 레이어 (1부터 시작)
            total_layers: 총 레이어 수
            elapsed_seconds: 경과 시간 (초)

        Returns:
            예상 남은 시간 (초)
        """
        if current_layer <= 0 or total_layers <= 0:
            return 0

        # 평균 레이어 시간
        avg_layer_time = elapsed_seconds / current_layer

        # 남은 레이어 수
        remaining_layers = total_layers - current_layer

        return avg_layer_time * remaining_layers

    @staticmethod
    def estimate_total_time(
        total_layers: int,
        bottom_layers: int,
        bottom_exposure: float,
        normal_exposure: float,
        lift_time: float = 3.0,
        blade_time: float = 2.0
    ) -> float:
        """
        총 프린트 시간 예상

        Args:
            total_layers: 총 레이어 수
            bottom_layers: 바닥 레이어 수
            bottom_exposure: 바닥 노광 시간 (초)
            normal_exposure: 일반 노광 시간 (초)
            lift_time: 리프트 시간 (초)
            blade_time: 블레이드 이동 시간 (초)

        Returns:
            예상 총 시간 (초)
        """
        normal_layers = total_layers - bottom_layers

        # 바닥 레이어 시간
        bottom_time = bottom_layers * (bottom_exposure + lift_time + blade_time)

        # 일반 레이어 시간
        normal_time = normal_layers * (normal_exposure + lift_time + blade_time)

        # 초기화 시간 (홈, 평탄화 등)
        init_time = 30

        return init_time + bottom_time + normal_time

    @staticmethod
    def format_eta(seconds: float) -> str:
        """
        ETA (예상 완료 시간) 포맷

        Args:
            seconds: 남은 시간 (초)

        Returns:
            "HH:MM" 형식의 완료 예정 시간
        """
        now = datetime.now()
        eta = now + timedelta(seconds=seconds)
        return eta.strftime("%H:%M")


# 편의 함수
def format_time(seconds: float, style: str = "mmss") -> str:
    """
    시간 포맷 편의 함수

    Args:
        seconds: 초
        style: "mmss", "hhmmss", "readable"

    Returns:
        포맷된 문자열
    """
    if style == "hhmmss":
        return TimeFormatter.seconds_to_hhmmss(seconds)
    elif style == "readable":
        return TimeFormatter.seconds_to_readable(seconds)
    else:
        return TimeFormatter.seconds_to_mmss(seconds)


def format_duration(seconds: float) -> str:
    """
    지속 시간 포맷 (자동 선택)

    Args:
        seconds: 초

    Returns:
        적절한 형식의 문자열
    """
    if seconds < 3600:  # 1시간 미만
        return TimeFormatter.seconds_to_mmss(seconds)
    else:
        return TimeFormatter.seconds_to_hhmmss(seconds)


# 테스트용
if __name__ == "__main__":
    # 기본 포맷 테스트
    print("=== 시간 포맷 테스트 ===")
    test_seconds = [30, 90, 3600, 7265, 36000]

    for s in test_seconds:
        print(f"{s}초:")
        print(f"  MM:SS: {TimeFormatter.seconds_to_mmss(s)}")
        print(f"  HH:MM:SS: {TimeFormatter.seconds_to_hhmmss(s)}")
        print(f"  Readable: {TimeFormatter.seconds_to_readable(s)}")

    # 예상 시간 테스트
    print("\n=== 예상 시간 테스트 ===")
    total_time = TimeFormatter.estimate_total_time(
        total_layers=1000,
        bottom_layers=8,
        bottom_exposure=50.0,
        normal_exposure=6.0
    )
    print(f"총 예상 시간: {TimeFormatter.seconds_to_readable(total_time)}")
    print(f"ETA: {TimeFormatter.format_eta(total_time)}")

    # 남은 시간 테스트
    remaining = TimeFormatter.estimate_remaining_time(
        current_layer=250,
        total_layers=1000,
        elapsed_seconds=1800  # 30분
    )
    print(f"\n현재 250/1000, 경과 30분")
    print(f"예상 남은 시간: {TimeFormatter.seconds_to_readable(remaining)}")
