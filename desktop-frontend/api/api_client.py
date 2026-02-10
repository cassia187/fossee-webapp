import requests
from typing import Optional, Dict, List

class APIClient:
    """
    API Client for connecting PyQt frontend to Django backend
    """
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.token = None
    
    def get_headers(self):
        """Get authorization headers with token"""
        if self.token:
            return {'Authorization': f'Token {self.token}'}
        return {}
    
    # ========== Authentication Endpoints ==========
    
    def register(self, username: str, email: str, password: str) -> Dict:
        """
        Register a new user
        Returns: {'success': bool, 'message': str, 'token': str (if success)}
        """
        try:
            response = requests.post(
                f"{self.base_url}/register/",
                json={
                    'username': username,
                    'email': email,
                    'password': password
                }
            )
            
            if response.status_code == 201:
                data = response.json()
                self.token = data.get('token')
                return {
                    'success': True,
                    'message': 'Registration successful',
                    'token': self.token,
                    'user': data.get('user')
                }
            else:
                error_data = response.json()
                error_msg = str(error_data)
                return {
                    'success': False,
                    'message': f'Registration failed: {error_msg}'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Connection error: {str(e)}'
            }
    
    def login(self, username: str, password: str) -> Dict:
        """
        Login user and get authentication token
        Returns: {'success': bool, 'message': str, 'token': str (if success)}
        """
        try:
            response = requests.post(
                f"{self.base_url}/login/",
                json={'username': username, 'password': password}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                return {
                    'success': True,
                    'message': 'Login successful',
                    'token': self.token,
                    'user': data.get('user')
                }
            else:
                return {
                    'success': False,
                    'message': 'Invalid username or password'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Connection error: {str(e)}'
            }
    
    def logout(self) -> Dict:
        """
        Logout user and delete token
        Returns: {'success': bool, 'message': str}
        """
        try:
            response = requests.post(
                f"{self.base_url}/logout/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                self.token = None
                return {
                    'success': True,
                    'message': 'Logged out successfully'
                }
            else:
                return {
                    'success': False,
                    'message': 'Logout failed'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Connection error: {str(e)}'
            }
    
    def get_profile(self) -> Optional[Dict]:
        """
        Get user profile with datasets info
        Returns: User profile data or None
        """
        try:
            response = requests.get(
                f"{self.base_url}/profile/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error getting profile: {e}")
            return None
    
    # ========== Dataset Endpoints ==========
    
    def upload_dataset(self, file_path: str) -> Dict:
        """
        Upload a CSV dataset
        Returns: {'success': bool, 'message': str, 'dataset': dict (if success)}
        """
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(
                    f"{self.base_url}/upload/",
                    files=files,
                    headers=self.get_headers()
                )
            
            if response.status_code == 201:
                data = response.json()
                return {
                    'success': True,
                    'message': data.get('message', 'Upload successful'),
                    'dataset': data.get('dataset')
                }
            else:
                error_data = response.json()
                return {
                    'success': False,
                    'message': error_data.get('error', 'Upload failed')
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Upload error: {str(e)}'
            }
    
    def get_datasets(self) -> List[Dict]:
        """
        Get all datasets for the current user
        Returns: List of datasets or empty list
        """
        try:
            response = requests.get(
                f"{self.base_url}/datasets/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return []
        except Exception as e:
            print(f"Error getting datasets: {e}")
            return []
    
    def get_dataset_details(self, dataset_id: int) -> Optional[Dict]:
        """
        Get detailed information about a specific dataset
        Returns: Dataset details or None
        """
        try:
            response = requests.get(
                f"{self.base_url}/datasets/{dataset_id}/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error getting dataset details: {e}")
            return None
    
    def delete_dataset(self, dataset_id: int) -> Dict:
        """
        Delete a dataset
        Returns: {'success': bool, 'message': str}
        """
        try:
            response = requests.delete(
                f"{self.base_url}/datasets/{dataset_id}/delete/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                return {
                    'success': True,
                    'message': 'Dataset deleted successfully'
                }
            else:
                return {
                    'success': False,
                    'message': 'Delete failed'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Delete error: {str(e)}'
            }
    
    def get_type_distribution(self, dataset_id: int) -> Optional[Dict]:
        """
        Get equipment type distribution for a dataset
        Returns: Distribution data or None
        """
        try:
            response = requests.get(
                f"{self.base_url}/datasets/{dataset_id}/type_distribution/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error getting type distribution: {e}")
            return None
    
    def download_report(self, dataset_id: int, save_path: str) -> Dict:
        """
        Download PDF report for a dataset
        Returns: {'success': bool, 'message': str}
        """
        try:
            response = requests.get(
                f"{self.base_url}/datasets/{dataset_id}/report/",
                headers=self.get_headers()
            )
            
            if response.status_code == 200:
                with open(save_path, 'wb') as f:
                    f.write(response.content)
                return {
                    'success': True,
                    'message': f'Report saved to {save_path}'
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to download report'
                }
        except Exception as e:
            return {
                'success': False,
                'message': f'Download error: {str(e)}'
            }
    
    def health_check(self) -> bool:
        """
        Check if API server is running
        Returns: True if server is up, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/health_check/")
            return response.status_code == 200
        except:
            return False
