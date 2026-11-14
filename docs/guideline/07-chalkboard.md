## 7. 칠판 인포그래픽과 노트 개구리

> 최종 수정: 2026-11-14 · 본문은 지금 유효한 규칙만 담는다. 바뀐 경위는 맨 아래 개정 이력.

**칠판을 쓰는 때**: 숫자·비교·변화·측정값이 나올 때.
- 과학·통계 주제에서 영상당 5~10개(최대 10), 한 번에 5~18초. 문단이 길면 칠판 장면과 일러스트 장면으로 나눈다.
- 역사 서사에서는 거의 쓰지 않는다.
- 모든 글자는 영어.

### 7-1. 배경과 프레임

| 요소 | 값 |
|---|---|
| 바탕 | 짙은 초록 `#2D4F40`(`#2A4E42`~`#2A4E36`) + 미세한 얼룩 질감 |
| 나무 틀 | 맨 아래, 높이 약 20~30px, `#9E7246` |
| 소품 | 아래 왼쪽 분필 4개(흰/노랑/코랄/하늘), 아래 오른쪽 지우개 2개 |
| 로고·자막 | 일반 컷과 같음 |

### 7-2. 노트 개구리
채널 캐릭터. 그림 `tools/assets/frog.svg`, 코드 `tools/frog.py`·`tools/frog_rig.py`, 자동 배치 `tools/build/frog_place.py`, 개념·테마 팩 `tools/concepts.py`.

**공통 원칙**
- 모든 영상에서 대본·그림의 상황마다 동작·표정·의상·말풍선을 고른다. 아래 표의 예시는 전부가 아니다. 표에 없는 상황은 맞는 동작·의상·말풍선을 새로 정해 쓴다(필요하면 `ACTS`·`frog.py`에 추가).
- 선택은 전부 코드 규칙이다: **단위 대본의 단어(정규식) + 그림 증거(그룹 이름·크기·팔레트) + 단위 번호**. 난수와 모델 판단이 없다. 같은 입력이면 어떤 모델이 돌려도 같은 사이드카가 나온다. 다르게 하려면 사이드카 `lock`으로만 바꾼다.

**절 찾기**

| 절 | 내용 |
|---|---|
| A | 역할(칠판 / 그림 장면) |
| B | 언제 나오나, 밀도 |
| C | 위치·크기·안전 구역 |
| D, D-2 | 동작 표, 판정 순서 |
| E | 의상 |
| F | 표정·말풍선 |
| G | 등장·퇴장·눈 깜빡임 |
| H | 작업 순서 |
| I | 관절 리그, 접촉·이동·의상 동작 |
| J | 빨려듦(pull) 횟수 제한 |
| K | 개념 규칙·테마 팩·최소 사용 선택·다양성 검사 |
| L | 맥동 오브젝트 반응, 카메라·전환·배경 효과 연동 |

#### A. 역할
1. **칠판 장면 = 설명하는 개구리**
   - 왼쪽 아래에 선다(출처 줄·분필은 오른쪽으로 밀린다). 아래에서 폴짝 등장한다.
   - 행·결론이 말해지는 순간 그쪽을 가리킨다. 팔은 대상이 바뀔 때만 돈다.
   - 말에 맞춰 입을 벌린다(`talk`).
   - 끄려면 `config.py`에 `FROG = False`.
2. **그림 장면 = 곁에 있는 개구리(설명·가리키기 없음)**
   - `plan.json`의 `frog_hint: true` 단위에만 나온다.
   - TTS에 맞춘 입 움직임이 없다(기본 `talk: false`). 놀람·외침 표정에서는 입을 벌려도 된다.

#### B. 언제 나오나
1. **이유가 있는 개구리만**: 상황에 맞는 동작(`act`), 오브젝트와 함께 움직임(`ride`·`cling`·`push`·`fly`), 장면 의상, 말풍선 중 하나가 있을 때만 나온다. 아무 이유 없이 오브젝트 위·화면 아래에 서 있는 개구리는 금지. 타는 것도 반응할 상황도 없으면 `frog_place.py`가 건너뛴다(`skip (no situation)`).
2. **밀도**: 롱폼·숏츠 모두 단위의 약 35~50%(한 단위씩 건너뛰며). 30% 아래면 `frog_place.py`가 경고한다. 그러면 상황이 있는 단위에 `frog_hint`를 더한다. 개구리가 0인 숏츠는 만들지 않는다.

#### C. 어디에 두나 (위치·크기)
1. **주인공 오브젝트의 한가운데 위에 앉히지 않는다**(화면의 초점을 가린다).
   - 강한 상황(바람·떨림·빨려듦 등)으로 탈 때: 오브젝트의 화면 가장자리 쪽 끝(가로 20%/80% 지점), 실제로 그려진 표면 위에 발을 붙인다(`perch`).
   - 차분한 동작(갸웃·살피기·끄덕임·숨쉬기·올려다보기·졸음): 오브젝트 옆 발치에 서서 오브젝트를 바라본다(`beside`, 같은 그룹 안이라 같이 움직인다).
2. 개구리·말풍선이 그림 속 글자(라벨·말풍선)와 겹치면 반대쪽 끝/옆으로 옮긴다. 화면 가로 12~88% 밖(드리프트 카메라에 잘림)에는 두지 않는다.

   **2-1. 안전 구역**

   | 번호 | 규칙 |
   |---|---|
   | ① 자막 | 자막 상자 위에 둔다: 롱폼 발 y ≤ H-190, 숏츠 ≤ H-360, 옆에 설 때 롱폼 ≤ H-290 |
   | ② 말풍선 자리 | 머리 위 말풍선이 잘리지 않게: 발 y ≥ 82·s+150. 배경 띠는 롱폼 340~780 |
   | ③ 로고 | 오른쪽 위 로고 구역(x > 0.74W이고 y < 430)에 두지 않는다 |
   | ④ 이동 오브젝트 | `mv-slide-*`·`mv-path-*`처럼 단위 중에 이동하는 오브젝트는 시작 위치 기준으로 붙으므로 화면 중앙 쪽 끝/옆에 붙인다 |
   | ⑤ 작은 오브젝트 | 폭 260 미만(별·광자·손목시계)에는 타지 않고 옆에 선다 |
   | ⑥ 구멍 | 구멍(블랙홀) 그룹을 골랐으면 그 위에 서지 않고 옆에 떠 있다가 `pull`(겁먹고 빨려 들어감) |

3. **크기**: 탈 때 s 0.8~1.25(오브젝트 폭/230), 곁에 설 때 0.95, 배경 이동 롱폼 ≈0.8·숏츠 ≈1.1(숏츠는 ×1.15). 같은 자리·같은 크기를 반복하지 않는다.

#### D. 무엇을 하나 (동작 `act`)
- 몸 동작은 안쪽 그룹 `#fg<tag>_ac`, 이동은 `_tr`, 회전은 `_rm`.
- 사이드카 `frog.act`(문자열 또는 `{"type":..}`)로 손으로 고칠 수 있다.
- 판정 순서는 D-2, 전체 우선순위는 I-7.

