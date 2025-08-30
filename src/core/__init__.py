"""
Core Business Logic for KeyMate

This package contains the core business logic including:
- API key validation
- Model management
- Provider detection
- Data processing
"""

from .key_tester import LLMKeyTester
from .providers import *

__version__ = "1.3.0"
__author__ = "KeyMate Team"
