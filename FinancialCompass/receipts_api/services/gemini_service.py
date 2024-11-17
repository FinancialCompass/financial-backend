import google.generativeai as genai
from django.conf import settings
import requests
import base64
from PIL import Image
from io import BytesIO

class GeminiService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro-vision')

    def get_image_from_ipfs(self, ipfs_hash):
        """Fetch image from IPFS gateway"""
        url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
        response = requests.get(url)
        if response.status_code != 200:
            raise Exception("Failed to fetch image from IPFS")
        return response.content

    def process_receipt(self, ipfs_hash):
        try:
            # Get image from IPFS
            image_content = self.get_image_from_ipfs(ipfs_hash)
            
            # Convert to PIL Image
            image = Image.open(BytesIO(image_content))

            # Prompt for Gemini
            prompt = """
            Analyze this receipt image and extract the following information in JSON format:
            - store_name: The name of the store
            - date: The date of purchase (YYYY-MM-DD format)
            - total: The total amount
            - tax: The tax amount
            - items: Array of items, each with:
              - name: Item name
              - quantity: Number of items
              - price: Price per item
            Only return the JSON, no additional text.
            """

            # Generate response from Gemini
            response = self.model.generate_content([prompt, image])
            
            # Extract JSON from response
            # Note: Gemini might wrap the JSON in markdown code blocks
            response_text = response.text
            if "```json" in response_text:
                # Extract JSON from code block
                response_text = response_text.split("```json")[1].split("```")[0]
            
            return response_text.strip()

        except Exception as e:
            raise Exception(f"Gemini Processing Error: {str(e)}")