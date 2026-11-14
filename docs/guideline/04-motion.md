## 4. 모션 규칙 (일러스트 장면)

> 최종 수정: 2026-11-14 · 본문은 지금 유효한 규칙만 담는다. 바뀐 경위는 맨 아래 개정 이력.

**공통 원칙**
- 연출은 코드 규칙으로 정한다: **대본 단어 > 그림 증거(그룹 이름·크기·팔레트) > 단위 번호**. 난수와 모델 판단이 없다. 바꾸려면 사이드카나 코드·지침서를 함께 고친다.
- 반복: '연속 사용 금지' 고정 규칙은 없다. 대본 상황이 이어지면 같은 효과·전환을 또 쓰고, 상황 없이 채우는 선택만 직전과 다르게 돌린다.
- 그림 에이전트는 오브젝트 그룹에 뜻이 드러나는 이름을 붙인다(`mv-<종류>-<물건>`, 머리 명사를 마지막에). 이름 없는 그룹은 어떤 규칙에도 걸리지 않는다.

**절 찾기**

| 절 | 내용 |
|---|---|
| 4-1 | 카메라, 인물 동작, 센터 모션, 오브젝트 모션, 배경 효과, 텍스트 효과 |
| 4-2 | 생성 클립 프롬프트 |
| 4-3 | 장면 나누기와 전환 |
| 4-4 | 방향 규칙 |
| 4-6 | 오픈소스 라이브러리 효과 |
| 4-7, 4-8 | 붙임 규칙·점검 도구, 축 카탈로그 |
| 4-9, 4-11 | 기울어진 은하, 사람 팔 곡선·천칭 |
| 4-10 | 오브젝트 모션 다양성·테마 팩 |
| 4-12 | 가닥마다 개별 축, 몸 쪽 끝 축, wiggle 값 |
| 4-13 | 센터 모션 단어 규칙·상한 |
| 4-14, 4-15 | 빠른 두근거림 금지, 등장 모션 숨김 |

(4-5는 없다.)

### 4-1. 움직임 방식

#### 카메라
- 모든 그림에 드리프트 카메라(20-1).
- **포커스 확대**: 사이드카 `focus [x, y, 배율]`(배율 1.5~2.2)과 `focus_word`(컷 대본에 있는 단어). 그 단어를 말하기 0.5초 전에 1.4초 동안 가속·감속으로 확대한 뒤 컷 끝까지 정지한다. 한 컷에서 여러 번 움직이지 않는다. 가장자리 밖이 보이지 않게 확대 중심을 제한한다.
- **포커스 스포트라이트**: 확대 1.4초 동안 주변이 어두워진다(가운데 투명, 바깥 검정 50%, 원 반지름은 배율에 맞춰 화면 폭의 30%~62%). 라벨·말풍선은 그 위. 사이드카 `"spot": false`로 끈다.
- **금지**: 그림 전체 부유(±12px), 먼지 입자, 빠른 휩팬·흔들림·회전. 움직임은 작고 자연스럽게.
- **이동 속도**: `mv-path`·트래킹 카메라는 구간의 15%만 부드럽게 출발·정지하고 나머지는 일정한 속도(`miyaCruise`). 경로는 급꺾임 없이 접선이 이어지는 곡선으로 그린다.

**카메라 트래킹**
- 쓰는 때: 대본이 길게 이어지는 움직임·여정·훑어봄을 말하는 단위(걸어가는 생물, 이동하는 무리, 시간선·먹이사슬·지층 훑기, 흐르는 강, 날아가는 것, 쓰러지는 연쇄 등). 예시 목록이 아니라 대본이 말하는 장면에서 정한다. 따라갈 움직임이 없는 단위에는 넣지 않는다.
- 자동: 경로를 따라 도는 물체(`mv-path`)나 도미노 연쇄(`mv-topple` 3개 이상)가 있으면 자동으로 따라간다.
- 직접: 그 밖에는 빈 그룹 `mv-track-*`(`data-path` = 카메라 중심 경로, `data-delay`, `data-dur`, `data-scale`)으로 정한다.
- 처음 12%에 확대(기본 1.3배, 사이드카 `"track": {"scale": 1.4}`)되고 끝 12%에 원래 크기로 돌아온다.
- 트래킹이 있는 그림은 포커스 확대와 드리프트 카메라를 쓰지 않는다. `"track": false`로 끈다.
- 구현 `tools/motions.py` `track_spec`·`miyaTrack`, 빌드 로그 `tracking cams`. 실제 MP4에서의 모습은 미확인.

**카메라 확장 (큰 그림 위를 지나감)**
그림 한 장을 크게 그리고(사이드카 `"world": [w, h]`, 예 [3840,1080] 가로 이동, [1920,2160] 세로 스크롤) 그 위를 `mv-track-*`로 지나간다. 트래킹 한계는 world 크기로 계산한다(`track_js`의 WW/WH).

| 연출 | 만드는 법 |
|---|---|
| 지역 이동 | 가로 world + 경로 |
| 세로 스크롤 | 세로 world + 경로 하나(일정 속도) |
| 밀어넣어 이어붙이기 | `data-scale`≥3 트래킹 뒤 `match`/`zoom` 전환 |
| 분할 화면 | `slide` 패널 둘 |
| 초점 이동 | `rack` |

쓰지 않는 것: 로그 줌 다이브, 끊기는 스크롤(빠르게 감기·속도 램프), 정지 화면(프리즈).

#### 인물·사물 동작 (필수)
인물 그림에 `mv-` 그룹 장면당 3~6개, 앞쪽 인물마다 최소 하나. 생물의 관절 모션은 20-6.

| 그룹 | 움직임 |
|---|---|
| `mv-breathe-*` | 몸통 세로 1.00→1.03, 2.2초(모든 인물) |
| `mv-nod-*` | 머리 ±3°, 1.8초(축 목) |
| `mv-lean-*` | ±2°, 3초 |
| `mv-arm-*` | ±7°, 1.4초(축 어깨: `tools/pivots.py`가 팔 첫 선의 몸 쪽 끝을 자동 계산) |
| `mv-hand-*` | 손 중심 ±5°, 1.0초(들어올림 없음) |
| `mv-walk-*` | 좌우 120px, 3.5초(양옆 60px 비울 때만) |
| `mv-flame-*` `mv-spark-*` | 세로 맥동 0.25~0.30초 |
| `mv-smoke-*` `mv-steam-*` `mv-cells-*` `mv-key-*` | 위로 떠오름 |
| `mv-glint-*` `mv-lamp-*` `mv-lantern-*` `mv-beacon-*` | 제자리 맥동(크기 1→1.06, 투명도 .85→1, 1.2~1.5초) |
| `mv-blink-<이름>` | 눈(흰자+눈동자) 그룹. 불규칙 간격(3.1 / 4.2 / 0.35 / 2.5초 순환)으로 0.07초 감았다 뜸. 눈을 따로 그룹으로 그릴 때만(`tools/art_spec.md` 7장) |

- 모르는 `mv-` 이름의 기본값은 느린 glow다(4-14).

#### 가운데 물체(센터) 모션 `mv-core-<타입>`
물체 성격으로 고른다. 가운데 물체 자체는 필수가 아니다(3-2).

| 타입 | 움직임 | 쓰는 곳 |
|---|---|---|
| `spin` | 회전 초당 36° | 렌즈·시계·행성 |
| `sway` | 축 ±14°, 1.4초(축은 이름으로, 아래 축 자동 교정) | 램프·종·열쇠 |
| `orbit` | ±34px·±26px, 2.4초·3.1초 | 위성·곤충 |
| `glide` | 좌우 ±60px, 2.6초 | 배·구름 |
| `heartbeat` | 기본은 느린 맥박(1.6초 주기, 1.07→1→1.04→1). 강한 박동(0.9초)은 4-13의 단어가 있을 때만 | 심장·세포 |
| `flicker` | 투명도 .35~1, 1초 | 촛불·별 |
| `swell` | 1→1.2, 2.2초 | 숨·풍선 |
| `tremble` | ±5px·±1.5°, 0.07초 | 긴장·균열 |
| `approach` | 컷 내내 1→1.3 | 발견·접근 |
| `reveal` | 투명도 .15→1·크기 .6→1, 0.7초 후 정지 | 처음 등장 |
| `squeeze` | 가로 .55·세로 1.2, 1.1초 | 세포·물방울 |
| `wobble` | 제자리 → 0.2초 뒤 14°·1.1배로 톡(0.18초) → 탄성 복귀 2초 | 충격 뒤 |
| `roll` | −110→+110px·−180→+180° | 구르는 것 |
| `pop` | 0.15초 뒤 .2→1, 0.6초 back.out | 새 등장 |
| `ping` | 고리 1.3초마다 .85→1.8, 불투명도 .95→0 | 신호·경보 |
| `stamp` | 1.8배·투명에서 쾅 0.28초 + 고리 | 결정·도장 |
| `flip` | 가로 뒤집기 0.46초, 2.4초마다 | 동전·반전 |
| `draw` | 윤곽 1.3초 후 채움 | 설계도·새 개념 |
| `drop` | −18° 기운 채 떨어져 튐, 0.9초 bounce.out | 떨어지는 것·결과 |
| `turn` | 그 그룹만 초당 90°(이웃을 묶지 않음) | 풍차 날개+허브처럼 코어 자체가 도는 부분 |

