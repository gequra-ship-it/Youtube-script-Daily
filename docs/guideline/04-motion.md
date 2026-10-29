## 4. 모션 규칙 (일러스트 장면)

### 4-1. 움직임 방식
- **카메라**: 모든 그림에 드리프트 카메라(20-1). 포커스 대상이 있는 컷은 사이드카 `focus [x, y, 배율]`(배율 1.5~2.2)과 `focus_word`(컷 대본에 있는 단어)를 두고, 그 단어를 말하기 **0.5초 전**에 1.4초 동안 가속·감속으로 확대한 뒤 컷 끝까지 정지. 한 컷에서 여러 번 움직이지 않는다. 가장자리 밖이 보이지 않게 확대 중심을 제한.
- **포커스 스포트라이트**: 확대 1.4초 동안 주변이 어두워짐(가운데 투명, 바깥 검정 50%, 원 반지름은 배율에 맞춰 화면 폭의 30%~62%). 라벨·말풍선은 그 위. 사이드카 `"spot": false`로 끔.
- 그림 전체 부유(±12px)·먼지 입자는 쓰지 않는다. 빠른 휩팬·흔들림·회전 금지. 움직임은 작고 자연스럽게.
- **이동 모션 속도 (2026-10-22 사용자: 방향 전환 때 빨라 보임)**: `mv-path`·트래킹 카메라는 구간 15%만 부드럽게 출발·정지하고 나머지는 일정한 속도(`miyaCruise`, 예전 `power2.inOut`은 중간에 2배로 빨라졌음). 경로는 급꺾임 없이 접선이 이어지는 곡선으로 그린다.
- **인물·사물 동작 (필수)**: 인물 그림에 `mv-` 그룹 장면당 3~6개, 앞쪽 인물마다 최소 하나. 생물의 관절 모션은 20-6.
  - `mv-breathe-*` 몸통 세로 1.00→1.03, 2.2초(모든 인물) · `mv-nod-*` 머리 ±3°, 1.8초(축 목) · `mv-lean-*` ±2°, 3초 · `mv-arm-*` ±7°, 1.4초(축 어깨: `tools/pivots.py`가 팔 첫 선의 몸 쪽 끝을 자동 계산) · `mv-hand-*` 손 중심 ±5°, 1.0초(들어올림 없음) · `mv-walk-*` 좌우 120px, 3.5초(양옆 60px 비울 때만)
  - `mv-flame-*` `mv-spark-*` 세로 맥동 0.25~0.30초 · `mv-smoke-*` `mv-steam-*` `mv-cells-*` `mv-key-*` 위로 떠오름 · `mv-glint-*` `mv-lamp-*` `mv-lantern-*` `mv-beacon-*` 제자리 맥동(크기 1→1.06, 투명도 .85→1, 1.2~1.5초)

  **가운데 물체 모션 19종 (사용자 결정 2026-10-13)** — `mv-core-<타입>`, 물체 성격으로 고른다.
  `spin` 회전 초당 36°(렌즈·시계·행성) · `sway` 위쪽 축 ±14°, 1.4초(램프·종·열쇠) · `orbit` ±34px·±26px, 2.4초·3.1초(위성·곤충) · `glide` 좌우 ±60px, 2.6초(배·구름) · `heartbeat` 1.14→1→1.09→1 후 쉼, 0.9초(심장·세포) · `flicker` 투명도 .35~1, 1초(촛불·별) · `swell` 1→1.2, 2.2초(숨·풍선) · `tremble` ±5px·±1.5°, 0.07초(긴장·균열) · `approach` 컷 내내 1→1.3(발견·접근) · `reveal` 투명도 .15→1·크기 .6→1, 0.7초 후 정지(처음 등장) · `squeeze` 가로 .55·세로 1.2, 1.1초(세포·물방울) · `wobble` 30°·1.3배, 0.2초 뒤 탄성 복귀, 2.2초(충격 뒤) · `roll` −110→+110px·−180→+180°(구르는 것) · `pop` 0.15초 뒤 .2→1, 0.6초 back.out(새 등장) · `ping` 고리 1.3초마다 .85→1.8, 불투명도 .95→0(신호·경보) · `stamp` 1.8배·투명에서 쾅 0.28초+고리(결정·도장) · `flip` 가로 뒤집기 0.46초, 2.4초마다(동전·반전) · `draw` 윤곽 1.3초 후 채움(설계도·새 개념) · `drop` −18° 기운 채 떨어져 튐, 0.9초 bounce.out(떨어지는 것·결과)
  - **배분**: 앞뒤 같은 타입 금지, 한 영상 10종 이상, 한 종류 20% 이하, 위아래로만 움직이는 모션 금지. 위반 시 빌드 `WARNING`(멈추지 않음). `mv-glint-core`만 있으면 `tools/motions.py`의 `legacy_core_type`이 자동 배정하지만 에이전트가 직접 고르는 쪽이 낫다.
  - 렌더 페이지가 열릴 때 `miyaWrapCores`가 코어 그룹(글로우)과 그리기 순서상 이웃한 도형 중 가운데 원판(반지름 170px 안, 크기 460px 이하)에 놓인 것을 `<g>`로 묶어 모션을 건다. `ping`·`stamp` 고리는 어두운 테두리 12px + 노랑 `#ffcf5a` 6px. `draw`는 선 있는 도형을 그린 뒤 나머지를 페이드인.
  - **움직이는 부분이 있는 물체 (사용자 결정 2026-10-19, 풍차 날개 대신 탑 전체가 돌던 문제)**: 날개·바늘·시계 손·플라스마 고리처럼 **따로 움직여야 하는 부분이 있는 물체에는 물체 전체를 돌리거나 뒤집거나 흔드는 코어 모션(`spin`·`roll`·`flip`·`wobble`·`tremble`·`orbit`·`sway`)을 쓰지 않는다.** `miyaWrapCores`가 이웃 도형(탑·시계 판·받침)까지 한 덩어리로 묶기 때문이다. 대신 ① 움직이는 부분만 따로 그룹으로 그리고 — 계속 도는 것은 `mv-rotor-<이름>`(`data-pivot="x y"`, `data-per`=한 바퀴 초, `data-dir`=1/-1: 시계 분침 14초·시침 70초, 초침 6초, 플라스마 고리 9초), 왔다 갔다 하는 것은 `mv-joint-<이름>`(계기판·나침반 바늘, 진폭 3~22°) — ② 코어 모션은 `swell`·`heartbeat`·`approach` 같은 부드러운 것으로 하거나, 코어 그룹 자체가 돌 부분이면(풍차 날개+허브) `mv-core-turn`(그 그룹만 초당 90°, 이웃을 묶지 않음)을 쓴다. 날개 그룹 안에는 날개·허브·글로우만 두고 탑·몸통은 그룹 밖에 둔다. 에이전트 지시서에도 넣는다(`tools/art_spec.md` 7장).
  **객체 모션 21종 (사용자 결정 2026-10-22·10-24, 위치 제한 없음)** — 그림의 `mv-<종류>-<이름>` 그룹과 `data-*` 속성. 구현 `tools/motions.py`의 `obj_js`(시험 페이지에서 seek 확인, 실제 MP4는 아직 안 봄). 모두 유한 트윈이고 `data-delay`(그림 시작 후 초, 기본 0.3), `data-dur`(기본 1.0)을 받는다.
  - `mv-path-*` `data-path="M.. C.."` 경로를 따라 이동하고 진행 방향으로 돎(`data-rot="0"`이면 안 돎, 종이비행기·우주선, 기본 길이는 그림 길이−0.6초 최대 3.4초) · `mv-flip-*` `data-pivot` 둘레로 `data-deg`(180)° 뒤집기(모래시계) · `mv-fill-*` `data-from`→`data-to`(0→1) `data-axis`(y 또는 x) 크기 변화(모래 줄어듦·쌓임, 막대, 게이지; `mv-grow-*`는 0에서 시작) · `mv-swing-*` 감쇠 진자 `data-amp`(28°)·`data-per`(2.4초) · `mv-topple-*` `data-deg`(72)° 쓰러짐(도미노, 0.55초; 그룹마다 `data-delay`를 0.2초씩 늘려 연쇄) · `mv-liquid-*` `data-rise`(px) 올라오며 `data-scroll`(px) 옆으로 흐름(비커 액체: 물결 윗면의 넓은 도형을 용기 clipPath로 자른다) · `mv-bubble-*` `data-rise` 올라가며 사라짐, `data-per`(1.6초) 반복 · `mv-edge-*` 그룹 안의 선이 그려짐(네트워크 연결선) · `mv-keyturn-*` 옆에서 본 열쇠 손잡이가 축 둘레로 돎(세로 1→`data-to` .32) · `mv-shackle-*` 걸쇠가 `data-lift`(46)px 올라가며 `data-deg`(−16)° 열림 · `mv-popin-*` 제자리에서 튀어나옴(노드)
  - 추가 5종(2026-10-22): `mv-shake-*` 좌우 떨림 `data-amp`(3px)·`data-dur`(.25초)(자물쇠 찰칵·충돌) · `mv-dash-*` 점선이 선을 따라 흐름 `data-speed`(40px/초)(지나온 경로) · `mv-scroll-*` 그림 내내 옆으로 `data-dist`(160px) 흐름(별·구름 시차) · `mv-slam-*` 2.4배에서 쾅 들어옴(도장·제목) · `mv-rise-*` `data-from`(60px) 아래에서 떠오르며 나타남(태그·표지)
  - 추가 4종(2026-10-24, 곰 1분 시험 영상 v3에서 사용자 승인): `mv-slide-*` 패널·막대가 `data-dx`/`data-dy`(기본 −960/0)만큼 미끄러져 들어옴, `data-dir="out"`이면 나감, 0.7초(분할 화면 두 패널, 지우개) · `mv-fade-*` 투명도 `data-from`(0)→`data-to`(1), `data-dur`(.4)(유령 잔상 .1→.6, 지움 1→0) · `mv-ticks-*` 그룹 안 자식을 `data-step`(.1초)마다 하나씩 켬(`data-fill`로 채움 표시, 칸 n개 = 수량) · `mv-rack-*` 초점 이동: 같은 그룹의 흐린 복제 6장이 `data-r`(14px)에서 선명해짐(`data-dir`="in")/흐려짐("out"), SVG 필터 없이 구현, 1.2초. `mv-popin-*`은 `data-axis="x|y"`로 한 방향만 튀어나옴.
  - **카메라 확장 (2026-10-24, 승인)**: 그림 한 장을 크게 그려(사이드카 `"world": [w, h]`, 예 [3840,1080] 가로 이동, [1920,2160] 세로 스크롤) 그 위를 `mv-track-*`로 지나간다. 지역 이동 = 가로 world + 경로, **세로 스크롤 = 세로 world + 경로 하나(일정 속도라 부드럽다; 끊기는 빠르게 감기·속도 램프는 사용자가 불채택)**, 밀어넣어 이어붙이기 = `data-scale`≥3 트래킹 뒤 `match`/`zoom` 전환, 분할 화면 = `slide` 패널 둘, 초점 이동 = `rack`. 트래킹 한계는 world 크기로 계산(`track_js`의 WW/WH). **불채택(쓰지 않음)**: 로그 줌 다이브, 끊기는 스크롤.
  - **화면 구성 블록 → 만드는 법(승인된 것만)**: 격자=수량 → `ticks`(fill) · 지층 → `grow`+`fade` · 틈 속 들여다보기 → `slide` 층 + `mv-track` scale≈1.8 · 숫자 쾅 → `num` 라벨 + `slam` · 자석 → `path` · 펜 두 개 → `edge` 그룹 둘(같은 `data-delay`) · 지우개 → `slide`(dir out)+`fade` 1→0 · 유령 → `fade` .1→.6 · 페이지 넘김·찢긴 종이 → 전환 `page`/`zigzag` · 극단적 크기 대비·예외(기울이거나 옮긴 하나) → 그림 구성. 정지 화면(프리즈)·속도 램프는 파이프라인에 구현하지 않음(시험 영상 전용).
  - **장면은 대본 내용에서 정한다 (사용자 결정 2026-10-22, 거듭 확인: 예시 목록이 아님)**: 위 21종·트래킹·말풍선은 **블록**이고, 어떤 그림에 무엇을 쓸지는 **그 단위의 대본이 말하는 내용에서 정한다.** 그림 에이전트는 단위마다 ① 대본이 말하는 사건·움직임·변화·관계가 무엇인지 문장으로 적고(예: "열쇠가 구멍에 들어가 돌아 문이 열린다", "모래가 아래로 떨어진다", "배가 항구를 떠나 수평선으로 간다") ② 그것을 가장 정확히 보여 주는 모션을 고른다 — 21종을 조합하거나(경로 이동+점선 궤적+카메라 트래킹, 뒤집기+채움+흔들림), 맞는 것이 없으면 새 모션 종류를 `tools/motions.py`의 `obj_js`에 더하고 `OBJ_KINDS`·이 절·`art_spec.md` 7장에 적는다. 예시(여정→경로 이동, 연쇄→도미노, 모래→뒤집기+채움 등)에 없는 내용도 똑같이 대본에서 출발해 정한다. 움직일 사건이 없는 단위(정적 설명, 인물 대화)는 억지로 넣지 않고 인물 모션·말풍선·카메라로 둔다. 같은 종류가 이웃 그림에 이어지지 않게 하고, 쓴 모션과 이유를 그림 사이드카·보고에 한 줄로 적는다.
  - **카메라 트래킹 (사용자 결정 2026-10-22, 모션과 같은 규칙: 예시가 아니라 대본이 말하는 장면에서 정한다)**: 대본이 길게 이어지는 움직임·여정·훑어봄을 말하는 단위(걸어가는 생물, 이동하는 무리, 시간선·먹이사슬·지층을 따라 훑기, 흐르는 강, 날아가는 것, 쓰러지는 연쇄 등)에서 카메라가 그것을 따라간다. 그림 에이전트가 단위마다 판단해 따라갈 경로를 정한다. 방법: 경로를 따라 도는 물체(`mv-path`)나 도미노 연쇄(`mv-topple` 3개 이상)가 있으면 자동으로 따라가고, 그 밖의 모든 장면은 카메라만 따라갈 빈 그룹 `mv-track-*`(`data-path` = 카메라 중심이 지나갈 경로, `data-delay`, `data-dur`, `data-scale`)으로 직접 정한다. 따라갈 움직임이 없는 단위에는 넣지 않는다. 처음 12%에 확대(기본 1.3배, 사이드카 `"track": {"scale": 1.4}`)되고 끝 12%에 원래 크기로 돌아온다. 트래킹이 있는 그림은 포커스 확대와 드리프트 카메라를 쓰지 않는다(`"track": false`로 끔). 구현 `tools/motions.py` `track_spec`·`miyaTrack`, 빌드 로그 `tracking cams`. 시험 페이지에서 확인했고 실제 MP4는 아직 보지 못했다.
  - 규칙: 열쇠는 **옆에서 구멍에 꽂고 먼저 돌린 뒤** 걸쇠가 열린다(위로만 열리는 것 금지, 돌리는 방향은 시계방향). 모래시계는 뒤집은 뒤 윗칸 모래가 줄고 아랫칸이 바닥부터 쌓인다(위에서부터 채우지 않는다). 모션 시작은 같은 그림 안에서 `data-delay`로 순서를 맞춘다(두 번 재생되는 것처럼 보이지 않게, 전환 중 시작한 모션은 컷이 시작해도 이어진다).
