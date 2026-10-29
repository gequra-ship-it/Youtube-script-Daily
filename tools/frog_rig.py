# frog_rig.py -- the note-frog's joints and its CONTACT acts (2026-10-29, miya: "the frog itself is too static; the whole frog moves,
# its body does not"; example: standing under an apple tree, the apple drops on it and it keels over).
#
# Rig (tools/frog.py markup): #<t>_lf (life layer: breathing, weight shift) > #<t>_ac (acts) > legs #<t>_lgl / #<t>_lgr (hip pivots),
# arms #<t>_la / #<t>_ra (shoulder pivots), head #<t>_hd (+ #<t>_of outfits, #<t>_te tears; neck pivot). Pivots are svgOrigin values
# in the parent group's units: feet "0 6", left hip "-16 -10", right hip "28 -10", left shoulder "-34 -22", right shoulder "34 -22",
# neck "4 -40". Local +x = the frog's facing side (the group's flip mirrors everything).
#
# 1. life_js(): every frog breathes, shifts its weight, turns its head a little, glances, shuffles a foot -- nothing is frozen.
# 2. limb helpers: leg cycles for run / walk / hops, tucks in the air, kicks when hanging, braced stances.
# 3. contact acts (CONTACT): the frog meets a MOVING object of the picture at the object's own time (build3 passes the object's
#    motion timing in objt): bonk (dropped object lands on its head, it keels over, the object rolls off), squish (toppling object
#    flattens it), dodge (jumps over a rolling / sliding object), chase (runs after it), splash (a drop into water soaks it),
#    swingride (hangs under a swing in phase), bumped (jolted by a bouncing thing), blown (a gust rolls it over), tug (pulls a rope,
#    slips), lift (holds up a rising load), catch (catches the dropped thing), trip (stumbles over a low thing while running).
#    Which one, where the frog stands and the sound word are chosen by tools/frog_place.py (object group names + sizes + sentence
#    words, guideline 7-2 G); the times come from obj_span() here, shared by frog_place (bubble times) and build3 (absolute times).
# Everything is absolute-time GSAP on the main timeline (seek-safe, chunk-render-safe); no randomness.
import json, math, os

A = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
try: BNC = json.load(open(os.path.join(A, 'ease_miyaBnc.json')))   # CustomBounce "miyaBnc" sampled at 201 points (tools/assets, made with Chromium)
except Exception: BNC = None
P_TD = .305   # progress of the first touchdown of miyaBnc (from the samples)

FEET = 'svgOrigin:"0 6"'; HIPL = 'svgOrigin:"-16 -10"'; HIPR = 'svgOrigin:"28 -10"'; SHL = 'svgOrigin:"-34 -22"'; SHR = 'svgOrigin:"34 -22"'; NECK = 'svgOrigin:"4 -40"'
CONTACT = ('bonk', 'squish', 'dodge', 'chase', 'splash', 'swingride', 'bumped', 'blown', 'tug', 'lift', 'catch', 'trip',
           'sidestep', 'flattened', 'trampoline', 'knocked', 'shockwave', 'magnetized', 'hopalong', 'dripped', 'rimride', 'launched', 'unrolled', 'balloonride', 'sinkride')   # 2026-10-29 b: 13 more (miya: contact is the fun part)
STARS = {'bonk', 'squish', 'trip', 'flattened', 'knocked', 'unrolled'}


def bnc_inv(e):
    """progress p at which miyaBnc first reaches value e (0..1) -- where a dropping object's bottom crosses a height"""
    if not BNC: return min(max(e, 0), 1) * P_TD
    for i, v in enumerate(BNC):
        if v >= e: return i / (len(BNC) - 1)
    return P_TD


def ease_inv(name, e):
    """progress for eased value e: power1.inOut, power3.out, power2.inOut, none"""
    e = min(max(e, 0), 1)
    if name == 'power1.inOut': return math.sqrt(e / 2) if e < .5 else 1 - math.sqrt((1 - e) / 2)
    if name == 'power2.inOut': return (e / 4) ** (1 / 3) if e < .5 else 1 - ((1 - e) / 4) ** (1 / 3)
    if name == 'power3.out': return 1 - (1 - e) ** (1 / 3)
    if name == 'power2.out': return 1 - math.sqrt(1 - e)
    if name == 'power2.in': return math.sqrt(e)
    return e


def obj_span(kind, at):
    """(start, duration) of an object's one-shot motion in seconds AFTER the unit start t0, from the group's data-* (same numbers as
    motions.core_js / obj_js). kind = 'core-drop', 'topple', 'rollby', 'slide', 'rise'; None for motions that start at the
    transition (bouncing, swing, pendulum: build3 passes v0 for those)."""
    f = lambda k, d: float(at.get('data-' + k, d))
    if kind == 'core-drop': return .15, .9
    if kind == 'topple': return f('delay', .3), f('dur', .55)
    if kind == 'rollby': return f('delay', .3), f('dur', 3)
    if kind == 'slide': return f('delay', .3), f('dur', .7)
    if kind == 'rise': return f('delay', .3), f('dur', .5)
    # 2026-10-29 b (miya: "some gags are out of sync"): the kinds of the second round, same numbers as motions.obj_js
    if kind == 'slam': return f('delay', .3), .28
    if kind == 'squash': return f('delay', .3), .1
    if kind == 'popin': return f('delay', .3), .45
    if kind in ('unroll', 'unfold'): return f('delay', .3), f('dur', .8)
    if kind == 'magnet': return f('delay', .3), f('dur', .9)
    if kind == 'hop': return f('delay', .3), f('per', 1.4)
    if kind == 'drip': return f('delay', .3), f('per', 1.8)
    return None


def travel(kind, at, box):
    """(start centre x, end centre x) in picture px of a rollby / slide group whose STATIC box is box = (x, y, w, h)"""
    f = lambda k, d: float(at.get('data-' + k, d))
    x, y, w, h = box; cx = x + w / 2
    if kind == 'rollby': return cx, cx + f('dist', 600)
    if kind == 'slide':
        if at.get('data-dir') == 'out': return cx, cx + f('dx', -960)
        return cx + f('dx', -960), cx
    return cx, cx


def pass_time(kind, at, box, px, t0):
    """absolute time at which a rollby / slide object's centre crosses picture x = px (None when it never does)"""
    sp_ = obj_span(kind, at)
    if not sp_: return None
    st, du = sp_; a, b = travel(kind, at, box)
    if b == a: return None
    fr = (px - a) / (b - a)
    if not (0 <= fr <= 1): return None
    ez = 'power1.inOut' if kind == 'rollby' else ('power3.in' if at.get('data-dir') == 'out' else 'power3.out')
    p = (fr ** (1 / 3)) if ez == 'power3.in' else ease_inv(ez, fr)
    return t0 + st + p * du


def stars_js(t, tm, dur, swirl=True):
    """stars circle over the head (+ swirl eyes) from tm for dur seconds (impact daze; swirl=False = magic sparkles only)"""
    if not swirl: return f'tl.set("#{t}_st",{{opacity:1}},{tm:.3f});tl.fromTo("#{t}_st",{{rotation:0,svgOrigin:"6 -74"}},{{rotation:360,duration:1.2,repeat:{max(int(dur / 1.2) - 1, 0)},ease:"none",svgOrigin:"6 -74",immediateRender:false}},{tm:.3f});tl.set("#{t}_st",{{opacity:0}},{tm + dur:.3f});'
    return (f'tl.set("#{t}_st",{{opacity:1}},{tm:.3f});tl.fromTo("#{t}_st",{{rotation:0,svgOrigin:"6 -74"}},{{rotation:360,duration:1.2,repeat:{max(int(dur / 1.2) - 1, 0)},ease:"none",svgOrigin:"6 -74",immediateRender:false}},{tm:.3f});'
            f'tl.set("#{t}_spl,#{t}_spr",{{opacity:1}},{tm:.3f});tl.fromTo("#{t}_spl",{{rotation:0}},{{rotation:720,duration:{dur:.3f},ease:"none",svgOrigin:"-10 -66",immediateRender:false}},{tm:.3f});'
            f'tl.fromTo("#{t}_spr",{{rotation:0}},{{rotation:-720,duration:{dur:.3f},ease:"none",svgOrigin:"22 -66",immediateRender:false}},{tm:.3f});'
            f'tl.set("#{t}_st,#{t}_spl,#{t}_spr",{{opacity:0}},{tm + dur:.3f});')


def legs_cycle(t, ta, te, per, amp=26):
    """alternating leg swing about the hips (run / walk), one yoyo tween per leg"""
    n = max(int((te - ta) / (per / 2)), 1)
    return [f'tl.fromTo("#{t}_lgl",{{rotation:{-amp},{HIPL}}},{{rotation:{amp},duration:{per / 2:.3f},yoyo:true,repeat:{n},ease:"sine.inOut",{HIPL},immediateRender:false}},{ta:.3f});',
            f'tl.fromTo("#{t}_lgr",{{rotation:{amp},{HIPR}}},{{rotation:{-amp},duration:{per / 2:.3f},yoyo:true,repeat:{n},ease:"sine.inOut",{HIPR},immediateRender:false}},{ta:.3f});',
            f'tl.set("#{t}_lgl,#{t}_lgr",{{rotation:0}},{ta + (n + 1) * per / 2 + .01:.3f});']


def arms_swing(t, ta, te, per, amp=22):
    """arms swing opposite to the legs while running"""
    n = max(int((te - ta) / (per / 2)), 1)
    return [f'tl.fromTo("#{t}_la",{{rotation:{-amp},{SHL}}},{{rotation:{amp},duration:{per / 2:.3f},yoyo:true,repeat:{n},ease:"sine.inOut",{SHL},immediateRender:false}},{ta:.3f});',
            f'tl.fromTo("#{t}_ra",{{rotation:{-amp},{SHR}}},{{rotation:{amp},duration:{per / 2:.3f},yoyo:true,repeat:{n},ease:"sine.inOut",{SHR},immediateRender:false}},{ta:.3f});']


def tuck(t, tm, up=.22, hold=.0, down=.3, deg=55):
    """legs pulled up under the body (a jump), then down"""
    return [f'tl.to("#{t}_lgl",{{rotation:{deg},duration:{up},ease:"power2.out",{HIPL}}},{tm:.3f});tl.to("#{t}_lgr",{{rotation:{-deg},duration:{up},ease:"power2.out",{HIPR}}},{tm:.3f});',
            f'tl.to("#{t}_lgl",{{rotation:0,duration:{down},ease:"power2.in",{HIPL}}},{tm + up + hold:.3f});tl.to("#{t}_lgr",{{rotation:0,duration:{down},ease:"power2.in",{HIPR}}},{tm + up + hold:.3f});']


def kicks(t, tm, n=5, per=.32, amp=22):
    """alternating little kicks (hanging, lying on the back)"""
    return [f'tl.fromTo("#{t}_lgl",{{rotation:{-amp},{HIPL}}},{{rotation:{amp},duration:{per / 2:.3f},yoyo:true,repeat:{n},ease:"sine.inOut",{HIPL},immediateRender:false}},{tm:.3f});',
            f'tl.fromTo("#{t}_lgr",{{rotation:{amp},{HIPR}}},{{rotation:{-amp},duration:{per / 2:.3f},yoyo:true,repeat:{n},ease:"sine.inOut",{HIPR},immediateRender:false}},{tm:.3f});']


def brace(t, tm, front=-24, back=18, dur=.35):
    """one leg forward, one back (standing against a push / pull / wind)"""
    return [f'tl.to("#{t}_lgl",{{rotation:{back},duration:{dur},ease:"power2.out",{HIPL}}},{tm:.3f});tl.to("#{t}_lgr",{{rotation:{front},duration:{dur},ease:"power2.out",{HIPR}}},{tm:.3f});']


def unbrace(t, tm, dur=.4):
    return [f'tl.to("#{t}_lgl,#{t}_lgr",{{rotation:0,duration:{dur},ease:"power2.inOut"}},{tm:.3f});']


def squash(t, tm, sy=.86, sx=1.1, dur=.1, back=.3):
    """impact squash of the whole body about the feet on the life layer, then back (does not touch #_ac, which the acts own)"""
    return [f'tl.to("#{t}_lf",{{scaleY:{sy},scaleX:{sx},duration:{dur},ease:"power2.out",{FEET}}},{tm:.3f});tl.to("#{t}_lf",{{scaleY:1,scaleX:1,duration:{back},ease:"back.out(2)",{FEET}}},{tm + dur:.3f});']


