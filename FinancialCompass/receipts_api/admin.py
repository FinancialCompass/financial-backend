from django.contrib import admin
from .models import Receipt, ReceiptItem

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'date', 'total', 'tax')
    list_filter = ('date', 'store_name')
    search_fields = ('store_name', 'raw_response')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('store_name', 'date', 'image')
        }),
        ('Financial Details', {
            'fields': ('subtotal', 'tax', 'total')
        }),
        ('System Fields', {
            'fields': ('raw_response', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ReceiptItem)
class ReceiptItemAdmin(admin.ModelAdmin):
    list_display = ('receipt', 'name', 'price')
    list_filter = ('receipt__store_name',)
    search_fields = ('name', 'receipt__store_name')
    
    fieldsets = (
        ('Item Details', {
            'fields': ('receipt', 'name', 'price')
        }),
    )