- **배분**: 앞뒤 같은 타입 금지, 한 영상 10종 이상, 한 종류 20% 이하, 위아래로만 움직이는 모션 금지. 위반 시 빌드 `WARNING`(멈추지 않음). 사건 종류의 단어 조건과 15 % 상한은 4-13.
- `mv-glint-core`만 있으면 `tools/motions.py`의 `legacy_core_type`이 자동 배정한다. 에이전트가 직접 고르는 쪽이 낫다.
- 렌더 페이지가 열릴 때 `miyaWrapCores`가 코어 그룹(글로우)과 그리기 순서상 이웃한 도형 중 가운데 원판(반지름 170px 안, 크기 460px 이하)에 놓인 것을 `<g>`로 묶어 모션을 건다.
- `ping`·`stamp` 고리: 어두운 테두리 12px + 노랑 `#ffcf5a` 6px. `draw`는 선 있는 도형을 그린 뒤 나머지를 페이드인.

**움직이는 부분이 있는 물체는 전체를 돌리지 않는다**
- 날개·바늘·시계 손·플라스마 고리처럼 따로 움직여야 하는 부분이 있는 물체에는 물체 전체를 돌리거나 뒤집거나 흔드는 코어 모션(`spin`·`roll`·`flip`·`wobble`·`tremble`·`orbit`·`sway`)을 쓰지 않는다(`miyaWrapCores`가 탑·시계 판·받침까지 한 덩어리로 묶는다).
- 움직이는 부분만 따로 그룹으로 그린다.

| 움직임 | 그룹 | 속성 |
|---|---|---|
| 계속 도는 것 | `mv-rotor-<이름>` | `data-pivot="x y"`, `data-per`(한 바퀴 초), `data-dir`(1/-1). 시계 분침 14초·시침 70초, 초침 6초, 플라스마 고리 9초 |
| 왔다 갔다 하는 것 | `mv-joint-<이름>` | 계기판·나침반 바늘, 진폭 3~22° |

- 코어 모션은 `swell`·`heartbeat`·`approach` 같은 부드러운 것으로 하거나, 코어 그룹 자체가 돌 부분이면 `mv-core-turn`.
- 날개 그룹 안에는 날개·허브·글로우만 두고 탑·몸통은 그룹 밖에 둔다.

#### 오브젝트 모션 73종 `mv-<종류>-<이름>` (위치 제한 없음)
구현 `tools/motions.py`의 `obj_js`·`OBJ_KINDS`. 모두 유한 트윈이고 `data-delay`(그림 시작 후 초, 기본 0.3), `data-dur`(기본 1.0)을 받는다. 종류마다 코드 주석에 축이 적혀 있다.

**속성이 정해진 종류**

| 종류 | 움직임과 `data-*` |
|---|---|
| `path` | `data-path="M.. C.."` 경로를 따라 이동하고 진행 방향으로 돎(`data-rot="0"`이면 안 돎). 기본 길이는 그림 길이−0.6초, 최대 3.4초 |
| `flip` | `data-pivot` 둘레로 `data-deg`(180)° 뒤집기(모래시계) |
| `fill` / `grow` | `data-from`→`data-to`(0→1), `data-axis`(y 또는 x) 크기 변화(모래, 막대, 게이지). `grow`는 0에서 시작 |
| `swing` | 감쇠 진자 `data-amp`(28°)·`data-per`(2.4초) |
| `topple` | `data-deg`(72)° 쓰러짐, 0.55초. 그룹마다 `data-delay`를 0.2초씩 늘려 연쇄 |
| `liquid` | `data-rise`(px) 올라오며 `data-scroll`(px) 옆으로 흐름(물결 윗면의 넓은 도형을 용기 clipPath로 자른다) |
| `bubble` | `data-rise` 올라가며 사라짐, `data-per`(1.6초) 반복 |
| `edge` | 그룹 안의 선이 그려짐(네트워크 연결선) |
| `keyturn` | 옆에서 본 열쇠 손잡이가 축 둘레로 돎(세로 1→`data-to` .32) |
| `shackle` | 걸쇠가 `data-lift`(46)px 올라가며 `data-deg`(−16)° 열림 |
| `popin` | 제자리에서 튀어나옴. `data-axis="x|y"`로 한 방향만 |
| `shake` | 좌우 떨림 `data-amp`(3px)·`data-dur`(.25초)(자물쇠 찰칵·충돌) |
| `dash` | 점선이 선을 따라 흐름 `data-speed`(40px/초)(지나온 경로) |
| `scroll` | 그림 내내 옆으로 `data-dist`(160px) 흐름(별·구름 시차) |
| `slam` | 2.4배에서 쾅 들어옴(도장·제목) |
| `rise` | `data-from`(60px) 아래에서 떠오르며 나타남(태그·표지) |
| `slide` | `data-dx`/`data-dy`(기본 −960/0)만큼 미끄러져 들어옴, `data-dir="out"`이면 나감, 0.7초 |
| `fade` | 투명도 `data-from`(0)→`data-to`(1), `data-dur`(.4)(유령 잔상 .1→.6, 지움 1→0) |
| `ticks` | 그룹 안 자식을 `data-step`(.1초)마다 하나씩 켬(`data-fill`로 채움 표시, 칸 n개 = 수량) |
| `rack` | 초점 이동: 흐린 복제 6장이 `data-r`(14px)에서 선명해짐(`data-dir`="in")/흐려짐("out"), 1.2초. SVG 필터 없이 구현 |
| `disc` | 기울어진 은하 원반의 자전(4-9) |

**이름으로 쓰는 종류 35종 (축)**
bob·hover·pendulum(꼭대기)·wiggle(값은 4-12)·tilt(밑)·crumble·emph·spin·rollby·float·flap(가운데 세로축)·swim·hop(발)·drip(위)·unfold(위 모서리)·unroll(왼쪽 모서리)·flagwave(깃대 쪽)·ripple·sparkle·circle(`data-pivot` 궤도 중심 필수, 없으면 float)·squash(발)·neon·shiver·beat·settle·magnet·bouncing(발)·creep·sink·ascend·tick(가운데)·flicker·breathe·nodding(목)·sway(밑).

**그 밖**: 라이브러리 6종 `draw·morph·toss·skid·coast·regroup`은 4-6, 2026-11-05에 더한 10종 `teeter·jiggle·peek·spiral·zigzag·lift·scatter·converge·nudge·hatch`는 4-13.

**순서 규칙**
- 열쇠는 옆에서 구멍에 꽂고 **먼저 돌린 뒤** 걸쇠가 열린다(위로만 열리는 것 금지, 시계방향).
- 모래시계는 뒤집은 뒤 윗칸 모래가 줄고 아랫칸이 바닥부터 쌓인다.
- 모션 시작은 같은 그림 안에서 `data-delay`로 순서를 맞춘다(두 번 재생되는 것처럼 보이지 않게). 전환 중 시작한 모션은 컷이 시작해도 이어진다.
- 시작 전에 숨겨야 하는 모션은 4-15.

#### 장면은 대본 내용에서 정한다
위 종류·트래킹·말풍선은 **블록**이다. 어떤 그림에 무엇을 쓸지는 그 단위의 대본에서 정한다(예시 목록이 아니다).
1. 그림 에이전트는 단위마다 대본이 말하는 사건·움직임·변화·관계를 문장으로 적는다(예: "열쇠가 구멍에 들어가 돌아 문이 열린다", "배가 항구를 떠나 수평선으로 간다").
2. 그것을 가장 정확히 보여 주는 모션을 고른다. 여러 종류를 조합해도 된다(경로 이동+점선 궤적+카메라 트래킹, 뒤집기+채움+흔들림).
3. 맞는 것이 없으면 새 종류를 `tools/motions.py`의 `obj_js`에 더하고 `OBJ_KINDS`·이 절·`art_spec.md` 7장·`frog_rig.obj_span`(7-2 I-6-2)에 적는다.
4. 움직일 사건이 없는 단위(정적 설명, 인물 대화)는 억지로 넣지 않고 인물 모션·말풍선·카메라로 둔다.
5. 쓴 모션과 이유를 그림 사이드카·보고에 한 줄로 적는다.

**화면 구성 블록 → 만드는 법**

| 구성 | 만드는 법 |
|---|---|
| 격자 = 수량 | `ticks`(fill) |
| 지층 | `grow` + `fade` |
| 틈 속 들여다보기 | `slide` 층 + `mv-track` scale≈1.8 |
| 숫자 쾅 | `num` 라벨 + `slam` |
| 자석 | `path` |
| 펜 두 개 | `edge` 그룹 둘(같은 `data-delay`) |
| 지우개 | `slide`(dir out) + `fade` 1→0 |
| 유령 | `fade` .1→.6 |
| 페이지 넘김·찢긴 종이 | 전환 `page`/`zigzag` |
| 극단적 크기 대비·예외 하나 | 그림 구성 |

#### 자동으로 붙는 생기
모두 단위의 시간·그룹 이름·단위 번호로만 정해진다.

| 항목 | 규칙 | 코드 |
|---|---|---|
| 칠판 빈칸 | 아직 안 나온 행의 점선 빈칸이 숨 쉰다(투명도 .5↔1, 1.1초, 행이 뜨면 사라짐) | `motions.chalk_life_js` |
| 칠판 공백 | 행 사이 공백이 7초를 넘으면 5초마다 마지막으로 뜬 행의 숫자가 한 번 커졌다 돌아오고(1.08배, 0.16초) 개구리 팔이 그 행을 톡 친다(y −7px). 결론 줄도 같다 | 같은 함수 |
| 멈춤 뒤 숨쉬기 | `path`·`slide`(in)·`slam`·`popin`·`rise`·`topple`·`flip` 같은 일회성 모션이 끝나고 2.5초 넘게 남으면 컷 끝까지 1→1.03 숨쉬기(2.6초 sine). 얼어붙은 물체 금지 | `motions.settle_js` |
| 유성 | 밤 배경·space/deepfield 팔레트 그림 중 6초 넘고 단위 번호 `k % 3 == 1`인 단위에 한 번(글로우 선+머리, 0.55초, 처음·끝 1.5초 제외, 위치·시각은 단위 번호의 황금비 분수) | `build3.py` `is_cosmic` |
| 두드림 파장 | 개구리 `tap` 동작 때 닿는 자리에 고리(`_tp`) | 7-2 D |

