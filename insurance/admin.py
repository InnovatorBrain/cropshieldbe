from django.contrib import admin
from .models import PolicyApplication
from .models import PolicyPremiumDeductible

@admin.register(PolicyApplication)
class PolicyApplicationAdmin(admin.ModelAdmin):
    list_display = ["farmerName", "createdAt", "cnic", "status"]  # Include "status" in the list_display
    list_filter = ["status"]
    search_fields = ["farmerName", "email"]

    def get_search_results(self, request, queryset, search_term):
        """
        Override the default search behavior to search both farmerName and emailAddress fields.
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        queryset |= self.model.objects.filter(email__icontains=search_term)
        return queryset, use_distinct

    def get_readonly_fields(self, request, obj=None):
        """
        Make certain fields readonly based on the status of the policy application.
        """
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj and obj.status == 'APPROVED':
            readonly_fields += ('farmerName', 'cnic', 'countryCode', 'phoneNumber', 'email', 
                                'address', 'passportPicture1', 'cnicPicture1', 'cnicPicture2', 
                                'domicilePicture', 'farmAddress', 'cropsInsured', 'otherCrop', 
                                'acreagePlanted', 'cropVariety', 'plantingDate', 'selectPolicy', 
                                'coverageAmount', 'startDate', 'riskFactor', 
                                'additionalComments', 'paymentMethod', 'cardNumber', 
                                'cardHolderName', 'expiryDate', 'cvc')
        return readonly_fields


@admin.register(PolicyPremiumDeductible)
class PolicyPremiumDeductibleAdmin(admin.ModelAdmin):
    list_display = ["selectPolicy", "premium", "deductible"]  # Display selectPolicy, premium, and deductible in the admin list view
    search_fields = ["selectPolicy"]  # Enable searching by selectPolicy field

    def get_readonly_fields(self, request, obj=None):
        """
        Make selectPolicy readonly as it should not be changed.
        """
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj:
            readonly_fields += ('selectPolicy',)
        return readonly_fields