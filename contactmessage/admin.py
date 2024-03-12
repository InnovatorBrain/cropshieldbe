from django.contrib import admin
from .models import ContactMessage, AdminReply


class AdminReplyInline(admin.TabularInline):
    model = AdminReply
    extra = 0
    fields = ["reply_content"]

    def get_formset(self, request, obj=None, **kwargs):
        """
        Override get_formset to prepopulate reply_content field.
        """
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields["reply_content"].initial = (
                "Default reply message"
            )
        return formset


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "message", "timestamp"]
    search_fields = ["name", "email", "message"]
    inlines = [AdminReplyInline]
    readonly_fields = ["name", "email", "message", "timestamp"]

    def save_related(self, request, form, formsets, change):
        """
        Override save_related to prevent marking ContactMessage as changed when only AdminReply objects are added/modified.
        """
        super().save_related(request, form, formsets, change)
        if not change:
            form.instance._change_message = "Added."
            form.instance.save(update_fields=["_change_message"])


@admin.register(AdminReply)
class AdminReplyAdmin(admin.ModelAdmin):
    list_display = ["message", "reply_content", "timestamp"]
    search_fields = ["message__name", "message__email", "reply_content"]
    readonly_fields = ["message", "reply_content", "timestamp"]
