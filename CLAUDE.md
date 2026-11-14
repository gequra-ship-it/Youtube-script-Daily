# Miya's Note 레포 안내 (Claude가 세션 시작 때 읽는 파일)

> 최종 수정: 2026-11-14 · 이 파일은 요약과 길잡이다. 규칙의 원본은 지침서이고, 이 파일과 지침서가 다르면 지침서가 우선이다.

영어 지식 유튜브 채널 Miya's Note의 대본 생성·영상 제작·렌더 레포다. **영상 작업(대본 → 음성 → 썸네일 → 그림 → 렌더 → Drive)을 하기 전에 지침서 핵심 파일을 끝까지 읽고 따른다.**

## 먼저 읽을 파일

| 파일 | 내용 |
|---|---|
| `docs/miyas-lab-guideline.md` | 지침서 핵심(항상 읽는다). 맨 아래 표에서 지금 단계에 해당하는 장만 `docs/guideline/`에서 읽는다 |
| `tools/README.md` | 도구 목록·사용법, `videos/<slug>/` 폴더 구성 |
| `tools/art_spec.md` (+ `videos/<slug>/art_brief.md`) | 그림 에이전트 명세 |
| `tools/briefs/` | 에이전트 지시문(썸네일 `thumb_art.md`, 리메이크 `remake_art.md` 등) |
| `docs/repo-changes.md` | 레포 구조 변경 기록 |
| `docs/project-instructions.md` | 프로젝트 채팅 설정에 붙이는 짧은 지침의 원본 |

## 브랜치

| 브랜치 | 역할 |
|---|---|
| `render-pipeline` | 영상 제작의 원본. `tools/`, `docs/`, `videos/`(영상별 원본), `render/`(렌더 원본), 렌더 워크플로 |
| `main` | 매일 대본 생성. `generators/daily.py`·`owl.py`·`igwahyung.py`, 워크플로 `schedule*.yml`, 대본 `scripts/<daily|owl|igwahyung>/`(각 폴더에 `history.txt`, `used/`). `docs/`·`tools/`·이 파일은 사본 |
| `archive/miyas-lab-2026-10-24` | 옛 Miya's Lab 영상·3D 실험·옛 문서 보관. 고치지 않는다 |

- 두 브랜치는 합치지 않는다. `docs/`·`tools/`·`CLAUDE.md`를 고치면 `render-pipeline`에 먼저 넣고 `main`에 같은 내용을 넣는다.
- `main`에 `render/`·`videos/`를 넣지 않는다(매일 대본 작업이 실행마다 그만큼 받게 된다).
- 예약 워크플로는 기본 브랜치인 `main`에서만 돈다.
- 보관 브랜치에서 꺼낼 때: `git checkout archive/miyas-lab-2026-10-24 -- <경로>`.

## 폴더 (`render-pipeline`)

| 폴더 | 내용 |
|---|---|
| `tools/build/` `check/` `fix/` `preview/` `writing/` | 실행 도구(용도별) |
| `tools/*.py` | 공용 라이브러리(`motions`, `frog`, `fxlib`, `paths` 등)와 `chunk_prep.py` |
| `tools/assets/` | 공용 렌더 자산(GSAP, 글꼴, 로고, 질감). 렌더 폴더에는 링크로만 들어간다 |
| `videos/<slug>/` | 영상별 원본(`script.py`, `config.py`, `plan.json`, `art3/`, `thumb/`) |
| `render/<slug>/` | 렌더 원본(`index.html`, `mix.m4a`, `deliver/`, 제어 파일) |
| `docs/guideline/` | 지침서 장별 파일 |

## 렌더 주의 (되돌리기 어려움)
- `render-pipeline` 푸시에서 아래 파일이 바뀌면 GitHub Actions 렌더가 **바로 시작**되고 Drive의 같은 이름 파일을 덮어쓴다. 의도하지 않았다면 건드리지 않는다.

