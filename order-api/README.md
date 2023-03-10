# Order Service

This services processes orders given a valid authentication token, a title number and a document type.

Authentication tokens are issued by the [authentication service](../auth-api) and are valid for **30 seconds**.

Document orders are then processed by an [OCR worker](../ocr-worker) in the background via a message queue.

## Dependencies

- Python 3.11+
- Redis

## Quickstart

Example:

```bash
$ python --version
Python 3.11.0
$ redis-cli ping
PONG
$ pip install -r requirements.txt
$ export HTTP_PORT=5000
$ export REDIS_URL=redis://127.0.0.1:6379/0
$ export JWT_SECRET=supersecret
$ python main.py
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

## Environment variables

| Environment variable | Description                                                                   |
| -------------------- | ----------------------------------------------------------------------------- |
| HTTP_PORT            | **Required**. Port to bind HTTP server. Default: `5000`.                      |
| REDIS_URL            | **Required**. Redis URL. Default: `redis://127.0.0.1:6379/0`                  |
| JWT_SECRET           | **Required**. [JSON Web Tokens] secret. Must be the same as that of Auth API. |

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
Date: Mon, 09 Jan 2023 17:56:12 GMT
Server: Werkzeug/2.2.2 Python/3.11.0

{
    "healthy": true
}
```

### POST /orders - Order a document

A valid authentication token generated by the [Auth API] is required. The `can_order` property of a user must be `true`.

Remember that authentication tokens are valid for **30 seconds**.

#### Request

| Argument      | Description                                                              |
| ------------- | ------------------------------------------------------------------------ |
| token         | **Required**. Valid authentication token from the [Auth API].            |
| title_number  | **Required**. Title number of the document to order. Example: OW12345678 |
| document_type | **Required**. Type of document to order. Example: `lease`, `deed`.       |

Example:

```bash
$ http --form post http://127.0.0.1:5000/orders \
    title_number=OW12345678 \
    document_type=lease
    token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFsaWNlIiwiY2FuX3RyYW5zYWN0Ijp0cnVlLCJleHAiOjE2NzMyODYxNTh9.gOaA5omC38CtHJmNArJBv-3Ej2J3hInS_3d6LUluxKk
```

```http
POST /orders HTTP/1.1
Accept: */*
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Length: 219
Content-Type: application/x-www-form-urlencoded; charset=utf-8
Host: 127.0.0.1:5000
User-Agent: HTTPie/3.2.1

title_number=OW12345678&document_type=lease&token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFsaWNlIiwiY2FuX3RyYW5zYWN0Ijp0cnVlLCJleHAiOjE2NzMyODYxNTh9.gOaA5omC38CtHJmNArJBv-3Ej2J3hInS_3d6LUluxKk
```

#### Response

```http
HTTP/1.1 200 OK
Connection: close
Content-Length: 66
Content-Type: application/json
Date: Mon, 09 Jan 2023 18:01:02 GMT
Server: Werkzeug/2.2.2 Python/3.11.0

{
    "document_type": "lease",
    "order_id": "59ed413f-4546-40e1-9eba-5db8a7473e89",
    "title_number": "OW12345678",
    "user_id": 1
}
```

[auth api]: ../auth-api
[json web tokens]: https://jwt.io/
