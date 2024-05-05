from rest_framework import serializers
from .models import ClaimApplication

class ClaimApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClaimApplication
        fields = ['farmerName', 'countryCode', 'phoneNumber','email', 'createdAt', 
                  'typeOfDamage', 'dateOfDamage', 'extentOfDamage', 'witnessName', 
                  'witnessCNIC', 'countryCode', 'witnessPhoneNumber', 'damageDescription', 
                  'claimPicture1', 'claimPicture2', 'claimPicture3', 'claimPicture4']
