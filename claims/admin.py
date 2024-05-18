from django.contrib import admin
from .models import ClaimApplication
from django.utils.html import format_html


@admin.register(ClaimApplication)
class ClaimApplicationAdmin(admin.ModelAdmin):
    list_display = [
        "farmerName",
        "selectPolicy",
        "user",
        "createdAt",
        "dateOfDamage",
        "status",
        "claimPicture1_display",
        "claimPicture2_display",
        "claimPicture3_display",
        "claimPicture4_display",
    ]
    list_filter = ["status"]
    search_fields = [
        "farmerName",
        "email",
        "typeOfDamage",
        "dateOfDamage",
        "user__username",
    ]
    list_per_page = 10
    list_editable = ["status"]
    actions = ["clear_status"]
    filter_horizontal = []

    def claimPicture1_display(self, obj):
        if obj.claimPicture1:
            return format_html(
                '<a href="{0}"><img src="{0}" width="40" height="40" /></a>',
                obj.claimPicture1.url,
            )
        return None

    claimPicture1_display.short_description = "Claim Picture 1"

    def claimPicture2_display(self, obj):
        if obj.claimPicture2:
            return format_html(
                '<a href="{0}"><img src="{0}" width="40" height="40" /></a>',
                obj.claimPicture2.url,
            )
        return None

    claimPicture2_display.short_description = "Claim Picture 2"

    def claimPicture3_display(self, obj):
        if obj.claimPicture3:
            return format_html(
                '<a href="{0}"><img src="{0}" width="40" height="40" /></a>',
                obj.claimPicture3.url,
            )
        return None

    claimPicture3_display.short_description = "Claim Picture 3"

    def claimPicture4_display(self, obj):
        if obj.claimPicture4:
            return format_html(
                '<a href="{0}"><img src="{0}" width="40" height="40" /></a>',
                obj.claimPicture4.url,
            )
        return None

    claimPicture4_display.short_description = "Claim Picture 4"


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
        queryset, use_distinct = super().get_search_results(
            request, queryset, search_term
        )
        queryset |= self.model.objects.filter(email__icontains=search_term)
        queryset |= self.model.objects.filter(user__username__icontains=search_term)
        return queryset, use_distinct

    def get_readonly_fields(self, request, obj=None):
        """
        Make certain fields readonly based on the status of the policy application.
        """
        readonly_fields = super().get_readonly_fields(request, obj=obj)
        if obj and obj.status == "APPROVED":
            readonly_fields += (
                "farmerName",
                "countryCode",
                "phoneNumber",
                "email",
                "createdAt",
                "typeOfDamage",
                "dateOfDamage",
                "extentOfDamage",
                "witnessName",
                "witnessCNIC",
                "countryCode",
                "witnessPhoneNumber",
                "damageDescription",
                "claimPicture1",
                "claimPicture2",
                "claimPicture3",
                "claimPicture4",
                "user",
            )
        return readonly_fields
