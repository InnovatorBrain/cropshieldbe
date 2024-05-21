from rest_framework import serializers
from .models import ClaimApplication
from insurance.models import PolicyApplication

class ClaimApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimApplication
        fields = ['user','selectPolicy','selectedPolicy', 'farmerName', 'countryCode', 'phoneNumber', 'email', 'createdAt',
                  'typeOfDamage', 'dateOfDamage', 'extentOfDamage', 'witnessName',
                  'witnessCNIC', 'countryCode', 'witnessPhoneNumber', 'damageDescription',
                  'claimPicture1', 'claimPicture2', 'claimPicture3', 'claimPicture4','status']

    def get_user_policies(self, obj):
        user = self.context['request'].user
        policies = PolicyApplication.objects.filter(user=user)
        return [{'display_id': policy.display_id, 'selectPolicy': policy.selectPolicy} for policy in policies]

    # def validate(self, data):
    #     # Retrieve the associated policy from the data
    #     selectPolicy = data.get('selectPolicy')

    #     # Check if the associated policy is approved
    #     if selectPolicy and selectPolicy.status != 'APPROVED':
    #         raise serializers.ValidationError("Cannot submit claim. Policy is either not enrolled or not approved.")

    #     return data
