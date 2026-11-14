## 15. HTML → MP4 렌더링 (최종 결과물)

> 최종 수정: 2026-11-14 · 본문은 지금 유효한 규칙만 담는다. 바뀐 경위는 맨 아래 개정 이력.

MP4는 별도 컴포지션(렌더 원본 `render/<슬러그>/`)으로 렌더한다. 13장 애니메틱은 그대로 렌더되지 않는다. SVG 그림 기준 MP4라는 것을 알리고, AI 생성 클립이 있으면 교체한다.

### 15-1. 도구
- **HyperFrames**(`npx hyperframes@0.8.141`, Apache-2.0): 헤드리스 Chrome이 프레임마다 seek해 캡처하고 FFmpeg로 인코딩한다.
- 출력: H.264 1920×1080 30fps, AAC 48kHz 스테레오.
- `data-volume` 0.5 = −6dB.
- Kokoro는 모노 24kHz라 스테레오 MP4에서 약 3 LU 커진다. 스테레오로 바꾼 뒤 정규화한다(15-2).
- `hyperframes transcribe`는 이 환경에서 403(단어 시간은 21-5).
- `hyperframes init`은 `~/.agents/skills/`에 스킬을 설치한다(사용자 PC에서 실행하면 알린다).

### 15-2. 컴포지션 규칙

| 항목 | 규칙 |
|---|---|
| 파일 | `index.html`, 오디오, 그림은 폴더 안 로컬 파일. 외부 CDN·폰트 링크 금지(`sub_timeline_script_failure`) |
| 공용 자산 | GSAP(3.15.0)·플러그인·`anime.min.js`·글꼴·로고·질감 PNG는 `tools/assets`에만 두고 렌더 폴더에는 링크한다(20-7). 렌더 폴더의 사본은 git에 올리지 않는다 |
| 루트 속성 | `data-composition-id`, `data-start`, `data-duration`, `data-width="1920"`, `data-height="1080"` |
| 시간 요소 | `class="clip"`, `data-start`, `data-duration`, `data-track-index` |
| 애니메이션 | 일시정지 상태 GSAP 타임라인 하나를 `window.__timelines["main"]`에 등록. CSS 키프레임·JS 타이머·`requestAnimationFrame` 금지(seek 불가) |
| 소리 | 파일 + `<audio>`. `mix.m4a` 한 트랙(15-5). Web Audio는 렌더에 들어가는지 미확인 |
| 필터 | SVG 필터 금지(`feTurbulence`+확대에서 초당 3.84프레임까지 떨어짐). 종이 질감은 정지 알파 노이즈 PNG 한 장을 맨 위층에 |
| ease | `CustomWiggle`·문자열 `wiggle()` 금지(15-8) |
| 자막·칠판·로고 | 5·6·7장 값 |

**자막 시각 검사**
- 타임라인을 만들 때 모든 자막이 `시작 < 끝`이고 다음 시작 ≥ 이전 시작인지 검사한다. 어긋난 줄은 앞뒤 사이로 제한한다.
- 컷 끝은 컷 경계를 넘지 않는다.
- 렌더 후 컷 경계·중후반 프레임에서 자막이 한 줄만 보이는지 확인한다. 시각 자체는 21-5의 단어 시간.

**음량**
1. 내레이션을 이어 붙인 파일을 스테레오로 변환한다.
2. ffmpeg `loudnorm` 2패스(`I=-16.8:TP=-1.5:LRA=3.5`, 1패스 측정값 + `linear=true`).
3. 48kHz로 저장하고 컷별로 자른다.
4. 최종 MP4도 `ebur128`로 측정한다(9-2).

