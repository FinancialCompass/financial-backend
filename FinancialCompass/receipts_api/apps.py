from django.apps import AppConfig
from django.contrib import admin


class ReceiptsApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "receipts_api"
    
    def ready(self):
        # Customize admin site
        admin.site.site_header = 'Receipt Analysis Admin'
        admin.site.site_title = 'Receipt Analysis Portal'
        admin.site.index_title = 'Welcome to Receipt Analysis Portal'
