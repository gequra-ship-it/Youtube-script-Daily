## 21. 기존 영상 다시 만들기 (그림 재사용, 2026-10-17 사용자 결정)

사용자: "기존 이미지를 재사용해서 그림 그리는 건 줄이자", "토큰 관리 좀 하자".

### 21-1. 무엇을 바꾸나
- **롱폼**: 20-2 기본값·색 막대 없음·배지 유지·느린 장면 차분한 전환을 `build3.py`가 자동 적용.
- **숏츠**: 예전 1분짜리 2편 대신 **새 3편, 각 2:00~2:55**(19장). 사실 확인된 롱폼 대본 안의 사실만(새 사실 금지, 같은 단서 표현 유지), 제목·훅·소재 겹치지 않게. 7~9장면, 약 380단어(330~440, 19-1). `config.py`에 `HOOK = dict(until=999, maxu=6.0, slow=7.5)`.
- **사람**: 새 그림은 3-1의 스타일(art_spec 6A·6B). 예전 그림의 사람은 사용자가 요청할 때만 고친다(`tools/briefs/people_restyle.md`).
- **썸네일 3장**: 있는 시안은 그대로, 모자란 장만 만든다(16장).
- **Drive**: `.dest`를 `old/<영상>`에서 주제 폴더 다음 번호로(18장). 남은 `.skip_deliver`는 지운다(대본·메타데이터·썸네일이 안 올라감).

### 21-2. 순서 (명령)
1. 음성: 작업 폴더에 없으면 `SLUG=<slug> HYPERFRAMES_PYTHON=/home/user/kvenv/bin/python tools/tts.sh` 후 `SLUG=<slug> python3 tools/audio_prep.py`(롱폼 45문단 약 15분, 백그라운드), 그다음 `align.py`(21-5).
1-1. (새 영상) 음성 뒤 썸네일 3장 → 사용자 확인 → 통과 후 그림(12-1 순서).
2. 롱폼: `SLUG=<slug> python3 tools/remake.py` → 예전 `plan.json`을 `$MIYA_WORK/<slug>/plan_prev.json`에 두고 다시 나눈 뒤 `remap_art.py`가 가장 많이 겹치는 예전 그림을 붙이고 `.dest`·`.skip_deliver`를 점검. 출력의 `NO ART`와 `NEEDS VARIANT`(앞 단위와 같은 그림)만 그린다.
3. 숏츠 대본 3편(에이전트, Sonnet) → 음성 → `SLUG=<slug>-shortN VERT=1 PLAN=1 python3 tools/build3.py` → 그림(21-3).
4. 빌드 4개(`fallback art 0` 확인), `tools/gen_text.py`(대본·메타데이터), 썸네일 `tools/thumb_shot.py`.
5. `render/.chunked`에 `<slug> 3`과 숏츠 `<slug>-shortN 1` 세 줄, 커밋·푸시(20-7). 렌더 확인은 예약 메시지로.

### 21-3. 그림 에이전트
- 지시문 `tools/briefs/remake_art.md`(재사용 우선, 세로 옮기기, 확인 항목)에 영상별 할 일만 몇 줄 붙인다.
- **모델 나누기(CLAUDE.md)**: 사람·동물·생물이나 복잡한 구성 → Opus(`model: "opus"`), 단순한 것(도표, 물체, 풍경, 아이콘, 변형) → Sonnet(`model: "sonnet"`). 대본 쓰기도 Sonnet. 에이전트를 띄우기 전에 영상의 단위를 두 묶음으로 나눈다.
- 스타일·규칙을 많은 그림에 바꾸기 전에 테스트 2~4장으로 먼저 확인받는다.
- 동시에 3개까지, 각자 다른 파일만, git 금지. 확인은 묶음별 비교 접촉 시트 1장, 보고 8줄 이내.
- 세로 옮기기: 가로 그림을 0.85배로 줄이면 위아래가 비므로 1.1~1.2배로 키우고 가운데 물체를 (540,860)에, 양옆 무리를 안쪽·위아래로 옮기고 바닥·하늘을 화면 끝까지 잇는다.

### 21-5. 자막·그림·효과음 시간은 음성에서 잰다 (사용자 지적 2026-10-17: "자막과 음성 싱크가 맞을 때도 안 맞을 때도 있다")
- 예전 글자 수 비율 추정은 중앙값 0.35초, 상위 5% 0.84초, 최대 1.2초 어긋났다.
- `tools/align.py`가 문단 음성(`build/s<NN>.wav`)을 faster-whisper(small.en, CPU)로 인식해 **대본 단어마다 시작·끝 시간**을 `build/words.json`에 쓴다(대본을 초기 프롬프트로). difflib로 짝짓고, 짝 없는 단어는 그 구간 시간 폭에 글자 수 비율로 넣는다. `build3.py`의 `tchar`가 이 시간을 자막 줄·그림 전환·효과음·강조 단어·숫자 배지에 쓴다.
- **순서**: `tts.sh` → `audio_prep.py` → **`SLUG=<slug> python3 tools/align.py`**(문단 45개 약 4분) → `PLAN=1 build3.py` → 빌드. words.json이 없거나 대본 단어의 90% 미만만 맞은 문단이 있으면 `build3.py`가 문단 번호를 출력하고 멈춘다(`ALIGN_LOOSE=1`은 예전 추정으로 진행, 쓰지 않는다).
- **재시간 맞추기**: `plan.json`이 있으면 단위 나눔은 그대로 두고 시간만 새로 잰다. 새로 나누려면 `UNITS=new`(`remake.py`는 자동). 대본을 고쳤으면 `align.py`를 다시 돌리고 `UNITS=new`.
- 검증: 다른 모델(base.en)과 단어 시작 시간 차이 중앙값 0.06초, 상위 5% 0.2초.


(21-4 보고와 토큰은 docs/miyas-lab-guideline.md에 있다.)
