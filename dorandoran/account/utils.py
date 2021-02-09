import jwt

from datetime import datetime, timedelta
from calendar import timegm
from django.conf import settings
from .models import User


def jwt_encode_handler(payload):
    key = settings.JWT_AUTH["JWT_SECRET_KEY"]
    algorithm = settings.JWT_AUTH["JWT_ALGORITHM"]

    return jwt.encode(dict(payload), key, algorithm).decode("utf-8")


def jwt_decode_handler(token):
    key = settings.JWT_AUTH["JWT_SECRET_KEY"]
    algorithm = settings.JWT_AUTH["JWT_ALGORITHM"]
    return jwt.decode(token, key, algorithm)


def jwt_payload_handler(user):
    expriation_time = datetime.utcnow() + settings.JWT_AUTH["JWT_EXPIRATION_DELTA"]
    payload = {
        "exp": timegm(expriation_time.utctimetuple()),
        "uid": user.uid,
        "email": user.email,
        "is_active": user.is_active,
        "name": user.name,
        "role": user.role,
    }

    if settings.JWT_AUTH["JWT_ALLOW_REFRESH"]:
        payload["iat"] = timegm(datetime.utcnow().utctimetuple())
    return payload


def get_username_field():
    try:
        username_field = User.USERNAME_FIELD
    except:
        username_field = "uid"
    return username_field