**상황 동작 표 (위에서부터 먼저 맞는 것)**

| 상황(대본·그림) | 동작 | 표정 | 말풍선 예 |
|---|---|---|---|
| 중력·시공간 휘어짐·깔때기·그릇 + 그림에 구덩이·격자·천·무거운 천체(없으면 하지 않음, 구멍 이름 그룹을 우선 목표) | `slide`(가장자리에서 바닥으로 미끄러짐, 바닥에서 살짝 헤롱) | surprised | Wheee! / Down I go! |
| 블랙홀·지평선·빨려듦(횟수 제한 J) | `pull`(똑바로 선 채 가늘게 떨며 쏠림, 기울임 없음) / 별에 타 있으면 `vanish`(돌며 작아져 사라짐) | scared | AAAAAH! / Nooo! / Heeelp! |
| 지평선 고리 `mv-edge-horizon` / 입자·고리 | `orbit`(고리를 입자처럼 돎) | dizzy | Whoa-oa-oa... |
| 속도·로켓·발사·상승 | `wind`(느린 사인 기울임 한 번, 바람 줄 없음) / 탈것이면 날개 옆 `cling` | squint | Whooosh! / Zoooom! |
| 인물이 탈것으로 날아감 | 발판 개구리 `fly`(슈퍼맨 자세, 인물은 그대로, 손으로 쓴 사이드카 `lock`) | excited | |
| 파도·바다 | `waves` | surprised | Whoa-oa! / Splash! |
| 외로움·공포·추위 | `shiver`(떨기, 기울임 없음, 트윈 하나) | scared | Brrrr... / Eek... |
| 거대한 것 | `awe`(올려다보며 뒤로 젖힘) | surprised | Woooow! / So big! |
| 느린 시간·기다림 | `sleepy` | sleepy | Zzz... |
| 더위·열 | `{"type":"dizzy"}`(소용돌이 눈·붉은 뺨·땀) | dizzy | So dizzy... |
| 노트·기록 + 그림에 책·종이 | `doodle`(연필 낙서) | curious | |
| 돋보기·상자처럼 움직이는 물체 | `push`(손잡이 쪽을 잡고 끙끙, 땀) | squint | Heave-ho! |
| 문 2개 이상 + 마을·집 | `huts`(집마다 들어가 옷 한 점씩, `fore_steps`) | excited | Woo-hoo! |
| 진짜 환호(solved·discover…) | `cheer`(낮은 점프, 두 번에 한 번은 `nod`) | excited | Yay! / Got it! |
| 배경 이동 | `roam`: 발판+뛰기 말 → 발판 위 `run`/`moonhop`, 휩쓸림 → `roll`, 우주·물 → `swim`/`lie`/`tumble`(느리게 출발·정지), 그 밖 `walk` | | Boing! / Blub blub! |
| 공포·끔찍함(terrifying·horror·scream…) | `hide`(두 손으로 눈 가림, 손가락 사이로 봄) | scared | Eek! / Can't look! |
| 숨김·비밀·미지(hidden·secret·mystery·lurk…) + 그림에 큰 단단한 물체(글로우·고리·선·배경 그룹 제외) | `peek`(그 물체 뒤에서 머리만 빼꼼, `behind`) | curious | Psst... / Who's there? |
| 매달림·풍선·절벽·붙잡음 + 그림에 balloon·branch·rope·wire·ring·hook·tail·fin·antenna·pole… 그룹 | `hang`(그 아래 두 손으로 매달려 흔들림) | surprised | Hold on! / Whee-ee! |
| 검사·측정·두드림·실험(test·check·measure·press·knock·scan…) + 탈 물체 | `tap`(앉아서 물체를 톡톡, 닿는 곳에 파장 고리 `_tp`) | curious | Knock knock! / Hmm? |
| 휴식·안도·안전·집(rest·calm·finally·safe·home…) + 탈 물체 | `rest`(물체 위에 기대 눕기, 느린 숨) | sleepy | Phew... / Ahh... |
| 관측·망원경·먼 곳(observe·telescope·distant·gaze…) 우주·밤 그림 | `scope`(망원경 `_sc`로 들여다봄, 가끔 내림) | squint | Oooh... / There! |
| 그림에 사람 그룹(person·astronaut·scientist·villager…) | 그 옆에서 `wave`(손 흔들기, 사람 쪽 시선) | happy | Hi! / Hello! |
| 탄 물체가 튀어나옴·쾅·신호(`core-pop/ping/stamp/drop/flicker`, `popin`) | `startle`(움찔 + 놀란 얼굴 → 제자리) | shock | Whoa! / Yikes! |
| 탄 물체가 이동(`core-glide/approach`, `path`, `slide`) 차분한 문장, 짝수 단위 | `lean`(진행 반대쪽으로 기울어 버팀) | squint | Hang on... |
| 상황 단어 없음 | 차분한 동작 `tilt`·`look`·`sway`·`nod`·`breathe`, 우주면 가끔 느린 `float`. **제자리 점프 금지** | 문장별 | 화면 내용 단어 우선(Tick tock... / Which way? / Let me see...), 없으면 Hmm? / I see! |

- 맥동하는 물체는 타지 않고 옆에서 반응한다(L-1, L-2).
- 가두는 장면: 그림 안쪽 `sad` + "Let me out!"(손 사이드카 `lock`).

**단어로 고르는 상황 동작 26종 (`frog_place.py`의 `DANCEW`·`SALUTEW`…·`ACT_WORDS2`)**

| 동작 | 상황 |
|---|---|
| dance | 음악·축제 |
| salute | 군인·명령·경례 |
| think | 수수께끼·why |
| facepalm | 실수·어리석음 |
| idea | 발견·깨달음(전구) |
| read | 책·기록·편지 |
| eat | 음식·먹기(무거운 주제 제외) |
| cry | 슬픔·이별(눈물) |
| photo | 기록·관찰(카메라+플래시) |
| sneeze | 먼지·꽃가루·감기(우주 제외) |
| clap | 공연·성공(박수) |
| magnify | 단서·조사(돋보기) |
| snooze | 지루함·긴 시간(Zz, 탄 채로) |
| dig | 발굴·화석(삽) |
| `SIMPLE_ACTS` 12종 | stretch·shrug·bow·nervous(땀)·flex·balance·listen(손을 귀에)·search(손차양)·yawn·write(연필)·wish(두 손 모음)·faint(별 도는 기절) |

**팔 축 (`tools/frog.py` 맨 위 ARM AXES 주석)**
- 회전축: 오른팔 어깨 (34,−22), 왼팔 (−34,−22).
- 오른팔 음수 회전은 팔을 밖·위로 올린다(wave·salute −118~−165). 양수는 몸 앞으로 돌린다(eat·yawn +160, clap +100~124, wish +142). 왼팔은 부호가 반대.
- 모든 팔 `fromTo`는 시작 상태에도 `svgOrigin`을 넣는다(없으면 팔이 날아간다).

