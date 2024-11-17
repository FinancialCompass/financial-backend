from django.urls import path
from .views import getChecks
from .views import getCheckById
from .views import getCheckItemsByDateRange
urlpatterns = [
    path('', getChecks, name='get-checks'),
    path('<int:check_id>/', getCheckById, name='get-check-by-id'),
    path('items/', getCheckItemsByDateRange, name='get-check-items-by-date-range'),
]