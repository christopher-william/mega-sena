from rest_framework import serializers


class UserSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    is_superuser = serializers.BooleanField()
    is_staff = serializers.BooleanField()


class UserLoginSerializer(serializers.Serializer):

    username = serializers.CharField()
    password = serializers.CharField()