#### D-2. 판정 순서 (오브젝트와의 관계)
쓰는 것: `tools/build/frog_place.py`의 `HIDEW`·`PEEKW`·`HANGW/HANGG`·`TAPW`·`RESTW`·`SCOPEW`·`PERSON`·`POPG`·`TRAVELG`… 정규식과 그림의 `mv-`/`id` 그룹 이름, 단위 번호.

1. hide → cry → facepalm → idea
2. peek → hang → tap → rest → scope
3. dig → magnify → read → photo → eat → dance → clap → salute → think → sneeze → snooze → 단순 동작
4. 사람 옆 wave
5. 탄 물체 반응: startle → lean
6. D 표의 상황 동작
7. 차분한 동작

- 제자리 동작이 정해지면 `roam`은 지운다.

#### E. 의상
단위 하나에 의상 하나. 단위 문장의 단어와 **그림 증거**(탑승 그룹 이름, 오브젝트 그룹 이름 + 화면 비율, 팔레트, 배경 종류)를 같이 본다. 배경 레이어(`mv-drift/cells/glint/twinkle…`, bg·sky·haze 이름)는 증거가 아니다.

**우선순위**: helmet / diver / goggles / fore → lab → explorer → scarf → nightcap → `OUTFIT_WORDS`(표 순서대로 첫 일치). 그림으로 판정한 물리 상태(scarf·umbrella·lifevest·helmet·diver)는 단어 의상(detective·beret…)보다 우선한다.

**기본 8종**

| 의상 | 상황 |
|---|---|
| `helmet` | 우주(`in_space()`, 아래) |
| `diver`(남색 슈트+공기통) | 깊고 어두운 바다 |
| `goggles` | 수면 가까운 물 |
| `fore` | 포레족·원주민 장면 |
| `lab`(흰 가운+고글) | 실험실·과학자·현미경 |
| `explorer`(탐험 모자+가방) | 탐험·정글·사막·동굴 |
| `scarf`(목도리, 입김) | 추위·얼음·눈 |
| `nightcap`(수면 모자) | 잠·꿈·밤 |

**단어 의상 56종 (`OUTFIT_WORDS`, 전체 64종)**
- 상황이 정해진 14종: crown(왕·여왕·왕국), wizard(마법·연금술), pirate(해적·보물, 우주 제외), chef(요리·부엌), hardhat(공사·광산·공학), headphones(소리·라디오·음악), knight(기사·성·갑옷), doctor(의사·병원·수술), gradcap(졸업·학교·대학), strawhat(농사·밭·여름), umbrella(비·폭풍), sunglasses(태양·사막·해변, 우주·바다 제외), partyhat(축하·생일), detective(탐정·단서·미스터리).
- `OUTFITS2` 41종: tophat·beret·cowboy·bandana·flowercrown·alien·bunny·santa·bowtie·cape·backpack·lifevest·raincoat·beanie·halo·ghost·viking·roman·samurai·headlamp·firefighter·police·aviator·monocle·glasses·medal·laurel·propcap·headband·vr·tinfoil·bandage·dino·shark·bee·clown·mustache·earmuffs·turtle·wings·crownleaf.
- 의상은 얼굴을 가리지 않아야 한다(의상 시트 `tools/frog.py` `outfit_markup`으로 확인).

**그림으로 판정하는 것**

| 판정 | 규칙 |
|---|---|
| 물속 `frog_place.underwater()` | 바다 생물·잠수정을 탔거나(shark·whale·fish·jelly·sub…), 팔레트 `ocean`, 물 그룹(water·sea·wave·lake·river·pool…)이 화면의 1/4 이상, 또는 바다 단어 |
| 깊음 → `diver` | `DEEP` 단어, 바다 생물 탑승, ocean 팔레트 |
| 수면 → `goggles` | surface·shallow·beach·boat… |
| 물속이면 | 단어 의상(shark·doctor…) 대신 잠수 장비(포레족 `huts` 장면만 예외) |
| 헬멧 `in_space()` | 우주선·혜성 탑승, 또는 우주 팔레트(space·deepfield·solar·cosmic)에서 우주 단어나 큰 우주 오브젝트(planet·moon·galaxy·probe·rocket·sun·earth… ≥ 6%)가 있을 때 |
| 헬멧이 아닌 경우 | 종이 배경, 큰 실내·지상 그룹(room·desk·street·dome…)이 있을 때. 별 배경만으로는 아니다 |
| 바다 팔레트(`ocean`) 영상 | 우주 헬멧·`slide`를 쓰지 않는다 |

**`PIC_OUTFIT` 표 (우선순위순, 단어로 고른 의상이 없을 때 채움)**

| 의상 | 그림 증거 |
|---|---|
| scarf | snow·ice·glacier·igloo·penguin… ≥ 6% 또는 팔레트 ice(바다의 marine snow 제외) |
| umbrella | rain·storm·thundercloud ≥ 8% 또는 팔레트 storm |
| lifevest | boat·raft·canoe·ship·deck를 탔을 때 |
| lab | microscope·beaker·flask·petri… 또는 팔레트 lab |
| headlamp | cave·mine·tunnel ≥ 25% |
| explorer | jungle·desert·dune·tent·canyon·ruins·temple ≥ 20% |
| nightcap | bed·pillow·blanket·cradle |
| hardhat | crane·excavator·scaffold… |
| chef | pot·pan·stove·kitchen·oven |
| doctor | hospital·stethoscope·syringe·ambulance |
| strawhat | barn·tractor·wheat·haystack·farm |
| sunglasses | beach·palm·parasol |

**그림 증거 동작 5종 (약한 동작일 때만, D의 단어 규칙 다음)**

| 그림 증거 | 동작 |
|---|---|
| 얼음 그룹·ice 팔레트 | `shiver`(chilly) |
| 그려진 블랙홀·우물(`HOLE_G`, ≥ 6%, 타지 않았을 때) | `pull`(scared) |
| 큰 불·태양(≥ 8%) | `dizzy` |
| 물 그룹 ≥ 25%에 서 있음 | `waves` |
| 우주선·비행기·기차·썰매를 탐 | `wind`(squint) |

#### F. 표정·말풍선
**F-0. 표정 34종 (`tools/frog.py` `MOODS`·`face_js`)**

| 묶음 | 표정 |
|---|---|
| 기본 14종 | happy·surprised·curious·worried·proud·excited·scared·squint·sleepy·dizzy·sad·`love`(하트 눈: beautiful·favorite·adorable…)·`shock`(동그란 눈·입: suddenly·unbelievable·boom…)·`angry`(찡그림: war·attack·greed·stolen…) |
| 단어표 `MOODW` 20종(이 순서, 첫 일치) | wink(비밀·힌트)·laugh(웃긴·농담)·grin(맛있는·승리)·pout(불공평·거절)·bored(지루·기다림)·confused(이상한·역설)·determined(임무·끝까지)·smug(당연히·쉬운)·chilly(추위)·hot(폭염)·tearful(이별·눈물)·queasy(썩은·악취)·disgust(역겨운)·suspicious(거짓·숨김)·awe(거대·셀 수 없는)·mischief(몰래·장난)·hurt(아픔·물림)·starry(보물·마법)·blush(수줍음·칭찬)·cheeky(장난스러운) |

