## 9. 오디오

> 최종 수정: 2026-11-14 · 본문은 지금 유효한 규칙만 담는다. 바뀐 경위는 맨 아래 개정 이력.

| 절 | 내용 |
|---|---|
| 9-1 | 참고 영상 실측 |
| 9-2 | 목소리·길이·음량 목표 |
| 9-3 | 효과음 |
| 9-4 | 배경음악 |
| 9-5 | 리듬 연출 |
| 9-6 | 고정 아웃트로 |
| 9-7 | 확인하지 못하는 것 |

### 9-1. 참고 영상 실측 (한국어 영상)
배경음악·효과음 없음, 남성 1인 TTS 추정(약 124Hz), -16.8 LUFS·LRA 3.5 LU, 초당 약 4.8음절, 19~27분. Miya's Note는 배경음악·효과음을 넣는다(9-3·9-4).

### 9-2. 목소리·길이·음량 목표

| 항목 | 값 |
|---|---|
| 목소리 | 영어 TTS, 남성 1인 Kokoro `am_michael`, 속도 1.0, 모든 영상 같은 목소리 |
| 내레이션 음량 | -16.8 LUFS, LRA 약 3.5 LU |
| 말 속도 | 분당 145단어로 계산(실측: 2,086단어 = 내레이션 861.8초 = 영상 14:50) |
| 영상 길이 | 15분 이내. 영상 길이 = 음성 + 장면 간격(0.8초 × 장면 수) + 앞뒤 여백 3.5초 |
| 대본 분량 | 목표 2,000~2,100단어, 허용 1,900~2,200단어. 아웃트로는 세지 않는다 |
| 렌더 시간 | 영상 길이의 약 3.75~3.9배(실측: 18분 본편 67분) |
| 최종 MP4 음량 | 효과음·음악을 섞으면 −17.4~−17.7 LUFS, 피크 −1.5 dBFS(실측). 렌더 후 재정규화 단계는 없다 |

- 2,200단어는 약 15:20이라 15분을 넘길 수 있다. 음성을 만든 뒤 반드시 실제 길이를 잰다(`tools/build/audio_prep.py`의 total).
- 허용 범위를 벗어나면 12-1의 길이 조정을 한다.
- 매일 대본 코드(`generators/daily.py`·`owl.py`·`igwahyung.py`)는 분량 미달이면 최대 3회 재생성한다.

### 9-3. 효과음

**원칙**
- 내레이션을 가리지 않는 조용한 효과음을 그림·전환에 맞춘다. 화면에서 일이 일어나는 시각에 낸다.
- 금지: 음정(띠리링)이 있는 소리, 상시 저음(드론) 앰비언트, 약 120Hz 아래를 계속 내는 소리, 웃음소리, 비명, 과장된 코믹 효과음, 고통·사망을 자극하는 소리, 출처 불명·저작권 음원.
- 음원은 직접 합성한다(`tools/sfx_lib.py`). 라이브러리 음원은 라이선스를 확인한 파일을 사용자가 올릴 때만 쓴다.
- 배경 소리는 그 장면에서만 짧고 낮게 내고, 장면이 바뀌면 끊는다.
- 큐는 HTML 장면 데이터와 대본 txt에 함께 적는다.

**소리 목록 (`tools/sfx_lib.py`, 92종)**
- 전부 고역통과 150Hz, 피크 −24dBFS, 스테레오 48kHz. 150Hz 아래 에너지 2% 미만(측정, 최대는 heartbeat 1.3%). 소리마다 변형 3개를 큐마다 돌려 쓴다.
- 기본 25종: swish, hush(별칭 shimmer), tick, crackle, bubble, wind, bell, click, creak, drip, thud, chime, rustle, pop, pencil, page, cloth, woodblock, sand, rain, splash, step, breath, stone, flutter. bell·chime·hush는 음정 없는 소리다.
- 우주 6종: 3-7.
- 자연: waves, shore, stream, thunder(먼 천둥, 150Hz 위만), leaves, cricket, cicada, buzz, snowstep, icecrack, gust, whoosh, crumble, gravel, dig, dust, ash, candle, hiss, steam, slosh.
- 물건·사람·공간: knock, door, coins, clink, keys, zipper, typing, typewriter, heartbeat, crunch, sizzle, chop, pour, cork, tear, stamp, gavel, switch, shutter, static, radio, steps, hooves, march, scrape, chain, arrow, scroll, quill, match, thrust, impact, crack, snap, wingbeat, clock, gear, pump, bookclose, bubbleup.
- 들어 보기: `/mnt/project-files/frog-rules/audio/sfx-catalog-92.mp4`(데모는 +6dB).