- 그림 단위에 모션이 전혀 없는 구간이 남으면 `python3 tools/check/motion_check.py render/<slug> --step 5`로 확인하고 그 단위에 `frog_hint` 또는 `mv-` 그룹을 더한다.

#### 축(피벗) 자동 교정
`motions.pivot_of`·`core_sanitize`·`obj_sanitize`, 빌드 로그 `motion sanity`. 그룹 이름의 꼬리말(`mv-core-sway-tree`의 `tree`)로 축을 정한다. 물건별 축은 4-8 카탈로그가 기준이다.

| 이름 묶음 | 규칙 |
|---|---|
| 땅에 선 것 `BOTTOM_NAMES`(tree·pole·tower·person·house·flag…) | 밑동 고정(origin 50% 100%, ±5° 2.2초) |
| 매달린 것 `HANG_NAMES`(lantern·bell·rope…) | 꼭대기 고정 |
| 가운데가 축인 것 `CENTER_NAMES`(ship·scale·planet…) | 가운데(±6°) |
| 둥근 것 `ROUND_NAMES`이 아닌 것 | spin/roll/flip/turn/circle을 wobble·glide·sway로 바꿈 |
| 무거운 것 `HEAVY_NAMES`(whale·ship…) | drop을 swell로 바꿈 |

- 일부러 그렇게 그린 경우만 그룹에 `data-keep="1"`.

#### 배경 효과 63종 (`motions.FX_KINDS`, `fx_for`가 그림마다 최대 하나)
그림 에이전트는 비·눈·입자를 그리지 않는다.

| 묶음 | 종류 |
|---|---|
| 입자 30종(`PARTICLES` 표에 모양·색·크기·방향·주기·흔들림·깜빡임) | snow·hail·bubbles·embers·sparks·ash·pollen·fireflies·leaves·petals·confetti·feathers·sand·meteors·twinkle·coins·notes·hearts·questions·plankton·seeds·spores·bats·birds·fish·jellies·germs·lanterns·balloons·droplets |
| 전면 효과 | rain·flash·bolt·fog·heat·rays·searchlight·vignette·tint·clouds·windlines·smoke·steam·shockwave·letterbox·scanlines·glitch·lightleak·flare·aurora·ripples·waves·rainbow·spotlight·frost·starburst |
| 물리 폭발 | `burst`(4-6) |
| 2026-11-05 추가 6종 | ink·paperbits·bokeh·crystals·eclipse·horizonglow(4-13) |

**고르는 순서**
1. 단위 대본 단어 규칙 `FX_WORDS`(우선순위 표, 예 rain→rain, bacteria→germs, death→vignette).
2. 그림 증거: `tools/picev.py`가 오브젝트 그룹 이름·크기로 읽은 태그(fire·smoke·steam·rain·ice·candle·bubble·water·flower·forest·desert·sun·insect·bird·wind·cloud·space·cave·bone)로 고른다(`motions.FX_PIC`: 그려진 불 → embers, 굴뚝 → smoke, 호수 → bubbles/ripples, 태양 → rays…). 배경 레이어(별 안개·입자 줄·하늘)는 증거가 아니다.
3. 팔레트별 잔잔한 효과 `FX_AMBIENT`를 짝수 단위마다 순환(ocean: bubbles·plankton·fish·ripples, forest: pollen·leaves·seeds·spores, space: twinkle·meteors…). body·lab은 단어가 있을 때만.

**조건**
- 단어로 고른 효과는 다음 그림에 같은 단어가 또 있으면 또 나온다. 채움용 앰비언트만 직전과 다른 것으로 돌린다.
- 무거운 효과(`HEAVY_FX`: vignette·flash·letterbox…)는 앞 두 그림에 무거운 효과가 없을 때만.
- 밤 전용(`NIGHT_ONLY`: twinkle·fireflies·bats·meteors·aurora·lanterns·searchlight·spotlight·bokeh)은 종이 배경에 안 나온다(그림 증거일 때는 `FX_PIC_DAY`로 대체).
- 3초 미만 그림과 칠판에는 없다. 우주 그림은 유성과 겹치지 않게 `k%3==0`에만 잔잔한 효과.
- 입자는 그림의 `<g translate>` 안에 두고 GSAP은 그 안쪽만 움직인다(x/y가 transform 속성을 덮어쓰기 때문).
- 방향은 4-4.

#### 텍스트 효과 39종 (`labels_lib`, 자막 제외)

| 대상 | 규칙 |
|---|---|
| 이름표 등장 `NAME_FX` 25종 | 그림 증거 `PIC_FX`가 있으면 그것(불 → glow, 물 → wave, 얼음 → squeeze, 비 → drop, 시계 → flip, 톱니 → spin, 책·타자기 → typewriter, 군중 → scatter, 새 → fan, 연기·동굴 → blur…). 없으면 `(단위 번호×7 + 라벨 번호) % 25`로 pop·typewriter·slideleft·rise·flip·zoom·stamp·wobble·blur·wave·drop·scatter·spin·swing·elastic·sink·slideright·bounceletters·zoomletters·flipletters·glow·underline·highlight·squeeze·fan 중 하나(글자별 효과를 위해 이름표 글자는 `<i>` 하나씩) |
| 이름표 단어 규칙 | `scramble`·`type`(4-6, 3-6 9번) |
| 말풍선 `SAY_FX` | 문장부호로: `!`=slam(쾅 들어와 떨림), `?`=tilt(갸웃), `...`=slowfade, `~`=jiggle, 그 외 pop. 3단어 이상이면 `splitwords`(4-6). 2.2초 넘게 떠 있으면 둥실(bob) |
| 숫자 배지 `NUM_FX` 6종 | slide·drop·flip·zoom·stamp·flashbg 순환(+카운트업·착지 바운스) |
| 강조 | 위험 단어(`DANGERW`)가 있으면 말풍선이 한 번 떤다. 핵심 문장 단어(`KEYW`: the key·in fact·turns out…)면 이름표가 1.1초 뒤 한 번 커졌다 돌아온다 |
| 칠판 | 제목 글자 쓰기(`chalk_title_js`), 결론 밑줄(`chalk_concl_js`) |

#### 구현 조건과 확인 상태
- 유한 반복 GSAP 트윈(seek 가능), SVG 필터 금지. 인물 `id`는 서로 다르게, 정지 상태로도 자연스럽게.
- 확인: 합성 페이지(오브젝트 56·효과 57·텍스트 36)에서 JS 오류 0, 모든 트윈이 컷 안에서 끝남, 축 교정 전후 비교.
- 미확인: 인물 동작의 자연스러움(사용자가 판단), 실제 영상 전편 렌더에서의 모습.

### 4-2. 이미지→영상 프롬프트 템플릿 (영어, 생성 클립용)
```
subtle natural motion, camera still until the focus object is mentioned then one slow eased push toward it, [one action of the main subject],
keep art style and line art consistent, no morphing, no text
```

### 4-3. 장면 나누기와 전환

**장면 나누기**
- **한 장면 = 새 그림 한 장 = 대본 의미 단위 하나.** 길이는 20-2가 기준이다(최소 8.5초, 최대 단위 9.3초, 초반 5분·숏츠·느린 장면 값).
- 그림 장수 제한 없음(15분 본편은 약 90~110장).
- 같은 그림을 확대·이동만 바꿔 여러 컷으로 쓰지 않는다. 컷이 바뀌면 그림이 바뀐다.

**전환 종류** (구현 `build3.py`, `tools/motions.py`의 `tr_js`·`miyaTr`)

| 전환 | 모습 | 쓰는 곳·단어 |
|---|---|---|
| `zoom` | 나가는 그림은 가운데 물체로 가속 확대(약 2.6배, 1.1초), 들어오는 그림은 확대 상태에서 감속(1.7초) | 큰 구간 전환, "들여다본다" |
| `match` | 가운데 물체 자리(반지름 120px 원)에서 0.9초 원형으로 열림 | 앞뒤 물체가 같은 위치·크기·색 계열이고 같은 장면 안일 때만 |
| `slide` | 오른쪽에서 0.7초, 나가는 그림은 폭 18%만 밀림 | 순서·나열·비교 |
| `fade` | 0.6초 | 같은 장소 시간 경과 |
| 워시 | 배경색(종이 `#ece4d1`, 밤 `#14122b`, 노을 `#5a4562`)으로 0.45초 덮였다 0.45초 걷힘 | 새 개념 |
| `wipe` | 노란 빛 선(`#ffd54a`) 대각선, 방향 번갈아, 0.8초 | 원인→결과 |
| `iris` | 사이드카 `iris: [x, y]`(없으면 가운데 밖 `focus` 점, 없으면 좌우 번갈아)에서 원이 열림, 0.9초 | 옆 대상 이야기로 |
| `eye` | 가로 한 줄에서 위아래로, 0.8초 | open, wake, realize, discover, reveal, see |
| `push` | 위로 밀기 0.7초 | fall, drop, sink, deep, down, rise, climb, up |
| `whip` | 0.45초 + 흰 속도선 9개 | speed, fast, race, rush, sudden, instant, light, flash |
| `tilt` | −8°·1.25배 카드처럼, 0.8초 | ?, imagine, what if, surprise, twist |
| `seam` | 좌하단에서 우상단으로 노란 선이 그어진 뒤(0.35초) 두 줄로 갈라지며 사선 띠가 넓어짐, 1.0초 | because·cause·result |
| `diamond` | 오른쪽 위(화면 73%·28%) 한 점에서 마름모가 열리고 노란 윤곽이 사라짐, 0.9초. 네 모서리를 완전히 덮은 뒤 끝난다 | 열쇠·보석·비밀·unlock |
| `page` | 앞 그림이 왼쪽 가장자리로 접혀 사라지고 새 그림이 오른쪽에서 드러남, 흰 선이 경계를 따라감, 0.8초 | chapter·story·history |
| `zigzag` | 흰 지그재그 찢김 선이 왼쪽에서 오른쪽으로 쓸고 감, 0.9초 | break·split·crack |
| `wave` | 노란 물결선이 아래에서 올라오며 새 그림이 드러남, 1.0초 | water·ocean·flow |
| 하드컷 | | 칠판 앞뒤 |

