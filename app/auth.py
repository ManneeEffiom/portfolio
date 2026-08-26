import functools

import jwt
from flask import jsonify, request

from app.config import config


def encode_token():
    payload = {"sub": config.ADMIN_USERNAME, "exp": _exp()}
    return jwt.encode(payload, config.SECRET_KEY, algorithm="HS256")


def _exp():
    from datetime import datetime, timedelta, timezone

    return datetime.now(timezone.utc) + timedelta(seconds=config.JWT_TTL_SECONDS)


def decode_token(token):
    try:
        return jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None


def login_required(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "missing token"}), 401
        token = auth.split(" ", 1)[1]
        if not decode_token(token):
            return jsonify({"error": "invalid token"}), 401
        return f(*args, **kwargs)

    return wrapper