**큐를 고르는 순서 (`tools/sfx_pick.py`, 코드 규칙, 7-2 D-2와 같은 방식)**

| 순서 | 근거 | 내용 |
|---|---|---|
| 1 | 대본 단어 | 단위 내레이션에 대한 단어 정규식 81개. 사건(thunder·crumble·impact·thrust·heartbeat·clock…)이 먼저, 질감이 뒤. 맞은 단어가 소리의 시각이 된다 |
| 2 | 그림 증거 | `tools/picev.py`가 그림에서 읽은 태그(`sfx_pick.SFX_PIC`, 로그 `auto: picture`). 아래 표 |
| 3 | 사이드카 | 그림 에이전트의 `sfx [{name, word, vol}]`(그림에만 보이는 일, 그 컷 대본 단어에 맞춤) |
| 4 | 앰비언트 | 3단위마다(`k % 3 == 1`, 6초 이상) 팔레트 앰비언트, 음량 .32. 아래 표 |

- 에이전트가 고른 큐를 그대로 쓰려면 사이드카에 `"sfx_lock": true`.
- 전환 소리는 4-3, 포커스는 tick, 칠판은 분필 소리.
- 0.9초 안에 겹치면 사건 > 전환 > 포커스 순으로 하나만 남긴다.
- 반복: 단어 규칙이 또 맞으면 같은 소리가 또 나온다(상황이 이어짐). 앰비언트 채움만 직전과 다르게 돌린다. '연달아 금지' 같은 고정 규칙은 없다.
- 1.5초가 넘는 질감은 4초 미만 단위에 쓰지 않는다.
- 밀도 상한: 큐가 단위의 45%를 넘으면 사건 규칙(앞 24개)만 통과한다. 그림 증거 큐에도 같이 적용한다.
- 우주(cosmic) 스타일은 지상 질감을 우주 가족으로 바꾼다(`COSMIC_SWAP`, 3-7).
- 확인: 빌드 로그 `sfx auto {...}`. `python3 tools/sfx_pick.py`는 모든 규칙이 있는 소리를 가리키는지 점검한다.

그림 증거 → 소리

| 그려진 것 | 소리 | 그려진 것 | 소리 |
|---|---|---|---|
| 불 | crackle | 새 | wingbeat |
| 촛불 | candle | 벌레 | buzz |
| 시계 | clock | 군중 | march |
| 종 | bell | 깃발·풍차 | gust |
| 톱니 | gear | 얼음 | icecrack |
| 동전 | coins | 물 | waves |
| 사슬 | chain | 굴뚝 | hiss |
| 심장 | heartbeat | 동굴 | drip |
| 문 | creak | 뼈 | stone |
| 책 | page | 숲 | leaves |

팔레트 앰비언트

| 팔레트 | 소리 |
|---|---|
| ocean | waves, shore, bubble, stream |
| forest | leaves, cricket, flutter, stream |
| desert | wind, dust, gust, sand |
| ice | gust, snowstep, icecrack, wind |
| storm | rain, thunder, gust, wind |
| history | candle, scroll, steps, quill |
| lab | bubble, typing, switch, static |
| body | heartbeat, breath, pulse |
| sunset | leaves, wind, cricket, cicada |
| 우주 팔레트 | glimmer, sparkle, pulse, static |

**음량 (제안, 실측 아님)**: 장면 소리는 내레이션보다 15~20dB 낮게, 큐는 피크 −24dBFS, 내레이션 중에는 4~6dB 더 낮게.

### 9-4. 배경음악

저작권 없고 가사 없는 잔잔한 음악을 직접 합성한다(`tools/bgm_lib.py`, `build3.py`에 연결). 샘플·외부 음원·보컬 없음(`seed=5`).

