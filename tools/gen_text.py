import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
SCENES = load_scenes(); CFG = load_config()
d = json.load(open(wdir() + '/build/build_data.json')); slug = d['slug']
OUT = f'{REPO}/render/{slug}/deliver'; os.makedirs(OUT, exist_ok=True)
def ts(t,dec=1):
    m=int(t//60); s=t-60*m
    return f'{m:02d}:{s:0{4 if dec else 2}.{dec}f}'
words=sum(len(s[4].split()) for s in SCENES)
L=[]
L+= [ CFG.TITLE,
 "Miya's Lab · 내레이션 대본",
 f"영상 길이 {ts(d['total'])} (장면 간격 {d['gap']}초, 앞 여백 {d['lead']}초, 끝 여백 2.5초), 단어 수 {words}, 장면 {len(SCENES)}개, 컷 {len(d['cuts'])}개. 길이는 Kokoro 음성(am_michael)의 실제 길이 기준.",
 "TTS: 영어, 남성 1인(Kokoro am_michael), 정규화 -16.8 LUFS. 원문 대비 바뀐 점: 사실 확인으로 수치·표현을 수정하고 단정 표현에 단서를 붙임(채팅의 확인 표 참고).",
 "", "===== 1부: TTS 입력용 전문 (장면당 한 문단) =====",""]
for s in SCENES: L+= [s[4],""]
L+= ["===== 2부: 장면별 대본 =====",""]
cuts=d['cuts']
for s in SCENES:
    i=int(s[0][1:]); st=d['starts'][str(i)]; dd=d['D'][str(i)]
    cs=[c for c in cuts if c['scene']==i]
    kind='칠판' if s[2]=='chalk' else '일러스트'
    L.append(f"[{s[0]}] {ts(st)}–{ts(st+dd)} ({dd:.1f}s) {kind} · {s[1]}")
    L.append(s[4])
    L.append("컷: "+", ".join(f"{c['id']} {ts(c['t0'])}–{ts(c['t1'])}" for c in cs))
    sfx=[]
    if i in CFG.WHOOSH: sfx.append(f"휙 @{ts(st)}")
    if i in CFG.CHALK: sfx.append("분필 @"+", ".join(ts(t) for t in d['chalk_pop'][str(i)]))
    else: sfx.append("배경 효과음(저음 드론)")
    L.append("효과음: "+" · ".join(sfx)); L.append("")
L+= ["===== 3부: 자막 줄 분할 (MP4 자막과 동일, 시작 시각) =====",""]
cur=None
for c in d['caps']:
    if c['scene']!=cur:
        cur=c['scene']; L+=["",f"[S{cur:02d}]"]
    L.append(f"{ts(c['t0'])}  {c['text']}")
open(f'{OUT}/{slug}_script.txt','w',encoding='utf-8').write("\n".join(L)+"\n")

ch=CFG.CHAPTERS
lines=[]
prev=None
for k,(i,t) in enumerate(ch):
    st=0.0 if k==0 else d['starts'][str(i)]
    if prev is not None: assert st-prev>=10
    prev=st; m=int(st//60); s=int(st%60); lines.append(f"{m:02d}:{s:02d} {t}")
import datetime
src = ("SOURCES\n" + "\n".join("- " + x for x in CFG.SOURCES) + "\n\n") if CFG.SOURCES else ""
M = (f"슬러그 {slug}, 작성일 {datetime.date.today().isoformat()}. 챕터 시각은 렌더 구성표(내레이션을 배치한 시각)에서 가져온 값이며, 렌더된 MP4 프레임으로 다시 재지는 않았음.\n"
     f"제목 길이 {len(CFG.TITLE)}자(70자 이하). 설명의 ABOUT 문구는 17장의 제안 문구이며 사용자 확인 전.\n\n"
     "=== TITLE ===\n" + CFG.TITLE + "\n\n=== DESCRIPTION ===\n" + "\n\n".join(CFG.DESC) + "\n\nCHAPTERS\n" + "\n".join(lines) + "\n\n" + src +
     "ABOUT MIYA'S LAB\nMiya's Lab turns big questions into calm, illustrated explainers. New videos keep coming, so subscribe if you want the next one.\n\n" + CFG.HASHTAGS + "\n")
assert len(CFG.TITLE) <= 70
open(f'{OUT}/{slug}_metadata.txt','w',encoding='utf-8').write(M)
print(M[:1500]); print(len(open(f'{OUT}/{slug}_script.txt').read()))
