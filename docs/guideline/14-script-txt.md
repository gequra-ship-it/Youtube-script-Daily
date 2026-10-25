## 14. 대본 텍스트 파일 규격

- **(2026-10-24) 이 파일은 사용자에게 넘기지 않는다(17-4). 작업 폴더에만 만들어 확인용으로 쓴다.**
- 파일명 `<슬러그>_script.txt`, UTF-8.
- **머리말**(한국어 가능): 영어 제목, `Miya's Note · 내레이션 대본`, 실제 길이와 단어 수(음성 실측), 컷 수, TTS 설정(영어, 여성 1인 af_heart, -16.8 LUFS), 원문 대비 바뀐 점 한두 줄.
- **1부 TTS 입력 전문**: 영어 내레이션만, 장면당 한 문단, 빈 줄로 구분. 타임코드·메모·한글 없음.
- **2부 장면별 대본**:
  ```
  [S001] 00:00.0–00:11.6 (11.6s) 일러스트
  <영어 내레이션>
  효과음: rustle @00:06.0, pop @00:07.6
  ```
- **3부 자막 줄 분할**: 컷마다 자막 줄과 시작 시각(MP4 자막과 같음).
  ```
  [S001]
  00:00.0  Take a look at your fingernails
  00:03.1  They have been growing
  ```
- 내레이션은 HTML 애니메틱과 글자 하나까지 같게(따옴표·대시 포함).
- **TTS는 Kokoro(무료 로컬, Apache-2.0)**, 기본 속도 1.0. **4자리 연도는 `tools/tts.sh`가 `tools/tts_text.py`로 읽는 말로 바꿔 넣는다**(1990→nineteen ninety, 1900→nineteen hundred, 1905→nineteen oh five, 2000→two thousand, 2005→two thousand five, 2010→twenty ten, 1990s→nineteen nineties; 쉼표·소수·$·단위가 붙은 숫자는 그대로). 직접 `hyperframes tts`를 부를 때는 연도를 영어 단어로 써서 넣는다(안 그러면 'nineteen hundred ninety'로 읽는다). 문단별로 만들고 컷 길이·자막 시각은 실제 음성(`ffprobe`)과 단어 시간(21-5)으로 확정. 영상 단위는 `tools/tts.sh`(21-2). 한 문장: `HYPERFRAMES_PYTHON=<kokoro-onnx·soundfile이 든 venv의 python> npx hyperframes@0.8.141 tts "<문장>" -v af_heart -o <파일>.wav`(채널 목소리 여성 `af_heart`; 시험용 남성 `am_adam`, `bm_george`). 설치 `python3 -m venv <dir> && <dir>/bin/pip install kokoro-onnx soundfile`(음성 데이터 약 27MB).
