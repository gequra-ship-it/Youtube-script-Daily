import os
import time
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
        
    prompt = f"""
너는 '글로벌 지식 전달'에 특화된 100만 해외 유튜버야.
사용자가 AI 스튜디오를 이용해 정지된 이미지 슬라이드쇼 + 영어 TTS(성우) + 영어 자막 형식의 6분짜리 지식 롱폼 영상을 만들 예정이야.

주제: "{youtube_title}"

[작성 규칙]:
1. 글로벌 시청자를 사로잡을 수 있는 원어민 영어 톤.
2. [시각 자료]: AI 스튜디오에서 어떤 사진을 띄워야 할지 한국어로 지시할 것.
3. [영어 자막]: 화면 정중앙에 띄울 짧은 문장 1개를 영어로 작성.
4. [영어 TTS 대본]: 성우가 15~20초 정도 읽을 분량을 영어로 작성.
5. [한글 번역]: 자막과 TTS 대본의 뜻을 요약한 한글 번역.

출력 양식:
[영상 제목]: (영어 제목) / (한국어 제목)

[슬라이드 1]
- 시각 자료: 
- 영어 자막: 
- 영어 TTS: 
- 한글 번역: 
"""
    
    # 끈기 있는 5회 재시도 로직 유지
    max_retries = 5
    for attempt in range(max_retries):
        try:
            # 구글의 지시에 따라 최신 모델인 3.8-flash로 고정
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
                    print("⚠️️ 5번 연속 서버 과부하로 대본 생성을 포기합니다.", flush=True)
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
            text_file_path = os.path.join(SAVE_DIR, "ai_studio_global_script.txt")
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(f"레퍼런스 주제: {title}\n\n")
                f.write(script_text)
            print(f"🎉 모든 작업 성공! 파일 저장 완료: {text_file_path}", flush=True)
        else:
            print("⚠ 대본 생성 실패로 파일을 저장하지 못했습니다.", flush=True)
