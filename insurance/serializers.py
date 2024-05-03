from rest_framework import serializers
from .models import PolicyApplication

class PolicyApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyApplication
        fields = '__all__'
