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
        
        # 💡 타겟 채널 변경: @sciencedream -> @이과형
        channel_request = youtube.search().list(
            part="id", q="@이과형", type="channel", maxResults=1
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
        if "quota" in error_msg or "429" in error_msg or "rate limit" in error_msg:
            print("\n🚨 [경고: 유튜브 API 한도 초과] 하루 무료 검색량(10,000 포인트)을 모두 소진했습니다!", flush=True)
            print("💡 해결책: 한국 시간 매일 오후 4시에 리셋되니 그때 다시 시도하시거나, 구글 콘솔에서 새 API 키를 발급받아 교체하세요.\n", flush=True)
        else:
            print(f"❌ 유튜브 검색 중 에러 발생: {e}", flush=True)
        return None, None

CAPTION_LANGS = ['ko', 'en', 'ja']
TRANSCRIPT_SOURCE = None  # "captions" | "auto" | None(제목)

def fetch_caption_segments(video_id):
    """자막 → 유튜브 자동 생성 자막 → None(제목) 순으로 찾는다. (segments, source) 반환.
    segments는 {'text', 'start', 'duration'} dict 리스트."""
    try:
        ytt = YouTubeTranscriptApi()
        tl = ytt.list(video_id)
    except AttributeError:
        try:
            return YouTubeTranscriptApi.get_transcript(video_id, languages=CAPTION_LANGS), "captions"
        except Exception as e:
            print(f"⚠️ 자막 목록 조회 실패 ({type(e).__name__}).", flush=True)
            return None, None
    except Exception as e:
        print(f"⚠️ 자막 목록 조회 실패 ({type(e).__name__}: {(str(e).strip().splitlines() or [''])[0][:150]}).", flush=True)
        return None, None

    transcripts = list(tl)
    steps = [
        ("captions", "업로더 자막", lambda: tl.find_manually_created_transcript(CAPTION_LANGS),
         [t for t in transcripts if not t.is_generated]),
        ("auto", "유튜브 자동 생성 자막", lambda: tl.find_generated_transcript(CAPTION_LANGS),
         [t for t in transcripts if t.is_generated]),
    ]
    for source, label, find_preferred, others in steps:
        candidates = []
        try:
            candidates.append(find_preferred())
        except Exception:
            pass
        candidates += [t for t in others if t not in candidates]
        for t in candidates:
            try:
                segments = t.fetch().to_raw_data()
            except Exception as e:
                print(f"⚠️ {label}({t.language_code}) 내려받기 실패 ({type(e).__name__}).", flush=True)
                continue
            if segments:
                print(f"✅ {label} 사용 (언어: {t.language_code}, {len(segments)}줄)", flush=True)
                return segments, source
        print(f"ℹ️ {label} 없음.", flush=True)
    return None, None

def get_video_transcript(video_id):
    global TRANSCRIPT_SOURCE
    print("📜 원본 유튜브 영상 자막 추출 시도 중... (순서: 자막 → 자동 생성 자막 → 제목)", flush=True)
    segments, TRANSCRIPT_SOURCE = fetch_caption_segments(video_id)
    if not segments:
        print("⚠️ 자막·자동 생성 자막 모두 없음. 제목만으로 대본을 창작합니다.", flush=True)
        return None
    text = " ".join(t['text'] for t in segments)
    print("✅ 원본 자막 추출 성공! (이 내용을 바탕으로 대본을 씁니다)", flush=True)
    return text

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
        
    if transcript_text and TRANSCRIPT_SOURCE == "auto":
        transcript_text = ("(아래는 유튜브 자동 생성 자막이라 음성 인식 오류·문장부호 누락이 있을 수 있음. 문맥상 명백한 오인식은 바로잡고, "
                           "확실하지 않은 고유명사·숫자는 쓰지 말 것.)\n" + transcript_text)
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
너는 'Miya's Lab' 채널의 영어 내레이션 작가야. 글로벌 시청자에게 지식을 차분하고 깊이 있게 전달하는 롱폼 영상의 **영어 내레이션 대본**을 쓴다. 이 대본은 그대로 TTS 음성과 모션그래픽(SVG 일러스트) 영상으로 만들어질 예정이야.

{source_material}

[작성 규칙 - 지침서 기준, 절대 어기지 마!]:
1. **언어**: 영상에 들리고 보이는 것은 전부 영어야. [1부]는 영어 내레이션만 쓰고 한글, 이모지, 괄호 연출 메모, 타임코드, 장면 번호를 절대 넣지 마(TTS에 그대로 붙여 넣을 글이야). 원본이 한국어·일본어여도 자연스러운 영어로 옮겨 써. 숫자·단위·날짜는 영어 표기(예: "2.461 billion years ago", "380,000 km").
​2. **분량**: [1부] 영어 단어 수는 **약 3,100단어(허용 2,900~3,300단어)**로 맞춰. (Kokoro TTS가 분당 약 163단어로 읽으므로 영상 약 18~21분이 돼.) 2,900단어에 못 미치면 구체적인 장면 묘사, 원리 설명, 일상 비유, **원본에 있는 사례**로 보강하고, 3,300단어를 넘으면 반복과 곁가지를 덜어내. 원본 자막이 있으면 원본의 디테일과 예시를 최대한 살려.
3. **문단 = 장면 하나**: [1부]는 문단마다 빈 줄로 구분해. 한 문단은 같은 장소·같은 생각을 다루는 장면 하나이고 **약 60~110단어(문장 4~7개, 약 25~40초)**로 써. 장면이 바뀔 때(장소·시대·예시·질문이 바뀔 때)만 문단을 나눠. 숫자 비교가 중심인 문단은 그 숫자들을 한 문단에 모아(영상에서 데이터 카드 한 장이 돼). 문장은 짧게(평균 15단어 안팎), 평서문과 의문문을 섞어.
4. **말투**: 한 사람에게 이야기하듯 따뜻하고 공손한 대화체. 시청자를 "you"로 부르고 축약형(it's, don't)을 써도 돼. 수사 의문문은 영상 전체에서 8~18개.
5. **구성**: ① 처음 60초 훅은 일상적인 감각("Take a look at your fingernails.") / 의
