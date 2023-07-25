# prep-exec-analysis Backend

## 백엔드 서버 실행 방법

```
docker-compose up --build -d
```

## 프로젝트 구조

```
app
├── app
│   ├── api                 - api 정의
│   ├── core                - 프로그램 구성, 시작 이벤트, 로깅처리
│   ├── crud                - 공통으로 사용되는 crud 함수 정의 및 커스텀 crud에 필요한 함수 정의
│   ├── db                  - DB 커넥션 관리
│   ├── models              - 모델 정의
│   ├── schemas             - pydantic으로 입출력 모델의 유형과 제약 조건 관리
│   └── main.py             - FastAPI 애플리케이션 생성 및 구성
└── README.md
```
