# Authentication Service

This service creates authentication tokens to valid users that have provided correct authentication details.

The tokens are valid for **30 seconds** and can be used to make requests to other services (only [Order API] in this exercise).

## Dependencies

- Python 3.11+

## Quickstart

Example:

```bash
$ python --version
Python 3.11.0
$ pip install -r requirements.txt
$ export HTTP_PORT=5000
$ export JWT_SECRET=supersecret
$ python main.py
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

## Environment variables

| Environment variable | Description                                                                      |
| -------------------- | -------------------------------------------------------------------------------- |
| HTTP_PORT            | **Required**. Port to bind HTTP server. Default: `5000`.                         |
| JWT_SECRET           | **Required**. [JSON Web Tokens] secret. Must be the same as that of [Order API]. |

## User database

User credentials are stored in the [users.json](users.json) file.

Example user model:

```json
{
  "id": 1,
  "username": "alice",
  "password": "password",
  "can_order": true
}
```

`can_order` determines whether the user is allowed to order documents using the [Order API].

User creation and management are out of the scope of this service.

## Endpoints

### GET /health - Health check

Health check to see if the service is up.

#### Request

```bash
$ http http://127.0.0.1:5000/health
```

```http
GET /health HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Host: 127.0.0.1:5000
User-Agent: HTTPie/3.2.1
```

#### Response

```http
HTTP/1.1 200 OK
Connection: close
Content-Length: 17
Content-Type: application/json
Date: Mon, 09 Jan 2023 17:41:01 GMT
Server: Werkzeug/2.2.2 Python/3.11.0

{
    "healthy": true
}
```

### POST /token - Create an authentication token

Create an authentication token for the given user. Tokens are valid for **30 seconds**.

#### Request

| Argument | Description                                  |
| -------- | -------------------------------------------- |
| username | **Required**. Username in the user database. |
| password | **Required**. Password for the user.         |

Usage:

```bash
$ http --form post http://127.0.0.1:5000/token \
    username=alice \
    password=password
```

```http
POST /token HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 32
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Host: 127.0.0.1:5000
User-Agent: HTTPie/3.2.1

username=alice&password=password
```

#### Response

```http
HTTP/1.1 200 OK
Connection: close
Content-Length: 186
Content-Type: application/json
Date: Mon, 09 Jan 2023 17:42:08 GMT
Server: Werkzeug/2.2.2 Python/3.11.0

{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFsaWNlIiwiY2FuX3RyYW5zYWN0Ijp0cnVlLCJleHAiOjE2NzMyODYxNTh9.gOaA5omC38CtHJmNArJBv-3Ej2J3hInS_3d6LUluxKk"
}
```

[order api]: ../order-api
[json web tokens]: https://jwt.io/
