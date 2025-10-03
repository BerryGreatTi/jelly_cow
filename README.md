# Jelly Cow - 투자 분석 에이전트

Jelly Cow는 금융 자산에 대한 포괄적인 보고서를 제공하도록 설계된 AI 기반 투자 분석 에이전트입니다. 기본적 분석, 기술적 분석, 뉴스 분석을 수행하기 위해 전문화된 AI 에이전트로 구성된 계층적 팀을 사용하며, 종합된 보고서를 Slack을 통해 전달합니다.

## 주요 기능

- **Slack 연동**: Slack 워크스페이스 내에서 DM이나 멘션을 통해 에이전트와 직접 상호작용할 수 있습니다.
- **계층적 에이전트 팀**: 루트 에이전트가 전문가 팀에게 작업을 위임합니다:
    - **기본적 분석가**: 재무 건전성 및 가치 평가를 담당합니다.
    - **기술적 분석가**: 차트 패턴과 시장 지표를 분석합니다.
    - **뉴스 분석가**: 최신 뉴스와 시장 심리를 수집하고 분석합니다.
- **확장 가능한 아키텍처**: 새로운 분석 도구나 데이터 소스(예: 한국투자증권 API 클라이언트 포함)를 쉽게 추가할 수 있습니다.
- **비동기 처리**: FastAPI와 asyncio로 구축되어 여러 요청을 효율적으로 처리합니다.

## 아키텍처

이 애플리케이션은 들어오는 Slack 이벤트를 처리하기 위해 FastAPI 서버를 실행하는 `app.py`에 의해 조율됩니다. `slack_bolt`의 `AsyncSlackRequestHandler`는 요청을 `apis/slack.py`의 에이전트 핸들러로 라우팅합니다.

사용자가 쿼리를 보내면 `slack.py`는 `root_agent`(`JellyMonsterRootAgent`)를 호출합니다. 이 루트 에이전트는 Google ADK 프레임워크를 사용하여 하위 에이전트(`fundamental_analyzer`, `technical_analyzer`, `news_analyzer`)를 조율하여 통찰력을 수집합니다. 마지막으로 정보를 단일의 일관된 보고서로 종합하여 원래 Slack 스레드에 다시 게시합니다.

## 시작하기

### 사전 요구 사항

- Python 3.12 이상
- Slack 워크스페이스 및 API 토큰
- API 키를 위한 환경 변수 (`.env_template` 참조)

### 설치

1.  **리포지토리 클론:**
    ```bash
    git clone <repository-url>
    cd jelly_cow
    ```

2.  **의존성 설치:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **환경 변수 설정:**
    - `.env_template` 파일을 `.env`라는 새 파일로 복사합니다.
    - 필요한 Slack 봇 토큰, 서명 비밀 및 기타 API 키 값을 입력합니다.

### 사용법

1.  **애플리케이션 실행:**
    ```bash
    python app.py
    ```
    FastAPI 서버가 `http://0.0.0.0:3000`에서 시작됩니다.

2.  **Slack에서 봇과 상호작용:**
    - 분석하려는 주식이나 자산의 이름으로 봇에게 다이렉트 메시지를 보냅니다 (예: "Apple").
    - 채널에서 봇을 멘션합니다 (예: "@JellyCow Tesla 분석해줘").

    봇은 :thinking_face: 이모티콘으로 요청을 확인하고 분석을 수행한 후 스레드에 최종 보고서를 게시합니다.