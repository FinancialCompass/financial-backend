import requests
from django.conf import settings

class PinataService:
    def __init__(self):
        self.api_key = settings.PINATA_API_KEY
        self.secret_key = settings.PINATA_SECRET_KEY
        self.headers = {
            'pinata_api_key': self.api_key,
            'pinata_secret_api_key': self.secret_key,
        }

    def upload_file(self, file_data):
        try:
            url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
            files = {'file': file_data}
            response = requests.post(url, headers=self.headers, files=files)
            
            if response.status_code != 200:
                raise Exception(f"Pinata upload failed: {response.text}")
                
            return response.json()['IpfsHash']
        except Exception as e:
            raise Exception(f"Pinata Error: {str(e)}")