고르는 순서(`tools/build/frog_place.py`):
1. 문장 단어표 `MOODW`.
2. 없으면 기본 규칙(물음표=curious, 느낌표=excited, 숫자=surprised…).
3. 첫 문장이 기본 표정(happy·curious·surprised)이고 강한 동작이 없으면 그림으로:
   - 탄 그룹 이름 `RIDE_MOOD`: rocket·ship→determined, whale·giant·planet→awe, treasure·gold→starry, fire·lava→hot, ice·snow→chilly, skull·carcass→queasy.
   - 그다음 팔레트 `PAL_MOOD`: ice→chilly, desert→hot.

**F-1. 표정**
- 표정은 문장마다 상황대로 정한다. 같은 표정이 이어져도 억지로 바꾸지 않는다.
- 옆에 서 있는 개구리는 눈동자가 물체 쪽을 본다(`gaze`, `beside()`가 자동으로 둠).
- 양팔이 항상 보인다(가리키지 않으면 짧은 오른팔 `#fg<tag>_ra`).

**F-2. 말풍선 `frog.says`**
- 머리 위, 개구리를 따라감, 글자는 항상 똑바로, 영어만, 24자 이하. 외침은 떨림.
- 한 단위에 최대 하나(`huts`·`push` 예외). `"t":초`로 시각 지정.
- 상황별 단어 묶음(`POOL`)에서 그 동작을 쓸 때마다 다음 말로 돌려 쓴다(`frog_place.pick_word`). '연달아 금지' 고정 규칙은 없다: 같은 상황 단어가 다시 나오면 같은 말도 다시 나온다.
- 강한 상황은 항상, 나머지는 한 단위 걸러, 차분한 동작은 항상 말풍선을 단다.

**F-3. 무거운 주제 (`config.py`의 `FROG_TONE = 'serious'`)**
- excited/happy → curious.
- 환호·Yay·Tada·Wheee·Hop·Boing·Got it·moonhop·run을 뺀다.
- 놀이형 표정(`PLAYFUL`: laugh·grin·cheeky·mischief·smug·wink·blush·starry)을 쓰지 않는다.
- 그렇게 해서 할 일이 없어진 개구리는 `look` + "Hmm..."(worried).

#### G. 등장·퇴장·눈 깜빡임
- 칠판 개구리만 아래에서 폴짝 등장한다.
- 그림 개구리는 그 자리에서 나타난다: 탈 때는 오브젝트 뒤에서 살짝 올라오고(`peek`), 접촉 동작은 `cut`(I-7), 배경 개구리는 그 컷의 전환에 맞춘다(L-3).
- 단위 끝 0.3초 전에 부드럽게 사라진다(한 프레임에 뚝 끊기지 않게).
- 눈 깜빡임은 불규칙한 간격(가끔 두 번 연속).

#### H. 작업 순서
1. 그림 에이전트는 개구리를 그리거나 사이드카에 쓰지 않는다. 그림이 끝나면 `python3 tools/build/frog_place.py <slug>` → `build3.py`.
2. 자동 선택이 안 맞으면 사이드카 `frog`를 손으로 고치고 `"lock": true`(다시 돌려도 안 덮어씀). 문·책·구멍 좌표는 SVG에서 읽는다(눈대중 금지).
3. 확인: `SLUG=<slug> python3 tools/preview/frogshot.py out.png 초,초,...`로 개구리 단위 프레임을 보고, 글자·자막·초점을 가리는 컷을 고친다.
4. 예전 영상에 새 규칙만 적용: 최신 `render-pipeline`을 받고 `frog_place.py <slug>`(corefix 포함) → `build3.py`만 다시 돈다.

#### I. 관절 리그와 접촉 동작
코드 `tools/frog_rig.py`(규칙은 `tools/build/frog_place.py`). `tools/assets/ease_miyaBnc.json`은 CustomBounce 샘플로, 떨어지는 물체의 첫 착지 시각 계산에 쓴다.

**I-1. 리그**
- 관절 그룹: 다리 `_lgl`/`_lgr`(엉덩이 축), 팔 `_la`/`_ra`(어깨 축), 머리 `_hd`(목 축, 의상·눈물 포함), 발 축 `"0 6"`.
- 그룹 순서: `_tr`(이동) > `_rm`(구르기) > `_lf`(생기) > `_ac`(동작).
- 모든 축은 부모 좌표 `svgOrigin`, 모든 트윈은 메인 타임라인 절대 시각(탐색·구간 렌더 안전, 난수 없음).

**I-2. 생기 층 `_lf`(`life_js`)**
- 모든 개구리가 숨 쉬고(스케일), 무게를 옮기고, 머리를 조금 돌리고, 눈을 흘끗 보고, 발을 끌어 움직인다. 멈춰 있는 개구리는 없다.
- 동작이 그 부위를 쓰면 그 부분만 끈다(`nohead`·`nolegs`·`noscale`·`noeyes`). 표정이 바뀌는 시각·단어 시작 시각은 피한다(`avoid`).

**I-3. 팔다리가 붙은 기존 동작**

| 동작 | 팔다리 |
|---|---|
| 달리기·걷기 | 다리 주기 + 팔 흔들기 + 발걸음마다 눌림 |
| `moonhop`·`cheer` | 공중에서 다리 접기 |
| `swim`·`float`·`hang` | 발차기 |
| `wind`·`pull`·`push` | 버티는 자세 |
| `dance` | 다리 스텝 |

**I-4. 접촉 동작 25종(`CONTACT`)**
- 그림의 움직이는 오브젝트와 그 오브젝트의 시각에 맞춰 만난다(`build3.obj_timing` → `frog_rig.obj_span`, 시각은 I-6-2).
- `frog_place.contact_pick`이 **오브젝트 종류(`mv-` 이름) + 크기 + 문장 단어**로 첫 번째 맞는 것을 고른다. 큰 오브젝트부터 보고, 탈것·`ride` 그룹은 건너뛴다.
- 우주 장면에는 땅 개그가 없다. 무거운 주제(`SERIOUS`)에는 bonk·squish·dodge·somersault가 없다.

