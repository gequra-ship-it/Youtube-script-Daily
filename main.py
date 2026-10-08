import os
import time
import multiprocessing
from datetime import datetime
from google import genai
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SAVE_DIR = "./scripts" 
HISTORY_FILE = os.path.join(SAVE_DIR, "history.txt")

def get_unprocessed_top_video():
    print("🔍 유튜브 API 연결 및 채널 검색 중...", flush=True)
    if not YOUTUBE_API_KEY:
        print("❌ 에러: YOUTUBE_API_KEY가 없습니다.", flush=True)
        return None, None
        
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        
        channel_request = youtube.search().list(
            part="id", q="@sciencedream", type="channel", maxResults=1
        )
        channel_response = channel_request.execute()
        
        if not channel_response.get("items"):
            print("❌ 채널을 찾을 수 없습니다.", flush=True)
            return None, None
            
        channel_id = channel_response["items"][0]["id"]["channelId"]
        
        processed_videos = []
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                processed_videos = f.read().splitlines()
        
        video_request = youtube.search().list(
            part="snippet", channelId=channel_id, type="video", order="viewCount", maxResults=50
        )
        video_response = video_request.execute()
        
        for item in video_response.get("items", []):
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"]
            
            if video_id not in processed_videos:
                print(f"✅ 새로운 타겟 영상 발견: {video_title}", flush=True)
                return video_title, video_id
                
        print("⚠️ 상위 50개 영상을 모두 처리했습니다!", flush=True)
        return None, None
        
    except Exception as e:
        print(f"❌ 유튜브 검색 중 에러 발생: {e}", flush=True)
        return None, None

def get_video_transcript(video_id):
    print("📜 원본 유튜브 영상 자막 추출 시도 중...", flush=True)
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en', 'ja'])
        text = " ".join([t['text'] for t in transcript_list])
        print("✅ 원본 자막 추출 성공! (이 내용을 바탕으로 대본을 씁니다)", flush=True)
        return text
    except Exception as e:
        print(f"⚠️ 자막 추출 실패 (자막이 없는 영상입니다). 제목만으로 대본을 창작합니다.", flush=True)
        return None

def fetch_gemini_response(api_key, prompt, return_dict):
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model='gemini-3.8-flash', contents=prompt)
        return_dict['status'] = 'SUCCESS'
        return_dict['text'] = response.text
    except Exception as e:
        return_dict['status'] = 'ERROR'
        return_dict['text'] = str(e)

def create_ai_studio_script(youtube_title, transcript_text):
    print("🤖 제미나이 15분 분량 대본 기획 시작...", flush=True)
    if not GEMINI_API_KEY:
        return None
        
    if transcript_text:
        source_material = f"""
[원본 영상 제목]: "{youtube_title}"
[원본 영상 실제 대본 내용 (이 내용을 완벽히 분석해서 우리만의 15분 대본으로 뼈대에 살을 붙여 길게 재창조할 것)]:
{transcript_text}
"""
    else:
        source_material = f"""
[원본 영상 제목]: "{youtube_title}"
(원본 자막을 구할 수 없습니다. 제목의 핵심 주제를 바탕으로 10분~15분 분량의 깊이 있는 내용을 스스로 길게 창작해 주세요.)
"""

    # 💡 1,500단어 이상 롱폼 생성을 강제하기 위한 매우 디테일한 프롬프트
    prompt = f"""
너는 '글로벌 지식 전달'에 특화된 100만 구독자 해외 유튜버야.
사용자가 이 대본을 바탕으로 **10분에서 15분 길이(영어 단어 수 기준 최소 1,500단어 ~ 2,250단어)의 아주 깊이 있는 지식 롱폼 영상**을 만들 예정이야.

{source_material}

[작성 규칙 - 매우 중요! 절대 어기지 마!]:
1. **분량 강제 (가장 중요)**: 전체 [영어 TTS]의 단어 수를 모두 합쳤을 때 **무조건 1,500단어 이상**이 되어야 해! 내용을 요약하거나 건너뛰지 말고, 원본 자막의 모든 디테일과 예시를 살려서 최대한 길고 상세하게 풀어써.
2. 장면(Scene) 수: 15분 분량을 꽉 채우기 위해 **최소 30개에서 40개의 장면(Scene)**으로 쪼개어 구성해.
3. 각 장면의 대사량: 하나의 [영어 TTS] 블록 안에는 성우가 20초~30초간 쉴 새 없이 읽을 수 있도록 **최소 5문장~8문장 이상(약 60~100단어)**의 아주 풍부한 영어 대사를 작성해. 대충 한두 줄로 넘어가면 절대 안 돼.
4. 타임라인(시간 표시)은 금지. [장면 1], [장면 2] 형식으로 번호만 매겨.
5. [시각 자료]와 [한글 번역]은 반드시 **한국어(Korean)**로 작성.
6. [영어 자막]과 [영어 TTS]는 반드시 원어민 수준의 자연스러운 **영어(English)**로 작성. (절대 한국어 섞지 말 것).
7. [영어 자막]은 화면 정중앙에 띄울 짧은 핵심 영어 문장 1개.

[출력 양식 예시]:
[영상 제목]: The Secret of the Black Hole / 블랙홀의 비밀

[장면 1]
- 시각 자료: 거대한 블랙홀이 별을 집어삼키는 3D 그래픽 화면
- 영어 자막: The Monster in the Dark
- 영어 TTS: Did you know that there are monsters lurking in the darkness of space? Today, we