- **쓰지 않음**: 색 막대(`blinds`, 코드는 남음), 시계방향 부채꼴 와이프, 점 격자/모자이크, `pulsevig`, `gridripple`.

**자동 선택(`TR_WORDS`)**
- 단위 대본에 위 단어가 있고 그 전환이 제 몫(전체의 1/16)의 1.3배 이하이면 항상 그 전환을 쓴다(연속이어도).
- 단어가 없는 컷은 적게 쓴 종류부터 고르며 직전 종류를 피한다.
- 장면이 바뀔 때는 줌·워시·눈 뜨기를 더 자주.
- 느린 장면은 차분한 전환만(20-2).
- 가운데 물체가 없는 그림 사이에서는 `match`·`zoom`을 후보에서 뺀다(3-2).

**효과음**

| 전환 | 일반 | 우주 모드 |
|---|---|---|
| 줌·슬라이드(낮게)·wipe·push·whip | swish | wipe·push·whip = warp |
| match·iris·eye | hush | iris·eye = glimmer |
| 워시 | rustle | |
| tilt | pop | |
| 페이드 | 무음 | |

- 전환은 앞 장면 빈 간격(0.8초) 안에서 시작해 내레이션과 겹치지 않는다.
- 미확인: 추가 전환의 Actions MP4 모습.

### 4-4. 방향 규칙 표
방향이 걸리는 모든 것은 **대본 단어·그룹 이름·그림 안 위치**로 코드가 맞춘다. 빌드 때 자동이며 로그 `direction sanity`에 나온다.

**방향 문맥 (`facing.context()`가 그림 한 장마다 정하는 세 값)**

| 값 | 정하는 법 |
|---|---|
| travel | 주인공 이동 방향(옆으로 이동하는 그룹의 경로·dist 부호) |
| wind | 사이드카 `wind: "left"|"right"`. 없으면 이동의 반대(맞바람), 이동이 없으면 +1(오른쪽) |
| attractor | 사이드카 `attractor: [x, y]`. 없으면 이름에 hole·vortex·whirl·drain·magnet·gravity·funnel·mouth·maw·sun·star가 든 가장 넓은 그룹의 중심 |

**A. 이동·중력·바람**

| 가족 | 무엇이 | 어떻게 맞추나 | 코드 |
|---|---|---|---|
| 이동 ↔ 머리 | path·swim·rollby·creep·magnet·slide 그룹 | 머리 = 어두운 동공(≤4개) 위치 > `data-face` > 눈이 없으면 **뾰족한 쪽**(rocket·arrow·probe·plane·comet·ship·boat·sub·sled·train·car… 이름일 때 좌우 20% 띠의 윤곽 높이 비 < .6). 이동과 다르면 그림을 몸통 중심으로 거울상. 그룹에 transform·text가 있으면 뒤집지 않고 로그만 | `facing.facing_sign`·`apply` |
| 중력 | 이름에 sink·fall·drop·descend·plunge·dive·settle(내려감) / rise·ascend·climb·launch·lift·soar·bubble·float·balloon·escape(올라감)가 든 `mv-path` | 경로가 반대로 가면 경로를 뒤집음(끝→시작). 탈것 이름(lander·carcass)은 판단하지 않음 | `facing._path_rules`, `reverse_path` |
| 빨림 | attractor가 있는 그림의 `mv-magnet`, 이름·태그에 pull·suck·spiral·drain·inward·toward·into·capture·plunge가 든 `mv-path` | magnet은 `data-dx/dy`를 attractor 쪽으로 다시 계산, path는 끝점이 attractor에서 멀어지면 뒤집음(A·S·T 명령 경로는 로그만) | 같은 함수 |
| 바람 흔적 | 배경 입자 수평 이동, 비 기울기(`x + ds·L·.35`), 바람선(`windlines`) 좌우, 안개·구름 흐름 | 전부 `dir_sign(kind, wind, travel)`: 생물 줄(fish·birds·bats)은 travel 쪽으로(머리도 뒤집음), 나머지는 wind 쪽으로 | `motions.fx_markup`·`fx_js` |
| 유성·줄무늬 | `streak` 꼬리 | 이동의 반대쪽 | `motions._shape0` |
| 카메라 | 이동 그림의 드리프트 팬 | 세계가 이동의 반대로 밀림(= 카메라가 따라감), 역방향 팬 금지 | `build3` `dx = -travel·W·.025` |
| 개구리 타기 | 탄 개구리 | 이동 방향을 봄(`flip = travel_sign`) | `frog_place` |
| 개구리 밀기 | 밀 수 있는 물건(lens·cart·crate·rock·sled…)이 오른쪽으로 이동 | 개구리는 물건 **뒤**(왼쪽)에서 밀며 오른쪽을 봄. 왼쪽 이동이면 원래 자리(오른쪽·손잡이) | `frog_place` PUSHG |
| 슬라이드 | `mv-slide` 패널 | 들어올 때 `data-dx` 반대로, 나갈 때(`data-dir="out"`) `data-dx` 쪽으로 이동하는 것으로 셈 | `facing.travel_sign` |

**B. 맞물림·바람·시선·빛 (`facing._dir_rules2`)**

| 가족 | 무엇이 | 규칙 | 비고 |
|---|---|---|---|
| 톱니 맞물림 | 이름에 gear·cog·sprocket이 든 `mv-spin`·`mv-rotor`·`mv-core-spin/turn` 그룹 | 서로 닿는(중심 거리 ≈ 반지름 합) 톱니는 반대 방향: `mv-core` 톱니가 기준(+1), 나머지 `data-dir`를 2색 칠하기로 고침 | 홀수 고리(세 톱니가 서로 다 닿음)는 고칠 수 없어 로그만 |
| 깃발 | 이름에 flag·banner·pennant·windsock·sail·streamer | 깃대 = 그룹 안 가장 키 큰 가느다란 도형. 천이 바람 반대쪽에 있으면 깃대를 축으로 거울상 | 깃대가 없으면 왼쪽 가장자리가 깃대 |
| 기울어진 것 | smoke·steam·plume·exhaust·hair·scarf·cape·spray·mane·mist·grass·reed·wheat·kelp·flame·fire·candle | 윤곽의 위 30%와 아래 30% 평균 x 차이가 높이의 8% 넘고 바람과 반대면 가운데 축으로 거울상 | 깃발·기울기 둘 다 바람을 아는 그림에서만(사이드카 `wind` 또는 이동 오브젝트). 멈춘 그림은 그린 대로 |
| 시선 | 이름에 person·man·woman·kid·scientist·astronaut·owl·cat·dog·bear·deer·cow·bird·fish… 그룹(부품 `mv-chain/joint/limb`·이동 그룹 제외) | 초점(이동 오브젝트의 경로 중간 > attractor > 가장 넓은 `mv-core`)이 150px 넘게 옆에 있는데 눈이 반대를 보면 몸 중심으로 거울상 | 눈이 없으면 판단 안 함(`data-face`로 지정 가능) |
| 빛·그림자 | 광원 = 사이드카 `light: "left"|"right"` 또는 이름에 sun·lamp·lantern·candle·torch·moon·bulb·fire·flame·window가 든 가장 넓은 그룹. 대상 = 오브젝트 그룹 안의 id/class에 shadow·shade·highlight·glint·shine·specular·rimlight가 든 도형 | 그림자는 광원 반대쪽, 하이라이트는 광원 쪽(그룹 중심 기준 폭의 8% 넘게 치우친 것만). 아니면 그룹 중심 축으로 거울상 | 광원이 없는 그림은 점검 안 함. 바닥 전체를 덮는 그림자(폭 90% 이상)는 제외. id 없는 도형은 로그만 |
| 소용돌이 ↔ 개구리 궤도 | 블랙홀·소용돌이를 도는 개구리(`orbit` 동작) | 고리 그룹의 `data-dir`(`mv-spin`·`mv-rotor`), 없으면 그림의 첫 `mv-circle`/`mv-spin`/`mv-rotor`의 `data-dir`, 없으면 시계방향. 개구리도 같은 방향 | `facing.spin_dir`, `frog_place`가 `act.dir`에 적음 |

- **그림 에이전트가 직접 맞추는 것**: 그려진 두 사람끼리의 시선 교환, 그룹 밖에 따로 그린 그림자. 톱니 셋이 서로 다 닿는 배치는 그리지 않는다. 눈이 없는 탈것·화살은 그룹에 `data-face`를 적는다(로그 `unknown facing`).
- **점검**: `python3 tools/facing.py <슬러그>`가 그림별 문맥·경로 규칙·그룹 판정을 출력한다(파일은 바꾸지 않음). 빌드 로그 `direction sanity`에 뒤집은 수·맞바람 그림 수·attractor 수가 나온다.
- 예시: `/mnt/project-files/frog-rules/direction/rules2-before-after.png`.

### 4-6. 오픈소스 라이브러리 효과 표
빌드에 들어 있는 것: GSAP 3.15 플러그인 14개, anime.js, lucide 아이콘 2,193개, svgo. `tools/fxlib.py`가 등록·이징·규칙을 맡고 파일은 `tools/assets/gsap/`·`anime.min.js`·`lucide.json`.
- 모델이 고르지 않는다. 사이드카로 끄거나 바꿀 수 있다. 빌드 로그 `library fx`에 무엇이 몇 번 붙었는지 찍힌다.
- 모든 효과는 GSAP 타임라인에서 seek된다(anime 타임라인도 `miyaAnime` 프록시로 seek). 구간 렌더에서도 같은 프레임이 나온다.

