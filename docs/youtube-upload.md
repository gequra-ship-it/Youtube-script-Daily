# YouTube 자동 업로드 (비공개 예약)

> 최종 수정: 2026-11-20 (miya 요청). 이 파일은 `render-pipeline`에 먼저 넣고 `main`에 사본을 둔다.

렌더가 Drive에 올라간 뒤 `render-chunked.yml`의 `youtube` 작업이 `tools/publish/yt_upload.py`를 실행한다.

| 항목 | 규칙 |
|---|---|
| 공개 상태 | 항상 비공개 + 예약(`publishAt`). 공개는 YouTube가 예약 시각에 한다 |
| 예약 시각(KST) | 화·목·토·일. 롱폼 07:00, 숏츠 08:00·08:30·09:00·09:30·10:00. 채널의 마지막 예약일 다음 날부터 |
| 재생목록 | 롱폼 `Deep Dives - <분류>`, 숏츠 `Bite-Sized Knowledge - <분류>`. Drive 폴더 `01.`=Life & Biology, `02.`=Space & Science |
| 설정 | 카테고리 27, 언어 en, 아동용 아님, 퍼가기·통계 공개, 태그 = `Miya's Note` + 해시태그 |
| 해시태그 | `#Miya's Note #...` (metadata의 `#MiyasNote`를 바꿈) |
| 썸네일 | 숏츠는 `*_thumbnail_A.png`를 올림. **롱폼 썸네일과 엔딩 화면은 miya가 Studio에서 설정** |
| 중복 | 채널에 같은 제목이 있으면 건너뜀 |
| 실패 | 작업은 `continue-on-error`라 렌더·Drive 업로드에 영향 없음 |
| 비밀값 | GitHub Actions secrets `YT_CLIENT_ID`·`YT_CLIENT_SECRET`·`YT_REFRESH_TOKEN`(읽거나 출력하지 않음) |

- 렌더가 `<슬러그> 0`(deliver만)이면 올리지 않는다.
- 하루 API 한도(10,000단위)를 넘으면 중단하고, 남은 영상은 같은 슬러그로 렌더 작업을 `reuse_run`으로 다시 실행하면 이어진다(이미 올라간 제목은 건너뜀).
- 예약된 영상을 교체해야 하면 miya가 Studio에서 지운다(자동 삭제 없음).

### 개정 이력
- 2026-11-20: 신설.