| 파일 | 뜻 |
|---|---|
| `render/.chunked`의 `<slug> <구간 수>` | 구간 병렬 렌더 뒤 Drive 업로드(20-7) |
| `render/.chunked`의 `<slug> 0` | 렌더 없이 `deliver/`(썸네일·메타데이터)만 업로드 |
| `.github/workflows/render-chunked.yml` | 워크플로 자체. 고치는 푸시도 `.chunked`의 줄을 전부 실행한다 |

- `.chunked`의 모든 줄이 푸시마다 다시 실행된다. 끝난 영상의 줄은 지운다(15-5).
- 구간 수는 `python3 tools/build/chunk_plan.py render/<slug>`. `final_check`를 통과한 빌드(`.checked`)에만 사양을 내놓는다.
- Drive 경로는 `render/<slug>/.dest`(18장): `Miya's Note/<01. Life & History | 02. Space & Science>/NN_<slug>`, 숏츠는 그 아래 `short/`. 폴더 이름이 바뀌면 `.dest`도 바꾼다.
- 병렬로 여러 영상을 만들 때는 Drive 폴더 번호와 `render/.chunked`가 겹치지 않게 푸시 전에 rebase한다.
- 이미 만든 영상에 새 모션 규칙만 적용: `frog_place.py <slug>` → `build3.py` 재실행(7-2 H). `restyle_motion.py`는 빌드 원본에만(15-7).
- 비밀값(`RCLONE_CONF`, API 키)은 읽거나 출력하지 않는다.

## 항상 지킬 것

