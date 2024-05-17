from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Payment, PaymentMethod
from .serializers import PaymentSerializer, PaymentMethodSerializer

class PaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
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
        data['user'] = user.id

        # Delete existing payment methods for the user
        PaymentMethod.objects.filter(user=user).delete()

        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        data = request.data.copy()
        user = request.user
        data['user'] = user.id

        # Delete existing payment methods for the user
        PaymentMethod.objects.filter(user=user).delete()

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
