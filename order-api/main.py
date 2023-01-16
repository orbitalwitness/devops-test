#!/usr/bin/env python
import os
import uuid

import jwt
from flask import Flask, jsonify
from flask import current_app
from flask import request
from flask_rq2 import RQ

app = Flask(__name__)
rq = RQ()


@app.route("/orders", methods=["POST"])
def create_order():
    token: str = request.form.get("token")
    title_number: str = request.form.get("title_number")
    document_type: str = request.form.get("document_type")

    if not token:
        return jsonify(error="Token is blank"), 422
    if not title_number:
        return jsonify(error="Title number is blank"), 422
    if not document_type:
        return jsonify(error="Document type is blank"), 422

    try:
        payload = jwt.decode(
            token,
            current_app.config["JWT_SECRET"],
            algorithms=["HS256"],
        )
    except jwt.InvalidTokenError as exc:
        return jsonify(error=str(exc)), 422
    else:
        if payload["can_order"]:
            order_id = str(uuid.uuid4())

            # TODO: Download documents from an External API

            rq.get_queue().enqueue(
                "__main__.ocr_document",
                order_id=order_id,
                user_id=payload["user_id"],
                title_number=title_number,
                document_type=document_type,
            )
            return jsonify(
                order_id=order_id,
                user_id=payload["user_id"],
                title_number=title_number,
                document_type=document_type,
            )
        else:
            return jsonify(error="User cannot order documents"), 403


@app.route("/health")
def health():
    return jsonify(healthy=True)


if __name__ == "__main__":
    # Env
    redis_url: str = os.getenv("REDIS_URL", "redis://127.0.0.1:6379/0")
    http_port: int = int(os.getenv("HTTP_PORT", 5000))
    jwt_secret: str = os.environ["JWT_SECRET"]

    # Flask config
    app.config["RQ_REDIS_URL"] = redis_url
    app.config["JWT_SECRET"] = jwt_secret
    rq.init_app(app)

    # Run app
    app.run(host="0.0.0.0", port=http_port, threaded=True)
