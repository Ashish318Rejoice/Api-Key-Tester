import requests
import json
from typing import Dict, List, Tuple, Optional

class ClaudeTester:
    """Test Claude (Anthropic) API key validity and get model information"""
    
    def __init__(self):
        self.base_url = "https://api.anthropic.com/v1"
        self.models_endpoint = f"{self.base_url}/models"
    
    def test_api_key(self, api_key: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Test if a Claude API key is valid
        
        Args:
            api_key: The API key to test
            
        Returns:
            Tuple of (is_valid, message, data)
        """
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
        
        try:
            response = requests.get(self.models_endpoint, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get("data", [])
                
                # Check if it's a paid account by looking for premium models
                has_claude_3 = any('claude-3' in model.get('id', '').lower() for model in models)
                has_claude_2 = any('claude-2' in model.get('id', '').lower() for model in models)
                account_type = "Paid" if (has_claude_3 or has_claude_2) else "Free"
                
                message = f"✅ Valid Claude API key ({account_type} account)"
                return True, message, data
                
            elif response.status_code == 401:
                return False, "❌ Invalid Claude API key - Authentication failed", None
            elif response.status_code == 403:
                return False, "❌ Claude API key access denied - Check permissions", None
            elif response.status_code == 429:
                return False, "❌ Claude API rate limit exceeded", None
            else:
                return False, f"❌ Claude API error: {response.status_code}", None
                
        except requests.exceptions.Timeout:
            return False, "❌ Claude API request timed out", None
        except requests.exceptions.RequestException as e:
            return False, f"❌ Claude API connection error: {str(e)}", None
        except Exception as e:
            return False, f"❌ Unexpected error: {str(e)}", None
    
    def get_model_details(self, api_key: str) -> Dict:
        """Get detailed model information"""
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
        
        try:
            response = requests.get(self.models_endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = data.get("data", [])
                
                # Categorize models
                claude_3_models = [m for m in models if 'claude-3' in m.get('id', '').lower()]
                claude_2_models = [m for m in models if 'claude-2' in m.get('id', '').lower()]
                other_models = [m for m in models if 'claude-3' not in m.get('id', '').lower() and 'claude-2' not in m.get('id', '').lower()]
                
                # Build per-model metrics (Anthropic models API does not expose rpm/rpd/tpm)
                per_model = []
                for m in models:
                    per_model.append({
                        'id': m.get('id'),
                        'rpm': None,
                        'rpd': None,
                        'tpm': None
                    })
                
                return {
                    'total_models': len(models),
                    'claude_3_models': len(claude_3_models),
                    'claude_2_models': len(claude_2_models),
                    'other_models': len(other_models),
                    'all_models': [m.get('id') for m in models],
                    'claude_3_model_list': [m.get('id') for m in claude_3_models],
                    'claude_2_model_list': [m.get('id') for m in claude_2_models],
                    'per_model': per_model
                }
            else:
                return {'error': f'Failed to fetch models: {response.status_code}'}
        except Exception as e:
            return {'error': f'Error fetching models: {str(e)}'}
    
    def check_account_status(self, api_key: str) -> Dict:
        """Check if account has access to paid features"""
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
        
        try:
            response = requests.get(self.models_endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = data.get("data", [])
                
                # Check for premium models
                has_claude_3_opus = any('claude-3-opus' in m.get('id', '').lower() for m in models)
                has_claude_3_sonnet = any('claude-3-sonnet' in m.get('id', '').lower() for m in models)
                has_claude_3_haiku = any('claude-3-haiku' in m.get('id', '').lower() for m in models)
                has_claude_2 = any('claude-2' in m.get('id', '').lower() for m in models)
                
                return {
                    'is_paid': has_claude_3_opus or has_claude_3_sonnet or has_claude_3_haiku or has_claude_2,
                    'has_claude_3_opus': has_claude_3_opus,
                    'has_claude_3_sonnet': has_claude_3_sonnet,
                    'has_claude_3_haiku': has_claude_3_haiku,
                    'has_claude_2': has_claude_2,
                    'account_type': 'Paid' if (has_claude_3_opus or has_claude_3_sonnet or has_claude_3_haiku or has_claude_2) else 'Free'
                }
            else:
                return {'error': f'Failed to check account status: {response.status_code}'}
        except Exception as e:
            return {'error': f'Error checking account status: {str(e)}'}

    def get_model_info(self, api_key: str, model_id: str) -> Dict:
        """Fetch a single model's details. Falls back to scanning the list if needed."""
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01"
        }
        try:
            resp = requests.get(f"{self.models_endpoint}/{model_id}", headers=headers, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            resp = requests.get(self.models_endpoint, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json().get('data', [])
                for m in data:
                    if m.get('id') == model_id:
                        return m
                return {'error': 'Model not found'}
            return {'error': f'Failed to fetch model info: {resp.status_code}'}
        except Exception as e:
            return {'error': f'Error fetching model info: {str(e)}'}
