# 레포 구조 변경 기록

브랜치 병합, 파일 합치기·이동·삭제처럼 레포 구조가 바뀐 일을 적는다. 영상 제작 규칙의 변경은 `docs/miyas-lab-guideline.md`의 개정 이력에 적는다.

---

## 2026-10-14 옛 시험 렌더 폴더 5개 삭제 (사용자 결정)

- 지운 폴더(`render/` 아래, 합계 약 86MB): `never-eat-human-meat`, `never-eat-human-meat-v2`, `never-eat-human-meat-v3`, `never-eat-human-meat-short`, `epomis-frog-hunter`. 모두 새 방식으로 다시 만든 영상(`never-eat-human-meat-v4`와 숏츠, `epomis-frog-hunter-v2`와 숏츠)으로 대체된 시험 렌더이고, Drive에 대응하는 폴더가 없다.
- `videos/<슬러그>/`(대본·그림·설정)는 그대로 둔다.
- 내레이션 음성은 `render/<슬러그>/n##.m4a`에만 있고 `videos/`에는 없다. 그래서 지운 5개의 음성은 이 시점 이후 git 기록에서만 복구할 수 있다. 남긴 영상의 `render/` 폴더를 지우면 음성이 사라진다.
- 렌더는 시작되지 않는다(`render/.slug`, `render.yml`, `render/sample/**` 변경 없음).

---

## 2026-10-14 `CLAUDE.md`와 프로젝트 지침 문구 추가 (사용자 결정)

사용자 판단: 프로젝트 채팅도 깃 커넥터로 레포를 보고 렌더를 돌리므로, 프로젝트에 지침서 전문을 넣을 필요가 없다 → 지침서는 레포 한 곳(`render-pipeline`의 `docs/miyas-lab-guideline.md`)에서만 관리한다.
- `CLAUDE.md`(레포 최상위, 새로 만듦): Claude Code 세션이 시작할 때 자동으로 읽는 안내. 먼저 읽을 파일, 브랜치 역할, 렌더가 시작되는 조건과 Drive 경로 주의, 항상 지킬 규칙.
- `docs/project-instructions.md`(새로 만듦): Claude 프로젝트 설정의 "지침"에 붙여 넣는 짧은 문구의 원본. 작업 전에 깃 커넥터로 지침서를 끝까지 읽게 하고, 다 읽지 못하면 먼저 알리게 했다.
- 지침서 15-7에 `CLAUDE.md` 안내 한 줄 추가.
- 두 브랜치(`render-pipeline`, `main`) 모두에 같은 내용을 넣음.
- 확인하지 못한 것: 프로젝트 채팅의 깃 커넥터가 지침서(약 128KB)를 잘리지 않고 끝까지 읽는지. `docs/project-instructions.md` 끝의 확인 방법으로 사용자가 확인한다.

---

## 2026-10-13 브랜치 정리와 그림 명세 합치기 (사용자 결정)

