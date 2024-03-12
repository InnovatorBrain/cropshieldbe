from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage, AdminReply
from .filters import ContactMessageFilter


class AdminReplyInline(admin.TabularInline):
    model = AdminReply
    extra = 0
    fields = ["reply_content"]
    list_display = ["get_message_name", "reply_content", "get_user_message", "timestamp"]

    def get_formset(self, request, obj=None, **kwargs):
        """
        Override get_formset to prepopulate reply_content field.
        """
        formset = super().get_formset(request, obj, **kwargs)
        if obj:
            formset.form.base_fields["reply_content"].initial = "Default reply message"
        return formset
    
    def get_user_message(self, obj):
        return obj.message.message
    get_user_message.short_description = "User Message"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    actions = ["message"]
    list_display = ["name", "email", "message", "timestamp"]
    list_per_page = 10
    search_fields = ["name", "email", "message"]
    readonly_fields = ["name", "email", "message", "timestamp"]
    list_filter = [ContactMessageFilter]
    inlines = [AdminReplyInline]

    def adminmessage(self, request, queryset):
        pass

    adminmessage.short_description = "Admin Message"


@admin.register(AdminReply)
class AdminReplyAdmin(admin.ModelAdmin):
    list_display = ["get_message_name", "reply_content", "get_user_message", "timestamp"]
    search_fields = ["message__name", "message__email", "reply_content"]

    def get_message_name(self, obj):
        return obj.message.name

    def get_user_message(self, obj):
        return obj.message.message
    get_user_message.short_description = "User Message"

    get_message_name.short_description = "Message Name"

    readonly_fields = ["get_message_name", "reply_content", "timestamp"]

    def save_model(self, request, obj, form, change):
        """
        Override save_model to send an email to the user's specific email address.
        """
        super().save_model(request, obj, form, change)
        subject = "Your message has been replied"
        # message = f"Your message:\n{obj.message.message}\n\nAdmin's reply:\n{obj.reply_content}"
        message = f"""
Dear {obj.message.name},

We sincerely appreciate you reaching out to us.

Your Message:
{obj.message.message}

Admin's Reply:
{obj.reply_content}

If you have any further questions or concerns, please feel free to contact us again.

Warm regards,

Cropshields support
"""

        from_email = settings.EMAIL_HOST_USER
        recipient_list = [obj.message.email]
        try:
            send_mail(subject, message, from_email, recipient_list)
            self.message_user(request, "Email sent successfully.")
        except Exception as e:
            self.message_user(request, f"Error sending email: {e}", level="ERROR")
