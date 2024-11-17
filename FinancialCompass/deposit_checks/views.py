from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CheckDeposit
from .serializers import CheckDepositSerializer

# Create your views here.

class CheckDepositViewSet(viewsets.ModelViewSet):
    queryset = CheckDeposit.objects.all()
    serializer_class = CheckDepositSerializer

    @action(detail=True, methods=['post'])
    def process_deposit(self, request, pk=None):
        check = self.get_object()
        check.status = 'COMPLETED'
        check.save()
        return Response({
            'status': 'success',
            'message': f'Check #{check.check_number} has been processed'
        })