# ---------------------------------------------------------------- life layer ----------------------------------------------------------------
def life_js(t, a0, T, k, nohead=False, nolegs=False, noscale=False, noeyes=False, avoid=()):
    """small continuous life for every frog (2026-10-29): breathing + weight shift on #_lf, head micro-turns on the head group,
    glances (pupils), a foot shuffle. k = unit index (phases differ from frog to frog). avoid = times (s) near which the pupils must
    not be moved (mood changes set them). Acts that drive the same parts switch the matching layer off."""
    o = []; span = T - a0
    if span < 1.2: return o
    if not noscale:
        per = 2.3 + (k % 3) * .3; n = max(int((span - .4) / per), 1)
        o.append(f'tl.fromTo("#{t}_lf",{{scaleY:1,{FEET}}},{{scaleY:1.025,duration:{per:.2f},yoyo:true,repeat:{n},ease:"sine.inOut",{FEET},immediateRender:false}},{a0 + .4:.3f});')
        per2 = 5.2 + (k % 2) * .9; n2 = max(int((span - .8) / per2), 1); sg = 1 if k % 2 == 0 else -1
        o.append(f'tl.fromTo("#{t}_lf",{{rotation:{-1.2 * sg},{FEET}}},{{rotation:{1.2 * sg},duration:{per2:.2f},yoyo:true,repeat:{n2},ease:"sine.inOut",{FEET},immediateRender:false}},{a0 + .8:.3f});')
    if not nohead and span > 2.4:
        per = 1.9 + (k % 4) * .4; n = max(int((span - .8) / per), 1); sg = 1 if k % 3 else -1
        o.append(f'tl.fromTo("#{t}_hd,#{t}_of,#{t}_te",{{rotation:{-2.4 * sg},{NECK}}},{{rotation:{2.4 * sg},duration:{per:.2f},yoyo:true,repeat:{n},ease:"sine.inOut",{NECK},immediateRender:false}},{a0 + .6 + (k % 3) * .5:.3f});')
    if not noeyes:
        tb = a0 + 1.6 + (k % 3) * .4; j = 0
        while tb < T - 1.0:
            if not any(abs(tb - x) < .5 or abs(tb + .7 - x) < .5 for x in avoid):
                dx = 2.2 if (j + k) % 2 == 0 else -2.2
                o.append(f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cx:"+={dx}"}},duration:.1,ease:"power1.out"}},{tb:.3f});tl.to("#{t}_pl,#{t}_pr",{{attr:{{cx:"-={dx}"}},duration:.12,ease:"power1.out"}},{tb + .7:.3f});')
            tb += (2.7, 4.3, 3.4)[j % 3]; j += 1
    if not nolegs:
        tb = a0 + 2.4 + (k % 2) * 1.3; j = 0
        while tb < T - 1.0:
            lg, org = (f'{t}_lgr', HIPR) if (j + k) % 2 == 0 else (f'{t}_lgl', HIPL)
            sg = -1 if lg.endswith('r') else 1
            o.append(f'tl.to("#{lg}",{{rotation:{16 * sg},duration:.22,ease:"power2.out",{org}}},{tb:.3f});tl.to("#{lg}",{{rotation:0,duration:.28,ease:"power2.in",{org}}},{tb + .3:.3f});')
            tb += 5.1 + (j % 2) * 1.7; j += 1
    return o


