import os
import re
import time
import multiprocessing
from datetime import datetime
from google import genai
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SAVE_DIR = "./scripts_igwahyung"

PUBLISHED_DATE = None  # 선택된 영상의 게시일(YYYY-MM-DD), 없으면 실행일 사용

def script_date():
    return PUBLISHED_DATE or datetime.now().strftime("%Y-%m-%d")

def video_title_of(script_text, fallback):
    """대본의 '[영상 제목]: 영어 / 한국어'에서 영어 제목만 뽑는다(없으면 fallback)."""
    m = re.search(r"\[영상 제목\]:\s*(.+)", script_text)
    if not m:
        return fallback
    en = re.sub(r"\s*\(Part \d+/\d+\)\s*$", "", m.group(1).split(" / ")[0]).strip()
    return en or fallback

def korean_title_of(script_text, summary, fallback):
    """한국어 제목: '[영상 제목]: 영어 / 한국어' 뒤쪽, 없으면 요약의 '■ 영상 제목: 영어 (한국어)' 괄호 안, 그래도 없으면 fallback."""
    m = re.search(r"\[영상 제목\]:\s*(.+)", script_text or "")
    if m and " / " in m.group(1):
        ko = m.group(1).split(" / ", 1)[1].strip()
        if re.search(r"[가-힣]", ko):
            return ko
    m = re.search(r"■ 영상 제목:\s*(.+)", summary or "")
    if m:
        g = re.search(r"\(([^()]*[가-힣].*)\)\s*$", m.group(1))
        if g:
            return re.sub(r"\s*\(\d+부[^()]*\)\s*$", "", g.group(1)).strip()
    return fallback

def safe_title(title, max_len=80):
    t = re.sub(r'[\\/:*?"<>|\x00-\x1f]', "", title)
    t = re.sub(r"\s+", " ", t).strip(" .")
    return t[:max_len].rstrip(" .") or "untitled"
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
                global PUBLISHED_DATE
                PUBLISHED_DATE = item["snippet"].get("publishedAt", "")[:10] or None
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

CAPTION_LANGS = ['ko', 'en', 'ja']
TRANSCRIPT_SOURCE = None  # "captions" | "auto" | None(제목)

def fetch_caption_segments(video_id):
    """자막 → 유튜브 자동 생성 자막 → None(제목) 순으로 찾는다. (segments, source) 반환.
    segments는 {'text', 'start', 'duration'} dict 리스트."""
    try:
        ytt = YouTubeTranscriptApi()
        tl = ytt.list(video_id)
    except AttributeError:
        # youtube-transcript-api 1.0 이전 버전: 정적 get_transcript만 있음 (수동/자동 구분 불가)
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
        candidates += [t for t in others if t not in candidates]  # ko/en/ja가 없으면 다른 언어라도 사용
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

def log_hook_score(script_text):
    """[1부] 첫 약 40단어(첫 15초)의 훅 점수를 로그로만 남긴다(참고용, tools/hookscore.py; 재생성하지 않음)."""
    try:
        import sys as _sys
        _sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
        import hookscore
        start = script_text.index("=== 1부")
        body = script_text[start:].split("\n", 1)[1]
        hook = " ".join(body.split()[:40])
        _, verdict, name, _ = hookscore.score(hook)
        print(f"🎣 훅 점수(참고용) {verdict}/100 {hookscore.band(verdict)} · 공식: {name}", flush=True)
    except Exception as e:
        print(f"ℹ️ 훅 점수 건너뜀: {e}", flush=True)

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
2. **분량**: [1부] 영어 단어 수는 **약 3,450단어(허용 3,300~3,700단어)**로 맞춰. (Kokoro TTS가 분당 약 163단어로 읽으므로 영상 약 20~23분이 돼. 20분 미만은 안 돼.) 3,300단어에 못 미치면 구체적인 장면 묘사, 원리 설명, 일상 비유, **원본에 있는 사례**로 보강하고, 3,700단어를 넘으면 반복과 곁가지를 덜어내. 원본 자막이 있으면 원본의 디테일과 예시를 최대한 살려.
3. **문단 = 장면 하나**: [1부]는 문단마다 빈 줄로 구분해. 한 문단은 같은 장소·같은 생각을 다루는 장면 하나이고 **약 60~110단어(문장 4~7개, 약 25~40초)**로 써. 장면이 바뀔 때(장소·시대·예시·질문이 바뀔 때)만 문단을 나눠. 숫자 비교가 중심인 문단은 그 숫자들을 한 문단에 모아(영상에서 데이터 카드 한 장이 돼). 문장은 짧게(평균 15단어 안팎), 평서문과 의문문을 섞어.
4. **말투**: 한 사람에게 이야기하듯 따뜻하고 공손한 대화체. 시청자를 "you"로 부르고 축약형(it's, don't)을 써도 돼. 수사 의문문은 영상 전체에서 8~18개.
5. **구성**: ① 처음 60초 훅은 일상적인 감각("Take a look at your fingernails.") / 의외의 숫자나 사실 / 뒤집기 / 핵심 질문 / 출발 선언 중에서 골라 시작해. ② 본문은 구체적인 장면 묘사로 열고, 원리를 설명하고, 일상 비유를 들어. ③ 도입과 결말에 현대인의 일상 장면을 넣어. ④ 결말은 시청자의 현재로 돌아와 감성적으로 정리하고, 마지막에 주제에 맞는 은유로 구독을 부탁해. 채널은 "Miya's Lab" 또는 "this lab"이라고 부르고(철자 그대로), '서재(library)'라는 표현과 원본 채널 이름은 절대 쓰지 마.
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

