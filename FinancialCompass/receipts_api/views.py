from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import google.generativeai as genai
import os
from PIL import Image
import logging
import json
from decimal import Decimal
from django.core.files.base import ContentFile
from .models import Receipt, ReceiptItem
import requests
from django.conf import settings
from datetime import datetime


logger = logging.getLogger(__name__)

class ReceiptViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pinata_api_key = os.getenv('PINATA_API_KEY')
        self.pinata_secret_key = os.getenv('PINATA_SECRET_KEY')
        genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def upload_to_pinata(self, file):
        url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
        
        headers = {
            'pinata_api_key': self.pinata_api_key,
            'pinata_secret_api_key': self.pinata_secret_key
        }
        
        files = {
            'file': file
        }
        
        response = requests.post(url, headers=headers, files=files)
        
        if response.status_code == 200:
            return response.json()['IpfsHash']
        else:
            raise Exception(f"Pinata upload failed: {response.text}")

    @action(detail=False, methods=['POST'])
    def process_receipt(self, request):
        try:
            file = request.FILES.get('file')
            if not file:
                return Response({'error': 'No file provided'}, status=400)

            # Process with Gemini
            image = Image.open(file)
            prompt = """
            Analyze this receipt and provide a JSON response with:
            - store_name: Name of the store/restaurant
            - date: Date of purchase (YYYY-MM-DD format)
            - items: Array of items, each with:
                - name: Item name
                - price: Price as number
                - category: the category of the item
            - subtotal: Subtotal before tax
            - tax: Tax amount
            - total: Total amount

            Format all numbers as decimal values without currency symbols.
            Format the date in YYYY-MM-DD format.
            """

            response = self.model.generate_content([prompt, image])
            response_text = response.text
            
            if '```json' in response_text:
                json_str = response_text.split('```json')[1].split('```')[0].strip()
            else:
                json_str = response_text.strip()
            
            receipt_data = json.loads(json_str)
            
            # Parse the date string to a datetime object
            try:
                receipt_date = datetime.strptime(receipt_data['date'], '%Y-%m-%d').date()
            except ValueError:
                try:
                    receipt_date = datetime.strptime(receipt_data['date'], '%m/%d/%Y').date()
                except ValueError:
                    try:
                        receipt_date = datetime.strptime(receipt_data['date'], '%m-%d-%Y').date()
                    except ValueError:
                        receipt_date = None

            # Create Receipt instance
            receipt = Receipt.objects.create(
                store_name=receipt_data['store_name'],
                date=receipt_date,
                subtotal=Decimal(str(receipt_data['subtotal'])),
                tax=Decimal(str(receipt_data['tax'])),
                total=Decimal(str(receipt_data['total'])),
                raw_response=receipt_data
            )
            
            # Create ReceiptItem instances
            for item in receipt_data['items']:
                ReceiptItem.objects.create(
                    receipt=receipt,
                    name=item['name'],
                    price=Decimal(str(item['price'])),
                    purchase_date=receipt_date,
                    category= item['category']
                )

            return Response({
                'success': True,
                'receipt_data': receipt_data
            })

        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({
                'error': str(e)
            }, status=500)
