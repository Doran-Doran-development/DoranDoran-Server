from django.test import TestCase, Client
from rest_framework import status
from team.models import Team, LinkedTeamUser
from account.models import User
from django.contrib.auth.hashers import make_password


client = Client()

# 등록 예외 상황
# 1. 이미 해당 팀에 등록되어 있을때 => LinkedTeamUser 테이블에 자신의 email, teamid가 이미 존재할 경우
# 2. email이 존재하지 않을 경우 => User 테이블에 이메일이 없을 경우
# 3. teacher의 position이 teacher이 아닐때
class RegisterTeam(TestCase):
    def setUp(self):
        self.exist_user = {
            "email": "woungsub1234@gmail.com",
            "name": "변웅섭",
            "pwd": make_password("woungsub123!"),
            "is_teacher": False,
        }

        self.exist_teacher = {
            "email": "gildong@naver.com",
            "name": "홍길동",
            "pwd": make_password("gildong9876!"),
            "is_teacher": True,
        }

        self.exist_team = {
            "project": "[2021ImagineCup]-[Test]",
            "description": "microsoft에서 주최하는 ImagineCup에 참가하는 test 팀입니다.",
            "teacher": "gildong@naver.com",
        }

        self.exist_linked_user = {"email": "wougnsub1234@gmail.com"}

        User.objects.create(**self.exist_user)
        User.objects.create(**self.exist_teacher)
        Team.objects.create(**self.exist_team)
        # LinkedTeamUser.objects.create(**self.exist_linked_user)

    def tearDown(self):
        User.objects.all().delete()
        Team.objects.all().delete()
        LinkedTeamUser.objects.all().delete()

    # 등록 성공할 테스트
    def test_register_success(self):
        success_data = {
            "email": "woungsub1234@gmail.com",
            "project": "안채웅양치프로젝트",
            "description": "WHO에서 주최하는 환경보전 아이디어대회에 안채웅양치프로젝트로 참가하는 clean팀입니다",
            "teacher": "gildong@naver.com",
        }
        response = client.post("/team", success_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 이미 해당 팀에 등록 되어 있는경우
    def test_register_failed_with_already_registered(self):
        new_exist_team
        response = client.post(
            "/team", self.exist_team, content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 회원 이메일이 존재하지 않는 경우
    def test_register_failed_with_email_not_existed(self):
        fail_data = {
            "email": "chaeul123@gmail.com",
            "project": "안채웅양치프로젝트",
            "description": "WHO에서 주최하는 환경보전 아이디어대회에 안채웅양치프로젝트로 참가하는 clean팀입니다",
            "teacher": "gildong@naver.com",
        }
        response = client.post("/team", fail_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 담당 선생님이 존재하지 않는 경우
    def test_register_failed_with_teacher_not_existed(self):
        fail_data = {
            "email": "woungsub1234@gmail.com",
            "project": "안채웅양치프로젝트",
            "description": "WHO에서 주최하는 환경보전 아이디어대회에 안채웅양치프로젝트로 참가하는 clean팀입니다",
            "teacher": "chaeul@naver.com",
        }
        response = client.post("/team", fail_data, content_type="application/json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