# ---------------------------------------------------------------- contact acts ----------------------------------------------------------------
def contact_js(t, d, act, t0, a0, T, k, objt=None, face=None, moods=None):
    """GSAP lines for one contact act. act = {'type', 'obj': group id, ...}; objt = {group id: {'kind', 'at', 'box', 'g', 'st', 'du', 'v0'}}
    from build3 (st/du absolute; v0 = transition start for bouncing / swing). face(mood, tm) -> tl.set block (frog.face_js bound to t).
    Returns (lines, info) with info = {'nohead','nolegs','noscale','noeyes': bools for life_js, 'says': {k: abs time}}."""
    o = []; info = dict(nohead=False, nolegs=True, noscale=True, noeyes=False, says={})
    s = d['s']; ac = f'"#{t}_ac"'; TR = f'"#{t}_tr"'; RM = f'"#{t}_rm"'
    ob = (objt or {}).get(act.get('obj')) or {}
    kind = ob.get('kind', ''); at = ob.get('at', {}); g = ob.get('g')
    st = ob.get('st'); du = ob.get('du'); v0 = ob.get('v0')
    F = (lambda m, tm: face(m, tm)) if face else (lambda m, tm: '')
    ty = act['type']
    if ty in ('swingride', 'lift', 'climb', 'dangle') or d.get('ride'): o.append(f'tl.set("#{t}_sh",{{opacity:0}},0);')   # no ground shadow under a hanging / riding frog
    if ty in COSTUME_ACTS: return o + generic_js(t, d, COSTUME_ACTS[ty], a0, T, k, F, act)[0], generic_js(t, d, COSTUME_ACTS[ty], a0, T, k, F, act)[1]
    if ty in LOCO:
        l_, i_ = loco_js(t, d, act, a0, T, k, F); return o + l_, i_
    if ty == 'bonk':   # the dropped object lands on its head (head top = the object's final bottom), it is dazed, keels over backward; the object rolls off its head to the ground
        if st is None: st, du = t0 + .15, .9
        th = st + P_TD * du; info['nohead'] = True; info['noeyes'] = True
        o.append(f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-72}},duration:.3}},{a0:.3f});tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:-6,duration:.4,ease:"power2.out",{NECK}}},{a0:.3f});')   # looks up at it
        o += squash(t, th, .84, 1.12, .08, .35); o.append(stars_js(t, th, 2.6)); o.append(F('shock', th))
        o.append(f'tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:0,duration:.1,{NECK}}},{th:.3f});')
        o.append(f'tl.fromTo({ac},{{rotation:0}},{{rotation:5,duration:.22,yoyo:true,repeat:3,ease:"sine.inOut",{FEET}}},{th + .1:.3f});')   # dazed wobble while the thing sits on its head
        t2 = th + 1.05
        o.append(f'tl.to({ac},{{rotation:-84,duration:.5,ease:"power2.in",{FEET}}},{t2:.3f});tl.to({ac},{{rotation:-80,duration:.2,ease:"power1.out",{FEET}}},{t2 + .5:.3f});tl.to({ac},{{rotation:-84,duration:.18,{FEET}}},{t2 + .7:.3f});')
        o += kicks(t, t2 + .3, 5, .3, 24); o.append(f'tl.to("#{t}_ra",{{rotation:-70,duration:.3,{SHR}}},{t2 + .2:.3f});tl.to("#{t}_la",{{rotation:60,duration:.3,{SHL}}},{t2 + .2:.3f});')
        if g: o.append(f'tl.to({g},{{x:{62 * s * d["flip"]:.0f},y:{80 * s:.1f},rotation:{40 * d["flip"]},duration:.55,ease:"bounce.out"}},{t2 + .12:.3f});')   # rolls off the head to the ground in front of the frog (the frog fell backward)
        info['says'][0] = th + .12
        if T - t2 > 3.2:   # sits up, rubs its head, sulks
            t3 = t2 + 1.9
            o.append(f'tl.set("#{t}_st,#{t}_spl,#{t}_spr",{{opacity:0}},{t3:.3f});' + F('hurt', t3))
            o.append(f'tl.to({ac},{{rotation:0,duration:.7,ease:"back.out(1.2)",{FEET}}},{t3:.3f});tl.to("#{t}_la",{{rotation:0,duration:.5,{SHL}}},{t3:.3f});')
            o.append(f'tl.to("#{t}_ra",{{rotation:-168,duration:.4,ease:"power2.out",{SHR}}},{t3 + .5:.3f});tl.fromTo("#{t}_ra",{{rotation:-168,{SHR}}},{{rotation:-152,duration:.28,yoyo:true,repeat:5,ease:"sine.inOut",{SHR},immediateRender:false}},{t3 + .9:.3f});')
            o.append(f'tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:-7,duration:.5,ease:"sine.inOut",{NECK}}},{t3 + .6:.3f});' + F('pout', min(t3 + 2.6, T - .3)))
            if len(d.get('says') or []) > 1: info['says'][1] = t3 + 1.1
    elif ty == 'squish':   # a toppling object lands on it: flattened, stars; later it crawls out from under and pops back into shape
        if st is None: st, du = t0 + .3, .55
        th = st + .92 * du; info['nohead'] = True; info['noeyes'] = True
        o.append(f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-71}},duration:.25}},{max(a0, th - .5):.3f});' + F('shock', max(a0, th - .4)))
        o.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.2,{SHR}}},{max(a0, th - .35):.3f});tl.to("#{t}_la",{{rotation:150,duration:.2,{SHL}}},{max(a0, th - .35):.3f});')
        o.append(f'tl.to({ac},{{scaleY:.2,scaleX:1.55,duration:.1,ease:"power3.in",{FEET}}},{th:.3f});' + stars_js(t, th + .05, 2.2))
        info['says'][0] = th + .1
        t2 = th + 1.6
        if T - t2 > 2.0:
            o.append(f'tl.to({TR},{{x:-150,duration:.8,ease:"power2.inOut"}},{t2:.3f});')   # crawls out backward (local -x: it faces the fallen thing)
            o.append(f'tl.to({ac},{{scaleY:1,scaleX:1,duration:.5,ease:"elastic.out(1,.45)",{FEET}}},{t2 + .5:.3f});tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.4}},{t2 + .5:.3f});')
            o.append(f'tl.set("#{t}_st,#{t}_spl,#{t}_spr",{{opacity:0}},{t2 + 1.2:.3f});' + F('dizzy', t2 + .5))
            o.append(f'tl.fromTo({ac},{{rotation:-8,{FEET}}},{{rotation:8,duration:.5,yoyo:true,repeat:3,ease:"sine.inOut",{FEET},immediateRender:false}},{t2 + 1.0:.3f});' + F('pout', min(t2 + 3.2, T - .3)))
            if len(d.get('says') or []) > 1: info['says'][1] = t2 + 1.3
    elif ty in ('dodge', 'chase'):   # a rolling / sliding object comes along its lane
        tp = act.get('tp')   # absolute pass time (build3 computes it from the frog's x), else from the act's own 'pass' (unit-relative)
        if tp is None and act.get('pass') is not None: tp = t0 + float(act['pass'])
        if tp is None: tp = a0 + 1.2
        if ty == 'dodge':
            hj = min(max(float(act.get('h', 120)) * .9 + 30, 60), 230) / s   # jump high enough to clear the object (local units)
            tj = tp - .32; info['nohead'] = True
            o.append(F('shock', max(a0, tj - .4)) + f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cx:"-=4"}},duration:.2}},{max(a0, tj - .5):.3f});')   # sees it coming (it comes from the facing side)
            o += squash(t, tj - .14, .82, 1.12, .12, .1)
            o.append(f'tl.to({TR},{{y:{-hj:.1f},duration:.36,ease:"power2.out"}},{tj:.3f});tl.to({TR},{{y:0,duration:.34,ease:"power2.in"}},{tj + .36:.3f});')
            o += tuck(t, tj + .05, .2, .2, .25, 60)
            o.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.25,{SHR}}},{tj:.3f});tl.to("#{t}_la",{{rotation:150,duration:.25,{SHL}}},{tj:.3f});tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.4}},{tj + .8:.3f});')
            o += squash(t, tj + .7, .86, 1.1, .08, .3)
            o.append(f'tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:14,duration:.5,ease:"power2.out",{NECK}}},{tj + .9:.3f});tl.to("#{t}_pl,#{t}_pr",{{attr:{{cx:"-=2"}},duration:.3}},{tj + .9:.3f});')   # looks after it
            o.append(F('happy', tj + 1.0))
            if T - tj > 3.0: o.append(f'tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:0,duration:.6,ease:"sine.inOut",{NECK}}},{tj + 2.6:.3f});tl.to("#{t}_pl,#{t}_pr",{{attr:{{cx:"+=6"}},duration:.3}},{tj + 2.6:.3f});')
            info['says'][0] = tj
        else:   # chase: runs after it along the lane (local +x = the object's way), reaching, then stops out of breath
            L = float(act.get('dist', 400)) / s; ta = max(a0 + .1, (st if st is not None else a0 + .3) + .25); te = min(T - .4, ta + (du if du else 2.0) + .5)
            if te - ta < .8: te = min(T - .2, ta + .8)
            per = .42
            o.append(f'tl.to({TR},{{x:{L:.1f},duration:{te - ta:.3f},ease:"power1.inOut"}},{ta:.3f});')
            o.append(f'tl.to({RM},{{rotation:12,duration:.3,svgOrigin:"0 0"}},{ta:.3f});tl.to({RM},{{rotation:-6,duration:.3,ease:"power2.out",svgOrigin:"0 0"}},{te - .1:.3f});tl.to({RM},{{rotation:0,duration:.5,ease:"sine.inOut",svgOrigin:"0 0"}},{te + .4:.3f});')
            tm = ta
            while tm < te - .1:
                o.append(f'tl.to({TR},{{y:-14,duration:{per / 2:.2f},ease:"power2.out"}},{tm:.3f});tl.to({TR},{{y:0,duration:{per / 2:.2f},ease:"power2.in"}},{tm + per / 2:.3f});'); tm += per
            o += legs_cycle(t, ta, te, per, 30)
            o.append(f'tl.to("#{t}_ra",{{rotation:-80,duration:.3,{SHR}}},{ta:.3f});tl.to("#{t}_la",{{rotation:-30,duration:.3,{SHL}}},{ta:.3f});')   # reaching forward
            o.append(F('determined', a0) + F('squint', te) + f'tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.4}},{te:.3f});')
            if T - te > 1.2:   # panting: quick shallow breaths on the life layer
                n = max(int((T - te - .4) / .34), 2)
                o.append(f'tl.fromTo("#{t}_lf",{{scaleY:1,{FEET}}},{{scaleY:.955,duration:.17,yoyo:true,repeat:{n},ease:"sine.inOut",{FEET},immediateRender:false}},{te + .2:.3f});')
                o.append(f'tl.to({ac},{{rotation:10,y:2,duration:.4,ease:"power2.out",{FEET}}},{te + .2:.3f});tl.set("#{t}_sw",{{opacity:1}},{te + .3:.3f});tl.fromTo("#{t}_sw1",{{y:0,opacity:1}},{{y:30,opacity:0,duration:1.0,repeat:{max(int((T - te) / 1.2) - 1, 0)},ease:"power1.in",immediateRender:false}},{te + .3:.3f});')
            info['says'][0] = ta + .2
    elif ty == 'splash':   # the dropped thing hits the water next to it: a fan of drops flies over it, it recoils, shakes off, wipes its face
        if st is None: st, du = t0 + .15, .9
        th = st + P_TD * du   # the object is on its facing side (frog_place faces it)
        o.append(f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-70}},duration:.3}},{a0:.3f});' + F('curious', a0))
        for i in range(6):   # splash drops: from the object side up and over the frog
            dxv = -(40 + (i % 3) * 22); dyv = -(70 + (i % 4) * 18)
            o.append(f'tl.fromTo("#{t}_sp{i}",{{x:0,y:0,opacity:1}},{{x:{dxv},y:{dyv},duration:.32,ease:"power1.out",immediateRender:false}},{th + i * .03:.3f});'
                     f'tl.to("#{t}_sp{i}",{{y:{dyv + 90},opacity:0,duration:.4,ease:"power1.in"}},{th + .32 + i * .03:.3f});')
        o.append(f'tl.set("#{t}_spk",{{opacity:1}},{th:.3f});tl.set("#{t}_spk",{{opacity:0}},{th + .9:.3f});')
        o.append(F('shock', th + .05) + f'tl.to({ac},{{x:-9,rotation:-9,duration:.14,ease:"power2.out",{FEET}}},{th + .05:.3f});')
        o.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.15,{SHR}}},{th + .05:.3f});tl.to("#{t}_la",{{rotation:150,duration:.15,{SHL}}},{th + .05:.3f});')
        o.append(f'tl.fromTo({ac},{{x:-9,rotation:-9,{FEET}}},{{x:-9,rotation:-9,duration:.9,ease:"wiggle({{wiggles:7,type:{chr(39)}easeOut{chr(39)}}})",{FEET},immediateRender:false}},{th + .6:.3f});')   # shakes the water off
        o.append(f'tl.to({ac},{{x:0,rotation:0,duration:.4,ease:"power2.inOut",{FEET}}},{th + 1.5:.3f});tl.to("#{t}_la",{{rotation:0,duration:.4,{SHL}}},{th + 1.5:.3f});')
        o.append(f'tl.to("#{t}_ra",{{rotation:-165,duration:.3,{SHR}}},{th + 1.6:.3f});tl.fromTo("#{t}_ra",{{rotation:-165,{SHR}}},{{rotation:-140,duration:.3,yoyo:true,repeat:3,ease:"sine.inOut",{SHR},immediateRender:false}},{th + 1.9:.3f});tl.to("#{t}_ra",{{rotation:0,duration:.4,{SHR}}},{th + 3.2:.3f});')   # wipes its face
        o.append(F('pout', th + 1.6))
        if T - th > 4.6: o.append(F('happy', th + 4.2))
        info['says'][0] = th + .15; info['nohead'] = True
    elif ty == 'swingride':   # hangs under a swing / pendulum by both hands; legs and body lag behind the swing
        per = float(at.get('data-per', 2.4 if kind == 'swing' else 1.2)); amp = float(at.get('data-amp', 28 if kind == 'swing' else 18))
        ta = v0 if v0 is not None else a0
        o.append(f'tl.set("#{t}_ra",{{rotation:-170,{SHR}}},0);tl.set("#{t}_la",{{rotation:170,{SHL}}},0);')
        n = max(int((T - ta) / (per / 2)), 1); lag = per / 7
        o.append(f'tl.fromTo({ac},{{rotation:{amp * .35:.1f},svgOrigin:"0 -34"}},{{rotation:{-amp * .35:.1f},duration:{per / 2:.3f},yoyo:true,repeat:{n},ease:"sine.inOut",svgOrigin:"0 -34",immediateRender:false}},{ta + lag:.3f});')
        o.append(f'tl.fromTo("#{t}_lgl,#{t}_lgr",{{rotation:{amp * .7:.1f}}},{{rotation:{-amp * .7:.1f},duration:{per / 2:.3f},yoyo:true,repeat:{n},ease:"sine.inOut",svgOrigin:"6 -10",immediateRender:false}},{ta + 2 * lag:.3f});')
        o.append(F('excited', a0)); info['says'][0] = a0 + .8; info['nohead'] = False
    elif ty == 'bumped':   # beside something that keeps bouncing: every landing jolts it off the ground a little, arms flap
        per = float(at.get('data-per', .9)); ta = (v0 if v0 is not None else a0) + P_TD * per
        o.append(F('surprised', a0)); j = 0; tm = ta
        while tm < T - .5:
            if tm >= a0:
                o.append(f'tl.to({ac},{{y:-11,duration:.12,ease:"power2.out"}},{tm:.3f});tl.to({ac},{{y:0,duration:.34,ease:"bounce.out"}},{tm + .12:.3f});')
                o.append(f'tl.to("#{t}_ra",{{rotation:-60,duration:.1,{SHR}}},{tm:.3f});tl.to("#{t}_ra",{{rotation:0,duration:.3,{SHR}}},{tm + .12:.3f});tl.to("#{t}_la",{{rotation:60,duration:.1,{SHL}}},{tm:.3f});tl.to("#{t}_la",{{rotation:0,duration:.3,{SHL}}},{tm + .12:.3f});')
                o += tuck(t, tm, .1, 0, .25, 20)
                if j == 2: o.append(F('laugh' if not act.get('serious') else 'squint', tm))
                j += 1
            tm += per
        info['says'][0] = ta + .1
    elif ty == 'blown':   # a gust: braced against the wind (facing it), pushed back sliding, then rolled over backward, lands sitting
        a1 = a0 + .4; info['nohead'] = True
        o += brace(t, a1, -26, 22) + [f'tl.to({ac},{{rotation:18,duration:.5,ease:"power2.out",{FEET}}},{a1:.3f});' + F('squint', a1)]
        o.append(f'tl.set("#{t}_wd",{{opacity:1}},{a1:.3f});tl.fromTo("#{t}_wd",{{x:40,opacity:0}},{{x:-120,opacity:.9,duration:.45,repeat:{max(int((T - a1) / .45) - 1, 1)},ease:"none",immediateRender:false}},{a1:.3f});')   # air streaks fly past (toward its back)
        o.append(f'tl.fromTo("#{t}_la",{{rotation:-40,{SHL}}},{{rotation:40,duration:.22,yoyo:true,repeat:7,ease:"sine.inOut",{SHL},immediateRender:false}},{a1:.3f});tl.fromTo("#{t}_ra",{{rotation:40,{SHR}}},{{rotation:-40,duration:.22,yoyo:true,repeat:7,ease:"sine.inOut",{SHR},immediateRender:false}},{a1:.3f});')
        tg = a1 + 1.9
        o.append(f'tl.to({TR},{{x:-60,duration:1.5,ease:"power1.in"}},{a1 + .4:.3f});')   # slides back on its heels
        o.append(F('shock', tg) + f'tl.to({TR},{{x:-200,duration:.75,ease:"power2.in"}},{tg:.3f});tl.to({RM},{{rotation:-360,duration:.75,ease:"power1.in",svgOrigin:"0 -34"}},{tg:.3f});')
        o.append(f'tl.to({ac},{{rotation:-70,duration:.01,{FEET}}},{tg + .75:.3f});tl.to({ac},{{rotation:-62,duration:.4,ease:"bounce.out",{FEET}}},{tg + .76:.3f});' + ''.join(unbrace(t, tg + .75, .2)))   # lands on its bottom, legs out
        o.append(f'tl.to("#{t}_lgl,#{t}_lgr",{{rotation:0,duration:.1}},{tg + .75:.3f});tl.to("#{t}_la,#{t}_ra",{{rotation:0,duration:.2}},{tg + .75:.3f});tl.set("#{t}_wd",{{opacity:0}},{tg + .8:.3f});')
        o.append(F('dizzy', tg + .8) + stars_js(t, tg + .8, 1.8))
        if T - tg > 3.4: o.append(f'tl.to({ac},{{rotation:0,duration:.6,ease:"back.out(1.3)",{FEET}}},{tg + 2.5:.3f});' + F('pout', tg + 2.5))
        info['says'][0] = tg
    elif ty == 'sidestep':   # under the dropping thing: looks up, hops aside at the last moment, the thing thuds beside it, wipes its brow
        if st is None: st, du = t0 + .15, .9
        th = st + P_TD * du; tj = th - .3; info['nohead'] = True
        o.append(f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-72}},duration:.3}},{a0:.3f});' + F('curious', a0) + F('shock', max(a0, tj - .25)))
        o += squash(t, tj - .12, .84, 1.1, .1, .1)
        o.append(f'tl.to({TR},{{x:{-150 / s:.1f},y:-46,duration:.22,ease:"power2.out"}},{tj:.3f});tl.to({TR},{{y:0,duration:.14,ease:"power2.in"}},{tj + .22:.3f});')   # hop backward (local -x), landing just before the thud
        if g: o.append(f'tl.to({g},{{y:{80 * s:.0f},duration:.45,ease:"bounce.out",immediateRender:false}},{st + du + .02:.3f});')   # the drop ends where the head was: once its own tween is over it falls the rest of the way to the ground
        o += tuck(t, tj, .15, 0, .2, 50) + squash(t, tj + .36, .88, 1.08, .08, .3)
        o.append(f'tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:0,duration:.2,{NECK}}},{th:.3f});tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-64,cx:"+=4"}},duration:.25}},{th + .1:.3f});')   # looks at the thing on the ground
        o.append(f'tl.to("#{t}_ra",{{rotation:-165,duration:.3,ease:"power2.out",{SHR}}},{th + .5:.3f});tl.fromTo("#{t}_ra",{{rotation:-165,{SHR}}},{{rotation:-140,duration:.3,yoyo:true,repeat:3,ease:"sine.inOut",{SHR},immediateRender:false}},{th + .8:.3f});tl.to("#{t}_ra",{{rotation:0,duration:.4,{SHR}}},{th + 2.1:.3f});')   # wipes its brow
        o.append(F('happy', th + .6)); info['says'][0] = th + .4
    elif ty == 'flattened':   # a BIG thing drops on it: pancaked under it, stars; crawls out from under, pops back, dizzy
        if st is None: st, du = t0 + .15, .9
        th = st + P_TD * du; info['nohead'] = True; info['noeyes'] = True
        o.append(f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-72}},duration:.3}},{a0:.3f});' + F('curious', a0) + F('shock', max(a0, th - .35)))
        o.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.2,{SHR}}},{max(a0, th - .3):.3f});tl.to("#{t}_la",{{rotation:150,duration:.2,{SHL}}},{max(a0, th - .3):.3f});')
        o.append(f'tl.to({ac},{{scaleY:.16,scaleX:1.7,duration:.08,ease:"power3.in",{FEET}}},{th:.3f});' + stars_js(t, th + .05, 2.2))
        info['says'][0] = th + .1; t2 = th + 1.5
        if T - t2 > 2.0:
            L = float(act.get('out', 150)) / s
            o.append(f'tl.to({TR},{{x:{L:.1f},duration:.9,ease:"power2.inOut"}},{t2:.3f});')   # crawls out forward (local +x)
            o.append(f'tl.to({ac},{{scaleY:1,scaleX:1,duration:.5,ease:"elastic.out(1,.45)",{FEET}}},{t2 + .6:.3f});tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.4}},{t2 + .6:.3f});')
            o.append(f'tl.set("#{t}_st,#{t}_spl,#{t}_spr",{{opacity:0}},{t2 + 1.3:.3f});' + F('dizzy', t2 + .6))
            o.append(f'tl.fromTo({ac},{{rotation:-8,{FEET}}},{{rotation:8,duration:.5,yoyo:true,repeat:3,ease:"sine.inOut",{FEET},immediateRender:false}},{t2 + 1.1:.3f});' + F('pout', min(t2 + 3.2, T - .3)))
            if len(d.get('says') or []) > 1: info['says'][1] = t2 + 1.4
    elif ty == 'trampoline':   # rides ON a bouncing thing: at every landing it squashes and is thrown higher than the thing, legs tucked, arms up
        per = float(at.get('data-per', .9)); hgt = float(at.get('data-h', 60)); ta = (v0 if v0 is not None else a0) + P_TD * per
        o.append(f'tl.set("#{t}_sh",{{opacity:0}},0);' + F('excited', a0)); j = 0; tm = ta; up = min(per * .42, .5); hop = min(max(hgt * .7, 40), 160) / s
        while tm < T - .6:
            if tm >= a0:
                o += squash(t, tm, .78, 1.18, .08, .12)
                o.append(f'tl.to({TR},{{y:{-hop:.1f},duration:{up:.3f},ease:"power2.out"}},{tm + .08:.3f});tl.to({TR},{{y:0,duration:{min(per - up - .1, up):.3f},ease:"power2.in"}},{tm + .08 + up:.3f});')
                o += tuck(t, tm + .1, .15, up - .2, .22, 55)
                o.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.2,{SHR}}},{tm + .08:.3f});tl.to("#{t}_la",{{rotation:150,duration:.2,{SHL}}},{tm + .08:.3f});tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.25}},{tm + per - .3:.3f});')
                if j == 2: o.append(F('laugh' if not act.get('serious') else 'happy', tm))
                j += 1
            tm += per
        info['says'][0] = ta + .2; info['nohead'] = True
    elif ty == 'knocked':   # stands where a big swinging thing reaches: it comes round and bowls the frog over backward (local -x), stars, sits up
        per = float(at.get('data-per', 2.4 if kind == 'swing' else 1.2)); ta = v0 if v0 is not None else a0
        tk = ta + (per / 2 if kind == 'swing' else per) - .06; info['nohead'] = True
        if tk < a0 + .3: tk += per if kind == 'pendulum' else per   # the next time it comes round
        o.append(F('curious', a0) + f'tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:-8,duration:.4,{NECK}}},{a0:.3f});')   # watches it come
        o.append(F('shock', tk) + f'tl.to({TR},{{x:{-170 / s:.1f},duration:.6,ease:"power2.out"}},{tk:.3f});tl.to({RM},{{rotation:-300,duration:.6,ease:"power1.out",svgOrigin:"0 -34"}},{tk:.3f});')
        o.append(f'tl.to({ac},{{rotation:-64,duration:.01,{FEET}}},{tk + .6:.3f});tl.to({ac},{{rotation:-58,duration:.3,ease:"bounce.out",{FEET}}},{tk + .61:.3f});tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:0,duration:.2,{NECK}}},{tk:.3f});')
        o.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.2,{SHR}}},{tk:.3f});tl.to("#{t}_la",{{rotation:150,duration:.2,{SHL}}},{tk:.3f});tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.3}},{tk + .7:.3f});')
        o += kicks(t, tk + .2, 4, .3, 22); o.append(stars_js(t, tk + .65, 2.0) + F('dizzy', tk + .7))
        info['says'][0] = tk + .05
        if T - tk > 3.4: o.append(f'tl.to({ac},{{rotation:0,duration:.6,ease:"back.out(1.3)",{FEET}}},{tk + 2.6:.3f});tl.set("#{t}_st,#{t}_spl,#{t}_spr",{{opacity:0}},{tk + 2.6:.3f});' + F('pout', tk + 2.6))
    elif ty == 'shockwave':   # beside a thing that slams down: the thud throws it up, arms and legs flailing, lands with a squash
        if st is None: st, du = t0 + .3, .28
        ts = st + (du if kind == 'slam' else .1); info['nohead'] = True
        o.append(F('curious', a0) + F('shock', ts) + f'tl.to({TR},{{y:{-95 / s:.1f},duration:.3,ease:"power2.out"}},{ts:.3f});tl.to({TR},{{y:0,duration:.3,ease:"power2.in"}},{ts + .3:.3f});')
        o.append(f'tl.to({ac},{{rotation:-12,duration:.3,ease:"power2.out",{FEET}}},{ts:.3f});tl.to({ac},{{rotation:0,duration:.3,{FEET}}},{ts + .3:.3f});')
        o.append(f'tl.to("#{t}_ra",{{rotation:-160,duration:.15,{SHR}}},{ts:.3f});tl.to("#{t}_la",{{rotation:160,duration:.15,{SHL}}},{ts:.3f});tl.fromTo("#{t}_lgl",{{rotation:40,{HIPL}}},{{rotation:-30,duration:.12,yoyo:true,repeat:4,ease:"sine.inOut",{HIPL},immediateRender:false}},{ts:.3f});tl.fromTo("#{t}_lgr",{{rotation:-40,{HIPR}}},{{rotation:30,duration:.12,yoyo:true,repeat:4,ease:"sine.inOut",{HIPR},immediateRender:false}},{ts:.3f});')
        o += squash(t, ts + .6, .8, 1.16, .1, .35); o.append(f'tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.3}},{ts + .65:.3f});tl.to("#{t}_lgl,#{t}_lgr",{{rotation:0,duration:.1}},{ts + .6:.3f});' + F('pout', ts + .9))
        info['says'][0] = ts + .1
        if T - ts > 2.8: o.append(F('surprised', ts + 2.4))
    elif ty == 'magnetized':   # holding the thing that gets yanked away: dragged along on its heels with it (same ease), lets go dizzy
        if st is None: st, du = t0 + .3, 1.5
        dx = abs(float(at.get('data-dx', -200))); dd = du if du else float(at.get('data-dur', .9)); info['nohead'] = True
        o.append(F('curious', a0) + f'tl.to("#{t}_ra",{{rotation:-85,duration:.3,{SHR}}},{a0:.3f});tl.to("#{t}_la",{{rotation:-100,duration:.3,{SHL}}},{a0:.3f});')   # both hands on it (it is on the facing side)
        o.append(F('shock', st) + f'tl.to({TR},{{x:{dx * .85 / s:.1f},duration:{dd:.3f},ease:"elastic.out(1,.6)"}},{st:.3f});tl.to({ac},{{rotation:-26,duration:.15,ease:"power2.out",{FEET}}},{st:.3f});')
        o += brace(t, st, -30, 26, .15)
        o.append(f'tl.set("#{t}_wd",{{opacity:1,scaleX:-1,svgOrigin:"0 0"}},{st:.3f});tl.fromTo("#{t}_wd",{{x:0,opacity:0}},{{x:60,opacity:.8,duration:.3,repeat:2,ease:"none",immediateRender:false}},{st:.3f});tl.set("#{t}_wd",{{opacity:0}},{st + .95:.3f});')   # heel streaks behind
        o.append(f'tl.to({ac},{{rotation:0,duration:.5,ease:"back.out(1.4)",{FEET}}},{st + dd * .6:.3f});' + ''.join(unbrace(t, st + dd * .6, .3)) + f'tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.4}},{st + dd * .6 + .2:.3f});' + F('dizzy', st + dd * .6))
        info['says'][0] = st + .1
        if T - st > 3.2: o.append(F('surprised', st + 2.8))
    elif ty == 'hopalong':   # beside a hopping creature: hops in time with it
        per = float(at.get('data-per', 1.4)); hgt = min(max(float(at.get('data-h', 40)) * .8, 28), 90) / s
        if st is None: st = t0 + .3
        tm = st; o.append(F('happy', a0)); j = 0
        while tm < T - .9:
            if tm >= a0:
                o += squash(t, tm, .9, 1.06, .12, .1)
                o.append(f'tl.to({TR},{{y:{-hgt:.1f},duration:.26,ease:"power2.out"}},{tm + .12:.3f});tl.to({TR},{{y:0,duration:.26,ease:"power2.in"}},{tm + .38:.3f});')
                o += tuck(t, tm + .12, .14, .1, .2, 45) + squash(t, tm + .64, .9, 1.06, .08, .25)
                if j == 1: o.append(F('excited', tm))
                j += 1
            tm += per
        info['says'][0] = st + .2; info['nohead'] = False
    elif ty == 'dripped':   # under a dripping thing: every drop lands on its head, it flinches, pouts, finally looks up
        per = float(at.get('data-per', 1.8)); cyc = .4 + per * .5
        if st is None: st = t0 + .3
        th = st + .3 + per * .5; j = 0; info['nohead'] = True
        o.append(F('curious', a0))
        while th < T - .4:
            if th >= a0:
                o.append(f'tl.to("#{t}_hd,#{t}_of,#{t}_te",{{scaleY:.9,duration:.06,ease:"power2.out",{NECK}}},{th:.3f});tl.to("#{t}_hd,#{t}_of,#{t}_te",{{scaleY:1,duration:.3,ease:"back.out(2)",{NECK}}},{th + .06:.3f});')
                o.append(f'tl.to({ac},{{rotation:-5,duration:.08,{FEET}}},{th:.3f});tl.to({ac},{{rotation:0,duration:.3,{FEET}}},{th + .08:.3f});tl.set("#{t}_spk",{{opacity:1}},{th:.3f});tl.set("#{t}_spk",{{opacity:0}},{th + .5:.3f});')
                o.append(F('pout' if j % 2 == 0 else 'squint', th + .05))
                if j == 1: o.append(f'tl.to("#{t}_ra",{{rotation:-125,duration:.25,{SHR}}},{th + .15:.3f});tl.to("#{t}_ra",{{rotation:0,duration:.4,{SHR}}},{th + .9:.3f});')   # hand over its head
                if j == 2: o.append(f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-72}},duration:.3}},{th + .4:.3f});tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:-10,duration:.4,{NECK}}},{th + .4:.3f});' + F('angry' if not act.get('serious') else 'worried', th + .5))   # looks up at the culprit
                j += 1
            th += cyc
        info['says'][0] = st + .3 + per * .5 + .1
    elif ty == 'rimride':   # clings to the rim of a spinning wheel and goes round with it: the frog stays OUTSIDE the group (an injected frog would shift the wheel's bbox centre) and orbits the wheel centre itself, dizzy after a turn
        per = max(float(at.get('data-per', 6)), .4); ta = v0 if v0 is not None else a0; dr = -1 if str(at.get('data-dir', '1')).startswith('-') else 1
        r = float(act.get('r', 200)) / s; turns = (T - ta) / per
        o.append(f'tl.set("#{t}_sh",{{opacity:0}},0);tl.set("#{t}_ra",{{rotation:-70,{SHR}}},0);tl.set("#{t}_la",{{rotation:70,{SHL}}},0);' + F('excited', a0))
        o.append(f'tl.fromTo("#{t}_in",{{rotation:0,svgOrigin:"0 {r:.1f}"}},{{rotation:{dr * d["flip"] * 360 * turns:.1f},duration:{T - ta:.3f},ease:"none",svgOrigin:"0 {r:.1f}",immediateRender:false}},{ta:.3f});')
        o.append(f'tl.fromTo("#{t}_lgl",{{rotation:30,{HIPL}}},{{rotation:40,duration:.3,yoyo:true,repeat:{max(int((T - a0) / .3), 1)},ease:"sine.inOut",{HIPL},immediateRender:false}},{a0:.3f});tl.set("#{t}_lgr",{{rotation:-35,{HIPR}}},0);')
        t1_ = max(a0 + .4, ta + per); info['nohead'] = True; info['noeyes'] = True
        if T - t1_ > .8: o.append(F('dizzy', t1_))
        if T - (ta + 2 * per) > .8: o.append(stars_js(t, ta + 2 * per, T - (ta + 2 * per) - .3))
    elif ty == 'launched':   # standing where a thing pops in: lifted up on top of it, arms flailing, sits on it swinging its legs
        if st is None: st, du = t0 + .3, .45
        hgt = float(act.get('h', 160)) / s; info['nohead'] = True; info['nolegs'] = True
        o.append(F('curious', a0) + F('shock', st) + f'tl.to({TR},{{y:{-hgt:.1f},duration:{du:.3f},ease:"back.out(1.4)"}},{st:.3f});')
        o.append(f'tl.to("#{t}_ra",{{rotation:-155,duration:.15,{SHR}}},{st:.3f});tl.to("#{t}_la",{{rotation:155,duration:.15,{SHL}}},{st:.3f});tl.fromTo("#{t}_ra",{{rotation:-155,{SHR}}},{{rotation:-125,duration:.12,yoyo:true,repeat:5,ease:"sine.inOut",{SHR},immediateRender:false}},{st + .15:.3f});')
        o += tuck(t, st, .2, .2, .3, 45)
        o.append(f'tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.4}},{st + du + .5:.3f});' + F('surprised', st + du + .3) + f'tl.set("#{t}_sh",{{opacity:0}},{st + .1:.3f});')
        o += kicks(t, st + du + .6, 7, .5, 18); o.append(F('happy', st + du + 1.4)); info['says'][0] = st + .25
    elif ty == 'unrolled':   # on the lane of a carpet / scroll unrolling toward it: swept off its feet when the edge arrives, lands on its back
        if st is None: st, du = t0 + .3, .8
        tr_ = st + ease_inv('power2.out', float(act.get('frac', .7))) * du; info['nohead'] = True
        o.append(F('curious', a0) + f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cx:"+=4"}},duration:.3}},{a0:.3f});')
        o.append(F('shock', tr_) + f'tl.to({TR},{{x:{90 / s:.1f},y:-30,duration:.25,ease:"power2.out"}},{tr_:.3f});tl.to({TR},{{y:0,duration:.2,ease:"power2.in"}},{tr_ + .25:.3f});')   # carried a little along the unroll (local +x)
        o.append(f'tl.to({ac},{{rotation:-80,duration:.4,ease:"power2.in",{FEET}}},{tr_:.3f});tl.to({ac},{{rotation:-72,duration:.25,ease:"bounce.out",{FEET}}},{tr_ + .4:.3f});')
        o.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.2,{SHR}}},{tr_:.3f});tl.to("#{t}_la",{{rotation:150,duration:.2,{SHL}}},{tr_:.3f});tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.3}},{tr_ + .7:.3f});')
        o += kicks(t, tr_ + .2, 4, .3, 22); o.append(stars_js(t, tr_ + .5, 1.8) + F('dizzy', tr_ + .5)); info['says'][0] = tr_ + .05
        if T - tr_ > 3.2: o.append(f'tl.to({ac},{{rotation:0,duration:.6,ease:"back.out(1.3)",{FEET}}},{tr_ + 2.4:.3f});tl.set("#{t}_st,#{t}_spl,#{t}_spr",{{opacity:0}},{tr_ + 2.4:.3f});' + F('pout', tr_ + 2.4))
    elif ty in ('balloonride', 'sinkride'):   # hangs under a rising thing with its legs kicking / stands on a sinking thing waving for help
        o.append(f'tl.set("#{t}_sh",{{opacity:0}},0);')
        if ty == 'balloonride':
            o.append(f'tl.set("#{t}_ra",{{rotation:-170,{SHR}}},0);tl.set("#{t}_la",{{rotation:170,{SHL}}},0);' + F('excited', a0))
            o += kicks(t, a0 + .3, max(int((T - a0) / .45), 2), .9, 16); info['nohead'] = False
        else:
            o.append(F('worried', a0) + f'tl.to("#{t}_ra",{{rotation:-165,duration:.3,{SHR}}},{a0 + .3:.3f});tl.fromTo("#{t}_ra",{{rotation:-165,{SHR}}},{{rotation:-135,duration:.3,yoyo:true,repeat:{max(int((T - a0 - 1) / .3), 2)},ease:"sine.inOut",{SHR},immediateRender:false}},{a0 + .6:.3f});')
            o.append(f'tl.to("#{t}_la",{{rotation:150,duration:.3,{SHL}}},{a0 + .4:.3f});tl.fromTo("#{t}_la",{{rotation:150,{SHL}}},{{rotation:120,duration:.3,yoyo:true,repeat:{max(int((T - a0 - 1) / .3), 2)},ease:"sine.inOut",{SHL},immediateRender:false}},{a0 + .7:.3f});')
            o.append(f'tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:-10,duration:.5,{NECK}}},{a0 + .3:.3f});'); info['nohead'] = True
        info['says'][0] = a0 + .6
    elif ty == 'tug':   # both hands on a rope on its facing side: leans back and heaves three times, slips, lands on its bottom, gets up
        a1 = a0 + .4; info['nohead'] = True
        o.append(f'tl.to("#{t}_ra",{{rotation:-75,duration:.3,{SHR}}},{a1:.3f});tl.to("#{t}_la",{{rotation:-105,duration:.3,{SHL}}},{a1:.3f});' + F('determined', a1))
        o += brace(t, a1, -30, 26); o.append(f'tl.set("#{t}_sw",{{opacity:1}},{a1 + .5:.3f});')
        for j in range(3):
            tm = a1 + .5 + j * 1.0
            o.append(f'tl.to({ac},{{rotation:-24,x:-6,duration:.45,ease:"power2.out",{FEET}}},{tm:.3f});tl.to({ac},{{rotation:-12,x:2,duration:.5,ease:"sine.inOut",{FEET}}},{tm + .45:.3f});')
            o.append(f'tl.fromTo("#{t}_sw{j}",{{y:0,opacity:1}},{{y:30,opacity:0,duration:.8,ease:"power1.in",immediateRender:false}},{tm + .2:.3f});')
        ts = a1 + 3.5
        o.append(F('shock', ts) + f'tl.to({ac},{{rotation:-78,x:-14,duration:.22,ease:"power3.in",{FEET}}},{ts:.3f});tl.to({ac},{{rotation:-62,x:-12,duration:.3,ease:"bounce.out",{FEET}}},{ts + .22:.3f});')
        o.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.2,{SHR}}},{ts:.3f});tl.to("#{t}_la",{{rotation:150,duration:.2,{SHL}}},{ts:.3f});' + ''.join(unbrace(t, ts, .2)) + f'tl.set("#{t}_sw",{{opacity:0}},{ts:.3f});')
        o += kicks(t, ts + .25, 3, .3, 20)
        info['says'][0] = a1 + .6; info['says'][1] = ts + .1
        if T - ts > 2.6: o.append(f'tl.to({ac},{{rotation:0,x:0,duration:.6,ease:"back.out(1.3)",{FEET}}},{ts + 1.6:.3f});tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.4}},{ts + 1.6:.3f});' + F('pout', ts + 1.6))
    elif ty == 'lift':   # under a rising load with both arms up, knees shaking, sweat; rides up with it (inside the group)
        if st is None: st, du = t0 + .3, .5
        o.append(f'tl.set("#{t}_ra",{{rotation:-165,{SHR}}},0);tl.set("#{t}_la",{{rotation:165,{SHL}}},0);' + F('determined', a0))
        o += brace(t, a0, -14, 12, .01)
        n = max(int((T - a0 - .3) / .14), 4)
        o.append(f'tl.fromTo("#{t}_lgl",{{rotation:12,{HIPL}}},{{rotation:18,duration:.07,yoyo:true,repeat:{n},ease:"none",{HIPL},immediateRender:false}},{a0 + .3:.3f});tl.fromTo("#{t}_lgr",{{rotation:-14,{HIPR}}},{{rotation:-20,duration:.07,yoyo:true,repeat:{n},ease:"none",{HIPR},immediateRender:false}},{a0 + .3:.3f});')   # knees shaking
        o.append(f'tl.fromTo({ac},{{scaleY:.94,{FEET}}},{{scaleY:.9,duration:.5,yoyo:true,repeat:{max(int((T - a0) / .5), 1)},ease:"sine.inOut",{FEET},immediateRender:false}},{a0:.3f});')
        o.append(f'tl.set("#{t}_sw",{{opacity:1}},{a0 + .5:.3f});tl.fromTo("#{t}_sw0,#{t}_sw1,#{t}_sw2",{{y:0,opacity:1}},{{y:28,opacity:0,duration:1.0,stagger:.33,repeat:{max(int((T - a0) / 1.5), 1)},ease:"power1.in",immediateRender:false}},{a0 + .5:.3f});')
        info['says'][0] = max(a0 + .6, st + du + .2)
    elif ty == 'catch':   # under the dropping thing: arms up, catches it at touchdown, knees bend, staggers back two steps, proud
        if st is None: st, du = t0 + .15, .9
        th = st + P_TD * du
        o.append(f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-72}},duration:.3}},{a0:.3f});' + F('determined', a0))
        o.append(f'tl.to("#{t}_ra",{{rotation:-160,duration:.3,ease:"power2.out",{SHR}}},{max(a0, th - .5):.3f});tl.to("#{t}_la",{{rotation:160,duration:.3,ease:"power2.out",{SHL}}},{max(a0, th - .5):.3f});')
        o += squash(t, th, .86, 1.08, .1, .35); o += brace(t, th, -18, 16, .12)
        o.append(f'tl.to({TR},{{x:-18,duration:.25,ease:"power2.out"}},{th:.3f});tl.to({TR},{{x:-34,duration:.3,ease:"power2.out"}},{th + .35:.3f});')   # two small steps back
        o.append(f'tl.to({ac},{{rotation:-10,duration:.25,ease:"power2.out",{FEET}}},{th:.3f});tl.to({ac},{{rotation:0,duration:.5,ease:"back.out(1.5)",{FEET}}},{th + .5:.3f});')
        o += unbrace(t, th + .7); o.append(F('shock', th) + F('proud', th + .9))
        o.append(f'tl.to("#{t}_pl,#{t}_pr",{{attr:{{cy:-66}},duration:.3}},{th + .9:.3f});')
        info['says'][0] = th + .9; info['nohead'] = True
    elif ty == 'trip':   # runs along (local +x), catches its foot on a low thing at fraction frac of the way, tumbles, lies, gets up and walks on
        L = float(act.get('dist', 300)) / s; fr = min(max(float(act.get('frac', .55)), .2), .8); ta = a0 + .4; te = T - .3
        if te - ta < 2.0: fr = .5
        run_t = max(.8, (te - ta) * .38); tt = ta + run_t   # reaches the obstacle
        per = .44; info['nohead'] = True
        o.append(f'tl.to({TR},{{x:{L * fr:.1f},duration:{run_t:.3f},ease:"none"}},{ta:.3f});')
        tm = ta
        while tm < tt - .05:
            o.append(f'tl.to({TR},{{y:-16,duration:{per / 2:.2f},ease:"power2.out"}},{tm:.3f});tl.to({TR},{{y:0,duration:{per / 2:.2f},ease:"power2.in"}},{tm + per / 2:.3f});'); tm += per
        o += legs_cycle(t, ta, tt, per, 30) + arms_swing(t, ta, tt, per, 24)
        o.append(f'tl.to({RM},{{rotation:10,duration:.3,svgOrigin:"0 0"}},{ta:.3f});' + F('happy', a0))
        o.append(F('shock', tt) + f'tl.to({TR},{{x:{L * fr + 70:.1f},y:-30,duration:.3,ease:"power1.out"}},{tt:.3f});tl.to({TR},{{y:0,duration:.25,ease:"power2.in"}},{tt + .3:.3f});')
        o.append(f'tl.to({RM},{{rotation:92,duration:.5,ease:"power2.in",svgOrigin:"0 -34"}},{tt:.3f});tl.to({RM},{{rotation:84,duration:.25,ease:"power1.out",svgOrigin:"0 -34"}},{tt + .55:.3f});tl.to({RM},{{rotation:90,duration:.2,svgOrigin:"0 -34"}},{tt + .8:.3f});')   # face down
        o.append(f'tl.to("#{t}_ra",{{rotation:-100,duration:.3,{SHR}}},{tt:.3f});tl.to("#{t}_la",{{rotation:-80,duration:.3,{SHL}}},{tt:.3f});')
        o += kicks(t, tt + .4, 3, .3, 18); o.append(stars_js(t, tt + .55, 1.6))
        info['says'][0] = tt + .3
        t3 = tt + 2.1
        if te - t3 > 1.6:
            o.append(f'tl.to({RM},{{rotation:0,duration:.7,ease:"back.out(1.2)",svgOrigin:"0 0"}},{t3:.3f});tl.to("#{t}_la",{{rotation:0,duration:.4,{SHL}}},{t3:.3f});' + F('pout', t3))
            o.append(f'tl.to("#{t}_ra",{{rotation:-165,duration:.4,{SHR}}},{t3 + .5:.3f});tl.to("#{t}_ra",{{rotation:0,duration:.4,{SHR}}},{t3 + 1.5:.3f});')   # rubs its head
            if te - t3 > 3.0:   # walks on, slower, limping a little
                t4 = t3 + 1.9; per2 = .66
                o.append(f'tl.to({TR},{{x:{L * fr + 70 + min(L * (1 - fr) * .6, 140):.1f},duration:{te - t4:.3f},ease:"none"}},{t4:.3f});')
                tm = t4
                while tm < te - .1:
                    o.append(f'tl.to({TR},{{y:-7,duration:{per2 / 2:.2f},ease:"power2.out"}},{tm:.3f});tl.to({TR},{{y:0,duration:{per2 / 2:.2f},ease:"power2.in"}},{tm + per2 / 2:.3f});'); tm += per2
                o += legs_cycle(t, t4, te, per2, 18) + [F('happy', t4 + .8)]
    return o, info


