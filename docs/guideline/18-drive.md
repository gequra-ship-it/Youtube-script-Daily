## 18. 저장 위치 (Google Drive, 영상별 폴더)

- **Miya's Note 새 채널 (2026-10-24 사용자 결정, 기존 영상과 섞이면 확인이 어려워서)**: 새 영상은 모두 `Video & Thumbnail /` 아래 **`Miya's Note/NN_<슬러그>/`**(NN은 이 폴더 안 두 자리 순서, 01부터, 주제 구분 없음). 숏츠 5편은 `Miya's Note/NN_<슬러그>/short/`(`<슬러그>-short1~5`). `render/<슬러그>/.dest`를 `Miya's Note/NN_<슬러그>`(숏츠 `/short`)로 둔다. 아래 `Space & Science`·`Life & Biology`·`old`·`cinema`는 **옛 채널(Miya's Lab) 보관**이라 새 영상을 넣지 않는다. 폴더는 처음 올릴 때 Actions(rclone)가 만든다(미확인: 폴더 이름의 작은따옴표가 rclone 경로에서 문제없는지는 첫 업로드에서 확인).
- **위치 (2026-10-16 사용자 결정)**: `유튜브 자동화 / Video & Thumbnail /` 아래 네 폴더.
  - `Space & Science/NN_<슬러그>/` — 우주·과학 새 영상. NN은 이 폴더 안 두 자리 순서(01부터). 숏츠는 `short/`.
  - `Life & Biology/NN_<슬러그>/` — 생명·생물학 새 영상. 번호는 따로 01부터. 숏츠는 `short/`.
  - `old/<영상>/` — 2026-10-16 이전 SVG 영상 보관(번호 없음).
  - `cinema/<영상>/` — 3D 실험 보관(`cosmic-prison-cine`, `_ci-test`).
- 새 영상의 `render/<슬러그>/.dest`는 `Space & Science/NN_<슬러그>` 또는 `Life & Biology/NN_<슬러그>`(숏츠 `/short`). 예전 영상은 `.dest`가 `old/<영상>`이라 다시 렌더하면 보관본을 덮어쓴다. 고친 예전 영상을 새 작업으로 올리면 주제 폴더 다음 번호로. **폴더 이름이 바뀌면 `.dest`도 바꾼다**(안 그러면 새 폴더가 생긴다).
- 영상마다 폴더 하나(루트에 파일 금지, 다른 영상 파일이 섞이지 않게 확인). 안의 파일은 모두 같은 슬러그로 시작: `<slug>.mp4`, `_thumbnail_A/B/C.png`, `_script.txt`, `_metadata.txt`, `_render_report.txt`, 그리고 `short/`에 `<slug>-short1~5`의 `.mp4`·`_script.txt`·`_metadata.txt`·`_render_report.txt`.
- **올리는 방법**: 모두 Actions가 올린다(15-5). Drive 커넥터 파일 업로드(base64)는 쓰지 않는다(폴더 생성·목록 확인은 됨). PC가 연결된 세션은 동기화 폴더 `G:\내 드라이브\유튜브 자동화\Video & Thumbnail\<폴더>\`에서 목록·리포트를 읽을 수 있다(승인 필요).
