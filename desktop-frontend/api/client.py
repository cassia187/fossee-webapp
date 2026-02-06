import requests

class APIClient:
    def __init__(self, base_url="http://localhost:8000/api"):
        self.base_url = base_url
        self.token = None
    
    def login(self, username, password):
        response = requests.post(f"{self.base_url}/login/", json={'username': username, 'password': password})
        if response.status_code == 200:
            self.token = response.json()['token']
            return True
        return False
    
    def get_headers(self):
        return {
            'Authorization': f'Token {self.token}'
        }
    
    def upload_dataset(self, file):
        with open(file, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{self.base_url}/upload/",
                files=files,
                headers=self.get_headers()
            )
        if response.status_code == 201:
            return response.json() 
        else:
            return None
    
    # Returns list of datasets [200] or empty list []
    def get_datasets(self):
        response = requests.get(
            f"{self.base_url}/datasets/",
            headers=self.get_headers()
        )
        if response.status_code == 200:
            return response.json()
        return []

    def get_profile(self):
        response = requests.get(
            f"{self.base_url}/profile/",
            headers=self.get_headers()
        )
        if response.status_code == 200:
            return response.json()
        return None