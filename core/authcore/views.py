from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView 

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        if user.is_superuser:
            token['superadmin'] = True
        if user.role == 'admin':
            token['role'] = 'admin'
        if user.role == 'staff':
            token['role']= 'staff'
        if user.role == 'user':
            token['role'] = 'user'

        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class =  MyTokenObtainPairSerializer

class TestHomeView(APIView):
    def get(self,request):
        return Response({"message":"Hello"})