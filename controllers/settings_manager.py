"""
VERICOM DLP 3D Printer - Settings Manager
사용자 설정 저장 및 로드 (JSON)
"""

import json
import os
from dataclasses import dataclass, asdict, field
from typing import Optional, List


# 설정 파일 경로
SETTINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
SETTINGS_FILE = os.path.join(SETTINGS_DIR, "settings.json")


@dataclass
class MaterialPreset:
    """소재별 프린트 프리셋"""
    name: str = "Default"
    blade_speed: int = 5            # Blade 속도 (1-30 mm/s)
    led_power: int = 43             # LED 파워 (9-100%)
    blade_cycles: int = 1           # 블레이드 반복 횟수 (1~3)
    y_dispense_distance: float = 1.0  # Resin 토출거리 (mm/레이어, 0.1~5.0)
    y_dispense_speed: int = 3       # Resin 토출속도 (mm/s, 1~15)
    y_dispense_delay: float = 5.0   # Resin 토출 대기시간 (초, 0.5~20.0)
    # 확장 항목
    leveling_cycles: int = 1        # Resin 평탄화 횟수 (0~5)
    lift_height: float = 5.0        # 리프트 높이 (mm, 1.0~20.0)
    drop_speed: int = 150           # Z축 하강 속도 (mm/min, 10~300)


# 기본 내장 소재 프리셋
DEFAULT_MATERIALS = [
    MaterialPreset(
        name="Zirconia",
        blade_speed=5, led_power=43, blade_cycles=1,
        y_dispense_distance=1.0, y_dispense_speed=3, y_dispense_delay=5.0,
        leveling_cycles=1, lift_height=5.0, drop_speed=150
    ),
    MaterialPreset(
        name="Alumina",
        blade_speed=5, led_power=50, blade_cycles=1,
        y_dispense_distance=1.0, y_dispense_speed=3, y_dispense_delay=5.0,
        leveling_cycles=1, lift_height=5.0, drop_speed=150
    ),
    MaterialPreset(
        name="Hydroxyapatite",
        blade_speed=4, led_power=45, blade_cycles=1,
        y_dispense_distance=1.2, y_dispense_speed=3, y_dispense_delay=5.0,
        leveling_cycles=1, lift_height=5.0, drop_speed=120
    ),
]


@dataclass
class PrintSettings:
    """프린트 관련 설정"""
    led_power: int = 43         # LED 파워 (9-100%, 1023=100%, 440=43%)
    blade_speed: int = 5        # Blade 속도 (1-30 mm/s)
    y_dispense_distance: float = 1.0   # Resin 토출거리 (mm/레이어)
    y_dispense_speed: int = 3          # Resin 토출속도 (mm/s)
    y_dispense_delay: float = 5.0      # Resin 토출 대기시간 (초)
    y_priming_position: float = 0.0    # Resin 프라이밍 완료 위치 (mm)


@dataclass
class AppSettings:
    """앱 전체 설정"""
    print_settings: PrintSettings = None
    language: str = "en"        # 언어 설정
    theme: str = "Light"        # 테마 설정
    materials: List[MaterialPreset] = field(default_factory=list)
    selected_material: str = ""  # 선택된 소재 이름

    def __post_init__(self):
        if self.print_settings is None:
            self.print_settings = PrintSettings()
        if not self.materials:
            self.materials = [MaterialPreset(**asdict(m)) for m in DEFAULT_MATERIALS]
            self.selected_material = self.materials[0].name


