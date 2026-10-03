import os
import sys
from google import genai
from googleapiclient.discovery import build

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

# GitHub Secrets에서 안전하게 키를 불러옵니다.
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 클라우드 저장소 내부 폴더로 경로 변경
SAVE_DIR = "./scripts" 

def get_popular_space_topic():
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    search_keyword = "우주 미스터리 OR 제임스 웹 발견 OR black hole discovery"
    request = youtube.search().list(part="snippet", q=search_keyword, type="video", order="viewCount", maxResults=1)
    response = request.execute()
    items = response.get("items", [])
    if not items: return None
    return items[0]["snippet"]["title"]

def create_ai_studio_script(youtube_title, client):
    prompt = f"""
너는 '글로벌 지식 전달'에 특화된 100만 해외 유튜버야.
주제: "{youtube_title}"
(이하 기존과 동일한 글로벌 타겟 영어 롱폼 대본 기획 프롬프트)
[영상 제목]: (클릭을 유도하는 영어 제목) / (한국어 제목)
[슬라이드 1]
- 시각 자료: (한국어 지시)
- 영어 자막: (영어 자막)
- 영어 TTS: (영어 대본)
- 한글 번역: (한글 해석)
"""
    try:
        response = client.models.generate_content(model='gemini-3.8-flash', contents=prompt)
        return response.text
    except Exception:
        return None

if __name__ == "__main__":
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
            
    title = get_popular_space_topic()
    if title:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        script_text = create_ai_studio_script(title, gemini_client)
        if script_text:
            text_file_path = os.path.join(SAVE_DIR, "ai_studio_global_script.txt")
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(f"레퍼런스 주제: {title}\n\n")
                f.write(script_text)