- **3차 보강 (2026-10-26, miya: 오브젝트 모션도 모델·대본이 달라도 같은 규격)** — 4편(whale-fall·eating-humans·edge-of-universe·stolen-time) 전체를 `tools/motion_check.py --step 5`로 돌린 결과, 5초 이상 멈춘 구간은 **전부 칠판 행 사이 공백**이었고(그림 단위는 2곳: 일회성 모션이 끝난 뒤 멈춘 u72·u112), 그래서 아래를 코드 규칙으로 넣었다. 모두 단위의 시간·그룹 이름·단위 번호로만 정해지고 난수가 없다.
  - **칠판 생기** (`tools/motions.py` `chalk_life_js`, `build3.py` 칠판 JS): ① 아직 안 나온 행의 점선 빈칸이 숨 쉰다(투명도 .5↔1, 1.1초, 행이 뜨면 사라짐). ② 행 사이 공백이 7초를 넘으면 5초마다 마지막으로 뜬 행의 숫자가 한 번 커졌다 돌아오고(1.08배, 0.16초) 개구리 가리키는 팔이 그 행을 톡 친다(y −7px). 결론 줄도 같다.
  - **멈춤 뒤 숨쉬기** (`motions.settle_js`): `path`·`slide`(in)·`slam`·`popin`·`rise`·`topple`·`flip` 같은 일회성 모션이 끝나고 2.5초 넘게 남으면, 그 물체는 멈춘 순간부터 컷 끝까지 1→1.03 숨쉬기(2.6초 sine). 얼어붙은 물체 금지.
  - **유성** (`build3.py` `is_cosmic`): 밤 배경·space/deepfield 팔레트 그림 중 6초 넘고 단위 번호 `k % 3 == 1`인 단위에 한 번, 윗하늘을 가로지르는 유성(글로우 선+머리, 0.55초, 처음·끝 1.5초 제외; 위치·시각은 단위 번호의 황금비 분수로 고정).
  - **눈 깜빡임** `mv-blink-<이름>`: 눈(흰자+눈동자) 그룹에 붙이면 불규칙 간격(3.1 / 4.2 / 0.35 / 2.5초 순환)으로 0.07초 감았다 뜬다. 그림 에이전트가 생물·사람 눈을 따로 그룹으로 그릴 때만 생긴다(`tools/art_spec.md` 7장).
  - **개구리 두드림 파장**: 개구리 `tap` 동작 때 닿는 자리에 고리(`_tp`)가 퍼진다(7-2 D).
  - 그림 단위에서 모션이 전혀 없는 구간이 남으면 빌드 뒤 `python3 tools/motion_check.py render/<slug> --step 5`로 확인하고, 그 단위에 `frog_hint` 또는 `mv-` 그룹을 더한다(모델 판단이 아니라 이 점검표로).