class SettingsManager:
    """설정 관리 클래스"""

    _instance: Optional['SettingsManager'] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True
        self._settings = AppSettings()
        self._load()

    def _ensure_dir(self):
        """설정 디렉토리 확인/생성"""
        if not os.path.exists(SETTINGS_DIR):
            os.makedirs(SETTINGS_DIR)
            print(f"[Settings] 설정 디렉토리 생성: {SETTINGS_DIR}")

    def _load(self):
        """설정 파일 로드"""
        if not os.path.exists(SETTINGS_FILE):
            print("[Settings] 설정 파일 없음, 기본값 사용")
            return

        try:
            with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # PrintSettings 로드
            print_data = data.get('print_settings', {})
            self._settings.print_settings = PrintSettings(
                led_power=print_data.get('led_power', 100),
                blade_speed=print_data.get('blade_speed', 5),
                y_dispense_distance=print_data.get('y_dispense_distance', 1.0),
                y_dispense_speed=print_data.get('y_dispense_speed', 5),
                y_dispense_delay=print_data.get('y_dispense_delay', 2.0),
                y_priming_position=print_data.get('y_priming_position', 0.0)
            )

            # 기타 설정 로드
            self._settings.language = data.get('language', 'en')
            self._settings.theme = data.get('theme', 'Light')

            # 소재 프리셋 로드
            materials_data = data.get('materials', [])
            if materials_data:
                self._settings.materials = []
                for m in materials_data:
                    self._settings.materials.append(MaterialPreset(
                        name=m.get('name', 'Unknown'),
                        blade_speed=m.get('blade_speed', 5),
                        led_power=m.get('led_power', 43),
                        blade_cycles=m.get('blade_cycles', 1),
                        y_dispense_distance=m.get('y_dispense_distance', 1.0),
                        y_dispense_speed=m.get('y_dispense_speed', 5),
                        y_dispense_delay=m.get('y_dispense_delay', 2.0),
                        leveling_cycles=m.get('leveling_cycles', 1),
                        lift_height=m.get('lift_height', 5.0),
                        drop_speed=m.get('drop_speed', 150),
                    ))

            self._settings.selected_material = data.get('selected_material', '')
            # 선택된 소재가 없거나 삭제된 경우 첫 번째 소재 선택
            if self._settings.materials and self._settings.selected_material not in [m.name for m in self._settings.materials]:
                self._settings.selected_material = self._settings.materials[0].name

            print(f"[Settings] 설정 로드 완료: {SETTINGS_FILE}")
            print(f"  - LED Power: {self._settings.print_settings.led_power}%")
            print(f"  - Blade Speed: {self._settings.print_settings.blade_speed}mm/s")
            print(f"  - 소재 프리셋: {len(self._settings.materials)}개")

        except Exception as e:
            print(f"[Settings] 설정 로드 실패: {e}")

    def save(self):
        """설정 파일 저장"""
        self._ensure_dir()

        try:
            data = {
                'print_settings': asdict(self._settings.print_settings),
                'language': self._settings.language,
                'theme': self._settings.theme,
                'materials': [asdict(m) for m in self._settings.materials],
                'selected_material': self._settings.selected_material
            }

            with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            print(f"[Settings] 설정 저장 완료: {SETTINGS_FILE}")

        except Exception as e:
            print(f"[Settings] 설정 저장 실패: {e}")

    # ==================== 소재 프리셋 관리 ====================

    def get_materials(self) -> List[MaterialPreset]:
        """소재 프리셋 목록 반환"""
        return self._settings.materials

    def get_material_by_name(self, name: str) -> Optional[MaterialPreset]:
        """이름으로 소재 프리셋 반환"""
        for m in self._settings.materials:
            if m.name == name:
                return m
        return None

    def add_material(self, preset: MaterialPreset):
        """소재 프리셋 추가"""
        # 이름 중복 방지
        existing_names = [m.name for m in self._settings.materials]
        if preset.name in existing_names:
            base_name = preset.name
            i = 2
            while f"{base_name} ({i})" in existing_names:
                i += 1
            preset.name = f"{base_name} ({i})"

        self._settings.materials.append(preset)
        self.save()
        print(f"[Settings] 소재 추가: {preset.name}")

    def update_material(self, original_name: str, preset: MaterialPreset):
        """소재 프리셋 수정"""
        for i, m in enumerate(self._settings.materials):
            if m.name == original_name:
                self._settings.materials[i] = preset
                # 선택된 소재 이름도 갱신
                if self._settings.selected_material == original_name:
                    self._settings.selected_material = preset.name
                self.save()
                print(f"[Settings] 소재 수정: {original_name} → {preset.name}")
                return True
        return False

    def delete_material(self, name: str) -> bool:
        """소재 프리셋 삭제"""
        if len(self._settings.materials) <= 1:
            print("[Settings] 최소 1개 소재는 유지해야 합니다")
            return False

        for i, m in enumerate(self._settings.materials):
            if m.name == name:
                self._settings.materials.pop(i)
                # 삭제된 소재가 선택 중이면 첫 번째 소재로 변경
                if self._settings.selected_material == name:
                    self._settings.selected_material = self._settings.materials[0].name
                self.save()
                print(f"[Settings] 소재 삭제: {name}")
                return True
        return False

    def get_selected_material(self) -> str:
        """선택된 소재 이름 반환"""
        return self._settings.selected_material

    def set_selected_material(self, name: str):
        """소재 선택"""
        if any(m.name == name for m in self._settings.materials):
            self._settings.selected_material = name
            self.save()

    def get_selected_material_preset(self) -> Optional[MaterialPreset]:
        """선택된 소재의 프리셋 반환"""
        return self.get_material_by_name(self._settings.selected_material)

    # ==================== LED Power ====================

    def get_led_power(self) -> int:
        """LED 파워 값 반환"""
        return self._settings.print_settings.led_power

    def set_led_power(self, value: int):
        """LED 파워 값 설정 (9-100%, 1023=100%)"""
        value = max(9, min(100, value))
        self._settings.print_settings.led_power = value
        self.save()

    # ==================== Blade Speed ====================

    def get_blade_speed(self) -> int:
        """Blade 속도 반환"""
        return self._settings.print_settings.blade_speed

    def set_blade_speed(self, value: int):
        """Blade 속도 설정 (10-100 mm/s)"""
        value = max(10, min(100, value))
        self._settings.print_settings.blade_speed = value
        self.save()

    # ==================== Y Dispense Distance ====================

    def get_y_dispense_distance(self) -> float:
        return self._settings.print_settings.y_dispense_distance

    def set_y_dispense_distance(self, value: float):
        value = max(0.1, min(5.0, value))
        self._settings.print_settings.y_dispense_distance = value
        self.save()

    # ==================== Y Dispense Speed ====================

    def get_y_dispense_speed(self) -> int:
        return self._settings.print_settings.y_dispense_speed

    def set_y_dispense_speed(self, value: int):
        value = max(1, min(15, value))
        self._settings.print_settings.y_dispense_speed = value
        self.save()

    # ==================== Y Dispense Delay ====================

    def get_y_dispense_delay(self) -> float:
        return self._settings.print_settings.y_dispense_delay

    def set_y_dispense_delay(self, value: float):
        value = max(0.5, min(10.0, value))
        self._settings.print_settings.y_dispense_delay = value
        self.save()

    # ==================== Resin Priming Position ====================

    def get_y_priming_position(self) -> float:
        return self._settings.print_settings.y_priming_position

    def set_y_priming_position(self, value: float):
        value = max(0.0, min(125.0, value))
        self._settings.print_settings.y_priming_position = value
        self.save()
        print(f"[Settings] Resin priming position saved: {value}mm")

    # ==================== Language ====================

    def get_language(self) -> str:
        """언어 설정 반환"""
        return self._settings.language

    def set_language(self, lang: str):
        """언어 설정"""
        self._settings.language = lang
        self.save()

    # ==================== Theme ====================

    def get_theme(self) -> str:
        """테마 설정 반환"""
        return self._settings.theme

    def set_theme(self, theme: str):
        """테마 설정"""
        self._settings.theme = theme
        self.save()

    # ==================== Generic get/set ====================

    def get(self, key: str, default=None):
        """일반적인 설정 값 반환"""
        if key == "theme":
            return self._settings.theme
        elif key == "language":
            return self._settings.language
        elif key == "led_power":
            return self._settings.print_settings.led_power
        elif key == "blade_speed":
            return self._settings.print_settings.blade_speed
        elif key == "y_dispense_distance":
            return self._settings.print_settings.y_dispense_distance
        elif key == "y_dispense_speed":
            return self._settings.print_settings.y_dispense_speed
        elif key == "y_dispense_delay":
            return self._settings.print_settings.y_dispense_delay
        elif key == "y_priming_position":
            return self._settings.print_settings.y_priming_position
        return default

    def set(self, key: str, value):
        """일반적인 설정 값 저장"""
        if key == "theme":
            self._settings.theme = value
        elif key == "language":
            self._settings.language = value
        elif key == "led_power":
            self._settings.print_settings.led_power = value
        elif key == "blade_speed":
            self._settings.print_settings.blade_speed = value
        elif key == "y_dispense_distance":
            self._settings.print_settings.y_dispense_distance = value
        elif key == "y_dispense_speed":
            self._settings.print_settings.y_dispense_speed = value
        elif key == "y_dispense_delay":
            self._settings.print_settings.y_dispense_delay = value
        elif key == "y_priming_position":
            self._settings.print_settings.y_priming_position = value
        self.save()


# 싱글톤 인스턴스 접근
def get_settings() -> SettingsManager:
    """SettingsManager 싱글톤 인스턴스 반환"""
    return SettingsManager()
