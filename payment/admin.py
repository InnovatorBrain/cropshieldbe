from django.contrib import admin
from .models import Payment, PaymentMethod

class UserFilteredAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(user=request.user)

@admin.register(Payment)
class PaymentAdmin(UserFilteredAdmin):
    list_display = ('id', 'user', 'policy_application', 'amount', 'payment_date', 'payment_method', 'transaction_id', 'status')
    search_fields = ('user__username', 'policy_application__id', 'transaction_id')
    list_filter = ('status', 'payment_date')
    ordering = ('-payment_date',)

@admin.register(PaymentMethod)
class PaymentMethodAdmin(UserFilteredAdmin):
    list_display = ('id', 'user', 'method_type', 'card_holder_name', 'expiry_month', 'expiry_year')
    search_fields = ('user__username', 'card_holder_name', 'method_type')
    list_filter = ('method_type',)
    ordering = ('user',)