- **4차 보강 (2026-10-26, miya: "오브젝트 모션 축 점검 + 오브젝트 모션·배경 효과·텍스트 효과 대량 추가")** — 전부 코드 규칙(`tools/motions.py`, `tools/labels_lib.py`, `tools/build3.py`), 난수·모델 판단 없음.
  - **축(피벗) 자동 교정** (`motions.pivot_of`·`core_sanitize`·`obj_sanitize`, build3가 "motion sanity (round 4)"로 출력): 그룹 이름의 꼬리말(`mv-core-sway-tree`의 `tree`)로 축을 정한다. 땅에 선 것(`BOTTOM_NAMES`: tree·pole·tower·person·house·flag…)은 **밑동 고정**(origin 50% 100%, ±5° 2.2초), 매달린 것(`HANG_NAMES`: lantern·bell·rope…)은 꼭대기 고정, 가운데가 축인 것(`CENTER_NAMES`: ship·scale·planet…)은 가운데(±6°). 둥근 것(`ROUND_NAMES`)이 아니면 spin/roll/flip/turn/circle은 wobble·glide·sway로, 무거운 것(`HEAVY_NAMES`: whale·ship…)의 drop은 swell로 바꾼다. 인간 영상의 나무가 꼭대기 축으로 흔들리던 문제(miya 2026-10-26)가 이 규칙으로 모든 대본에 자동 적용된다. 4편 전수 검사 결과: core-sway tree·sign 3곳, flip/roll/spin clock·key 4곳, drop whale 2곳, swing ship·pole·island·flag 축이 교정됐다. 작가가 일부러 그렇게 그린 경우만 그룹에 `data-keep="1"`.
  - **오브젝트 모션 62종** (`OBJ_KINDS`, 4차 추가 35종 + 2026-10-29 라이브러리 6종 `draw·morph·toss·skid·coast·regroup`(4-6), 종류마다 코드 주석에 축이 적혀 있다): bob·hover·pendulum(꼭대기)·wiggle·tilt(밑)·crumble·emph·spin·rollby·float·flap(가운데 세로축)·swim·hop(발)·drip(위)·unfold(위 모서리)·unroll(왼쪽 모서리)·flagwave(깃대 쪽)·ripple·sparkle·circle(`data-pivot` 궤도 중심 필수, 없으면 float)·squash(발)·neon·shiver·beat·settle·magnet·bouncing(발)·creep·sink·ascend·tick(가운데)·flicker·breathe·nodding(목)·sway(밑). `mv-<kind>-<이름>`으로 쓰고, 이름이 축과 안 맞으면 위 교정이 먼저 돈다. 56종을 합성 페이지에서 모두 틀었다(JS 오류 0, 트윈이 컷을 넘지 않음).
  - **배경 효과 59종** (`motions.FX_KINDS`, 2026-10-29 `burst`(Physics2D 폭발)·`gridripple`(anime.js 격자 물결) 추가, 4-6; `fx_for`가 그림마다 최대 하나): 입자 30종(snow·hail·bubbles·embers·sparks·ash·pollen·fireflies·leaves·petals·confetti·feathers·sand·meteors·twinkle·coins·notes·hearts·questions·plankton·seeds·spores·bats·birds·fish·jellies·germs·lanterns·balloons·droplets, 한 표 `PARTICLES`에 모양·색(종이/밤)·크기·방향·주기·흔들림·깜빡임) + 전면 효과 27종(rain·flash·bolt·fog·heat·rays·searchlight·vignette·pulsevig·tint·clouds·windlines·smoke·steam·shockwave·letterbox·scanlines·glitch·lightleak·flare·aurora·ripples·waves·rainbow·spotlight·frost·starburst). 고르는 순서: ① 단위 대본 단어 규칙 `FX_WORDS`(우선순위 표, 예 rain→rain, bacteria→germs, death→vignette) ② 없으면 팔레트별 잔잔한 효과 `FX_AMBIENT`를 짝수 단위마다 순환(ocean: bubbles·plankton·fish·ripples, forest: pollen·leaves·seeds·spores, space: twinkle·meteors…, body·lab은 단어가 있을 때만). 단어로 고른 효과는 다음 그림에 같은 단어가 또 있으면 또 나오고(상황이 이어짐), 채움용 앰비언트만 직전과 다른 것으로 돌리며, 전면이 바뀌는 무거운 효과(`HEAVY_FX`: vignette·flash·letterbox…)는 앞 두 그림에 무거운 효과가 없을 때만. 밤 전용(`NIGHT_ONLY`: twinkle·fireflies·bats·meteors·aurora·lanterns·searchlight·spotlight)은 종이 배경에 안 나온다. 3초 미만 그림과 칠판에는 없음. 우주 그림은 유성(k%3==1)과 겹치지 않게 k%3==0에만 잔잔한 효과. **그림 증거(2026-10-27, miya "그림 규칙도 모두")**: 단어 규칙이 없으면 앰비언트보다 먼저 `tools/picev.py`가 그림의 오브젝트 그룹 이름·크기로 읽은 태그(fire·smoke·steam·rain·ice·candle·bubble·water·flower·forest·desert·sun·insect·bird·wind·cloud·space·cave·bone)로 고른다(`motions.FX_PIC`: 그려진 불 → embers, 굴뚝 → smoke, 호수 → bubbles/ripples, 태양 → rays…; 밤 전용은 종이에서 `FX_PIC_DAY` 대체). 배경 레이어(별 안개·입자 줄·하늘)는 증거가 아니다. 먼지 입자(dust motes)는 4-1 금지 그대로 없다. 입자는 그림의 `<g translate>` 안에 두고 GSAP은 그 안쪽만 움직인다(x/y가 transform 속성을 덮어쓰기 때문).
  - **텍스트 효과 39종** (`labels_lib.NAME_FX` 25 + 단어 규칙 `scramble`·`type`(2026-10-29)·`SAY_FX` 5 + `splitwords`·`NUM_FX` 6, 자막은 제외, 지침서 5장): 이름표 등장은 `(단위 번호×7 + 라벨 번호) % 25`로 pop·typewriter·slideleft·rise·flip·zoom·stamp·wobble·blur·wave·drop·scatter·spin·swing·elastic·sink·slideright·bounceletters·zoomletters·flipletters·glow·underline·highlight·squeeze·fan 중 하나(글자별 효과를 위해 이름표 글자는 `<i>` 하나씩). 말풍선은 문장부호로: `!`=slam(쾅 들어와 떨림), `?`=tilt(갸웃), `...`=slowfade, `~`=jiggle, 그 외 pop, 2.2초 넘게 떠 있으면 둥실(bob). 숫자 배지는 순서대로 slide·drop·flip·zoom·stamp·flashbg 순환(+카운트업·착지 바운스). 단위 대본에 위험 단어(`DANGERW`)가 있으면 말풍선이 한 번 떨고, 핵심 문장 단어(`KEYW`: the key·in fact·turns out…)면 이름표가 1.1초 뒤 한 번 커졌다 돌아온다. **그림 증거(2026-10-27)**: 그림에 불·물·얼음·시계·톱니·책·새·군중… 태그가 있으면 이름표 등장이 그걸 따른다(`labels_lib.PIC_FX`: 불 → glow, 물 → wave, 얼음 → squeeze, 비 → drop, 시계 → flip, 톱니 → spin, 책·타자기 → typewriter, 군중 → scatter, 새 → fan, 연기·동굴 → blur…), 없을 때만 단위·라벨 번호 순환. 칠판: 제목 글자 쓰기(`chalk_title_js`), 결론 밑줄(`chalk_concl_js`).
  - 확인한 것: 합성 페이지(오브젝트 56·효과 57·텍스트 36)에서 JS 오류 0, 모든 트윈이 컷 안에서 끝남, 축 교정 전후 비교(나무·간판). 확인하지 못한 것: 실제 영상 전편 렌더(다음 영상 빌드 때 `motion sanity` 출력과 `motion_check.py`로 확인).
