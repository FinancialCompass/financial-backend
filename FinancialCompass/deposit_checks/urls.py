from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CheckDepositViewSet

# Create a router and register our viewsets
router = DefaultRouter()
router.register(r'checks', CheckDepositViewSet, basename='check')

# The API URLs are determined automatically by the router
urlpatterns = router.urls  # Note: this is different from before
