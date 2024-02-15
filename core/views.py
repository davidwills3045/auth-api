from django.shortcuts import get_object_or_404,render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import Userserializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth import logout
from django.shortcuts import redirect

@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])
    if not user.check_password(request.data['password']):
        return Response({"detail":"Not found."}, status=status.HTTP_400_BAD_REQUEST)
    token, created = Token.objects.get_or_create(user=user)
    serializer =Userserializer(instance=user)
    return Response({"token":token.key, "user": serializer.data})
@api_view(['POST'])
def signup(request):
    serializer = Userserializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # retrieving the saved user
        user = User.objects.get(username=request.data['username'])
        user.set_password(request.data['password'])
        user.save()
        token = Token.objects.create(user=user)
        return Response({"token":token.key, "user": serializer.data})
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import authentication_classes,permission_classes
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([SessionAuthentication,TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):

    return Response("passed for {}".format(request.user.email))

@api_view(['GET'])
def logout(request):
    logout(request)
    return redirect("login")