### 15-3. 렌더 명령 (샌드박스)
```
export HYPERFRAMES_BROWSER_PATH=$(python3 -c "import sys; sys.path.insert(0,'tools'); import paths; print(paths.chrome())")
npx --yes hyperframes@0.8.141 render
```
- 설치된 Chromium을 지정한다(자동 다운로드는 프록시 403). 경로의 버전 번호는 기기마다 달라 `paths.chrome()`이 찾는다.
- 결과는 `renders/`의 MP4. `ffprobe`, 프레임 몇 장, `volumedetect`로 확인한다.
- **긴 렌더는 분리 실행**(`&`만 쓰면 `render_cancelled_parent_exited`): 끝나면 `render.done`에 `EXIT <코드> SECONDS <초>`를 쓰는 `run_render.sh`를 `setsid nohup ./run_render.sh < /dev/null > /dev/null 2>&1 & disown`으로 실행한다(이 호출만 따로). `tools/build/tts.sh`도 같은 방식.
- `pkill -f hyperframes` 금지.
- 진행은 `render.log`의 `"done":N`. 6분 동안 안 늘면 멈춘 것이다. 100% 뒤 `Assembling final video`에서 0으로 보이는 것은 정상.
- 중단되면 처음부터 다시 한다.

### 15-4. 안전 원칙
- 새 도구는 빈 폴더 샘플로 먼저 검증한다. 애니메틱 원본은 건드리지 않는다.
- 버전 고정(`@0.8.141`). 올릴 때 샘플로 다시 확인한다.
- 작업 폴더 밖에 생기는 파일은 사용자에게 알린다.
- 도구 설명과 이 장이 다르면 직접 렌더한 결과를 따른다.

### 15-5. GitHub Actions 서버 렌더 + Drive 자동 업로드
MP4는 서버에서 렌더해 Drive로 바로 올린다(대화·GitHub를 거치지 않는다).

**저장소** `gequra-ship-it/youtube-script-daily`
- 예전 이름 `ht`/`HT`/`Youtube-script-Daily`로 연결돼 있으면 Actions API가 막힌다. `list_repos`로 확인하고 `add_repo`(access: push), 로컬 `origin`도 바꾼다.

**워크플로 `render-chunked.yml` (하나뿐이다)**
- 시작 조건(`render-pipeline` 푸시): `render/.chunked` 또는 `.github/workflows/render-chunked.yml`이 바뀔 때. 수동 실행 입력 `spec`(쉼표로 여러 개), `reuse_run`(20-7).
- **시작 조건은 되돌리기 어렵다**: 위 파일이 바뀌면 바로 렌더하고 Drive의 같은 이름 MP4를 덮어쓴다. 의도 없이 건드리지 않는다.

| `render/.chunked`의 줄 | 뜻 |
|---|---|
| `<슬러그> <구간 수>` | 구간별 병렬 렌더 뒤 합쳐 Drive에 올린다(20-7) |
| `<슬러그> 0` | 렌더하지 않고 `render/<슬러그>/deliver/`(썸네일·메타데이터)만 올린다 |
| `#`으로 시작하는 줄 | 무시. 슬러그 줄이 하나도 없으면 아무것도 하지 않는다 |

- `.chunked`의 **모든 줄**이 푸시마다 다시 실행된다. 끝난 영상의 줄은 지우고, 다른 영상의 줄을 남기지 않는다.
- 구간 작업 단계: Node 22 → FFmpeg → Chrome 예열(버전 확인 최대 3번 + 빈 페이지) → `tools/chunk_prep.py` → `npx hyperframes@0.8.141 render`(MP4가 없으면 재시도, 3번까지) → 구간 리포트. 합치는 작업: 구간 연결 → 음성 합치기 → ffprobe·음량 → Drive 업로드(비밀값이 있을 때만).
- 작업 하나의 시간 한도는 300분(합치는 작업 180분).

**렌더 원본 `render/<슬러그>/`**
- `index.html`, `mix.m4a`, 그림, 공용 자산 링크(15-2).
- `mix.m4a`는 모든 소리를 미리 합친 한 트랙이다(`<audio>` 수백 트랙은 ffmpeg 5분 제한으로 실패). `SEPARATE_AUDIO=1`은 예전 방식.
- 100MB 넘는 파일은 일반 푸시가 안 된다.

**제어 파일**

