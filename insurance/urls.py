from django.urls import path
from .views import PolicyApplicationCreate, PolicyApplicationDetail, PolicyPremiumDeductibleAdmin, PolicyPremiumDeductibleUser

urlpatterns = [
    path("apply-policy/", PolicyApplicationCreate.as_view(), name="policy_application_create"),
    path('insurance/policy-application/<int:pk>/', PolicyApplicationDetail.as_view(), name='policy-application-detail'),
    path('admin/policy-premium-deductible/', PolicyPremiumDeductibleAdmin.as_view(), name='policy-premium-deductible-admin'),
    path('policy-premium-deductible/', PolicyPremiumDeductibleUser.as_view(), name='policy-premium-deductible-user'),
]
