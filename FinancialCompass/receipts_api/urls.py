from django.urls import path
from .views import ReceiptViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'receipts', ReceiptViewSet, basename='receipt')

urlpatterns = router.urls
