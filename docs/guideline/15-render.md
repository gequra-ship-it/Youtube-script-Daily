## 15. HTML → MP4 렌더링 (최종 결과물)

MP4는 별도 컴포지션(렌더 원본 `render/<슬러그>/`)으로 렌더한다. 13장 애니메틱은 그대로 렌더되지 않는다. SVG 그림 기준 MP4라는 것을 알리고, AI 생성 클립이 있으면 교체한다.

### 15-1. 도구와 검증 상태
- **HyperFrames**(`npx hyperframes@0.8.141`, Apache-2.0): 헤드리스 Chrome이 프레임마다 seek해 캡처, FFmpeg 인코딩. 출력 H.264 1920×1080 30fps, AAC 48kHz 스테레오.
- 확인: `data-volume` 0.5 = −6dB. **Kokoro는 모노 24kHz라 스테레오 MP4에서 약 3 LU 커진다 → 스테레오로 바꾼 뒤 정규화**(15-2). `hyperframes transcribe`는 이 환경에서 403(단어 시간은 21-5). `init`은 `~/.agents/skills/`에 스킬을 설치한다(사용자 PC에서 실행 시 알림).

### 15-2. 컴포지션 규칙
- 폴더 하나에 `index.html`과 GSAP·폰트·오디오·로고를 **모두 로컬 파일로**. 외부 CDN·폰트 링크 금지(`sub_timeline_script_failure`). GSAP는 `npm pack gsap@3.14.2`의 `gsap.min.js`.
- 루트에 `data-composition-id`, `data-start`, `data-duration`, `data-width="1920"`, `data-height="1080"`. 시간 요소는 `class="clip"`, `data-start`, `data-duration`, `data-track-index`.
- 애니메이션은 일시정지 상태 GSAP 타임라인 하나를 `window.__timelines["main"]`에 등록. CSS 키프레임·JS 타이머·`requestAnimationFrame` 금지(seek 불가).
- 소리는 파일 + `<audio>`(Web Audio는 렌더에 들어가는지 미확인). 현행은 `mix.m4a` 한 트랙(15-5).
- **SVG 필터 금지**(`feTurbulence`+확대에서 초당 3.84프레임까지 떨어짐). 종이 질감은 정지 알파 노이즈 PNG 한 장을 맨 위층에.
- 자막·칠판·로고는 5·6·7장 값.
- **자막 시각 검사**: 모든 자막이 `시작 < 끝`, 다음 시작 ≥ 이전 시작인지 타임라인을 만들 때 검사하고, 어긋난 줄은 앞뒤 사이로 제한. 컷 끝은 컷 경계를 넘지 않는다. 렌더 후 컷 경계·중후반 프레임에서 자막이 한 줄만 보이는지 확인. 시각 자체는 21-5의 단어 시간.
- **음량 (검증됨)**: 내레이션을 이어 붙인 파일을 **스테레오로 변환** → ffmpeg `loudnorm` 2패스(`I=-16.8:TP=-1.5:LRA=3.5`, 1패스 측정값 + `linear=true`) → 48kHz 저장 → 컷별로 자름. 최종 MP4도 `ebur128`로 측정(9-2).

### 15-3. 렌더 명령 (샌드박스)
```
export HYPERFRAMES_BROWSER_PATH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
npx --yes hyperframes@0.8.141 render
```
- 설치된 Chromium 지정(자동 다운로드는 프록시 403). 결과는 `renders/`의 MP4(`ffprobe`, 프레임 몇 장, `volumedetect`로 확인).
- **긴 렌더는 분리 실행**(`&`만 쓰면 `render_cancelled_parent_exited`): 끝나면 `render.done`에 `EXIT <코드> SECONDS <초>`를 쓰는 `run_render.sh`를 `setsid nohup ./run_render.sh < /dev/null > /dev/null 2>&1 & disown`으로(이 호출만 따로). `pkill -f hyperframes` 금지. `tools/tts.sh`도 같은 방식.
- 진행은 `render.log`의 `"done":N`(6분 동안 안 늘면 멈춤, 100% 뒤 `Assembling final video`에서 0으로 보이는 것은 정상). 중단되면 처음부터 다시.

### 15-4. 안전 원칙
- 새 도구는 빈 폴더 샘플로 먼저 검증. 애니메틱 원본은 건드리지 않는다.
- 버전 고정(`@0.8.141`), 올릴 때 샘플로 재확인.
- 작업 폴더 밖에 생기는 파일은 사용자에게 알린다.
- 도구 설명과 이 장이 다르면 직접 렌더한 결과를 따른다.

