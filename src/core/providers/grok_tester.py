import requests
import json
from typing import Dict, List, Tuple, Optional

class GrokTester:
    """Test Grok (xAI) API key validity and get model information"""
    
    def __init__(self):
        self.base_url = "https://api.x.ai/v1"
        self.models_endpoint = f"{self.base_url}/models"
    
    def test_api_key(self, api_key: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Test if a Grok API key is valid
        
        Args:
            api_key: The API key to test
            
        Returns:
            Tuple of (is_valid, message, data)
        """
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            response = requests.get(self.models_endpoint, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                models = data.get("data", [])
                
                # Check if it's a paid account by looking for premium models
                has_grok = any('grok' in model.get('id', '').lower() for model in models)
                has_grok_beta = any('grok-beta' in model.get('id', '').lower() for model in models)
                account_type = "Paid" if (has_grok or has_grok_beta) else "Free"
                
                message = f"✅ Valid Grok API key ({account_type} account)"
                return True, message, data
                
            elif response.status_code == 401:
                return False, "❌ Invalid Grok API key - Authentication failed", None
            elif response.status_code == 403:
                return False, "❌ Grok API key access denied - Check permissions", None
            elif response.status_code == 429:
                return False, "❌ Grok API rate limit exceeded", None
            else:
                return False, f"❌ Grok API error: {response.status_code}", None
                
        except requests.exceptions.Timeout:
            return False, "❌ Grok API request timed out", None
        except requests.exceptions.RequestException as e:
            return False, f"❌ Grok API connection error: {str(e)}", None
        except Exception as e:
            return False, f"❌ Unexpected error: {str(e)}", None
    
    def get_model_details(self, api_key: str) -> Dict:
        """Get detailed model information"""
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            response = requests.get(self.models_endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = data.get("data", [])
                
                # Categorize models
                grok_models = [m for m in models if 'grok' in m.get('id', '').lower()]
                other_models = [m for m in models if 'grok' not in m.get('id', '').lower()]
                
                # Build per-model metrics (xAI model list typically does not expose rpm/rpd/tpm)
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
                    'grok_models': len(grok_models),
                    'other_models': len(other_models),
                    'all_models': [m.get('id') for m in models],
                    'grok_model_list': [m.get('id') for m in grok_models],
                    'per_model': per_model
                }
            else:
                return {'error': f'Failed to fetch models: {response.status_code}'}
        except Exception as e:
            return {'error': f'Error fetching models: {str(e)}'}
    
    def check_account_status(self, api_key: str) -> Dict:
        """Check if account has access to paid features"""
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            response = requests.get(self.models_endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = data.get("data", [])
                
                # Check for premium models
                has_grok = any('grok' in m.get('id', '').lower() for m in models)
                has_grok_beta = any('grok-beta' in m.get('id', '').lower() for m in models)
                has_grok_pro = any('grok-pro' in m.get('id', '').lower() for m in models)
                
                return {
                    'is_paid': has_grok or has_grok_beta or has_grok_pro,
                    'has_grok': has_grok,
                    'has_grok_beta': has_grok_beta,
                    'has_grok_pro': has_grok_pro,
                    'account_type': 'Paid' if (has_grok or has_grok_beta or has_grok_pro) else 'Free'
                }
            else:
                return {'error': f'Failed to check account status: {response.status_code}'}
        except Exception as e:
            return {'error': f'Error checking account status: {str(e)}'}

    def get_model_info(self, api_key: str, model_id: str) -> Dict:
        """Fetch a single model's details. Falls back to scanning the list if needed."""
        headers = {"Authorization": f"Bearer {api_key}"}
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
