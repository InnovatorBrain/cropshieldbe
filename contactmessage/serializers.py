from rest_framework import serializers
from .models import ContactMessage, AdminReply

class AdminReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminReply
        fields = '__all__'

class ContactMessageSerializer(serializers.ModelSerializer):
    replies = AdminReplySerializer(many=True, read_only=True)

    class Meta:
        model = ContactMessage
        fields = '__all__'