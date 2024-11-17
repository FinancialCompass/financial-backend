from django.contrib import admin
from .models import Receipt, ReceiptItem

class ReceiptItemInline(admin.TabularInline):
    model = ReceiptItem
    extra = 1
    fields = ('name', 'quantity', 'price', 'category')

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('store_name', 'date', 'total_amount', 'tax_amount', 'created_at')
    list_filter = ('store_name', 'date')
    search_fields = ('store_name', 'ipfs_hash')
    readonly_fields = ('created_at', 'ipfs_hash')
    inlines = [ReceiptItemInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('store_name', 'date')
        }),
        ('Financial Details', {
            'fields': ('total_amount', 'tax_amount')
        }),
        ('Technical Details', {
            'fields': ('ipfs_hash', 'created_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(ReceiptItem)
class ReceiptItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'receipt', 'quantity', 'price', 'category')
    list_filter = ('receipt__store_name', 'category')
    search_fields = ('name', 'receipt__store_name')
