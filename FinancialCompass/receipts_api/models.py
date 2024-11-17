from django.db import models
from django.utils import timezone
from decimal import Decimal

class Receipt(models.Model):
    store_name = models.CharField(max_length=255)
    date = models.DateField(null=True, blank=True)
    subtotal = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        null=True,
        blank=True
    )
    tax = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        null=True,
        blank=True
    )
    total = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00'),
        null=True,
        blank=True
    )
    ipfs_hash = models.CharField(max_length=255, null=True, blank=True)
    raw_response = models.JSONField(default=dict, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.store_name} - {self.date or 'No date'} (${self.total or 0})"

    @property
    def ipfs_url(self):
        if self.ipfs_hash:
            return f"https://gateway.pinata.cloud/ipfs/{self.ipfs_hash}"
        return None

class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=Decimal('0.00')
    )
    purchase_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=255,default='food')
    def __str__(self):
        return f"{self.name} - ${self.price}"