# 📋 Online Survey Platform

### **"누구나 쉽게 만들고, 배포하고, 분석하는 온라인 설문/투표 플랫폼"**

설문지 생성부터 배포, 응답 수집, 통계 시각화까지 한 곳에서 처리할 수 있는 풀스택 웹 서비스입니다.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)

---

## 📌 프로젝트 소개

**Online Survey Platform**은 사용자가 설문지를 직접 만들어 이메일로 배포하고, 수집된 응답을 통계로 확인할 수 있는 웹 서비스입니다. 선택형·단답형 질문을 조합해 설문을 구성하고, 공개/비공개 설정과 마감일 관리 기능을 통해 체계적인 설문 운영이 가능합니다.

### 🎯 해결하고자 한 문제

| 문제점 | 솔루션 |
| --- | --- |
| 설문지 공유가 번거롭고 별도 링크 관리가 필요함 | Gmail SMTP 기반 이메일 직접 배포 기능 |
| 응답 결과를 수동으로 집계해야 함 | 선택형/텍스트형 응답 자동 통계 집계 API |
| 설문 기간 관리가 어려움 | 마감일 자동 설정 (기본: 생성일 + 14일) |
| 비밀번호 분실 시 계정 복구가 불편함 | 이메일 인증코드 기반 비밀번호 재설정 |

---

## ✨ 주요 기능

### 📝 설문지 관리

- 설문지 생성 / 수정 / 삭제
- 선택형(단일·복수) 및 텍스트 단답형 질문 구성
- 공개/비공개 설정으로 참여 대상 제한
- 마감일 설정 (기본값: 생성일로부터 14일)

### 📨 설문 배포

- Gmail SMTP를 통한 이메일 직접 발송
- 배포 링크로 비회원도 응답 참여 가능

### 📊 응답 및 통계

- 응답 수집 및 저장
- 선택형 질문: 선택지별 응답 수 집계
- 텍스트 질문: 응답 목록 조회
- 설문별 통합 통계 조회 API

### 👤 사용자 인증

- 회원가입 / 로그인 / 로그아웃
- JWT 기반 인증 (Access Token + Refresh Token, HttpOnly Cookie)
- 역할 기반 접근 제어 (User / Admin)
- 프로필 이미지 업로드 및 삭제
- 이메일 인증코드를 통한 비밀번호 찾기 및 재설정

---

## 🛠️ 기술 스택

| 분류 | 기술 |
| --- | --- |
| **Backend Framework** | FastAPI |
| **언어** | Python 3.x |
| **Database** | MySQL, SQLAlchemy 2.0 (Async ORM) |
| **DB 마이그레이션** | Alembic |
| **인증** | PyJWT, Passlib (bcrypt), HttpOnly Cookie |
| **이메일** | Gmail SMTP (smtplib) |
| **Frontend** | React 19, Vite |
| **스타일링** | Tailwind CSS v4 |
| **라우팅** | React Router DOM v7 |
| **HTTP 통신** | Axios |
| **알림 UI** | SweetAlert2 |

---

## 🏗️ 시스템 아키텍처

```
[Frontend - React + Vite]
         │  Axios (REST API 호출)
         ▼
[Backend - FastAPI]
  ├── Router Layer      # API 엔드포인트 정의
  ├── Service Layer     # 비즈니스 로직 처리
  ├── CRUD Layer        # DB 쿼리 로직
  └── Database Layer    # SQLAlchemy Async ORM
         │
         ▼
[MySQL Database]
  ├── users / user_roles / roles
  ├── surveys / survey_questions / survey_options
  ├── responses / response_details
  ├── images
  └── email_logs
```

---

## 📁 프로젝트 구조

