## 9. 오디오

### 9-1. 참고 영상 실측 (한국어 영상)
배경음악·효과음 없음, 남성 1인 TTS 추정(약 124Hz), -16.8 LUFS·LRA 3.5 LU, 초당 약 4.8음절, 19~27분. (Miya's Note은 배경음악·효과음을 넣는다, 9-3·9-4.)

### 9-2. 영어 출력 목표
- 영어 TTS, **남성 1인(Kokoro `am_michael`, 차분한 중저음)**, 모든 영상 같은 목소리. miya 2026-10-26: 2026-10-24~26에 쓰던 여성 `af_heart`에서 원래 남성 목소리로 되돌림(그 사이 만든 4편은 af_heart, 새 영상부터 am_michael). 내레이션 **-16.8 LUFS**, LRA 약 3.5 LU.
- **말 속도 (2026-10-10 재측정)**: 기본 속도에서 분당 약 160~167단어(평균 약 163). 계산은 **분당 163단어**, 음성을 만든 뒤 반드시 실제 길이를 잰다.
- **영상 길이 15분 이내 (2026-10-24 새 채널 Miya's Note 사용자 결정; 이전 20분 이상 규칙을 대체)**. 영상 길이 = 음성 + 장면 간격(0.8초 × 장면 수) + 앞뒤 여백 3.5초.
- **대본 약 2,200단어, 허용 2,000~2,300단어**(분당 163단어로 계산한 음성 12.3~14.1분 + 장면 간격·여백, 영상 약 13~15분 이내; 계산이며 렌더 실측 전). 이전: 3,450단어(영상 약 21~23분, 2026-10-19 변경: 3,100단어 기준은 실제 대본이 2,900 안팎에 머물러 20분에 못 미쳤음). 2,000 미만이면 12-1 길이 조정, 2,300 초과면 줄인다. 매일 대본 코드(`main.py`·`main_이과형.py`)는 미달 시 최대 3회 재생성한다.
- 렌더 시간: 영상 길이의 약 3.75~3.9배(실측, 18분 본편 67분).
- 최종 MP4 음량(실측): 효과음·음악을 섞으면 −17.4~−17.7 LUFS, 피크 −1.5 dBFS(목표보다 0.6~0.9 LU 낮음). 렌더 후 재정규화 단계는 아직 없음.

### 9-3. 효과음 (채널 결정, 2026-10-09 개정)
내레이션을 가리지 않는 조용한 효과음을 그림·전환에 싱크. 음정(띠리링)이 있는 소리 금지. **상시 저음(드론) 앰비언트 금지**(2026-10-09 "웅" 소리 지적).
- **자동 선택 (2026-10-27, miya: "효과음을 더 만들고 대본·영상 상황에 맞게 자동으로")**: 효과음 큐는 `tools/sfx_pick.py`가 고른다(개구리·오브젝트 규칙과 같은 코드 규칙, 7-2 D-2). 순서: ① 단위 내레이션에 대한 단어 정규식 81개(사건이 먼저: thunder·crumble·impact·thrust·heartbeat·clock… 질감은 뒤), 맞은 단어가 소리의 시각이 된다 ② 없으면 그림 에이전트의 사이드카 `sfx`(그림에만 보이는 일) ③ 없으면 3단위마다(`k % 3 == 1`, 6초 이상) 팔레트 앰비언트(ocean=waves·shore·bubble·stream, forest=leaves·cricket·flutter·stream, desert=wind·dust·gust·sand, ice=gust·snowstep·icecrack·wind, storm=rain·thunder·gust·wind, history=candle·scroll·steps·quill, lab=bubble·typing·switch·static, body=heartbeat·breath·pulse, sunset=leaves·wind·cricket·cicada, 우주 팔레트=glimmer·sparkle·pulse·static; 음량 .32). 단어 규칙이 또 맞으면 같은 소리가 또 나오고(상황이 이어짐, 2026-10-27 miya: '연달아 금지' 고정 규칙 없음) 앰비언트 채움만 직전과 다르게 돌림, 1.5초 넘는 질감은 4초 미만 단위에 안 씀, 단위의 45%를 넘으면 사건 규칙(앞 24개)만 통과(기존 영상 4편 실측 46%). 우주(cosmic) 스타일은 지상 질감을 우주 가족으로 바꿈(`COSMIC_SWAP`, 3-7). 에이전트가 고른 큐를 그대로 쓰려면 사이드카 `"sfx_lock": true`. 빌드 로그 `sfx auto {...}`로 확인.
- **합성 소리 v3 (`tools/sfx_lib.py`, 2026-10-27)**: 61종 추가 → 92종. 자연 waves·shore·stream·thunder(먼 천둥, 150Hz 위만)·leaves·cricket·cicada·buzz·snowstep·icecrack·gust·whoosh·crumble·gravel·dig·dust·ash·candle·hiss·steam·slosh / 물건·사람·공간 knock·door·coins·clink·keys·zipper·typing·typewriter·heartbeat·crunch·sizzle·chop·pour·cork·tear·stamp·gavel·switch·shutter·static·radio·steps·hooves·march·scrape·chain·arrow·scroll·quill·match·thrust·impact·crack·snap·wingbeat·clock·gear·pump·bookclose·bubbleup. 전부 측정: 피크 −24dBFS, 150Hz 아래 에너지 2% 미만(heartbeat 1.3%가 최대). 들어 보기: `/mnt/project-files/frog-rules/audio/sfx-catalog-92.mp4`(데모는 +6dB). 소리가 자연스러운지는 사용자가 듣고 판단(나는 들을 수 없음).
- **합성 소리 v2 (`tools/sfx_lib.py`, 2026-10-10)**: 25종 swish, hush(별칭 shimmer), tick, crackle, bubble, wind, bell, click, creak, drip, thud, chime, rustle, pop, pencil, page, cloth, woodblock, sand, rain, splash, step, breath, stone, flutter(+우주 6종, 3-7). 소리마다 변형 3개(큐마다 돌려 씀). bell·chime·hush는 음정 없는 소리로 대체됨. 전부 고역통과 150Hz, **피크 −24dBFS**, 스테레오 48kHz.
- **큐**: 전환(4-3), 포커스 → tick, 장면 사건 → `sfx_pick`(위) 또는 사이드카 `sfx [{name, word, vol}]`(그 컷 대본 단어). 화면에서 일이 일어나는 시각에 맞춘다. 0.9초 안에 겹치면 사건 > 전환 > 포커스로 하나만. 같은 소리 두 컷 연속 금지. 칠판은 분필 소리.
- 배경 소리는 그 장면에서만 짧고 낮게(장면이 바뀌면 끊음). 약 120Hz 아래를 계속 내는 소리 금지.
- 음량 **(제안, 실측 아님)**: 장면 소리는 내레이션보다 15~20dB 낮게, 큐는 피크 −24dBFS, 내레이션 중에는 4~6dB 더 낮게.
- 금지: 웃음소리, 비명, 과장된 코믹 효과음, 고통·사망을 자극하는 소리, 출처 불명·저작권 음원. 음원은 직접 합성(라이브러리 음원은 라이선스 확인한 파일을 사용자가 올릴 때만).
- 큐는 HTML 장면 데이터와 대본 txt에 함께 적는다. 소리의 자연스러움은 사용자가 듣고 판단(나는 들을 수 없음).

### 9-4. 배경음악 (채널 결정, 2026-10-10 — 9장 첫머리의 "배경음악 없음" 규칙을 대체)
저작권 없고 가사 없는 잔잔한 음악을 **직접 합성**(`tools/bgm_lib.py`, `build3.py`에 연결).
- **스타일·분위기 자동 선택 (2026-10-27, miya)**: 스타일 9종(음색·템포, 영상당 하나) `warm`(기본)·`cosmic`·`ancient`(역사·사막)·`ocean`·`mystery`(실험실)·`tense`(폭풍)·`bright`·`gentle`(생물·몸·숲)·`solemn`(얼음). `bgm_lib.style_for`: config `STYLE`이 있으면 그것, 없으면 `PAL_DEFAULT`→스타일(`PAL_STYLE`), 대본 전체의 분위기 단어가 1000단어당 6개 이상이고 다른 분위기의 1.5배면 `tense`/`solemn`/`bright`로 바꿈(예: 고래 낙하 = dark 71개 → solemn, 식인 = body → gentle). 분위기 4종(calm·bright·dark·tense)은 장면마다 `scene_moods`가 내레이션 단어(`MOODW`)로 정하고(2개 이상, 다른 분위기의 1.5배; 첫 장면은 tense 대신 dark), 다음 코드 경계에서 그 분위기의 진행 풀로 바꾸며(최소 2코드 유지; 진행은 분위기가 바뀔 때 바뀌고 같은 분위기 안에서는 두 바퀴마다 풀의 다음 것) 플럭 밀도도 바뀐다(bright ×1.3, dark ×.7, tense ×.6). 스타일마다 분위기별 진행 2개 → 80진행. `cosmic`은 전환 소리·속도선·효과음 표까지 우주 가족으로 바꾼다(`build3` `COSMIC`). 들어 보기: `/mnt/project-files/frog-rules/audio/bgm-styles-9.mp4`. 빌드 로그 `music style … (auto|config)`, `bgm moods [...]`.
- 작곡(`warm` 기준): 코드 진행 풀(Am-F-C-G 계열 등), 코드 하나 8초, 부드러운 패드(사인파+약한 배음, 좌우 미세 디튠) + 박마다 약 40% 확률의 작은 플럭. 진행은 분위기를 따라 바뀜(위). 영상 길이만큼, 처음 3초 페이드인·끝 5초 페이드아웃. 샘플·외부 음원·보컬 없음(`seed=5`).
- 저음 없음: 250Hz 고역통과 + 4.5kHz 저역통과.
- **덕킹**: 내레이션 파일(`n##.wav`)에서 50ms 단위 음량 곡선. 말 구간(−48dBFS 이상, 0.6초 이하 틈은 이음)은 기준 음량, 틈에서는 +4dB(어택 0.25초, 릴리스 1.2초). 음악 파일에 미리 구움.
- **음량**: 말 구간 음악 RMS를 내레이션보다 **13dB 낮게**(`BGM_BELOW` 환경변수). 내레이션+음악 통합 음량은 내레이션만과 0.1 LU 미만 차이(측정).
- `NOBGM=1`이면 음악 없음.
- 모든 소리(내레이션·효과음·분필·음악)는 `build3.py`가 `mix.m4a` 하나로 미리 합친다(15-5).

**규칙**: 내레이션 우선. 한 영상 안에서 음색·템포를 바꾸지 않는다(분위기에 따라 진행 풀·플럭 밀도만 바뀜). 칠판 구간에도 같은 음악. 숏츠도 같은 음악(길이만큼 따로 합성). 크기·느낌은 사용자가 듣고 판단, 조정은 `BGM_BELOW`, `bgm_lib.py`의 진행·플럭 확률.

### 9-5. 리듬 연출 (사용자 결정 2026-10-24, 시험 영상 v3에서 승인)
그림 길이는 내레이션을 따르므로 컷을 박자 격자에 맞추지 않는다. 대신 아래 둘을 `tools/rhythm.py`가 `build3.py`에 넣는다.
- **큰 전환 강조**: 새 장면의 첫 단위(하드컷·칠판 제외)의 전환 한가운데에 그때 울리는 코드의 음 2개를 부드러운 플럭으로 더함(`bgm_lib.synth(accents=)`). `NOACCENT=1`이면 끔.
- **거의 무음 구간**: 영상당 2개 — ① 장면 하나 앞(내레이션이 끝나기 1.2초 전 ~ 다음 장면 시작 0.4초 전) ② 끝(마지막 낱말 0.3초 뒤~끝). 이때 음악·효과음만 꺼지고(0.15초 가장자리) 내레이션은 그대로. config `SILENCE = [장면 번호]`로 고르고(`[]`이면 끝만) 없으면 약 60% 지점. `NOSILENCE=1`이면 끔. `SEPARATE_AUDIO=1` 경로에는 적용되지 않음.
- J컷/L컷은 전환 소리 오프셋(`TRSND` 음수)으로 이미 있음. 정지 화면(프리즈)은 구현하지 않음.
- 확인: 시험 빌드의 로그(`rhythm: accents N | near-silences [...]`)와 구간 계산만 확인. 소리가 자연스러운지는 사용자가 듣고 판단(나는 들을 수 없음).

## 9-6. 고정 아웃트로 (2026-10-24, miya)
- 롱폼은 항상 같은 아웃트로로 끝난다(숏츠는 없음): 내레이션 고정 파일 `tools/assets/outro.wav`(am_michael, 2026-10-26 다시 생성, "Thanks for watching! Subscribing and liking really help me make these videos. See you in the next one.") + 고정 그림 `tools/assets/outro.svg`(칠판 배경, 글자 없음: 개구리 손 흔들기 + 분필 선 벨·좋아요, 자막이 글자를 대신함). 끝 여백을 4초로 늘려 그림이 약 10초 나온다.
- 코드: `tools/paths.py`의 `load_scenes`가 마지막에 장면 `OUTRO`를 붙인다(`-shortN` 슬러그·`VERT=1`은 제외, `config.py`에 `OUTRO = False`면 끔 = 옛 영상 재빌드용). `tools/tts.sh`는 이 장면에 고정 wav를 복사하고, `build3.py`는 그림을 `art3/<uid>.svg`로 복사한다. `plan.json`에는 안 들어가니 그림 에이전트는 그리지 않는다.
- 대본 단어 수(2,000~2,300)에는 아웃트로를 세지 않는다. 바꾸려면 `OUTRO_TEXT`·wav·svg를 함께 고친다(wav는 `npx hyperframes tts <txt> -v am_michael -o tools/assets/outro.wav`).
- 유튜브 종료 화면(끝 화면) 자리: 왼쪽 = 다음 영상 칸(약 600×338, x90~690·y370~708), 오른쪽 = 채널 원형(중심 x1620·y540, 반지름 160)을 분필 점선 틀로 비워 둔다. 개구리·벨·좋아요는 가운데 열. 종료 화면 요소는 영상 마지막 구간에 YouTube 스튜디오에서 직접 배치한다(업로드 때 수동, 점선 틀에 맞춘다).
개정: 2026-10-26 (miya) 목소리를 af_heart → am_michael(원래 남성)로 되돌림, 아웃트로 wav 다시 생성.
개정: 2026-10-27 (miya) 효과음 61종 추가(92종)와 자동 선택(`sfx_pick.py`), 배경음악 9스타일×4분위기 자동 선택(`bgm_lib.style_for`·`scene_moods`), 9-3·9-4.
개정: 2026-10-27 (miya) 효과음 '연달아 금지' 제거(단어가 또 맞으면 반복), 배경음악 진행은 분위기 변화에 따라 바뀜(`bgm_lib._order`).
