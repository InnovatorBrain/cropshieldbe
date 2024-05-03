from django.contrib import admin
from .models import PolicyApplication


@admin.register(PolicyApplication)
class PolicyApplicationAdmin(admin.ModelAdmin):
    list_display = ["farmerName", "createdAt", "cnic"]
    list_filter = ["status"]
    search_fields = ["farmerName", "emailAddress"]
