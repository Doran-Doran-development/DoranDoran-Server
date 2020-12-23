from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import exceptions
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _

from .models import User


def jwt_get_uid_from_payload_handler(payload):
    return payload.get("uid")


class CustomJSONWebTokenAuthentication(JSONWebTokenAuthentication):
    def authenticate_credentials(self, payload):
        """
        Returns an active user that matches the payload's user id and uid.
        """
        uid = jwt_get_uid_from_payload_handler(payload)

        if not uid:
            msg = _("Invalid payload.")
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get_by_natural_key(uid)
        except User.DoesNotExist:
            msg = _("Invalid signature.")
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = _("User account is disabled.")
            raise exceptions.AuthenticationFailed(msg)

        return user