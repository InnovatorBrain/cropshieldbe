from django.urls import path
from .views import PolicyApplicationCreate, PolicyApplicationDetail, PolicyPremiumDeductibleAdmin, PolicyPremiumDeductibleUser, ManagePolicyApplicationsAPIView, PolicyPaymentCountView, UserPoliciesView
from . import views

urlpatterns = [
    path("apply-policy/", PolicyApplicationCreate.as_view(), name="policy_application_create"),
    path('insurance/policy-application/<int:pk>/', PolicyApplicationDetail.as_view(), name='policy-application-detail'),
    path('admin/policy-premium-deductible/', PolicyPremiumDeductibleAdmin.as_view(), name='policy-premium-deductible-admin'),
    path('policy-premium-deductible/', PolicyPremiumDeductibleUser.as_view(), name='policy-premium-deductible-user'),
    path('manage-policies/', ManagePolicyApplicationsAPIView.as_view(), name='manage-policies-api'),
    path('policies/<int:policy_id>/payment-count/', PolicyPaymentCountView.as_view(), name='policy-payment-count'),
    path('insurance/policies/&lt;int:policy_id&gt;/payment-count/', views.payment_count, name='payment-count'),
    path('user-policies/', UserPoliciesView.as_view(), name='user-policies'),


]