사용자 요청: "브랜치 두 개 합치고, 여기저기 흩어져 있고 중복된 md 파일 합치기" → 추천안(아래 1)으로 진행, 그림 명세 6개를 하나로 합치고, 이 기록 파일을 만들고, 진행 중인 재렌더(실행 #50~#57)가 끝난 뒤 예약 실행으로 병합한다.

### 1. 브랜치

**정리 전**

| 브랜치 | 내용 | 비고 |
|---|---|---|
| `main` | 매일 대본 생성(`main.py`, `main_owl.py`, `scripts/`, `scripts_owl/`), 워크플로 `schedule.yml`·`schedule_owl.yml` | 기본 브랜치. 예약(cron) 워크플로는 GitHub 규칙상 기본 브랜치에서만 돈다. 봇이 매일 대본을 커밋한다. 약 1.2MB |
| `render-pipeline` | 영상 제작 도구(`tools/`), 지침서 사본(`docs/`), 영상별 원본(`videos/`), 렌더 원본(`render/`), 워크플로 `render.yml` | `render.yml`은 이 브랜치에 푸시할 때(그리고 `render/.slug`·`render.yml`·`render/sample/**`이 바뀔 때)만 렌더한다. 약 654MB(`render/` 548MB, `videos/` 101MB) |
| `claude/epic-ritchie-0mujsz` | 2026-10-13 세션의 작업 브랜치: `main.py`·`main_owl.py` 프롬프트를 지침서 기준으로 변경, `docs/`·`tools/` 수정(모션 19종, 카운트업, 스포트라이트, 자막 하이라이트, 칠판 맞춤, 패치 도구, 이 정리) | `main`에서 갈라졌다 |

**정리 방법(추천안)**: 작업 브랜치를 `render-pipeline`과 `main` 양쪽에 병합하고 작업 브랜치는 지운다.
- `main`에 넣는 이유: 매일 대본 생성이 새 프롬프트로 돌게 하려면 `main`에 있어야 한다.
- 전부 `main`으로 합치지 않은 이유: `main`이 렌더 파일 654MB를 떠안으면 매일 대본 작업 두 개가 실행마다 그만큼 받아야 하고, `render.yml`의 트리거도 바꿔야 한다.
- 병합 결과 `main`에는 `docs/`·`tools/`(약 5MB)가 추가되고 `render/`·`videos/`는 들어가지 않는다. `render-pipeline`에는 `main.py`·`main_owl.py`·`schedule_owl.yml`·`scripts/`·`scripts_owl/`가 추가된다(렌더와 무관, 크기 작음).
- 시험 병합(작업 브랜치 → `render-pipeline`, 푸시 안 함): 충돌 0건, `render/.slug`와 `render.yml`은 바뀌지 않음(병합 푸시로 렌더가 새로 시작되지 않음).

**실행 결과** (2026-10-13 14:07~14:20 UTC, 예약 실행)
- 사전 조건: 재렌더 #50~#57이 모두 성공으로 끝난 뒤 실행(마지막 cosmic-prison #50이 13:56 UTC 완료). `render-pipeline`의 `docs/`·`tools/`가 작업 브랜치 `ec1b430`과 같음을 확인.
- `render-pipeline`: 병합 커밋 `b71dd1e`(이전 `4b46670`). 충돌 3건(`docs/miyas-lab-guideline.md`, `tools/README.md`, `tools/art_spec.md`, 모두 양쪽 추가 AA)은 작업 브랜치 쪽을 택함. 옛 명세 5개(`art_spec_v2/v3/v3_vertical/v4_backdrop/cosmic.md`)는 git 기준으로 이 브랜치만 추가한 파일이라 병합 후에도 남아서 따로 삭제. `render/.slug`·`render.yml`은 바뀌지 않음.
- 옛 명세 이름을 고친 영상별 문서 11개: `videos/carnian-rain`, `cosmic-prison`, `desert-oasis`, `dinosaur-restorations`, `epomis-frog-hunter-v2`, `left-handed-ten-percent`, `never-eat-human-meat-v4`, `paleozoic-chronicles`, `ribeiroia-monster-frogs`, `stolen-time`, `whale-fall`의 `art_brief.md`. 다른 세션의 절대 경로(`/home/claude/youtube-script-daily/tools/...`)도 레포 기준 경로로 바꿈.
- `main`: 작업 브랜치로 빨리 감기(`e8d7dd3` → `5e99cf4`). 들어간 것은 `docs/`·`tools/`(약 5MB)와 `main.py`·`main_owl.py` 프롬프트 변경. `render/`·`videos/`는 들어가지 않음. 매일 대본 생성(예약 실행)은 다음 실행부터 새 프롬프트를 쓴다.
- 재렌더 결과(같은 날 실행 #50~#57, 13종 기준 #42~#49는 중단): 8개 주제 모두 성공, Drive의 MP4 24개(롱폼 8, 숏츠 16)가 12:42~13:56 UTC에 같은 파일로 덮어써짐(파일 ID·생성일 유지). `Video & Thumbnail` 루트에는 분류 폴더 2개(`Space & Science`, `Life & History`)뿐이라 엉뚱한 새 폴더는 생기지 않음.
- 작업 브랜치 `claude/epic-ritchie-0mujsz` 원격 삭제: **실패**. `git push origin --delete`가 두 번 모두 "the remote end hung up unexpectedly"로 끝났다(지침서 15-5 오류 대응에 적힌 것과 같은 증상). 브랜치 내용은 `main`(`5e99cf4`)과 `render-pipeline`(`b71dd1e`)에 모두 들어 있어 지워도 잃는 것이 없다. 사용자가 GitHub에서 직접 지운다(저장소 → Branches → 휴지통 아이콘).

### 2. 그림 명세 6개 → `tools/art_spec.md` 하나

그림 에이전트에게 주던 명세가 덧칠 구조("v3가 v2와 다르면 v3 우선", "cosmic이 v2/v3/v4보다 우선")로 6개 파일에 나뉘어 있었다. 코드(`.py`, `.sh`, 워크플로)는 이 파일들을 읽지 않는다(참조 0건). md 파일끼리 파일 이름으로 가리키고, 에이전트에게 이름으로 넘겨준다.

| 옛 파일 | 새 위치 |
|---|---|
| `tools/art_spec.md` (v1, 첫 화풍) | `tools/art_spec.md` 부록 B (옛 화풍, 첫 영상 재현용) |
| `tools/art_spec_v2.md` | 2절(파일 규칙), 3절(화풍), 4절(가운데 물체), 6절(구도), 7절(모션 그룹), 9절(확인) |
| `tools/art_spec_v3.md` | 1절(그릴 것), 2절, 3절(배경 모드·팔레트), 4절(match 전환), 6절, 7절, 8절(사이드카·효과음·화면 텍스트), 9절(작업 방법) |
| `tools/art_spec_v3_vertical.md` | 10절(숏츠) |
| `tools/art_spec_v4_backdrop.md` | 5절(배경 규칙), 부록 A(기존 그림 배경 고치기) |
| `tools/art_spec_cosmic.md` | 11절(우주 모드, 한국어 원문을 영어로 옮김) |

**합치면서 정리한 충돌·낡은 내용** (뒤 문서와 지침서가 우선이라는 원래 규칙대로)
- v2 "종이 8장·밤 8장 이상, 나머지 노을" → v3대로 `plan.json`의 `bg`를 따른다.
- v2 노을 색 고정(복숭아→분홍→보라) → 팔레트의 `dusk_stops`.
- v2 "카메라가 1.04~1.22배로 천천히 흐른다" → 포커스가 없으면 카메라 정지(v3, 지침서 4-1).
- v2 파일 크기 600KB → 그림 하나 120KB(v3), 숏츠 100KB.
- v2 안에 `mv-hand` 규칙이 두 줄(제자리 ±5° / 10px 들어올림 ±6°) → 지침서 4-1의 ±5°·들어올림 없음(2026-10-11 수정).
- v1 `mv-arm` ±14° 0.9초 → ±7° 1.4초, 어깨 축(부록 B에 옛 값으로만 남김).
- v3 효과음 목록에 남아 있던 `riser`·`sweep` → 삭제(2026-10-12에 파도 소리 같아서 뺌).
- cosmic "13종" → 19종(2026-10-13).
- v4 "`mv-glint-core` 그룹을 유지" → `mv-core-*` 또는 `mv-glint-core`.
- 모션 그룹 개수: v2 "장면당 3~6개", v3 "그림당 1~4개", cosmic "4~8개" → 그림당 1~4개, 우주 모드 4~8개.
- 사이드카에 `spot`(스포트라이트 끄기)과 숫자 배지 카운트업 설명 추가(2026-10-13 기능).
- 다른 세션의 임시 경로(`/home/claude/vid3/...`, `/home/claude/ht/...`, 참고 영상 프레임 `/tmp/...`) → 레포 기준 경로(`videos/<slug>/art3/`, `tools/svgshot.py`). v2가 가리키던 참고 영상 프레임 파일은 레포에 없어 경로를 뺐다.

**참조를 고친 곳**: `docs/miyas-lab-guideline.md`(개정 이력 밖의 8곳), `tools/README.md`(6곳). 개정 이력의 옛 파일 이름은 과거 기록이라 그대로 두었다(위 대응표로 찾는다). `render-pipeline`의 영상별 `videos/*/art_brief.md`에 있는 옛 이름은 병합 때 고친다(실행 결과에 적음).

### 3. 일부러 합치지 않은 md 파일

| 파일 | 이유 |
|---|---|
| `videos/*/art_brief.md` (11개) | 영상마다 내용이 다른 등장인물·장소 시트. 중복이 아니다 |
| `videos/never-eat-human-meat-v4/NEXT.md`, `videos/stolen-time/STATUS.md` | 영상별 작업 메모. 아무 데서도 참조하지 않지만 그 영상의 진행 기록이라 남겼다 |
| `docs/miyas-lab-guideline.md` | Claude 프로젝트 지식 파일의 사본. 레포에서 고치면 프로젝트 파일도 교체해야 한다 |
| `tools/README.md`, `README.md` | 도구 사용법과 레포 소개. 역할이 다르다 |

---

## 2026-10-14 시네마틱 3D(cine) 도구 추가 (사용자 결정)

| 추가 | 역할 |
|---|---|
| `tools/cine/cine.js`, `cine.css`, `assets/` | 실행 라이브러리: 장면 모듈 등록, WebGL 합성 단계(톤 매핑·전환 10종), HUD, 글자 층, 데이터 카드, 자막. Three.js r169(MIT), GSAP, Lora·Inter(OFL) |
| `tools/cine/scenes/*.js` | 3D 장면 라이브러리 |
| `tools/build_cine.py` | `videos/<slug>/cine.json` + build_data → `render/<slug>/index.html` |
| `tools/build3.py` `CINE=1` | 그림 없이 음성·자막·효과음·음악과 build_data만 만드는 모드 |
| `tools/cineshot.py` | 미리보기·프레임당 시간·구간 수 추정 |
| `tools/cine_spec.md` | 3D 장면·cine.json 작성 명세(에이전트용) |
| `.github/workflows/render-chunked.yml`, `tools/chunk_prep.py`, `render/.chunked` | 구간 동시 렌더 후 합치기 |
| `render/proto-cine`, `render/proto-cine2`, `render/test-3d`, `render/cine-test` | 시험 렌더 원본(Drive `_ci-test/`) |

예전 SVG 방식(`tools/art_spec.md`, `tools/build3.py` 기본 모드, `render.yml`, `render/.slug`)은 그대로 둔다(예전 영상 재렌더용).

