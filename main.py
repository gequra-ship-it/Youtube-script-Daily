import os
import time
import multiprocessing
from datetime import datetime
from google import genai
from googleapiclient.discovery import build

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
            print("❌ 과학드림 채널을 찾을 수 없습니다.", flush=True)
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

# 💡 '복제 인간'이 실행할 완전히 독립된 작업 지시서
def fetch_gemini_response(api_key, prompt, return_dict):
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model='gemini-3.8-flash', contents=prompt)
        return_dict['status'] = 'SUCCESS'
        return_dict['text'] = response.text
    except Exception as e:
        return_dict['status'] = 'ERROR'
        return_dict['text'] = str(e)

def create_ai_studio_script(youtube_title):
    print("🤖 제미나이 대본 기획 시작...", flush=True)
    if not GEMINI_API_KEY:
        return None
        
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
        # 복제 인간(Process)과 결과를 주고받을 특수 메모장
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        
        # 독립된 프로세스(가상 컴퓨터) 생성 및 시작
        p = multiprocessing.Process(target=fetch_gemini_response, args=(GEMINI_API_KEY, prompt, return_dict))
        p.start()
        
        # 💡 타이머 시작: 정확히 120초만 칼같이 기다립니다.
        p.join(120)
        
        # 120초가 지났는데도 프로세스가 살아있다? -> 즉시 강제 사살(Terminate)
        if p.is_alive():
            print(f"❌ 제미나이 통신 에러 (시도 {attempt+1}/{max_retries}): 120초 무응답, 연결 강제 절단(Kill)!", flush=True)
            p.terminate()
            p.join() # 시체(좀비 메모리) 정리
            
            if attempt < max_retries - 1:
                print("⏳ 30초 후 다시 시도합니다...", flush=True)
                time.sleep(30)
            else:
                print("⚠ 5번 연속 무응답으로 대본 생성을 포기합니다.", flush=True)
        else:
            # 120초 안에 정상적으로 처리가 완료된 경우
            status = return_dict.get('status')
            text = return_dict.get('text')
            
            if status == 'SUCCESS':
                print("✅ 대본 생성 성공!", flush=True)
                return text
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
        script_text = create_ai_studio_script(title)
        
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
