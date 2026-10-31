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
- **붙임 규칙·최종 점검(2026-10-29, miya, 지침서 4-7·15-8)**: 움직이는 부분(꼬리·다리·목·그물·시곗바늘·톱니·나무·풀·팻말)은 몸에 붙어 있고 `data-pivot`이 닿는 점이어야 한다. 그림 에이전트는 낼 때마다 `python3 tools/attachcheck.py <slug> <uid..>`가 0이어야 보고하고, **메인은 렌더 푸시 전에 `SLUG=<slug> python3 tools/final_check.py`(통과하면 `render/<slug>/.checked`)를 돌리고 사용자가 짚은 장면은 `tools/motionaudit.py` 띠 이미지를 눈으로 본다.** `chunk_plan.py`는 `.checked`가 없으면 렌더 사양을 내놓지 않는다. **축 카탈로그(2026-10-29, miya, 지침서 4-8)**: 축은 에이전트가 찍지 않고 그룹 이름의 물건(`tools/axis_catalog.md`, 머리 명사 마지막)으로 `tools/axisfix.py`가 그림에서 재서 써 준다. 에이전트는 `axisfix` → `attachcheck` 순, `build3`가 시작할 때 자동 실행, attachcheck·final_check가 카탈로그 불일치(물건에 안 맞는 종류·축 없는 것의 회전·빠진 피벗·발/매단 점/허브/깃대 변에서 벗어난 피벗)를 걸면 렌더 전에 돌려보내 다시 한다.
- **렌더 멈춤 금지(2026-10-30, miya, 지침서 15-8)**: CustomWiggle·문자열 `wiggle({...})` ease는 Actions 캡처를 멈추게 한다(그림은 멈추고 소리만 남음). 떨림은 `fxlib.miyaW`/`miyaJit` 함수 ease만, `final_check.py`가 남은 것을 막는다. 렌더가 끝나면 청크 MP4를 받아 `python3 tools/freezecheck.py`로 멈춤 구간이 없는지 확인한 뒤에 완료로 알린다. 새 ease·플러그인은 로컬 렌더 + freezecheck로 먼저 검증.
- 영상에 들리고 보이는 것(내레이션, 자막, 화면 텍스트, 칠판)은 영어만. 채널명은 "Miya's Note".
- 사실 확인은 A~D 등급(지침서 12-1). 존재하지 않는 사례·연구·숫자·인용·인물을 지어내지 않는다.
- 확인하지 않은 것을 확인했다고 쓰지 않는다. 지침서의 "확인한 것 / 확인하지 못한 것" 구분을 유지한다.
- 출력 토큰 절약(사용자 결정 2026-10-17): 단계마다 결과를 알리지 않는다. 최종 렌더가 Drive에 올라갔을 때(또는 질문받았을 때, 막혀서 결정이 필요할 때)만 1~3줄로 알린다. 그림·영상 수정은 예시 이미지 몇 장으로 먼저 확인받는다(지침서 21-4).
- 썸네일은 영상마다 서로 다른 소재 3장(A·B·C), 지침서 16-6: 영화 오마주형 + 직관형을 섞고(기준 4장 = 트루먼 쇼·인터스텔라 오마주 2 + 직관형 2), 재미있고 시선을 끌어야 한다. **썸네일은 항상 Opus 에이전트가 만든다**(`tools/briefs/thumb_art.md`), 사용자에게 예시로 먼저 확인받는다(사용자 2026-10-18).
- **사용한 대본은 렌더를 올릴 때 `main` 브랜치에서 `scripts/used/` 또는 `scripts_owl/used/`(이과형은 `scripts_igwahyung/used/`)로 옮긴다**(`<슬러그>__<원래 파일명>.txt`, 지침서 12장 10번 · miya 2026-10-22). 사용자가 대본을 채팅에 붙여 줬어도 같은 이름의 원본이 `main`의 `scripts*/`에 있으면 그것을 옮긴다. 옮기지 않으면 맨 위에 안 쓴 대본으로 남는다(2026-10-25 우주의 끝 영상에서 빠뜨렸다가 나중에 옮김).
- **개구리 규칙은 지침서 7-2(2026-10-26 정리본)를 따른다.** **2026-10-29 관절 리그(7-2 I, `tools/frog_rig.py`)**: 모든 개구리가 숨 쉬고 움직이며, 그림의 움직이는 소품(`mv-core-drop`·`topple`·`rollby`·`bouncing`·`swing`·`rise`)과 그 시각에 맞춰 접촉 동작 25종(사과 맞고 쓰러짐·깔림·트램펄린·추에 맞음 등)·이동 10종·의상 동작 38종을 `frog_place.py`가 단어+그룹 이름+크기로 고른다. 그림 에이전트는 작은 소품을 움직이게 그리고 이름을 붙인다(art_spec 12). 팔은 머리 위로 올릴 때 굽음이 자동으로 반전된다(`frog_rig.arm_bend_pass`). 그림이 끝나면 `python3 tools/frog_place.py <slug>`가 대본·그림으로 동작·표정·의상·말풍선·위치를 고르고, 안 맞으면 사이드카 `frog`를 손으로 고치고 `lock: true`. 핵심: 칠판 외 설명·가리키기 없음, 의미 있는 개구리만(동작·함께 이동·의상·말풍선 중 하나), 주인공 오브젝트 한가운데 위에 앉히지 않음(끝에 타거나 옆에 서기), 제자리 점프 금지, 상황마다 새로 판단(miya 2026-10-25·26). **의상·동작은 대본 단어 + 그림 증거를 같이 본다(miya 2026-10-27)**: 탑승 그룹·오브젝트 그룹 이름·화면 비율·팔레트로 물속(diver)·우주(helmet)·추위(scarf)·비(umbrella)·배(lifevest) 등을 판정하고, 배경 레이어는 증거가 아니다(지침서 7-2 E).
- **다양성 층(2026-10-31, miya, 지침서 7-2 K·4-10·15-8)**: 단어 규칙이 빗나간 개구리는 문장의 개념 25종(크기·시간·탄생·위험·발견·숨김…) × 영역 9종(우주·바다·역사·몸·생물·시간·지구·기술·일반) 풀에서 **이 영상에서 가장 적게 쓴 동작**을 받고(`tools/concepts.py`, 동작 34종·소품 의상 20종 추가), 거듭되는 강한 동작(wind·shiver·awe·pull)도 변형 풀에서 돈다. 그림 에이전트는 영상의 테마 팩(`tools/concepts_catalog.md`) 소품·구도를 쓰고 4~6장마다 움직이는 소품 1장을 넣는다(art_spec 7B). `final_check.py`가 `tools/variety_check.py`(최다 동작 ≤ 40 %, 동작 ≥ 8, 의상 ≥ 4, 오브젝트 모션 ≥ 8종, 소품 할당량은 경고)를 돌린다.
- **오픈소스 라이브러리(2026-10-29, miya)**: GSAP 3.15 플러그인 14개·anime.js·lucide 픽토그램·svgo가 빌드에 들어 있다(지침서 4-6 표, `tools/fxlib.py`). 새 `mv-` 종류 `draw·morph·toss·skid·coast·regroup`는 그림 에이전트가 문장에 맞을 때 쓰고(art_spec 7), 속도 램프·카메라 떨림·스프링·burst·스크램블·타자기·픽토그램은 코드가 대본 단어로 고른다. 빌드 로그 `library fx`·`svgo`로 확인. 렌더 폴더에 `gsap/` 하위 폴더가 생긴다.
- **반복 원칙(2026-10-27, miya)**: 어떤 항목에도 '연속 사용 금지' 고정 규칙을 두지 않는다. 대본 상황이 이어지면(같은 단어 규칙이 또 맞으면) 같은 효과음·배경 효과·전환·말풍선·표정을 또 쓰고, 상황 없이 채우는 선택(앰비언트·풀 순환·횟수 균형)만 직전과 다르게 돌린다. 배경음악 진행은 분위기가 바뀔 때 바뀐다.
- **4차(2026-10-26, miya)**: 오브젝트 모션 축은 그룹 이름으로 자동 교정(나무는 밑동 고정, 둥근 것만 회전, `data-keep="1"`만 예외, 지침서 4-1 '4차 보강'); 개구리 동작 56종·의상 64종·표정 34종(7-2 D·E·F), 오브젝트 모션 56종, 배경 효과 57종(`motions.fx_for`), 텍스트 효과 36종(`labels_lib`)이 전부 단어·팔레트·단위 번호 규칙으로 붙는다. 그림 에이전트는 비·눈·입자를 그리지 않는다. **그림 증거(2026-10-27, miya)**: 배경 효과·효과음·이름표 효과도 `tools/picev.py`가 오브젝트 그룹 이름·크기로 읽은 태그(불·물·얼음·시계·종·톱니·새…)를 단어 다음, 앰비언트·순환보다 먼저 쓴다. 그러니 그림 에이전트는 오브젝트 그룹에 뜻이 드러나는 이름을 붙인다(art_spec 7). **움직이는 오브젝트의 이름표·말풍선은 오브젝트를 따라간다(miya 2026-10-27, 지침서 3-6 5번, `miyaFollow`)**.
- **방향 점검(2026-10-27, miya)**: 옆으로 이동하는 오브젝트는 머리 쪽으로 움직여야 한다. `tools/facing.py`가 눈 위치로 판단해 어긋나면 그림을 거울상으로 뒤집고(`build3` 로그 `direction sanity`), 배경 입자(fish·유성)는 코드가 방향을 맞추며, 탄 개구리는 이동 방향을 본다. 눈이 없는 탈것·화살은 그룹에 `data-face`를 적는다(art_spec 7). **확장(같은 날, 지침서 4-4 표)**: 눈 없는 뾰족한 것은 뾰족한 쪽이 머리, 내려감·올라감·빨려듦은 그룹 이름으로 경로를 뒤집어 맞추고, 비·바람선·안개·입자는 바람(사이드카 `wind`, 기본 맞바람)·물고기 떼는 이동 방향, 카메라 팬은 이동을 따라가고, 개구리는 타면 이동 방향을 보고 밀면 뒤에서 민다. **2차(같은 날, 4-4 B)**: 닿는 톱니는 반대로 돌고, 깃발·연기·머리카락은 바람 쪽으로, 사람·동물은 초점을 보고, 그룹 안 그림자·하이라이트는 광원(사이드카 `light` 또는 sun·lamp 그룹) 기준으로, 개구리 궤도는 고리 회전 방향으로 코드가 맞춘다. 남는 수작업: 두 사람의 시선 교환, 그룹 밖 그림자.
- **소리도 코드 규칙(2026-10-27, miya)**: 효과음 92종(`tools/sfx_lib.py`)은 `tools/sfx_pick.py`가 대본 단어·팔레트·단위 번호로 고르고(에이전트 사이드카 `sfx`는 단어 규칙이 없을 때만, `sfx_lock`으로 고정), 배경음악은 `tools/bgm_lib.py`가 스타일 9종(팔레트+대본 전체 분위기, config `STYLE`이 우선)과 장면별 분위기 4종(진행 풀·플럭 밀도)을 고른다(지침서 9-3·9-4). 빌드 로그 `music style`·`bgm moods`·`sfx auto`로 확인.
- **개구리·오브젝트 연출은 전부 코드 규칙이다(miya 2026-10-26 3차)**: 동작·의상·표정·말풍선·칠판 생기·멈춤 뒤 숨쉬기·유성은 대본 정규식 + 그룹 이름 + 단위 번호로 정해진다(지침서 7-2 D-2, 4-1 '3차 보강'). 모델이 임의로 고르지 않고, 바꾸고 싶으면 사이드카 `lock` 또는 코드·지침서를 함께 고친다.
- 비밀값(`RCLONE_CONF`, API 키)은 읽거나 출력하지 않는다.
- 지침서를 고치면 개정 이력에 날짜와 이유를 남긴다. 레포 구조를 바꾸면 `docs/repo-changes.md`에 남긴다.


## Picture agents: model split and token budget (user decision 2026-10-17)
- Units with people, animals or other creatures, or a complex composition -> Opus agent (`model: "opus"`); simple units (charts, objects, landscapes, icons) -> Sonnet agent (`model: "sonnet"`). Split each video's units into these two groups before launching agents.
- Before changing a style or rule across many pictures, make 2-4 test pictures and get the owner's OK first.
- Agents check with one before/after contact sheet per batch and report in at most 8 lines.
- Reporting (user decision 2026-10-17): do not report each finished step; report briefly only when the final render is on Drive. When changing pictures or video, show only a few sample images first.
- Remakes of existing videos reuse pictures: `tools/remake.py`, agent brief `tools/briefs/remake_art.md`, guideline section 21.