- **구현 조건**: 유한 반복 GSAP 트윈(seek 가능), SVG 필터 금지. 인물 `id`는 서로 다르게, 정지 상태로도 자연스럽게. 인물 동작의 자연스러움은 확인하지 못함(사용자가 판단).

### 4-2. 이미지→영상 프롬프트 템플릿 (영어, 생성 클립용)
```
subtle natural motion, camera still until the focus object is mentioned then one slow eased push toward it, [one action of the main subject],
keep art style and line art consistent, no morphing, no text
```

### 4-3. 장면 나누기와 전환 (사용자 결정 2026-10-09)

**장면 나누기**
- **한 장면 = 새 그림 한 장 = 대본 의미 단위 하나.** 길이 기준(2026-10-22 ×1.5 적용: 최소 8.5초(그림 수가 많은 문단은 균등 분할, 20-2), 최대 단위 9.3초, 초반 5분·숏츠·느린 장면 값)은 20-2가 현행이다. 그림 장수 제한 없음(15분 본편은 컷 길이 20-2에 따라 약 90~110장, 900초÷8.5~9.3초 계산).
- 같은 그림을 확대·이동만 바꿔 여러 컷으로 쓰지 않는다. 컷이 바뀌면 그림이 바뀐다.

**전환 (2026-10-27 miya: '연속 금지' 고정 규칙 없음. 대본 단어에 맞는 전환은 연속이어도 쓰고, 단어가 없는 컷만 적게 쓴 종류부터 고르며 직전 종류를 피한다)**
- **줌**: 나가는 그림은 가운데 물체로 가속 확대(약 2.6배, 1.1초), 들어오는 그림은 확대 상태에서 감속(1.7초). 큰 구간 전환, "들여다본다".
- **모양 겹치기(`match`)**: 가운데 물체 자리(반지름 120px 원)에서 0.9초 원형으로 열림. 앞뒤 물체가 같은 위치·크기·색 계열이고 **같은 장면 안일 때만**.
- **슬라이드**: 오른쪽에서 0.7초, 나가는 그림은 폭 18%만 밀림(순서·나열·비교). **페이드**: 0.6초(같은 장소 시간 경과).
- **워시**(스케치→채색 자리): 배경색(종이 `#ece4d1`, 밤 `#14122b`, 노을 `#5a4562`)으로 0.45초 덮였다 0.45초 걷힘(새 개념).
- **`wipe`** 노란 빛 선(`#ffd54a`) 대각선, 방향 번갈아, 0.8초(원인→결과) · **`iris`** 사이드카 `iris: [x, y]`(없으면 가운데 밖 `focus` 점, 없으면 좌우 번갈아)에서 원이 열림, 0.9초(옆 대상 이야기로) · **`eye`** 가로 한 줄에서 위아래로, 0.8초(open, wake, realize, discover, reveal, see) · **`push`** 위로 밀기 0.7초(fall, drop, sink, deep, down, rise, climb, up) · **`whip`** 0.45초 + 흰 속도선 9개(speed, fast, race, rush, sudden, instant, light, flash) · **`tilt`** −8°·1.25배 카드처럼, 0.8초(?, imagine, what if, surprise, twist).
- **새 전환 5종 (사용자 결정 2026-10-22, 20초 시험 영상 확인)** — 구현 `tools/motions.py`의 `tr_js`·`miyaTr`(seek 가능한 clip-path, 시험 페이지에서 확인)
  - **`seam`** 좌하단에서 우상단으로 노란 선이 쭉 그어진 뒤(0.35초) 선이 두 줄로 갈라지며 사선 띠가 넓어져 다음 장면이 드러남, 1.0초(원인→결과, because·cause·result)
  - **`diamond`** 오른쪽 위(화면 73%·28%) 한 점에서 마름모가 열리고 노란 윤곽이 서서히 사라짐, 0.9초(열쇠·보석·비밀·unlock). 마름모는 네 모서리를 완전히 덮은 뒤 끝나서 끝에 튀지 않는다
  - **`page`** 앞 그림이 왼쪽 가장자리로 접혀 사라지고(가로 1→0) 새 그림이 오른쪽에서 드러남, 흰 선이 경계를 따라감, 0.8초(chapter·story·history)
  - **`zigzag`** 흰 지그재그 찢김 선이 왼쪽에서 오른쪽으로 쓸고 감, 0.9초(break·split·crack)
  - **`wave`** 노란 물결선이 아래에서 올라오며 새 그림이 드러남, 1.0초(water·ocean·flow)
  - 이 5종도 느린 장면 제외·횟수 균형 규칙을 따르고, `TR_WORDS`에 단어가 들어 있다. 시험 영상에서 시계방향 부채꼴 전환은 사용자가 별로라고 해 뺐다.
