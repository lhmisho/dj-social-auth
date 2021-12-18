from django.urls import path
from .views import UserRegisterView, VerifyEmail, LoginApiView
from social_auth.views import GoogleSocialAuthView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('verify-email/', VerifyEmail.as_view(), name='email-verify'),
    path('login/', LoginApiView.as_view(), name='login'),
    path('login/google/', GoogleSocialAuthView.as_view(), name='google-login'),
]