from django.db import models
from django.utils import timezone

class CheckDeposit(models.Model):
    DEPOSIT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    ]

    check_number = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payee_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    routing_number = models.CharField(max_length=9)
    account_number = models.CharField(max_length=17)
    deposit_date = models.DateField(default=timezone.now)
    memo = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=10, choices=DEPOSIT_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Check #{self.check_number} - ${self.amount}"

    class Meta:
        ordering = ['-deposit_date']