| 라이브러리 | 무엇 | 규칙(누가 고르나) | 코드 |
|---|---|---|---|
| DrawSVGPlugin | 오브젝트 외곽선이 펜으로 그리듯 그려지고 채색이 뒤따름 | 그림 에이전트가 `mv-draw-<이름>`(지도·설계도·경로·스케치 장면). 라벨·배지 픽토그램은 자동으로 이렇게 등장 | `motions.obj_js('draw')`, `fxlib.LIB_JS miyaIconDraw` |
| MorphSVGPlugin | 한 모양이 다른 모양이 됨(A가 B로 변한다는 문장) | 에이전트가 `mv-morph-<이름>` 그룹에 첫 path(지금)+마지막 path(목표, `opacity="0"`). `data-back="1"`이면 되돌아옴 | `miyaMorph` |
| MotionPathPlugin | 등록만(`mv-path`는 자체 `miyaPath`) | | |
| SplitText | 3단어 이상 말풍선의 단어가 하나씩 내려앉음 | `say` 라벨이 느낌표·물음표·말줄임 규칙에 안 걸리고 3단어 이상이면 자동 | `labels_lib.label_js` `splitwords` |
| ScrambleTextPlugin | 이름표 글자가 잡음에서 정리됨 | 단위 문장에 secret·code·decode·cipher·mystery·unknown·signal·hidden·random…(`fxlib.SCRAMBLE_W`). 숫자 있는 라벨은 숫자 문자로 | `name_fx → 'scramble'` |
| TextPlugin | 이름표 타자기(한 글자씩) | 단위 문장에 typed·wrote·letter·telegram·diary·journal·manuscript·report…(`TYPE_W`) | `name_fx → 'type'` |
| Physics2DPlugin | 배경 `burst`: 중심에서 조각 72개가 중력으로 날아감 + 고리 | 단어 confetti·fireworks·shatter·scatter·splash·spray·erupt·burst·explode·detonate·sneeze…(`FX_WORDS` 첫 규칙, 무거운 효과라 2장면 간격) | `fx_markup/fx_js('burst')` |
| Physics2DPlugin | 오브젝트 `toss`: 던져져 포물선 | 에이전트 `mv-toss-<이름>`(`data-v`·`data-angle`·`data-g`) | `obj_js('toss')` |
| InertiaPlugin | `skid`: 미끄러지다 멈춤(스냅) | 에이전트 `mv-skid-<이름>`(`data-v`·`data-dist`·`data-res`) | `obj_js('skid')` |
| PhysicsPropsPlugin | `coast`: 바퀴·팽이·동전이 돌다가 마찰로 멈춤 | 에이전트 `mv-coast-<이름>`. 축 점검은 `spin`과 같음(나무는 못 돎) | `obj_js('coast')` |
| Flip | `regroup`: 여러 개가 그려진 자리에서 고리·줄·격자로 재배치 | 에이전트 `mv-regroup-<이름>`(자식 2개 이상, `data-shape` ring/line/grid). 모이다·줄 서다·흩어졌다 모이다 문장 | `miyaRegroup` |
| CustomBounce | 진짜 튕김 + 찌그러짐 | `bouncing` 오브젝트·센터 `drop`이 자동으로 이 이징(`miyaBnc`·`miyaBnc-squash`) | `REGISTER_JS` |
| CustomWiggle | **쓰지 않는다**(렌더가 멈춘다, 15-8) | 흔들림(`shake`·`shiver`·센터 `tremble`·개구리 `shiver`)은 순수 함수 ease `miyaW`·`miyaJit`. `fxlib.plain_wiggles()`가 문자열 `wiggle()`을 바꾼다 | `REGISTER_JS` |
| CustomEase | 등록(CustomBounce의 바탕) | | |
| EasePack SlowMo | 이동 오브젝트의 속도 램프(천천히→질주→천천히) | 단위 문장에 rush·dash·race·speed·fast·zoom·accelerate…(`SPEED_W`) → `mv-path`의 `data-ease`. 에이전트가 적은 `data-ease`가 우선 | `fxlib.path_ease` |
| EasePack RoughEase | 카메라 자체가 덜컹거림 | 단위 문장에 earthquake·tremor·turbulence·bumpy·rough·storm·engine(s)…(`ROUGH_W`, `engineer(s)`·`engineering`은 제외). 드리프트 카메라만, `randomize:false`(구간 렌더 일치). 주의는 4-12 7번 | build3 드리프트 |
| EasePack ExpoScaleEase | 줌이 일정한 체감 속도로 | 포커스 카메라가 있고 문장에 zoom·closer·magnify·microscope·telescope·tiny·vast…(`ZOOM_W`) | build3 포커스 |
| anime.js spring | 통통 튀는 등장 | 문장이 playful(bounce·hop·jump·spring·excited·cheer…)이고 grim 단어가 없을 때 `popin`·`rise` 오브젝트와 `pop` 이름표. 단위 번호로 soft/medium/stiff | `fxlib.spring_params`, `miyaSpringTo` |
| lucide | 이름표·숫자 배지 앞의 작은 픽토그램(선 그리기로 등장) | 라벨 글자의 단어가 `fxlib.OVERRIDE`(whale→fish, years→calendar, brain, virus→biohazard…) 또는 아이콘 이름과 같을 때만. UI 아이콘·태그 매칭은 쓰지 않는다. 말풍선에는 안 붙임 | `fxlib.icon_for`, `labels_lib.html_for` |
| svgo | 그림 SVG를 빌드 전에 정리(숫자 2자리, 편집기 찌꺼기 제거). 원본은 그대로, 사본 `build/art_opt/` | id·data-*·그룹·숨김 요소·기본 도형·빈 그룹·transform 보존(규칙이 읽는 것). `npx` 없으면 건너뜀(로그 `svgo: skipped`), `SVGO=0`으로 끔 | `tools/build/svg_opt.py` |

**쓰지 않는 것**

| 대상 | 이유 |
|---|---|
| ScrollTrigger·ScrollSmoother·ScrollTo·Observer·Draggable | 스크롤·마우스용 |
| Pixi·Easel | 다른 렌더러 |
| CSSRule, GSDevTools·MotionPathHelper | 개발 도구 |
| anime.js의 svg 도구(createDrawable·morphTo·createMotionPath) | GSAP 플러그인과 겹침 |
| three.js·lottie·rive·remotion·theatre·penpot | 쓰지 않기로 판정 |

- 에이전트용 요약은 `tools/art_spec.md` 7.
- 확인: 합성 페이지에서 새 모션 6종·배경 2종·텍스트 5종 동작(JS 오류 0), whale-fall-short1 전체 빌드 seek JS 오류 0. 미확인: 네 영상 전체 재빌드의 화면.

### 4-7. 붙임 규칙과 점검

**규칙 (그림 에이전트와 메인 모두): 움직이는 부분은 몸에 붙어 있어야 한다.**
1. `mv-joint`/`mv-chain`/`mv-swing`/`mv-rotor`/`mv-pendulum`의 `data-pivot`은 **그 부분이 몸·받침에 닿는 점**이다. 부분 위에 있고(≤12 px) 몸(또는 부모 마디)에도 닿아야 한다. 허공 중심이면 안 된다. 힌지 핀(작은 원)이 그룹 안에 있으면 그 핀이 받침이다. 화면 가장자리에 매달린 것(천장 램프)은 가장자리가 받침이다.
2. **그물·깃발·막대에 붙은 것**: 피벗을 막대 끝과 테두리가 만나는 점에 둔다(그물 주머니만 흔들고 막대는 가만히 있으면 떨어져 보인다).
3. **둥근 면 위의 회전**(시계 바늘·바퀴): 피벗 = 그 둥근 면의 중심.
   - 톱니바퀴: 피벗 = 톱니 중심. 이웃 톱니는 이가 맞물리고(중심 거리 = 두 피치 반지름의 합) 반대 방향, 주기는 톱니 수에 반비례. 껍질·창 같은 원 안에 들어가야 한다.
   - 도구: `python3 tools/fix/gearmesh.py <svg> <톱니A id> <톱니B id> <각도>`(두 톱니를 맞물리게 다시 그림).
4. **몸이 이동하면 꼬리·다리·목도 그 이동 그룹 안**에 넣는다(`tools/fix/joinpart.py`). 꼬리 사슬(`mv-chain-*-1` → `-2`)은 부모 마디 안에 중첩.
5. **새 목+머리**는 한 사슬: 머리를 목 그룹 안에 넣어 함께 움직인다.
6. **서 있는 것(나무·갈대·풀·팻말·기둥·탑)**
   - 그룹에는 그것 자체만(팻말은 기둥 + 판 전부, 그림자·물·땅은 밖).
   - 한 그룹에 떨어진 덩이가 둘 이상이면 덩이마다 그룹으로 나눈다(`tools/fix/splitclumps.py`).
   - 축은 줄기·기둥의 **발**이다. `tools/fix/setbase.py <slug>`가 `data-pivot`을 써 준다(코어 `mv-core-sway-*`도 `data-pivot`을 따른다).
7. 이름표·말풍선의 `to`는 움직이는 오브젝트 **안**에 찍는다(옆 45 px 이내면 점검이 걸리고 `attachcheck.py --fix`가 안으로 옮긴다).
8. 흔들리는 기둥에 달린 부품은 같은 그룹 안에 둔다(4-14 2번).

