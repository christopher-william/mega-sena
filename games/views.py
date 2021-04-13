import random

from rest_framework import status, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Game
from .serializers import GameSerializer, NumbersSerializer


class GameViewSets(viewsets.ViewSet):
    queryset = Game.objects.all()
    serializer = GameSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # def generete_random_numbers(self, length):
    #     return random.choices([i for i in range(61)], k=length)

    def generete_random_numbers(self, length):

        mega_sena_numbers = []

        while len(mega_sena_numbers) < length:
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

        except ImportError:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['GET'])
    def result(self, request, pk=None):

        try:

            game = Game.objects.get(id=pk, user=request.user)

            # pegar o resultado com webscrapping
            winner_numbers = [1, 2, 3, 4, 5, 6]

            response_data = {
                "winning_numbers": winner_numbers,
                "game_numbers": game.numbers,
                "matching_numbers": set(game.numbers).intersection(
                    set(winner_numbers))
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except ImportError:
            return Response(status=status.HTTP_404_NOT_FOUND)
