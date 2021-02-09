import os

SETTINGS_MODULE = os.environ.get("DJANGO_SETTINGS_MODULE")
# 환경 변수에서 DJANGO_SETTINGS_MODULE을 지정해주지 않으면 .local 파일을 임포트 해준다
if not SETTINGS_MODULE or SETTINGS_MODULE == "config.settings":
    from .dev import *
