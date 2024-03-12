from django.urls import path
from .views import ContactMessageListCreateAPIView, AdminReplyCreateAPIView

urlpatterns = [
    path('', ContactMessageListCreateAPIView.as_view(), name='contact_message_list_create'),
    path('reply/', AdminReplyCreateAPIView.as_view(), name='admin_reply_create'),
]