# ---------------------------------------------------------------- locomotion + costume acts (miya 2026-10-29: "add running, jumping, hanging,
# swimming ... and things tied to the frog's costumes") ----------------------------------------------------------------
# Data-driven acts: ra / la = (from, to, period) yoyo arm swings or a single angle; legs = ('cycle'|'brace'|'kicks'|'tuck', amp, period);
# body = (from dict, to dict, period) yoyo on #_ac; head = (deg, period) yoyo on the head; travel = local x distance factor of act['dist']
# (0 = in place) with hop (height, period); mouth = open-mouth ry held; stars = magic sparkles over the head; mood = first face; prop = part id shown.
COSTUME_ACTS = {
 'castspell':  dict(ra=(-120, -165, .5), la=-20, legs=('brace', -10, 8), body=({'rotation': -4}, {'rotation': 4}, 1.0), stars=True, mood='mischief'),            # wizard: wand arm circles, sparkles over the head
 'charge':     dict(ra=-160, la=-40, legs=('cycle', 30, .42), travel=.8, hop=(16, .42), body=({'rotation': 10}, {'rotation': 14}, .42), mood='determined', mouth=8),   # knight / viking / roman / samurai: fist up, storms forward
 'stir':       dict(ra=(-60, -100, .45), la=-20, body=({'rotation': 0, 'x': 0}, {'rotation': 3, 'x': 3}, .9), head=(-6, 1.8), mood='happy'),                           # chef: stirs the pot, sniffs
 'hose':       dict(ra=-85, la=-105, legs=('brace', -24, 20), body=({'rotation': -14, 'x': -4}, {'rotation': -10, 'x': 2}, .32), mood='determined'),                    # firefighter: both hands on the hose, kicked back by the jet
 'lasso':      dict(ra=(-130, -170, .22), la=-30, legs=('brace', -14, 12), body=({'rotation': -3}, {'rotation': 3}, .44), head=(5, .9), mood='excited'),                # cowboy: rope whirls over the head
 'flap':       dict(ra=(-30, -120, .32), la=(30, 120, .32), legs=('tuck', 30, 0), rise=-46, body=({'y': -4}, {'y': 4}, .64), mood='happy'),                              # wings / bee / aviator: flaps and lifts off a little
 'bunnyhop':   dict(legs=('tuck', 45, 0), hop=(26, .7), travel=.6, ra=-120, la=120, body=({'rotation': 2}, {'rotation': -2}, .7), mood='happy'),                        # bunny: quick double-hops along
 'groove':     dict(head=(9, .5), legs=('tap', 14, .5), ra=(-10, -30, .5), la=(20, 40, .5), body=({'y': 0}, {'y': -3}, .5), mood='happy'),                              # headphones: head bob, foot tap
 'hammer':     dict(ra=(-130, -30, .55), la=-70, legs=('brace', -14, 10), body=({'rotation': -4, 'y': 0}, {'rotation': 8, 'y': 3}, .55), mood='determined'),            # hardhat: hammer arm comes down again and again
 'sow':        dict(ra=(-40, -100, .9), la=-20, legs=('cycle', 16, 1.2), travel=.5, hop=(5, 1.2), head=(4, 2.4), mood='happy'),                                            # strawhat: walks along scattering seeds
 'cool':       dict(ra=108, la=-108, body=({'rotation': -6, 'y': 0}, {'rotation': -8, 'y': -1}, 1.6), head=(-6, 2.2), legs=('brace', -6, 16), mood='smug'),            # sunglasses: arms crossed, leaning back, slow nod
 'hohoho':     dict(ra=(-120, -150, .9), la=-20, body=({'scaleY': 1}, {'scaleY': .95}, .3), head=(6, .9), mood='laugh', mouth=9),                                        # santa: belly bounces, hand waves
 'floatghost': dict(ra=-95, la=95, rise=-18, body=({'y': -12, 'rotation': -3}, {'y': 10, 'rotation': 3}, 2.4), legs=('tuck', 20, 0), mood='mischief', mouth=7),           # ghost / halo: hovers with arms out front
 'chomp':      dict(ra=-70, la=-70, body=({'rotation': 6, 'x': 0}, {'rotation': 16, 'x': 12}, .5), legs=('brace', -20, 16), mouthcycle=(11, .5), mood='mischief'),        # shark: lunges and snaps its mouth
 'stomp':      dict(legs=('cycle', 34, 1.1), travel=.5, hop=(10, 1.1), ra=-50, la=-50, body=({'rotation': 6}, {'rotation': 2}, 1.1), stompshake=True, mood='angry', mouth=10),   # dino: heavy stamping steps
 'jog':        dict(legs=('cycle', 32, .36), ra=(-40, -90, .36), la=(40, 90, .36), hop=(10, .36), body=({'rotation': 4}, {'rotation': 6}, .36), mood='determined'),       # headband: jogging on the spot
 'halt':       dict(ra=-95, la=20, legs=('tap', 12, 1.0), body=({'rotation': 0}, {'rotation': -3}, 1.0), head=(-4, 2.0), mood='angry'),                                   # police: hand raised, foot tapping
 'victory':    dict(ra=(-140, -165, .3), la=(140, 165, .3), hop=(14, .6), body=({'rotation': -3}, {'rotation': 3}, .6), mood='proud', mouth=8),                             # medal / laurel: fists pumping
 'vrgrab':     dict(ra=(-40, -120, .7), la=(80, 140, .9), body=({'rotation': -8, 'x': -4}, {'rotation': 8, 'x': 4}, 1.4), legs=('cycle', 10, 1.4), head=(10, 1.4), mood='confused'),   # vr: gropes about blindly
 'hike':       dict(legs=('cycle', 22, .8), travel=.6, hop=(7, .8), ra=(-20, -50, .8), la=(20, 50, .8), body=({'rotation': 5}, {'rotation': 7}, .8), wipe=True, mood='determined'),      # backpack: marches on, wipes its brow halfway
 'paddle':     dict(ra=(-50, -130, .8), la=(-130, -50, .8), body=({'rotation': -6, 'x': -3}, {'rotation': 6, 'x': 4}, .8), legs=('brace', -30, 30), mood='determined'),                 # lifevest: paddles, leaning with each stroke
 'puddlejump': dict(legs=('tuck', 50, 0), hop=(42, 1.6), splash=True, ra=-150, la=150, mood='laugh', mouth=8),                                                             # raincoat: jumps into a puddle, drops fly
 'rubhands':   dict(ra=(100, 118, .18), la=(-100, -118, .18), body=({'scaleY': 1, 'x': -1}, {'scaleY': .98, 'x': 1}, .36), head=(3, .36), mood='chilly'),               # scarf / beanie: rubs its hands, shivering
 'regal':      dict(ra=(-135, -150, .5), la=20, body=({'rotation': -4}, {'rotation': -6}, 2.2), head=(-7, 2.2), legs=('brace', -6, 6), mood='smug'),                     # crown / top hat / monocle: the little royal wave, nose up
 'alienwave':  dict(ra=(-150, -170, .35), la=(150, 170, .35), head=(12, .9), body=({'y': -2}, {'y': 2}, .7), mood='curious', mouth=6),                                   # alien: both arms up, head tilting
 'mustache':   dict(ra=152, la=20, body=({'rotation': 2}, {'rotation': -2}, 2.0), head=(-5, 2.0), strokem=True, mood='smug'),                                            # mustache: strokes it, nodding wisely
 'coverears':  dict(ra=-128, la=128, body=({'rotation': 0, 'y': 0}, {'rotation': -3, 'y': 2}, .6), flinch=1.4, mood='squint'),                                          # earmuffs: hands over the ears, flinches at each bang
 'limp':       dict(legs=('limp', 26, .9), travel=.4, hop=(4, .9), ra=(-20, -40, .9), la=30, body=({'rotation': 4, 'y': 0}, {'rotation': 8, 'y': 3}, .9), mood='hurt'),   # bandage: hobbles along
 'sniff':      dict(ra=-40, la=20, body=({'rotation': 18, 'y': 2}, {'rotation': 20, 'y': 2}, 2.0), head=(4, 1.0), sniffup=True, mood='love'),                            # flower crown: bends to a flower, lifts it to its nose
 'paint':      dict(ra=(-62, -84, .4), la=-110, body=({'rotation': -4, 'x': -2}, {'rotation': 2, 'x': 2}, 1.6), head=(6, 1.6), prop='pc', mood='curious'),             # beret: dabs at a canvas, steps back to look
 'windbrella': dict(ra=20, la=170, legs=('brace', -22, 18), body=({'rotation': 10, 'x': 0}, {'rotation': 16, 'x': 4}, .7), gustlift=True, mood='worried', prop='um'),    # umbrella: the wind tugs it, lifts the frog in gusts
 'juggle':     dict(ra=(-70, -110, .3), la=(110, 70, .3), head=(-4, .6), body=({'y': 0}, {'y': -2}, .3), juggle=True, mood='happy'),                                    # clown / party hat: juggles three balls (the sweat drops stand in as balls)
 'hideshell':  dict(ra=140, la=-140, body=({'scaleY': 1}, {'scaleY': .72}, 2.6), head=(0, 1), tuckhead=True, mood='worried'),                                           # turtle: pulls its head in, peeks out
 'pray':       dict(ra=118, la=-118, body=({'y': 0}, {'y': -1}, 2.2), head=(-6, 2.2), rise=-10, mood='love'),                                                            # halo: hands together, floats up a little
 'tosscap':    dict(ra=(-20, -165, .5), la=120, hop=(18, 1.4), legs=('tuck', 30, 0), body=({'rotation': 0}, {'rotation': -5}, 1.4), mood='proud', mouth=8),             # gradcap: throws its cap arm up and hops
 'dig2':       dict(ra=(-30, -80, .7), la=-70, legs=('brace', -16, 14), body=({'rotation': 12, 'y': 3}, {'rotation': -2, 'y': -2}, .7), prop='sv', mood='curious'),      # headlamp / explorer: digs with the shovel
 'stretchlegs': dict(legs=('cycle', 40, 1.6), ra=(-150, -165, 1.6), la=(150, 165, 1.6), body=({'scaleY': 1}, {'scaleY': 1.06}, 1.6), mood='sleepy', mouth=9),           # propcap / toy: big slow stretches
 'bob':        dict(ra=-100, la=100, body=({'y': -5, 'rotation': -5}, {'y': 5, 'rotation': 5}, 1.6), legs=('kicks', 14, 1.6), mood='happy'),                            # lifevest in water: bobs with arms out
}
# hand-written locomotion acts (frog_rig.contact_js handles them): real swimming, climbing, a running leap, hanging by one hand and slipping,
# skating, a somersault, sneaking, crawling, log-rolling, tightrope walking
LOCO = ('swimstroke', 'climb', 'leap', 'dangle', 'skate', 'somersault', 'tiptoe', 'crawl', 'logroll', 'tightrope')
MOVES = tuple(COSTUME_ACTS) + LOCO
TRAVEL_ACTS = tuple(a for a, v in COSTUME_ACTS.items() if v.get('travel')) + ('swimstroke', 'leap', 'skate', 'tiptoe', 'crawl', 'logroll', 'tightrope', 'charge')   # frog_place gives these a lane (x, dist) like a roam
# costume -> act when the sentence gave no situation (frog_place, after the word rules); first key that matches the outfit list
OUTFIT_ACT = {'wizard': 'castspell', 'knight': 'charge', 'viking': 'charge', 'roman': 'charge', 'samurai': 'charge', 'chef': 'stir', 'firefighter': 'hose', 'cowboy': 'lasso',
              'wings': 'flap', 'bee': 'flap', 'aviator': 'flap', 'bunny': 'bunnyhop', 'headphones': 'groove', 'hardhat': 'hammer', 'strawhat': 'sow', 'sunglasses': 'cool',
              'santa': 'hohoho', 'ghost': 'floatghost', 'shark': 'chomp', 'dino': 'stomp', 'headband': 'jog', 'police': 'halt', 'medal': 'victory', 'laurel': 'victory',
              'vr': 'vrgrab', 'backpack': 'hike', 'explorer': 'hike', 'lifevest': 'paddle', 'raincoat': 'puddlejump', 'scarf': 'rubhands', 'beanie': 'rubhands',
              'crown': 'regal', 'tophat': 'regal', 'monocle': 'regal', 'bowtie': 'regal', 'alien': 'alienwave', 'mustache': 'mustache', 'earmuffs': 'coverears',
              'bandage': 'limp', 'flowercrown': 'sniff', 'crownleaf': 'sniff', 'beret': 'paint', 'umbrella': 'windbrella', 'clown': 'juggle', 'partyhat': 'juggle',
              'turtle': 'hideshell', 'halo': 'pray', 'gradcap': 'tosscap', 'headlamp': 'dig2', 'propcap': 'stretchlegs', 'diver': 'swimstroke', 'goggles': 'swimstroke',
              'pirate': 'scope', 'detective': 'magnify', 'glasses': 'think', 'doctor': 'magnify', 'lab': 'magnify', 'nightcap': 'snooze', 'helmet': 'float', 'cape': 'fly', 'tinfoil': 'look'}
