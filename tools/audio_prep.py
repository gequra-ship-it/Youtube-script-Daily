# Build normalized narration (per-scene clips) + SFX files. Run once.
import subprocess, json, re, os, sys, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import *
SCENES = load_scenes()
TTS = wdir() + '/tts'; B = wdir() + '/build'; os.makedirs(B, exist_ok=True)
GAP=0.5
def run(*a,**k):
    return subprocess.run(a,capture_output=True,text=True,**k)
def dur(f):
    return float(run('ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f).stdout)
n=len(SCENES); D=[]
for i in range(1,n+1):
    f=f'{TTS}/p{i:02d}.wav'; d=dur(f); D.append(d)
    run('ffmpeg','-y','-v','error','-i',f,'-ar','48000','-ac','2',f'{B}/s{i:02d}.wav')
run('ffmpeg','-y','-v','error','-f','lavfi','-i','anullsrc=r=48000:cl=stereo','-t',str(GAP),f'{B}/gap.wav')
with open(f'{B}/list.txt','w') as fh:
    for i in range(1,n+1):
        fh.write(f"file 's{i:02d}.wav'\nfile 'gap.wav'\n")
r=run('ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',f'{B}/list.txt','-c','copy',f'{B}/cat.wav'); print(r.stderr[:200])
# two-pass loudnorm
p1=run('ffmpeg','-nostats','-i',f'{B}/cat.wav','-af','loudnorm=I=-16.8:TP=-1.5:LRA=3.5:print_format=json','-f','null','-')
j=json.loads(p1.stderr[p1.stderr.rindex('{'):])
af=("loudnorm=I=-16.8:TP=-1.5:LRA=3.5:measured_I=%s:measured_TP=%s:measured_LRA=%s:measured_thresh=%s:offset=%s:linear=true"
    %(j['input_i'],j['input_tp'],j['input_lra'],j['input_thresh'],j['target_offset']))
r=run('ffmpeg','-y','-v','error','-i',f'{B}/cat.wav','-af',af,'-ar','48000','-ac','2',f'{B}/nar_norm.wav'); print(r.stderr[:200])
# slice back
T=0.0; starts=[]
for i,d in enumerate(D,1):
    starts.append(T)
    run('ffmpeg','-y','-v','error','-ss',f'{T:.4f}','-t',f'{d+GAP:.4f}','-i',f'{B}/nar_norm.wav','-ar','48000','-ac','2',f'{B}/n{i:02d}.wav')
    T+=d+GAP
json.dump({'D':D,'starts':starts,'gap':GAP,'total':T},open(f'{B}/timing_base.json','w'))
m=run('ffmpeg','-nostats','-i',f'{B}/nar_norm.wav','-af','ebur128=peak=true','-f','null','-').stderr
print(re.findall(r'I:\s+(-?[\d.]+) LUFS',m)[-1:], re.findall(r'LRA:\s+([\d.]+)',m)[-1:], 'total',round(T,2),'sum d',round(sum(D),2))