**규칙**
- 내레이션이 우선이다.
- 한 영상 안에서 음색·템포를 바꾸지 않는다. 분위기에 따라 진행 풀과 플럭 밀도만 바뀐다.
- 칠판 구간에도 같은 음악. 숏츠도 같은 음악을 길이만큼 따로 합성한다.
- `NOBGM=1`이면 음악 없음.

**스타일 (영상당 하나, `bgm_lib.style_for`)**

| 스타일 | 쓰는 곳 |
|---|---|
| `warm` | 기본 |
| `cosmic` | 우주. 전환 소리·속도선·효과음 표까지 우주 가족으로 바꾼다(`build3` `COSMIC`) |
| `ancient` | 역사·사막 |
| `ocean` | 바다 |
| `mystery` | 실험실 |
| `tense` | 폭풍 |
| `bright` | 밝은 주제 |
| `gentle` | 생물·몸·숲 |
| `solemn` | 얼음 |

- 고르는 순서: config `STYLE` > `PAL_DEFAULT`에서 정한 스타일(`PAL_STYLE`) > 대본 전체 분위기. 분위기 단어가 1000단어당 6개 이상이고 다른 분위기의 1.5배면 `tense`/`solemn`/`bright`로 바꾼다(예: 고래 낙하 = dark 71개 → solemn, 식인 = body → gentle).

**장면별 분위기 (`bgm_lib.scene_moods`)**
- 4종: calm, bright, dark, tense. 장면마다 내레이션 단어(`MOODW`)로 정한다(2개 이상이고 다른 분위기의 1.5배). 첫 장면은 tense 대신 dark.
- 분위기가 바뀌면 다음 코드 경계에서 그 분위기의 진행 풀로 바꾼다(최소 2코드 유지). 같은 분위기 안에서는 두 바퀴마다 풀의 다음 진행.
- 플럭 밀도: bright ×1.3, dark ×.7, tense ×.6.
- 스타일마다 분위기별 진행 2개, 모두 80진행.

**소리 만들기**
- 작곡(`warm` 기준): 코드 진행 풀(Am-F-C-G 계열 등), 코드 하나 8초, 부드러운 패드(사인파 + 약한 배음, 좌우 미세 디튠) + 박마다 약 40% 확률의 작은 플럭.
- 영상 길이만큼 만들고 처음 3초 페이드인, 끝 5초 페이드아웃.
- 저음 없음: 250Hz 고역통과 + 4.5kHz 저역통과.
- 덕킹: 내레이션 파일(`n##.wav`)에서 50ms 단위 음량 곡선을 만든다. 말 구간(−48dBFS 이상, 0.6초 이하 틈은 이음)은 기준 음량, 틈에서는 +4dB(어택 0.25초, 릴리스 1.2초). 음악 파일에 미리 굽는다.
- 음량: 말 구간 음악 RMS를 내레이션보다 13dB 낮게(`BGM_BELOW` 환경변수). 내레이션+음악 통합 음량은 내레이션만과 0.1 LU 미만 차이(측정).
- 모든 소리(내레이션·효과음·분필·음악)는 `build3.py`가 `mix.m4a` 하나로 미리 합친다(15-5).
- 조정: `BGM_BELOW`, `bgm_lib.py`의 진행·플럭 확률.
- 확인: 빌드 로그 `music style … (auto|config)`, `bgm moods [...]`. 들어 보기: `/mnt/project-files/frog-rules/audio/bgm-styles-9.mp4`.

### 9-5. 리듬 연출

그림 길이는 내레이션을 따르므로 컷을 박자 격자에 맞추지 않는다. 대신 아래 둘을 `tools/rhythm.py`가 `build3.py`에 넣는다.

| 연출 | 내용 | 끄기 |
|---|---|---|
| 큰 전환 강조 | 새 장면의 첫 단위(하드컷·칠판 제외) 전환 한가운데에, 그때 울리는 코드의 음 2개를 부드러운 플럭으로 더한다(`bgm_lib.synth(accents=)`) | `NOACCENT=1` |
| 거의 무음 구간 | 영상당 2개. ① 장면 하나 앞(내레이션이 끝나기 1.2초 전 ~ 다음 장면 시작 0.4초 전) ② 끝(마지막 낱말 0.3초 뒤 ~ 끝). 음악·효과음만 꺼지고(0.15초 가장자리) 내레이션은 그대로 | `NOSILENCE=1` |

