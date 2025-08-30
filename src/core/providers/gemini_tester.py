import requests
import json
from typing import Dict, List, Tuple, Optional

class GeminiTester:
    """Test Gemini (Google Generative AI) API key validity and get model information"""
    
    def __init__(self):
        self.base_url = "https://generativelanguage.googleapis.com/v1"
        self.models_endpoint = f"{self.base_url}/models"
    
    def test_api_key(self, api_key: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Test if a Gemini API key is valid
        
        Args:
            api_key: The API key to test
            
        Returns:
            Tuple of (is_valid, message, data)
        """
        params = {"key": api_key}
        
        try:
            response = requests.get(self.models_endpoint, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                
                # Check if it's a paid account by looking for Gemini Pro models
                has_pro = any('gemini-pro' in model.get('name', '').lower() for model in models)
                has_ultra = any('gemini-ultra' in model.get('name', '').lower() for model in models)
                account_type = "Paid" if (has_pro or has_ultra) else "Free"
                
                message = f"✅ Valid Gemini API key ({account_type} account)"
                return True, message, data
                
            elif response.status_code == 400:
                return False, "❌ Invalid Gemini API key - Bad request", None
            elif response.status_code == 401:
                return False, "❌ Invalid Gemini API key - Authentication failed", None
            elif response.status_code == 403:
                return False, "❌ Gemini API key access denied - Check permissions", None
            else:
                return False, f"❌ Gemini API error: {response.status_code}", None
                
        except requests.exceptions.Timeout:
            return False, "❌ Gemini API request timed out", None
        except requests.exceptions.RequestException as e:
            return False, f"❌ Gemini API connection error: {str(e)}", None
        except Exception as e:
            return False, f"❌ Unexpected error: {str(e)}", None
    
    def get_model_details(self, api_key: str) -> Dict:
        """Get detailed model information"""
        params = {"key": api_key}
        
        try:
            response = requests.get(self.models_endpoint, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                
                # Categorize models
                gemini_models = [m for m in models if 'gemini' in m.get('name', '').lower()]
                text_models = [m for m in models if 'text' in m.get('name', '').lower()]
                other_models = [m for m in models if 'gemini' not in m.get('name', '').lower() and 'text' not in m.get('name', '').lower()]
                
                # Build per-model metrics (Gemini model list typically does not expose rpm/rpd/tpm)
                per_model = []
                for m in models:
                    per_model.append({
                        'id': m.get('name'),
                        'rpm': None,
                        'rpd': None,
                        'tpm': None
                    })
                
                return {
                    'total_models': len(models),
                    'gemini_models': len(gemini_models),
                    'text_models': len(text_models),
                    'other_models': len(other_models),
                    'all_models': [m.get('name') for m in models],
                    'gemini_model_list': [m.get('name') for m in gemini_models],
                    'text_model_list': [m.get('name') for m in text_models],
                    'per_model': per_model
                }
            else:
                return {'error': f'Failed to fetch models: {response.status_code}'}
        except Exception as e:
            return {'error': f'Error fetching models: {str(e)}'}
    
    def check_account_status(self, api_key: str) -> Dict:
        """Check if account has access to paid features"""
        params = {"key": api_key}
        
        try:
            response = requests.get(self.models_endpoint, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = data.get("models", [])
                
                # Check for premium models
                has_gemini_pro = any('gemini-pro' in m.get('name', '').lower() for m in models)
                has_gemini_ultra = any('gemini-ultra' in m.get('name', '').lower() for m in models)
                has_gemini_flash = any('gemini-flash' in m.get('name', '').lower() for m in models)
                
                return {
                    'is_paid': has_gemini_pro or has_gemini_ultra or has_gemini_flash,
                    'has_gemini_pro': has_gemini_pro,
                    'has_gemini_ultra': has_gemini_ultra,
                    'has_gemini_flash': has_gemini_flash,
                    'account_type': 'Paid' if (has_gemini_pro or has_gemini_ultra or has_gemini_flash) else 'Free'
                }
            else:
                return {'error': f'Failed to check account status: {response.status_code}'}
        except Exception as e:
            return {'error': f'Error checking account status: {str(e)}'}

    def get_model_info(self, api_key: str, model_id: str) -> Dict:
        """Fetch a single model's details. Falls back to scanning the list if needed."""
        params = {"key": api_key}
        try:
            # Gemini model names are full resource names (e.g., models/gemini-1.5-pro)
            # Try direct endpoint
            resp = requests.get(f"{self.models_endpoint}/{model_id}", params=params, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            # Fallback: list and find
            resp = requests.get(self.models_endpoint, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json().get('models', [])
                for m in data:
                    if m.get('name') == model_id:
                        return m
                return {'error': 'Model not found'}
            return {'error': f'Failed to fetch model info: {resp.status_code}'}
        except Exception as e:
            return {'error': f'Error fetching model info: {str(e)}'}
