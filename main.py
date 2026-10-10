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
        error_msg = str(e).lower()
        # 💡 유튜브 API 한도 초과 감지 기능 추가
        if "quota" in error_msg or "429" in error_msg or "rate limit" in error_msg:
            print("\n🚨 [경고: 유튜브 API 한도 초과] 하루 무료 검색량(10,000 포인트)을 모두 소진했습니다!", flush=True)
            print("💡 해결책: 한국 시간 매일 오후 4시에 리셋되니 그때 다시 시도하시거나, 구글 콘솔에서 새 API 키를 발급받아 교체하세요.\n", flush=True)
        else:
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
        print("⚠️ 자막 추출 실패 (자막이 없는 영상입니다). 제목만으로 대본을 창작합니다.", flush=True)
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
    print("🤖 제미나이 20분 분량 대본 기획 시작...", flush=True)
    if not GEMINI_API_KEY:
        return None
        
    if transcript_text:
        source_material = f"""
[원본 영상 제목]: "{youtube_title}"
[원본 영상 실제 대본 내용 (이 내용을 완벽히 분석해서 우리만의 20분 대본으로 뼈대에 살을 붙여 길게 재창조할 것)]:
{transcript_text}
"""
    else:
        source_material = f"""
[원본 영상 제목]: "{youtube_title}"
(원본 자막을 구할 수 없습니다. 제목의 핵심 주제를 바탕으로 20분 분량의 깊이 있는 내용을 스스로 길게 창작해 주세요.)
"""

    prompt = f"""
너는 '글로벌 지식 전달'에 특화된 100만 구독자 해외 유튜버야.
사용자가 이 대본을 바탕으로 **20분 길이(영어 단어 수 기준 최소 2,600단어 ~ 3,000단어)의 아주 깊이 있는 지식 롱폼 영상**을 만들 예정이야.

{source_material}

[작성 규칙 - 매우 중요! 절대 어기지 마!]:
1. **분량 강제 (가장 중요)**: 전체 [영어 TTS]의 단어 수를 모두 합쳤을 때 **무조건 2,600단어 이상**이 되어야 해! 내용을 요약하거나 건너뛰지 말고, 원본 자막의 모든 디테일과 예시를 살려서 최대한 길고 상세하게 풀어써.
2. 장면(Scene) 수: 20분 분량을 꽉 채우기 위해 **최소 45개에서 55개의 장면(Scene)**으로 쪼개어 구성해.
3. 각 장면의 대사량: 하나의 [영어 TTS] 블록 안에는 성우가 20초~30초간 쉴 새 없이 읽을 수 있도록 **최소 5문장~8문장 이상(약 60~100단어)**의 아주 풍부한 영어 대사를 작성해. 대충 한두 줄로 넘어가면 절대 안 돼.
4. 타임라인(시간 표시)은 금지. [장면 1], [장면 2] 형식으로 번호만 매겨.
5. [시각 자료]와 [한글 시각자료 내용 번역]은 반드시 **한국어(Korean)**로 작성.
6. [영어 자막]과 [영어 TTS]는 반드시 원어민 수준의 자연스러운 **영어(English)**로 작성. (절대 한국어 섞지 말 것).
7. [영어 자막]은 화면 정중앙에 띄울 짧은 핵심 영어 문장 1개.

[출력 양식 예시]:
[영상 제목]: The Secret of the Black Hole / 블랙홀의 비밀

[장면 1]
- 시각 자료: 거대한 블랙홀이 별을 집어삼키는 3D 그래픽 화면
- 영어 자막: The Monster in the Dark
- 영어 TTS: Did you know that there are monsters lurking in the darkness of space? Today, we are diving into the ultimate mystery: Black Holes. These cosmic giants possess gravitational pulls so strong that not even light can escape their grasp. Imagine a vacuum cleaner large enough to swallow entire star systems whole, leaving absolutely nothing behind. We will explore how they form, where they hide, and what would happen if you were to fall into one.
- 한글 번역: 우주의 어둠 속에 괴물이 숨어있다는 사실을 아시나요? 오늘 우리는 궁극의 미스터리, 블랙홀로 빠져들어 봅니다. 이 우주의 거인들은 빛조차 빠져나갈 수 없을 정도로 강력한 중력을 가지고 있습니다. 별의 무리를 통째로 집어삼키고 아무것도 남기지 않는 거대한 진공청소기를 상상해 보세요. 우리는 이것들이 어떻게 형성되는지, 어디에 숨어 있는지, 그리고 만약 당신이 그 안으로 떨어진다면 어떤 일이 벌어질지 알아볼 것입니다.

위 예시처럼 [영어 TTS] 부분의 분량을 길고 꽉 차게 작성해서, [장면 45] 이상까지 기승전결이 완벽한 2,600단어 이상의 롱폼 대본을 끝까지 출력해줘. 중간에 끊거나 요약하지 마.
"""
    
    max_retries = 5
    for attempt in range(max_retries):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        
        p = multiprocessing.Process(target=fetch_gemini_response, args=(GEMINI_API_KEY, prompt, return_dict))
        p.start()
        
        p.join(300)
        
        if p.is_alive():
            print(f"❌ 제미나이 통신 에러 (시도 {attempt+1}/{max_retries}): 300초 무응답, 연결 강제 절단(Kill)!", flush=True)
            p.terminate()
            p.join() 
            
            if attempt < max_retries - 1:
                print("⏳ 30초 후 다시 시도합니다...", flush=True)
                time.sleep(30)
            else:
                print("⚠ 5번 연속 무응답으로 대본 생성을 포기합니다.", flush=True)
        else:
            status = return_dict.get('status')
            text = return_dict.get('text')
            
            if status == 'SUCCESS':
                print("✅ 20분 분량(2,600단어 이상) 대본 생성 성공!", flush=True)
                return text
            else:
                # 💡 제미나이 API 한도 초과 감지 기능 추가
                error_msg_lower = text.lower()
                if "429" in error_msg_lower or "quota" in error_msg_lower or "resource_exhausted" in error_msg_lower:
                    print(f"\n🚨 [경고: 제미나이 API 한도 초과] (시도 {attempt+1}/{max_retries}) 무료 할당량을 모두 소진했거나 1분당 요청 한도를 넘었습니다!", flush=True)
                    print("💡 해결책: 구글 AI 스튜디오에서 결제 수단(신용카드)을 연동해 제한을 해제하거나, 할당량이 초기화될 때까지 기다리세요.\n", flush=True)
                else:
                    print(f"❌ 제미나이 내부 에러 (시도 {attempt+1}/{max_retries}): {text}", flush=True)
                
                if attempt < max_retries - 1:
                    print("⏳ 30초 후 다시 시도합니다...", flush=True)
                    time.sleep(30)
                else:
                    print("⚠ 5번 연속 에러로 대본 생성을 포기합니다.", flush=True)
                    
    return None

if __name__ == "__main__":
    print("🚀 클라우드 대본 생성 작업 시작!", flush=True)
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
            
    title, video_id = get_unprocessed_top_video()
    
    if title and video_id:
        transcript_text = get_video_transcript(video_id)
        
        script_text = create_ai_studio_script(title, transcript_text)
        
        if script_text:
            current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"script_{current_time}.txt"
            text_file_path = os.path.join(SAVE_DIR, filename)
            
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(f"레퍼런스 주제: {title}\n\n")
                f.write(script_text)
                
            with open(HISTORY_FILE, "a", encoding="utf-8") as f:
                f.write(f"{video_id}\n")
                
            print(f"🎉 모든 작업 성공! 파일 저장 완료: {text_file_path}", flush=True)
        else:
            print("⚠ 대본 생성 실패로 파일을 저장하지 못했습니다.", flush=True)
    else:
         print("⚠ 처리할 영상을 찾지 못해 작업을 종료합니다.", flush=True)
