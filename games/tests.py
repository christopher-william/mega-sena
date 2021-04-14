from django.test import TestCase
from rest_framework.test import APIClient


class TestView(TestCase):

    def setUp(self):

        self.user_dict1 = {
            "username": "christopher",
            "password": "1234",
            "is_staff": False,
            "is_superuser": False
        }

        self.user_dict2 = {
            "username": "william",
            "password": "4321",
            "is_staff": False,
            "is_superuser": False
        }

    def test_create_games(self):
        """ Create a new game with random number """
        client = APIClient()

        # create a new user
        user = client.post('/api/accounts/register/', self.user_dict1)
        self.assertEqual(user.status_code, 201, user.data)

        # get token from user login
        token = client.post('/api/accounts/login/', self.user_dict1)
        self.assertEqual(token.status_code, 200, user.data)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.data['token'])

        # create a new game
        response = client.post("/api/games/", {"numbers": 6})

        self.assertEqual(response.status_code, 201, response.data)
        self.assertEqual(len(response.data['numbers']), 6)
        self.assertDictEqual(user.data, response.data['user'])

    def test_create_games_with_status_code_400(self):
        """ Create a new game with status code error -> 400"""
        client = APIClient()

        # create a new user
        user = client.post('/api/accounts/register/', self.user_dict1)
        self.assertEqual(user.status_code, 201, user.data)

        # get token from user login
        token = client.post('/api/accounts/login/', self.user_dict1)
        self.assertEqual(token.status_code, 200, user.data)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' + token.data['token'])

        # create a new game with numbers less than 6
        response = client.post("/api/games/", {"numbers": 5})
        self.assertEqual(response.status_code, 400)

        # create a new game with numbers greater than 10
        response = client.post("/api/games/", {"numbers": 11})
        self.assertEqual(response.status_code, 400)

        # create a new game with empty json
        response = client.post("/api/games/", {})
        self.assertEqual(response.status_code, 400)

        # create a new game with number instead of numbers
        response = client.post("/api/games/", {"number": 10})
        self.assertEqual(response.status_code, 400)

    def test_list_games_from_user_1_and_user_2(self):
        """ list games from users """

        client = APIClient()

        # create a new user 1
        user_1 = client.post('/api/accounts/register/', self.user_dict1)
        self.assertEqual(user_1.status_code, 201, user_1.data)

        # get token from user_1 login
        token_user_1 = client.post('/api/accounts/login/', self.user_dict1)
        self.assertEqual(token_user_1.status_code, 200, user_1.data)

        # create a new user 2
        user_2 = client.post('/api/accounts/register/', self.user_dict2)
        self.assertEqual(user_2.status_code, 201, user_2.data)

        # get token from user_2 login
        token_user_2 = client.post('/api/accounts/login/', self.user_dict2)
        self.assertEqual(token_user_2.status_code, 200, user_2.data)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                           token_user_1.data['token'])

        # create a new games
        response_game_1 = client.post("/api/games/", {"numbers": 6})
        response_game_2 = client.post("/api/games/", {"numbers": 7})
        response_game_3 = client.post("/api/games/", {"numbers": 8})
        response_game_4 = client.post("/api/games/", {"numbers": 9})
        response_game_5 = client.post("/api/games/", {"numbers": 10})

        all_games_user1 = [
            response_game_1.data,
            response_game_2.data,
            response_game_3.data,
            response_game_4.data,
            response_game_5.data
        ]

        # get all games user 1
        response = client.get("/api/games/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, all_games_user1)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                           token_user_2.data['token'])

        # create a new games
        response_game_1 = client.post("/api/games/", {"numbers": 10})
        response_game_2 = client.post("/api/games/", {"numbers": 9})
        response_game_3 = client.post("/api/games/", {"numbers": 8})
        response_game_4 = client.post("/api/games/", {"numbers": 7})
        response_game_5 = client.post("/api/games/", {"numbers": 6})

        all_games_user2 = [
            response_game_1.data,
            response_game_2.data,
            response_game_3.data,
            response_game_4.data,
            response_game_5.data
        ]

        # get all games user 2
        response = client.get("/api/games/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, all_games_user2)

    def test_retrive_games_from_user_1_and_user_2(self):
        """ retrive games from users """

        client = APIClient()

        # create a new user 1
        user_1 = client.post('/api/accounts/register/', self.user_dict1)
        self.assertEqual(user_1.status_code, 201, user_1.data)
        print(user_1.data)

        # get token from user_1 login
        token_user_1 = client.post('/api/accounts/login/', self.user_dict1)
        self.assertEqual(token_user_1.status_code, 200, user_1.data)

        # create a new user 2
        user_2 = client.post('/api/accounts/register/', self.user_dict2)
        self.assertEqual(user_2.status_code, 201, user_2.data)

        # get token from user_2 login
        token_user_2 = client.post('/api/accounts/login/', self.user_dict2)
        self.assertEqual(token_user_2.status_code, 200, user_2.data)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                           token_user_1.data['token'])

        # create a new games to user 1
        response = client.post("/api/games/", {"numbers": 6})
        self.assertEqual(response.status_code, 201)
        print(response.data)

        response = client.post("/api/games/", {"numbers": 7})
        self.assertEqual(response.status_code, 201)

        response = client.post("/api/games/", {"numbers": 8})
        self.assertEqual(response.status_code, 201)

        response = client.post("/api/games/", {"numbers": 9})
        self.assertEqual(response.status_code, 201)

        response = client.post("/api/games/", {"numbers": 10})
        self.assertEqual(response.status_code, 201)

        # get games of user 1 with token of user 1
        response = client.get("/api/games/12/")
        self.assertEqual(response.status_code, 200)

        response = client.get("/api/games/13/")
        self.assertEqual(response.status_code, 200)

        response = client.get("/api/games/14/")
        self.assertEqual(response.status_code, 200)

        response = client.get("/api/games/15/")
        self.assertEqual(response.status_code, 200)

        response = client.get("/api/games/16/")
        self.assertEqual(response.status_code, 200)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                           token_user_2.data['token'])

        # create a new games to user 2
        response = client.post("/api/games/", {"numbers": 10})
        self.assertEqual(response.status_code, 201)

        response = client.post("/api/games/", {"numbers": 9})
        self.assertEqual(response.status_code, 201)

        response = client.post("/api/games/", {"numbers": 8})
        self.assertEqual(response.status_code, 201)

        response = client.post("/api/games/", {"numbers": 7})
        self.assertEqual(response.status_code, 201)

        response = client.post("/api/games/", {"numbers": 6})
        self.assertEqual(response.status_code, 201)

        # get games of user 1 with token of user 2
        response = client.get("/api/games/12/")
        self.assertEqual(response.status_code, 404)

        response = client.get("/api/games/13/")
        self.assertEqual(response.status_code, 404)

        response = client.get("/api/games/14/")
        self.assertEqual(response.status_code, 404)

        response = client.get("/api/games/15/")
        self.assertEqual(response.status_code, 404)

        response = client.get("/api/games/16/")
        self.assertEqual(response.status_code, 404)

        # get games of user 2 with token of user 2
        response = client.get("/api/games/17/")
        self.assertEqual(response.status_code, 200)

        response = client.get("/api/games/18/")
        self.assertEqual(response.status_code, 200)

        response = client.get("/api/games/19/")
        self.assertEqual(response.status_code, 200)

        response = client.get("/api/games/20/")
        self.assertEqual(response.status_code, 200)

        response = client.get("/api/games/21/")
        self.assertEqual(response.status_code, 200)

        client.credentials(HTTP_AUTHORIZATION='Bearer ' +
                           token_user_1.data['token'])

        # get games of user 2 with token of user 1
        response = client.get("/api/games/17/")
        self.assertEqual(response.status_code, 404)

        response = client.get("/api/games/18/")
        self.assertEqual(response.status_code, 404)

        response = client.get("/api/games/19/")
        self.assertEqual(response.status_code, 404)

        response = client.get("/api/games/20/")
        self.assertEqual(response.status_code, 404)

        response = client.get("/api/games/21/")
        self.assertEqual(response.status_code, 404)
