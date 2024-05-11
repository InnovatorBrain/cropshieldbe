from rest_framework import serializers
from .models import PolicyApplication

class PolicyApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyApplication
        fields = ['farmerName', 'createdAt', 'dateOfBirth', 'gender', 'cnic', 'countryCode', 'phoneNumber',
                  'email', 'address', 'passportPicture1', 'cnicPicture1', 'cnicPicture2', 'domicilePicture',
                  'farmAddress', 'cropsInsured', 'otherCrop', 'acreagePlanted', 'cropVariety', 'plantingDate',
                  'selectPolicy', 'coverageAmount', 'startDate', 'riskFactor', 'additionalComments',
                  'paymentMethod', 'cardNumber', 'cardHolderName', 'expiryDate', 'cvc', 'status']