| 파일 | 뜻 |
|---|---|
| `.dest` | Drive 폴더(18장). 없으면 `<슬러그>/`, `-short`·`-short1`~`-short9`면 접미어를 뗀 이름의 `short/` |
| `.outname` | Drive 파일 이름 |
| `.skip_deliver` | `deliver/`를 다시 올리지 않는다 |
| `.checked` | `final_check` 통과 표시(15-8). 렌더를 시작시키지 않는다 |

**Drive 업로드**
- `rclone copyto … gdrive:<폴더>/… --drive-root-folder-id <Video & Thumbnail 폴더 ID>`.
- 비밀값 `RCLONE_CONF`(remote `gdrive`, 종류 `drive`, scope `1`)는 사용자가 Secrets에 등록한다. **비밀값은 읽거나 출력하지 않는다.**

**결과 확인과 감시**
- 결과는 Actions 실행 로그의 렌더 리포트(`cat report.txt`)에서 본다. `_render_report.txt`는 Drive에 올리지 않는다.
- 실행 상태는 `api.github.com/repos/<소유자>/<저장소>/actions/runs`·`jobs_url`. 실패 로그가 필요하면 사용자가 Actions 탭에서 복사한다.
- 예약 메시지로 확인하고 중간 "정상" 보고는 하지 않는다(21-4). 끝나면 Drive 목록과 리포트를 확인한다.

**확인하지 못한 것**
- 서버 MP4의 실제 화면·소리(사용자가 훑어본다).
- rclone 공용 클라이언트 ID 중단 경고(본인 ID로 바꾸고 `RCLONE_CONF`를 다시 등록해야 할 수 있다).
- 월 무료 실행 시간.

**오류 대응**

| 증상 | 대응 |
|---|---|
| "푸시 안 된 커밋" 경고 | `git ls-remote --heads origin <브랜치>`와 `git rev-parse HEAD`가 같으면 무시 |
| 브랜치 삭제 푸시 실패 | 사용자가 GitHub에서 지운다 |
| `__pycache__` 경고 | `.git/info/exclude`에 추가하고 `.pyc`를 되돌린다 |
| 서버 렌더 불가 | 차선은 사용자 PC 렌더(`render-package/` → `C:\miya-render`, `run_render.ps1`, 미검증) |

### 15-6. 렌더 원본 만들기

**제작 순서 (`tools/README.md`에도 있음)**
1. 음성: `tools/build/tts.sh` → `tools/build/audio_prep.py` → `tools/build/align.py`(21-5).
2. 썸네일 3장을 만들어 사용자 확인(통과/수정)을 받는다(16-6, 12-1). **통과 전에는 그림을 시작하지 않는다.**
3. `SLUG=x PLAN=1 python3 tools/build/build3.py` → `videos/x/plan.json`(uid, 대본, 배경 종류, 전환, 앞뒤 대본, `pal`).
4. 그림: `tools/art_spec.md`(세로 10절, 우주 11절) + `art_brief.md`(등장인물 시트, 에이전트별 스크래치 폴더)로 하위 에이전트가 `videos/x/art3/<uid>.svg`·`.json`을 그린다(에이전트당 10~20장, 장면 단위, 21-3).
   - 사이드카 키: `centre`, `focus`, `focus_word`, `sfx`, `labels`, `iris`, `spot`, `speed`.
   - 확인: `tools/preview/svgshot.py`, `tools/preview/labelshot.py`.
5. `SLUG=x python3 tools/build/build3.py` → `render/x/`. 로그 `fallback art 0`을 확인한다.
   - 먼저 `tools/build/svg_opt.py`가 그림을 `build/art_opt/`로 svgo 정리해 쓴다(`npx`가 없으면 건너뛰고 로그 `svgo: skipped`).
   - 옵션: 세로 `VERT=1`, 일부 시험 `SEL=1,2,3`, 그림 없을 때 시험용 `FALLBACK=1`.
6. `tools/check/motion_check.py`(20-4), 최종 점검(15-8), 시험 렌더로 확인한 뒤 푸시한다.