OUTFIT_SAYS = {'castspell': 'Abracadabra!', 'charge': 'Chaaarge!', 'stir': 'Mmm!', 'hose': 'Whoosh!', 'lasso': 'Yeehaw!', 'flap': 'Flap flap!', 'bunnyhop': 'Boing boing!', 'groove': 'La la la~',
               'hammer': 'Bang! Bang!', 'sow': 'Grow, grow!', 'cool': 'Cool.', 'hohoho': 'Ho ho ho!', 'floatghost': 'Boooo!', 'chomp': 'Chomp!', 'stomp': 'ROAR!', 'jog': 'Hup hup!', 'halt': 'Halt!',
               'victory': 'Yes!', 'vrgrab': 'Whoa...', 'hike': 'Onward!', 'paddle': 'Row, row!', 'puddlejump': 'Splash!', 'rubhands': 'Brrr!', 'regal': 'Hm-hm.', 'alienwave': 'Bleep!', 'mustache': 'Indeed.',
               'coverears': 'Too loud!', 'limp': 'Ow, ow.', 'sniff': 'Ahh~', 'paint': 'Hmm, hmm.', 'windbrella': 'Whoa-oa!', 'juggle': 'Ta-da!', 'hideshell': 'Eep.', 'pray': '...', 'tosscap': 'Hooray!',
               'dig2': 'Dig, dig!', 'stretchlegs': 'Ahh...', 'bob': 'Blub!', 'swimstroke': 'Blub blub!', 'climb': 'Up we go!', 'leap': 'Wheee!', 'dangle': 'Uh-oh...', 'skate': 'Wheee!',
               'somersault': 'Ta-da!', 'tiptoe': 'Shh...', 'crawl': 'Hup...', 'logroll': 'Waaah!', 'tightrope': 'Steady...'}


