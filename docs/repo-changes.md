# 레포 구조 변경 기록 (요약)

브랜치 병합, 파일 합치기·이동·삭제처럼 레포 구조가 바뀐 일만 한 줄씩 적는다. 자세한 옛 기록(명령, 충돌 목록, 대응표)은 브랜치 `archive/miyas-lab-2026-10-24`의 `docs/archive/repo-changes-full-2026-10-18.md`. 영상 제작 규칙의 변경은 지침서 맨 위 결정 날짜 요약과 `docs/archive/guideline-full-2026-10-18.md`.

## 현재 구조
| 브랜치 | 내용 |
|---|---|
| `main` (기본) | 매일 대본 생성: `main.py`(6시), `main_owl.py`(7시), `main_이과형.py`(9시, KST) + 워크플로 `schedule.yml`·`schedule_owl.yml`·`schedule_igwahyung.yml`, 봇이 커밋하는 `scripts/`·`scripts_owl/`·`scripts_igwahyung/`. `docs/`·`tools/`는 `render-pipeline`의 사본. `render/`·`videos/`는 넣지 않는다(약 650MB) |
| `render-pipeline` | 영상 제작 원본: `tools/`, `docs/`, `videos/<슬러그>/`, `render/<슬러그>/`, 워크플로 `render-chunked.yml`(구간 병렬 렌더)·`render.yml`(`render/.slug`) |
| `claude/epic-ritchie-0mujsz` | 세션 작업 브랜치(`main`에 합쳐 쓰는 대본 도구용) |
- `cine-test/`(3D 보관)와 `docs/archive/`는 2026-10-24에 지웠다. 필요하면 브랜치 `archive/miyas-lab-2026-10-24`에서 꺼낸다.
- 일부러 합치지 않은 것: `videos/*/art_brief.md`(영상별 등장인물·장소 시트), `videos/*/STATUS.md`·`NEXT.md`(영상별 작업 메모), `tools/README.md`(사용법).

## 타임라인
- 2026-10-13: 브랜치 정리(작업 브랜치를 `render-pipeline`·`main`에 병합), 그림 명세 6개를 `tools/art_spec.md` 하나로 합침, 이 기록 파일 신설.
- 2026-10-14: `CLAUDE.md`·`docs/project-instructions.md` 신설. 시네마틱 3D(cine) 도구 추가 후 같은 날 SVG 도구를 모두 지우고 3D만 남기는 정리를 했다(옛 렌더 원본·옛 판 영상 폴더 삭제).
- 2026-10-15: 실제 3D 모델·실사 사진 시험 도구와 관련 워크플로 삭제(이질감, 깃 기록 `48f15d3`에 남아 있음).
- 2026-10-16: 사용자 결정으로 **SVG 모션그래픽 방식을 복원**(지운 SVG 도구·지침서를 새 커밋으로 되살림). 3D 문서·코드·영상을 `cine-test/`로 옮김. 새로 만듦: `tools/chunk_plan.py`, `build3.py`의 `HOOK`·드리프트 카메라·속도선·관절 모션, `tools/motion_check.py`.
- 2026-10-17: 다시 만들기 도구(`tools/remake.py`, `remap_art.py` NEEDS VARIANT, `tools/briefs/*`), 사람·손 그리기 도구(`tools/body.py`, `tools/hands.py`), 단어 단위 싱크(`tools/align.py`, `build3.py`의 `tchar`가 `words.json` 사용, 지침서 21-5).
- 2026-10-18: 이과형 채널 매일 대본(`main_이과형.py` + `schedule_igwahyung.yml`, 올라온 파일이 중간에서 잘려 `main.py`로 이어 붙이고 저장 폴더를 `scripts_igwahyung/`로 분리). 썸네일 도구·규칙(`tools/thumb_lib.py`, `tools/briefs/thumb_art.md`, `thumb_shot.py` A~F, 지침서 16-6·16-7). 문서 슬림화(`docs/archive/`에 전체 사본 보관).
- 2026-10-19: 모션 수정(사용자 지적: 풍차 날개 대신 탑 전체가 돎). `tools/motions.py`에 코어 타입 `turn`(그룹 하나만 회전, 이웃 도형을 묶지 않음), `tools/build3.py`에 `mv-rotor-<이름>`(`data-pivot`·`data-per`·`data-dir` 연속 회전) 추가. 지침서 4-1·`tools/art_spec.md` 7장에 '움직이는 부분이 있는 물체' 규칙. kardashev-scale 그림 19장(풍차·시계·나침반·스톱워치·계기판 등) 수정.
- 2026-10-22: 작업 순서를 대본 확인·수정 → TTS → 썸네일 → 그림 → 렌더로 고정하고 썸네일 3장은 사용자 통과/수정 확인 뒤에만 그림·업로드(12-1, 15-6, 16-6, 16-7, 21-2).
- 2026-10-22: 사용자 결정으로 가운데 원형 고정을 풀고(3-2) 전환 5종(`seam`·`diamond`·`page`·`zigzag`·`wave`)과 위치 제한 없는 객체 모션 12종을 추가(`tools/motions.py`, `build3.py`, 지침서 4-1·4-3, `art_spec.md` 7장). 20초 시험 영상 v8에서 확인.
- 2026-10-22: 대본 초반 5분을 질문·가정 상황·영화 장면 훅으로 재밌게 쓰는 규칙(지침서 10-2A)과 대본 생성 프롬프트 반영(`main.py`, `main_owl.py` 구성 항목).

