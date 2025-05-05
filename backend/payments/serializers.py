from rest_framework import serializers
from .models import Payment, Transaction
from tours.serializers import ParticipationSerializer
from tours.models import Participation


class PaymentSerializer(serializers.ModelSerializer):
    participation = ParticipationSerializer(read_only=True)
    
    class Meta:
        model = Payment
        fields = ['id', 'participation', 'amount', 'status', 'transaction_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class PaymentCreateSerializer(serializers.ModelSerializer):
    participation_id = serializers.PrimaryKeyRelatedField(
        queryset=Participation.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Payment
        fields = ['participation_id', 'amount']
    
    def create(self, validated_data):
        participation = validated_data.pop('participation_id')
        payment = Payment.objects.create(participation=participation, **validated_data)
        return payment


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'payment', 'amount', 'transaction_type', 'description', 'timestamp']
        read_only_fields = ['id', 'user', 'payment', 'timestamp'] 