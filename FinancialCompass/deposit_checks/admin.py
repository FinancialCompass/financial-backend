from django.contrib import admin
from .models import CheckDeposit

@admin.register(CheckDeposit)
class CheckDepositAdmin(admin.ModelAdmin):
    list_display = ('check_number', 'amount', 'payee_name', 'deposit_date', 'status')
    list_filter = ('status', 'deposit_date', 'bank_name')
    search_fields = ('check_number', 'payee_name', 'memo')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Check Information', {
            'fields': ('check_number', 'amount', 'payee_name', 'memo')
        }),
        ('Bank Details', {
            'fields': ('bank_name', 'routing_number', 'account_number')
        }),
        ('Status', {
            'fields': ('deposit_date', 'status')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
