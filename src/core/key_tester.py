#!/usr/bin/env python3
"""
KeyMate - Core Business Logic

This module provides the main business logic for:
- API key validation across multiple providers
- Model listing and details retrieval
- Provider auto-detection
- Model analysis and insights

Supports: OpenAI, Google Gemini, Deepseek, Anthropic Claude, xAI Grok, Groq
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple

from .providers import (
    OpenAITester,
    GeminiTester,
    DeepseekTester,
    ClaudeTester,
    GrokTester,
    GroqTester,
)


class LLMKeyTester:
    """
    Main orchestrator for LLM API key testing and model analysis.
    
    Provides a unified interface for validating API keys across multiple
    LLM providers and retrieving model information.
    """

    def __init__(self):
        """Initialize the tester with all supported providers."""
        self.testers = {
            "openai": OpenAITester(),
            "gemini": GeminiTester(),
            "deepseek": DeepseekTester(),
            "claude": ClaudeTester(),
            "grok": GrokTester(),
            "groq": GroqTester(),
        }

    def detect_provider(self, api_key: str) -> Tuple[Optional[str], bool, str, Dict[str, Any]]:
        """
        Auto-detect the provider from an API key and validate it.
        
        Args:
            api_key: The API key to test
            
        Returns:
            Tuple of (provider_id, is_valid, message, additional_info)
        """
        if not api_key or not api_key.strip():
            return None, False, "No API key provided", {}

        # Provider detection based on key format
        provider_priority = self._get_provider_priority(api_key)
        
        for provider_id in provider_priority:
            tester = self.testers[provider_id]
            try:
                is_valid, message, info = tester.test_api_key(api_key)
                if is_valid:
                    return provider_id, True, f"Valid {provider_id.title()} API key", info
            except Exception as e:
                # Continue to next provider on error
                continue
        
        return None, False, "Invalid or unauthorized API key", {}

    def get_detailed_info(self, provider: str, api_key: str) -> Dict[str, Any]:
        """
        Get detailed account and model information for a validated provider.
        
        Args:
            provider: The provider ID
            api_key: The validated API key
            
        Returns:
            Dictionary with account status and model details
        """
        if provider not in self.testers:
            return {"error": f"Unsupported provider: {provider}"}
        
        try:
            tester = self.testers[provider]
            account_status = tester.check_account_status(api_key)
            model_details = tester.get_model_details(api_key)
            
            return {
                "account_status": account_status,
                "model_details": model_details,
            }
        except Exception as e:
            return {"error": f"Error fetching details: {str(e)}"}

    def guess_provider_from_model_id(self, model_id: str) -> Optional[str]:
        """
        Guess the provider from a model ID.
        
        Args:
            model_id: The model ID to analyze
            
        Returns:
            Guessed provider ID or None
        """
        model_id_lower = model_id.lower()
        
        # Provider-specific patterns
        if model_id_lower.startswith(("gpt-", "text-", "dall-e", "whisper")):
            return "openai"
        elif model_id_lower.startswith(("gemini", "models/")):
            return "gemini"
        elif model_id_lower.startswith(("deepseek", "deepseek-chat")):
            return "deepseek"
        elif model_id_lower.startswith(("claude", "anthropic")):
            return "claude"
        elif model_id_lower.startswith(("grok", "xai")):
            return "grok"
        elif model_id_lower.startswith(("llama", "mixtral", "gemma", "gsk_")):
            return "groq"
        
        return None

    def parse_model_parts(self, model_id: str) -> Dict[str, str]:
        """
        Parse a model ID into its components.
        
        Args:
            model_id: The model ID to parse
            
        Returns:
            Dictionary with parsed components
        """
        parts = {
            "Namespace": "",
            "Family": "",
            "Version": "",
            "Suffix": "",
        }
        
        # Remove common prefixes
        clean_id = model_id
        if clean_id.startswith("models/"):
            parts["Namespace"] = "models"
            clean_id = clean_id[7:]
        
        # Split by common separators
        if "-" in clean_id:
            segments = clean_id.split("-")
            parts["Family"] = segments[0]
            if len(segments) > 1:
                parts["Version"] = "-".join(segments[1:])
        else:
            parts["Family"] = clean_id
        
        return parts

    def reference_capabilities(self, provider: Optional[str]) -> Optional[Dict[str, Any]]:
        """
        Get reference capabilities for a provider.
        
        Args:
            provider: The provider ID
            
        Returns:
            Dictionary with reference capabilities or None
        """
        if not provider or provider not in self.testers:
            return None
        
        # For now, return None as reference capabilities are not implemented
        return None

    def _get_provider_priority(self, api_key: str) -> List[str]:
        """
        Get the priority order for provider testing based on key format.
        
        Args:
            api_key: The API key to analyze
            
        Returns:
            List of provider IDs in priority order
        """
        key_lower = api_key.lower()
        
        # Provider-specific key patterns
        if key_lower.startswith("sk-ant-"):
            return ["claude"]
        elif key_lower.startswith("xai-"):
            return ["grok"]
        elif key_lower.startswith("gsk_"):
            return ["groq"]
        elif key_lower.startswith("ai"):
            return ["gemini"]
        elif key_lower.startswith("sk-"):
            # Could be OpenAI or Deepseek - test OpenAI first
            return ["openai", "deepseek"]
        else:
            # Generic order for unknown formats
            return ["openai", "gemini", "deepseek", "claude", "grok", "groq"]
