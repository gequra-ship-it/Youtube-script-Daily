# 레포 구조 변경 기록 (요약)

브랜치 병합, 파일 합치기·이동·삭제처럼 레포 구조가 바뀐 일만 한 줄씩 적는다. 자세한 옛 기록(명령, 충돌 목록, 대응표)은 `docs/archive/repo-changes-full-2026-10-18.md`. 영상 제작 규칙의 변경은 지침서 맨 위 결정 날짜 요약과 `docs/archive/guideline-full-2026-10-18.md`.

## 현재 구조
| 브랜치 | 내용 |
|---|---|
| `main` (기본) | 매일 대본 생성: `main.py`(6시), `main_owl.py`(7시), `main_이과형.py`(9시, KST) + 워크플로 `schedule.yml`·`schedule_owl.yml`·`schedule_igwahyung.yml`, 봇이 커밋하는 `scripts/`·`scripts_owl/`·`scripts_igwahyung/`. `docs/`·`tools/`는 `render-pipeline`의 사본. `render/`·`videos/`는 넣지 않는다(약 650MB) |
| `render-pipeline` | 영상 제작 원본: `tools/`, `docs/`, `videos/<슬러그>/`, `render/<슬러그>/`, 워크플로 `render-chunked.yml`(구간 병렬 렌더)·`render.yml`(`render/.slug`) |
| `claude/epic-ritchie-0mujsz` | 세션 작업 브랜치(`main`에 합쳐 쓰는 대본 도구용) |
- `cine-test/`: 3D(cine) 방식 보관(문서·코드·영상). 사용자가 3D를 요청할 때만 쓴다.
- `docs/archive/`: 슬림화 전 전체 사본(지침서, art_spec, repo-changes). 평소에는 읽지 않는다.
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
- 2026-10-24: 메타데이터에 출처(SOURCES)는 유지(출처가 있을 때만).
