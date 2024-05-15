from django.urls import path
from .views import ClaimApplicationCreate, ClaimApplicationDetail, ManageClaimApplicationsAPIView

urlpatterns = [
    path("apply-claim/", ClaimApplicationCreate.as_view(), name="Claim_application_create"),
    path('claim/claim-application/<int:pk>/', ClaimApplicationDetail.as_view(), name='claim-application-detail'),
    path('manage-claims/', ManageClaimApplicationsAPIView.as_view(), name='manage-claim-api'),
]