- **쓰지 않음**: 색 막대(`blinds`, 2026-10-16 모든 영상에서 뺌, 코드는 남음), 시계방향 부채꼴 와이프(2026-10-22), 점 격자/모자이크(2026-10-14 삭제).
- **자동 선택(`TR_WORDS`)**: 단위 대본에 위 단어가 있고 제 몫(전체의 1/16)의 1.3배 이하이면 항상(2026-10-27, 전에는 50% 확률) 그 전환, 아니면 많이 쓴 전환일수록 덜 뽑힘. 장면이 바뀔 때는 줌·워시·눈 뜨기를 더 자주. 느린 장면은 차분한 전환만(20-2). 칠판 앞뒤는 하드컷.
- 효과음: 줌·슬라이드(낮게)·wipe·push·whip=swish, match·iris·eye=hush, 워시=rustle, tilt=pop, 페이드 무음. 우주 모드 wipe·push·whip=warp, iris·eye=glimmer.
- 전환은 앞 장면 빈 간격(0.8초) 안에서 시작해 내레이션과 겹치지 않는다. 추가 전환의 Actions MP4 모습은 확인하지 못함.
### 4-4. 방향 규칙 표 (2026-10-27, miya: "눈이 없는 것들, 바람·빨려 들어가는 것도 방향성이다 … 다양하게 생각해")

방향이 걸리는 모든 것은 **대본 단어·그룹 이름·그림 안 위치**로 코드가 맞춘다. 모델이 그림마다 따로 판단하지 않는다. 그림 한 장의 방향 문맥은 `facing.context()`가 세 값으로 정한다: **travel**(주인공 이동 방향, 옆으로 이동하는 그룹의 경로·dist 부호), **wind**(사이드카 `wind: "left"|"right"`, 없으면 이동의 반대 = 맞바람, 이동이 없으면 +1 오른쪽), **attractor**(사이드카 `attractor: [x, y]`, 없으면 이름에 hole·vortex·whirl·drain·magnet·gravity·funnel·mouth·maw·sun·star가 든 가장 넓은 그룹의 중심).

| 가족 | 무엇이 | 어떻게 맞추나 | 코드 |
|---|---|---|---|
| 이동 ↔ 머리 | path·swim·rollby·creep·magnet·slide 그룹 | 머리 = 어두운 동공(≤4개) 위치 > `data-face` > 눈이 없으면 **뾰족한 쪽**(rocket·arrow·probe·plane·comet·ship·boat·sub·sled·train·car… 탈것·뾰족한 물건 이름일 때 좌우 20% 띠의 윤곽 높이 비 < .6). 이동과 다르면 그림을 몸통 중심으로 거울상 | `facing.facing_sign`·`apply` |
| 중력 | 이름에 sink·fall·drop·descend·plunge·dive·settle(내려감) / rise·ascend·climb·launch·lift·soar·bubble·float·balloon·escape(올라감)가 든 `mv-path` | 경로가 반대로 가면 경로를 뒤집음(끝→시작). 탈것 이름(lander·carcass)은 판단하지 않음(스톨른타임 U115 우주선은 위로 날아가는 그림) | `facing._path_rules`, `reverse_path` |
| 빨림 | attractor가 있는 그림의 `mv-magnet`, 이름·태그에 pull·suck·spiral·drain·inward·toward·into·capture·plunge가 든 `mv-path` | magnet은 `data-dx/dy`를 attractor 쪽으로 다시 계산, path는 끝점이 attractor에서 멀어지면 뒤집음(A·S·T 명령 경로는 로그만) | 같은 함수 |
| 바람 흔적 | 배경 입자 수평 이동, 비 기울기(`x + ds·L·.35`), 바람선(`windlines`) 좌우, 안개·구름 흐름 | 전부 `dir_sign(kind, wind, travel)`: 생물 줄(fish·birds·bats)은 travel 쪽으로(머리도 뒤집음), 나머지는 wind 쪽으로 | `motions.fx_markup`·`fx_js` |
| 유성·줄무늬 | `streak` 꼬리 | 이동의 반대쪽 | `motions._shape0` |
| 카메라 | 이동 그림의 드리프트 팬(mv 1·2) | 세계가 이동의 반대로 밀림(= 카메라가 따라감), 역방향 팬 금지 | `build3` `dx = -travel·W·.025` |
| 개구리 타기 | 탄 개구리 | 이동 방향을 봄(`flip = travel_sign`) | `frog_place` |
| 개구리 밀기 | 밀 수 있는 물건(lens·cart·crate·rock·sled…)이 오른쪽으로 이동 | 개구리는 물건 **뒤**(왼쪽)에서 밀며 오른쪽을 봄; 왼쪽 이동이면 원래 자리(오른쪽·손잡이) | `frog_place` PUSHG |
| 슬라이드 | `mv-slide` 패널 | 들어올 때 `data-dx` 반대로, 나갈 때(`data-dir="out"`) `data-dx` 쪽으로 이동하는 것으로 셈 | `facing.travel_sign` |

