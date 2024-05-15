from rest_framework import serializers
from .models import ClaimApplication

class ClaimApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimApplication
        fields = ['selectPolicy','farmerName', 'countryCode', 'phoneNumber', 'email', 'createdAt',
                  'typeOfDamage', 'dateOfDamage', 'extentOfDamage', 'witnessName',
                  'witnessCNIC', 'countryCode', 'witnessPhoneNumber', 'damageDescription',
                  'claimPicture1', 'claimPicture2', 'claimPicture3', 'claimPicture4','status']

    def validate(self, data):
        # Retrieve the associated policy from the data
        selectPolicy = data.get('selectPolicy')

        # Check if the associated policy is approved
        if selectPolicy and selectPolicy.status != 'APPROVED':
            raise serializers.ValidationError("Cannot submit claim. Policy is either not enrolled or not approved.")

        return data
