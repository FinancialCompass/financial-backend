from rest_framework import serializers
from .models import CheckDeposit

class CheckDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckDeposit
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at', 'status')