| 주제 | 규칙 | 지침서 |
|---|---|---|
| 언어 | 영상에 들리고 보이는 것(내레이션, 자막, 화면 텍스트, 칠판)은 영어만. 채널명은 "Miya's Note" | 0장 |
| 작업 순서 | 대본 확인 → TTS → 썸네일 3장(사용자 통과 뒤에만 다음) → 그림 → 렌더 | 12-1 |
| 사실 확인 | A~D 등급. 존재하지 않는 사례·연구·숫자·인용·인물을 지어내지 않는다 | 12-1 |
| 확인 표시 | 확인하지 않은 것을 확인했다고 쓰지 않는다. "확인 / 미확인" 구분을 유지한다 | 21-4 |
| 보고 | 단계마다 알리지 않는다. 최종 렌더가 Drive에 올라갔을 때, 질문받았을 때, 결정이 필요할 때만 1~3줄. 수정은 예시 이미지 몇 장으로 먼저 확인받는다 | 21-4 |
| 음성 | Kokoro `am_michael`, 분당 약 145단어. 본편 15분 이내(약 2,000~2,100단어) + 숏츠 5편(각 2:00~2:55) | 9-2, 19장 |
| 썸네일 | 롱폼은 서로 다른 소재 3장(A·B·C), Opus 에이전트가 만들고 사용자 확인. 숏츠는 편당 세로 1장, 스타일 B, 확인 없이 납품 | 16-6, 16-9 |
| 사용한 대본 | 렌더를 올릴 때 `main`에서 `scripts/<종류>/used/<슬러그>__<원래 파일명>.txt`로 옮긴다. 원문 그대로, 슬러그당 하나. `tools/check/used_check.py <슬러그>`가 OK | 12-1 |
| 코드 규칙 | 개구리·오브젝트·배경·텍스트·전환·소리 연출은 대본 단어 + 그림 증거(그룹 이름·크기·팔레트) + 단위 번호로 코드가 정한다. 모델이 임의로 고르지 않는다. 바꾸려면 사이드카 `lock` 또는 코드와 지침서를 함께 고친다 | 4장, 7-2, 9-3·9-4 |
| 그룹 이름 | 그림 에이전트는 오브젝트 그룹에 뜻이 드러나는 이름을 붙인다(머리 명사 마지막). 비·눈·입자·개구리는 그리지 않는다 | 4-8, art_spec 7 |
| 반복 | '연속 사용 금지' 고정 규칙은 없다. 상황이 이어지면 같은 효과를 또 쓰고, 채움 선택만 직전과 다르게 | 4장 공통 원칙 |
| 축·붙임 | 움직이는 부분은 몸에 붙어 있고 `data-pivot`은 닿는 점. 축은 그룹 이름으로 `axisfix.py`가 써 준다. 가닥(촉수·다리)은 하나씩 따로 그룹 | 4-7, 4-8, 4-12 |
| 그림 에이전트 점검 | `axisfix` → `splitlimbs` → `partaxis` → `attachcheck`가 0이어야 보고 | 4-12 5번 |
| 최종 점검 | 메인은 렌더 푸시 전에 `SLUG=<slug> python3 tools/check/final_check.py`. 사용자가 짚은 장면은 `tools/preview/motionaudit.py` 띠 이미지를 눈으로 본다 | 15-8 |
| 렌더 멈춤 | `CustomWiggle`·문자열 `wiggle()` ease 금지(`fxlib.miyaW`/`miyaJit`만). 렌더 뒤 청크 MP4를 `tools/check/freezecheck.py`로 확인한 다음에 완료로 알린다 | 15-8 |
| 등장 모션 | 시작 전에 숨겨야 하는 모션은 `tl.set`으로 먼저 숨긴다 | 4-15 |
| 센터 모션 | 사건 종류(heartbeat·swell 등)는 단어·이름이 있을 때만, 종류별 ≤ 15 %. 빠른 박동 ≤ 10 % | 4-13, 4-14 |
| 개구리 | 칠판에서만 설명. 그림 장면은 이유가 있을 때만 나오고, 주인공 한가운데 위에 앉히지 않고, 맥동 오브젝트는 타지 않고 옆에서 반응. 그림 뒤 `tools/build/frog_place.py <slug>` | 7-2 |
| 다양성 | 테마 팩 소품·구도, 4~6장마다 움직이는 소품 1장. `variety_check.py`가 최종 점검에서 본다 | 4-10, 7-2 K |
| 손 | 손가락이 보이는 손은 `tools/figlib.py` `hand()` 12동작만 | 3-1 |
| 방향 | 이동·바람·빨림·시선·빛 방향은 코드가 맞춘다(`tools/facing.py`). 눈 없는 탈것은 `data-face` | 4-4 |
| 문서 유지 | 본문에는 지금 유효한 규칙만. 바뀌면 그 자리를 고쳐 쓰고, 이력은 장 맨 아래 한 줄, 최종 수정 날짜 갱신, 같은 값은 다른 문서도 같은 커밋에서. 구조 변경은 `docs/repo-changes.md` | 핵심 파일 맨 위 |

## Picture agents: model split and token budget
- Units with people, animals or other creatures, or a complex composition -> Opus agent (`model: "opus"`); simple units (charts, objects, landscapes, icons) -> Sonnet agent (`model: "sonnet"`). Split each video's units into these two groups before launching agents.
- Before changing a style or rule across many pictures, make 2-4 test pictures and get the owner's OK first.
- Agents check with one before/after contact sheet per batch and report in at most 8 lines.
- Remakes of existing videos reuse pictures: `tools/build/remake.py`, agent brief `tools/briefs/remake_art.md`, guideline section 21.

---

### 개정 이력
- 2026-10-16: SVG 방식 복귀. 2026-10-17 (사용자): 그림 에이전트 모델 나누기, 보고 절약.
- 2026-10-24: 새 채널 Miya's Note, 옛 영상·3D는 보관 브랜치로.
- 2026-10-26~11-11: 개구리·축·방향·소리·다양성·렌더 멈춤·`used/` 규칙 요약 추가(자세한 경위는 각 장 개정 이력).
- 2026-11-14 (miya): 레포 구조 개편 반영. 렌더 워크플로를 `render-chunked.yml` 하나로. 문서 유지 규칙 형식으로 줄임(20KB → 요약 표 + 장 번호).
