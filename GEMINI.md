# Gemini Context: 비즈톤 변환기

## 프로젝트 개요

"비즈톤 변환기" 프로젝트는 일상적인 언어를 전문적인 비즈니스 말투로 변환하는 데 도움을 주기 위해 설계된 AI 기반 웹 애플리케이션입니다. 이 솔루션은 공식적인 의사소통에 어려움을 겪을 수 있는 신입 사원이나 비원어민을 대상으로 합니다.

이 애플리케이션은 사용자가 텍스트를 입력하고, 대상(상사, 동료, 고객)을 선택하면 해당 대상에 적합하게 재구성된 텍스트를 받을 수 있는 간단하고 직관적인 인터페이스를 제공합니다.

**주요 기술:**

*   **백엔드**: **Flask** 프레임워크를 사용하는 Python 기반 웹 서버입니다. 프론트엔드를 제공하고, API 요청을 처리하며, Groq AI 서비스와 통합됩니다.
*   **프론트엔드**: 바닐라 **HTML, CSS, JavaScript**로 구축된 단일 페이지 애플리케이션입니다. 스타일링을 위해 **Tailwind CSS** (CDN을 통해)를 사용합니다.
*   **AI 서비스**: **Groq AI** (`moonshotai/kimi-k2-instruct-0905` 모델)가 자연어 변환에 사용됩니다.

**아키텍처:**

프로젝트는 프론트엔드와 백엔드 간의 명확한 분리를 따릅니다:
*   `frontend/` 디렉토리에는 모든 클라이언트 측 파일(`index.html`, `js/script.js`)이 포함됩니다.
*   `backend/` 디렉토리에는 Flask 서버(`app.py`)와 그 종속성(`requirements.txt`)이 포함됩니다.
*   Flask 서버는 정적 프론트엔드 파일을 제공하고 톤 변환 로직을 위한 `/api/convert` 엔드포인트를 제공하는 역할을 모두 수행합니다.

## 빌드 및 실행

### 1. 백엔드 설정

1.  **프로젝트 루트 디렉토리로 이동합니다.**

2.  **Python 가상 환경을 생성합니다:**
    ```bash
    python -m venv .venv
    ```

3.  **가상 환경을 활성화합니다:**
    *   Windows:
        ```bash
        .\.venv\Scripts\activate
        ```
    *   macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```

4.  **종속성을 설치합니다:**
    ```bash
    pip install -r backend/requirements.txt
    ```

5.  **환경 변수 설정:**
    *   프로젝트 루트 디렉토리에 `.env`라는 파일을 생성합니다.
    *   파일에 Groq API 키를 다음과 같이 추가합니다:
        ```
        GROQ_API_KEY="your_actual_api_key_here"
        ```
    *   이 파일은 `.gitignore`에 등록되어 버전 제어에 커밋되지 않습니다.

### 2. 애플리케이션 실행

1.  **백엔드 서버를 시작합니다:**
    ```bash
    python backend/app.py
    ```
2.  **프론트엔드에 접속합니다:**
    *   웹 브라우저를 열고 `http://127.0.0.1:5000`으로 이동합니다.

Flask 서버는 `index.html` 파일을 제공하고 프론트엔드에서 이루어지는 API 호출을 처리합니다.

## 개발 규칙

*   **API 엔드포인트**: 주 API 엔드포인트는 `POST /api/convert`입니다. 이는 `text` (원본 텍스트) 및 `target` (`upward`, `lateral`, `external`)를 포함하는 JSON 페이로드를 예상하며, 변환된 텍스트를 반환합니다.
*   **구성**: 백엔드는 `python-dotenv`를 사용하여 `.env` 파일에서 `GROQ_API_KEY`를 로드합니다.
*   **로깅**: Flask 앱은 표준 `logging` 모듈을 사용하여 서버 이벤트, API 호출 및 오류를 로깅합니다.
*   **프론트엔드 로직**: 모든 프론트엔드 상호 작용은 `frontend/js/script.js`에서 처리됩니다. 비동기 호출을 위해 `fetch` API를 사용합니다.
*   **스타일링**: UI는 `frontend/index.html`에서 직접 Tailwind CSS 유틸리티 클래스를 사용하여 스타일링됩니다. 로컬 CSS 파일은 없습니다.