**구조**
- 의미 단위: 문장 → 쉼표 → 단어 순으로 쪼개 최대 길이(기본 9.3초 = 6.2×PACE 1.5, 20-2) 이하로 합친다. 1.6초 미만 단위는 이웃과 합치고, 장면 마지막 단위가 2초 미만이면 경계를 다시 나눈다.
- 컷 = `div.t`(전환) 안 `div.w`(카메라) 안 SVG. id에 `u<번호>_` 접두어.
- 장면 간격 0.8초, 앞 여백 1.0초, 끝 여백 2.5초(본편).
- 자막 줄: 문장 단위, 30자·7단어 이하(세로 22자·4단어), 쉼표에서 우선 끊는다.
- 칠판은 레이아웃 B 3행.

### 15-7. 새 세션에서 시작하는 방법 (사용자는 대본만 보내면 된다)

| 무엇 | 어디 |
|---|---|
| 도구 | `render-pipeline` 브랜치의 `tools/`(목록·사용법 `tools/README.md`) |
| 영상별 원본 | `videos/<슬러그>/`(`script.py`, `art3/*.svg`+`*.json`, `plan.json`, `config.py`, `art_brief.md`, `thumb/`) |
| 레포 구조 변경 기록 | `docs/repo-changes.md` |
| 안내 파일 | `CLAUDE.md`(자동으로 읽힘), 프로젝트 채팅용 `docs/project-instructions.md` |

**시작 순서**
1. `list_repos` → `add_repo`(access: push).
2. `git clone --depth 1 -b render-pipeline …`.
3. `tools/README.md` 순서대로 진행한다.
4. 대본을 받으면 `videos/<슬러그>/`를 만든다. `script.py`는 12-1 사실 확인 뒤의 영어 내레이션, `art3/`는 하위 에이전트, `config.py`·`thumb/`는 예시를 따른다.

- 렌더 시작 파일(`render/.chunked`)은 내가 적는다(사용자 일이 아니다).

**이미 만든 영상의 모션만 바꾸기**
- `python3 tools/build/restyle_motion.py render/<슬러그>`가 `index.html`을 현재 모션 규칙(19종, 빛 맥동, 이웃 도형 묶기, 칠판 글자 맞춤, 배지 카운트업, 스포트라이트, 자막 단어 강조)으로 바꾼다.
- `mix.m4a`·그림·자막·전환·카메라는 그대로다. 음성 `p01.wav…`은 저장소에 없어 전체 재빌드는 TTS부터 한다.
- 빌드 원본(이 도구를 안 거친 파일)에만 쓴다. 이미 패치된 파일은 건너뛰므로 규칙이 바뀌면 git에서 원본을 꺼내 다시 적용한다.
- 푸시하면 같은 Drive MP4를 덮어쓴다. 롱폼 동작은 미확인.
- 단위·그림 수를 바꾸는 다시 만들기는 21장.

### 15-8. 렌더 전 최종 점검 게이트
그림 에이전트가 자기 그림을 `attachcheck.py`로 점검해 보고해도(4-7), 메인(이 세션)이 만든 페이지에서 마지막에 한 번 더 확인한다. **점검을 건너뛰고 렌더를 푸시하지 않는다.**

**순서**
1. `build3.py`: 시작에 `axisfix.py`가 카탈로그 축을 자동으로 적고(4-8), 끝에 attachcheck가 자동으로 돈다.
2. `SLUG=<slug> python3 tools/check/final_check.py`.
3. 사용자가 짚은 장면은 `tools/preview/motionaudit.py`로 띠 이미지를 **눈으로** 본다.
4. 문제가 있으면 고치고(축이 안 맞으면 그 그림을 에이전트에게 돌려보낸다) 다시 빌드·점검한다.
5. 통과하면 `render/<slug>/.checked`가 생기고, `chunk_plan.py render/<slug>`가 사양을 내놓는다(없으면 경고하고 종료코드 2).

**`final_check.py`가 보는 것**