| 오브젝트(`mv-`) + 조건 | 동작 | 내용 | 말풍선 |
|---|---|---|---|
| `core-drop` 작은 것(≤260×220) + catch·grab·save 단어 | `catch` | 아래에서 두 팔 들고 받아 두 걸음 물러나 자랑 | Got it! |
| `core-drop` + 물(바다 팔레트·물 그룹 ≥20%) | `splash` | 옆에 서 있다가 물보라 6방울(`_sp0..5`) 맞고 몸 털기·닦기 | Splash! |
| `core-drop` + avoid·miss·escape·narrow·just in time·safe 단어 | `sidestep` | 아래에 있다가 올려다보고 마지막 순간 옆으로 폴짝 피함, 물체는 옆에 쿵, 이마 닦음 | Phew! |
| `core-drop` 큰 것(>260×220, anvil·boulder·rock·crate·weight·piano·safe·block·meteor·barrel·box·chest 이름) | `flattened` | 밑에 깔려 납작, 별, 앞으로 기어 나와 탄성 복원 | Oof! / Ow ow ow. |
| `core-drop` 그 밖(진지하지 않을 때) | `bonk` | 위에서 떨어지는 물건 아래 → 머리에 맞고(머리 눌림, 별 `_spk`) 뒤로 넘어짐, 물체는 옆으로 굴러 떨어짐, 앉아서 머리 문지름 | Bonk! / Ouch... |
| `topple`(높이 120~600, 양수 각도) | `squish` | 넘어지는 쪽 끝에 서 있다가 납작해졌다가(`scaleY .2`) 기어 나와 탄성 복원 | Oof! / Ow ow ow. |
| `rollby`·`slide` + chase·follow·escape 단어 또는 큰 것(h>240) | `chase` | 출발점 뒤에서 달려 쫓아가며 손 뻗고 헐떡임 | Wait! |
| `rollby`·`slide` 그 밖 | `dodge` | 경로 62% 지점에 서 있다가 지나가는 순간(`pass`) 높이만큼 뛰어넘고 뒤돌아봄 | Whoa! |
| `swing`·`pendulum` 높이 ≥250(추·철거 공), hang 단어 없음 | `knocked` | 추가 닿는 끝 지점(왼쪽, I-6-2)에 서 있다가 처음 닿는 순간 뒤로 나뒹굴고(별) 앉았다 일어남 | Bonk! |
| `swing`·`pendulum`(h ≥ 80) | `swingride` | 아래에 두 손으로 매달려 같은 위상으로 흔들림(다리·몸은 살짝 늦게) | Wheee! |
| `bouncing` 큰 것(폭 ≥120) + bounce·jump·spring·hop 단어 또는 `data-h` ≥80 | `trampoline` | 공 위에 타고(끝 쪽) 착지마다 눌렸다가 공보다 높이 튀어 오름, 다리 접고 팔 위로 | Boing! |
| `bouncing`(≤400) | `bumped` | 옆에 서서 착지마다 움찔 | Boing! |
| `rise`(≤320×300) + heavy·lift·carry 단어 | `lift` | 아래에서 두 팔로 받쳐 들고 무릎 떨림·땀 | Hnnng... |
| rope·chain·cable… 그룹(폭 ≥150) + pull·tug·haul 단어 | `tug` | 밧줄 옆에서 세 번 당기다 놓쳐 넘어짐 | Hnnng... / Oof! |
| wind·gust·storm 단어(탑승·우주 아님) | `blown` | 바람 반대로 버티다(`_wd` 바람 줄) 밀려 구르고 앉음 | Whoaaa! |
| 배경 `run`/`walk` 경로 위 낮은 그룹(rock·root·log·puddle… ≤80 높이) | `trip` | 달리다 걸려 넘어지고(별) 일어나 절뚝임 | Oof! |
| `slam`·`squash`(쾅 찍히는 것 ≤500) | `shockwave` | 옆에 있다가 쿵 하는 순간 팔다리 허우적대며 튀어 올랐다 눌리며 착지 | Yikes! |
| `magnet`(`data-dx` ≥120) | `magnetized` | 물체를 잡고 있다가 같은 이징으로 뒤꿈치로 끌려감(뒤에 줄), 어질 | Whoa-oa! |
| `hop`(작은 생물 ≤260) | `hopalong` | 옆에서 같은 박자로 같이 깡총 | Hop hop! |
| `drip`(`data-fall` ≥80) | `dripped` | 물방울 떨어지는 자리 아래: 방울마다 머리 움찔·뿌루퉁, 손으로 가리고, 세 번째에 올려다보며 째려봄 | Drip... |
| `spin` 바퀴(wheel·gear·cog·fan·windmill·ferris·turntable·carousel·propeller… 160~600) | `rimride` | 바퀴 테두리에 매달려 함께 한 바퀴(그룹 밖에서 중심 기준 공전), 한 바퀴 뒤 어질·별 | 없음 |
| `popin`(≤320) | `launched` | 튀어나오는 자리에 서 있다가 그 위로 들려 올라가 팔 허우적, 위에 앉아 다리 흔듦 | Whoa! |
| `unroll`(폭 ≥400 카펫·두루마리) | `unrolled` | 펼쳐지는 길 위 70% 지점: 끝이 닿는 순간 휩쓸려 벌렁 넘어짐(별), 일어남 | Whoa! |
| `ascend`(≤320 풍선·등불) | `balloonride` | 아래에 두 손으로 매달려 다리 발장구 | Up, up! |
| `sink`(120~500 뗏목·배) | `sinkride` | 끝 쪽에 서서 두 팔 흔들며 도움 요청, 같이 가라앉음 | Help! |

같은 오브젝트 종류 안의 정확한 판정 순서는 `frog_place.contact_pick` 코드가 기준이다.

**I-5. 이동 동작 10종(`LOCO`, `loco_pick`, 단어 + 필요한 그룹)**

| 단어 + 그림 | 동작 |
|---|---|
| swim·paddle + 물 | `swimstroke`(평영. 잠수 의상이면 둥둥 떠 있는 단위마다 번갈아) |
| climb + rope·pole·tree·ladder·cliff 그룹(높이 ≥200) | `climb`(그 옆을 기어오름) |
| leap·jump over·gap(우주 아님) | `leap` |
| slip·let go·cling + 매달릴 그룹 | `dangle`(매달렸다 떨어짐, "Uh-oh... / Oof!") |
| skate·glide·slippery·sled | `skate`(목도리) |
| somersault·flip·acrobat·trick | `somersault` |
| sneak·tiptoe·quietly | `tiptoe` |
| crawl·tunnel·squeeze | `crawl` |
| 배경 `roll` | `logroll`(통나무 구르기) |
| tightrope·balance·narrow beam + 가로 긴 그룹(≥300×≤80) | `tightrope`(그 위를 건넘) |

**I-6. 의상 동작 38종(`COSTUME_ACTS`, `OUTFIT_ACT`, `costume_pick`)**
다른 규칙이 약한 동작만 남겼을 때 입은 의상이 동작을 정한다. 말풍선은 `OUTFIT_SAYS`(Abracadabra! / Chaaarge! / Yeehaw! …).

| 의상 | 동작 | 의상 | 동작 |
|---|---|---|---|
| wizard | castspell | knight·viking·roman·samurai | charge |
| chef | stir | firefighter | hose |
| cowboy | lasso | wings·bee·aviator | flap |
| bunny | bunnyhop | headphones | groove |
| hardhat | hammer | strawhat | sow |
| sunglasses | cool | santa | hohoho |
| ghost | floatghost | shark | chomp |
| dino | stomp | headband | jog |
| police | halt | medal·laurel | victory |
| vr | vrgrab | backpack·explorer | hike |
| lifevest | paddle | raincoat | puddlejump |
| scarf·beanie | rubhands | crown·tophat·monocle·bowtie | regal |
| alien | alienwave | mustache | mustache |
| earmuffs | coverears | bandage | limp |
| flowercrown·crownleaf | sniff | beret | paint |
| umbrella | windbrella | clown·partyhat | juggle |
| turtle | hideshell | halo | pray |
| gradcap | tosscap | headlamp | dig2 |
| propcap | stretchlegs | diver·goggles | swimstroke |

