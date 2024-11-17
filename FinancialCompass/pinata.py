import requests
import os
from dotenv import load_dotenv

load_dotenv()

class PinataClient:
    def __init__(self):
        self.api_key = os.getenv('PINATA_API_KEY')
        self.api_secret = os.getenv('PINATA_API_SECRET')
        self.headers = {
            'pinata_api_key': self.api_key,
            'pinata_secret_api_key': self.api_secret
        }
        self.base_url = 'https://api.pinata.cloud'

    def upload_file(self, file_data):
        try:
            url = f"{self.base_url}/pinning/pinFileToIPFS"
            
            files = {
                'file': file_data
            }
            
            response = requests.post(
                url,
                files=files,
                headers=self.headers
            )
            
            if response.status_code == 200:
                return response.json()['IpfsHash']
            else:
                raise Exception(f"Pinata upload failed: {response.text}")
                
        except Exception as e:
            raise Exception(f"Error uploading to Pinata: {str(e)}")