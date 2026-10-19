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
