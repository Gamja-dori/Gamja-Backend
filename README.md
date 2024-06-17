# Gamja-Backend
> 다시: 은퇴한 시니어를 위한 긱 워킹 채용 플랫폼의 백엔드 리포지토리

<p align="center">
    <a href="https://dasi-expert.com" target="_blank">
        <img src="https://github.com/Gamja-dori/Gamja-Backend/assets/100199530/97ab599d-3892-4a43-9cd8-fd77dfe3e8aa" alt="dasi" width="750"/>
        <br>웹 사이트 바로가기
    </a>
</p>

# 설치 및 실행

1. 프로젝트 클론

```sh
git clone https://github.com/Gamja-dori/Gamja-Backend.git
cd Gamja-Backend
```

2. 가상환경 설정

```sh
python -m venv venv
venv\Scripts\activate
```

3. 필수 패키지 설치

```sh
pip install -r dasi/requirements.txt
```

4. 환경 변수 설정
settings.py와 같은 폴더 안에 `.env` 파일을 생성하고 환경 변수를 설정합니다.

```sh
NAME=
DB_USER=
PASSWORD=
HOST=
PORT=
SECRET_KEY=
EC2_PUBLIC_ADDR=
KAKAO_SECRET_KEY=
```

5. 실행

```sh
python manage.py runserver
```

# 기술 스택

## Development
![Django](https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white)

