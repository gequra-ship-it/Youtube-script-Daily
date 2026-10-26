# Miya's Note 레포 안내 (Claude가 세션 시작 때 읽는 파일)

영어 지식 유튜브 채널 Miya's Note의 대본 생성·영상 제작·렌더 레포다. **영상 작업(대본 → 음성 → 그림 → 렌더 → Drive)을 하기 전에 지침서를 끝까지 읽고 따른다.**

## 먼저 읽을 파일
- 지침서 원본: `docs/miyas-lab-guideline.md` (`render-pipeline` 브랜치가 원본, 현재 규칙만 담은 핵심 약 11KB + 장별 파일 `docs/guideline/`, 지금 단계에 해당하는 장만 읽는다). 이 파일과 지침서가 다르면 지침서가 우선이다. 옛 기록·전체 사본은 브랜치 `archive/miyas-lab-2026-10-24`의 `docs/archive/`에만 있다(이 브랜치에서는 2026-10-24에 지움, 평소 읽지 않는다).
- **영상은 SVG 모션그래픽 방식으로 만든다(2026-10-16 사용자 결정으로 복귀).** 그림 명세: `tools/art_spec.md` (+ 영상별 `videos/<slug>/art_brief.md`). 3D 실험에서 얻은 카메라·속도감·초반 밀도·숏츠·관절 모션·병렬 렌더 규칙은 지침서 20장(코드: `tools/build3.py`의 `DRIFT`·`HOOK`·속도선·`mv-joint`/`mv-chain`, `tools/motion_check.py`, `tools/chunk_plan.py`)
- 시네마틱 3D(cine) 실험, 옛 Miya's Lab 영상(`videos/`·`render/` 전부)과 옛 문서는 2026-10-24에 지웠다. 필요하면 `archive/miyas-lab-2026-10-24` 브랜치에서 꺼낸다(`git checkout archive/miyas-lab-2026-10-24 -- <경로>`).
- 도구 사용법: `tools/README.md`
- 레포 구조 변경 기록: `docs/repo-changes.md`

## 브랜치
| 브랜치 | 역할 |
|---|---|
| `render-pipeline` | 영상 제작의 원본(매일 대본 코드·대본은 `main`에만 둔다, 2026-10-24 옛 복사본 삭제). `tools/`, `docs/`, `videos/`(영상별 원본), `render/`(렌더 원본), 렌더 워크플로 `render.yml` |
| `main` | 매일 대본 생성(`main.py`, `main_owl.py`, 워크플로 `schedule.yml`·`schedule_owl.yml`). 예약 워크플로는 GitHub 규칙상 기본 브랜치인 `main`에서만 돈다. 봇이 매일 `scripts/`·`scripts_owl/`에 대본을 커밋한다. `docs/`·`tools/`는 사본 |

- `docs/`·`tools/`를 고치면 `render-pipeline`에 먼저 반영하고 `main`에도 같은 내용을 넣는다(두 사본이 어긋나지 않게).
- `main`에 `render/`·`videos/`(약 650MB)를 넣지 않는다. 매일 대본 작업이 실행마다 그만큼 받게 된다.