- **B. 2차(2026-10-27, miya "자동 아닌 것도 규격화", `facing._dir_rules2`)** — 위에서 '자동 아님'이던 것들도 코드 규칙으로 바꿨다. 빌드 때 자동, 로그 `direction sanity`에 같이 나온다.

| 가족 | 무엇이 | 규칙 | 비고 |
|---|---|---|---|
| 톱니 맞물림 | 이름에 gear·cog·sprocket이 든 `mv-spin`·`mv-rotor`·`mv-core-spin/turn` 그룹 | 서로 닿는(중심 거리 ≈ 반지름 합) 톱니는 반대 방향: `mv-core` 톱니가 기준(+1), 나머지 `data-dir`를 2색 칠하기로 고침 | 홀수 고리(세 톱니가 서로 다 닿음)는 고칠 수 없어 로그만 |
| 깃발 | 이름에 flag·banner·pennant·windsock·sail·streamer | 깃대 = 그룹 안 가장 키 큰 가느다란 도형; 천이 바람 반대쪽에 있으면 깃대를 축으로 거울상 | 깃대가 없으면 왼쪽 가장자리가 깃대(flagwave 규칙과 같음) |
| 기울어진 것 | smoke·steam·plume·exhaust·hair·scarf·cape·spray·mane·mist·grass·reed·wheat·kelp·flame·fire·candle | 윤곽의 위 30%와 아래 30% 평균 x 차이(기울기)가 높이의 8% 넘고 바람과 반대면 가운데 축으로 거울상 | 깃발·기울기 둘 다 **바람을 아는 그림에서만**(사이드카 `wind` 또는 이동 오브젝트가 있을 때); 멈춘 그림은 그린 대로 |
| 시선 | 이름에 person·man·woman·kid·scientist·astronaut·owl·cat·dog·bear·deer·cow·bird·fish… (사람·동물) 그룹, 부품(`mv-chain/joint/limb`)·이동 그룹 제외 | **초점**(이동 오브젝트의 경로 중간 > attractor > 가장 넓은 `mv-core`)이 150px 넘게 옆에 있는데 눈이 반대를 보면 몸 중심으로 거울상 | 눈이 없으면 판단 안 함(`data-face`로 지정 가능) |
| 빛·그림자 | 광원 = 사이드카 `light: "left"|"right"` 또는 이름에 sun·lamp·lantern·candle·torch·moon·bulb·fire·flame·window가 든 가장 넓은 그룹. 대상 = 오브젝트 그룹 **안**의 id/class에 shadow·shade(그림자)·highlight·glint·shine·specular·rimlight(하이라이트)가 든 도형 | 그림자는 광원 반대쪽, 하이라이트는 광원 쪽에 있어야 하고(그룹 중심 기준 폭의 8% 넘게 치우친 것만) 아니면 그룹 중심 축으로 거울상 | 광원이 없는 그림은 점검 안 함. 바닥 전체를 덮는 그림자(폭 90% 이상)는 제외. id 없는 도형은 로그만 |
| 소용돌이 ↔ 개구리 궤도 | 블랙홀·소용돌이를 도는 개구리(`orbit` 동작) | 고리 그룹의 `data-dir`(`mv-spin`·`mv-rotor`), 없으면 그림의 첫 `mv-circle`/`mv-spin`/`mv-rotor`의 `data-dir`, 없으면 시계방향 → 개구리도 같은 방향 | `facing.spin_dir`, `frog_place`가 `act.dir`에 적음 |

- 그림 에이전트가 여전히 직접 맞춰야 하는 것: 그려진 두 사람끼리의 시선 교환(초점이 하나뿐이므로), 그룹 밖에 따로 그린 그림자, 톱니 셋이 서로 다 닿는 배치(안 그린다).
- 예시: `/mnt/project-files/frog-rules/direction/rules2-before-after.png`(합성 그림: 톱니·깃발·연기·시선·그림자가 한 번에 고쳐짐).
- 점검: `python3 tools/facing.py <슬러그>`가 그림별 문맥·경로 규칙·그룹 판정을 출력하고 파일은 바꾸지 않는다. 빌드 로그 `direction sanity`에 뒤집은 수·맞바람 그림 수·attractor 수가 나온다.
- 2026-10-27 4편 점검: 뒤집힌 그룹 고래 낙하 U002 하나, 경로 뒤집음 0, 눈·뾰족함으로 판단 못 한 그룹은 로그에 `unknown facing`으로 남음(그림 에이전트가 `data-face`를 적으면 해결).

### 4-6. 오픈소스 라이브러리 효과 표 (2026-10-29, miya: "시연 안 한 것까지 모두 파이프라인에 붙이고 대본·그림 규칙으로 일괄 적용")

GSAP 3.15(2025년부터 플러그인 전부 무료) 14개 플러그인 + anime.js 4 + lucide 아이콘 2,193개 + svgo를 빌드에 넣었다(`tools/fxlib.py`가 등록·이징·규칙, `tools/assets/gsap/`·`anime.min.js`·`lucide.json`). 모델이 고르지 않는다: **대본 단어 > 그림 증거(그룹 이름) > 단위 번호** 순서의 코드 규칙이며, 사이드카로 끄거나 바꿀 수 있다. 빌드 로그 `library fx`에 무엇이 몇 번 붙었는지 찍힌다. 모든 효과는 기존과 같이 GSAP 타임라인에서 seek되며(anime 타임라인도 `miyaAnime` 프록시로 seek), 구간 렌더에서도 같은 프레임이 나온다.

