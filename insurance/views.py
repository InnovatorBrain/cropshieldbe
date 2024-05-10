from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import PolicyApplication
from .serializers import PolicyApplicationSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from .models import PolicyPremiumDeductible

class PolicyApplicationCreate(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        serializer = PolicyApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PolicyApplicationDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = PolicyApplication.objects.all()
    serializer_class = PolicyApplicationSerializer



class PolicyPremiumDeductibleAdmin(APIView):
    def post(self, request, format=None):
        data = request.data
        select_policy = data.get('selectPolicy', None)
        premium = data.get('premium', None)
        deductible = data.get('deductible', None)

        if select_policy is None or premium is None or deductible is None:
            return Response({"error": "selectPolicy, premium, and deductible are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Check if policy type already exists
        existing_policy = PolicyPremiumDeductible.objects.filter(selectPolicy=select_policy).first()
        if existing_policy:
            existing_policy.premium = premium
            existing_policy.deductible = deductible
            existing_policy.save()
            return Response({"message": "Premium and deductible values updated successfully"}, status=status.HTTP_200_OK)
        else:
            PolicyPremiumDeductible.objects.create(selectPolicy=select_policy, premium=premium, deductible=deductible)
            return Response({"message": "Premium and deductible values set successfully"}, status=status.HTTP_201_CREATED)
        
class PolicyPremiumDeductibleUser(APIView):
    queryset = PolicyPremiumDeductible.objects.all() 
    def get(self, request, format=None):
        select_policy = request.query_params.get('selectPolicy', None)

        if select_policy is None:
            return Response({"error": "selectPolicy parameter is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            policy_values = PolicyPremiumDeductible.objects.get(selectPolicy=select_policy)
            return Response({"premium": policy_values.premium, "deductible": policy_values.deductible}, status=status.HTTP_200_OK)
        except PolicyPremiumDeductible.DoesNotExist:
            return Response({"error": "Policy type not found"}, status=status.HTTP_404_NOT_FOUND)