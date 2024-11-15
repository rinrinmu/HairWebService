# HairWebService

**HairWebService**는 두피 이미지를 분석하고, AI 모델을 통해 개인화된 솔루션을 제공하며, PDF 보고서를 생성하고 사용자 기록을 관리하는 웹 애플리케이션입니다. 이 프로젝트는 FastAPI 백엔드와 React 프론트엔드로 구성되어 있습니다.

## 목차

- [프로젝트 개요](#프로젝트-개요)
- [프로젝트 트리](#프로젝트-트리)
- [프로젝트 상세 구조](#프로젝트-상세-구조)
- [설치 방법](#설치-방법)
  - [백엔드 설치](#백엔드-설치)
    - [필수 사항](#백엔드-필수-사항)
    - [가상 환경 설정](#백엔드-가상-환경-설정)
    - [의존성 설치](#백엔드-의존성-설치)
    - [환경 변수 설정](#백엔드-환경-변수-설정)
 - [데이터베이스 초기화](#백엔드-데이터베이스-초기화)
  - [프론트엔드 설치](#프론트엔드-설치)
    - [필수 사항](#프론트엔드-필수-사항)
    - [의존성 설치](#프론트엔드-의존성-설치)
- [사용 방법](#사용-방법)
- [기여 가이드](#기여-가이드)
- [보안 고지](#보안-고지)
- [라이선스](#라이선스)
- [문의하기](#문의하기)

## 프로젝트 개요

**HairWebService**는 다음과 같은 주요 기능을 제공합니다:

1. **이미지 분석**: 사용자로부터 업로드된 두피 이미지를 분석하여 상태를 판정합니다.
2. **개인화 솔루션 제공**: 분석 결과를 기반으로 OpenAI의 GPT API를 활용하여 맞춤형 솔루션을 생성합니다.
3. **PDF 보고서 생성**: 분석 결과와 솔루션을 포함한 PDF 보고서를 자동으로 생성합니다.
4. **기록 관리**: 사용자의 분석 기록을 저장하고, 과거 기록을 조회 및 PDF를 재다운로드할 수 있습니다.

## 프로젝트 트리

```bash
backinit
├── .venv  # Python 가상 환경 (Git 제외)
├── app  # 백엔드 코드 (FastAPI)
│     ├── __init__.py
│     ├── models
│     │     ├── __init__.py
│     │     └── hairAI.h5  # AI 모델 파일
│     ├── static
│     │     ├── fonts
│     │     │     ├── malgun.ttf
│     │     │     └── malgunbd.ttf
│     │     ├── images  # 이미지 파일 (하위 내용만 Git 제외)
│     │     │     └── .gitkeep
│     │     └── pdfs  # PDF 파일 (하위 내용만 Git 제외)
│     │           └── .gitkeep
│     ├── utils
│     │     ├── __init__.py
│     │     ├── ai_prediction.py
│     │     ├── pdf_generator.py
│     │     └── solution.py
│     ├── database.py
│     ├── db_models.py
│     ├── main.py
│     └── schemas.py
├── frontend   # 프론트엔드 코드 (React)
│     ├── package.json  #프론트엔드 React 의존성
│     ├── package-lock.json
│     ├── node_modules  # Node.js 의존성 (Git 제외)
│     ├── public
│     └── src
│          ├── components
│          │   └── views
│          │         ├── AnalyzePage
│          │         │     └── AnalyzePage.js
│          │         ├── MainPage
│          │         │     ├── ChoosePage.css
│          │         │     ├── ChoosePage.js
│          │         │     ├── StartPage.css
│          │         │     └── StartPage.js
│          │         ├── NavBar
│          │         │     └── NavBar.js
│          │         ├── RecordsPage
│          │         │     ├── RecordsPage.css
│          │         │     └── RecordsPage.js
│          │         ├── ResultPage
│          │         │     └── ResultPage1.js
│          │         └── style
│          │             ├── resultStyle.css
│          │             └── style.css
│          ├── App.js
│          ├── index.css
│          ├── index.js
│          └── reportWebVitals.js
├── .env  # 환경 변수 파일 (Git 제외)
├── .gitignore   # Git 무시 파일 설정
├── .gitattributes  # Git 환경 파일 설정
├── app.db  # SQLite 데이터베이스 파일 (Git 제외)
├── requirements.txt # 백엔드 Python 의존성
└── README.md  # 프로젝트 문서
```

## 프로젝트 상세 구조

## .venv
- **설명:** Python 가상 환경으로, 프로젝트의 Python 의존성을 격리하여 관리합니다.
- **비고:** .gitignore에 포함되어 Git에 포함되지 않습니다.

---

## app
- **설명:** 백엔드 코드가 위치한 디렉토리로, FastAPI 프레임워크를 사용하여 API를 구현합니다.

  - ### `__init__.py`
    - **설명:** Python 패키지 초기화 파일입니다.

  - ### models
    - **설명:** 데이터 모델을 정의하는 디렉토리입니다.

    - #### `__init__.py`
      - **설명:** Python 패키지 초기화 파일입니다.

    - #### hairAI.h5
      - **설명:** AI 모델 파일로, 두피 이미지 분석에 사용됩니다.

  - ### static
    - **설명:** 정적 파일들이 위치한 디렉토리입니다.

    - #### fonts
      - **설명:** 애플리케이션에서 사용하는 폰트 파일들이 위치한 디렉토리입니다.

      - **malgun.ttf:** 맑은 고딕 폰트 파일입니다.
      - **malgunbd.ttf:** 맑은 고딕 볼드 폰트 파일입니다.
        
- #### images
  - **설명:** 이미지 파일들이 위치한 디렉토리입니다.
  - **비고:** 하위 내용은 `.gitignore`에 포함되어 Git에 포함되지 않습니다.
  - **파일:** `.gitkeep`  
    빈 디렉토리를 Git에 유지하기 위한 파일입니다.

- #### pdfs
  - **설명:** PDF 파일들이 위치한 디렉토리입니다.
  - **비고:** 하위 내용은 `.gitignore`에 포함되어 Git에 포함되지 않습니다.
  - **파일:** `.gitkeep`  
    빈 디렉토리를 Git에 유지하기 위한 파일입니다.

  - ### utils
    - **설명:** 유틸리티 스크립트들이 위치한 디렉토리입니다.

    - #### `__init__.py`
      - **설명:** Python 패키지 초기화 파일입니다.

    - #### ai_prediction.py
      - **설명:** AI 예측 관련 로직을 포함하는 스크립트입니다.

    - #### pdf_generator.py
      - **설명:** PDF 생성 관련 로직을 포함하는 스크립트입니다.

    - #### solution.py
      - **설명:** 개인화된 솔루션 제공 관련 로직을 포함하는 스크립트입니다.

  - ### database.py
    - **설명:** 데이터베이스 설정 및 연결을 관리하는 스크립트입니다.

  - ### db_models.py
    - **설명:** 데이터베이스 모델을 정의하는 스크립트입니다.

  - ### main.py
    - **설명:** FastAPI 애플리케이션의 메인 엔트리 포인트입니다.

  - ### schemas.py
    - **설명:** 데이터 스키마를 정의하는 스크립트입니다.

---

## frontend
- **설명:** 프론트엔드 코드가 위치한 디렉토리로, React 프레임워크를 사용하여 사용자 인터페이스를 구현합니다.

  - ### package.json
    - **설명:** 프론트엔드의 의존성과 스크립트를 관리하는 파일입니다.
    - **내용:** 프로젝트의 의존성 목록, 스크립트 명령어, 프로젝트 메타데이터 등이 포함됩니다.

  - ### package-lock.json
    - **설명:** 프론트엔드의 의존성 버전을 고정하기 위한 파일입니다.
    - **내용:** package.json에 명시된 의존성들의 정확한 버전과 설치 정보를 포함합니다.

  - ### node_modules
    - **설명:** Node.js 의존성들이 설치된 디렉토리입니다.
    - **비고:** .gitignore에 포함되어 Git에 포함되지 않습니다.

  - ### public
    - **설명:** 공개적으로 접근 가능한 정적 파일들이 위치한 디렉토리입니다.

  - ### src
    - **설명:** 소스 코드가 위치한 디렉토리입니다.

    - #### components
      - **설명:** 재사용 가능한 React 컴포넌트들이 위치한 디렉토리입니다.

      - ##### views
        - **설명:** 각 페이지의 뷰 컴포넌트들이 위치한 디렉토리입니다.

        - ###### AnalyzePage
          - **설명:** 두피 이미지 분석 페이지 관련 컴포넌트입니다.
          - **AnalyzePage.js:** AnalyzePage 컴포넌트 파일입니다.

        - ###### MainPage
          - **설명:** 메인 페이지 관련 컴포넌트입니다.
          - **ChoosePage.css:** ChoosePage 스타일 시트입니다.
          - **ChoosePage.js:** ChoosePage 컴포넌트 파일입니다.
          - **StartPage.css:** StartPage 스타일 시트입니다.
          - **StartPage.js:** StartPage 컴포넌트 파일입니다.

        - ###### NavBar
          - **설명:** 네비게이션 바 컴포넌트입니다.
          - **NavBar.js:** NavBar 컴포넌트 파일입니다.

        - ###### RecordsPage
          - **설명:** 기록 관리 페이지 관련 컴포넌트입니다.
          - **RecordsPage.css:** RecordsPage 스타일 시트입니다.
          - **RecordsPage.js:** RecordsPage 컴포넌트 파일입니다.

        - ###### ResultPage
          - **설명:** 결과 페이지 관련 컴포넌트입니다.
          - **ResultPage1.js:** ResultPage 컴포넌트 파일입니다.

        - ###### style
          - **설명:** 추가적인 스타일 시트들이 위치한 디렉토리입니다.
          - **resultStyle.css:** 결과 페이지 스타일 시트입니다.
          - **style.css:** 일반 스타일 시트입니다.

    - ### App.js
      - **설명:** React 애플리케이션의 메인 컴포넌트입니다.

    - ### index.css
      - **설명:** 애플리케이션의 전역 스타일 시트입니다.

    - ### index.js
      - **설명:** React 애플리케이션의 엔트리 포인트입니다.

    - ### reportWebVitals.js
      - **설명:** 웹 성능 측정을 위한 스크립트입니다.

---

## .env
- **설명:** 환경 변수 파일로, API 키 및 기타 민감한 정보를 저장합니다.
- **비고:** .gitignore에 포함되어 Git에 포함되지 않습니다.

---

## .gitignore
- **설명:** Git에서 무시할 파일 및 디렉토리를 지정하는 파일입니다.
- **내용:** .venv/, node_modules/, .env, app.db 등 민감하거나 불필요한 파일들이 포함됩니다.

---

## .gitattributes
- **설명:** Git의 동작을 제어하기 위한 파일로, 특정 파일 유형에 대한 속성 설정 등을 포함합니다.

---

## app.db
- **설명:** SQLite 데이터베이스 파일로, 애플리케이션의 데이터를 저장합니다.
- **비고:** .gitignore에 포함되어 Git에 포함되지 않습니다.

---

## requirements.txt
- **설명:** 백엔드의 Python 의존성을 관리하는 파일입니다.
- **내용:** 프로젝트에 필요한 Python 패키지 목록과 버전이 포함됩니다.

---

## README.md
- **설명:** 프로젝트의 문서 파일로, 프로젝트 개요, 설치 방법, 사용 방법, 기여 가이드 등을 포함합니다.


<br>


## 설치 방법

### 백엔드 설치

#### 백엔드 필수 사항

- **Python 3.8 이상**: [Python 공식 사이트](https://www.python.org/downloads/)에서 다운로드 및 설치.
- **pip**: Python 패키지 관리자 (Python 설치 시 기본 포함).
- **Git**: [Git 공식 사이트](https://git-scm.com/downloads)에서 다운로드 및 설치.

#### 백엔드 가상 환경 설정

백엔드의 의존성을 관리하기 위해 가상 환경을 설정합니다.
반드시 가상 환경을 설정한 이후 의존성을 설치해주세요!!

1. **백엔드 디렉토리로 이동**:

    ```bash
    cd backinit/app
    ```

2. **가상 환경 생성**:

    ```bash
    python -m venv venv
    ```

3. **가상 환경 활성화**:

    - **Windows**:

        ```bash
        venv\Scripts\activate
        ```

    - **Linux/macOS**:

        ```bash
        source venv/bin/activate
        ```

#### 백엔드 의존성 설치

1. **`requirements.txt` 파일 생성**:

    백엔드 의존성을 관리하기 위해 `requirements.txt` 파일을 생성합니다. (이미 존재하는 경우 이 단계를 건너뛰세요.)

    ```text
    fastapi
    uvicorn
    sqlalchemy
    pydantic
    pillow
    reportlab
    openai
    python-dotenv
    ```

2. **의존성 설치**:

    ```bash
    pip install -r requirements.txt
    ```

  #### 백엔드 환경 변수 설정

1. **`.env` 파일 생성**:

    프로젝트 루트 디렉토리(`backinit/`)에 `.env` 파일을 생성합니다.

    ```bash
    cd backinit
    nano .env
    ```

2. **환경 변수 추가**:

    ```env
    OPENAI_API_KEY="openAI API 키를 여기에 삽입하십시오."
    ```

    > **주의:** `.env` 파일은 민감한 정보를 포함하고 있으므로, 반드시 `.gitignore`에 추가되어 있어야 합니다.

    #### 데이터베이스 초기화
    
    백엔드 서버를 처음 실행하면 데이터베이스 테이블이 자동으로 생성됩니다.
    
    ```bash
    uvicorn app.main:app --reload
    ```
    
    ### 프론트엔드 설치
    
    #### 프론트엔드 필수 사항
    
    - **Node.js (v14 이상)**: [Node.js 공식 사이트](https://nodejs.org/)에서 다운로드 및 설치.
    - **npm**: Node.js 설치 시 기본 포함.
    - **Git**: [Git 공식 사이트](https://git-scm.com/downloads)에서 다운로드 및 설치.
    
    #### 프론트엔드 의존성 설치
    
    1. **프론트엔드 디렉토리로 이동**:
    
        ```bash
        cd backinit/frontend
        ```
    
    2. **의존성 설치**:
    
        ```bash
        npm install
        ```
    
    #### 가상 환경 설정
    
    프론트엔드는 별도의 가상 환경을 사용하지 않지만, 개발 환경을 일관되게 유지하기 위해 일부 설정이 필요할 수 있습니다. 아래는 Windows와 Linux/macOS 환경에서의 설정 방법입니다.
    
    - **Windows**과 **Linux/macOS** 모두 동일한 명령어로 환경을 설정할 수 있습니다.
    
    #### 프론트엔드 개발 서버 실행
    
    개발 중인 프론트엔드를 실행하려면 다음 명령어를 사용합니다:
    
    ```bash
    npm start
    ```
    
    브라우저에서 `http://localhost:3000`으로 접속하여 프론트엔드가 정상적으로 동작하는지 확인합니다.
    
    #### 프로덕션 빌드 생성
    
    배포를 위해 프론트엔드의 프로덕션 빌드를 생성하려면 다음 명령어를 사용합니다:
    
    ```bash
    npm run build
    ```
    
    빌드된 파일은 `frontend/build/` 디렉토리에 생성됩니다. 이 파일들은 Nginx나 다른 웹 서버를 통해 배포할 수 있습니다.
    
    ## 사용 방법
    
    1. **백엔드 서버 실행**:
    
        백엔드 가상 환경을 활성화한 후, 서버를 실행합니다.
    
        ```bash
        cd backinit/app
        # 가상 환경 활성화
        # Windows
        venv\Scripts\activate
        # Linux/macOS
        source venv/bin/activate
        # 서버 실행
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ```
    
    2. **프론트엔드 개발 서버 실행**:
    
        별도의 터미널에서 프론트엔드 디렉토리로 이동하여 개발 서버를 실행합니다.
    
        ```bash
        cd backinit/frontend
        npm start
        ```
    
    3. **애플리케이션 접근**:
    
        브라우저에서 `http://localhost:3000`으로 접속하여 애플리케이션을 사용합니다.
    
    ## 기여 가이드
    
    프로젝트에 기여하고자 하는 분들을 위해 다음 단계를 따라 주세요.
    
    1. **레포지토리 포크(Fork)**:
    
        GitHub에서 이 레포지토리를 포크합니다.
    
    2. **브랜치 생성**:
    
        새로운 기능이나 버그 수정을 위한 브랜치를 생성합니다.
    
        ```bash
        git checkout -b feature/your-feature-name
        ```
    
    3. **변경 사항 커밋**:
    
        변경된 파일을 스테이지에 추가하고 커밋합니다.
    
        ```bash
        git add .
        git commit -m "Add your feature description"
        ```
    
    4. **브랜치 푸시**:
    
        원격 저장소에 브랜치를 푸시합니다.
    
        ```bash
        git push origin feature/your-feature-name
        ```
    
    5. **Pull Request 생성**:
    
        GitHub 레포지토리 페이지에서 `feature/your-feature-name` 브랜치에 대한 Pull Request를 생성합니다.
    
    6. **코드 리뷰 및 병합**:
    
        팀원들이 코드를 리뷰한 후, 승인되면 `main` 브랜치로 병합합니다.
    
    ## 보안 고지
    
    - **민감한 파일 제외**:
      - `.env`는 GitHub에 포함되지 않습니다.
      - `.gitignore`에 이미 추가되어 있으므로, 실수로 커밋되지 않도록 주의하세요.
    
    - **API 키 관리**:
      - `.env` 파일에 저장된 API 키는 외부에 노출되지 않도록 철저히 관리합니다.
      - GitHub에 실수로 커밋되었다면, 즉시 API 키를 재발급 받고 `.env` 파일을 정리해야 합니다.
    
    ## 라이선스
    
    이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.
    
    ## 문의하기
    
    프로젝트에 대한 질문이나 의견이 있으시면 아래 연락처로 문의해 주세요:
    
    - **이메일:** poranara27@gmail.com
    - **GitHub Issues:** [Issues 페이지](https://github.com/rinrinmu/HairWebService/issues)
