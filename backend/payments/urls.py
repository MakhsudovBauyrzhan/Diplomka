from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, TransactionViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'transactions', TransactionViewSet, basename='transaction')

urlpatterns = [
    path('', include(router.urls)),
] 