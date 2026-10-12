import os
import time
import multiprocessing
from datetime import datetime
from google import genai
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SAVE_DIR = "./scripts_owl" 
HISTORY_FILE = os.path.join(SAVE_DIR, "history.txt")

def get_unprocessed_top_video():
    print("🔍 유튜브 API 연결 및 채널 검색 중...", flush=True)
    if not YOUTUBE_API_KEY:
        print("❌ 에러: YOUTUBE_API_KEY가 없습니다.", flush=True)
        return None, None
        
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        
        channel_id = "UCrBpV_pG2kyMMEHCMTNzjAQ" # 리뷰엉이 채널 고유 ID
        
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
            
            # 💡 [핵심 수정] 우주/과학 영상만 골라내는 엄격한 필터링 로직
            allowed_keywords = ['우주', '지구', '태양', '행성', '블랙홀', '양자', '과학', '외계', '은하', '물리', '상대성', '차원', '빛', '빅뱅', '다중우주', '달', '별', '중력', '우주선', 'NASA', '나사', '엔트로피', '타임머신', '시간', '입자', '광속', '우주인']
            excluded_keywords = ['영화', '마블', '어벤져스', '결말', '스포', '리뷰', '예고편', '쿠키', '드라마', '애니', '스파이더맨', '배트맨', '아이언맨', 'DC', 'MCU', '해석', '디즈니', '넷플릭스', '극장']
            
            # 1. 영화/애니메이션 관련 키워드가 제목에 하나라도 있으면 즉시 건너뜀
            if any(ext_kw in video_title.upper() for ext_kw in excluded_keywords):
                continue
                
            # 2. 우주/과학 관련 키워드가 제목에 단 하나라도 있어야만 통과
            if not any(allow_kw in video_title for allow_kw in allowed_keywords):
                continue

            if video_id not in processed_videos:
                print(f"✅ 우주/과학 타겟 영상 발견: {video_title}", flush=True)
                return video_title, video_id
                
        print("⚠️ 상위 50개 영상 중 조건(우주/과학)에 맞는 새로운 영상을 찾지 못했습니다!", flush=True)
        return None, None
        
    except Exception as e:
        error_msg = str(e).lower()
        if "quota" in error_msg or "429" in error_msg or "rate limit" in error_msg:
            print("\n🚨 [경고: 유튜브 API 한도 초과] 하루 무료 검색량(10,000 포인트)을 모두 소진했습니다!", flush=True)
        else:
            print(f"❌ 유튜브 검색 중 에러 발생: {e}", flush=True)
        return None, None

def get_video_transcript(video_id):
    print("📜 원본 유튜브 영상 자막 추출 시도 중...", flush=True)
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko', 'en', 'ja'])
        
        chunks = []
        current_chunk = []
        chunk_limit = 1200 
        
        for t in transcript_list:
            if t['start'] >= chunk_limit:
                chunks.append(" ".join(current_chunk))
                current_chunk = []
                chunk_limit += 1200
            current_chunk.append(t['text'])
            
        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        print(f"✅ 원본 자막 추출 성공! (20분 단위로 총 {len(chunks)}개의 파트로 나눔)", flush=True)
        return chunks
    except Exception as e:
        print("⚠️ 자막 추출 실패 (자막이 없는 영상입니다).", flush=True)
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

