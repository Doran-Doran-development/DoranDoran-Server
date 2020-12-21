from .base import *

import datetime

# 개발환경의 추가 설정을 넣어주자

CONFIG_SECRET_FILE = os.path.join(CONFIG_SECRET_DIR, "settings_develop.json")

if os.path.isfile(CONFIG_SECRET_FILE):
    # 로컬 환경 또는 배포 환경
    config_secret_file = json.loads(open(CONFIG_SECRET_FILE).read())
else:
    # 테스팅 환경 (환경변수로 지정해야댐)
    config_secret_file = json.loads(os.environ["SECRET_SETTING"])

SECRET_KEY = config_secret_file["django"]["secret_key"]  # Django Secret key

# ======= JWT 설정 =======
JWT_AUTH = {
    "JWT_ALLOW_REFRESH": True,
    "JWT_SECRET_KEY": config_secret_file["jwt"]["secret_key"],
    "JWT_ALGORITHM": config_secret_file["jwt"]["algorithm"],
    "JWT_EXPIRATION_DELTA": datetime.timedelta(days=1),
    "JWT_REFRESH_EXPIRATION_DELTA": datetime.timedelta(weeks=2),
}
# ========================

DATABASES = config_secret_file["django"]["database"]  # DB 설정