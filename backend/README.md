# prep-exec-analysis Backend

## 백엔드 서버 실행 방법

```
docker-compose up --build -d
```

## DB 마이그레이션 버전 업그레이드/다운그레이드

```
$ docker exec -it backend bash
# alembic alembic upgrade head -> 업그레이드
# alembic alembic downgrade -1 -> 다운그레이드
# alembic revision --autogenerate -m "comment" -> 마이그레이션 파일 생성
```

## 프로젝트 구조

```
app
├── alembic                 - 리비전을 사용하여 DB 스키마 관리
│   └── versions            - 마이그레이션 버전 관리
├── app
│   ├── api                 - api 정의
│   ├── core                - 프로그램 구성, 시작 이벤트, 로깅처리
│   ├── crud                - 공통으로 사용되는 crud 함수 정의 및 커스텀 crud에 필요한 함수 정의
│   ├── db                  - DB 커넥션 관리
│   ├── fastapi_pagination  - 페이지네이션 정의
│   ├── models              - 모델 정의
│   ├── schemas             - pydantic으로 입출력 모델의 유형과 제약 조건 관리
│   └── main.py             - FastAPI 애플리케이션 생성 및 구성
└── README.md
```