기존 동작으로 가는 의상: pirate→scope, detective·doctor·lab→magnify, glasses→think, nightcap→snooze, helmet→float, cape→fly, tinfoil→look.

**I-6-1. 팔 굽힘 (자동)**
- 쉬는 팔은 바깥으로 굽은 `( O )` 모양이다. 어깨에서 그대로 돌리면 머리 위에서 안쪽으로 꺾여 보이므로 굽힘을 뒤집는다.
- `frog_rig.arm_bend_pass`가 모든 팔 회전 트윈(`_la`·`_ra`의 `to`·`set`·`fromTo`)에 같은 시간·이징·yoyo의 경로 `d` 트윈을 덧붙인다. |각도| 55° 이하는 바깥 굽음, 125° 이상은 안쪽 굽음(머리 위에서 `\ o /`), 사이는 보간.
- 모든 동작에 자동 적용된다.

**I-6-2. 그림자·접촉 시각**
1. 바닥 그림자 `_sh`: `frog_rig.shadow_follow_pass`가 `_tr`의 모든 가로 이동 트윈을 복사해 따라간다. 점프(y)는 복사하지 않아 바닥에 남는다.
2. 접촉 시각: `frog_rig.obj_span`이 종류마다 `motions.obj_js`와 같은 숫자로 계산한다.
   - drop `.15/.9`, topple `.55`, rollby `.3/3`, slide `.3/.7`, rise `.3/.5`, slam `.28`, squash `.1`, popin `.45`, unroll `dur`, magnet `dur`, hop `per`, drip `per`. 모두 `data-delay` 기본 `.3`.
   - 튀는 공·그네·추·회전·상승·침강은 전환 시각 `v0`부터. 튀는 공은 CustomBounce 착지마다.
   - **새 종류를 쓰면 반드시 `obj_span`에도 넣는다**(안 넣으면 기본 0.3초로 어긋난다).
3. SVG 회전은 시계 방향이라 추·그네의 첫 극점(+amp)은 **왼쪽**이다. `knocked` 개구리는 왼쪽에 선다.
4. 접촉 개구리는 전부 `enter: cut`(코드가 강제).
5. 점검: 합성 페이지에서 충돌 순간 ±0.3초 프레임(`frog_rig.HITS`에 동작별 핵심 시각)을 시트로 본다.

**I-7. 우선순위**
D의 단어 규칙(강한 동작) → 접촉(`contact_pick`) → 이동(`loco_pick`) → 배경 이동 변형(trip·logroll) → 의상(`costume_pick`) → 맥동 반응(L-2)·개념 풀(K) → 차분한 기본 동작.
- 접촉 개구리는 오브젝트가 움직이기 전에 그 자리에 있어야 하므로 `enter: cut`(단위 시작 0.02초)으로 바로 나타난다.

**I-8. 사이드카**
`frog.act = {"type": "bonk", "obj": "<그룹 id>"}`. 손으로 고칠 수 있는 키: `type`, `obj`(접촉 대상), `pass`(dodge 통과 시각), `dist`(이동 거리), `frac`(trip 위치), `drop`(dangle 낙하), `h`(dodge 높이). `lock: true`로 고정한다.

**I-9. 그림 에이전트가 할 일 (art_spec 7·12)**
- 개그가 생기려면 그림에 작은 소품이 **움직여야** 한다. 이름 없는 그룹은 아무 규칙에도 안 걸린다. 개구리는 그리지 않는다.
- `mv-core-drop`은 그려진 자리 160px 위에서 떨어져 그려진 자리에 멈춘다. 나무에서 열매가 떨어지는 그림이 되지는 않으므로 '위에서 무언가 떨어짐'으로 쓴다(사과·나무일 필요 없음).
- 대본 규칙과 그림 규칙이 같은 단어를 본다. 그림 에이전트는 아래 표로 소품을 넣고, 개구리 쪽 단어 규칙(`frog_place`)이 같은 단어로 동작을 고른다.

| 대본 단어 | 소품 |
|---|---|
| fall·drop | `mv-core-drop`(위에서 떨어지는 작은 물건) |
| topple | `mv-topple`(넘어지는 기둥·표지판) |
| roll | `mv-rollby`(굴러가는 바퀴·공) |
| bounce | `mv-bouncing`(튀는 공) |
| swing | `mv-swing`(흔들리는 그네·추) |
| slam | `mv-slam` |
| magnet | `mv-magnet` |
| hop | `mv-hop` |
| drip | `mv-drip` |
| wheel | `mv-spin` |
| pop up | `mv-popin` |
| unroll | `mv-unroll` |
| rise | `mv-ascend` |
| sink | `mv-sink` |
| lift | `mv-rise`(떠오르는 상자) |
| rope | rope 그룹(밧줄·장대·사다리·나무·줄은 rope·pole·ladder·tree·wire 이름) |

**I-10. 확인 상태**
- 확인: 합성 페이지 45장면(접촉 25·이동 10·의상 38) 전체 탐색 JS 오류 0, whale-fall-short1 전체 빌드 오류 0(`frog-rules/rig-2026-10-29/` 시트·mp4).
- 미확인: Actions 렌더와 실제 영상의 접촉 장면.

#### J. 빨려듦(pull) 횟수 제한
- 빨려드는 동작은 대본에 블랙홀·소용돌이·배수구 등 진짜 빨려드는 말이 있을 때만 쓴다(`swell`은 구멍이 아니다, `HOLE` 정규식 `(?<!s)well\b`).
- `frog_place.py`가 영상마다 롱폼 최대 3번(25단위 이상 간격), 숏츠 최대 1번으로 제한한다. 넘는 것은 놀란 표정(`look`)으로 바꾼다.

#### K. 개념 규칙·테마 팩·최소 사용 선택
두 번째 층이다. 쓰는 때: ① 단어 규칙(D)·접촉(I)·이동·의상 동작이 모두 빗나가 개구리가 차분한 기본 동작으로 남을 때 ② 같은 강한 단어 동작이 한 영상에서 거듭될 때. 코드 `tools/concepts.py`, 적용 `frog_place.py`(`concept_apply`·`VARIANTS`·`pack_accessory`).

**K-1. 개념 25종 (모든 영역 공통)**
- 문장을 정규식으로 분류한다: scale(크기 비교)·timespan(긴 시간)·expansion·lightspeed·gravity·cold_empty·observe·unknown·birth·death·journey·danger·discovery·counting·change·speed·slowness·hidden·giant_tiny·home_safe·signal·heat·food·build·celebrate.
- 문장에서 먼저 나온 개념이 우선.
- 개념마다 공통(`*`) 동작 풀 3~5개가 있고(예: scale → measure·shrinkdown·growtall·binocs·peer), 영역별 변형 풀 113개가 덮어쓴다(예: scale/sea → "Whale-sized!" measure, scale/body → "Cell-sized!" shrinkdown).
- 개념이 없으면 영역 채움 풀(`DOMAIN_FILLER`).