**코드가 보장하는 것**
- `data-pivot`을 쓰는 트윈(`svgOrigin:miyaPv`)과 퍼센트 축 트윈은 이름표 따라가기 측정이 끝난 **뒤에** 만들어진다(`build3.py`, 로그 `hinge tweens added after the follow measuring`). 숨겨진 그림에서 축이 빈 bbox 모서리로 굳지 않게 하기 위해서다.
- 모든 `svgOrigin`에 `smoothOrigin:false`.
- 이름표 따라가기는 그림이 시작할 때(오브젝트가 그려진 자리)를 기준으로 옮김을 잰다.

**점검 도구**

| 도구 | 무엇 | 누가 언제 |
|---|---|---|
| `tools/check/attachcheck.py <slug> [uid..]`(`--fix`) | 그림 SVG 정적 점검: 위 1~7, 카탈로그 불일치(4-8) | 그림 에이전트가 그림을 낼 때마다(보고 전 필수), `build3`이 끝날 때 자동 |
| `tools/preview/motionaudit.py <dir> <uid..>` | 만든 페이지를 3시각에서 찍어 피벗마다 빨간 점을 그린 띠 이미지 | 에이전트가 사람·동물·기계 그림을 눈으로 확인(점이 몸 위인지) |
| `tools/check/pivotlive.py` | 만든 페이지에서 힌지의 실제 회전 중심을 재서, 피벗이 10 px 이상 끌려가면 실패 | 메인 최종 점검 |
| `tools/check/originlive.py` | 만든 페이지에서 data-pivot 없는 회전 그룹(spin·turn·roll·wobble)이 자기 중심에서 10 px 넘게 끌려가면 실패 | 메인 최종 점검 |
| `tools/check/partaxis.py <slug> [--fix]` | 팔·턱·꼬리·더듬이·날개가 몸 쪽 끝에 축이 있는지(휴리스틱, 참고) + `mv-wiggle` 값(4-12) | 그림이 끝나고, `final_check`가 자동 |
| `tools/fix/splitlimbs.py <slug> [--dry\|--check]` | 한 그룹에 여러 가닥이 묶여 한 축을 쓰면 가닥마다 개별 힌지로 나눔(4-12) | 그림이 끝나고, `final_check`가 `--check`로 자동 |
| `tools/check/final_check.py` | 위 점검 + 그림 누락·다양성·금지 ease·등장 숨김(15-8). 통과하면 `render/<slug>/.checked`(index.html sha1) | **메인이 렌더 푸시 직전 반드시.** `chunk_plan.py`는 `.checked`가 없거나 낡으면 렌더 사양을 내놓지 않는다 |

보조: `tools/preview/grpinfo.py <slug> <uid..>`(mv 그룹 상자·피벗·부모 목록), `tools/fix/setbase.py`, `tools/fix/splitclumps.py`, `tools/fix/joinpart.py`, `tools/fix/gearmesh.py`.

### 4-8. 축 카탈로그
**원칙**: 축은 에이전트가 생각해서 찍는 값이 아니라 **그 물건의 이름이 정하는 값**이다.
- `tools/axis_lib.py`의 카탈로그가 물건 이름 약 380개를 7가지 축 규칙에 묶어 둔다. 사람이 읽는 표는 `tools/axis_catalog.md`(`python3 tools/axis_lib.py --doc`로 생성).
- 에이전트는 그룹 이름에 물건을 적기만 한다(`mv-<종류>-<물건>`, 머리 명사를 마지막에: `net-bag`, `bird-neck`, `windmill-blades`, `gear-1`). 축 좌표는 코드가 그림에서 잰다.

| 축 규칙 | 뜻 | 물건(예) | 맞는 종류 | 틀린 종류 |
|---|---|---|---|---|
| **base** 발(밑동) | 바닥에 닿는 가는 모양의 x 중심, y = 그룹 바닥 | 나무·풀·갈대·팻말·기둥·탑·촛불·병·사람·동물(몸통) | sway tilt topple core-sway | spin wobble roll orbit |
| **top** 매단 점 | 꼭대기에 닿는 가는 모양(끈)의 x 중심, y = 그룹 꼭대기 | 랜턴·종·추·밧줄·덩굴·고드름·자루·주머니·꼭두각시 | swing pendulum sway | spin roll topple |
| **contact** 몸에 닿는 점 | 부분과 몸이 겹치는 영역 중 자유 끝에서 가장 먼 1/4의 중심. 그룹 안 힌지 핀이 있으면 그 핀 | 꼬리·다리·팔·목·날개·턱·지느러미·문·뚜껑·손에 든 도구 | joint chain swing flap | sway spin rotor topple |
| **round** 둥근 면 중심 | 그룹 자신의 원(허브). 정사각형에 가까운 그룹은 상자 중심. 길쭉한 바늘은 한 끝에 닿는 둥근 면(문자판)의 중심 | 바퀴·톱니·팬·프로펠러·풍차 날개·시곗바늘·다이얼 | rotor spin turn | sway topple wobble |
| **edge** 깃대 쪽 가장자리 | 옆에 닿는 길고 가는 몸 모양(깃대) 쪽 변의 중점 | 깃발·페넌트·돛·바람자루 | flagwave swing sway | spin rotor topple |
| **center** 중심 | 그룹 상자 중심(받침 핀을 따로 그렸으면 `data-pivot`으로 그 핀) | 시소·저울·배·풍선·행성·공·상자·수레·떼·올챙이·벌레 | tilt bob float spin wiggle … | (물건마다 다름) |
| **none** 축 없음 | 회전 금지 | 물·파도·비·연기·안개·불·빛·그림자·땅·하늘 | ripple flicker drift fade | joint rotor sway swing spin topple |

**도구와 순서**
1. **그림 에이전트**: 이름을 붙여 그리고 `python3 tools/fix/axisfix.py <slug> <uid..>`(빠진 `data-pivot`을 카탈로그 축으로 써 줌) → `python3 tools/check/attachcheck.py <slug> <uid..>`가 0이어야 보고한다.
   - attachcheck의 카탈로그 줄(`catalogue …`): 물건에 안 맞는 종류(물을 sway, 나무를 spin), 축 없는 것의 회전, 빠진 피벗, 발·매단 점·허브·깃대 변에서 12 px(매단 점은 32 px) 넘게 벗어난 피벗.
2. **메인**: `build3.py`가 시작할 때 `axisfix`를 자동으로 돌리고(로그 `axisfix:`), 끝에 attachcheck, 렌더 푸시 전 `final_check.py`(15-8)가 같은 점검을 다시 한다. 문제가 하나라도 있으면 `.checked`가 안 나온다. 해당 그림을 에이전트에게 돌려보내 고치고 다시 빌드·점검한다.
3. **에이전트가 찍은 피벗이 카탈로그와 다를 때**
   - 발·매단 점·허브·깃대 변은 카탈로그가 맞다(`axisfix.py --force`로 덮어씀).
   - contact(팔다리·꼬리·목)와 center는 거리로 걸지 않는다. 빠졌을 때만 써 주고, 맞는지는 attachcheck(부분 위 + 몸 위)와 motionaudit 띠 이미지로 본다.
   - 생물·기계 이름의 joint/chain은 부분으로 본다(`mv-chain-ant-1`, `mv-joint-valve`).
4. 전체 점검 순서는 4-12 5번.

- 확인: 합성 그림 13종에서 기대 축과 일치, 기존 영상 30편(약 1,000장) 리포트 모드에서 물건에 안 맞는 종류 0. 미확인: Actions 렌더.

### 4-9. 기울어진 은하·천칭
1. **비스듬히 그린 은하 원반**(축 비율 < 0.88)은 그림 전체 회전이 아니라 원반면 안에서 자전한다. `tools/fix/galaxyfix.py`가 `mv-disc-galaxy`(`data-tilt/ratio/cx/cy/per/dir`)로 바꾸고 build3가 자동 실행한다. 정면 은하(비율 ≥ 0.88)는 `mv-core-spin`.
2. **천칭**은 4-11 2번. 이미 기울여 그린 천칭은 통째 sway 금지(`heartbeat` 등으로).
3. 점검은 대본 시각만이 아니라 전 영상(롱폼·숏츠) 전체에 한다.

### 4-10. 오브젝트 모션 다양성과 테마 팩 그림 규칙
오브젝트 모션 종류는 그림 에이전트가 문장으로 고른다(4-1). 문장이 서로 비슷한 주제(우주: 크기·거리·팽창·시간)에서 같은 그림이 반복되지 않게 아래를 지킨다.
1. **테마 팩 그림 규칙(`tools/concepts_catalog.md`, `tools/concepts.PACK_PICTURE`)**: 영역(space·sea·history·body·bio·time·earth·tech·generic)마다 작은 소품 9~11개(이름 + `mv-` 종류), 권장 모션 종류, 구도 5~6종. 그림 에이전트는 영상의 팩에서 구도 4종 이상·모션 5종 이상을 쓰고 같은 구도를 연달아 두지 않는다(art_spec 7B).
2. **움직이는 소품 할당량**: 4~6장마다 1장은 주인공 옆에 이름 붙인 작은 소품이 움직인다.
   - 세는 종류: `core-drop`·`topple`·`rollby`·`bouncing`·`swing`·`pendulum`·`rise`·`popin`·`drip`·`toss`·`coast`·`unroll`·`magnet`·`hop`·`nudge`·`hatch`·`lift`·`teeter`·`scatter`·`converge`·`zigzag`.
   - 개구리 접촉 개그(7-2 I)는 이것 없이는 나오지 않는다.
   - 우주에서도 된다(떠가는 렌치가 coast, 운석이 rollby, 착륙선 다리가 joint, 줄이 swing, 깃발이 flagwave).