| 라이브러리 | 무엇 | 규칙(누가 고르나) | 코드 |
|---|---|---|---|
| DrawSVGPlugin | 오브젝트 외곽선이 펜으로 그리듯 그려지고 채색이 뒤따름 | 그림 에이전트가 `mv-draw-<이름>`(지도·설계도·경로·스케치 장면); 라벨·배지 픽토그램은 자동으로 이렇게 등장 | `motions.obj_js('draw')`, `fxlib.LIB_JS miyaIconDraw` |
| MorphSVGPlugin | 한 모양이 다른 모양이 됨(A가 B로 변한다는 문장) | 에이전트가 `mv-morph-<이름>` 그룹에 첫 path(지금)+마지막 path(목표, `opacity="0"`); `data-back="1"`이면 되돌아옴 | `miyaMorph` |
| MotionPathPlugin | 등록만(기존 `mv-path`는 자체 `miyaPath` 유지) | — | — |
| SplitText | 3단어 이상 말풍선의 단어가 하나씩 내려앉음 | `say` 라벨이 느낌표·물음표·말줄임 규칙에 안 걸리고 3단어 이상이면 자동 | `labels_lib.label_js` `splitwords` |
| ScrambleTextPlugin | 이름표 글자가 잡음에서 정리됨 | 단위 문장에 secret·code·decode·cipher·mystery·unknown·signal·hidden·random… (`fxlib.SCRAMBLE_W`); 숫자 있는 라벨은 숫자 문자로 | `name_fx → 'scramble'` |
| TextPlugin | 이름표 타자기(한 글자씩) | 단위 문장에 typed·wrote·letter·telegram·diary·journal·manuscript·report… (`TYPE_W`) | `name_fx → 'type'` |
| Physics2DPlugin | **배경 `burst`**: 중심에서 조각 72개가 중력으로 날아감 + 고리 | 단어 confetti·fireworks·shatter·scatter·splash·spray·erupt·burst·explode·detonate·sneeze… (`FX_WORDS` 첫 규칙, 무거운 효과라 2장면 간격) | `fx_markup/fx_js('burst')` |
| Physics2DPlugin | **오브젝트 `toss`**: 던져져 포물선 | 에이전트 `mv-toss-<이름>` (`data-v`·`data-angle`·`data-g`) | `obj_js('toss')` |
| InertiaPlugin | **`skid`**: 미끄러지다 멈춤(스냅) | 에이전트 `mv-skid-<이름>` (`data-v`·`data-dist`·`data-res`) | `obj_js('skid')` |
| PhysicsPropsPlugin | **`coast`**: 바퀴·팽이·동전이 돌다가 마찰로 멈춤 | 에이전트 `mv-coast-<이름>`; 축 점검은 `spin`과 같음(나무는 못 돎) | `obj_js('coast')` |
| Flip | **`regroup`**: 여러 개가 그려진 자리에서 고리·줄·격자로 재배치 | 에이전트 `mv-regroup-<이름>` (자식 2개 이상, `data-shape` ring/line/grid) — 모이다·줄 서다·흩어졌다 모이다 문장 | `miyaRegroup` |
| CustomBounce | 진짜 튕김 + 찌그러짐 | 기존 `bouncing` 오브젝트·중심 `drop`가 자동으로 이 이징(`miyaBnc`·`miyaBnc-squash`) | `REGISTER_JS` |
| CustomWiggle | 흔들림이 잦아듦/일정/불규칙 | 기존 `shake`(easeOut)·`shiver`(uniform)·중심 `tremble`(random)·개구리 `shiver`(uniform)가 자동으로 이 이징 | `wiggle({wiggles,type})` |
| CustomEase | 등록(위 이징들의 바탕) | — | — |
| EasePack SlowMo | 이동 오브젝트의 속도 램프(천천히→질주→천천히) | 단위 문장에 rush·dash·race·speed·fast·zoom·accelerate… (`SPEED_W`) → `mv-path`의 `data-ease`; 에이전트가 적은 `data-ease`가 우선 | `fxlib.path_ease` |
| EasePack RoughEase | 카메라 자체가 덜컹거림 | 단위 문장에 earthquake·tremor·turbulence·bumpy·rough·storm·engine… (`ROUGH_W`), 드리프트 카메라만; `randomize:false`(구간 렌더 일치) | build3 드리프트 |
| EasePack ExpoScaleEase | 줌이 일정한 체감 속도로 | 포커스 카메라가 있고 문장에 zoom·closer·magnify·microscope·telescope·tiny·vast… (`ZOOM_W`) | build3 포커스 |
| anime.js spring | 통통 튀는 등장 | 문장이 playful(bounce·hop·jump·spring·excited·cheer…)이고 grim 단어가 없을 때 `popin`·`rise` 오브젝트와 `pop` 이름표; 단위 번호로 soft/medium/stiff | `fxlib.spring_params`, `miyaSpringTo` |
| anime.js stagger grid | **배경 `gridripple`**: 점 격자가 중심에서 물결치고, 이어서 왼쪽부터 쓸고 감 | 단어 spread out/across·chain reaction·domino·contagion·epidemic·outbreak·broadcast·echo·propagate·cascade·went viral·wave of | `fx_js('gridripple')` + `miyaAnime` |
| lucide | 이름표·숫자 배지 앞의 작은 픽토그램(선 그리기로 등장) | 라벨 글자의 단어가 `fxlib.OVERRIDE`(whale→fish, years→calendar, brain, virus→biohazard…) 또는 아이콘 이름과 같을 때만; UI 아이콘·태그 매칭은 안 씀(2026-10-29 드라이런에서 hole→drill 같은 오매칭) ; 말풍선에는 안 붙임 | `fxlib.icon_for`, `labels_lib.html_for` |
| svgo | 그림 SVG를 빌드 전에 정리(숫자 2자리, 편집기 찌꺼기 제거) — 원본은 그대로, 사본 `build/art_opt/` | id·data-*·그룹·숨김 요소·기본 도형·빈 그룹·transform 보존(규칙이 읽는 것). `npx` 없으면 건너뜀(로그 `svgo: skipped`), `SVGO=0`으로 끔 | `tools/svg_opt.py` |

- 안 넣은 것과 이유: ScrollTrigger·ScrollSmoother·ScrollTo·Observer·Draggable(스크롤·마우스), Pixi·Easel(다른 렌더러), CSSRule, GSDevTools·MotionPathHelper(개발 도구); anime.js의 svg 도구(createDrawable·morphTo·createMotionPath)는 GSAP 플러그인과 겹쳐 GSAP 쪽만 씀; three.js·lottie·rive·remotion·theatre·penpot(2026-10-28 판정).
- 에이전트용 요약은 `tools/art_spec.md` 7(새 `mv-` 종류와 data-*), 반복 원칙은 그대로(단어가 이어지면 같은 효과 반복).
- 확인한 것(2026-10-29): 합성 페이지에서 새 모션 6종·배경 2종·텍스트 5종 동작(JS 오류 0, 프레임 시트), whale-fall-short1 실제 빌드 전체 seek JS 오류 0(픽토그램 3, ExpoScale 1, 배경 1, svgo 297→279 KB). 확인하지 못한 것: 실제 MP4 렌더(Actions)와 네 영상 전체 재빌드의 화면 — 다음 렌더에서 본다.

