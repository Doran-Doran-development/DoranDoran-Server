from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserBackend(BaseBackend):
    """
    settings.AUTH_USER_MODEL 셋팅에 의존한다.
    """
    def authenticate(self, email = None, password = None, *args, **kwargs):
        # is_active인지 체크하고
        # email에 맞는 인스턴스 존재하는지 확보,
        # password랑 맞는지 체크

    

    