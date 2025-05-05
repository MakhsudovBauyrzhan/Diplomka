from django.contrib import admin
from .models import Payment, Transaction


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'participation', 'amount', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('participation__user__email', 'participation__tour__title')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'transaction_type', 'description', 'timestamp')
    list_filter = ('transaction_type',)
    search_fields = ('user__email', 'description')
    readonly_fields = ('timestamp',)
