from django.db import models
from django.core.exceptions import ObjectDoesNotExist


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AdminReply(models.Model):
    message = models.ForeignKey(
        ContactMessage, related_name="replies", on_delete=models.CASCADE, default=1
    )
    reply_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        try:
            return f"Reply to: {self.message.name} ({self.message.email})"
        except ObjectDoesNotExist:
            return "Reply to: Unknown"