**K-2. 영역(테마 팩) 9종**: space·sea·history·body·bio·time·earth·tech·generic.
- 영상 영역: 전체 대본 단어 + 팔레트(`video_domain`, 빌드 로그 `theme pack:`).
- 단위 영역: 그 문장에 단어가 2개 이상이면 자기 것, 아니면 그림 태그 → 팔레트 → 영상 영역(`unit_domain`).
- 팩이 주는 것: 동작 풀 변형, 의상 소품(아래), 그림 규칙(소품·모션·구도, art_spec 7B).

| 영역 | 의상 소품(각 풀에 '없음'도 한 자리) |
|---|---|
| space | 헬멧 위 jetpack·moonboots·goldvisor·antenna·patch |
| sea | flippers·sailorhat·lifering·captainhat·shellhat |
| history | toga·shield·turban·feathercap·crown·knight·laurel·tophat·monocle |
| body | doctor·lab·facemask·glasses·headlamp |
| bio | leafhat·explorer·bee·flowercrown·backpack·strawhat |
| time | clockhat·pocketwatch·nightcap·glasses·tophat |
| earth | explorer·raincoat·scarf·sunglasses·hardhat·headlamp |
| tech | hardhat·goggles·vr·headphones·tinfoil·glasses |
| generic | cap·bowler·bowtie·beanie·glasses·headband |

- 우주 소품은 헬멧을 쓴 개구리에게만(우주 문장이라도 땅 그림이면 generic 팩).
- 잠수복에는 flippers·patch만.
- 모자 위에 모자 없음(`HATS`·`SUITS` 호환표).

**K-3. 최소 사용 선택(`concepts.Tally`)**
- 풀에서 고를 때는 이 영상에서 지금까지 가장 적게 쓴 것을 고르고, 동률이면 단위 번호로 정한다. 무작위 없음.
- 동작(`act`)과 의상(`outfit`)을 따로 센다.
- 탑승 중이면 이동형 동작을 풀에서 빼고, 무거운 주제(`FROG_TONE serious`)면 환호형을 뺀다.

**K-4. 강한 단어 동작의 변형 (최소 사용으로 고름)**

| D가 고른 동작 | 변형 풀 |
|---|---|
| wind(탈것·속도) | wind·leanback·pointfar·helmetwipe(우주만)·binocs |
| shiver(추위·공포) | shiver·hug·rubhands·duck |
| awe(거대함) | awe·gasp·shrinkdown·measure·leanback |
| pull(블랙홀) | pull(2자리)·leanback·pushaway·duck |
| 탈것 탑승의 wind | 탑승 자세 6가지 순환: wind·pointfar·salute·binocs·leanback·wavebig |

**K-5. 개념 동작 34종(`frog_rig.CONCEPT_ACTS`, generic_js 데이터)**
zerogroll(무중력 공중제비, `_rm` 회전)·jetpack(불꽃 뿜으며 떠오름, 제트팩 소품 자동)·moonbounce·plantflag(깃발 소품 `_fg`, 팔에 맞춰 세워 그림)·starcatch·pushoff·helmetwipe·countstars·magnetwalk·sunshade·measure·shrinkdown·growtall·stretchwide·speedrun·slowwalk·peer·binocs·present·countfingers·hug·gasp·chinrub·pacing·oldman·leanback·pushaway·pointfar·spinaround(제자리 돌기, scaleX 반전)·duck·cupshout·wavebig·fan·rubbelly.
- 말풍선은 풀의 세 번째 값(없으면 `OUTFIT_SAYS`).

**K-6. 다양성 검사(`tools/check/variety_check.py`, 15-8·4-10)**

| 항목 | 기준 |
|---|---|
| 최다 동작 | ≤ 40 % |
| 동작 종류(개구리 20마리 이상일 때) | ≥ 8종 |
| 의상 조합 | ≥ 4 |
| 첫 표정 | ≥ 4 |
| 오브젝트 모션 종류(롱폼) | ≥ 8 |
| 움직이는 소품 그림 | ≥ 1/6(경고만) |
| 맥동 오브젝트 탑승(L-1) | 0 |
| 센터 모션 사건 종류(4-13) | 종류별 ≤ 15 % |

- `final_check.py`가 돌리고 실패하면 `.checked`를 내지 않는다.
- 확인: 합성 54장면(새 동작 34 + 소품 의상 20) JS 오류 0, 깃발·제트팩·공중제비 프레임 눈으로 확인. 미확인: Actions 렌더, 실제 영상에서의 보임새.

#### L. 맥동 오브젝트 옆에서 반응, 카메라·전환·배경 효과 연동
**L-1. 맥동하는 것은 타지 않는다**
- 탑승 가능 그룹(`frog_place.OK`): `mv-core-sway|glide|approach|drop`, `mv-path`, `mv-slide`, `mv-swing`뿐이다.
- 이유: 개구리가 그룹 안에 들어가면 그 그룹의 배율·흔들림을 그대로 물려받아 같이 두근거린다.
- 에이전트 사이드카의 `ride`도 같은 검사를 거친다(맥동 그룹이면 버림).

**L-2. 반응 동작(`pulse_response`, `frog_rig.RESPONSE_ACTS`)**
조건: 단어 동작(STRONG·ACTIVE·ROLL)이 없고, 그림에 맥동 센터(`mv-core-heartbeat|swell|tremble|wobble|ping|squeeze|pop|stamp`, 120×80 px 이상, corefix 뒤라 이유가 있는 것)가 있을 때. 가장 큰 것 **옆**(`beside`)에 서서 그 리듬에 맞춰 반응한다. 말풍선은 동작 고정('Thump... thump.', 'Whoa, it grows!', 'Steady...!').

| 센터 모션 | 반응 |
|---|---|
| heartbeat | `heartlisten`(귀에 손, 1.6초) |
| swell | `backstep`(커질 때 물러남, 2.2초) |
| tremble | `bracehold`(팔 벌려 버팀) |
| wobble | `steadyit`(두 손으로 잡아 줌) |
| ping | `listen` |
| squeeze·stamp | `duck` |
| pop | `startle` |

**L-2-1. 반응 동작은 실루엣이 서로 달라야 한다**
- 한 풀에서 번갈아 나오는 동작은 팔 각도·머리·다리 중 하나가 눈에 띄게 달라야 한다.
- heartlisten은 손을 귀 옆(`ra` −158. −135는 "팔을 오브젝트 쪽으로 뻗음"으로 읽힌다), backstep은 두 팔을 뒤로(+25/−25)하고 물러남, steadyit은 먼 팔이 가슴을 가로질러(−125~−135) 두 손이 오브젝트 쪽.
- `python3 tools/frog_rig.py --check`가 같은 풀 안에서 팔 각도가 15° 안에 겹치고 다리·머리도 같은 쌍을 적는다(경고).
- 데모 영상을 뽑을 때 장면 0초는 캡처하지 않는다(`tl.set` 적용 전이라 첫 프레임 결함).

