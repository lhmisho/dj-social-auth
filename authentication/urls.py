from django.urls import path
from .views import UserRegisterView, VerifyEmail


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmail.as_view(), name='email-verify'),
]