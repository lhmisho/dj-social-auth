from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from .serializers import GoogleSocialuthSerializer


class GoogleSocialAuthView(GenericAPIView):
    serializer_class = GoogleSocialuthSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response(data.get('auth_token'), status=status.HTTP_200_OK)