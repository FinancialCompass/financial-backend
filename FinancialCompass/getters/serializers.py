# serializers.py (inside the 'getters' app)
from rest_framework import serializers
from receipts_api.models import Receipt, ReceiptItem

class ReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptItem
        fields = '__all__'

class ReceiptSerializer(serializers.ModelSerializer):
    items = ReceiptItemSerializer(many=True)  # Nested serializer for items

    class Meta:
        model = Receipt
        fields = '__all__'