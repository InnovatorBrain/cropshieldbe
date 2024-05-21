from rest_framework import serializers
from .models import PolicyApplication

class PolicyApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyApplication
        fields = ['display_id','farmerName', 'createdAt', 'dateOfBirth', 'gender', 'cnic', 'countryCode', 'phoneNumber',
                  'email', 'address', 'passportPicture1', 'cnicPicture1', 'cnicPicture2', 'domicilePicture',
                  'farmAddress', 'cropsInsured', 'otherCrop', 'acreagePlanted', 'cropVariety', 'plantingDate',
                  'selectPolicy', 'coverageAmount', 'startDate', 'riskFactor', 'additionalComments',
                  'paymentMethod', 'cardNumber', 'cardHolderName', 'expiryDate', 'cvc', 'status']

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if instance.user != user:
            raise serializers.ValidationError("You don't have permission to modify this instance.")
        return super().update(instance, validated_data)

class UserPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyApplication
        fields = ['display_id', 'farmerName', 'selectPolicy', 'status']