```
TeamProject(Online_Survey_Platform)/
├── backend/
│   ├── app/
│   │   ├── core/                  # 핵심 설정 (JWT, 인증, 보안)
│   │   ├── database/
│   │   │   ├── models/            # SQLAlchemy 모델
│   │   │   │   ├── user.py        # 사용자 (역할, 프로필 이미지, 인증코드)
│   │   │   │   ├── surveys.py     # 설문지 (공개여부, 마감일)
│   │   │   │   ├── survey_question.py
│   │   │   │   ├── survey_option.py
│   │   │   │   ├── responses.py
│   │   │   │   ├── response_detail.py
│   │   │   │   ├── roles.py / user_roles.py
│   │   │   │   ├── image.py
│   │   │   │   └── email_logs.py
│   │   │   ├── schemas/           # Pydantic 스키마
│   │   │   └── crud/              # DB 쿼리 함수
│   │   ├── router/                # API 라우터
│   │   │   ├── user.py            # 회원 CRUD, 비밀번호 재설정
│   │   │   ├── survey.py          # 설문지 CRUD
│   │   │   ├── survey_question.py
│   │   │   ├── survey_option.py
│   │   │   ├── response.py        # 응답 수집
│   │   │   ├── survey_stats.py    # 통계 조회
│   │   │   ├── email.py           # 이메일 발송
│   │   │   └── image.py           # 이미지 업로드
│   │   ├── service/               # 비즈니스 로직
│   │   └── middleware/            # 토큰 갱신 미들웨어
│   ├── alembic/                   # DB 마이그레이션
│   ├── main.py                    # FastAPI 앱 진입점
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── api/                   # Axios API 모듈
│       ├── Components/
│       │   ├── Auth/              # 로그인, 회원가입, 비밀번호 찾기/재설정
│       │   ├── Pages/             # 메인, 설문 생성/수정, 내 설문 목록, 응답 페이지
│       │   ├── Survey/            # 설문 배포, 결과 페이지
│       │   ├── Forms/             # 공통 폼 컴포넌트
│       │   └── Layout/            # 공통 레이아웃
│       ├── App.jsx
│       └── main.jsx
└── README.md
```

---

## 🚀 실행 방법

### 환경 요구사항

- Python 3.x
- Node.js 18.x 이상
- MySQL 8.0 이상

### Backend 실행

```bash
# 1. 저장소 클론
git clone <repository_url>

# 2. backend 폴더로 이동
cd backend

# 3. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 4. 의존성 설치
pip install -r requirements.txt

# 5. 환경변수 설정 (.env 파일 생성)
# DB 설정
DB_USER=<your_db_user>
DB_PASSWORD=<your_db_password>
DB_HOST=localhost
DB_PORT=3306
DB_NAME=team_project_db

# JWT 설정
SECRET_KEY=<your_secret_key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE=6000
REFRESH_TOKEN_EXPIRE=604800

# Gmail SMTP 설정
GMAIL_USER=<your_gmail>
GMAIL_APP_PASSWORD=<your_app_password>
FRONTEND_URL=http://localhost:5173

# 6. DB 마이그레이션
alembic upgrade head

# 7. 서버 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 8. API 문서 확인
# http://localhost:8000/docs
```

### Frontend 실행

```bash
# frontend 폴더로 이동
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev

# 브라우저 접속
# http://localhost:5173
```

---

## 📊 주요 API 엔드포인트

### 인증 (Users)

| Method | Endpoint | 설명 |
| --- | --- | --- |
| POST | `/users/register` | 회원가입 |
| POST | `/users/login` | 로그인 |
| POST | `/users/logout` | 로그아웃 |
| GET | `/users/userme` | 내 정보 조회 |
| POST | `/users/forgot-password` | 비밀번호 찾기 (인증코드 발송) |
| POST | `/users/reset-password` | 비밀번호 재설정 |
| POST | `/users/profile-image` | 프로필 이미지 업로드 |
| DELETE | `/users/profile-image` | 프로필 이미지 삭제 |

### 설문지 (Surveys)

| Method | Endpoint | 설명 |
| --- | --- | --- |
| POST | `/surveys` | 설문지 생성 |
| GET | `/surveys` | 내 설문지 목록 |
| GET | `/surveys/get_all_public_surveys` | 공개 설문 전체 조회 |
| GET | `/surveys/{survey_id}` | 설문지 상세 조회 |
| PATCH | `/surveys/{survey_id}` | 설문지 수정 |
| DELETE | `/surveys/{survey_id}` | 설문지 삭제 |

### 응답 및 통계

| Method | Endpoint | 설명 |
| --- | --- | --- |
| POST | `/responses/create` | 응답 제출 |
| GET | `/survey_stats/{survey_id}/complete` | 설문 통계 조회 (선택형 + 텍스트 포함) |

---

## 👥 팀 구성

**개발 기간**: 2025.09 ~ 2025.11 (6주)

| 이름 | 역할 | 담당 |
| --- | --- | --- |
| 이경준 | **PL, Backend** | DB↔Backend 연동, Gmail SMTP 이메일 서비스, 비밀번호 찾기/재설정, 프로필 이미지 API, 역할 기반 접근 제어(M:M), 설문 통계 API |
| 팀원 B | Backend | 추후 업데이트 |
| 팀원 C | Backend | 추후 업데이트 |
| 팀원 D | Frontend | 추후 업데이트 |
| 팀원 E | Frontend | 추후 업데이트 |
| 팀원 F | Frontend | 추후 업데이트 |

---

## 📝 라이선스

This project is licensed under the MIT License.
