from accounts.serializers import UserSerializer
from rest_framework import serializers

from .models import Game


class NumbersSerializer(serializers.Serializer):

    numbers = serializers.IntegerField(min_value=6, max_value=10)


class GameSerializer(serializers.ModelSerializer):

    class Meta:

        model = Game
        fields = '__all__'

    numbers = serializers.ListField(
        child=serializers.IntegerField())
    user = UserSerializer()
