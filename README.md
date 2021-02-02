# DoranDoran
---------
## Commit 메세지 작성 규칙

- `Feature ` - 새로운 기능 추가
- `Update  ` - 기능 수정
- `Fix     ` - 버그 fix
- `Refactor` - 코드 리팩토링
- `Style   ` - 스타일 (코드 형식, 세미콜론 추가: 비즈니스 로직에 변경 없음)
- `Docs    ` - 문서 추가, 수정, 삭제
- `Test    ` - 테스트 코드 추가, 수정, 삭제
- `Etc     ` - 기타 변경사항 (빌드 스크립트 수정 등)


------
## API 명세

자세한 정보는 [Notion](https://www.notion.so/API-91a928aa0af940f1a06f136633f4166b)에서 확인해주세요
### 앞에 `AUTH` 가 붙어있으면 header 에 `"Auhtorization" : "jwt <token>"` 넣어야 한다.

# Authentication

- POST /auth/login/ - 로그인
- `AUTH` POST /auth/refresh - 토큰 변경

---

# User

- POST auth/users/ - 유저 생성 (회원가입)
- GET auth/users/ - 유저 정보 조회 (모두)
- GET auth/users/<uid>/ - 유저 정보 조회 (단일)
- `AUTH` DELETE auth/users/<uid>/ - 유저 삭제 (모두)
- `AUTH` PATCH auth/users/<uid>/change-name - 유저 이름 변경
- `AUTH` PATCH auth/users/<uid>/change-password - 유저 삭제

# Conference Room

- `AUTH` POST /room (회의실 생성)
- `AUTH` GET /room (회의실 조회)
- `AUTH` GET /room/{room_id} (회의실 세부정보)
- `AUTH` DELETE /room/{room_id} (회의실 삭제)
- `AUTH` PUT /room/{room_id} (회의실 정보 변경)

---

# Reservation

- `AUTH` POST /reserve (회의실 예약) // 하나의 팀이 회의실을 여러교시 독점해도 되는지 나중에 회의하자
- `AUTH` DELETE /reserve/{reserve_id} (예약 취소)
- `AUTH` GET /reserve (예약 조회)
- `AUTH` GET /reserve/{reserve_id} (예약 세부 정보)
- `AUTH` PATCH /reserve/{reserve_id} (예약 응답)

# Team

- `AUTH` GET /team/ (모든 팀 기본정보 확인)
- `AUTH` POST /team (팀 생성)
- `AUTH` DELETE /team/{team_id} (팀 삭제)
- `AUTH` POST /team/member(팀원 추가)
- `AUTH` DELETE /team/member/{team_id} (팀원 삭제)
- `AUTH` GET /team/member/{team_id}/detailed/ (전체 팀원)