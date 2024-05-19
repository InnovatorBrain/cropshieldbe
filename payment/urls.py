from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PaymentMethodViewSet, CreatePaymentIntentView

router = DefaultRouter()
router.register(r'payments', PaymentViewSet)
router.register(r'payment-methods', PaymentMethodViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create-payment-intent/', CreatePaymentIntentView.as_view(), name='create-payment-intent'),
]
