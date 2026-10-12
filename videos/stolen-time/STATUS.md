# stolen-time — 진행 상태 (새 세션이 이어서 할 때 읽는 파일)

영상: "The Physics of Stolen Time: How 3 Hours Can Equal 23 Years" (우주 모드, 길이 제한 없음, 약 24분, 3,932단어). 숏츠 `stolen-time-short1`, `-short2`.
사실 확인 결과는 `script.py` 머리 주석에 있음.

## 단계 (끝난 것은 [x])
- [x] 대본 사실 확인 → `script.py`, `config.py` (본편), `videos/stolen-time-short1/`, `-short2/` 의 script·config
- [x] `art_brief.md` (등장인물 시트), 에이전트 프롬프트 `/home/claude/work/art_prompt_st.txt` (작업 공간이 새로 시작되면 `videos/cosmic-prison` 쪽 프롬프트 형식을 따라 다시 만든다: SLUGX/RANGE/SCRATCH/CANVAS/PREVIEWENV 자리표시자)
- [ ] TTS: `/home/claude/work/tts_st.sh` 실행 중 → `/home/claude/work/<slug>/tts/p##.wav`. 로그 `/home/claude/work/tts_st.log` 에 `DONE` 이면 끝. 작업 공간이 사라졌으면 Kokoro venv부터 다시(`tools/README.md` 1단계)
- [ ] `SLUG=x python3 tools/audio_prep.py` (세 슬러그), `PLAN=1 tools/build3.py` (숏츠는 `VERT=1`)
- [ ] 그림: 숏츠 2개 에이전트, 본편은 plan.json 단위를 장면 경계로 12~19개씩 묶어 에이전트 1개씩 (동시 20개 한도). 사이드카에 `labels`, sfx 는 우주 모드 이름만
- [ ] 빌드 `tools/build3.py` (세 슬러그), 누락 uid·sfx 연속 중복 검사, `gen_text.py`, 썸네일 2장 (`thumb/A.html`, `B.html`, `tools/thumb_shot.py`)
- [ ] `render/.slug` 에 세 슬러그를 적고 푸시 → Actions 렌더 → Drive 확인 → 사용자 보고 (사실 확인 표 포함)

## 사용 한도 메모
2026-10-12 저녁: 주간 한도 96% 상태에서 Fable로 시작. 끊기면 목요일 08:00 KST 초기화 이후에 이 파일부터 읽고 이어서 한다.
