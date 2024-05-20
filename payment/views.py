from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment, PaymentMethod
from .serializers import PaymentSerializer, PaymentMethodSerializer
import stripe
from django.conf import settings
from .serializers import CreatePaymentIntentSerializer
from rest_framework.views import APIView
from insurance.models import PolicyApplication

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentMethodViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer

    def get_queryset(self):
        return PaymentMethod.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        user = request.user
        data["user"] = user.id

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            if serializer.validated_data.get("is_default"):
                PaymentMethod.objects.filter(user=user, is_default=True).update(
                    is_default=False
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        user = request.user
        data["user"] = user.id

        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            if serializer.validated_data.get("is_default"):
                PaymentMethod.objects.filter(user=user, is_default=True).update(
                    is_default=False
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreatePaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreatePaymentIntentSerializer(data=request.data)
        if serializer.is_valid():
            policy_application = PolicyApplication.objects.get(
                id=serializer.validated_data["policy_application_id"]
            )
            amount = serializer.validated_data["amount"]

            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  
                currency="usd",
                metadata={"policy_application_id": policy_application.id},
            )

            policy_application.stripe_payment_intent_id = intent.id
            policy_application.save()

            return Response(
                {"client_secret": intent.client_secret}, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
