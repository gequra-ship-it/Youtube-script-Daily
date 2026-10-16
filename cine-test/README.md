# cine-test — 시네마틱 3D(cine) 실험 보관 폴더 (2026-10-14~16)

2026-10-16 사용자 결정으로 기본 방식은 SVG 모션그래픽(`docs/miyas-lab-guideline.md`, `tools/build3.py`)으로 돌아갔다.
이 폴더는 3D 실험에서 쓰던 문서와 코드를 그대로 모아 둔 곳이다. 사용자가 3D를 요청할 때만 쓴다.
여기서 얻은 것 중 SVG에 쓸 만한 것은 기본 지침서 **20장**과 `tools/`에 옮겼다(드리프트 카메라, 초반 밀도 `HOOK`,
속도선, 관절 체인 모션, 지루한 구간 측정 `motion_check.py`, 병렬 렌더 `render-chunked.yml`+`chunk_prep.py`).

| 경로 | 내용 |
|---|---|
| `docs/miyas-lab-guideline-cine.md` | 3D 방식 지침서(보관본) |
| `tools/cine_spec.md` | 3D 장면·`cine.json` 작성 명세 |
| `tools/cine/` | 실행 라이브러리(`cine.js`, `cine.css`), 실사감 도구(`kit.js`), 장면 라이브러리(`scenes/`), Three.js·GSAP·글꼴 |
| `tools/build_audio.py` | 3D용 단위 나누기·자막·소리 믹스 → `render/<slug>/mix.m4a` + `build_data.json` |
| `tools/build_cine.py` | `cine-test/videos/<slug>/cine.json` → `render/<slug>/index.html` |
| `tools/cineshot.py` | 3D 페이지 미리보기·프레임당 시간·구간 수 추정(`--estimate`) |
| `tools/camprobe.py` | 장면별 카메라 위치 조사 |
| `videos/<slug>-cine*` | 3D판 영상 원본(대본·설정·`cine.json`·영상별 장면) |

사용법(공용 도구 `tools/paths.py` 등을 그대로 쓴다. `vdir()`가 `cine-test/videos/<slug>`도 찾는다):
```
SLUG=<slug>-cine MIYA_WORK=... python3 cine-test/tools/build_audio.py        # 음성은 tools/tts.sh, tools/audio_prep.py로 먼저
SLUG=<slug>-cine python3 cine-test/tools/build_cine.py
python3 cine-test/tools/cineshot.py render/<slug>-cine out 5 30
```
렌더 원본(`render/<slug>-cine*`)은 렌더 워크플로가 `render/` 아래를 보므로 `render/`에 그대로 둔다.
