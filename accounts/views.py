import ipdb
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserLoginSerializer, UserSerializer


class AccountsViewSets(viewsets.ViewSet):
    authentication_classes = [TokenAuthentication]
    queryset = User.objects.all()
    serializer = UserSerializer

    @action(detail=False, methods=['POST'])
    def register(self, request):

        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:

            user = User.objects.create_user(
                password=request.data['password'],
                username=request.data['username'],
                is_staff=request.data['is_staff'],
                is_superuser=request.data['is_superuser'],
            )

        except IntegrityError:
            return Response({"username": 'this field already exists'}, status=status.HTTP_409_CONFLICT)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def login(self, request):

        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=request.data['username'],
            password=request.data['password'],
        )

        if user and user.is_active:

            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)

        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['PUT'])
    def edit(self, request):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        request.user.username = request.data['username']
        request.user.set_password(request.data['password'])

        if request.user.is_staff and request.data.get(['is_staff']):
            request.user.is_staff = request.data['is_staff']

        if request.user.is_superuser and request.data.get(['is_superuser']):
            request.user.is_superuser = request.data['is_superuser']

        if request.user.is_superuser or request.user.is_staff and request.data.get(['is_active']):
            request.user.is_active = request.data['is_active']

        request.user.save()

        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['DELETE'])
    def delete(self, request):

        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        try:

            request.user.is_active = False
            request.user.save()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