| 검사 | 기준 |
|---|---|
| attachcheck·pivotlive·originlive | 붙임·축(4-7, 4-8) |
| 그림 누락 | 0 |
| 다양성 `variety_check.py`(7-2 K-6, 4-10) | 최다 개구리 동작 ≤ 40 %, 동작 ≥ 8종, 의상 ≥ 4, 오브젝트 모션 종류 ≥ 8. 소품 할당량은 WARN 줄로 읽는다 |
| 맥동 오브젝트 탑승(7-2 L) | 0 |
| 센터 모션 사건 종류(4-13) | 종류별 ≤ 15 % |
| 금지 ease | `ease:"wiggle(`·`CustomWiggle.create`·`random` 형 wiggle이 있으면 막는다 |

**금지 ease (렌더가 멈춘다)**
- `CustomWiggle`과 문자열 `wiggle()` ease를 페이지에 두지 않는다. Chrome 캡처가 그 트윈 끝에서 멈춰 뒤 프레임이 전부 같은 그림이 된다.
- 대신 쓰는 것(`tools/fxlib.py` `REGISTER_JS`): 시드 고정 떨림 `miyaJit(n,seed)`(이름 ease `miyaWigR`), 순수 함수 ease `miyaW(n,type)`와 `miyaWig`·`miyaWigU`·`miyaWigA`.
- `fxlib.plain_wiggles()`가 build3 출력의 문자열 `wiggle()`을 `miyaW`로 바꾼다.
- 새 ease·플러그인을 넣을 때: 로컬에서 그 구간을 렌더해(`chunk_prep.py <slug> <n> <i>`로 구간만, 약 0.25초/프레임) `freezecheck.py`로 확인한다.

**렌더 뒤 멈춤 확인**
- Actions 렌더가 "성공"이어도 캡처가 중간에 멈춰 뒤쪽 프레임이 전부 같은 그림일 수 있다(프레임 수·길이는 정상이라 로그만으로는 안 보인다).
- 렌더 직후 `gh run download <run> -n chunk-<slug>-<i>`로 청크 MP4를 받아 `python3 tools/check/freezecheck.py chunk.mp4`를 돌린다. 5초 이상 서로 다른 프레임이 2장 이하이면 FROZEN(종료코드 1).
- FROZEN이면 그 슬러그만 `render-chunked` 수동 실행(`spec`)으로 다시 렌더한다.
- 청크 아티팩트 보존 기간은 2일.

---

### 개정 이력
- 2026-10-09: 서버 렌더 + Drive 업로드, 새 화풍 렌더 원본 방식 확인.
- 2026-10-24 (miya): `_render_report.txt`를 납품물에서 제외(Drive에 올리지 않음).
- 2026-10-29 (miya): 최종 점검 게이트("마지막에 메인이 다시 한번 확인"). build3에 svgo 사본·플러그인(4-6). 숏츠3 끝부분이 멈추고 음성만 나와 렌더 뒤 freezecheck 추가(그때 프레임당 시간이 0.1→0.4초로 느려짐).
- 2026-10-30 (miya): 멈춤 원인 확정. ① `CustomWiggle` `random` 형(`mv-core-tremble`)이 트윈 끝에서 캡처를 멈춤(stolen-time 숏츠3 37.6초, 식인 숏츠3 6.8초, 괴물 개구리 숏츠3 117.5초). ② 문자열 `wiggle({type:'easeOut'|'uniform'})`와 `CustomWiggle.create`도 같은 증상(stolen-time 숏츠1 72.6초). 로컬 구간 렌더 이분 탐색으로 확인, `miyaBnc`(CustomBounce)는 원인이 아님.
- 2026-10-31: 다양성 검사. 2026-11-05: 맥동 탑승 0, 센터 모션 ≤ 15 %.
- 2026-11-14: 공용 자산을 `tools/assets` 링크로, GSAP 3.14.2 → 3.15.0 표기, Chromium 경로는 `paths.chrome()`, 저장소 "비공개" 표기 삭제.
- 2026-11-14 (miya): 문서 유지 규칙 형식으로 정리(현재 규칙만, 이력은 여기).
- 2026-11-14 (miya): `render.yml`(한 작업 방식, `render/.slug`, `.deliver_only`)을 없애고 `render-chunked.yml` 하나로 통합. 썸네일만 올리기는 `.chunked`의 `<슬러그> 0`.