- 무음 구간 ①의 장면은 config `SILENCE = [장면 번호]`로 고른다. `[]`이면 끝만, 없으면 약 60% 지점.
- `SEPARATE_AUDIO=1` 경로에는 무음 구간이 적용되지 않는다.
- J컷/L컷은 전환 소리 오프셋(`TRSND` 음수)으로 이미 있다. 정지 화면(프리즈)은 구현하지 않는다.
- 확인: 빌드 로그 `rhythm: accents N | near-silences [...]`.

### 9-6. 고정 아웃트로

- 롱폼은 항상 같은 아웃트로로 끝난다. 숏츠에는 없다.
- 내레이션: 고정 파일 `tools/assets/outro.wav`(am_michael). 문구는 "Thanks for watching! Subscribing and liking really help me make these videos. See you in the next one."
- 그림: 고정 파일 `tools/assets/outro.svg`. 칠판 배경에 글자 없이 개구리 손 흔들기 + 분필 선 벨·좋아요. 자막이 글자를 대신한다.
- 끝 여백 4초, 그림은 약 10초 나온다.
- 코드: `tools/paths.py`의 `load_scenes`가 마지막에 장면 `OUTRO`를 붙인다. `-shortN` 슬러그와 `VERT=1`은 제외하고, `config.py`에 `OUTRO = False`면 끈다(옛 영상 재빌드용). `tools/build/tts.sh`는 이 장면에 고정 wav를 복사하고 `build3.py`는 그림을 `art3/<uid>.svg`로 복사한다. `plan.json`에는 안 들어가니 그림 에이전트는 그리지 않는다.
- 바꾸려면 `OUTRO_TEXT`·wav·svg를 함께 고친다(wav는 `npx hyperframes tts <txt> -v am_michael -o tools/assets/outro.wav`).
- 유튜브 종료 화면 자리: 왼쪽 = 다음 영상 칸(약 600×338, x90~690·y370~708), 오른쪽 = 채널 원형(중심 x1620·y540, 반지름 160)을 분필 점선 틀로 비워 둔다. 개구리·벨·좋아요는 가운데 열. 종료 화면 요소는 업로드 때 YouTube 스튜디오에서 점선 틀에 맞춰 직접 배치한다.

### 9-7. 확인하지 못하는 것

- 소리가 자연스러운지, 음악의 크기·느낌이 맞는지는 사용자가 듣고 판단한다(나는 들을 수 없다). 내가 확인하는 것은 합성 수치(피크·주파수 에너지)와 빌드 로그뿐이다.

---

### 개정 이력
- 2026-10-09: 효과음 규칙 개정. 상시 저음 앰비언트 금지("웅" 소리 지적).
- 2026-10-10: 효과음 합성 v2(25종). 배경음악 도입("배경음악 없음" 규칙 대체). 여성 음성 기준 분당 163단어 측정.
- 2026-10-19: 대본 분량 3,100 → 3,450단어(20분 이상 기준, 이후 폐지).
- 2026-10-24: 새 채널 Miya's Note. 영상 15분 이내, 고정 아웃트로, 리듬 연출(시험 영상 v3에서 승인). 목소리 `af_heart`(여성)로 변경.
- 2026-10-26 (miya): 목소리를 `am_michael`(남성)로 되돌림, 아웃트로 wav 다시 생성. 10-24~26에 만든 4편은 af_heart.
- 2026-10-27 (miya): 효과음 61종 추가(92종)와 자동 선택(`sfx_pick.py`), 그림 증거 단계 추가(4편 점검: 단위당 큐 수 46·60·61·51 그대로, 앰비언트 16곳이 그림 큐로 바뀜). '연달아 금지' 제거. 배경음악 9스타일 × 4분위기 자동 선택.
- 2026-11-02: 남성 음성 재측정 분당 145단어. 분량 2,000~2,300 → 목표 2,000~2,100, 허용 1,900~2,200(2,200단어 안팎이 15분을 넘김: edge-of-universe 16:04, eating-humans 15:23).
- 2026-11-14 (miya): 본문을 현재 규칙만 남게 다시 씀(절 번호는 그대로, 9-7 추가). 목록을 표로 바꿈.
