import os
from google import genai
from googleapiclient.discovery import build

# 깃허브 시크릿(Secrets)에서 안전하게 키를 불러옵니다.
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SAVE_DIR = "./scripts" 

def get_popular_space_topic():
    print("🔍 유튜브 API 연결 확인 중...", flush=True)
    if not YOUTUBE_API_KEY:
        print("❌ 에러: YOUTUBE_API_KEY가 없습니다. 깃허브 Secrets 설정을 확인해주세요.", flush=True)
        return None
        
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        search_keyword = "우주 미스터리 OR 제임스 웹 발견 OR black hole discovery"
        request = youtube.search().list(part="snippet", q=search_keyword, type="video", order="viewCount", maxResults=1)
        response = request.execute()
        items = response.get("items", [])
        if not items:
            print("❌ 유튜브 영상을 찾지 못했습니다.", flush=True)
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
        print("❌ 에러: GEMINI_API_KEY가 없습니다. 깃허브 Secrets 설정을 확인해주세요.", flush=True)
        return None
        
    prompt = f"""
너는 '글로벌 지식 전달'에 특화된 100만 해외 유튜버야.
사용자가 AI 스튜디오를 이용해 **정지된 이미지 슬라이드쇼 + 영어 TTS(성우) + 영어 자막** 형식의 6분짜리 지식 롱폼 영상을 만들 예정이야.

주제: "{youtube_title}"

이 영상은 전 세계 시청자를 대상으로 하며, '깊이 있는 정보'와 '몰입감 있는 스토리텔링'으로 승부해야 해.
영상 제작 툴에 바로 복사/붙여넣기 할 수 있도록, 전체 6분 분량을 약 15~20개의 슬라이드(장면)로 쪼개서 대본을 작성해 줘.

[작성 규칙]:
1. [말투]: 글로벌 시청자를 사로잡을 수 있는 흥미롭고 지적인 원어민 영어 톤 (예: "Did you know that...?", "The mind-blowing fact here is...")
2. [시각 자료]: AI 스튜디오에서 어떤 사진을 띄워야 할지 제작자가 알아보기 쉽게 **한국어**로 지시할 것.
3. [영어 자막]: 화면 정중앙에 띄울 핵심 키워드나 짧은 문장 1개를 **영어**로 작성.
4. [영어 TTS 대본]: 영어 원어민 성우가 15~20초 정도 읽을 분량의 흥미로운 지식 전달 텍스트를 **영어**로 작성.
5. [한글 번역]: 한국인 제작자가 내용을 완벽히 이해할 수 있도록 자막과 TTS 대본의 뜻을 요약한 한글 번역을 덧붙일 것.
6. 출력 형식은 반드시 아래 양식을 따를 것:

[영상 제목]: (클릭을 유도하는 영어 제목) / (한국어 제목)

[슬라이드 1]
- 시각 자료: (한국어 지시)
- 영어 자막: (영어 자막)
- 영어 TTS: (영어 대본)
- 한글 번역: (한글 해석)
"""
    try:
        response = client.models.generate_content(model='gemini-3.8-flash', contents=prompt)
        print("✅ 대본 생성 성공!", flush=True)
        return response.text
    except Exception as e:
        print(f"❌ 제미나이 통신 중 에러 발생: {e}", flush=True)
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
            print("⚠️ 대본 생성 실패로 파일을 저장하지 못했습니다.", flush=True)
    else:
        print("⚠️ 주제 검색 실패로 작업을 종료합니다.", flush=True)