def create_ai_studio_script(youtube_title, transcript_text, part_num, total_parts):
    print(f"🤖 제미나이 20분 분량 대본 기획 시작... (시리즈 Part {part_num}/{total_parts})", flush=True)
    if not GEMINI_API_KEY:
        return None
        
    if total_parts > 1:
        if part_num < total_parts:
            connection_instruction = "이 대본은 내용이 방대하여 여러 편으로 나눈 시리즈 중 하나야. 대본의 마지막 장면(Scene)은 다음 편(Part)을 안 보고는 못 배기도록 아주 극적이고 긴장감 넘치는 클리프행어(To be continued...)로 끊어줘."
        else:
            connection_instruction = "이 대본은 시리즈의 마지막 편(Part)이야. 이전 편의 분위기를 자연스럽게 이어받고, 마지막에는 모든 궁금증을 폭발적으로 해소하며 웅장하게 마무리해."
    else:
        connection_instruction = "이 대본은 단일 영상으로 끝나는 20분짜리 대본이야. 기승전결이 완벽하게 마무리되도록 해줘."

    if transcript_text:
        source_material = f"""
[원본 영상 제목]: "{youtube_title}" (전체 시리즈 중 Part {part_num}/{total_parts})
[원본 영상 실제 대본 내용 (이 내용을 완벽히 분석해서 우리만의 20분 대본으로 길게 재창조할 것)]:
{transcript_text}
"""
    else:
        source_material = f"""
[원본 영상 제목]: "{youtube_title}"
(원본 자막을 구할 수 없습니다. 제목의 핵심 주제를 바탕으로 20분 분량의 지식 대본을 스스로 창작해 주세요.)
"""

    prompt = f"""
너는 '글로벌 지식 전달'에 특화된 100만 구독자 해외 유튜버야.
사용자가 이 대본을 바탕으로 **20분 길이(영어 단어 수 기준 최소 2,600단어 ~ 3,000단어)의 극적으로 몰입감 넘치는 지식 롱폼 영상**을 만들 예정이야.

{source_material}

[작성 규칙 - 매우 중요! 절대 어기지 마!]:
1. **분량 강제 (가장 중요)**: 전체 [영어 TTS]의 단어 수를 모두 합쳤을 때 **무조건 2,600단어 이상**이 되어야 해! 내용을 요약하지 말고, 최대한 디테일을 살려 길게 풀어써.
2. **영화 내용 완전 삭제 (필터링)**: 원본 내용 중 '영화(Movie)', '시네마', '마블', '특정 영화 제목이나 영화 속 설정'과 관련된 언급, 비유, 예시가 단 한 줄이라도 있다면 대본에서 **100% 완전히 삭제해!!** 오직 '실제 과학적/역사적/미스터리적 사실과 지식'에만 집중해서 대본을 완벽히 재구성해.
3. **과장과 극적 연출 허용**: 거짓말을 지어내면 안 되지만, 시청자가 미친 듯이 몰입해서 볼 수 있도록 사실을 바탕으로 한 아주 흥미진진한 묘사, 소름 돋는 연출, 약간 과장된 수사법(Dramatize)을 팍팍 섞어줘. 유튜브 시청자의 호기심을 극도로 자극해야 해.
4. **시리즈 연결**: {connection_instruction}
5. 장면(Scene) 수: 20분 분량을 꽉 채우기 위해 **최소 45개에서 55개의 장면(Scene)**으로 구성해.
6. 각 장면의 대사량: 하나의 [영어 TTS] 블록 안에는 성우가 20초~30초간 쉴 새 없이 읽을 수 있도록 **최소 5문장~8문장 이상(약 60~100단어)**의 아주 풍부한 영어 대사를 작성해. 대충 한두 줄로 넘어가면 안 돼.
7. 타임라인(시간 표시) 금지. [장면 1], [장면 2] 형식으로 번호만 매겨.
8. [시각 자료]와 [한글 시각자료 내용 번역]은 반드시 **한국어(Korean)**로 작성.
9. [영어 자막]과 [영어 TTS]는 반드시 원어민 수준의 자연스러운 **영어(English)**로 작성. (절대 한국어 섞지 말 것).
10. [영어 자막]은 화면 정중앙에 띄울 짧은 핵심 영어 문장 1개.

[출력 양식 예시]:
[영상 제목]: The Secret of the Black Hole / 블랙홀의 비밀 (Part 1/2)

[장면 1]
- 시각 자료: 거대한 블랙홀이 별을 집어삼키는 3D 그래픽 화면
- 영어 자막: The Monster in the Dark
- 영어 TTS: Did you know that there are monsters lurking in the darkness of space? Today, we are diving into the ultimate mystery: Black Holes. These cosmic giants possess gravitational pulls so strong that not even light can escape their grasp. Imagine a vacuum cleaner large enough to swallow entire star systems whole, leaving absolutely nothing behind. We will explore how they form, where they hide, and what would happen if you were to fall into one.
- 한글 번역: 우주의 어둠 속에 괴물이 숨어있다는 사실을 아시나요? 오늘 우리는 궁극의 미스터리, 블랙홀로 빠져들어 봅니다. 이 우주의 거인들은 빛조차 빠져나갈 수 없을 정도로 강력한 중력을 가지고 있습니다. 별의 무리를 통째로 집어삼키고 아무것도 남기지 않는 거대한 진공청소기를 상상해 보세요. 우리는 이것들이 어떻게 형성되는지, 어디에 숨어 있는지, 그리고 만약 당신이 그 안으로 떨어진다면 어떤 일이 벌어질지 알아볼 것입니다.

위 예시처럼 [영어 TTS] 부분의 분량을 길고 꽉 차게 작성해서, [장면 45] 이상까지 기승전결이 완벽한 2,600단어 이상의 롱폼 대본을 끝까지 출력해줘.
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
                print(f"✅ 20분 분량(2,600단어 이상) 대본 생성 성공! (Part {part_num}/{total_parts})", flush=True)
                return text
            else:
                error_msg_lower = text.lower()
                if "429" in error_msg_lower or "quota" in error_msg_lower or "resource_exhausted" in error_msg_lower:
                    print(f"\n🚨 [경고: 제미나이 API 한도 초과] 무료 할당량을 모두 소진했습니다!", flush=True)
                else:
                    print(f"❌ 제미나이 내부 에러 (시도 {attempt+1}/{max_retries}): {text}", flush=True)
                
                if attempt < max_retries - 1:
                    print("⏳ 30초 후 다시 시도합니다...", flush=True)
                    time.sleep(30)
                else:
                    print("⚠ 5번 연속 에러로 대본 생성을 포기합니다.", flush=True)
                    
    return None

if __name__ == "__main__":
    print("🚀 리뷰엉이 채널 전용 클라우드 대본 공장 가동!", flush=True)
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
            
    title, video_id = get_unprocessed_top_video()
    
    if title and video_id:
        transcript_chunks = get_video_transcript(video_id)
        
        if not transcript_chunks:
            transcript_chunks = [None] 
            
        total_parts = len(transcript_chunks)
        all_parts_success = True
        
        for i, chunk_text in enumerate(transcript_chunks):
            part_num = i + 1
            script_text = create_ai_studio_script(title, chunk_text, part_num, total_parts)
            
            if script_text:
                current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"script_{current_time}_Part{part_num}.txt"
                text_file_path = os.path.join(SAVE_DIR, filename)
                
                with open(text_file_path, "w", encoding="utf-8") as f:
                    f.write(f"레퍼런스 주제: {title} (총 {total_parts}부작 중 {part_num}부)\n\n")
                    f.write(script_text)
                    
                print(f"🎉 Part {part_num} 작업 성공! 파일 저장 완료: {text_file_path}", flush=True)
            else:
                print(f"⚠ Part {part_num} 대본 생성 실패.", flush=True)
                all_parts_success = False
                break 
                
            if part_num < total_parts:
                print("⏳ 다음 파트 생성을 위해 10초 대기 중...", flush=True)
                time.sleep(10)
        
        if all_parts_success:
            with open(HISTORY_FILE, "a", encoding="utf-8") as f:
                f.write(f"{video_id}\n")
            print("🏁 타겟 영상의 모든 파트 처리가 완료되어 진도표에 기록되었습니다.", flush=True)
    else:
         print("⚠ 처리할 영상을 찾지 못해 작업을 종료합니다.", flush=True)
