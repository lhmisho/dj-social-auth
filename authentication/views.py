from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
import jwt
from .serializers import UserSerializer, LoginSerializer
from .models import User
from .utils import Util

class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = User.objects.get(email=serializer.data.get('email'))
        token = RefreshToken.for_user(user).access_token

        relativeLink = reverse('email-verify')
        current_site = get_current_site(request)

        absurl = 'http://' + current_site.domain + relativeLink+"?token="+str(token)
        email_body = 'Hi, ' + user.username + ' Use this link to verify your account' + absurl
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'Verify your account'}
        Util.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VerifyEmail(generics.GenericAPIView):

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({'success': 'User successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as e:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)