- 2026-10-22: 제목·썸네일 규칙은 기존 유지(60자/3단어 개정안은 채택 안 함), `tools/title_lint.py`·`hookscore.py`·`hooks.json` 추가(출처 youtube-agent-skill, MIT), 사용한 대본은 `scripts/used/`·`scripts_owl/used/`로 보관(12-1).

- 2026-10-22: 지침서 분리(토큰 절약): `docs/miyas-lab-guideline.md`는 핵심 약 11KB, 장별 내용은 `docs/guideline/NN-*.md`(내용은 그대로, 21-4·12-1·0·1·11장은 핵심에). 분리 직전 전체본은 `docs/archive/guideline-2026-10-22-before-split.md`.

## 2026-10-22 (후속)
- `build3.py` `PACE = 1.5`: 컷 길이(최소·최대) ×1.5, config `PACE = 1`이면 예전 길이. 전환 풀은 중심 코어 물체가 없는 쌍에서 `match`·`zoom`을 뺀다.
- `motions.py` `miyaCruise`: 경로 객체와 트래킹 카메라는 일정 속도(양 끝 15%만 부드럽게).
- `tools/motion_preview.py`, `tools/briefs/scene_motion.md` 추가. 문어 영상 샘플 그림·새 plan은 브랜치 `octopus-sample-redraw`에만 있다(render-pipeline에 넣지 않음).

## 2026-10-24
- 곰 1분 시험 영상(v3, `/mnt/project-files/motion-demo/`)에서 승인된 것을 합침: `motions.py` 객체 모션 `slide`·`fade`·`ticks`·`rack`·`popin` axis, 트래킹 world 크기 분리(`miyaTrack` WW/WH), `build3.py` 사이드카 `world`, 새 `tools/rhythm.py`(거의 무음 구간·전환 강조)와 `bgm_lib.synth(accents=)`. 지침서 4-1·9-5, `art_spec.md` 7·8장. 불채택: 로그 줌, 끊기는 스크롤, 정지 화면·속도 램프(미구현).
- `tools/paths.py` `chrome()`: 하드코딩된 chromium 경로를 쓰던 도구 6개가 설치된 크로미움을 자동으로 찾음.

