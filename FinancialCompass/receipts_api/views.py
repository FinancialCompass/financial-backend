from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import json
from .models import Receipt, ReceiptItem
from .gemini_client import GeminiClient

# Create your views here.

class ReceiptViewSet(viewsets.ModelViewSet):
    @action(detail=False, methods=['POST'])
    def process(self, request):
        try:
            # 1. Get IPFS hash from frontend
            ipfs_hash = request.data.get('ipfs_hash')
            if not ipfs_hash:
                return Response({'error': 'No IPFS hash provided'}, status=400)

            # 2. Process with Gemini
            gemini = GeminiClient()
            receipt_data = json.loads(gemini.process_receipt(ipfs_hash))

            # 3. Save to database (optional, depending on your needs)
            receipt = Receipt.objects.create(
                ipfs_hash=ipfs_hash,
                store_name=receipt_data.get('store_name'),
                date=receipt_data.get('date'),
                total_amount=receipt_data.get('total'),
                tax_amount=receipt_data.get('tax')
            )

            return Response({
                'message': 'Receipt processed successfully',
                'data': receipt_data
            })

        except Exception as e:
            return Response({'error': str(e)}, status=500)
