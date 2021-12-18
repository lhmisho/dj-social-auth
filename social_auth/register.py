from django.contrib.auth import authenticate
from authentication.models import User
from django.conf import settings
import os, random
from rest_framework.exceptions import AuthenticationFailed


def register_social_auth(provider, user_id, email, name):
    filter_user_by_email = User.objects.filter(email=email)

    if filter_user_by_email.exists():
        if provider == filter_user_by_email[0].auth_provider:
            registered_user = authenticate(email=email, password=settings.SOCIAL_SECRET)
            return {
                'username': registered_user.username,
                'email': registered_user.email,
                'tokens': registered_user.tokens()
            }
        else:
            raise AuthenticationFailed(detail='Please continue using login' + filter_user_by_email[0].auth_provider)
    else:
        user = {
            'username': name + 'abc',
            'email': email,
            'password': settings.SOCIAL_SECRET
        }
        user = User.objects.create_user(**user)
        user.is_verified = True
        user.save()

        new_user = authenticate(email=email, password=settings.SOCIAL_SECRET)
        return {
            'email': new_user.email,
            'username': new_user.username,
            'tokens': new_user.tokens()
        }
