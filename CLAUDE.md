# Miya's Lab 레포 안내 (Claude가 세션 시작 때 읽는 파일)

영어 지식 유튜브 채널 Miya's Lab의 대본 생성·영상 제작·렌더 레포다. **영상 작업(대본 → 음성 → 3D 장면 → 렌더 → Drive)을 하기 전에 지침서를 끝까지 읽고 따른다.**

## 먼저 읽을 파일
- 지침서: `docs/miyas-lab-guideline.md` (`render-pipeline` 브랜치가 원본). 이 파일과 지침서가 다르면 지침서가 우선이다.
- 3D 장면 명세(에이전트에게 주는 문서): `tools/cine_spec.md`
- 도구 사용법: `tools/README.md`
- 레포 구조 변경 기록: `docs/repo-changes.md`

영상은 모두 **시네마틱 3D(cine) 방식**으로 만든다(2026-10-14 사용자 결정). 예전 SVG 방식과 그 도구는 지웠다(깃 기록의 커밋 `ff7818b`에 남아 있음).

## 레포 구조 (`render-pipeline`)
| 경로 | 내용 |
|---|---|
| `tools/` | 제작 도구: 음성(`tts.sh`, `audio_prep.py`), 단위 나누기·소리 믹스(`build_audio.py`), 3D 렌더 원본(`build_cine.py`, `cine/`), 확인(`cineshot.py`), 구간 렌더(`chunk_prep.py`), 텍스트·썸네일(`gen_text.py`, `thumb_shot.py`) |
| `tools/cine/` | 실행 라이브러리(`cine.js`, `cine.css`), 실사감 도구(`kit.js`), 장면 라이브러리(`scenes/`), Three.js·GSAP·글꼴(`assets/`) |
| `videos/<slug>/` | 영상별 원본: `script.py`(대본), `config.py`(팔레트·데이터 카드·제목·설명), `plan.json`(단위), `cine.json`(장·샷·화면 글자), `scenes/`(그 영상의 새 장면) |
| `videos/_playlists/` | 재생목록 표지 |
| `render/<slug>/` | 렌더 원본(빌드 결과). `render/.chunked`가 렌더할 영상 목록 |
| `docs/` | 지침서, 레포 변경 기록, 프로젝트 지침 문구 |

## 브랜치
| 브랜치 | 역할 |
|---|---|
| `render-pipeline` | 영상 제작의 원본. `tools/`, `docs/`, `videos/`, `render/`, 렌더 워크플로 `render-chunked.yml` |
| `main` | 매일 대본 생성(`main.py`, `main_owl.py`, 워크플로 `schedule.yml`·`schedule_owl.yml`). 예약 워크플로는 기본 브랜치인 `main`에서만 돈다. 봇이 매일 `scripts/`·`scripts_owl/`에 대본을 커밋한다. `docs/`·`tools/`는 사본 |

- `docs/`·`tools/`를 고치면 `render-pipeline`에 먼저 넣고 `main`에도 같은 내용을 넣는다(두 사본이 어긋나지 않게).
- `main`에 `render/`·`videos/`를 넣지 않는다(매일 대본 작업이 실행마다 받게 된다).

## 렌더 주의 (되돌리기 어려움)
- `render-pipeline`에 `render/.chunked`(또는 `.github/workflows/render-chunked.yml`)를 바꾸는 푸시는 렌더를 바로 시작하고, 끝나면 **Drive의 같은 이름 MP4를 덮어쓴다.** 의도한 영상만 적는다. 줄 형식 `"<slug> <구간 수>"`, `#`은 주석.
- Drive 경로는 `render/<slug>/.dest`로 정한다: `Space & Science/NN_<slug>`, `Life & History/NN_<slug>`(숏츠는 그 안의 `short`), 시험은 `_ci-test/<slug>`. 폴더 이름이 바뀌면 `.dest`도 바꾼다(안 그러면 새 폴더가 생긴다).
- 구간 하나는 작업 하나(300분 한도)로 동시에 렌더된다. 구간 수는 `python3 tools/cineshot.py render/<slug> --estimate`로 정한다.

## 항상 지킬 것 (자세한 내용은 지침서)
- 영상에 들리고 보이는 것(내레이션, 자막, 화면 글자, 데이터 카드)은 영어만. 채널명은 "Miya's Lab".
- 사실 확인은 A~D 등급(지침서 10-1). 존재하지 않는 사례·연구·숫자·인용·인물을 지어내지 않는다.
- 확인하지 않은 것을 확인했다고 쓰지 않는다.
- 비밀값(`RCLONE_CONF`, API 키)은 읽거나 출력하지 않는다.
- 지침서를 고치면 개정 이력에 날짜와 이유를 남긴다. 레포 구조를 바꾸면 `docs/repo-changes.md`에 남긴다.
