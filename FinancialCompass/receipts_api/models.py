from django.db import models
from django.utils import timezone

class Receipt(models.Model):
    store_name = models.CharField(max_length=255, default='Unknown Store')
    date = models.DateField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    ipfs_hash = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.store_name} - {self.date}"

    class Meta:
        ordering = ['-date']

class ReceiptItem(models.Model):
    CATEGORY_CHOICES = [
        ('GROCERY', 'Grocery'),
        ('ELECTRONICS', 'Electronics'),
        ('CLOTHING', 'Clothing'),
        ('FOOD', 'Food & Dining'),
        ('OTHER', 'Other'),
    ]

    receipt = models.ForeignKey(Receipt, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='Unknown Item')
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='OTHER'
    )

    def __str__(self):
        return f"{self.name} ({self.receipt.store_name})"