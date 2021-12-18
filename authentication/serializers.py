from rest_framework import serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError('The username only contains alpha newmeric character')

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(min_length=4, max_length=255, write_only=True)
    username = serializers.CharField(min_length=4, max_length=255, read_only=True)
    tokens   = serializers.CharField(min_length=4, max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')

        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials')
        if not user.is_verified:
            raise AuthenticationFailed('Email not verified yet')
        if not user.is_active:
            raise AuthenticationFailed('Account not activated yet')

        return {
            'email': user.email,
            'username': user.username,
            'tokens': user.tokens()
        }
        # return super(LoginSerializer, self).validate(attrs)