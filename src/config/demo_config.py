#!/usr/bin/env python3
"""
Demo Configuration for Modern LLM API Key Tester & Analyzer

This file contains demo data and configuration for showcasing the modern UI features.
"""

# Demo data for showcasing the modern UI
DEMO_MODELS = {
    "openai": [
        {
            "id": "gpt-4o",
            "type": "Chat",
            "context_length": 128000,
            "created": "2024-05-13",
            "status": "Available",
            "description": "GPT-4o is OpenAI's most advanced model, optimized for speed and cost.",
            "capabilities": ["text-generation", "vision", "function-calling"]
        },
        {
            "id": "gpt-4o-mini",
            "type": "Chat", 
            "context_length": 128000,
            "created": "2024-05-13",
            "status": "Available",
            "description": "GPT-4o Mini is a smaller, faster version of GPT-4o.",
            "capabilities": ["text-generation", "function-calling"]
        },
        {
            "id": "text-embedding-3-large",
            "type": "Embedding",
            "context_length": 8192,
            "created": "2024-01-25",
            "status": "Available",
            "description": "High-quality text embeddings for semantic search and analysis.",
            "capabilities": ["embeddings"]
        }
    ],
    "claude": [
        {
            "id": "claude-3-5-sonnet-20241022",
            "type": "Chat",
            "context_length": 200000,
            "created": "2024-10-22",
            "status": "Available",
            "description": "Claude 3.5 Sonnet is Anthropic's most capable model.",
            "capabilities": ["text-generation", "vision", "function-calling"]
        },
        {
            "id": "claude-3-haiku-20240307",
            "type": "Chat",
            "context_length": 200000,
            "created": "2024-03-07",
            "status": "Available",
            "description": "Claude 3 Haiku is fast and cost-effective.",
            "capabilities": ["text-generation", "vision"]
        }
    ],
    "gemini": [
        {
            "id": "models/gemini-1.5-pro",
            "type": "Chat",
            "context_length": 1000000,
            "created": "2024-02-15",
            "status": "Available",
            "description": "Gemini 1.5 Pro with 1M token context window.",
            "capabilities": ["text-generation", "vision", "function-calling"]
        },
        {
            "id": "models/gemini-1.5-flash",
            "type": "Chat",
            "context_length": 1000000,
            "created": "2024-02-15",
            "status": "Available",
            "description": "Gemini 1.5 Flash optimized for speed and efficiency.",
            "capabilities": ["text-generation", "vision"]
        }
    ]
}

# Demo metrics for dashboard
DEMO_METRICS = {
    "total_models": 7,
    "providers": ["OpenAI", "Anthropic", "Google"],
    "api_status": "Valid",
    "selected_model": "gpt-4o"
}

# Demo notifications
DEMO_NOTIFICATIONS = [
    {
        "message": "Successfully connected to OpenAI",
        "type": "success"
    },
    {
        "message": "Loaded 7 models from your account",
        "type": "success"
    },
    {
        "message": "Model details fetched successfully",
        "type": "info"
    }
]

# UI Theme Configuration
THEME_CONFIG = {
    "primary_color": "#667eea",
    "secondary_color": "#764ba2",
    "success_color": "#43e97b",
    "warning_color": "#f093fb",
    "error_color": "#fa709a",
    "background_color": "#f8fafc",
    "text_color": "#1f2937",
    "border_radius": "12px",
    "shadow": "0 4px 20px rgba(0,0,0,0.08)",
    "animation_duration": "0.3s"
}

# Feature flags for demo mode
DEMO_FEATURES = {
    "show_demo_data": True,
    "enable_animations": True,
    "show_notifications": True,
    "enable_advanced_filters": True,
    "show_export_options": True,
    "enable_model_comparison": True
}

# Demo provider information
DEMO_PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "emoji": "🟦",
        "color": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "models_count": 3,
        "status": "Active"
    },
    "claude": {
        "name": "Anthropic Claude",
        "emoji": "🟪", 
        "color": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "models_count": 2,
        "status": "Active"
    },
    "gemini": {
        "name": "Google Gemini",
        "emoji": "🟨",
        "color": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "models_count": 2,
        "status": "Active"
    }
}

# Demo comparison data
DEMO_COMPARISON = {
    "model_a": {
        "id": "gpt-4o",
        "provider": "OpenAI",
        "context_length": 128000,
        "capabilities": ["text-generation", "vision", "function-calling"],
        "cost_per_1k_tokens": "$0.005"
    },
    "model_b": {
        "id": "claude-3-5-sonnet-20241022", 
        "provider": "Anthropic",
        "context_length": 200000,
        "capabilities": ["text-generation", "vision", "function-calling"],
        "cost_per_1k_tokens": "$0.003"
    }
}

def get_demo_data():
    """Get all demo data for the application."""
    return {
        "models": DEMO_MODELS,
        "metrics": DEMO_METRICS,
        "notifications": DEMO_NOTIFICATIONS,
        "theme": THEME_CONFIG,
        "features": DEMO_FEATURES,
        "providers": DEMO_PROVIDERS,
        "comparison": DEMO_COMPARISON
    }

def is_demo_mode():
    """Check if demo mode is enabled."""
    import os
    return os.getenv("DEMO_MODE", "false").lower() == "true"

def get_demo_models_for_provider(provider):
    """Get demo models for a specific provider."""
    return DEMO_MODELS.get(provider, [])

def get_demo_provider_info(provider):
    """Get demo provider information."""
    return DEMO_PROVIDERS.get(provider, {})

def get_demo_comparison_data():
    """Get demo comparison data."""
    return DEMO_COMPARISON
