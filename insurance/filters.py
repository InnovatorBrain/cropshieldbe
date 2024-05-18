import django_filters
from .models import PolicyApplication

class PolicyApplicationFilter(django_filters.FilterSet):
    class Meta:
        model = PolicyApplication
        fields = {
            'farmerName': ['icontains'],
            'cnic': ['exact'],
            'createdAt': ['date__gt', 'date__lt'],
            'cropsInsured': ['exact'],
            'status': ['exact'],
        }
