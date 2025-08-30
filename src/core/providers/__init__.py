"""
KeyMate Providers Package
Contains testers for various LLM providers: OpenAI, Gemini, Deepseek, Claude, Grok, and Groq
"""

from .openai_tester import OpenAITester
from .gemini_tester import GeminiTester
from .deepseek_tester import DeepseekTester
from .claude_tester import ClaudeTester
from .grok_tester import GrokTester
from .groq_tester import GroqTester

__all__ = [
    'OpenAITester',
    'GeminiTester', 
    'DeepseekTester',
    'ClaudeTester',
    'GrokTester',
    'GroqTester'
]

__version__ = "1.0.0"
__author__ = "KeyMate"
__description__ = "A comprehensive tool to test and analyze LLM API keys"
