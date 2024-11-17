import google.generativeai as genai
import requests
from PIL import Image
from io import BytesIO
import os

class GeminiClient:
    def __init__(self):
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        self.model = genai.GenerativeModel('gemini-pro-vision')

    def process_receipt(self, ipfs_hash):
        # Get image from IPFS
        ipfs_url = f"https://gateway.pinata.cloud/ipfs/{ipfs_hash}"
        response = requests.get(ipfs_url)
        img = Image.open(BytesIO(response.content))

        # Process with Gemini
        prompt = """
        Analyze this receipt image and return the data in the following JSON format:
        {
            "store_name": "store name",
            "date": "YYYY-MM-DD",
            "items": [
                {
                    "name": "item name",
                    "quantity": number,
                    "price": number
                }
            ],
            "total": number,
            "tax": number
        }
        Extract only what you can see clearly and return null for missing values.
        """

        response = self.model.generate_content([prompt, img])
        return response.text  # This will be JSON string

# backend/receipts_api/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Receipt, ReceiptItem
from .gemini_client import GeminiClient
import json

class ReceiptViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['POST'])
    def process(self, request):
        try:
            ipfs_hash = request.data.get('ipfs_hash')
            if not ipfs_hash:
                return Response({'error': 'No IPFS hash provided'}, status=400)

            # Process with Gemini
            gemini = GeminiClient()
            receipt_data = json.loads(gemini.process_receipt(ipfs_hash))

            # Save to database
            receipt = Receipt.objects.create(
                user=request.user,
                ipfs_hash=ipfs_hash,
                store_name=receipt_data.get('store_name'),
                date=receipt_data.get('date'),
                total_amount=receipt_data.get('total'),
                tax_amount=receipt_data.get('tax')
            )

            # Save items
            for item in receipt_data.get('items', []):
                ReceiptItem.objects.create(
                    receipt=receipt,
                    name=item['name'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            return Response({
                'message': 'Receipt processed successfully',
                'data': receipt_data
            })

        except Exception as e:
            return Response({'error': str(e)}, status=500)