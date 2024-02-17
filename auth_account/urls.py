from django.urls import path
from .views import UserSignupView, UserLoginView, CustomPasswordResetView, UserProfileView
from django.contrib.auth.views import PasswordResetConfirmView

urlpatterns = [
    path("signup/", UserSignupView.as_view(), name="user_signup"),
    path("login/", UserLoginView.as_view(), name="user_login"),
    path('password_reset/', CustomPasswordResetView.as_view(), name='custom_password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('profile/', UserProfileView.as_view(), name='profile')
]