개정: 2026-10-27 (miya, 고래 영상 물고기 역주행) 방향 점검: 배경 입자 `fish` 머리 방향·유성 꼬리 방향을 이동 방향에 맞춤(`motions._shape0`), 옆으로 이동하는 오브젝트(path·swim·rollby·creep·magnet)는 `tools/facing.py`가 눈(어두운 동공) 위치로 머리 방향을 알아내 이동 방향과 다르면 그림을 몸통 중심으로 거울상으로 뒤집음(`build3` 로그 `direction sanity`, 그룹 `data-face="left|right"`로 지정 가능, 그룹에 transform·text가 있으면 뒤집지 않고 로그만), 탄 개구리는 이동 방향을 봄(`frog_place`). 4편 점검: 고래 낙하 U002(가라앉는 고래)만 뒤집힘, 나머지는 눈이 없어 판단 안 함.
개정: 2026-10-27 (miya) 전환·배경 효과의 '연속 금지' 고정 규칙 제거: 단어가 맞으면 연속 허용, 채움 선택만 직전과 다르게(코드 `build3` 전환, `motions.fx_for`).
개정: 2026-10-27 (miya, "바람·빨림도 방향성") 4-4 방향 규칙 표 신설: 이동↔머리(눈 없으면 뾰족한 쪽), 중력·빨림 경로 뒤집기, 바람 흔적(입자·비·바람선·안개), 카메라 팬, 개구리 타기·밀기를 코드 규칙으로(`facing.context`·`_path_rules`, `motions.dir_sign`, `build3` DIRC).
개정: 2026-10-27 (miya, "자동 아닌 것도 규격화") 4-4 B 신설: 톱니 맞물림·깃발/기울어진 것의 바람 방향·사람/동물 시선·그림자/하이라이트의 빛 방향·개구리 궤도 방향을 코드 규칙으로(`facing._dir_rules2`·`spin_dir`, 사이드카 `light`).
개정: 2026-10-27 (miya, "오브젝트·개구리·배경·텍스트 모두 그림 규칙+대본 규칙") 배경 효과·텍스트 효과에 그림 증거(`tools/picev.py` 태그) 추가: 단어 > 그림 > 앰비언트/순환.
개정: 2026-10-29 (miya, 오픈소스 라이브러리 통합) 4-6 신설: GSAP 플러그인 14개·anime.js·lucide·svgo를 빌드에 넣고 대본 단어·그림 증거·단위 번호 규칙으로 자동 적용(오브젝트 62종, 배경 59종, 텍스트 39종). 시연 영상 /mnt/project-files/motion-demo/opensource-2026-10-29/.

### 4-7. 붙임 규칙과 점검 (2026-10-29, miya: "풍차·그물·개구리 다리·꼬리·목·시곗바늘·톱니·나무·풀·팻말 축이 이상하다 … 에이전트가 놓치지 않게 점검 코드를 넣고 마지막에 메인이 다시 확인")

**규칙(그림 에이전트와 메인 모두).** 움직이는 부분은 몸에 붙어 있어야 한다.
1. `mv-joint`/`mv-chain`/`mv-swing`/`mv-rotor`/`mv-pendulum`의 `data-pivot`은 **그 부분이 몸·받침에 닿는 점**이다. 부분 위에 있고(≤12 px) 몸(또는 부모 마디)에도 닿아야 한다. 허공 중심이면 안 된다. 힌지 핀(작은 원)이 그룹 안에 있으면 그 핀이 받침이다. 화면 가장자리에 매달린 것(천장 램프)은 가장자리가 받침이다.
2. **그물·깃발·막대에 붙은 것**: 그물 주머니만 흔들고 막대는 가만히 있으면 떨어져 보인다. 피벗을 막대 끝과 테두리가 만나는 점에 둔다.
3. **둥근 면 위의 회전**(시계 바늘·바퀴): 피벗 = 그 둥근 면의 중심. **톱니바퀴**: 피벗 = 톱니 중심, 이웃 톱니는 이 맞물림(중심 거리 = 두 피치 반지름의 합)과 반대 방향, 주기는 톱니 수에 반비례. 껍질·창 같은 원 안에 들어가야 한다. 도구: `python3 tools/gearmesh.py <svg> <톱니A id> <톱니B id> <각도>`(두 톱니를 맞물리게 다시 그림).
4. **몸이 이동하면 꼬리·다리·목도 그 이동 그룹 안**에 넣는다(`tools/joinpart.py`). 이동 그룹(`mv-path/creep/swim/glide/...`) 밖에 꼬리가 있으면 몸만 간다. 꼬리 사슬(`mv-chain-*-1` → `-2`)은 부모 마디 안에 중첩.
5. **새 목+머리**는 한 사슬: 머리를 목 그룹 안에 넣어 함께 움직인다.
6. **서 있는 것(나무·갈대·풀·팻말·기둥·탑)**: 그룹에는 그것 자체만(팻말은 **기둥 + 판 전부**, 그림자·물·땅은 밖), 한 그룹에 떨어진 덩이 둘 이상이면 덩이마다 그룹으로 나눈다(`tools/splitclumps.py`). 축은 줄기·기둥의 **발**이다. `tools/setbase.py <slug>`가 `data-pivot`을 써 준다(코어 `mv-core-sway-*`도 `data-pivot`을 따른다).
7. 이름표·말풍선의 `to`는 움직이는 오브젝트 **안**에 찍는다(옆 45 px 이내면 점검이 걸리고 `attachcheck.py --fix`가 안으로 옮긴다).

**코드가 보장하는 것(같은 날 원인 수정).** ① 이름표 따라가기 측정(`miyaFollowInit`)이 페이지를 불러올 때 타임라인을 감아 보면, 그때 아직 숨겨진(display:none) 그림의 힌지 트윈이 처음 그려지며 GSAP가 빈 bbox 모서리를 `svgOrigin`으로 굳혔다. 그래서 풍차·톱니·개구리 다리·꼬리·목·시곗바늘이 전부 엉뚱한 점을 중심으로 돌았다(2026-10-27 이후 만든 영상 전부). 이제 `data-pivot`을 쓰는 트윈(`svgOrigin:miyaPv`)은 **측정이 끝난 뒤에** 만들어진다(`build3.py`, 로그 `hinge tweens added after the follow measuring`). ② 모든 `svgOrigin`에 `smoothOrigin:false`(가만히 있을 때 몸에서 밀려나 있던 정적 오프셋 제거). ③ 이름표 따라가기는 그림이 시작할 때(오브젝트가 그려진 자리)를 기준으로 옮김을 잰다(라벨이 뜨기 전에 오브젝트가 이미 움직였어도 어긋나지 않음).

**점검 코드(누가 언제).**
| 도구 | 무엇 | 언제 |
|---|---|---|
| `tools/attachcheck.py <slug> [uid..]` (`--fix`) | 그림 SVG 정적 점검: 위 1~7 | 그림 에이전트가 **그림을 낼 때마다**(보고 전 필수), `build3`이 끝날 때 자동 |
| `tools/motionaudit.py <dir> <uid..>` | 만든 페이지를 3시각에서 찍어 피벗마다 빨간 점을 그린 띠 이미지 | 에이전트가 사람·동물·기계 그림을 **눈으로** 확인(점이 몸 위인지) |
| `tools/pivotlive.py` | 만든 페이지에서 힌지의 실제 회전 중심을 재서, 피벗이 10 px 이상 끌려가면 실패 | 메인 최종 점검 |
| `tools/final_check.py` | 위 둘 + 그림 누락 점검, 통과하면 `render/<slug>/.checked`(index.html sha1) | **메인이 렌더 푸시 직전 반드시**. `chunk_plan.py`는 `.checked`가 없거나 낡으면 렌더 사양을 내놓지 않는다 |
보조: `tools/grpinfo.py <slug> <uid..>`(mv 그룹 상자·피벗·부모 목록), `tools/setbase.py`, `tools/splitclumps.py`, `tools/joinpart.py`, `tools/gearmesh.py`.