- 2026-10-24 새 채널 Miya's Note: 채널명 치환(지침서·도구·`main.py`·`main_owl.py`), 롱폼 15분 이내(2,000~2,300단어), 숏츠 3→5편(`main.py`·`main_owl.py` 3부 5편 × 약 380단어, 19장), Drive `Miya's Note/NN_<슬러그>`(18장). 이미 만든 대본·`videos/*/config.py` 해시태그는 아직 안 바꿈.
- 2026-10-24: 납품물을 영상·썸네일·메타데이터 txt로 줄임(대본 txt·렌더 리포트 제외; 리포트 업로드를 끄는 워크플로 수정은 렌더가 시작될 수 있어 보류). 메타데이터는 제목·1~2문장 설명·타임라인·해시태그만(`tools/gen_text.py`), 제목 기준 개정(짧게 약 50자, 질문형 불필요, 직관/은유 자유, 17장, `title_lint.py`).
- 2026-10-24: 내레이션 목소리를 Kokoro `am_michael`(남성) → `af_heart`(여성)로 변경(miya 선택; `tools/tts.sh`, `gen_text.py`, 지침서 9·14장). 이미 만든 음성은 옛 목소리라 새 영상부터 적용.
- 2026-10-24: 본문 대본·`main*.py` 프롬프트에서 마지막 구독 요청 제거(고정 아웃트로와 중복, 지침서 10-5). 이미 쓴 대본 파일의 구독 문장은 개편 때 함께 정리.
- 2026-10-24: 롱폼 고정 아웃트로(지침서 9-6): `paths.load_scenes`가 장면 `OUTRO`를 붙임, `tools/assets/outro.wav`·`outro.svg`, `tts.sh`·`build3.py` 처리. 시험 빌드(2장면 샘플)로 장면 길이 약 9.9초 확인, 전체 영상 렌더는 아직 안 함.
- 2026-10-24: 썸네일에 노트 개구리 필수(지침서 16-8, `tools/briefs/thumb_art.md`, `tools/assets/frog.svg`).
- 2026-10-24: Drive 새 경로 `Miya's Note/<01. Life & History | 02. Space & Science>/NN_<슬러그>`(miya가 폴더 생성, 18장), 숏츠 3→5 문구 정리(21장, README), render-report 업로드 제거는 다음 렌더 때.
- 2026-10-24: 렌더 워크플로(`render-chunked.yml`·`render.yml`)에서 `_render_report.txt` Drive 업로드 줄 제거(miya 요청), `render/.chunked`는 주석만 둠(옛 영상 렌더 방지; 푸시로 시작되는 실행은 렌더할 슬러그가 없어 바로 실패/종료).
- 2026-10-24: `render-pipeline`의 옛 대본 복사본(`scripts/`, `scripts_owl/`)·`main.py`·`main_owl.py`·`schedule*.yml` 삭제(진짜 대본·매일 대본 코드는 `main`).
- 2026-10-24 (miya 요청, 카드로 확인): 새 대본으로 새로 만들기 위해 `render-pipeline`에서 옛 영상 `videos/*`(89개)·`render/<슬러그>/`(`sample`·`.slug`·`.chunked` 제외)·`cine-test/`·`docs/archive/`를 지움. 전체 사본은 브랜치 `archive/miyas-lab-2026-10-24`, 옛 작업 브랜치는 `archive/octopus-*`. `.chunked`가 옛 슬러그를 가리키니 새 영상 렌더 때 갱신한다. (git 기록 크기는 그대로, 기록 재작성 안 함.)
- 2026-10-24: 설명하는 개구리 파이프라인(지침서 7-2, `tools/frog.py`, `build3.py`: 칠판 자동·그림 사이드카 `frog`, `plan.json`의 `frog_hint`, art_spec 12). 고정 아웃트로 그림의 개구리 찌그러짐 수정. 대본 파일명 날짜 = 생성일(`main*.py`).
- 2026-10-24: 메타데이터에 출처(SOURCES)는 유지(출처가 있을 때만).
- 2026-10-25: 개구리 도구 정리(`tools/frog_place.py` 신설: 그림 장면 개구리 배치, `tools/frogshot.py`: 시간 이동 프레임 확인, `frog.py`: ride·팔 추적·표정·복장), 로고 교체(`tools/assets/logo.png`), `build3.py` 최소 화면 시간 기본값 8.5초. 임시 도구(`frog_auto.py`, `frog_obj.py`, `frog_auto2.py`)는 `frog_place.py`로 합치고 지움.
- 2026-10-25 (miya, 고래 낙하 영상 검수): ① `tools/motions.py` `miyaPv`/`miyaM`: `data-pivot`(chain·joint·rotor 등)을 부품의 부모 좌표로 바꿔 쓰고, 에이전트가 감싼 그룹 안 좌표로 쓴 경우는 부품에 더 가까운 쪽을 고른다(꼬리가 몸통과 따로 도는 문제), `miyaPath`도 같은 변환 ② `mv-path-*` id에 sink|fall|drop|plunge|descen|carcass가 있으면 카메라가 따라가지 않는다(따라가면 낙하가 멈춰 보임), 새 도구 `tools/fallwrap.py`(오브젝트 전체를 낙하 경로 그룹으로 감쌈)·`tools/pivcheck.py`(회전축 검사) ③ `frog.py`: 복장 `diver`(잠수복), 그림 속 개구리는 말 입 모양 동기화 끔(`talk`, 칠판만), `frog_place.py`: 심해 단어면 diver·수면은 goggles, 구석 자리 4곳 순환, `build3.py` `FROG_HINT`: 약 4번째 그림마다(상한 26 %). 지침서 7-2·헤더 결정·art_spec 7.

- 2026-10-25: 개구리 상황별 행동(`act`)·표정 추가 — `tools/frog.py`(`_ac` 그룹, 모션 8종, 표정 scared·squint·sleepy), `tools/frog_place.py`(단어로 act 선택), 지침서 7-2. stolen-time 6편에 적용(miya 요청).

- 2026-10-25: 그림 속 개구리 오른팔이 안 보이던 문제 수정 — `tools/frog.py`에 짧은 오른팔 `_ra` 추가(가리키지 않을 때 표시), 지침서 7-2. 다른 영상은 `frog_place.py` 없이 `build3.py`만 다시 돌리면 적용된다.
- 2026-10-26: 개구리가 배경을 돌아다니고(`frog.roam`: swim·lie·tumble·roll·run·moonhop·walk, 상황별 선택, 러닝머신 등 발판 위에서 점프) 머리 위 말풍선·소리 단어를 붙임(`frog.says`). `tools/frog.py`·`frog_place.py`, 지침서 7-2. 바람 줄 표현 삭제.

- 2026-10-26: 개구리 상황별 규칙 추가 — 블랙홀로 끌려가는 물체에 탄 개구리는 작아져 사라짐(`vanish`), 로켓·우주선 말이 나오면 날개 옆에 붙음(`VEH`), `pull`·`wind` 모션 부드럽게(지침서 7-2).
- 2026-10-26: `tools/frog_place.py` `pull` 규칙에서 sink·crush 제외(가라앉는 고래·수압은 빨려드는 상황이 아님, crush는 shiver로), `tools/clip_prep.py`(어느 구간이든 20초 샘플 렌더: `python3 tools/clip_prep.py <slug> <시작초> <길이>` 후 `npx hyperframes@0.8.141 render`, 오디오는 ffmpeg -ss로 합침).

- 2026-10-26: 개구리 `fore` 복장, `dizzy` 표정·동작, `doodle` 동작(연필 낙서) 추가(`tools/frog.py`, 지침서 7-2).
- 2026-10-26: 개구리 등장 비율을 약 26%→50%로 늘림(`build3.py` FROG_HINT: 2단위마다, 처음 4초 이후), ride 개구리가 화면 위로 잘리지 않게 위치 하한(`frog_place.py`). 지침서 7-2.

- 2026-10-26: 개구리 `push`·`huts` 동작, `fore_steps` 복장(부분 켜기), `says.t`(`tools/frog.py`, 지침서 7-2).
- 2026-10-26: 개구리 `dizzy`(입자 그룹을 타고 돌며 어지러워함)·`orbit`(블랙홀 고리를 입자처럼 돎) 동작과 `dizzy` 표정 추가, `pull`/`orbit`의 좌우 반전 위치 오류 수정(`tools/frog.py`, `frog_place.py`, 지침서 7-2).
- 2026-10-26: 사건의 지평선 고리를 도는 개구리(`orbit`, `mv-edge-horizon` 장면은 힌트 없이도 등장), stolen-time U060의 우주인을 우주복 개구리로 교체(손으로 쓴 `lock` 사이드카). `frog.py`·`frog_place.py`, 지침서 7-2.
- 2026-10-26 (miya, 고래 롱폼 검수: "의미 없이 하단에 나오는 개구리가 많다"): `tools/frog_place.py` 의미 게이트: 탈 오브젝트가 없는 배경 개구리는 강한 상황(pull·wind·shiver·awe·orbit·dizzy, 달리기·구르기)일 때만 둔다(waves·sleepy·cheer만으로는 제외). 그림이 끝나면 기존 개구리 사이드카를 지우고(`lock` 제외) `frog_place.py`를 다시 돌린다.