3. **개념 → 그림 제안**: 문장의 개념(7-2 K-1)이 그림을 바꾼다. 크기 비교는 익숙한 물건이 `popin`, 세기는 줄이 `regroup`, 숨김은 덮개가 `slide`로 걷힘, 속도는 `path` + `dash`. 주제가 늘 쓰는 한 그림(행성 자, 늘어나는 격자)은 영상에 두 번까지.
4. **검사**: `python3 tools/check/variety_check.py <slug> [--report]`가 그림의 `mv-` 종류 수(배경 종류 제외)와 소품 그림 수를 센다. 롱폼은 종류 ≥ 8이 아니면 `final_check.py`가 막고, 소품 수는 경고로 낸다. 그림 에이전트도 보고 전에 `--report`로 돈다. 전체 기준은 7-2 K-6.

### 4-11. 사람 팔 곡선·천칭 모션
1. **올린 팔**
   - 손목이 어깨보다 위(어깨–손목 거리의 0.2배 넘게)면 팔꿈치는 어깨–손목 선의 **아래쪽**에 있어야 한다(양팔을 올리면 ヽOﾉ). 개구리 팔(`frog_rig.arm_bend_pass`)과 같은 규칙.
   - `tools/body.py arm()`이 만들 때 굽음 방향을 맞춘다.
   - `tools/fix/armfix.py`가 이미 그려진 그림의 어긋난 팔을 고친다(한 덩어리 팔 = 선 기준 거울상, 두 마디 팔 = 아래팔만 윗팔 선 기준 거울상, 여러 번 돌려도 같은 결과).
   - `build3`가 시작할 때 자동 실행, `final_check`가 `armfix.py --check`로 막는다.
2. **천칭(저울)**
   - 막대만 막대 가운데(허브)를 축으로 기운다.
   - 접시·줄·담긴 물건은 막대 끝에 **매달려** 수평을 유지한 채 막대 끝을 따라 오르내린다(기울거나 옆으로 미끄러지지 않음). 걸이 줄·받침대는 움직이지 않는다.
   - 그리는 법: 막대는 가운데 허브가 있는 납작한 한 도형, 접시·줄은 막대 밖 별도 도형. 직접 묶을 때는 막대만 `mv-tilt-*` 그룹에서 기울고 끈·접시·올린 물건은 각각 `data-hang="x y"`(매단 점) 그룹으로 넣는다.
   - `tools/fix/scalefix.py`가 그림 직계 자식을 막대/왼쪽/오른쪽/고정으로 나눈다(`build3`가 `mv-swing|tilt|joint|core-*-…scale|balance|seesaw` 그룹에 자동 적용, `fxlib.miyaScaleP`). 막대를 못 읽는 그림은 원래 모션을 둔다.
   - 확인: `python3 tools/fix/scalefix.py [slug]`.

### 4-12. 가닥마다 개별 축·몸 쪽 끝 축·떨림 값
1. **여러 가닥은 가닥마다 그룹과 축.**
   - 촉수·다리·팔·더듬이·수염처럼 같은 종류가 여러 개면 한 `mv-joint-*` 그룹에 묶지 않는다. `mv-joint-<단수 이름>-<번호>` 그룹으로 하나씩 나눠 각자 **몸에 닿는 끝**에 `data-pivot`을 둔다(한 점에서 같이 돌리면 먼 가닥은 몸에서 떨어진다).
   - 위상은 가닥마다 엇갈리게(`data-phase`).
   - 이미 묶인 그림은 `python3 tools/fix/splitlimbs.py <slug> [uid..]`(뿌리 간격 > 25 px, transform 있는 그룹은 건너뜀).
   - 의도한 한 축(몸이 화면 밖인 다리 등)은 `data-keep="1"`.
2. **축은 몸 쪽 끝.** 턱·팔·다리·더듬이·날개·꼬리의 `data-pivot`은 몸에 붙은 쪽 끝이다(자유 끝·가운데 금지). attachcheck가 바닥·받침을 몸으로 보고 지나칠 수 있으니 `tools/check/partaxis.py`도 돌린다. 몸 쪽 끝 추정은 휴리스틱이라 날개·더듬이 뿌리가 오탐일 수 있다. 그때는 `motionaudit.py` 띠 이미지로 눈 확인.
3. **`mv-wiggle` 값.** `data-amp`는 **배율 비율**(기본 .06)이지 픽셀이 아니다(5를 쓰면 5배 늘었다 줄어든다). `data-per`는 한 번 오가는 초(기본 .35는 매우 빠름, 해파리·촉수는 1 안팎). `partaxis.py`가 amp > .3 또는 per < .6을 막고 `--fix`가 .06 / 1로 고친다.
4. **생물 행(물고기·새·박쥐)**은 진행 방향으로 헤엄친다(`motions.fx_js`: 생물 행은 로컬 +x). 왼쪽으로 가는 물고기가 거꾸로 헤엄치는 옛 영상은 다시 빌드하면 고쳐진다.
5. **점검 순서(그림 에이전트·메인).** `axisfix` → `splitlimbs` → `partaxis` → `attachcheck`(그림을 낼 때마다) → 메인 `build3` → `final_check` → 사용자가 짚은 장면은 `motionaudit` 띠 이미지.
6. **회전체(풍속계·바람개비·프로펠러·날개·터빈·컵)의 축은 날/십자의 중심.** 둥근 면이 없는 십자·날개 묶음의 `mv-rotor` `data-pivot`이 묶음 중심에서 `max(12px, 크기의 8%)` 넘게 벗어나면 `attachcheck`가 막는다. 돌리는 그림은 '그림 평면에서 중심축 회전'이 기본이고, 수평면(위에서 본 원) 회전은 사용자가 말할 때만.
7. **카메라 흔들림(RoughEase)은 문장 단어 규칙이다.** `fxlib.ROUGH_W`가 맞는 문장의 드리프트 카메라만 흔든다. 새 단어를 넣을 때는 `\b`로 단어 전체만 맞는지 확인한다(다른 단어의 일부에 걸리면 줌인이 뚝뚝 끊긴다). 사용자가 끊김을 말하면 `plan`의 단위 문장에 `ROUGH_W`가 맞는지 먼저 본다.
8. **'정지 뒤 튐' 효과는 시작 자세를 바꿔 두지 않는다.** `wobble` 코어는 맞기 전까지 제자리에 있다가 톡 치고 복귀한다(4-1 표). 비슷한 효과를 새로 만들 때도 같다.
9. **다리 이름의 앞·뒤 접두어도 점검한다.** `partaxis.py`가 `fore|hind|front|rear|back` + 부위 이름도 검사한다. 앞다리·팔 축은 어깨(몸에 붙은 끝), 뒷다리 축은 엉덩이다.

### 4-13. 센터 모션 단어 규칙·상한, 오브젝트 모션 10종·배경 효과 6종
1. **센터 모션의 '사건' 종류는 이유가 있을 때만.** `mv-core-`의 heartbeat·swell·tremble·ping·wobble·squeeze·pop·stamp·drop은 단위 문장에 그 단어가 있거나 그룹 이름이 그 물건일 때만 남는다.

   | 종류 | 문장 단어(`motions.CORE_WORDS`) |
   |---|---|
   | heartbeat | heart·pulse·beat·throb·alive… |
   | swell | grow·expand·inflate·balloon·breath… |
   | tremble | shake·quake·fear·vibrate… |
   | ping | signal·radar·echo·beacon… |
   | wobble | wobble·unsteady·teeter·dizzy… |
   | squeeze | squeeze·crush·press·shrink… |
   | pop | pop·appear·sudden·emerge… |
   | stamp | stamp·slam·seal·hit·strike… |
   | drop | fall·drop·land·plummet… |

   - 그룹 이름(`CORE_NAMES`): heart·pulsar·drum / sun·star·balloon·lung·bubble / radar·dish·antenna·satellite… / volcano·bomb·engine·reactor / top·jelly·tower·stack·plate·vase·egg·boat 등.
   - **상한**: 영상당 종류별 15 %(최소 3장). 넘으면 그 뒤부터는 고요 종류(glide·sway·approach·orbit, 빛 이름(lamp·star·sun·candle·screen·light·fire·neon…)이면 flicker)로 바뀐다. 고요 종류도 최소 사용으로 고른다(동률이면 순서).
   - **대체 종류는 축 카탈로그(4-8)에 맞춘다(`motions.core_fit`)**: 그 물건의 카탈로그 행에서 금지된 종류는 빼고(구·행성·세포는 `core-sway` 금지 → orbit), 허용 목록에 있는 종류를 먼저 쓴다(나무·기둥은 sway).
   - `data-keep="1"`만 예외.
   - `tools/fix/corefix.py <slug> [--report]`가 그림의 id를 직접 고쳐 쓴다. `build3.py`·`frog_place.py`가 시작할 때 자동 실행(로그 `corefix: N centre motions changed, M strong heartbeats`).
