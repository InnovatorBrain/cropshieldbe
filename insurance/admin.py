from django.contrib import admin
from .models import PolicyApplication
from .models import PolicyPremiumDeductible
from django.utils.html import format_html


@admin.register(PolicyApplication)
class PolicyApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "display_id",
        "farmerName",
        "createdAt",
        "cnic",
        "status",
        "passport_picture",
        "cnic_picture1",
        "cnic_picture2",
        "domicile_picture",
    ]
    list_filter = ["status"]
    search_fields = ["farmerName", "email", "status"]
    list_per_page = 10
    list_editable = ["status"]
    actions = ["clear_status"]
    ordering = ["id", "farmerName", "createdAt", "cnic", "status"]
    filter_horizontal = []

    def passport_picture(self, obj):
        if obj.passportPicture1:
            return format_html(
                '<a href="{0}"><img src="{0}" width="40" height="40" /></a>',
                obj.passportPicture1.url,
            )
        return None

    passport_picture.short_description = "Passport Picture"

    def cnic_picture1(self, obj):
        if obj.cnicPicture1:
            return format_html(
                '<a href="{0}"><img src="{0}" width="40" height="40" /></a>',
                obj.cnicPicture1.url,
            )
        return None

    cnic_picture1.short_description = "CNIC Picture 1"

    def cnic_picture2(self, obj):
        if obj.cnicPicture2:
            return format_html(
                '<a href="{0}"><img src="{0}" width="40" height="40" /></a>',
                obj.cnicPicture2.url,
            )
        return None

    cnic_picture2.short_description = "CNIC Picture 2"

    def domicile_picture(self, obj):
        if obj.domicilePicture:
            return format_html(
                '<a href="{0}"><img src="{0}" width="40" height="40" /></a>',
                obj.domicilePicture.url,
            )
        return None

    domicile_picture.short_description = "Domicile Picture"

    @admin.action(description="Clear Status")
    def clear_status(self, request, queryset):
        updated_count = queryset.update(status="PENDING")
        self.message_user(
            request, f"{updated_count} policy applications were successfully updated."
        )

    def get_search_results(self, request, queryset, search_term):
        """
        Override the default search behavior to search both farmerName and emailAddress fields.
        """
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        queryset |= self.model.objects.filter(email__icontains=search_term)
        return queryset, use_distinct

    def get_readonly_fields(self, request, obj=None):
        """
        Make certain fields readonly based on the status of the policy application.
        """
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj and obj.status == "APPROVED":
            readonly_fields += (
                "display_id",
                "farmerName",
                "cnic",
                "countryCode",
                "phoneNumber",
                "email",
                "address",
                "passportPicture1",
                "cnicPicture1",
                "cnicPicture2",
                "domicilePicture",
                "farmAddress",
                "cropsInsured",
                "otherCrop",
                "acreagePlanted",
                "cropVariety",
                "plantingDate",
                "selectPolicy",
                "coverageAmount",
                "startDate",
                "riskFactor",
                "additionalComments",
                "paymentMethod",
                "cardNumber",
                "cardHolderName",
                "expiryDate",
                "cvc",
                "status",
            )
        return readonly_fields


@admin.register(PolicyPremiumDeductible)
class PolicyPremiumDeductibleAdmin(admin.ModelAdmin):
    list_display = [
        "selectPolicy",
        "premium",
        "deductible",
    ]
    search_fields = ["selectPolicy"]

    def get_readonly_fields(self, request, obj=None):
        """
        Make selectPolicy readonly as it should not be changed.
        """
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj:
            readonly_fields += ("selectPolicy",)
        return readonly_fields
