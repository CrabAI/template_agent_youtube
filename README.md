# template_agent_youtube

> GPT를 활용해 유튜브 설명글을 자동 생성하는 로컬 에이전트 템플릿

---

## 개요

`input.txt`에 영상 내용을 넣으면, GPT가 자동으로 완성된 유튜브 설명글을 생성해 `output/` 폴더에 저장합니다.

단순 대화형 GPT 사용이 아닌, **GPT를 업무 흐름 안에 붙이는 구조**를 익히는 실전 템플릿입니다.

```
input.txt  →  [run.py + GPT API]  →  output/youtube_description.txt
```

---

## 구조

```
template_agent_youtube/
├── run.py               # 메인 에이전트 스크립트
├── input.txt            # 영상 요약/메모 입력 파일
├── output/              # 생성된 설명글 저장 폴더
├── requirements.txt     # 의존성 패키지
├── .env.example         # 환경변수 템플릿 (복사해서 .env로 사용)
└── .gitignore
```

---

## 시작하기

### 1. 패키지 설치

```bash
python3 -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일을 열고 실제 API 키를 입력:

```
OPENAI_API_KEY=sk-proj-여기에_실제_API_키_입력
```

> API 키는 [OpenAI Platform](https://platform.openai.com/api-keys)에서 발급받으세요.

### 3. 입력 파일 작성

`input.txt`에 영상 내용을 작성합니다. (요약, 메모, 스크립트 등 자유 형식)

```
오늘 영상은 로컬 에이전트를 만드는 방법에 대해 다룹니다.
input 폴더에 파일을 넣으면 GPT가 자동으로 처리합니다.
...
```

### 4. 실행

```bash
python run.py
```

결과물은 `output/youtube_description.txt`에 저장됩니다.

---

## 출력 예시

```
오늘 영상은
로컬 에이전트를 직접 만들어보는 실전 편입니다.
...

✅ 이런 분들께 추천합니다
• API 기반 자동화가 궁금한 분
...

#유튜브자동화 #GPT활용 #로컬에이전트 ...
```

---

## 보안 주의사항

- `.env` 파일은 **절대 커밋하지 마세요** — `.gitignore`에 포함되어 있습니다.
- API 키가 외부에 노출된 경우, 즉시 [OpenAI Platform](https://platform.openai.com/api-keys)에서 키를 재발급하세요.

---

## 관련 채널

**크랩(Crab)** — 어렵지 않게, 일에 바로 쓰는 AI.
매주 실전 / 개념 / 인사이트로 한 문제씩 함께 해결합니다.

📩 info@creativeflow.co.kr
