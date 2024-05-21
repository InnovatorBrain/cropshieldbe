from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import PolicyApplication, PolicyPremiumDeductible
from .serializers import PolicyApplicationSerializer, UserPolicySerializer
from rest_framework import generics
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.http import JsonResponse
import stripe
from django.conf import settings
stripe.api_key = settings.STRIPE_SECRET_KEY

class PolicyApplicationCreate(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Merge the request data with the authenticated user
        data = request.data.copy()
        data['user'] = request.user  # Assign the authenticated user's id to the 'user' field

        serializer = PolicyApplicationSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PolicyApplicationDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PolicyApplicationSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return PolicyApplication.objects.filter(user=self.request.user)
        else:
            return PolicyApplication.objects.none()



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
        

# Manage Policy
class ManagePolicyApplicationsAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PolicyApplicationSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return PolicyApplication.objects.filter(user=self.request.user)
        else:
            return PolicyApplication.objects.none()
        

class PolicyPaymentCountView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, policy_id):
        user = request.user
        try:
            policy_application = PolicyApplication.objects.get(id=policy_id, user=user)
            payment_count = policy_application.payments.count()
            return Response({'paymentMade': payment_count}, status=status.HTTP_200_OK)
        except PolicyApplication.DoesNotExist:
            return Response({'error': 'Policy application not found'}, status=status.HTTP_404_NOT_FOUND)

def payment_count(request, policy_id):
    try:
        policy_application = PolicyApplication.objects.get(id=policy_id)
        payment_count = policy_application.count_payments()
        return JsonResponse({'payment_count': payment_count})
    except PolicyApplication.DoesNotExist:
        return JsonResponse({'error': 'PolicyApplication not found'}, status=404)
    

    

class UserPoliciesView(generics.ListAPIView):
    serializer_class = UserPolicySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return PolicyApplication.objects.filter(user=user)