import random

from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from webscraper import webscraper_mega_sena_number

from .models import Game
from .serializers import GameSerializer, NumbersSerializer


class GameViewSets(viewsets.ViewSet):
    queryset = Game.objects.all()
    serializer = GameSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def generete_random_numbers(self, length):

        mega_sena_numbers = []

        while len(mega_sena_numbers) < int(length):
            new_number = random.randrange(6, 61)

            if not new_number in mega_sena_numbers:
                mega_sena_numbers.append(new_number)

        return mega_sena_numbers

    def create(self, request):

        serializer = NumbersSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        game = Game.objects.create(
            numbers=self.generete_random_numbers(
                length=request.data['numbers']),
            user=request.user
        )

        serializer = GameSerializer(game)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):

        game_list = Game.objects.filter(user=request.user)

        if not len(game_list):
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = GameSerializer(game_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):

        try:

            game = Game.objects.get(id=pk, user=request.user)
            serializer = GameSerializer(game)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['GET'])
    def result(self, request, pk=None):

        try:

            game = Game.objects.get(id=pk, user=request.user)

            winner_numbers = webscraper_mega_sena_number()

            response_data = {
                "winning_numbers": winner_numbers,
                "game_numbers": game.numbers,
                "matching_numbers": set(game.numbers).intersection(
                    set(winner_numbers))
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'])
    def megasena(self, request):
        try:
            return Response(webscraper_mega_sena_number(), status=status.HTTP_200_OK)

        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)
