from django.urls import path
from .views import PolicyApplicationCreate, PolicyApplicationDetail

urlpatterns = [
    path("apply-policy/", PolicyApplicationCreate.as_view(), name="policy_application_create"),
    path('insurance/policy-application/<int:pk>/', PolicyApplicationDetail.as_view(), name='policy-application-detail'),

]
