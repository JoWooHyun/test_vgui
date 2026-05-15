"""
Test VGUI - Pages Package (DLP 제거)
"""

from .base_page import BasePage
from .main_page import MainPage
from .tool_page import ToolPage
from .manual_page import ManualPage
from .setting_page import SettingPage
from .material_page import MaterialPage
from .print_test_page import PrintTestPage
from .test_progress_page import TestProgressPage

__all__ = [
    'BasePage',
    'MainPage',
    'ToolPage',
    'ManualPage',
    'SettingPage',
    'MaterialPage',
    'PrintTestPage',
    'TestProgressPage',
]
