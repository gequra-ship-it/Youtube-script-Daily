import os
import time
from datetime import datetime
from google import genai
from googleapiclient.discovery import build

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SAVE_DIR = "./scripts" 

def get_popular_space_topic():
    print("🔍 유튜브 API 연결 확인 중...", flush=True)
    if not YOUTUBE_API_KEY:
        print("❌ 에러: YOUTUBE_API_KEY가 없습니다.", flush=True)
        return None
        
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        search_keyword = "우주 미스터리 OR 제임스 웹 발견 OR black hole discovery"
        request = youtube.search().list(part="snippet", q=search_keyword, type="video", order="viewCount", maxResults=1)
        response = request.execute()
        items = response.get("items", [])
        if not items:
            return None
        video_title = items[0]["snippet"]["title"]
        print(f"✅ 유튜브 참고 영상 찾기 완료: {video_title}", flush=True)
        return video_title
    except Exception as e:
        print(f"❌ 유튜브 검색 중 에러 발생: {e}", flush=True)
        return None

def create_ai_studio_script(youtube_title, client):
    print("🤖 제미나이 대본 기획 시작...", flush=True)
    if not GEMINI_API_KEY:
        return None
        
    # 💡 AI가 절대 헷갈리지 않도록 강력한 지시와 예시를 추가했습니다.
    prompt = f"""
너는 '글로벌 지식 전달'에 특화된 100만 해외 유튜버야.
사용자가 AI 스튜디오를 이용해 정지된 이미지 슬라이드쇼 + 영어 TTS(성우) + 영어 자막 형식의 6분짜리 지식 롱폼 영상을 만들 예정이야.

주제: "{youtube_title}"

[작성 규칙 - 매우 중요!]:
1. [시각 자료]와 [한글 번역]은 반드시 **한국어(Korean)**로 작성해.
2. [영어 자막]과 [영어 TTS]는 반드시 원어민 수준의 자연스러운 **영어(English)**로 작성해야 해!! 절대 한국어로 적지 마.
3. [영어 자막]은 화면 정중앙에 띄울 짧은 영어 문장 1개.
4. [영어 TTS]는 원어민 성우가 15~20초 정도 읽을 분량의 영어 대본.

[출력 양식 예시]:
[영상 제목]: The Secret of the Black Hole / 블랙홀의 비밀

[슬라이드 1]
- 시각 자료: 거대한 블랙홀이 별을 집어삼키는 3D 그래픽 화면
- 영어 자막: The Monster in the Dark
- 영어 TTS: Did you know that there are monsters lurking in the darkness of space? Today, we are diving into the ultimate mystery: Black Holes.
- 한글 번역: 우주의 어둠 속에 괴물이 숨어있다는 사실을 아시나요? 오늘 우리는 궁극의 미스터리, 블랙홀로 빠져들어 봅니다.

위 예시처럼 슬라이드 15~20개 분량의 6분짜리 대본을 작성해줘.
"""
    
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(model='gemini-3.8-flash', contents=prompt)
            print("✅ 대본 생성 성공!", flush=True)
            return response.text
        except Exception as e:
            error_msg = str(e)
            print(f"❌ 제미나이 통신 에러 (시도 {attempt+1}/{max_retries}): {error_msg}", flush=True)
            if "503" in error_msg or "UNAVAILABLE" in error_msg or "429" in error_msg:
                if attempt < max_retries - 1:
                    print("⏳ 구글 서버 과부하입니다. 30초 후 다시 시도합니다...", flush=True)
                    time.sleep(30)
                else:
                    print("⚠ 5번 연속 서버 과부하로 대본 생성을 포기합니다.", flush=True)
            else:
                break
    return None

if __name__ == "__main__":
    print("🚀 클라우드 대본 생성 작업 시작!", flush=True)
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
            
    title = get_popular_space_topic()
    if title:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        script_text = create_ai_studio_script(title, gemini_client)
        
        if script_text:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"script_{current_time}.txt"
            text_file_path = os.path.join(SAVE_DIR, filename)
            
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(f"레퍼런스 주제: {title}\n\n")
                f.write(script_text)
            print(f"🎉 모든 작업 성공! 파일 저장 완료: {text_file_path}", flush=True)
        else:
            print("⚠ 대본 생성 실패로 파일을 저장하지 못했습니다.", flush=True)
