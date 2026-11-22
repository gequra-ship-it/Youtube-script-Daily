# YouTube 자동 업로드 (miya OK 뒤, 비공개 예약)

> 최종 수정: 2026-11-22 (miya 요청). 이 파일은 `render-pipeline`에 먼저 넣고 `main`에 사본을 둔다.

순서: 대본 → 영상 제작 → 렌더(`render-chunked.yml`, Drive까지) → **miya가 Drive의 렌더를 확인하고 OK** → `render/.upload`에 롱폼 슬러그 한 줄을 넣고 푸시 → `youtube-upload.yml`이 `tools/publish/yt_upload.py`로 롱폼과 `<슬러그>-short1~5`를 올린다. 렌더만으로는 YouTube에 올라가지 않는다.

| 항목 | 규칙 |
|---|---|
| 시작 | miya OK 뒤 `render/.upload`에 `<롱폼 슬러그>` 줄 추가 후 푸시, 또는 Actions에서 `youtube-upload` 수동 실행 |
| 공개 상태 | 항상 비공개 + 예약(`publishAt`). 공개는 YouTube가 예약 시각에 한다 |
| 예약 시각(KST) | 화·목·토·일. 롱폼 07:00, 숏츠 08:00·08:30·09:00·09:30·10:00. 채널의 마지막 예약일 다음 날부터 |
| 순서 | Life / Space를 번갈아 배치(마지막 예약 롱폼과 반대 분류부터). 같은 분류 안에서는 Drive 폴더 번호 순 |
| 재생목록 | 롱폼 `Deep Dives - …`, 숏츠 `Bite-Sized Knowledge - …`. 이름에 Life/Space가 든 목록을 찾는다. Drive 폴더 `01.`=Life, `02.`=Space |
| 설정 | 카테고리 27, 언어 en, 아동용 아님, 퍼가기·통계 공개, 태그 = `Miya's Note` + 해시태그 |
| 설명란 | `#MiyasNote` → `#Miya's Note`, `<` `>` 제거, 4,900바이트 이하 |
| 썸네일 | 숏츠는 `*_thumbnail_A.png`를 YouTube 처리 완료 뒤 설정(업로드 직후에는 덮어써짐). **롱폼 썸네일과 종료 화면은 miya가 Studio에서 설정** |
| 중복 | 채널에 같은 제목이 있으면 건너뜀. 그래서 `.upload`의 줄은 다시 실행해도 안전하다 |
| 제목을 바꿔 다시 만든 영상 | 옛 제목과 다르면 중복으로 보이지 않는다. 옛 예약 영상은 Studio에서 먼저 지운다 |
| 비밀값 | GitHub Actions secrets `YT_CLIENT_ID`·`YT_CLIENT_SECRET`·`YT_REFRESH_TOKEN`(읽거나 출력하지 않음) |

- 하루 API 한도를 넘으면(403/429) 중단한다. 같은 줄로 다음 날 다시 실행하면 남은 것만 올라간다.
- 로컬 도구(miya PC, `Desktop\miya's note`): `upload_new.py`(Drive에만 있는 영상 올리기), `fix_thumbs.py`, `reupload.py`. 같은 규칙을 쓴다.

### 개정 이력
- 2026-11-20: 신설(렌더 뒤 자동 업로드).
- 2026-11-22: miya OK 뒤 `render/.upload`로 올리는 방식으로 변경, 분류 번갈아 배치, 설명란·썸네일 처리 보강.
