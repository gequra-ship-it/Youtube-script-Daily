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
 "Miya's Note · 내레이션 대본",
 f"영상 길이 {ts(d['total'])} (장면 간격 {d['gap']}초, 앞 여백 {d['lead']}초, 끝 여백 {d.get('tail',2.5)}초), 단어 수 {words}, 장면 {len(SCENES)}개, 단위(그림) {len(d['cuts'])}개. 길이는 Kokoro 음성(af_heart)의 실제 길이 기준.",
 "TTS: 영어, 여성 1인(Kokoro af_heart), 정규화 -16.8 LUFS. 원문 대비 바뀐 점: 사실 확인으로 수치·표현을 수정하고 단정 표현에 단서를 붙임(채팅의 확인 표 참고).",
 "", "===== 1부: TTS 입력용 전문 (장면당 한 문단) =====",""]
for s in SCENES: L+= [s[4],""]
L+= ["===== 2부: 장면별 대본 =====",""]
cuts=d['cuts']
for s in SCENES:
    if not s[0][1:].isdigit(): continue   # fixed outro scene (id OUTRO) has no script entry
    i=int(s[0][1:])
    if str(i) not in d['starts']: continue   # partial build
    st=d['starts'][str(i)]; dd=d['D'][str(i)]
    cs=[c for c in cuts if c['scene']==i]
    CINE3D=os.path.exists(f'{REPO}/render/{slug}/cine.js')
    kind=('데이터 카드' if CINE3D else '칠판') if (s[2]=='chalk' or i in CFG.CHALK) else ('3D' if CINE3D else '일러스트')
    L.append(f"[{s[0]}] {ts(st)}–{ts(st+dd)} ({dd:.1f}s) {kind} · {s[1]}")
    L.append(s[4])
    L.append(("의미 단위: " if CINE3D else "그림(의미 단위): ")+", ".join(f"{c['id']} {ts(c['t0'])}–{ts(c['t1'])} [{c['tr']}]" for c in cs))
    sfx=[f"{x['name']} @{ts(x['t'])}" for x in d.get('sfx',[]) if x['unit'] in {c['id'] for c in cs}]
    if i in CFG.CHALK: sfx.append("분필 @"+", ".join(ts(t) for t in d['chalk_pop'][str(i)]))
    if not sfx: sfx.append("없음")
    L.append("효과음: "+" · ".join(sfx)); L.append("")
L+= ["===== 3부: 자막 줄 분할 (MP4 자막과 동일, 시작 시각) =====",""]
cur=None
for c in d['caps']:
    if c['scene']!=cur:
        cur=c['scene']; L+=["",f"[S{cur:02d}]"]
    L.append(f"{ts(c['t0'])}  {c['text']}")
SCRIPT_REF = wdir() + f'/build/{slug}_script.txt'   # 2026-10-24: not delivered to Drive any more (miya), kept in the work dir for checking
open(SCRIPT_REF,'w',encoding='utf-8').write("\n".join(L)+"\n")

DESC_SHORT = CFG.DESC[0]   # 2026-10-24: description = 1-2 sentences only (about 1/3 of the old one); ABOUT and SOURCES are not delivered
if len(DESC_SHORT) > 260: print(f"WARNING: description {len(DESC_SHORT)} chars (aim <= 260)")
if not CFG.CHAPTERS:   # Shorts: title + description + hashtags only (no timeline)
    SRC = ("SOURCES\n" + "\n".join("- " + x for x in CFG.SOURCES) + "\n\n") if getattr(CFG, 'SOURCES', None) else ""
    M="=== TITLE ===\n"+CFG.TITLE+"\n\n=== DESCRIPTION ===\n"+DESC_SHORT+"\n\n"+SRC+CFG.HASHTAGS+"\n"
    open(f'{OUT}/{slug}_metadata.txt','w',encoding='utf-8').write(M); print(M); raise SystemExit
ch=CFG.CHAPTERS
lines=[]
prev=None
for k,(i,t) in enumerate([c for c in ch if str(c[0]) in d['starts'] or c[0]==ch[0][0]]):
    st=0.0 if k==0 else d['starts'][str(i)]
    if prev is not None: assert st-prev>=10
    prev=st; m=int(st//60); s=int(st%60); lines.append(f"{m:02d}:{s:02d} {t}")
SRC = ("SOURCES\n" + "\n".join("- " + x for x in CFG.SOURCES) + "\n\n") if CFG.SOURCES else ""   # kept in the metadata (miya 2026-10-24); block omitted when the video names no source
M = ("=== TITLE ===\n" + CFG.TITLE + "\n\n=== DESCRIPTION ===\n" + DESC_SHORT + "\n\nTIMELINE\n" + "\n".join(lines) + "\n\n" + SRC + CFG.HASHTAGS + "\n")
assert len(CFG.TITLE) <= 100
open(f'{OUT}/{slug}_metadata.txt','w',encoding='utf-8').write(M)
print(M)