def generic_js(t, d, A, a0, T, k, F, act):
    """interpreter for COSTUME_ACTS"""
    o = []; info = dict(nohead=bool(A.get('head')) or bool(A.get('tuckhead')), nolegs=bool(A.get('legs')) or bool(A.get('hop')), noscale=any('scaleY' in x for x in (A.get('body') or ({}, {}))[:2]), noeyes=False, says={0: a0 + .9})
    ac = f'"#{t}_ac"'; TR = f'"#{t}_tr"'; a1 = a0 + .35; span = T - a1
    if span < .8: return o, info
    if A.get('mood'): o.append(F(A['mood'], a0))
    if A.get('prop'): o.append(f'tl.set("#{t}_{A["prop"]}",{{opacity:1}},{a0:.3f});')
    for arm, key, org in (('ra', 'ra', SHR), ('la', 'la', SHL)):
        v = A.get(key)
        if v is None: continue
        if isinstance(v, tuple):
            f0, f1, per = v; n = max(int((span - .3) / per), 1)
            o.append(f'tl.fromTo("#{t}_{arm}",{{rotation:{f0},{org}}},{{rotation:{f1},duration:{per},yoyo:true,repeat:{n},ease:"sine.inOut",{org},immediateRender:false}},{a1:.3f});')
        else: o.append(f'tl.to("#{t}_{arm}",{{rotation:{v},duration:.35,ease:"power2.out",{org}}},{a1:.3f});')
    lg = A.get('legs')
    if lg:
        kd, amp, per = lg
        if kd == 'cycle': o += legs_cycle(t, a1, T - .2, per, amp)
        elif kd == 'brace': o += brace(t, a1, amp, per)
        elif kd == 'kicks': o += kicks(t, a1, max(int(span / (per / 2)), 2), per, amp)
        elif kd == 'tuck': o.append(f'tl.to("#{t}_lgl",{{rotation:{amp},duration:.3,{HIPL}}},{a1:.3f});tl.to("#{t}_lgr",{{rotation:{-amp},duration:.3,{HIPR}}},{a1:.3f});')
        elif kd == 'tap':
            n = max(int(span / per), 1)
            o.append(f'tl.fromTo("#{t}_lgr",{{rotation:0,{HIPR}}},{{rotation:{-amp},duration:{per / 2:.3f},yoyo:true,repeat:{2 * n - 1},ease:"power1.inOut",{HIPR},immediateRender:false}},{a1:.3f});')
        elif kd == 'limp':
            n = max(int(span / (per / 2)), 1)
            o.append(f'tl.fromTo("#{t}_lgl",{{rotation:{-amp},{HIPL}}},{{rotation:{amp},duration:{per / 2:.3f},yoyo:true,repeat:{n},ease:"sine.inOut",{HIPL},immediateRender:false}},{a1:.3f});')
            o.append(f'tl.fromTo("#{t}_lgr",{{rotation:6,{HIPR}}},{{rotation:-8,duration:{per / 2:.3f},yoyo:true,repeat:{n},ease:"sine.inOut",{HIPR},immediateRender:false}},{a1:.3f});')   # the stiff leg barely moves
    if A.get('body'):
        fr, to, per = A['body']; n = max(int((span - .3) / per), 1); jsd = lambda d_: ','.join(f'{q}:{v}' for q, v in d_.items())
        o.append(f'tl.fromTo({ac},{{{jsd(fr)},{FEET}}},{{{jsd(to)},duration:{per},yoyo:true,repeat:{n},ease:"sine.inOut",{FEET},immediateRender:false}},{a1:.3f});')
    if A.get('head'):
        deg, per = A['head']; n = max(int((span - .3) / per), 1)
        o.append(f'tl.fromTo("#{t}_hd,#{t}_of,#{t}_te",{{rotation:{-deg * .4:.1f},{NECK}}},{{rotation:{deg},duration:{per},yoyo:true,repeat:{n},ease:"sine.inOut",{NECK},immediateRender:false}},{a1:.3f});')
    if A.get('hop'):
        hh, per = A['hop']; tm = a1
        while tm < T - per:
            o.append(f'tl.to({TR},{{y:{-hh},duration:{per / 2:.3f},ease:"power2.out"}},{tm:.3f});tl.to({TR},{{y:0,duration:{per / 2:.3f},ease:"power2.in"}},{tm + per / 2:.3f});')
            if A.get('stompshake'): o.append(f'tl.fromTo("#{t}_in",{{x:0}},{{x:3,duration:.3,ease:"wiggle({{wiggles:4,type:{chr(39)}easeOut{chr(39)}}})",immediateRender:false}},{tm + per:.3f});')
            if A.get('splash'):
                for i in range(6): o.append(f'tl.fromTo("#{t}_sp{i}",{{x:0,y:0,opacity:1}},{{x:{-50 + i * 20},y:{-60 - (i % 3) * 14},duration:.3,ease:"power1.out",immediateRender:false}},{tm + per:.3f});tl.to("#{t}_sp{i}",{{y:20,opacity:0,duration:.35,ease:"power1.in"}},{tm + per + .3:.3f});')
                o.append(f'tl.set("#{t}_spk",{{opacity:1}},{tm + per:.3f});tl.set("#{t}_spk",{{opacity:0}},{tm + per + .7:.3f});'); o += squash(t, tm + per, .8, 1.15, .1, .35)
            tm += per * (2 if A.get('splash') else 1)
    if A.get('travel'):
        L = float(act.get('dist', 300)) / d['s'] * A['travel']
        o.append(f'tl.to({TR},{{x:{L:.1f},duration:{span - .2:.3f},ease:"none"}},{a1:.3f});')
    if A.get('rise'): o.append(f'tl.to({TR},{{y:{A["rise"]},duration:1.4,ease:"power1.out"}},{a1:.3f});')
    if A.get('mouth'): o.append(f'tl.set("#{t}_sm",{{opacity:0}},{a1:.3f});tl.set("#{t}_mo",{{attr:{{ry:{A["mouth"]},cy:{-44 + A["mouth"]}}}}},{a1:.3f});')
    if A.get('mouthcycle'):
        ry, per = A['mouthcycle']; n = max(int(span / per), 1)
        o.append(f'tl.set("#{t}_sm",{{opacity:0}},{a1:.3f});tl.fromTo("#{t}_mo",{{attr:{{ry:0,cy:-44}}}},{{attr:{{ry:{ry},cy:{-44 + ry}}},duration:{per / 2:.3f},yoyo:true,repeat:{2 * n - 1},ease:"power2.inOut",immediateRender:false}},{a1:.3f});')
    if A.get('stars'): o.append(stars_js(t, a1 + .3, max(span - .6, .5), swirl=False))   # sparkles only, no swirl eyes
    if A.get('wipe') and span > 4: tm = a1 + span / 2; o.append(f'tl.to("#{t}_ra",{{rotation:-165,duration:.35,{SHR},overwrite:"auto"}},{tm:.3f});tl.to("#{t}_ra",{{rotation:-20,duration:.4,{SHR}}},{tm + 1.0:.3f});tl.set("#{t}_sw",{{opacity:1}},{tm:.3f});tl.fromTo("#{t}_sw1",{{y:0,opacity:1}},{{y:30,opacity:0,duration:.8,immediateRender:false}},{tm + .2:.3f});')
    if A.get('strokem'): n = max(int(span / .9), 1); o.append(f'tl.fromTo("#{t}_ra",{{rotation:152,{SHR}}},{{rotation:140,duration:.45,yoyo:true,repeat:{2 * n - 1},ease:"sine.inOut",{SHR},immediateRender:false}},{a1 + .4:.3f});')
    if A.get('flinch'):
        tm = a1 + .8
        while tm < T - .6: o += squash(t, tm, .9, 1.06, .08, .3); tm += A['flinch']
    if A.get('sniffup') and span > 2.2: o.append(f'tl.to({ac},{{rotation:0,y:0,duration:.6,ease:"power2.inOut",{FEET},overwrite:"auto"}},{a1 + 1.6:.3f});tl.to("#{t}_ra",{{rotation:150,duration:.5,{SHR}}},{a1 + 1.6:.3f});tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:-8,duration:.6,{NECK}}},{a1 + 2.0:.3f});')
    if A.get('gustlift'):
        tm = a1 + 1.2
        while tm < T - 1.4:
            o.append(f'tl.to({TR},{{y:-34,duration:.5,ease:"power2.out"}},{tm:.3f});tl.to({TR},{{y:0,duration:.45,ease:"bounce.out"}},{tm + .5:.3f});')
            o.append(f'tl.fromTo("#{t}_um",{{rotation:-8,svgOrigin:"-48 -118"}},{{rotation:10,duration:.5,yoyo:true,repeat:3,ease:"sine.inOut",svgOrigin:"-48 -118",immediateRender:false}},{tm - .4:.3f});'); tm += 2.6
    if A.get('juggle'):
        o.append(f'tl.set("#{t}_sw",{{opacity:1}},{a1:.3f});')
        for i in range(3):
            tm = a1 + i * .3
            while tm < T - .9: o.append(f'tl.fromTo("#{t}_sw{i}",{{y:40,x:{(i - 1) * 10}}},{{y:-40,x:{(1 - i) * 10},duration:.45,yoyo:true,repeat:1,ease:"sine.out",immediateRender:false}},{tm:.3f});'); tm += .9
    if A.get('tuckhead'):
        tm = a1
        while tm < T - 2.6:
            o.append(f'tl.to("#{t}_hd,#{t}_of,#{t}_te",{{scaleY:.3,y:14,duration:.5,ease:"power2.in",{NECK}}},{tm:.3f});tl.to("#{t}_hd,#{t}_of,#{t}_te",{{scaleY:1,y:0,duration:.6,ease:"back.out(1.4)",{NECK}}},{tm + 1.6:.3f});'); tm += 4.0
    return o, info


