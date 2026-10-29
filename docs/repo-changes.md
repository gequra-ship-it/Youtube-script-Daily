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
- 2026-10-26: frog_place 자동 상황 규칙(dizzy·doodle·push·huts·fore)과 `FROG_TONE='serious'` 추가, 그림 규칙: 오두막 문은 `id="doorN"`(`tools/art_spec.md` 12, 지침서 7-2).
- 2026-10-26: 사건의 지평선 고리를 도는 개구리(`orbit`, `mv-edge-horizon` 장면은 힌트 없이도 등장), stolen-time U060의 우주인을 우주복 개구리로 교체(손으로 쓴 `lock` 사이드카). `frog.py`·`frog_place.py`, 지침서 7-2.
- 2026-10-26: U060 우주인은 그대로 두고 발 아래 우주복 개구리를 발판으로 배치(손으로 쓴 `lock` 사이드카), 입자 타기 자동 규칙(`PARTICLE`)을 `frog_place.py`에서 뺌, 지침서 7-2 정정.
- 2026-10-26 (miya, 고래 롱폼 검수: "의미 없이 하단에 나오는 개구리가 많다"): `tools/frog_place.py` 의미 게이트: 탈 오브젝트가 없는 배경 개구리는 강한 상황(pull·wind·shiver·awe·orbit·dizzy, 달리기·구르기)일 때만 둔다(waves·sleepy·cheer만으로는 제외). 그림이 끝나면 기존 개구리 사이드카를 지우고(`lock` 제외) `frog_place.py`를 다시 돌린다.
- 2026-10-26: 개구리 `fly`(슈퍼맨 자세 발판) 동작 추가(`tools/frog.py`), 지침서 7-2 ⑥⑧: 빨려듦 비명→지평선 고리 헤롱→발판 날기, 모든 영상에 대본·그림 상황별 적용.
- 2026-10-26: 개구리 기본 동작을 점프(cheer)·큰 출렁임(float)에서 차분한 `tilt`·`look`·`sway`·`nod`·`breathe`로 바꿈, cheer는 진짜 환호 단어일 때만(절반은 nod), 높이 -26→-16. `tools/frog.py`, `frog_place.py`, 지침서 7-2 ⑨.
- 2026-10-26: 개구리 `slide`(중력 구덩이로 미끄러짐) 추가, 차분한 기본 동작에는 항상 말풍선(`CALM`), 지침서 7-2 ⑩⑪(의미 있는 개구리만: 모션·상황·의상·말풍선·오브젝트와 이동 중 하나는 필수). `frog.py`·`frog_place.py`.
- 2026-10-26 (3차, miya): 개구리 관계 동작 10종·의상 4종·표정 3종·시선(`tools/frog.py`, `tools/frog_place.py`), 오브젝트 규칙 `tools/motions.py` `chalk_life_js`(칠판 행 사이 생기)·`settle_js`(일회성 모션 뒤 숨쉬기), `tools/build3.py` 유성(`is_cosmic`)·`mv-blink` 종류. 지침서 7-2 D-2, 4-1 '3차 보강', `tools/art_spec.md` 7·12장, `CLAUDE.md`. 4편 사이드카 재배치(`frog_place.py`), 렌더는 아직 안 돌림.
- 2026-10-26 (레포 정리, miya 위임): 구간 렌더 잔재 `render/eating-humans-deadly-bet__s0~2`(mp4 포함 30MB) 삭제, `render/stolen-time-short1~5`에 남아 있던 미사용 `sfx_*.wav` 465개 삭제(다른 영상 폴더처럼 `mix.m4a`에 이미 섞여 있음), 루트 `README.md`를 레포 안내로 교체. 도구 55개는 전부 다른 코드·문서에서 참조되어 그대로 둠.
- 2026-10-26 (4차, miya): `tools/motions.py`에 축 교정(`pivot_of`·`core_sanitize`·`obj_sanitize`), 오브젝트 모션 35종, 배경 효과 표(`PARTICLES`·`OVERLAYS`·`FX_WORDS`·`FX_AMBIENT`, 57종), `tools/labels_lib.py`에 텍스트 효과(`NAME_FX`·`SAY_FX`·`NUM_FX`·`label_js`·`badge_js`), `tools/frog.py`에 동작 26종·의상 56종(`SIMPLE_ACTS`·`OUTFITS2`), `tools/frog_place.py`에 그 단어 규칙, `tools/build3.py`에 연결(`motion sanity` 출력, 효과 마크업·JS, 라벨 효과). 지침서 4-1 '4차 보강'·7-2 D/E, art_spec 7(축 규칙). 데모 `/mnt/project-files/frog-rules/round4/`.
- 2026-10-26 (4차 추가, miya): 표정 20종 추가(`tools/frog.py` `MOODS` 34종, `face_js`, 별 눈 `_st`·이 `_th` 부품), 선택 규칙 `tools/frog_place.py` `MOODW`·`RIDE_MOOD`·`PAL_MOOD`·`PLAYFUL`. 지침서 7-2 F-0.
- 2026-10-26 (miya): 내레이션 목소리를 `af_heart` → `am_michael`(원래 남성)로 되돌림: `tools/tts.sh`, `gen_text.py`, `tools/README.md`, 지침서 9·14장, `tools/assets/outro.wav` 재생성. 10-24~26에 만든 4편은 af_heart 그대로. 아웃트로 음성 약 6.4초(전 5.9초, `build3.py` 주석 갱신). 레포 전체 점검: `tools/README.md`에 빠진 도구 6개(tts_text·svgshot·mvcheck·motion_preview·hookscore·pivots) 추가, `docs/project-instructions.md`의 `docs/archive/` 안내 갱신. 지운 파일 없음.
- 2026-10-26: `tools/build3.py`가 `motions`를 쓰기 전에 import하지 않아(4차 보강의 배경 효과 `motions.fx_for`) 빌드가 NameError로 멈추던 것을 맨 위 import로 고침.
- 2026-10-27: `frog_place.py` 크래시 수정(dict act를 `ACT_MOOD2`에 `in`으로 비교하면 unhashable, 문자열일 때만 비교).
- 2026-10-27 (miya): 소리 자동화. `tools/sfx_lib.py` v3(+61종 = 92종), 새 `tools/sfx_pick.py`(단어 규칙 81 + 우주 6, 팔레트 앰비언트, 밀도 상한, `COSMIC_SWAP`), `tools/bgm_lib.py` 재작성(스타일 9 `STYLES`·분위기 풀 `POOLS` 80진행, `style_for`·`scene_moods`, 코드 기호 파서 `chord()`; `synth_cosmic`은 `synth(style='cosmic')`로), `tools/build3.py`에 `BGM_STYLE`·`COSMIC`·`SFXPREV` 연결. 지침서 9-3·9-4, art_spec 8·11, README, CLAUDE.md. 데모 `/mnt/project-files/frog-rules/audio/`.
- 2026-10-27 (miya): '연속 사용 금지' 고정 규칙 제거(`motions.fx_for`, `sfx_pick.sfx_for`, `bgm_lib._order`, `build3` 전환 `last2`, `frog_place.pick_word`·문장 표정). 상황이 이어지면 반복, 채움 선택만 직전과 다르게. CLAUDE.md '반복 원칙', 지침서 4·7·9장.
- 2026-10-27 (miya, 고래 영상 물고기 역주행): 새 `tools/facing.py`(이동 오브젝트 머리 방향 ↔ 이동 방향 검사·거울상 수정), `build3.py` `FACE`/`FACEFIX` 연결, `motions.py` 배경 입자 fish 머리 방향·streak 꼬리 방향 수정, `frog_place.py` 탄 개구리 이동 방향 보기. art_spec 7 방향 규칙, 지침서 4장, CLAUDE.md, README.
- 2026-10-27 (miya, "바람·빨림도 방향성"): 방향 규칙 확장. `tools/facing.py`에 `context`(travel·wind·attractor)·`reverse_path`·`_path_rules`(중력 이름·빨림·magnet)·뾰족함 판정·`boxes`, `tools/motions.py`에 `dir_sign`과 `fx_markup/fx_js`의 `wind`/`travel` 인자(입자·비·바람선·안개·생물 줄), `tools/build3.py`에 그림별 `DIRC` 문맥·드리프트 팬 방향, `tools/frog_place.py` 밀기 개구리 뒤쪽 배치. 지침서 4-4 표 신설, art_spec 7·8(사이드카 `wind`·`attractor`), README, CLAUDE.md.
- 2026-10-27 (miya, "자동 아닌 것도 규격화"): `tools/facing.py` 2차 — JS 탐색을 역할별(travel·gaze·lean·flag)로 넓히고 그림자/하이라이트 수집(캐시 키 `v2`), `_dir_rules2`(톱니 맞물림·깃발/기울기 바람·시선·빛/그림자), `_mirror_group`·`_set_attr`·`spin_dir`, `context()`에 focus·light·wind_known; `frog_place.py` orbit `act.dir`, `frog.py` orbit `sd`. 지침서 4-4 B 표, art_spec 7·8(사이드카 `light`), README, CLAUDE.md.
- 2026-10-27 (miya, 상어 탄 개구리에 잠수복 없음): `tools/frog_place.py` `underwater()`(탑승 그룹 `SEA_RIDE`·물 그룹 `WATER_G`·팔레트·단어) — 사이드카 쓰기 직전에 잠수 장비를 단어 의상보다 우선 적용. 지침서 7-2 E.
- 2026-10-27 (miya, 대본+그림 규칙): `tools/frog_place.py`에 `has_group`·`BG_LAYER`·`in_space`(`SPACE_PAL`·`SPACE_RIDE`·`SPACE_G`·`GROUND_G`)·`PIC_OUTFIT`/`pic_outfit`·`HOLE_G`·`ICE_G`·`FIRE_G`, 약한 동작 체인 끝에 그림 증거 동작 5종, 사이드카 쓰기 직전 헬멧·잠수 장비 물리 상태 우선. 지침서 7-2 E, CLAUDE.md.
- 2026-10-27 (miya, 배경·효과음·텍스트도 그림 규칙): 새 `tools/picev.py`(그룹 이름·크기 → 태그), `motions.fx_for(pic=)` `FX_PIC`/`FX_PIC_DAY`, `sfx_pick.sfx_for(pic=)` `SFX_PIC`(auto 'picture'), `labels_lib.name_fx(pic=)`/`label_js(pic=)` `PIC_FX`, `build3.py` `PIC[nn]`(FACE boxes에서). 지침서 4-1·9-3, art_spec 7, README, CLAUDE.md.
- 2026-10-27 (miya, 전체 점검): `frog_place.py`의 미정의 이름 `dood`(read 동작 분기에서 NameError 가능) 정의; '연속 금지' 잔재 문구 정리(art_spec 7·8, 지침서 9-3 큐, README motions, briefs/scene_motion, build3 주석); 핵심 지침서 12-1에 frog_place→build3→빌드 로그 확인 단계 추가. 숏츠 1편(whale-fall-short1) TTS→정렬→build3 전체 실행으로 오늘 변경(방향·그림 증거·소리) 통합 확인(JS 오류 0).
- 2026-10-27 (miya, 움직이는 오브젝트의 라벨 고정 문제): `tools/motions.py`에 `miyaFollow`·`miyaCtm`·`miyaFollowInit`(라벨이 뜨는 시각에 그룹 중심 기준점을 잡고, 매 seek 뒤 라벨·선·꼬리를 그룹 이동량만큼 다시 맞춤), `tools/build3.py`에 `PICPATH`·`MOVING`/`MOVING_CORE`·라벨 연결 패스(로그 `labels follow moving objects`)와 `miyaFollowInit(tl)` 호출. 지침서 3-6, art_spec 8, CLAUDE.md.
- 2026-10-28 (miya, 전체 재점검): pyflakes·규칙 표 개수(동작 56·의상 64·표정 34·오브젝트 56·배경 57·텍스트 36·효과음 92·BGM 9)·지침서가 가리키는 파일·main 사본 대조·whale-fall-short1 테스트 빌드(JS 오류 0) 모두 통과. 고친 것은 `build3.py` 전환 효과음 표 `TRSND`의 중복 키 `zoom` 하나뿐(값 같음, 동작 변화 없음).
- 2026-10-29 (miya, 오픈소스 라이브러리 통합): 새 `tools/fxlib.py`(플러그인 등록·이징·스프링·단어 규칙·lucide 픽토그램)·`tools/svg_opt.py`(svgo 사본), `tools/assets/gsap/`(플러그인 14개)·`gsap.min.js` 3.15.0·`anime.min.js`·`lucide.json`; `motions.py`(오브젝트 draw·morph·toss·skid·coast·regroup, 배경 burst, CustomBounce/Wiggle 이징, `miyaPath` ease 인자), `labels_lib.py`(scramble·type·splitwords·스프링·픽토그램), `frog.py`(shiver=CustomWiggle), `build3.py`(자산 복사·등록·svgo·ExpoScale·RoughEase·`library fx` 로그). 지침서 4-6 신설, 3-6 6번, 7-2·15장 메모, art_spec 7, README, CLAUDE.md. 레포에 넣기 전 1분 시연으로 miya 확인(2026-10-29 "시연 없어도 될 것 같아 … 모두 파이프라인에 붙이고").
- 2026-10-29 (miya, 개구리가 너무 정적): 새 `tools/frog_rig.py`(관절 리그·생기 층·접촉 12·이동 10·의상 38 동작)와 `tools/assets/ease_miyaBnc.json`(CustomBounce 샘플 201점); `tools/frog.py` 마크업을 관절 그룹(`_lf`·`_lgl`·`_lgr`·`_la`·`_ra`·`_hd`)으로 재구성, `tools/build3.py` `obj_timing`, `tools/frog_place.py` `contact_pick`·`loco_pick`·`costume_pick`. 지침서 7-2 I, art_spec 12, README. 렌더 트리거 파일은 건드리지 않음.
- 2026-10-29 2차 (miya, 접촉 동작 더·팔 꺾임): `tools/frog_rig.py` CONTACT 25종(+13), `arm_bend_pass`(팔 경로 d 트윈 자동 추가, `frog.js` 끝에서 호출), `tools/frog_place.py` 새 종류 규칙(`SIDESTEPW`·`BOUNCEW`·`HEAVYG`·`WHEELG`). 지침서 7-2 I-4 표·I-6-1, art_spec 12, README, CLAUDE.md.
- 2026-10-29 3차 (miya, 타이밍·그림자): `tools/frog_rig.py` `obj_span` 종류 확장·`shadow_follow_pass`·`HITS`·`ease_inv`(power2.out/in), `tools/frog.py` 접촉 동작 `enter: cut` 강제, `tools/frog_place.py` knocked 왼쪽. 지침서 7-2 I-6-2.

