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

def count_narration_words(script_text):
    """[1부] TTS 입력용 전문의 영어 단어 수를 센다."""
    try:
        start = script_text.index("=== 1부")
        body = script_text[start:].split("\n", 1)[1]
        end = body.find("\n=== ")
        if end != -1:
            body = body[:end]
        return len(body.split())
    except (ValueError, IndexError):
        return None

def log_word_count(script_text, low, high):
    words = count_narration_words(script_text)
    if words is None:
        print("⚠️ [1부] 구분선을 찾지 못했습니다. 출력 양식이 지침서와 다를 수 있습니다.", flush=True)
    elif low and words < low:
        print(f"⚠️ [1부] 영어 단어 수 {words}개: 목표 하한 {low}단어보다 짧습니다.", flush=True)
    elif high and words > high:
        print(f"⚠️ [1부] 영어 단어 수 {words}개: 목표 상한 {high}단어를 넘었습니다.", flush=True)
    else:
        print(f"📊 [1부] 영어 단어 수 {words}개 (Kokoro 약 163단어/분 기준 약 {words/163:.1f}분)", flush=True)

def create_ai_studio_script(youtube_title, transcript_text):
    print("🤖 제미나이 영어 내레이션 대본 기획 시작...", flush=True)
    if not GEMINI_API_KEY:
        return None
        
    if transcript_text:
        source_material = f"""
[원본 영상 제목]: "{youtube_title}"
[원본 영상 실제 대본 내용 (이 내용에 있는 사실만 근거로 삼아 우리만의 영어 내레이션으로 재구성할 것)]:
{transcript_text}
"""
    else:
        source_material = f"""
[원본 영상 제목]: "{youtube_title}"
(원본 자막을 구할 수 없습니다. 제목의 핵심 주제를 바탕으로 쓰되, 확실히 아는 일반 지식만 사용하고 구체적인 숫자·연도·인명·연구는 지어내지 마세요. 확신이 없는 내용은 B등급(가설 표현)으로만 쓰세요.)
"""

    prompt = f"""
너는 'Miya's Lab' 채널의 영어 내레이션 작가야. 글로벌 시청자에게 지식을 차분하고 깊이 있게 전달하는 롱폼 영상의 **영어 내레이션 대본**을 쓴다. 이 대본은 그대로 TTS 음성과 그림 영상으로 만들어질 예정이야.

{source_material}

[작성 규칙 - 지침서 기준, 절대 어기지 마!]:
1. **언어**: 영상에 들리고 보이는 것은 전부 영어야. [1부]는 영어 내레이션만 쓰고 한글, 이모지, 괄호 연출 메모, 타임코드, 장면 번호를 절대 넣지 마(TTS에 그대로 붙여 넣을 글이야). 원본이 한국어·일본어여도 자연스러운 영어로 옮겨 써. 숫자·단위·날짜는 영어 표기(예: "2.461 billion years ago", "380,000 km").
2. **분량**: [1부] 영어 단어 수는 **약 3,100단어(허용 2,900~3,300단어)**로 맞춰. (Kokoro TTS가 분당 약 163단어로 읽으므로 영상 약 18~21분이 돼.) 2,900단어에 못 미치면 구체적인 장면 묘사, 원리 설명, 일상 비유, **원본에 있는 사례**로 보강하고, 3,300단어를 넘으면 반복과 곁가지를 덜어내. 원본 자막이 있으면 원본의 디테일과 예시를 최대한 살려.
3. **문단 = 장면 하나**: [1부]는 문단마다 빈 줄로 구분해. 한 문단은 대본의 의미 단위 하나이고, 성우가 7초 안에 읽을 수 있게 **문장 하나(길어도 약 19단어 이하), 짧은 문장이면 두 개까지**만 써. 문장은 짧게(평균 15단어 안팎), 평서문과 의문문을 섞어.
4. **말투**: 한 사람에게 이야기하듯 따뜻하고 공손한 대화체. 시청자를 "you"로 부르고 축약형(it's, don't)을 써도 돼. 수사 의문문은 영상 전체에서 8~18개.
5. **구성**: ① 처음 5분은 설명보다 끌어당김이 먼저야: 시청자에게 던지는 질문 / "만약 ~라면?" 가정 상황(가정임을 밝히고 수치는 A등급만) / 친숙한 영화 장면(영화의 실제 내용만, 확인 못 하면 쓰지 말고 질문·가정으로 대체) 중에서 소재에 맞게 골라 섞어 시작하고, 답을 바로 주지 말고 궁금증을 유지한 채 1~2분 안에 본론으로 이어가. 처음 60초 훅은 일상적인 감각("Take a look at your fingernails.") / 의외의 숫자나 사실 / 뒤집기 / 핵심 질문 / 출발 선언 중에서 골라 시작해. ② 본문은 구체적인 장면 묘사로 열고, 원리를 설명하고, 일상 비유를 들어. ③ 도입과 결말에 현대인의 일상 장면을 넣어. ④ 결말은 시청자의 현재로 돌아와 감성적으로 정리하고, 마지막에 주제에 맞는 은유로 구독을 부탁해. 채널은 "Miya's Lab" 또는 "this lab"이라고 부르고(철자 그대로), '서재(library)'라는 표현과 원본 채널 이름은 절대 쓰지 마.
6. **사실 확인 (지어내기 금지)**: 존재하지 않는 사례·연구·숫자·인용·인물을 절대 만들지 마. 자극적으로 만드는 방법은 오직 '사실의 배열'(가장 놀라운 확인된 사실을 앞에, 반전은 확인된 사실로, 질문과 긴장감 있는 문장)이야. 모든 사실 주장을 아래 등급으로 나눠서 처리해:
   - A: 아래 원본에 사실로 적혀 있는 내용 → 단정해서 써.
   - B: 원본이 가설·추정·"의심된다"로 말한 내용, 또는 원본에는 없고 네 배경지식으로만 아는 내용 → "scientists suspect…", "one hypothesis is…"처럼 가설임을 밝혀서만 써. 구체적인 숫자·연도·인명·논문은 쓰지 마.
   - C: 근거를 모르는 주장 → 쓰지 마. 모른다는 사실 자체가 확실할 때만 "No one knows for sure" 같은 미스터리 훅으로 바꿔.
   - D: 원본이나 확실한 지식과 모순되는 틀린 주장 → 반드시 고쳐서 써.
   등급이 애매하면 한 단계 보수적으로(A가 아니라 B로) 처리해. 너는 인터넷 검색을 할 수 없으니 네가 직접 확인했다고 말하지 마.

[출력 양식 - 이 구조와 구분선을 정확히 지켜]:
[영상 제목]: <영어 Title Case, 70자 이하, 이모지 없음, 전부 대문자 금지, 영상에 없는 내용을 약속하지 않기>

=== 1부: TTS 입력용 전문 ===
<영어 내레이션 문단들, 문단 사이 빈 줄>

=== 2부: 사실 확인 표 (한국어) ===
| 항목 | 원문(또는 요지) | 등급(A~D) | 처리·근거 |
|---|---|---|---|
<대본에 쓴 주요 사실 주장을 전부 한 줄씩. B등급·D등급 처리를 반영한 항목은 처리 칸에 표시>

=== 3부: 숏츠 대본 2편 ===
[숏츠 1] 제목: <영어, Title Case>
<영어 내레이션 약 150단어(140~160단어). 1부와 겹치지 않는 구간에서 가장 흥미로운 부분을 골라, 질문이나 의외의 사실로 시작해 첫 2초 안에 훅을 던지고, 마지막 한 줄은 본편을 보게 만드는 문장. 1부에 있는 사실만 사용>

[숏츠 2] 제목: <영어, Title Case, 숏츠 1과 소재·훅이 겹치지 않게>
<같은 규칙의 영어 내레이션 약 150단어>

위 구조로 [1부]를 중간에 끊거나 요약하지 말고 끝까지 출력해줘. 2부와 3부까지 빠짐없이 출력해.
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
                print("✅ 대본 생성 성공!", flush=True)
                log_word_count(text, 2900, 3300)
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
