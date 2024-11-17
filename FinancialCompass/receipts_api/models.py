from django.db import models
from django.contrib.auth.models import User

class Receipt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ipfs_hash = models.CharField(max_length=500)
    store_name = models.CharField(max_length=200, null=True)
    date = models.DateField(null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ReceiptItem(models.Model):
    receipt = models.ForeignKey(Receipt, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)