from django.shortcuts import render
from django.http import JsonResponse
from receipts_api.models import Receipt
from django.utils.dateparse import parse_date
from django.shortcuts import get_object_or_404
from .serializers import ReceiptSerializer, ReceiptItemSerializer

# Create your views here.
def getChecks(request):

    receipts = Receipt.objects.all()  # Fetch all receipts
    serializer = ReceiptSerializer(receipts, many=True)
    return JsonResponse(serializer.data, safe=False)

def getCheckById(request, check_id):
    receipt = get_object_or_404(Receipt, id=check_id)
    
    receipt_serializer = ReceiptSerializer(receipt)
    items_serializer = ReceiptItemSerializer(receipt.items.all(), many=True)

    # Combine the data into a dictionary to send back in the response
    response_data = {
        "receipt": receipt_serializer.data,
        "items": items_serializer.data
    }

    # Return the combined data as JSON response
    return JsonResponse(response_data, safe=False)
def getCheckItemsByDateRange(request):

    # Get start and end dates from the query parameters
    start_date_str = request.GET.get('start_date')  # Example: '2024-01-01'
    end_date_str = request.GET.get('end_date')  # Example: '2024-12-31'

    if not start_date_str or not end_date_str:
        return JsonResponse({'error': 'Please provide both start_date and end_date.'}, status=400)

    # Parse the string dates into date objects
    start_date = parse_date(start_date_str)
    end_date = parse_date(end_date_str)

    if not start_date or not end_date:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    # Filter receipts within the date range
    receipts = Receipt.objects.filter(date__range=[start_date, end_date])

    # Fetch all associated items for the filtered receipts
    items = []
    for receipt in receipts:
        items.extend(receipt.items.all())  # Get all items for each receipt

    # Serialize the list of items
    items_serializer = ReceiptItemSerializer(items, many=True)

    # Return the serialized data as JSON
    return JsonResponse(items_serializer.data, safe=False)