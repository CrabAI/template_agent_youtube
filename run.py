import os
from dotenv import load_dotenv
from openai import OpenAI

# =========================
# 0) 기본 설정
# =========================
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY가 .env에 없습니다. .env 파일을 확인해주세요.")

client = OpenAI(api_key=api_key)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_PATH = os.path.join(BASE_DIR, "input.txt")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "youtube_description.txt")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================
# 1) 크랩 유튜브 설명글 템플릿(참고용)
#    - 모델에게는 '참고'로만 제공
#    - 출력에는 절대 그대로 포함하지 않게 지시
# =========================
YOUTUBE_TEMPLATE = """오늘 영상은
클로드봇 같은 완성형 사례가 아니라
직접 로컬 에이전트를 만들어보는 실전편입니다.

input 폴더에 파일을 넣으면
GPT가 자동으로 요약하고
output 폴더에 결과 파일을 생성합니다.

중요한 건 기능이 아니라 구조입니다.
GPT와 대화하는 것이 아니라
GPT를 업무 흐름 안에 붙이는 방법을 보여드립니다.

🎁 노션 작업노트 링크 (✨전체 코드 제공)
https://www.notion.so/30c87e39e7c480abb956c2e0b425e2fc?pvs=21

✅ 이런 분들께 추천합니다
• 로컬 에이전트를 직접 만들어보고 싶은 분
• API 기반 자동화가 실제로 어떻게 돌아가는지 궁금한 분
• GPT를 단순 대화 도구 이상으로 쓰고 싶은 분
• AI 자동화 구조를 이해하고 싶은 분

✅ 오늘 영상에서 다루는 내용
• 로컬 에이전트 기본 구조 이해
• input / output 폴더 기반 자동 요약 구조
• gpt-3.5-turbo를 활용한 가벼운 실습
• “모델이 아니라 구조”라는 핵심 개념

✅ 크랩(Crab) 채널 미션
• 어렵지 않게, 일에 바로 쓰는 AI.
• 매주 실전 / 개념 / 인사이트로 한 문제씩 함께 해결합니다.

💌 문의
• info@creativeflow.co.kr
"""

SYSTEM = (
    "너는 유튜브 설명글을 작성하는 실무 보조자다. "
    "사용자가 준 템플릿은 '참고용'이며, 템플릿 원문을 그대로 복사해 출력하면 안 된다. "
    "최종 출력은 항상 '완성된 설명글' 한 덩어리만 내보낸다. "
    "한국어로, 과장/낚시 없이, 자연스럽고 읽기 좋게 작성한다."
)

def build_prompt(video_source_text: str) -> str:
    return f"""
아래 [템플릿]을 참고해서, 같은 구조와 톤으로 '완성된 유튜브 설명글'을 작성해줘.

요구사항:
1) 첫번째 단락에는 이번 영상 내용을 구체적으로 3~6줄로 써줘. (템플릿 '오늘 영상은' 부분을 이번 영상에 맞게 새롭게 작성)
2) 두번째 단락 앞에는 ✅를 붙이고, '이런 분들께 추천합니다' 부분을 이번 영상에 맞게 새롭게 작성. (추천 대상은 4~6개 정도)
3) 세번째 단락 앞에도 ✅를 붙이고, '오늘 영상에서 다루는 내용' 부분을 이번 영상에 맞게 새롭게 작성. (다루는 내용은 4~6개 정도)
4) 네번째 단락 앞에도 ✅를 붙이고, '크랩(Crab) 채널 미션' 부분을 템플릿과 동일하게 작성해줘.
5) 다섯번째 단락 앞에는 💌를 붙이고, '문의' 부분을 템플릿과 동일하게 작성해줘.
6) 맨 마지막에 해시태그를 한 줄로 추가해 (#으로 시작, 15~25개).
7) 출력에는 라벨([FINAL] 등) 붙이지 말고, '최종 설명글'만 출력해.

[템플릿(참고용)]
{YOUTUBE_TEMPLATE}

[이번 영상 내용]
{video_source_text}
""".strip()

def generate_description(video_source_text: str) -> str:
    prompt = build_prompt(video_source_text)

    resp = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
    )

    output = resp.choices[0].message.content.strip()

    # =========================
    # 2) 안전장치:
    # 혹시라도 템플릿 원문이 그대로 섞여 나오면 제거
    # (초급용: 단순 replace)
    # =========================
    template_clean = YOUTUBE_TEMPLATE.strip()
    if template_clean and template_clean in output:
        output = output.replace(template_clean, "").strip()

    # 아주 드물게 템플릿 일부 블록이 통째로 포함될 수 있어,
    # 특정 헤더가 연속으로 등장하면 앞쪽을 정리하는 간단한 방어
    # (원치 않으면 삭제하셔도 됩니다)
    while "\n\n\n" in output:
        output = output.replace("\n\n\n", "\n\n")

    return output

def main():
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"input.txt가 없습니다: {INPUT_PATH}")

    with open(INPUT_PATH, "r", encoding="utf-8") as f:
        video_text = f.read().strip()

    if not video_text:
        raise ValueError("input.txt 내용이 비어있습니다. 영상 요약/메모를 넣어주세요.")

    final_text = generate_description(video_text)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(final_text)

    print(f"✅ 생성 완료: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()