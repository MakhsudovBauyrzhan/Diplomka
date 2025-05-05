from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone

from .models import Payment, Transaction
from .serializers import (
    PaymentSerializer, 
    PaymentCreateSerializer,
    TransactionSerializer
)
from tours.models import Tour, Participation


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return PaymentCreateSerializer
        return PaymentSerializer
    
    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(participation__user=user)
    
    def perform_create(self, serializer):
        with transaction.atomic():
            # Create payment
            payment = serializer.save()
            
            # Link to participation and update its payment status
            participation = payment.participation
            participation.payment_status = True
            participation.save()
            
            # Create transaction record
            Transaction.objects.create(
                user=participation.user,
                payment=payment,
                amount=payment.amount,
                transaction_type='payment',
                description=f"Payment for {participation.tour.title}"
            )
    
    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        payment = self.get_object()
        
        # Check if payment is eligible for refund
        if payment.status != 'completed':
            return Response(
                {"error": "Only completed payments can be refunded"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        with transaction.atomic():
            # Update payment status
            payment.status = 'refunded'
            payment.save()
            
            # Update participation payment status
            participation = payment.participation
            participation.payment_status = False
            participation.save()
            
            # Create refund transaction
            Transaction.objects.create(
                user=participation.user,
                payment=payment,
                amount=payment.amount,
                transaction_type='refund',
                description=f"Refund for {participation.tour.title}"
            )
        
        return Response({"message": "Payment refunded successfully"}, status=status.HTTP_200_OK)


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Transaction.objects.filter(user=user).order_by('-timestamp')