## 렌더 주의 (되돌리기 어려움)
- `render-pipeline`에 푸시할 때 `render/.slug`, `.github/workflows/render.yml`, `render/sample/**` 중 하나가 바뀌면 GitHub Actions 렌더가 바로 시작되고, 끝나면 Drive의 같은 이름 MP4를 덮어쓴다. 의도하지 않았다면 이 파일들을 건드리지 않는다.
- 렌더는 `render/.chunked`(`"<slug> <구간 수>"`, 구간 수는 `python3 tools/chunk_plan.py render/<slug>`)를 바꾸는 푸시로 `render-chunked.yml`이 구간별 동시 렌더 후 합쳐 올린다(SVG·3D 모두, 지침서 20-7). 예전 한 작업 방식 `render.yml`은 `render/.slug`(한 줄에 슬러그 하나)로 돈다. 둘 다 바로 시작되고 덮어쓴다. 렌더 없이 워크플로 파일만 바꿀 때는 `.slug`를 없는 슬러그(예: `none`)로 두어 실행이 아무것도 올리지 않고 끝나게 한다.
- 렌더 1회(작업 하나) 시간 한도는 300분이고, 슬러그를 순서대로 렌더한다. 롱폼은 영상 길이의 약 3~4배가 걸린다(2026-10-13 실행: 약 20분 영상이 숏츠 2편 포함 약 62~90분). 숏츠는 영상마다 5편(각 2:00~2:55, 지침서 19장)이라 롱폼과 숏츠를 다른 커밋으로 나눠 푸시하면 시간 한도에 여유가 생긴다. 여러 주제는 주제별로 커밋을 나눠 하나씩 푸시해 병렬로 돌린다(지침서 15-5).
- Drive 경로는 `render/<slug>/.dest`로 정한다(지침서 18장). **2026-10-24 새 채널 Miya's Note: 새 영상은 `Miya's Note/<01. Life & History | 02. Space & Science>/NN_<slug>`(숏츠 `/short`, 5편), 아래 옛 구조는 Miya's Lab 보관용**(2026-10-16 구조): 새 영상은 `Space & Science/NN_<slug>`, `Life & Biology/NN_<slug>`(주제 폴더마다 01부터 번호, 숏츠는 `/short`), 예전 SVG 영상 보관은 `old/<영상>`, 3D 실험은 `cinema/<영상>`. 폴더 이름이 바뀌면 `.dest`도 바꾼다(안 그러면 새 폴더가 생긴다).
- 이미 만든 영상에 새 모션 규칙만 적용할 때는 `tools/restyle_motion.py`를 빌드 원본에만 쓴다(지침서 15-7).

## 항상 지킬 것 (자세한 내용은 지침서)
- 영상에 들리고 보이는 것(내레이션, 자막, 화면 텍스트, 칠판)은 영어만. 채널명은 "Miya's Note".
- 사실 확인은 A~D 등급(지침서 12-1). 존재하지 않는 사례·연구·숫자·인용·인물을 지어내지 않는다.
- 확인하지 않은 것을 확인했다고 쓰지 않는다. 지침서의 "확인한 것 / 확인하지 못한 것" 구분을 유지한다.
- 출력 토큰 절약(사용자 결정 2026-10-17): 단계마다 결과를 알리지 않는다. 최종 렌더가 Drive에 올라갔을 때(또는 질문받았을 때, 막혀서 결정이 필요할 때)만 1~3줄로 알린다. 그림·영상 수정은 예시 이미지 몇 장으로 먼저 확인받는다(지침서 21-4).
- 썸네일은 영상마다 서로 다른 소재 3장(A·B·C), 지침서 16-6: 영화 오마주형 + 직관형을 섞고(기준 4장 = 트루먼 쇼·인터스텔라 오마주 2 + 직관형 2), 재미있고 시선을 끌어야 한다. **썸네일은 항상 Opus 에이전트가 만든다**(`tools/briefs/thumb_art.md`), 사용자에게 예시로 먼저 확인받는다(사용자 2026-10-18).
- **사용한 대본은 렌더를 올릴 때 `main` 브랜치에서 `scripts/used/` 또는 `scripts_owl/used/`(이과형은 `scripts_igwahyung/used/`)로 옮긴다**(`<슬러그>__<원래 파일명>.txt`, 지침서 12장 10번 · miya 2026-10-22). 사용자가 대본을 채팅에 붙여 줬어도 같은 이름의 원본이 `main`의 `scripts*/`에 있으면 그것을 옮긴다. 옮기지 않으면 맨 위에 안 쓴 대본으로 남는다(2026-10-25 우주의 끝 영상에서 빠뜨렸다가 나중에 옮김).
- **개구리 규칙은 지침서 7-2(2026-10-26 정리본)를 따른다.** 그림이 끝나면 `python3 tools/frog_place.py <slug>`가 대본·그림으로 동작·표정·의상·말풍선·위치를 고르고, 안 맞으면 사이드카 `frog`를 손으로 고치고 `lock: true`. 핵심: 칠판 외 설명·가리키기 없음, 의미 있는 개구리만(동작·함께 이동·의상·말풍선 중 하나), 주인공 오브젝트 한가운데 위에 앉히지 않음(끝에 타거나 옆에 서기), 제자리 점프 금지, 같은 말풍선 연달아 금지, 상황마다 새로 판단(miya 2026-10-25·26).
- **개구리·오브젝트 연출은 전부 코드 규칙이다(miya 2026-10-26 3차)**: 동작·의상·표정·말풍선·칠판 생기·멈춤 뒤 숨쉬기·유성은 대본 정규식 + 그룹 이름 + 단위 번호로 정해진다(지침서 7-2 D-2, 4-1 '3차 보강'). 모델이 임의로 고르지 않고, 바꾸고 싶으면 사이드카 `lock` 또는 코드·지침서를 함께 고친다.
- 비밀값(`RCLONE_CONF`, API 키)은 읽거나 출력하지 않는다.
- 지침서를 고치면 개정 이력에 날짜와 이유를 남긴다. 레포 구조를 바꾸면 `docs/repo-changes.md`에 남긴다.


## Picture agents: model split and token budget (user decision 2026-10-17)
- Units with people, animals or other creatures, or a complex composition -> Opus agent (`model: "opus"`); simple units (charts, objects, landscapes, icons) -> Sonnet agent (`model: "sonnet"`). Split each video's units into these two groups before launching agents.
- Before changing a style or rule across many pictures, make 2-4 test pictures and get the owner's OK first.
- Agents check with one before/after contact sheet per batch and report in at most 8 lines.
- Reporting (user decision 2026-10-17): do not report each finished step; report briefly only when the final render is on Drive. When changing pictures or video, show only a few sample images first.
- Remakes of existing videos reuse pictures: `tools/remake.py`, agent brief `tools/briefs/remake_art.md`, guideline section 21.
