from django.urls import path
from .views import (
    UserRegisterView,
    EmailVerificationView,
    UserProfileView,
    UserProfileUpdateView,
    ChangePasswordView,
    ResendVerificationEmailView
)

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/', EmailVerificationView.as_view(), name='verify-email'),
    path('resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/update/', UserProfileUpdateView.as_view(), name='profile-update'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
] 