- 2026-10-29 (miya, 효과 삭제): `motions.py`에서 `pulsevig`(어두운 막+줌 반복)·`gridripple`(점 격자 깜빡임)과 단어 규칙·HEAVY_FX 항목 삭제, `build3.py` 로그·지침 4-1/4-6·README·art_spec·CLAUDE.md 정리. 배경 효과 59→57종.
- 2026-10-29 (miya, 괴물 개구리 영상 검수: 풍차·그물·개구리 다리·꼬리·목·시곗바늘·톱니·나무·풀·팻말 축): **원인 수정** `tools/build3.py`(힌지 트윈 `svgOrigin:miyaPv`을 `miyaFollowInit` 뒤에 생성, 로그 `hinge tweens added after the follow measuring`; 이름표 따라가기에 그림 시작 시각 `UST0` 전달), `tools/motions.py`(`miyaFollowInit` 정렬·기준 시각 `tm`, 모든 `svgOrigin`에 `smoothOrigin:false`, 코어 sway가 `data-pivot` 사용). **점검 코드** 새 `tools/attachcheck.py`·`motionaudit.py`·`pivotlive.py`·`final_check.py`(`.checked` 게이트, `chunk_plan.py`가 확인)·수리 도구 `gearmesh.py`·`setbase.py`·`splitclumps.py`·`joinpart.py`·`grpinfo.py`; `build3` 끝에서 attachcheck 자동. 문서: 지침서 4-7·15-8, `tools/art_spec.md` 7A·9, `tools/briefs/{scene_motion,remake_art,people_restyle}.md`, `tools/README.md`, `CLAUDE.md`. 2026-10-27 이후 만든 다른 영상(우주의 끝·고래 낙하·인간을 먹는 …·훔친 시간)은 `build3.py` 다시 돌려야 고쳐진다.
