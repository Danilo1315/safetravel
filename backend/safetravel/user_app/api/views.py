from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from user_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
# from user_app import models
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib import auth

# Create your views here.

@api_view(['POST',])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
    

@api_view(['POST',])
def registration_view(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            data['response'] = 'El registro del usuario fue exitoso'
            data['username'] = account.username
            data['email'] = account.email
            data['name'] = account.name
            # token = Token.objects.get(user=account).key
            # data['token'] = token
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
        else:
            data = serializer.errors
            
        return Response(data)
    

@api_view(['POST',])
def login_view(request):
    data = {}
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')
        print(email)
        account = auth.authenticate(email=email, password=password)
        print("Account: " + str(account))
        if account is not None:
            data['status'] = status.HTTP_200_OK
            data['username'] = account.username
            data['email'] = account.email
            data['name'] = account.name
            refresh = RefreshToken.for_user(account)
            data['token'] = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return Response(data)
        else:
            data['error'] = "Credenciales incorrectas!"
            data['status'] = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(data)