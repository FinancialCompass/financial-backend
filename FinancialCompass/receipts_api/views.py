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

logger = logging.getLogger(__name__)

class ReceiptViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            api_key = os.getenv('GEMINI_API_KEY')
            print(f"Initializing with Gemini API key: {'Present' if api_key else 'Missing'}")
            if not api_key:
                raise ValueError("GEMINI_API_KEY not configured")
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')
            print("Gemini model initialized successfully")
        except Exception as e:
            print(f"Error initializing Gemini: {str(e)}")
            raise

    @action(detail=False, methods=['POST'])
    def process_receipt(self, request):
        print("\n=== Starting Receipt Processing ===")
        try:
            file = request.FILES.get('file')
            if not file:
                print("No file received in request")
                return Response({'error': 'No file provided'}, status=400)
            print(f"Received file: {file.name} ({file.size} bytes)")

            try:
                image = Image.open(file)
                print(f"Image opened successfully: {image.format}, size: {image.size}")
            except Exception as e:
                print(f"Error opening image: {str(e)}")
                return Response({'error': f'Error opening image: {str(e)}'}, status=400)

            prompt = """
            Analyze this receipt and provide a JSON response with:
            - store_name: Name of the store/restaurant
            - date: Date of purchase (YYYY-MM-DD format)
            - items: Array of items, each with:
                - name: Item name
                - price: Price as number
            - subtotal: Subtotal before tax
            - tax: Tax amount
            - total: Total amount

            Format all numbers as decimal values without currency symbols.
            """
            print("Prompt prepared, sending to Gemini...")

            try:
                response = self.model.generate_content([prompt, image])
                print("Received response from Gemini")
                print(f"Raw response: {response.text[:200]}...")
            except Exception as e:
                print(f"Gemini API error: {str(e)}")
                return Response({'error': f'Gemini API error: {str(e)}'}, status=500)

            try:
                response_text = response.text
                if '```json' in response_text:
                    json_str = response_text.split('```json')[1].split('```')[0].strip()
                else:
                    json_str = response_text.strip()
                print(f"Processed response: {json_str[:200]}...")

                # Parse the JSON response
                receipt_data = json.loads(json_str)
                
                # Create Receipt instance
                receipt = Receipt.objects.create(
                    store_name=receipt_data['store_name'],
                    date=receipt_data['date'],
                    subtotal=Decimal(str(receipt_data['subtotal'])),
                    tax=Decimal(str(receipt_data['tax'])),
                    total=Decimal(str(receipt_data['total'])),
                    raw_response=receipt_data
                )
                
                # Save the image
                receipt.image.save(file.name, ContentFile(file.read()), save=True)
                
                # Create ReceiptItem instances
                for item in receipt_data['items']:
                    ReceiptItem.objects.create(
                        receipt=receipt,
                        name=item['name'],
                        price=Decimal(str(item['price']))
                    )
                
                print(f"Receipt saved with ID: {receipt.id}")
                
                return Response({
                    'success': True,
                    'receipt_id': receipt.id,
                    'receipt_data': receipt_data
                })

            except json.JSONDecodeError as e:
                print(f"JSON parsing error: {str(e)}")
                return Response({
                    'error': f'Invalid JSON response from Gemini: {str(e)}',
                    'raw_response': json_str
                }, status=500)
            except Exception as e:
                print(f"Unexpected error: {str(e)}")
                return Response({
                    'error': str(e)
                }, status=500)

        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({
                'error': str(e)
            }, status=500)