**L-3. 카메라·전환·배경 효과 연동(`frog.enter_js`·`frog.cam_js`)**
`build3`가 단위마다 `cam=`(이 컷 전환·다음 컷 전환·포커스 줌·배경 효과·추적 카메라·바람 방향)을 넘긴다. 배경 개구리(탑승·접촉 동작 아님)에 전부 자동으로 붙는다.

| 등장 = 이 컷의 전환 | 등장 방식 |
|---|---|
| slide·whip | `skid`(옆에서 미끄러져 들어와 기울었다 섬) |
| push | `drop`(위에서 떨어져 스쿼시) |
| zoom·match·iris | `pop`(발에서 자라남) |
| eye | `blink`(세로로 열림) |
| tilt | `tiltin`(카드처럼 기울어 들어옴) |
| wipe·seam·diamond·zigzag·wave·page·blinds·fade·wash·hard | 부드러운 fade |
| 접촉 동작 / 탑승 | `cut` / `peek` |

- 사이드카 `enter`가 있으면 그것이 우선.

| 퇴장 = 다음 컷의 전환(2.2초 이상 머물고 고요 동작일 때) | 퇴장 방식 |
|---|---|
| zoom | 움츠림(scaleY .9) |
| slide·whip | 그림이 나가는 쪽(왼쪽)으로 기울임 |
| push | 위를 올려다봄 |

- **포커스 줌**(`focus`): 줌 시작 시각에 눈동자·머리가 포커스 쪽으로 향했다가 2초 뒤 돌아온다(가리키는 개구리·탑승 제외).
- **추적 카메라**(`track_spec`): 그 그림의 약한 동작 개구리는 이동 방향으로 `jog`/`hike`(bio·history·earth)한다(`track_dir`).

| 배경 효과(고요 동작일 때) | 반응 |
|---|---|
| flash·bolt·shockwave·burst·starburst | 그 시각에 움찔(`miyaWig`)하며 `shock` 표정, 1.5초 뒤 원래 표정 |
| rain·snow·hail·ash·leaves·petals·meteors·droplets·confetti·feathers | 올려다봄 |
| windlines·sand | 바람을 거슬러 기울임(`motions.dir_sign`) |

**L-4. 고요 동작 목록(`frog.CAM_CALM`)**
없음·breathe·sway·look·nod·rest·tilt·sleepy·think·read·listen·tapfoot·armsfold·squintfar·sniffair·lookup·float·awe일 때만 퇴장·포커스·효과 반응이 붙는다(강한 동작은 몸을 쓰고 있어 겹치지 않게).

**L-5. 반응·카메라 동작 27종(generic_js 데이터)**
- 반응 12: heartlisten·backstep·bracehold·steadyit·lookup·holdhat·tapfoot·squintfar·kneel·sniffair·stepaside·armsfold.
- 카메라·개념 풀 15(`frog_rig.CAMERA_ACTS`): leanin·crouchlook·backaway·scratchhead·hugself·headshake·nodyes·stompfoot·wavebye·shrugbig·swingarms·bowhead·peekover·tiptoeback·rockheels.
- 개념 풀(K)의 danger·hidden·discovery·unknown·cold_empty·change·observe·home_safe·celebrate·slowness·signal·build·journey·counting·timespan 공통 풀에 하나씩 들어가 최소 사용으로 돌아간다.

**L-6. 검사**
- `variety_check.py`(K-6, 15-8): 맥동 오브젝트 탑승 0, 센터 모션 사건 종류 ≤ 15 %(4-13).
- 확인: 합성 59장면 JS 오류 0(새 동작 27, 전환별 등장 9, 퇴장 3, 포커스, 효과 반응 3), kardashev-scale 재배치 뒤 탑승 맥동 0, whale-fall 숏츠 전체 빌드 0 오류. 미확인: Actions 렌더.

---

### 개정 이력
- 2026-10-24: 노트 개구리 도입. 2026-10-25 (miya): 설명·가리키기는 칠판에서만, 그림 장면은 곁 캐릭터. 모든 장면에서 상황별 표정·동작.
- 2026-10-26 (miya): 이유 있는 개구리만(B). 정리본(구석 앉기·모든 그림 개구리 폴짝 등장·바람 줄 삭제). 검토 반영: 중앙 위 걸터앉기 금지, 글자 겹침 회피, 바다 영상 헬멧·slide 금지(고래 영상에 헬멧, 가라앉는 고래 사체에 "Wheee!"), 부드러운 등장·퇴장, 불규칙 깜빡임.
- 2026-10-26 2차 검토(4편 122장면): 안전 구역(자막을 밟는 개구리가 가장 많았음), 이동 오브젝트는 중앙 쪽, 작은 오브젝트는 옆, 구멍 위 금지, slide는 구덩이가 그려진 그림에서만.
- 2026-10-26 3차 (miya): 관계 동작 10종·의상 4종·표정 3종·시선, 판정 순서(D-2).
- 2026-10-26 4차 (miya: "의상·동작 50개씩", "표정도 늘려줘"): 동작 56종, 의상 64종, 표정 34종, 팔 회전축 규칙(clap·wish에서 팔이 날아가던 것 수정).
- 2026-10-27 (miya): 말풍선 '연달아 금지'·표정 강제 변경 제거(한 영상에 AAAAAH! 10번 문제는 단어 묶음 돌려 쓰기로). 잠수 장비는 그림으로도 판정(상어를 탄 개구리가 잠수복 없이 나옴). 의상·동작 전부 단어 + 그림 증거("다른 것들에도 모두").
- 2026-10-29 (miya: "개구리가 너무 정적", "접촉이 재밌는 포인트"): I절. 관절 리그·생기 층, 접촉 12 → 25종, 이동 10, 의상 38. 팔 굽힘 자동 반전(머리 위에서 `) O (`로 꺾임). 그림자 따라가기·접촉 시각·추 위치(왼쪽) 수정. 떨어지는 물건은 사과가 아니어도 됨. 대본 단어 → 소품 표.
- 2026-10-29~30: `shiver`를 트윈 하나로. CustomWiggle 금지 뒤에는 빌드가 `miyaW`로 바꿈(15-8).
- 2026-10-30 (miya): pull 횟수 제한(J).
- 2026-10-31 (miya: "우주는 항상 비슷한 것만 나온다 … 다양성과 재미성이 중요"): K절. 옛 영상 5편 재배치 결과 동작 종류 19~37(전엔 약 12), 의상 조합 11~25.
- 2026-11-05 (miya: "두근거리는 모션이 너무 자주, 개구리가 붙어서 같이 두근거림 … 카메라·오브젝트·전환에 따라 유동적으로"): L절. `PULSEG → bounce`(탄 것과 같이 출렁) 규칙 삭제. 같은 날 데모 검토로 L-2-1(같은 동작이 반복돼 보임).
- 2026-11-14 (miya): 문서 유지 규칙 형식으로 정리(현재 규칙만, 이력은 여기). 절 순서를 A~L로 맞추고 C-4를 C-2-1 ⑥에 합침. I-4 표에서 같은 오브젝트 종류의 행을 모음.