## Deploy
![NGINX](https://img.shields.io/badge/nginx-009639?style=for-the-badge&logo=nginx&logoColor=white)
![Gunicorn](https://img.shields.io/badge/gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)
![Docker](https://img.shields.io/badge/docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/aws-232F3E?style=for-the-badge&logo=amazonwebservices&logoColor=white)
![Github Actions](https://img.shields.io/badge/githubactions-2088FF?style=for-the-badge&logo=githubactions&logoColor=white)

## AI
<p align="center">
    <img src="https://github.com/Gamja-dori/Gamja-Backend/assets/100199530/c1cf3604-0b24-40b8-bb7a-fc5e8a6ddff5" alt="Clova OCR" width="450"/>
</p>
Clova OCR을 이용해서 기존 이력서로부터 경력사항, 학력사항 정보를 추출했습니다.

<p align="center">
    <img src="https://github.com/Gamja-dori/Gamja-Backend/assets/100199530/958a27cd-4237-4e2d-9a91-27abe4fd342c" alt="OpenAI" width="450"/>
</p>
OpenAI를 이용하여 기존 이력서로부터 추출된 정보를 json 형식으로 포맷팅했습니다.
또한 작성한 이력서를 바탕으로 전문가 소개를 자동 생성했습니다.

<p align="center">
    <img src="https://github.com/Gamja-dori/Gamja-Backend/assets/100199530/9d77bee9-2bbf-49bb-a4bb-e8662026de15" alt="ElasticSearch" width="450"/>
</p>
ElasticSearch를 검색 엔진으로 이용하여 데이터 역색인 구조를 바탕으로 기업의 인재 검색 속도를 높였습니다. 

# 디렉토리 구조

```
dasi
├─dasi                      # 프로젝트 기본 세팅
│  ├─ .env
│  ├─ asgi.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ wsgi.py
│  ├─ __init__.py
│  └─ __pycache__
├─ users                    # 사용자 앱
|  ├─ admin.py
|  ├─ apps.py
|  ├─ migrations
|  ├─ models.py
|  ├─ serializers.py
|  ├─ tests.py
|  ├─ urls.py
|  ├─ views.py
|  ├─ __init__.py
|  └─ __pycache__
├─ resume                   # 이력서 앱
│  ├─ admin.py
│  ├─ apps.py
│  ├─ create_senior_intro.py
│  ├─ migrations
│  ├─ models.py
│  ├─ resume_ocr.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  ├─ __init__.py
│  └─ __pycache__
├─ recommend                # 인재 추천 앱
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations
│  ├─ models.py
│  ├─ recommendation.py
│  ├─ serializers.py
│  ├─ tests.py
│  ├─ urls.py
│  ├─ views.py
│  ├─ __init__.py
│  └─ __pycache__
├─ suggest                  # 채용 제안 앱
|  ├─ admin.py
|  ├─ apps.py
|  ├─ migrations
|  ├─ models.py
|  ├─ serializers.py
|  ├─ tests.py
|  ├─ urls.py
|  ├─ views.py
|  ├─ __init__.py
|  └─ __pycache__
├─ manage.py                # 도커 및 기타 패키지 설정파일
├─ db.sqlite3
├─ requirements.txt
├─ docker-compose.yml
├─ docker-compose.debug.yml
├─ Dockerfile
├─ nginx
│  ├─ Dockerfile
│  └─ nginx.conf
├─ elasticsearch
│  └─ Dockerfile
└─ scripts
   └─ rebuild.sh
```

# app 모듈별 설명
각 기능은 https://api.dasi-expert.com/swagger 에서 테스트해보실 수 있습니다.

## 👨‍💼 User App
### 개요
> 1. 사용자 정보 생성, 조회, 수정, 삭제
> 2. jwt 토큰 기반 로그인 상태 관리
> 3. 시니어 전문가 리뷰 관리  
### 상세 기능
- `SeniorUserCreateView`, `EnterpriseUserCreateView`

    시니어, 기업 사용자 생성
- `LoginView`, `LogoutView`
    
    사용자 로그인, 로그아웃

- `UserView`
    
    사용자 정보 조회, 수정, 삭제
- `UserSecretView`
    
    채용 성사 후 사용자의 개인정보 조회
- `ProfileImageView`
    
    사용자의 프로필 사진 조회 및 변경
- `TokenObtainPairView`, `TokenRefreshView`

    jwt 토큰 관리
- `CheckDuplicateView`

    중복된 사용자 id인지 확인
- `CreateReviewView`, `GetReviewListView`, `DeleteReviewView`

    시니어 사용자의 리뷰 등록, 목록 조회, 삭제

## 📑 Resume App
### 개요
> 1. 이력서 생성 및 세부 정보 생성, 조회, 수정, 삭제 
> 2. 기존 이력서에서 OCR로 텍스트 추출하여 반환 
> 3. 기본 이력서 설정, 이력서 복제, 이력서 목록 조회 
### 상세 기능
- `CreateResumeAPIView`, `GetResumeAPIView`, `EditResumeAPIView`, `DeleteResumeAPIView`

    이력서 생성, 조회, 수정, 삭제
- `SubmitResumeAPIView`
    
    인재풀에 이력서 등록
- `SetDefaultResumeAPIView`
    
    기본 이력서 설정
- `CreateResumeDetailAPIView`, `DeleteResumeDetailAPIView`
    
    이력서 상세 항목 생성 및 삭제
- `GetResumeListAPIView`

    이력서 목록 조회
- `ChangeResumeTitleAPIView`
    
    이력서 제목 변경
- `ExtractPriorResumeAPIView`

    기존 이력서에서 경력사항 추출
- `CreateSeniorIntroAPIView`

    작성한 이력서 바탕으로 전문가 소개 생성
- `CopyResumeAPIView`

    기존 이력서 복제 

## 🔍 Recommend App
### 개요
> 1. 인재 추천 AI를 거쳐 추천된 이력서 목록 반환
> 2. 인재 목록 필터링
> 3. 이력서 상세 조회
### 상세 기능
- `MainView`

    인재 추천 메인 화면에서 지금 떠오르는 인재 조회 (조회수 높은 순)
- `SearchView`
    
    인재 추천 및 필터링
- `ResumeDetailView`
    
    이력서 상세 조회

## 🤝 Suggest App
### 개요
> 1. 채용 제안 생성 및 관리 
> 2. 카카오페이와 연동하여 매칭 수수료 결제 
> 3. 채용 성사 여부 및 결제 여부 조회
### 상세 기능
- `CreateSuggestView`

    기업 사용자가 채용 제안 전송
- `GetSeniorListView`, `GetInProgressSeniorListView`,  `GetCompletedSeniorListView`
    
    기업 사용자의 조건별 채용 제안 목록 조회 (전체, 진행 중, 완료됨)
- `GetSuggestDetailView`

    채용 제안의 상세 내용 조회
- `GetNotificationCountView`
    
    새로운 알림 개수 조회
- `GetEnterpriseNotificationsView`

    기업 사용자의 알림창에서 채용 제안 목록 조회
- `GetSeniorNotificationsView`
    
    시니어 사용자의 알림창에서 채용 제안 목록 조회
- `PatchNotificationView`

    채용 제안 열람 여부 갱신
- `GetProgressView`, `UpdateProgressView`

    채용 제안의 상태 조회 및 변경 
    
    - 상태 목록: 'is_pending', 'is_declined', 'is_cancelled', 'is_paid', 'is_accepted', 'is_reviewed'
    
- `PaymentRequestView`, `PaymentApproveView`

    결제 요청 및 승인
- `GetIsPaidView`
    
    결제 완료 여부 조회

