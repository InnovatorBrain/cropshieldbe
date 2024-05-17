from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, ProfilePicture

class CustomUserAdmin(BaseUserAdmin):
    list_display = ["id", "email", "first_name", "last_name", "is_admin", "get_policy_count", "get_claim_count", "payment_info"]
    list_filter = ["is_admin"]
    list_editable = ["is_admin"]
    list_per_page = 10
    fieldsets = [
        ("CropShield User's Credentials", {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["first_name", "last_name"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": [
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ],
            },
        ),
    ]
    search_fields = ["first_name__startswith", "last_name__startswith", "email"]
    ordering = ["id", "first_name", "last_name"]
    filter_horizontal = []
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('policy_applications', 'claim_applications', 'payments', 'payment_methods')
        return queryset
    
    def get_policy_count(self, obj):
        policy_count = obj.policy_applications.count()
        url = reverse('admin:insurance_policyapplication_changelist') + f'?user__id={obj.id}'
        return format_html('<a href="{}">{}</a>', url, policy_count)
    
    get_policy_count.short_description = 'Policy Count'
    
    def get_claim_count(self, obj):
        claim_count = obj.claim_applications.count()
        url = reverse('admin:claims_claimapplication_changelist') + f'?user__id={obj.id}'
        return format_html('<a href="{}">{}</a>', url, claim_count)
    
    get_claim_count.short_description = 'Claim Count'
    
    def payment_info(self, obj):
        payment_method = obj.payment_methods.filter(is_default=True).first()
        if payment_method:
            return f'{payment_method.method_type} - {payment_method.card_holder_name}'
        return None

    payment_info.short_description = 'Payment Info'

class PolicyApplicationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "createdAt", "status"]
    search_fields = ["user__email"]
    list_filter = ["status"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user_id = request.GET.get('user__id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class ClaimApplicationAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "createdAt", "status"]
    search_fields = ["user__email"]
    list_filter = ["status"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user_id = request.GET.get('user__id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class PaymentAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "policy_application", "amount", "payment_date", "status"]
    search_fields = ["user__email", "policy_application__id"]
    list_filter = ["status"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user_id = request.GET.get('user__id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "method_type", "card_holder_name", "is_default"]
    search_fields = ["user__email"]
    list_filter = ["is_default"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        user_id = request.GET.get('user__id')
        if user_id:
            queryset = queryset.filter(user_id=user_id)
        return queryset

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(ProfilePicture)
admin.site.unregister(Group)
