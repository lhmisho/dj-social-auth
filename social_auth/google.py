import requests
from google.auth.transport import Request
from google.oauth2 import id_token


class Google:

    @staticmethod
    def validate(auth_token):
        try:
            idinfo = id_token.verify_oauth2_token(auth_token, requests.Request())
            if 'accounts.google.com' in idinfo['iss']:
                return idinfo
        except Exception as e:
            return "The token is invalid or expired"
