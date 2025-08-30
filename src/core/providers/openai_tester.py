import requests
import json
from typing import Dict, List, Tuple, Optional

class OpenAITester:
    """Test OpenAI API key validity and get model information"""
    
    def __init__(self):
        self.base_url = "https://api.openai.com/v1"
        self.models_endpoint = f"{self.base_url}/models"
        self.usage_endpoint = f"{self.base_url}/usage"
    
    def test_api_key(self, api_key: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Test if an OpenAI API key is valid
        
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
                models = data.get('data', [])
                
                # Check if it's a paid account by looking for GPT-4 models
                has_gpt4 = any('gpt-4' in model.get('id', '').lower() for model in models)
                account_type = "Paid" if has_gpt4 else "Free"
                
                message = f"✅ Valid OpenAI API key ({account_type} account)"
                return True, message, data
                
            elif response.status_code == 401:
                return False, "❌ Invalid OpenAI API key - Authentication failed", None
            elif response.status_code == 403:
                return False, "❌ OpenAI API key access denied - Check permissions", None
            else:
                return False, f"❌ OpenAI API error: {response.status_code}", None
                
        except requests.exceptions.Timeout:
            return False, "❌ OpenAI API request timed out", None
        except requests.exceptions.RequestException as e:
            return False, f"❌ OpenAI API connection error: {str(e)}", None
        except Exception as e:
            return False, f"❌ Unexpected error: {str(e)}", None
    
    def get_model_details(self, api_key: str) -> Dict:
        """Get detailed model information"""
        headers = {"Authorization": f"Bearer {api_key}"}
        
        try:
            response = requests.get(self.models_endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                models = data.get('data', [])
                
                # Categorize models
                gpt_models = [m for m in models if 'gpt' in m.get('id', '').lower()]
                embedding_models = [m for m in models if 'embedding' in m.get('id', '').lower()]
                other_models = [m for m in models if 'gpt' not in m.get('id', '').lower() and 'embedding' not in m.get('id', '').lower()]
                
                # Build per-model metrics where available (OpenAI models API does not expose rpm/rpd/tpm)
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
                    'gpt_models': len(gpt_models),
                    'embedding_models': len(embedding_models),
                    'other_models': len(other_models),
                    'all_models': [m.get('id') for m in models],
                    'gpt_model_list': [m.get('id') for m in gpt_models],
                    'embedding_model_list': [m.get('id') for m in embedding_models],
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
                models = data.get('data', [])
                
                # Check for premium models
                has_gpt4 = any('gpt-4' in m.get('id', '').lower() for m in models)
                has_gpt4_turbo = any('gpt-4-turbo' in m.get('id', '').lower() for m in models)
                has_gpt4o = any('gpt-4o' in m.get('id', '').lower() for m in models)
                
                return {
                    'is_paid': has_gpt4 or has_gpt4_turbo or has_gpt4o,
                    'has_gpt4': has_gpt4,
                    'has_gpt4_turbo': has_gpt4_turbo,
                    'has_gpt4o': has_gpt4o,
                    'account_type': 'Paid' if (has_gpt4 or has_gpt4_turbo or has_gpt4o) else 'Free'
                }
            else:
                return {'error': f'Failed to check account status: {response.status_code}'}
        except Exception as e:
            return {'error': f'Error checking account status: {str(e)}'}

    def get_model_info(self, api_key: str, model_id: str) -> Dict:
        """Fetch a single model's details. Falls back to scanning the list if needed."""
        headers = {"Authorization": f"Bearer {api_key}"}
        try:
            # Try direct model endpoint
            resp = requests.get(f"{self.models_endpoint}/{model_id}", headers=headers, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            # Fallback: list and find
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