2. **heartbeat는 기본이 느린 맥박.** 1.6초 주기의 작은 두 박(1.07→1→1.04→1). 문장에 pounding·racing·panic·thump·frantic 같은 `HEART_STRONG` 단어가 있을 때만 `data-strong="1"`로 빠르고 큰 박동(0.9초).
3. **개구리는 맥동 오브젝트를 타지 않는다**(7-2 L).
4. **오브젝트 모션 10종** (`motions.obj_js`, 축은 종류별 고정, 전부 유한 fromTo, CustomEase 없음)

   | 종류 | 뜻 | data-* (기본) | 축 |
   |---|---|---|---|
   | `teeter` | 밀린 화병·기둥이 발을 축으로 흔들리다 멈춤 | `deg` 9, `dur` 2.4, `delay` .3 | 발(바닥 중앙) |
   | `jiggle` | 젤리·푸딩·배·해파리 갓이 출렁 | `amp` .06, `per` .32, `dur` 1.6, `every` 0(반복 간격) | 발 |
   | `peek` | 뒤에 숨은 것이 옆으로 나와 보고 들어감 | `dx` -120, `dy` 0, `hold` 1.2 | 이동 |
   | `spiral` | 배수구·소용돌이·블랙홀로 나선을 그리며 빨려듦(작아짐) | `cx`/`cy`(그림 px, 기본 화면 중앙), `turns` 2, `dur` 3, `end` .15 | 자기 중심 |
   | `zigzag` | 잎·번개길·나방·가라앉는 동전의 지그재그 | `dx` 90, `dy` 320, `n` 4, `dur` 2.4 | 이동 |
   | `lift` | 크레인 짐·열기구·공중부양: 들려 올라가 떠 있음 | `dy` -160, `dur` 1.2 | 이동 |
   | `scatter` | 그룹의 직계 자식들이 중심에서 바깥으로 흩어짐(놀란 새 떼, 뿌린 씨) | `dist` 260, `dur` .9 | 자식마다 |
   | `converge` | 바깥에서 그린 자리로 모임(모여든 군중, 맞춰지는 조각) | `dist` 260, `dur` .9 | 자식마다 |
   | `nudge` | 한 번 툭 밀려 그 자리에 머묾(pushed·shoved·moved an inch) | `dx` 60, `dy` 0 | 이동 |
   | `hatch` | 알·싹·팝업처럼 단계로 나옴(0→1.12→.96→1) | `dur` .8 | 발 |

   - `nudge`·`hatch`·`scatter`·`converge`는 멈춘 뒤 숨쉬기(`settle_js`)가 붙고, `frog_rig.obj_span`이 시각을 알아 개구리 접촉 동작과 맞출 수 있다.
5. **배경 효과 6종** (`motions.PARTICLES`/`OVERLAYS`, 단어 규칙 `FX_WORDS`)

   | 효과 | 모습 | 단어 |
   |---|---|---|
   | `ink` | 잉크 방울이 가라앉으며 옅어짐 | ink·squid·octopus·quill·calligraphy |
   | `paperbits` | 찢긴 종이가 팔랑 | paper·parchment·manuscript·document·archive·shredded |
   | `bokeh` | 초점 나간 큰 불빛(밤 전용) | city lights·streetlight·headlights·neon·downtown·skyline |
   | `crystals` | 얼음·광물 결정이 떠다님 | crystal·diamond·gem·quartz·mineral·icicle |
   | `eclipse` | 위쪽 밝은 원을 어두운 원이 가로지름 | eclipse·blot out the sun·transit of |
   | `horizonglow` | 지평선 띠가 숨 쉼 | horizon·sunset·afterglow·distant lights·dusk |

   - 앰비언트: ice에 crystals, history에 paperbits, sunset에 horizonglow.
6. **검사.** `variety_check.py`의 '센터 모션 비율' 줄(사건 종류별 ≤ 15 %, 넘으면 `corefix.py` 안내)과 '맥동 오브젝트 탑승' 줄(0이어야 통과)(15-8, 7-2 K-6).
7. 확인: 합성 59장면 JS 오류 0, whale-fall 숏츠 전체 빌드 0 오류, kardashev-scale 135장 corefix 뒤 맥동 탑승 0. 미확인: Actions 렌더 MP4.

### 4-14. 빠른 두근거림 금지·붙은 부품·등장 모션
1. **모르는 `mv-` 이름은 차분하게**: build3 `MV` 표에 없는 이름의 기본값은 느린 glow. `drift`는 6초 느린 표류, `mv-drift-nebula*`는 성운 모션. 빠른 박동은 `flame`·`spark` 이름이나 문장 단어가 있을 때만 쓴다. `tools/check/variety_check.py`의 `fast throb tweens`(전체 장면의 10 % 이하)가 막는다.
2. **붙은 부품은 같은 그룹 안에**: 흔들리는 가로등 기둥·팻말·깃대 끝에 달린 램프·등·표지는 그 `mv-sway-*`/`mv-swing-*` 그룹의 자식으로 넣는다(따로 두면 기둥만 흔들린다).
3. **나타나는 모션은 시작 전에 없어야 한다**: `converge`는 시작 전 흩어진 자리·투명 상태로 숨겨 두었다가 모션과 함께 모인다(`miyaScatter`가 time 0에 상태를 둠). 4-15.
4. **이름표·말풍선이 가리키는 곳이 움직이는 물체가 지나갈 자리면**: `to` 점이 그림 속 시작 상자에 없어도, 이름표 글자와 이어지는 이름(`racing-star` ↔ "outer stars")의 이동 그룹을 따라가게 build3가 짝짓는다(로그 `labels follow moving objects`).

### 4-15. 완성 배치를 먼저 보여주지 않는다
1. 시작 전에 숨겨야 하는 모션(`converge`·`draw`·`drip`·`unfold`·`unroll`·`popin`·`hatch` 등)은 `tl.fromTo(..., immediateRender:false)`만 쓰면 시작 시각까지 완성 상태가 보인다. 반드시 **같은 속성을 숨긴 `tl.set(대상, {숨김}, v0)`를 먼저** 둔다.

   | 종류 | 숨김 상태 |
   |---|---|
   | `converge` | 흩어진 자리·투명 |
   | `draw` | `drawSVG:"0%"` + `fillOpacity:0` |
   | `drip` | `opacity:0` |

2. `tools/check/entrycheck.py <slug>`가 빌드된 `render/<slug>/index.html`에서 `.mv-` 그룹의 숨김 시작 `fromTo`에 앞선 `tl.set`이 없으면 막는다(`final_check.py`가 호출). 새 모션 종류를 만들 때도 같은 규칙.
3. 옛 영상은 `build3.py`를 다시 돌려야 고쳐진다.

---

### 개정 이력
- 2026-10-09 (사용자): 장면 나누기와 전환(4-3).
- 2026-10-13 (사용자): 가운데 물체 모션 19종. 2026-10-14: 점 격자/모자이크 전환 삭제. 2026-10-16: 색 막대(`blinds`) 폐지.
- 2026-10-19 (사용자): 움직이는 부분이 있는 물체는 전체 회전 금지(풍차 날개 대신 탑 전체가 돌던 문제).
- 2026-10-22 (사용자): 객체 모션·카메라 트래킹·새 전환 5종(시계방향 부채꼴은 별로라고 해 뺌), 장면은 대본에서 정함, 이동 모션 일정 속도(`power2.inOut`은 방향 전환 때 빨라 보임), 컷 길이 ×1.5.
- 2026-10-24 (승인): 객체 모션 4종(`slide`·`fade`·`ticks`·`rack`), 카메라 확장. 로그 줌 다이브·끊기는 스크롤은 불채택.
- 2026-10-26 3차 (miya): 칠판 생기·멈춤 뒤 숨쉬기·유성·눈 깜빡임(4편을 `motion_check`로 돌리니 5초 이상 멈춘 구간이 전부 칠판 행 사이 공백이었음).
- 2026-10-26 4차 (miya): 축 자동 교정(나무가 꼭대기 축으로 흔들리던 문제), 오브젝트 모션 56종, 배경 효과, 텍스트 효과.
- 2026-10-27 (miya): '연속 금지' 고정 규칙 제거(전환 단어 일치 시 50% 확률 → 항상). 방향 규칙 4-4 A(고래 영상 물고기 역주행, "바람·빨림도 방향성")와 B("자동 아닌 것도 규격화"). 배경·텍스트 효과에 그림 증거.
- 2026-10-28: three/lottie/rive/remotion/theatre/penpot 쓰지 않기로 판정.
- 2026-10-29 (miya): 오픈소스 라이브러리 통합(4-6, 오브젝트 62종). lucide 태그 매칭은 오매칭(hole→drill)으로 뺌. 붙임 규칙·점검(4-7)과 원인 수정(2026-10-27 이후 영상에서 힌지 축이 빈 bbox 모서리로 굳어 풍차·톱니·다리·꼬리가 엉뚱한 점으로 돌았음, 숏츠3 블랙홀이 화면을 돌아다님). 축 카탈로그(4-8, 30편 점검에서 진짜 문제 1건: parasite-monster-frogs U006 그물 주머니). `pulsevig`·`gridripple` 삭제.
- 2026-10-30 (miya): 기울어진 은하·천칭(4-9). CustomWiggle 금지(15-8).
- 2026-10-31 (miya: "우주 영상은 항상 비슷한 것만 나온다"): 4-10.
- 2026-11-01 (miya: "팔꿈치가 위로 꺾여 기괴하다 / 천칭에서 저울이 분리돼 움직인다"): 4-11.
- 2026-11-02 (miya, 해파리·오징어·아귀 축, 배경 물고기 역주행): 4-12. 생물 행 방향 코드 버그 수정.
- 2026-11-03: 풍속계 축(40px 어긋남) → 4-12 6번. `ROUGH_W`가 engineers에 걸려 줌인이 끊김 → 7번.
- 2026-11-04 (miya): `wobble`이 컷 시작부터 30°·1.3배로 얼어 있던 것 수정(8번), 앞다리 접두어 점검(9번).
- 2026-11-05 (miya: "두근거리는 모션이 너무 자주 … 모션 더 많이 추가"): 4-13(오브젝트 73종, 배경 63종). 같은 날 검토로 대체 종류의 카탈로그 적합 조건(space-nuke-short1 U021이 렌더를 막음). 4-14(dark-matter-96-percent 검수 4건: 모르는 이름이 0.5초 박동으로 떨어짐 등), 4-15(완성 배치가 먼저 보이던 converge·draw·drip).
- 2026-11-14 (miya): 문서 유지 규칙 형식으로 정리(현재 규칙만, 이력은 여기). 4-1을 소제목으로 나누고 '3차·4차 보강'을 내용별 자리로 옮김. 4-6 CustomWiggle 행을 15-8에 맞춤.
