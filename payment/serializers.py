# serializers.py
from rest_framework import serializers
from .models import Payment, PaymentMethod
from insurance.models import PolicyApplication

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'policy_application', 'amount', 'payment_date', 'payment_method', 'transaction_id', 'status']

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ['id', 'user', 'method_type', 'card_number', 'card_holder_name', 'expiry_month', 'expiry_year', 'cvc', 'is_default']

    def create(self, validated_data):
        if validated_data.get('is_default'):
            PaymentMethod.objects.filter(user=validated_data['user'], is_default=True).update(is_default=False)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('is_default'):
            PaymentMethod.objects.filter(user=instance.user, is_default=True).update(is_default=False)
        return super().update(instance, validated_data)

class CreatePaymentIntentSerializer(serializers.Serializer):
    policy_application_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_policy_application_id(self, value):
        if not PolicyApplication.objects.filter(id=value).exists():
            raise serializers.ValidationError("Invalid policy application ID")
        return value