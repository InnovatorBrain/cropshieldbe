from rest_framework import generics
from .models import ContactMessage, AdminReply
from .serializers import ContactMessageSerializer, AdminReplySerializer
from rest_framework.permissions import AllowAny


class ContactMessageListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [AllowAny]
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer


class AdminReplyCreateAPIView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = AdminReply.objects.all()
    serializer_class = AdminReplySerializer
