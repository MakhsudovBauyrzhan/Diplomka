from django.shortcuts import render
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from datetime import timedelta
import uuid

from .models import EmailVerification
from .serializers import (
    UserSerializer, 
    UserRegisterSerializer, 
    ChangePasswordSerializer,
    EmailVerificationSerializer,
    UserProfileUpdateSerializer
)

User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create email verification token
        token = str(uuid.uuid4())
        expires_at = timezone.now() + timedelta(days=1)
        EmailVerification.objects.create(user=user, token=token, expires_at=expires_at)
        
        # Send verification email
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
        send_mail(
            'Verify your email address',
            f'Please click the link to verify your email: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return Response(
            {"message": "User registered successfully. Please check your email for verification."},
            status=status.HTTP_201_CREATED
        )


class EmailVerificationView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = EmailVerificationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        
        try:
            verification = EmailVerification.objects.get(token=token)
            
            # Check if token is expired
            if verification.expires_at < timezone.now():
                return Response(
                    {"error": "Verification link has expired. Please request a new one."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Mark user as verified
            user = verification.user
            user.is_email_verified = True
            user.save()
            
            # Delete the verification object
            verification.delete()
            
            return Response({"message": "Email verified successfully."}, status=status.HTTP_200_OK)
            
        except EmailVerification.DoesNotExist:
            return Response(
                {"error": "Invalid verification token."},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserProfileUpdateView(generics.UpdateAPIView):
    serializer_class = UserProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        
        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)


class ResendVerificationEmailView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        user = request.user
        
        # Check if user is already verified
        if user.is_email_verified:
            return Response(
                {"message": "Email is already verified."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Delete existing verification if any
        EmailVerification.objects.filter(user=user).delete()
        
        # Create new verification token
        token = str(uuid.uuid4())
        expires_at = timezone.now() + timedelta(days=1)
        EmailVerification.objects.create(user=user, token=token, expires_at=expires_at)
        
        # Send verification email
        verification_url = f"{settings.FRONTEND_URL}/verify-email/{token}"
        send_mail(
            'Verify your email address',
            f'Please click the link to verify your email: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return Response(
            {"message": "Verification email sent. Please check your inbox."},
            status=status.HTTP_200_OK
        )