=== 3부: 숏츠 대본 3편 ===
[숏츠 1] 제목: <영어, Title Case>
<영어 내레이션 약 380단어(330~440단어, 읽으면 2분 이상 2분 55초 이하). 1부에서 가장 흥미로운 부분을 골라(세 편이 서로 다른 부분), 질문이나 의외의 사실로 시작해 첫 2초 안에 훅을 던지고, 마지막 한 줄은 본편을 보게 만드는 문장. 1부에 있는 사실만 사용>

[숏츠 2] 제목: <영어, Title Case, 숏츠 1과 소재·훅이 겹치지 않게>
<같은 규칙의 영어 내레이션 약 380단어>

[숏츠 3] 제목: <영어, Title Case, 숏츠 1·2와 소재·훅이 겹치지 않게>
<같은 규칙의 영어 내레이션 약 380단어>

위 구조로 [1부]를 중간에 끊거나 요약하지 말고 끝까지 출력해줘. 2부와 3부까지 빠짐없이 출력해.
"""
    
    max_retries = 5
    best_text, best_words, short_tries = None, 0, 0
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
                log_word_count(text, 3300, 3700)
                log_hook_score(text)
                words = count_narration_words(text) or 0
                if words > best_words:
                    best_text, best_words = text, words
                if words < 3300 and short_tries < 3 and attempt < max_retries - 1:
                    short_tries += 1
                    print(f"🔁 20분 미만({words}단어): 재생성합니다 ({short_tries}/3).", flush=True)
                    continue
                return best_text
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
                    
    return best_text

def create_korean_summary(script_text, label=""):
    """영어 대본을 전부 번역하지 않고, 읽기용 한국어 요약본만 만든다 (2026-10-16 사용자 요청: 대본이 영어라 이해가 어려움)."""
    print(f"🇰🇷 한국어 요약본 생성 중...{label}", flush=True)
    if not GEMINI_API_KEY:
        return None
    prompt = f"""
아래는 'Miya's Lab' 채널의 영어 영상 대본이야. **전체를 번역하지 말고**, 한국어 사용자가 내용을 빠르게 파악할 수 있는 **한국어 요약본**만 써줘.

[규칙]
- 대본에 있는 내용만 요약해. 대본에 없는 사실·숫자·해석을 더하지 마.
- 숫자·연도·고유명사는 대본 그대로 옮기고, 필요하면 영어 원어를 괄호로 붙여.
- 요약본만 출력하고 인사말이나 설명은 붙이지 마.

[출력 양식]
■ 영상 제목: <영어 제목> (<한국어 번역>)
■ 한 줄 요약: <한 문장>
■ 전체 흐름 (대본 순서대로 8~15줄):
- <장면/단락 흐름 한 줄씩>
■ 핵심 사실·숫자 (5~10개):
- <사실 한 줄씩>
■ 숏츠 3편:
- 숏츠 1: <영어 제목> (<한국어 번역>) — <2~3문장 요약>
- 숏츠 2: <영어 제목> (<한국어 번역>) — <2~3문장 요약>
- 숏츠 3: <영어 제목> (<한국어 번역>) — <2~3문장 요약>
(대본에 숏츠가 없으면 이 항목은 "없음")

[영어 대본]
{script_text}
"""
    for attempt in range(3):
        manager = multiprocessing.Manager()
        return_dict = manager.dict()
        p = multiprocessing.Process(target=fetch_gemini_response, args=(GEMINI_API_KEY, prompt, return_dict))
        p.start()
        p.join(180)
        if p.is_alive():
            p.terminate()
            p.join()
            print(f"❌ 요약 생성 무응답 (시도 {attempt+1}/3)", flush=True)
        elif return_dict.get('status') == 'SUCCESS':
            print("✅ 한국어 요약본 생성 성공!", flush=True)
            return return_dict.get('text')
        else:
            print(f"❌ 요약 생성 에러 (시도 {attempt+1}/3): {return_dict.get('text')}", flush=True)
        if attempt < 2:
            time.sleep(20)
    print("⚠ 한국어 요약본 생성 실패 (대본 파일은 요약 없이 저장합니다).", flush=True)
    return None


if __name__ == "__main__":
    print("🚀 이과형 채널 전용 클라우드 대본 공장 가동!", flush=True)
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
            
    title, video_id = get_unprocessed_top_video()
    
    if title and video_id:
        transcript_text = get_video_transcript(video_id)
        
        script_text = create_ai_studio_script(title, transcript_text)
        
        if script_text:
            summary = create_korean_summary(script_text)
            filename = f"{script_date()}_{safe_title(korean_title_of(script_text, summary, video_title_of(script_text, title)))}.txt"
            text_file_path = os.path.join(SAVE_DIR, filename)
            
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(f"날짜: {script_date()}\n제목: {video_title_of(script_text, title)}\n레퍼런스 주제: {title}\n\n")
                if summary:
                    f.write("=== 한국어 요약 (전체 번역이 아닌 요약본) ===\n" + summary.strip() + "\n\n")
                f.write(script_text)
                
            with open(HISTORY_FILE, "a", encoding="utf-8") as f:
                f.write(f"{video_id}\n")
                
            print(f"🎉 모든 작업 성공! 파일 저장 완료: {text_file_path}", flush=True)
        else:
            print("⚠ 대본 생성 실패로 파일을 저장하지 못했습니다.", flush=True)
    else:
         print("⚠ 처리할 영상을 찾지 못해 작업을 종료합니다.", flush=True)
