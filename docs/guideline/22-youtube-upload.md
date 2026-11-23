## 22. YouTube 업로드 (miya OK 뒤 비공개 예약)

> 최종 수정: 2026-11-22 · 본문은 지금 유효한 규칙만 담는다. 바뀐 경위는 맨 아래 개정 이력.

### 22-1. 흐름
1. 렌더가 Drive에 올라가면(15-5) miya에게 알린다(21-4). **이때까지 YouTube에는 아무것도 올라가지 않는다.**
2. miya가 Drive의 영상을 확인하고 OK(통과)를 준다.
3. OK를 받은 뒤에만 `render/.upload`에 **롱폼 슬러그 한 줄**을 넣고 `render-pipeline`에 푸시한다(숏츠 `<슬러그>-short1~5`는 같이 올라간다).
4. `youtube-upload.yml`이 `tools/check/title_unique.py`로 제목을 점검한 뒤 `tools/publish/yt_upload.py`로 올린다. Actions에서 `youtube-upload`를 수동 실행해도 된다(입력 `slugs`).

| 파일 | 뜻 |
|---|---|
| `render/.upload`의 `<롱폼 슬러그>` | 그 영상(롱폼 + 숏츠)을 YouTube에 올린다. 푸시하면 바로 시작한다(되돌리기 어려움: 올라간 영상은 Studio에서 지운다) |
| `#`으로 시작하는 줄 | 무시. 슬러그 줄이 없으면 아무것도 하지 않는다 |
| `.github/workflows/youtube-upload.yml` | 워크플로 자체. 고치는 푸시도 `.upload`의 줄을 전부 실행한다 |

- 줄은 다시 실행해도 안전하다(채널에 같은 제목이 있으면 건너뜀). 끝난 영상의 줄은 지워도 되고 남겨도 된다.
- `render/.chunked`와 별개다. 렌더 푸시만으로는 업로드되지 않고, `.upload` 푸시만으로는 렌더되지 않는다.

### 22-2. 올릴 때 정해지는 값 (채널에 miya가 올려 온 방식)

| 항목 | 규칙 |
|---|---|
| 공개 상태 | 항상 비공개 + 예약(`publishAt`). 공개는 YouTube가 예약 시각에 한다 |
| 예약 시각(KST) | 화·목·토·일. 롱폼 07:00, 숏츠 08:00·08:30·09:00·09:30·10:00. 채널의 마지막 예약일 다음 날부터, 영상 하나가 하루를 쓴다 |
| 순서 | Life / Space를 번갈아 배치(마지막 예약 롱폼과 반대 분류부터). 같은 분류 안에서는 Drive 폴더 번호 순 |
| 분류 | Drive 폴더 `01.`=Life, `02.`=Space(`.dest`) |
| 재생목록 | 롱폼 `Deep Dives …`, 숏츠 `Bite-Sized Knowledge …`. 이름에 Life/Space가 든 목록을 찾는다 |
| 설정 | 카테고리 27, 언어 en, 아동용 아님, 퍼가기·통계 공개, 라이선스 youtube |
| 태그·해시태그 | 태그 = `Miya's Note` + 설명의 해시태그(최대 8). 파일의 `#MiyasNote`는 `#Miya's Note`로 바꿔 올린다 |
| 설명란 | `<` `>` 제거, 4,900바이트 이하로 자른다(YouTube가 `invalidDescription`으로 거절) |
| 숏츠 썸네일 | `*_thumbnail_A.png`를 YouTube 처리가 끝난 뒤 설정한다(업로드 직후에 올리면 덮어써진다) |
| **miya가 Studio에서** | 롱폼 썸네일(A/B/C 중 선택, 17-3 업로드 기록), 종료 화면(구독 + 추천 영상, 마지막 약 10초). 숏츠는 종료 화면 없음 |

### 22-3. 올리기 전 점검
- `python3 tools/check/title_unique.py <롱폼 슬러그>`: 이 영상의 제목이 **다른 영상(롱폼·숏츠 모두)과 같지 않은지**, 제목 100자 이하, 설명 4,900바이트 이하를 본다. 워크플로가 업로드 전에 같은 점검을 하고, 걸리면 올리지 않고 멈춘다.
- 제목을 바꿔 다시 만든 영상은 옛 제목과 달라 중복으로 보이지 않는다. **옛 예약 영상은 Studio에서 먼저 지운다**(자동 삭제 없음).
- 하루 API 한도(10,000단위, 태평양 시간 자정 = 한국 시간 약 오후 5시에 초기화)를 넘으면(403/429) 중단한다. 같은 줄로 다시 실행하면 남은 것만 올라간다.
- 채널 상태(마지막 예약일, 재생목록)는 매번 YouTube에서 읽는다. 두 영상을 동시에 올려도 `concurrency`로 차례대로 돈다.

### 22-4. 도구와 비밀값
- Actions: `youtube-upload.yml` → `tools/publish/yt_upload.py`. 주간 통계 `yt-stats.yml` → `tools/publish/yt_stats.py`(`stats/yt_stats_<날짜>.csv`, 예약 실행은 기본 브랜치 `main`에서만 돈다. 트래픽 소스는 `yt_traffic_<날짜>.csv`, 노출수·CTR은 `yt_impressions_<날짜>.csv`에 시도한다(API가 거부하면 파일이 없다 → Studio에서 본다)).
- miya PC(`Desktop\miya's note`, 원본은 프로젝트 파일 `youtube-api/`): `upload_new.py`(Drive에만 있고 채널에 없는 영상 올리기: `python upload_new.py --skip=<폴더> --go`), `reupload.py`(다시 렌더한 영상으로 교체), `fix_thumbs.py`(숏츠 썸네일 재설정). 같은 규칙을 쓴다.
- 비밀값은 GitHub Actions secrets `YT_CLIENT_ID`·`YT_CLIENT_SECRET`·`YT_REFRESH_TOKEN`·`RCLONE_CONF`. **읽거나 출력하지 않는다.**

---

### 개정 이력
- 2026-11-20 (miya): 신설(렌더 뒤 자동 업로드 초안).
- 2026-11-22 (miya): 렌더 확인 → OK → `render/.upload`로 올리는 방식으로 확정. 분류 번갈아 배치, 설명란 `<` `>` 제거, 숏츠 썸네일은 처리 완료 뒤 설정, 제목 중복 점검(`title_unique.py`) 추가. 근거: 66개 교체 업로드 중 설명란 거절과 숏츠 썸네일 덮어쓰기, Drive 숏츠 제목이 다른 영상과 같아 중복으로 걸러진 일.
