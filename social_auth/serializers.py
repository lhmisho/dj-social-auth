from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
from .register import register_social_auth
from . import google


class GoogleSocialuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data['sub']
        except:
            raise serializers.ValidationError('The token is invalid or expired. Please login again')

        if user_data['aud'] != settings.GOOGLE_CLIENT_ID:
            raise AuthenticationFailed('OPS! who are your')

        user_id = user_data['sub']
        email = user_data['email']
        name = user_data['name']
        provider = 'google'

        return register_social_auth(provider, user_id, email, name)
