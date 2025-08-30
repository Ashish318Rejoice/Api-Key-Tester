"""
Application Configuration for KeyMate

This module contains the main application configuration including:
- App metadata
- Default settings
- Feature flags
- Environment configuration
"""

import os
from typing import Dict, Any

# App Metadata
APP_NAME = "KeyMate"
APP_VERSION = "1.3.0"
APP_DESCRIPTION = "Professional validation, exploration, and analysis of LLM API keys"
APP_AUTHOR = "KeyMate Team"

# Default Settings
DEFAULT_SETTINGS = {
    "timeout": 30,
    "max_retries": 3,
    "show_raw_json": False,
    "auto_refresh": False,
    "theme": "Light",
    "density": "Comfortable",
}

# Feature Flags
FEATURE_FLAGS = {
    "enable_advanced_analysis": True,
    "enable_model_comparison": True,
    "enable_export_functionality": True,
    "enable_notifications": True,
    "enable_animations": True,
    "enable_demo_mode": False,
}

# Supported Providers
SUPPORTED_PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "emoji": "🟦",
        "key_prefix": "sk-",
        "api_base": "https://api.openai.com/v1",
    },
    "gemini": {
        "name": "Google Gemini",
        "emoji": "🟨",
        "key_prefix": "AIza",
        "api_base": "https://generativelanguage.googleapis.com",
    },
    "deepseek": {
        "name": "Deepseek",
        "emoji": "🟧",
        "key_prefix": "sk-",
        "api_base": "https://api.deepseek.com/v1",
    },
    "claude": {
        "name": "Anthropic Claude",
        "emoji": "🟪",
        "key_prefix": "sk-ant-",
        "api_base": "https://api.anthropic.com",
    },
    "grok": {
        "name": "xAI Grok",
        "emoji": "⚫",
        "key_prefix": "xai-",
        "api_base": "https://api.x.ai",
    },
    "groq": {
        "name": "Groq",
        "emoji": "🟩",
        "key_prefix": "gsk_",
        "api_base": "https://api.groq.com/openai/v1",
    },
}

# UI Configuration
UI_CONFIG = {
    "primary_color": "#667eea",
    "secondary_color": "#764ba2",
    "success_color": "#43e97b",
    "warning_color": "#f093fb",
    "error_color": "#fa709a",
    "background_color": "#f8fafb",
    "text_color": "#1f2937",
    "border_radius": "12px",
    "shadow": "0 4px 20px rgba(0,0,0,0.08)",
    "animation_duration": "0.3s",
}

# Security Configuration
SECURITY_CONFIG = {
    "mask_api_keys": True,
    "store_keys_in_session": True,
    "log_api_calls": False,
    "enable_rate_limiting": True,
    "max_requests_per_minute": 60,
}

def get_config() -> Dict[str, Any]:
    """Get the complete application configuration."""
    return {
        "app": {
            "name": APP_NAME,
            "version": APP_VERSION,
            "description": APP_DESCRIPTION,
            "author": APP_AUTHOR,
        },
        "settings": DEFAULT_SETTINGS,
        "features": FEATURE_FLAGS,
        "providers": SUPPORTED_PROVIDERS,
        "ui": UI_CONFIG,
        "security": SECURITY_CONFIG,
    }

def get_setting(key: str, default: Any = None) -> Any:
    """Get a specific setting value."""
    return DEFAULT_SETTINGS.get(key, default)

def is_feature_enabled(feature: str) -> bool:
    """Check if a feature is enabled."""
    return FEATURE_FLAGS.get(feature, False)

def get_provider_config(provider: str) -> Dict[str, Any]:
    """Get configuration for a specific provider."""
    return SUPPORTED_PROVIDERS.get(provider, {})

def is_demo_mode() -> bool:
    """Check if demo mode is enabled."""
    return os.getenv("DEMO_MODE", "false").lower() == "true"