def loco_js(t, d, act, a0, T, k, F):
    """hand-written locomotion acts (LOCO)"""
    o = []; info = dict(nohead=True, nolegs=True, noscale=True, noeyes=False, says={0: a0 + 1.0})
    ac = f'"#{t}_ac"'; TR = f'"#{t}_tr"'; RM = f'"#{t}_rm"'; s = d['s']; ty = act['type']; a1 = a0 + .35; span = T - a1
    L = float(act.get('dist', 320)) / s
    if span < 1.0: return o, info
    if ty == 'swimstroke':   # breaststroke: prone (head toward +x), arm sweeps and frog kicks in rhythm, the body surges with each kick
        per = 1.15; n = max(int((span - .5) / per), 1)
        o.append(f'tl.to({ac},{{rotation:90,duration:.5,ease:"power2.out",svgOrigin:"0 -40"}},{a1:.3f});' + F('happy', a0))
        o.append(f'tl.fromTo("#{t}_ra",{{rotation:-160,{SHR}}},{{rotation:-60,duration:{per / 2},yoyo:true,repeat:{2 * n - 1},ease:"power2.inOut",{SHR},immediateRender:false}},{a1 + .5:.3f});tl.fromTo("#{t}_la",{{rotation:-160,{SHL}}},{{rotation:-60,duration:{per / 2},yoyo:true,repeat:{2 * n - 1},ease:"power2.inOut",{SHL},immediateRender:false}},{a1 + .5:.3f});')
        tm = a1 + .5
        while tm < T - per:
            o += tuck(t, tm, per * .35, 0, per * .25, 55)   # pull up, snap out
            o.append(f'tl.to({TR},{{x:"+={L / max(n, 1):.1f}",duration:{per * .6:.3f},ease:"power2.out"}},{tm + per * .35:.3f});tl.to({TR},{{y:{-6 if int((tm - a1) / per) % 2 else 6},duration:{per:.3f},ease:"sine.inOut"}},{tm:.3f});'); tm += per
        info['says'][0] = a1 + .8
    elif ty == 'climb':   # up a rope / pole / tree (frog_place: beside it, dist = height to climb): hand over hand, legs alternate, then waves from the top
        H = float(act.get('dist', 240)) / s; st_ = 22; nst = max(int(H / st_), 2); per = .5; tt = a1
        o.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.3,{SHR}}},{a0:.3f});tl.to("#{t}_la",{{rotation:150,duration:.3,{SHL}}},{a0:.3f});tl.to({ac},{{rotation:8,duration:.3,{FEET}}},{a0:.3f});' + F('determined', a0))
        o += legs_cycle(t, a1, a1 + nst * per, per * 2, 26)
        for i in range(nst):
            if tt > T - 1.4: break
            arm, org = ('ra', SHR) if i % 2 == 0 else ('la', SHL); sg = -1 if arm == 'ra' else 1
            o.append(f'tl.to("#{t}_{arm}",{{rotation:{sg * 172},duration:{per * .5:.3f},ease:"power2.out",{org}}},{tt:.3f});tl.to("#{t}_{arm}",{{rotation:{sg * 120},duration:{per * .5:.3f},ease:"power1.in",{org}}},{tt + per * .5:.3f});')
            o.append(f'tl.to({TR},{{y:{-st_ * (i + 1):.1f},duration:{per:.3f},ease:"power1.inOut"}},{tt:.3f});'); tt += per
        if T - tt > 1.6:   # at the top: looks around, waves
            o.append(f'tl.to("#{t}_la",{{rotation:160,duration:.3,{SHL}}},{tt:.3f});tl.to("#{t}_ra",{{rotation:-150,duration:.35,{SHR}}},{tt + .4:.3f});tl.fromTo("#{t}_ra",{{rotation:-150,{SHR}}},{{rotation:-125,duration:.2,yoyo:true,repeat:3,ease:"sine.inOut",{SHR},immediateRender:false}},{tt + .75:.3f});' + F('proud', tt + .3))
            o.append(f'tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:-10,duration:.5,{NECK}}},{tt + .3:.3f});tl.to("#{t}_hd,#{t}_of,#{t}_te",{{rotation:8,duration:.8,{NECK}}},{tt + 1.3:.3f});')
            info['says'][0] = tt + .5
    elif ty == 'leap':   # three running steps, a crouch, a long jump stretched out, lands with a squash and two stumbling steps
        per = .4; run = 3 * per; tj = a1 + run + .18
        o.append(F('determined', a0) + f'tl.to({TR},{{x:{L * .3:.1f},duration:{run:.3f},ease:"none"}},{a1:.3f});')
        o += legs_cycle(t, a1, a1 + run, per, 30) + arms_swing(t, a1, a1 + run, per, 24)
        tm = a1
        while tm < a1 + run - .05: o.append(f'tl.to({TR},{{y:-12,duration:{per / 2:.2f},ease:"power2.out"}},{tm:.3f});tl.to({TR},{{y:0,duration:{per / 2:.2f},ease:"power2.in"}},{tm + per / 2:.3f});'); tm += per
        o += squash(t, a1 + run, .78, 1.15, .18, .08)
        o.append(f'tl.to({TR},{{x:{L * .3 + L * .55:.1f},duration:.8,ease:"power1.out"}},{tj:.3f});tl.to({TR},{{y:-110,duration:.42,ease:"power2.out"}},{tj:.3f});tl.to({TR},{{y:0,duration:.38,ease:"power2.in"}},{tj + .42:.3f});')
        o.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.3,{SHR}}},{tj:.3f});tl.to("#{t}_la",{{rotation:-30,duration:.3,{SHL}}},{tj:.3f});tl.to("#{t}_lgl",{{rotation:30,duration:.3,{HIPL}}},{tj:.3f});tl.to("#{t}_lgr",{{rotation:-45,duration:.3,{HIPR}}},{tj:.3f});tl.to({ac},{{rotation:22,duration:.35,{FEET}}},{tj:.3f});' + F('excited', tj))
        o.append(f'tl.to({ac},{{rotation:-6,duration:.3,{FEET}}},{tj + .5:.3f});tl.to("#{t}_lgl,#{t}_lgr",{{rotation:0,duration:.25}},{tj + .55:.3f});')
        o += squash(t, tj + .8, .78, 1.18, .1, .4)
        o.append(f'tl.to({TR},{{x:{L * .95:.1f},duration:.5,ease:"power2.out"}},{tj + .85:.3f});tl.to({ac},{{rotation:0,duration:.5,ease:"back.out(1.4)",{FEET}}},{tj + .9:.3f});tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.4}},{tj + 1.0:.3f});' + F('proud', tj + 1.3))
        info['says'][0] = tj + .1
    elif ty == 'dangle':   # hangs by ONE hand, swinging, legs flailing; the grip slips, it drops and lands on its bottom
        o.append(f'tl.set("#{t}_ra",{{rotation:-172,{SHR}}},0);tl.to("#{t}_la",{{rotation:60,duration:.3,{SHL}}},{a0:.3f});' + F('worried', a0))
        ts = min(a1 + 3.2, T - 1.6)
        n = max(int((ts - a1) / .8), 1)
        o.append(f'tl.fromTo({ac},{{rotation:-12,svgOrigin:"34 -22"}},{{rotation:12,duration:.8,yoyo:true,repeat:{n},ease:"sine.inOut",svgOrigin:"34 -22",immediateRender:false}},{a1:.3f});')
        o += kicks(t, a1, max(int((ts - a1) / .18), 4), .36, 26)
        o.append(f'tl.fromTo("#{t}_la",{{rotation:60,{SHL}}},{{rotation:120,duration:.3,yoyo:true,repeat:{max(int((ts - a1) / .3), 2)},ease:"sine.inOut",{SHL},immediateRender:false}},{a1:.3f});')
        o.append(F('shock', ts - .4) + f'tl.to("#{t}_ra",{{rotation:-150,duration:.15,{SHR}}},{ts:.3f});tl.to({TR},{{y:{float(act.get("drop", 90)) / s:.1f},duration:.42,ease:"power2.in"}},{ts:.3f});')
        o.append(f'tl.to({ac},{{rotation:-62,duration:.42,ease:"power1.in",{FEET}}},{ts:.3f});tl.to({ac},{{rotation:-58,duration:.3,ease:"bounce.out",{FEET}}},{ts + .42:.3f});tl.to("#{t}_ra,#{t}_la",{{rotation:0,duration:.3}},{ts + .42:.3f});tl.to("#{t}_lgl,#{t}_lgr",{{rotation:0,duration:.2}},{ts + .42:.3f});')
        o.append(stars_js(t, ts + .45, 1.5)); info['says'] = {0: a1 + .6, 1: ts + .5}
        if T - ts > 3.0: o.append(f'tl.to({ac},{{rotation:0,duration:.6,ease:"back.out(1.3)",{FEET}}},{ts + 2.2:.3f});' + F('pout', ts + 2.2))
    elif ty == 'skate':   # glides along on one foot, the other leg stretched back, arms out, an S-curve, a spin at the end
        o.append(F('happy', a0) + f'tl.to("#{t}_lgl",{{rotation:48,duration:.4,{HIPL}}},{a1:.3f});tl.to("#{t}_ra",{{rotation:-85,duration:.4,{SHR}}},{a1:.3f});tl.to("#{t}_la",{{rotation:95,duration:.4,{SHL}}},{a1:.3f});tl.to({ac},{{rotation:12,duration:.4,{FEET}}},{a1:.3f});')
        te = T - 1.2
        o.append(f'tl.to({TR},{{x:{L:.1f},duration:{max(te - a1, 1):.3f},ease:"power1.inOut"}},{a1:.3f});')
        n = max(int((te - a1) / 1.1), 1)
        o.append(f'tl.fromTo({TR},{{y:-8}},{{y:8,duration:1.1,yoyo:true,repeat:{n},ease:"sine.inOut",immediateRender:false}},{a1:.3f});tl.fromTo({ac},{{rotation:12,{FEET}}},{{rotation:4,duration:1.1,yoyo:true,repeat:{n},ease:"sine.inOut",{FEET},immediateRender:false}},{a1 + .4:.3f});')
        if T - te > 1.0: o.append(f'tl.to("#{t}_lgl",{{rotation:0,duration:.2,{HIPL}}},{te:.3f});tl.to("#{t}_ra",{{rotation:-150,duration:.3,{SHR}}},{te:.3f});tl.to("#{t}_la",{{rotation:150,duration:.3,{SHL}}},{te:.3f});tl.fromTo({RM},{{rotation:0}},{{rotation:{360 if d["flip"] > 0 else -360},duration:.9,ease:"power1.inOut",svgOrigin:"0 -34",immediateRender:false}},{te:.3f});' + F('excited', te))
    elif ty == 'somersault':   # a running start, a forward flip, lands with a flourish
        per = .4; tj = a1 + 2 * per
        o.append(F('excited', a0) + f'tl.to({TR},{{x:{L * .3:.1f},duration:{2 * per:.3f},ease:"none"}},{a1:.3f});'); o += legs_cycle(t, a1, tj, per, 28)
        o.append(f'tl.to({TR},{{x:{L * .8:.1f},duration:.9,ease:"power1.out"}},{tj:.3f});tl.to({TR},{{y:-90,duration:.45,ease:"power2.out"}},{tj:.3f});tl.to({TR},{{y:0,duration:.45,ease:"power2.in"}},{tj + .45:.3f});')
        o.append(f'tl.fromTo({RM},{{rotation:0}},{{rotation:{360 if d["flip"] > 0 else -360},duration:.9,ease:"power1.inOut",svgOrigin:"0 -34",immediateRender:false}},{tj:.3f});'); o += tuck(t, tj, .2, .45, .2, 60)
        o.append(f'tl.to("#{t}_ra",{{rotation:100,duration:.2,{SHR}}},{tj:.3f});tl.to("#{t}_la",{{rotation:-100,duration:.2,{SHL}}},{tj:.3f});')
        o += squash(t, tj + .9, .8, 1.15, .1, .4); o.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.35,ease:"back.out(2)",{SHR}}},{tj + 1.0:.3f});tl.to("#{t}_la",{{rotation:150,duration:.35,ease:"back.out(2)",{SHL}}},{tj + 1.0:.3f});' + F('proud', tj + 1.0))
        info['says'][0] = tj + 1.1
    elif ty == 'tiptoe':   # sneaks: slow high steps, body bent forward, finger at the mouth, head turning to check
        per = 1.0
        o.append(F('mischief', a0) + f'tl.to({ac},{{rotation:14,duration:.5,{FEET}}},{a1:.3f});tl.to("#{t}_ra",{{rotation:150,duration:.4,{SHR}}},{a1:.3f});tl.to("#{t}_la",{{rotation:-60,duration:.4,{SHL}}},{a1:.3f});')
        o.append(f'tl.to({TR},{{x:{L * .7:.1f},duration:{span - .3:.3f},ease:"none"}},{a1:.3f});'); o += legs_cycle(t, a1, T - .2, per, 34)
        tm = a1
        while tm < T - per: o.append(f'tl.to({TR},{{y:-6,duration:{per / 2:.2f},ease:"sine.inOut"}},{tm:.3f});tl.to({TR},{{y:0,duration:{per / 2:.2f},ease:"sine.inOut"}},{tm + per / 2:.3f});'); tm += per
        n = max(int(span / 2.0), 1); o.append(f'tl.fromTo("#{t}_hd,#{t}_of,#{t}_te",{{rotation:-10,{NECK}}},{{rotation:10,duration:1.0,yoyo:true,repeat:{2 * n - 1},ease:"sine.inOut",{NECK},immediateRender:false}},{a1 + .5:.3f});')
    elif ty == 'crawl':   # on its belly (tunnels, caves, under things): arms pull alternately, legs push, inching forward
        per = .8; n = max(int((span - .5) / per), 1)
        o.append(F('squint', a0) + f'tl.to({ac},{{rotation:86,duration:.5,ease:"power2.out",svgOrigin:"0 -40"}},{a1:.3f});')
        o.append(f'tl.fromTo("#{t}_ra",{{rotation:-150,{SHR}}},{{rotation:-80,duration:{per / 2},yoyo:true,repeat:{2 * n - 1},ease:"power1.inOut",{SHR},immediateRender:false}},{a1 + .5:.3f});tl.fromTo("#{t}_la",{{rotation:-80,{SHL}}},{{rotation:-150,duration:{per / 2},yoyo:true,repeat:{2 * n - 1},ease:"power1.inOut",{SHL},immediateRender:false}},{a1 + .5:.3f});')
        o += legs_cycle(t, a1 + .5, T - .2, per, 22)
        tm = a1 + .5
        while tm < T - per: o.append(f'tl.to({TR},{{x:"+={L * .6 / n:.1f}",duration:{per * .5:.3f},ease:"power2.out"}},{tm:.3f});'); tm += per
    elif ty == 'logroll':   # lies down and rolls sideways along the ground (swept, tumbling, "rolled downhill")
        o.append(F('shock', a0) + f'tl.to({ac},{{rotation:88,duration:.4,ease:"power2.in",svgOrigin:"0 -40"}},{a1:.3f});')
        dur = max(span - .9, 1.0); turns = max(1, round(L / 180))
        o.append(f'tl.to({TR},{{x:{L:.1f},duration:{dur:.3f},ease:"power1.inOut"}},{a1 + .4:.3f});tl.fromTo({RM},{{rotation:0}},{{rotation:{360 * turns * (1 if d["flip"] > 0 else -1)},duration:{dur:.3f},ease:"power1.inOut",svgOrigin:"0 -34",immediateRender:false}},{a1 + .4:.3f});')
        o.append(f'tl.to("#{t}_ra",{{rotation:-150,duration:.3,{SHR}}},{a1:.3f});tl.to("#{t}_la",{{rotation:150,duration:.3,{SHL}}},{a1:.3f});'); o.append(stars_js(t, a1 + .4 + dur, max(T - a1 - .4 - dur, .4)))
        if T - (a1 + .4 + dur) > .5: o.append(F('dizzy', a1 + .4 + dur))
    elif ty == 'tightrope':   # walks a line: arms out, slow careful steps, wobbles and recovers twice
        per = 1.1
        o.append(F('squint', a0) + f'tl.to("#{t}_ra",{{rotation:-90,duration:.4,{SHR}}},{a1:.3f});tl.to("#{t}_la",{{rotation:90,duration:.4,{SHL}}},{a1:.3f});')
        o.append(f'tl.to({TR},{{x:{L * .8:.1f},duration:{span - .3:.3f},ease:"none"}},{a1:.3f});'); o += legs_cycle(t, a1, T - .2, per, 24)
        tm = a1 + 1.6; j = 0
        while tm < T - 1.6:
            sg = 1 if j % 2 == 0 else -1
            o.append(F('shock', tm) + f'tl.to({ac},{{rotation:{14 * sg},duration:.35,ease:"power2.out",{FEET}}},{tm:.3f});tl.fromTo("#{t}_ra",{{rotation:-90,{SHR}}},{{rotation:-130,duration:.12,yoyo:true,repeat:5,{SHR},immediateRender:false}},{tm:.3f});tl.fromTo("#{t}_la",{{rotation:90,{SHL}}},{{rotation:130,duration:.12,yoyo:true,repeat:5,{SHL},immediateRender:false}},{tm:.3f});')
            o.append(f'tl.to({ac},{{rotation:0,duration:.6,ease:"elastic.out(1,.5)",{FEET}}},{tm + .5:.3f});' + F('squint', tm + 1.0)); tm += 3.2; j += 1
    return o, info