### 15-5. GitHub Actions 서버 렌더 + Drive 자동 업로드 (2026-10-09 확인)

MP4는 서버에서 렌더해 Drive로 바로 올린다(대화·GitHub를 거치지 않음).

- 저장소 `gequra-ship-it/youtube-script-daily`(비공개, 예전 이름 `ht`/`HT`/`Youtube-script-Daily`; 옛 이름으로 연결돼 있으면 Actions API가 막힘 → `list_repos` 확인, `add_repo`(access: push), 로컬 `origin`도 변경).
- 워크플로 `.github/workflows/render.yml`(`render-video`, `ubuntu-24.04`, 300분)과 병렬 `render-chunked.yml`(20-7). 단계: Node 22 → FFmpeg·rclone → Chrome **예열**(버전 확인 최대 3번 + 빈 페이지) → `npx hyperframes@0.8.141 render`(MP4가 없으면 재시도, 3번까지) → ffprobe·음량 → Drive 업로드(비밀값이 있을 때만). 실패 로그 끝부분은 `<슬러그>_render_error.txt`로 Drive에. 한 슬러그가 실패해도 다음을 계속. 수동 실행 입력 `slug`(쉼표로 여러 개).
- **렌더 시작 조건 (되돌리기 어려움)**: `render-pipeline` 푸시에서 `render/.slug`, `.github/workflows/render.yml`, `render/sample/**` 중 하나가 바뀌면 즉시 렌더하고 Drive의 같은 이름 MP4를 덮어쓴다. 같은 내용 재렌더는 `.slug` 줄 순서를 바꾼다. 워크플로만 바꿀 때는 `.slug`를 `none`으로. `.slug`가 없으면 `sample`(→ `_ci-test/`).
- **다중 슬러그**: `.slug`에 한 줄에 하나(롱폼, `-short1`~`-short5`), 차례로 렌더. 목록은 fd 3으로 읽는다(`while read -r SLUG <&3 ... done 3< 파일`; 표준입력이면 첫 슬러그만 렌더되는 버그 — 롱폼이 몇 분 만에 끝나면 의심).
- **렌더 원본** `render/<슬러그>/`: `index.html`, `gsap.min.js`, 폰트, 로고, 질감 PNG, `mix.m4a`(모든 소리를 미리 합침; `<audio>` 수백 트랙은 ffmpeg 5분 제한으로 실패. `SEPARATE_AUDIO=1`은 예전 방식). 100MB 넘는 파일은 일반 푸시 불가.
- **제어 파일**: `.dest`(Drive 폴더, 18장; 없으면 `<슬러그>/`, `-short`·`-short1`~`-short9`면 접미어 뗀 이름의 `short/`), `.outname`(Drive 파일 이름), `.skip_deliver`(`deliver/` 다시 안 올림), `.deliver_only`(렌더 없이 `deliver/`만; 재렌더하려면 지움).
- Drive 업로드 `rclone copyto … gdrive:<폴더>/… --drive-root-folder-id <Video & Thumbnail 폴더 ID>`. 비밀값 `RCLONE_CONF`(remote `gdrive`, 종류 `drive`, scope `1`)는 사용자가 Secrets에 등록. **비밀값은 읽거나 출력하지 않는다.**
- 결과 확인은 Actions 실행 로그의 렌더 리포트(`cat report.txt`)에서 한다. `_render_report.txt`는 Drive에 올리지 않는다(2026-10-24 납품물에서 제외, 워크플로 업로드 줄 제거)(서버 로그 본문은 못 읽음). 실행 상태는 `api.github.com/repos/<소유자>/<저장소>/actions/runs`·`jobs_url`. 실패 로그가 필요하면 사용자가 Actions 탭에서 복사.
- **감시**: 예약 메시지로 확인하고 중간 "정상" 보고는 하지 않는다(21-4가 2026-10-10의 "5분마다 정상 보고"보다 새 규칙). 끝나면 Drive 목록과 리포트 확인.
- **확인하지 못한 것**: 서버 MP4의 실제 화면·소리(사용자가 훑어봄), rclone 공용 클라이언트 ID 2026년 중 중단 경고(본인 ID로 바꾸고 `RCLONE_CONF` 재등록 필요할 수 있음), 월 무료 실행 시간.
- **오류 대응**: "푸시 안 된 커밋" 경고는 `git ls-remote --heads origin <브랜치>`와 `git rev-parse HEAD`가 같으면 무시. 브랜치 삭제 푸시는 실패하므로 사용자가 GitHub에서 지움. `__pycache__` 경고는 `.git/info/exclude`에 추가하고 `.pyc`를 되돌림. 차선은 사용자 PC 렌더(`render-package/` → `C:\miya-render`, `run_render.ps1`, 미검증).

