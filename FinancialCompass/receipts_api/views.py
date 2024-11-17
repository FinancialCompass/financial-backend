from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .services.pinata_service import PinataService
from .services.gemini_service import GeminiService
from .services.appwrite_service import AppwriteService
import json

# Create your views here.

class ReceiptViewSet(viewsets.ModelViewSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pinata = PinataService()
        self.gemini = GeminiService()
        self.appwrite = AppwriteService()

    @action(detail=False, methods=['POST'])
    def process_receipt(self, request):
        try:
            # 1. Get file and upload to Pinata
            receipt_file = request.FILES.get('file')
            if not receipt_file:
                return Response({'error': 'No file provided'}, status=400)

            ipfs_hash = self.pinata.upload_file(receipt_file)

            # 2. Process with Gemini
            receipt_json = self.gemini.process_receipt(ipfs_hash)
            receipt_data = json.loads(receipt_json)

            # 3. Save to Appwrite (if using)
            appwrite_doc = self.appwrite.create_transaction(
                request.data.get('user_id'),
                receipt_data,
                ipfs_hash
            )

            return Response({
                'success': True,
                'ipfs_hash': ipfs_hash,
                'receipt_data': receipt_data,
                'appwrite_id': appwrite_doc['$id'] if appwrite_doc else None
            })

        except Exception as e:
            return Response({
                'success': False,
                'error': str(e)
            }, status=500)
