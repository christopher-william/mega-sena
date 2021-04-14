# Teste Técnico Mega Sena 

API que faz jogos da mega sena, o usuario escolhe a quantidade de dezenas por jogo e a API irá gerar aleatoriamente dezenas para o usuário. O usuário poderá consultar o resultado do ultimo jogo e comparar com suas dezenas para conferir quantos numeros acertou.
## Base URL

```
https://localhost:8000
```

# Endpoints

## POST /api/accounts/register/

Register one user

### Body

```json
{
  "username": "admin",
  "password": "1234",
  "is_superuser": true,
  "is_staff": true
}
```

### Response Return

```json
{
  "id": 1,
  "username": "admin",
  "is_staff": true,
  "is_superuser": true
}
```

## POST /api/accounts/login/

Login with a user

### Body

```json
{
  "username": "admin",
  "password": "1234"
}
```

### Response Return

```json
{
  "token": "BARER TOKEN"
}
```

## PUT /api/accounts/edit/

Edit one user

### header

```json
Authorization: 'Bearer ' + <TOKEN>
```


### Body

```json
{
  "username": "admin",
  "password": "1234",
  "is_staff": true, // Opicional
  "is_superuser": true, // Opicional
  "is_active": true // Opicional
}
```

### Response Return

```json
{
  "id": 1,
  "username": "admin",
  "password": "1234",
  "is_staff": true,
  "is_superuser": true
}
```

## DELETE /api/accounts/delete/

Delete / Desativate the user

### header

```json
Authorization: 'Bearer ' + <TOKEN>
```

### Response Return -> 204 NOT CONTENT


## Games

## POST /api/games/

Create a game

### header

```json
Authorization: 'Bearer ' + <TOKEN>
```


### Body

```json
{
  "numbers": 10
}
```

### Response Return

```json
{
  "id": 1,
  "numbers": [33, 50, 19, 16, 38, 11, 14, 43, 30, 8],
  "user": {
    "id": 1,
    "username": "admin",
    "is_superuser": true,
    "is_staff": true
  },
  "date": "2021-04-14",
  "time": "19:13:21.868947"
}
```

## GET /api/games/

List all user games

### header

```json
Authorization: 'Bearer ' + <TOKEN>
```

### Response Return

```json
[
 {
   "id": 1,
   "numbers": [33, 50, 19, 16, 38, 11, 14, 43, 30, 8],
   "user": {
     "id": 1,
     "username": "admin",
     "is_superuser": true,
     "is_staff": true
   },
   "date": "2021-04-14",
   "time": "19:13:21.868947"
 },
]
```

## GET /api/games/game_id/

Retrive one user game

### header

```json
Authorization: 'Bearer ' + <TOKEN>
```

### Response Return

```json
[
 {
   "id": 1,
   "numbers": [33, 50, 19, 16, 38, 11, 14, 43, 30, 8],
   "user": {
     "id": 1,
     "username": "admin",
     "is_superuser": true,
     "is_staff": true
   },
   "date": "2021-04-14",
   "time": "19:13:21.868947"
 },
]
```

## GET /api/games/game_id/result

Retrive one user game result

### header

```json
Authorization: 'Bearer ' + <TOKEN>
```

### Response Return

```json
{
  "winning_numbers": [14, 21, 22, 29, 35, 46],
  "game_numbers": [33, 50, 19, 16, 38, 11, 14, 43, 30, 8],
  "matching_numbers": [14]
}
```

## GET /api/games/megasena/

Retrive the mega sena result
### header

```json
Authorization: 'Bearer ' + <TOKEN>
```

### Response Return

```json
[14, 21, 22, 29, 35, 46]
```


- **Note: this project is create by [Christopher William](https://www.linkedin.com/in/christopher-william-4363321a5/), see more about!**