### 15-6. 렌더 원본 만들기 (새 화풍 방식, 2026-10-09 구현·확인)

**제작 순서 (`tools/README.md`에도 있음)**
1. 음성: `tools/tts.sh` → `tools/audio_prep.py` → `tools/align.py`(21-5). **그다음 썸네일 3장을 만들어 사용자 확인(통과/수정)을 받는다(16-6, 12-1). 통과 전에는 3번 그림을 시작하지 않는다.**
2. `SLUG=x PLAN=1 python3 tools/build3.py` → `videos/x/plan.json`(uid, 대본, 배경 종류, 전환, 앞뒤 대본, `pal`).
3. 그림: `tools/art_spec.md`(세로 10절, 우주 11절) + `art_brief.md`(등장인물 시트, 에이전트별 스크래치 폴더)로 하위 에이전트가 `videos/x/art3/<uid>.svg`·`.json`을 그린다(에이전트당 10~20장, 장면 단위, 21-3). 사이드카 키 `centre`, `focus`, `focus_word`, `sfx`, `labels`, `iris`, `spot`, `speed`. 확인 `tools/svgshot.py`, `tools/labelshot.py`.
4. `SLUG=x python3 tools/build3.py` → `render/x/`(세로 `VERT=1`, 일부 시험 `SEL=1,2,3`, 그림 없을 때 시험용 `FALLBACK=1`). 로그 `fallback art 0` 확인.
5. `tools/motion_check.py`(20-4)·시험 렌더로 확인 후 푸시.

**구조**
- 의미 단위: 문장→쉼표→단어 순으로 쪼개 최대 길이(기본 9.3초 = 6.2×PACE 1.5, 20-2) 이하로 합침. 1.6초 미만 단위는 이웃과 합치고, 장면 마지막 단위가 2초 미만이면 경계를 다시 나눈다.
- 컷 = `div.t`(전환) 안 `div.w`(카메라) 안 SVG. id에 `u<번호>_` 접두어. 장면 간격 0.8초, 앞 여백 1.0초, 끝 여백 2.5초(본편).
- 자막 줄: 문장 단위, 30자·7단어 이하(세로 22자·4단어), 쉼표에서 우선 끊음. 칠판은 레이아웃 B 3행.

### 15-7. 새 세션에서 시작하는 방법 (사용자는 대본만 보내면 된다)
- 도구는 `render-pipeline` 브랜치의 `tools/`(목록·사용법 `tools/README.md`), 영상별 원본은 `videos/<슬러그>/`(`script.py`, `art3/*.svg`+`*.json`, `plan.json`, `config.py`, `art_brief.md`, `thumb/`). 레포 구조 변경은 `docs/repo-changes.md`. 안내 파일 `CLAUDE.md`(자동으로 읽힘), Claude 프로젝트 채팅용 짧은 지침 `docs/project-instructions.md`.
- **시작 순서**: ① `list_repos` → `add_repo`(access: push) ② `git clone --depth 1 -b render-pipeline …` ③ `tools/README.md` 순서대로 ④ 대본을 받으면 `videos/<슬러그>/`(`script.py`는 12-1 사실 확인 뒤의 영어 내레이션, `art3/`는 하위 에이전트, `config.py`·`thumb/`는 예시를 따라).
- 렌더 시작 파일(`render/.chunked` 또는 `render/.slug`)은 내가 적는다(사용자 일이 아님).
- **이미 만든 영상의 모션만 바꾸기**: `python3 tools/restyle_motion.py render/<슬러그>`가 `index.html`을 현재 모션 규칙(19종, 빛 맥동, 이웃 도형 묶기, 칠판 글자 맞춤, 배지 카운트업, 스포트라이트, 자막 단어 강조)으로 바꾼다. `mix.m4a`·그림·자막·전환·카메라는 그대로(음성 `p01.wav…`은 저장소에 없어 전체 재빌드는 TTS부터). **빌드 원본(이 도구를 안 거친 파일)에만 쓴다**: 이미 패치된 파일은 건너뛰므로 규칙이 바뀌면 git에서 원본을 꺼내 다시 적용. 푸시하면 같은 Drive MP4를 덮어쓴다. 롱폼 동작은 미확인. 단위·그림 수를 바꾸는 다시 만들기는 21장.
