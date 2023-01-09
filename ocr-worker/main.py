#!/usr/bin/env python
import os

from redis import StrictRedis
from rq import Connection
from rq import Worker


def ocr_document(*, order_id: str, user_id: int, title_number: str, document_type: str):
    # TODO: OCR Document

    print(
        f"==> Processing document: {order_id=} {user_id=} {title_number=} {document_type=}"
    )


if __name__ == "__main__":
    redis_url: str = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")

    conn = StrictRedis.from_url(redis_url)

    with Connection(conn):
        worker = Worker("default")
        worker.work()
