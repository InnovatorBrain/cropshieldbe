from django.contrib import admin
from .models import ClaimApplication

@admin.register(ClaimApplication)
class ClaimApplicationAdmin(admin.ModelAdmin):
    list_display = ["farmerName", "selectPolicy", "user", "createdAt", "email", "dateOfDamage", "status"]
    list_filter = ["status"]
    search_fields = ["farmerName", "email", "typeOfDamage", "dateOfDamage", "user__username"]
    list_per_page = 10
    list_editable = ["status"]
    actions = ["clear_status"]
    filter_horizontal = []

    
    @admin.action(description="Clear Claims Status")
    def clear_status(self, request, queryset):
        updated_count = queryset.update(status="PENDING")
        self.message_user(
            request, f"{updated_count} policy applications were successfully updated."
        )

    def get_search_results(self, request, queryset, search_term):
        """
        Override the default search behavior to search both farmerName, emailAddress, and username fields.
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset |= self.model.objects.filter(email__icontains=search_term)
        queryset |= self.model.objects.filter(user__username__icontains=search_term)
        return queryset, use_distinct

    def get_readonly_fields(self, request, obj=None):
        """
        Make certain fields readonly based on the status of the policy application.
        """
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj and obj.status == 'APPROVED':
            readonly_fields += ('farmerName', 'countryCode', 'phoneNumber', 'email', 'createdAt', 
                                'typeOfDamage', 'dateOfDamage', 'extentOfDamage', 'witnessName', 
                                'witnessCNIC', 'countryCode', 'witnessPhoneNumber', 'damageDescription', 
                                'claimPicture1', 'claimPicture2', 'claimPicture3', 'claimPicture4', 'user')
        return readonly_fields