# ---------------------------------------------------------------- arm bend (2026-10-29, miya) ----------------------------------------------------------------
# The resting arm curves outward "( O )". Turned about the shoulder toward the head, that same curve ends up bulging toward the head
# ") O (" = a broken-looking elbow. So the bend follows the arm angle: every rotation tween on #<t>_la / #<t>_ra gets a companion tween of the
# path "d" (both strokes of the arm) that morphs the control point from bent-out (|angle| <= 55) to bent-in (|angle| >= 125), with the same
# duration / ease / yoyo / repeat, so a raised arm always curves away from the head like "\ o /". Pure post-processing of the generated lines.
ARM_OUT = (14.0, 6.0); ARM_IN = (1.4, 15.2)   # quadratic control point (right arm; the left one is mirrored in x), end point (16, 22) stays


def arm_d(side, rot):
    b = min(max((abs(rot) - 55) / 70, 0), 1); cx = ARM_OUT[0] + (ARM_IN[0] - ARM_OUT[0]) * b; cy = ARM_OUT[1] + (ARM_IN[1] - ARM_OUT[1]) * b
    return f'M34 -22 q{cx:.1f} {cy:.1f} 16 22' if side == 'ra' else f'M-34 -22 q{-cx:.1f} {cy:.1f} -16 22'


def _obj_end(s_, i):
    """index just past the balanced {...} that starts at s_[i] == '{'"""
    d = 0
    for j in range(i, len(s_)):
        if s_[j] == '{': d += 1
        elif s_[j] == '}':
            d -= 1
            if d == 0: return j + 1
    return -1


_ROT = __import__('re').compile(r'(?<![\w"])rotation:(-?\d+(?:\.\d+)?)(?![\d.])')
_KEEP = __import__('re').compile(r'(?:duration|ease|yoyo|repeat|repeatDelay):(?:"[^"]*"|[^,}]+)')


def arm_bend_pass(lines, t):
    """add the bend tweens for every arm rotation tween in lines (strings of ';'-separated tl.* calls)"""
    import re
    rx = re.compile(r'tl\.(to|set|fromTo)\(("[^"]*")\s*,')
    out = []
    for ln in lines:
        extra = []
        for m in rx.finditer(ln):
            sel = m.group(2).strip('"'); sides = [x.split('_')[-1] for x in sel.split(',') if x.strip().startswith('#' + t + '_') and x.strip().split('_')[-1] in ('la', 'ra')]
            if not sides: continue
            i = ln.find('{', m.end())
            if i < 0: continue
            j = _obj_end(ln, i); o1 = ln[i:j]; o2 = None
            if m.group(1) == 'fromTo':
                i2 = ln.find('{', j); j2 = _obj_end(ln, i2); o2 = ln[i2:j2]; j = j2
            mt = re.match(r'\s*,\s*(-?\d+(?:\.\d+)?)\s*\)', ln[j:])
            if not mt: continue
            tm = mt.group(1); tgt = o2 if o2 else o1
            r1 = _ROT.search(tgt)
            if not r1 or 'keyframes' in tgt: continue
            keep = ','.join(_KEEP.findall(tgt))
            for side in sides:
                dsel = f'"#{t}_{side}>path"'; d1 = arm_d(side, float(r1.group(1)))
                if m.group(1) == 'set': extra.append(f'tl.set({dsel},{{attr:{{d:"{d1}"}}}},{tm});')
                elif m.group(1) == 'fromTo':
                    r0 = _ROT.search(o1); d0 = arm_d(side, float(r0.group(1))) if r0 else d1
                    if d0 == d1 and 'yoyo' not in keep: continue
                    extra.append(f'tl.fromTo({dsel},{{attr:{{d:"{d0}"}}}},{{attr:{{d:"{d1}"}},{keep + "," if keep else ""}immediateRender:false}},{tm});')
                else: extra.append(f'tl.to({dsel},{{attr:{{d:"{d1}"}},{keep + "," if keep else ""}immediateRender:false}},{tm});')
        out.append(ln + ''.join(extra))
    return out


HITS = {}   # tag -> the act's key moment (filled by frog.js for tests)


def shadow_follow_pass(lines, t):
    """2026-10-29 b (miya: the shadow stayed where the frog started): every x move of #<t>_tr (the roam / contact travel layer) is mirrored
    on the ground shadow #<t>_sh (x only, same duration / ease / yoyo / repeat), so the shadow travels with the frog but stays on the ground
    while it jumps (y is not copied)."""
    import re
    rx = re.compile(r'tl\.(to|set|fromTo)\("#' + re.escape(t) + r'_tr"\s*,')
    xr = re.compile(r'(?<![\w"])x:("[^"]*"|-?\d+(?:\.\d+)?)(?![\d.])')
    out = []
    for ln in lines:
        extra = []
        for m in rx.finditer(ln):
            i = ln.find('{', m.end()); j = _obj_end(ln, i); o1 = ln[i:j]; o2 = None
            if m.group(1) == 'fromTo':
                i2 = ln.find('{', j); j2 = _obj_end(ln, i2); o2 = ln[i2:j2]; j = j2
            mt = re.match(r'\s*,\s*(-?\d+(?:\.\d+)?)\s*\)', ln[j:])
            if not mt: continue
            tm = mt.group(1); tgt = o2 if o2 else o1; x1 = xr.search(tgt)
            if not x1 or 'keyframes' in tgt: continue
            keep = ','.join(_KEEP.findall(tgt)); sh = f'"#{t}_sh"'
            if m.group(1) == 'set': extra.append(f'tl.set({sh},{{x:{x1.group(1)}}},{tm});')
            elif m.group(1) == 'fromTo':
                x0 = xr.search(o1); extra.append(f'tl.fromTo({sh},{{x:{x0.group(1) if x0 else 0}}},{{x:{x1.group(1)},{keep + "," if keep else ""}immediateRender:false}},{tm});')
            else: extra.append(f'tl.to({sh},{{x:{x1.group(1)},{keep + "," if keep else ""}immediateRender:false}},{tm});')
        out.append(ln + ''.join(extra))
    return out
