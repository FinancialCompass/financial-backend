from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .services.pinata_service import PinataService
from .services.gemini_service import GeminiService

# Create your views here.

class ReceiptViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pinata = PinataService()
        self.gemini = GeminiService()

    @action(detail=False, methods=['POST'])
    def process_receipt(self, request):
        try:
            # Get file from request
            receipt_file = request.FILES.get('file')
            if not receipt_file:
                return Response({'error': 'No file provided'}, status=400)

            # Upload to Pinata
            ipfs_hash = self.pinata.upload_file(receipt_file)

            # Process with Gemini
            receipt_data = self.gemini.process_receipt(ipfs_hash)

            return Response({
                'success': True,
                'ipfs_hash': ipfs_hash,
                'receipt_data': receipt_data
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)
