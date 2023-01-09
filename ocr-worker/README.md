# OCR Worker

This worker takes jobs from a message queue and performs OCR against the document.

For now, this service is a work-in-progress and only prints the job to the console.

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
$ export REDIS_URL=redis://127.0.0.1:6379/0
$ python main.py
14:13:19 Worker rq:worker:8313e0bf6a5e489ca4339886397a6094: started, version 1.11.1
14:13:19 Subscribing to channel rq:pubsub:8313e0bf6a5e489ca4339886397a6094
14:13:19 *** Listening on default..
```

## Environment variables

| Environment variable | Description                                                  |
| -------------------- | ------------------------------------------------------------ |
| REDIS_URL            | **Required**. Redis URL. Default: `redis://127.0.0.1:6379/0` |
