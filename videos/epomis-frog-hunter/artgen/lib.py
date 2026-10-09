# -*- coding: utf-8 -*-
# Small SVG drawing helpers for the Epomis video (flat 2D, black outlines, no filters/gradients/text).
import math
INK = "#0A0A0A"
NIGHT = "#1F2A44"; NIGHT2 = "#2B3442"; DAY = "#A9CFE6"; PAPER = "#D9C29A"; PAPER2 = "#C9A56E"
TEAL = "#3E7F8C"; OLIVE = "#8FA35A"; BRICK = "#B5483B"; LAMP = "#F2D27A"; WHITE = "#F1ECE0"
FROG = "#8FA35A"; FROG_D = "#6E8A45"; FROG_L = "#B3C27A"; BELLY = "#E3DCB5"; EYE = "#F2D27A"; PINK = "#D98B7A"
TOAD = "#9A7B55"; TOAD_D = "#7A5E3F"; TOAD_L = "#B79B73"
LARVA = "#EADFB3"; LARVA_D = "#C9B77A"; ORANGE = "#D9893B"; HEAD = "#5B4630"
BEETLE = "#2F7F8A"; BEETLE_D = "#215E68"; BEETLE_L = "#5FA6A6"; RIM = "#E0A840"; LEGC = "#D9B24A"
GREEN1 = "#5E7A45"; GREEN2 = "#7F9B55"; GREEN3 = "#3F5A38"; WOOD = "#8A6A45"; WOOD2 = "#6B4F33"


def S(sw=6):
    return f'stroke="{INK}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"'


def path(d, fill, sw=6, extra=''):
    st = S(sw) if sw else ''
    return f'<path d="{d}" fill="{fill}" {st} {extra}/>'


def ell(cx, cy, rx, ry, fill, sw=6, rot=0, extra=''):
    tf = f' transform="rotate({rot} {cx} {cy})"' if rot else ''
    st = S(sw) if sw else ''
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" {st}{tf} {extra}/>'


def circ(cx, cy, r, fill, sw=6, extra=''):
    st = S(sw) if sw else ''
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" {st} {extra}/>'


def rect(x, y, w, h, fill, rx=0, sw=6, extra=''):
    st = S(sw) if sw else ''
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" {st} {extra}/>'


def poly(pts, fill, sw=6, extra=''):
    p = ' '.join(f'{x},{y}' for x, y in pts)
    st = S(sw) if sw else ''
    return f'<polygon points="{p}" fill="{fill}" {st} {extra}/>'


def line(x1, y1, x2, y2, col=INK, w=6):
    return f'<path d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


def stroke(d, col=INK, w=6, extra=''):
    return f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def limb(d, w, col):
    """thick coloured limb with black outline: black path underneath, colour path on top"""
    return (f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="{w + 12}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')


def g(content, tf='', mv=None):
    a = f' transform="{tf}"' if tf else ''
    i = f' id="mv-{mv}"' if mv else ''
    return f'<g{i}{a}>{content}</g>'


def at(x, y, s=1.0, flip=False, rot=0):
    sx = -s if flip else s
    r = f' rotate({rot})' if rot else ''
    return f'translate({x} {y}){r} scale({sx} {s})'


def svg(body):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" height="1080">' + body + '</svg>')


# ---------------- creatures (local origin: ground contact at y=0, facing right) ----------------
def frog(open_=False, col=FROG, dark=FROG_D, light=FROG_L, eyes=True, dead=False):
    o = []
    # hind leg (behind body)
    o.append(limb("M-70 -100 L-120 -38 L40 -10", 46, dark))
    o.append(limb("M40 -10 L96 -6", 22, dark))
    o.append(path("M96 -6 l24 -2 M96 -6 l22 12 M96 -6 l18 -16", "none", 5))
    o.append(ell(0, -105, 150, 95, col))
    o.append(ell(30, -66, 104, 46, BELLY, 0))
    o.append(path("M-100 -150 Q-20 -210 80 -176 Q-10 -190 -100 -150Z", light, 0))
    for (x, y, r) in [(-70, -150, 14), (-10, -176, 12), (-90, -108, 11), (30, -168, 10)]:
        o.append(ell(x, y, r * 1.3, r, dark, 0))
    # head
    o.append(ell(118, -148, 92, 62, col))
    if open_:
        o.append(ell(150, -122, 66, 30, PINK, 5))
        o.append(g(ell(140, -108, 78, 20, col) + ell(130, -118, 50, 8, PINK, 0), f"rotate(26 70 -118)"))
    else:
        o.append(stroke("M62 -128 Q150 -104 214 -136", INK, 5))
    # eye
    o.append(circ(148, -204, 28, EYE if eyes else col))
    if eyes:
        o.append(ell(154, -203, 8, 15, INK, 0))
        o.append(path("M122 -208 Q148 -236 176 -210", "none", 4))
    o.append(circ(206, -166, 4, INK, 0))
    # front leg
    o.append(limb("M70 -78 L98 -12", 30, dark))
    o.append(path("M98 -12 l26 0 M98 -12 l24 -12 M98 -12 l20 10", "none", 5))
    return ''.join(o)


def toad():
    o = []
    o.append(limb("M-60 -90 L-100 -30 L20 -8", 50, TOAD_D))
    o.append(limb("M20 -8 L70 -6", 24, TOAD_D))
    o.append(ell(0, -100, 150, 98, TOAD))
    o.append(ell(30, -62, 104, 40, "#D8C9A0", 0))
    for (x, y) in [(-90, -140), (-40, -170), (10, -150), (-110, -100), (-60, -118), (40, -176), (0, -120), (-20, -80)]:
        o.append(circ(x, y, 9, TOAD_D, 0))
    o.append(ell(112, -140, 88, 58, TOAD))
    o.append(stroke("M60 -118 Q150 -98 208 -128", INK, 5))
    o.append(circ(142, -192, 26, "#D9A94A"))
    o.append(ell(148, -191, 8, 13, INK, 0))
    o.append(ell(100, -176, 34, 18, TOAD_L, 4, rot=-20))          # parotoid gland
    o.append(circ(200, -156, 4, INK, 0))
    o.append(limb("M66 -70 L92 -10", 30, TOAD_D))
    o.append(path("M92 -10 l24 0 M92 -10 l22 -10", "none", 5))
    return ''.join(o)


def larva(wave=0.0, antenna=True, jaws=1.0):
    """horizontal larva, head at x~0 facing right, body extends to the left, length ~ 420"""
    o = []
    n = 10
    segs = []
    for k in range(n):
        x = -34 - k * 34
        y = math.sin(k * 0.55 + wave) * 6 - 22
        rx = 27 - k * 1.3; ry = 25 - k * 1.4
        segs.append((x, y, rx, ry))
    # tail prongs
    x, y, rx, ry = segs[-1]
    o.append(limb(f"M{x - rx + 6} {y - 4} L{x - rx - 44} {y - 26}", 9, HEAD))
    o.append(limb(f"M{x - rx + 6} {y + 4} L{x - rx - 46} {y + 12}", 9, HEAD))
    # legs
    for k in (0, 1, 2):
        x, y, rx, ry = segs[k]
        o.append(limb(f"M{x} {y + ry - 6} L{x + 6} {y + ry + 20}", 8, HEAD))
    for k in range(n - 1, -1, -1):
        x, y, rx, ry = segs[k]
        o.append(ell(round(x, 1), round(y, 1), round(rx, 1), round(ry, 1), LARVA if k % 2 == 0 else LARVA_D))
        if k % 2 == 1:
            o.append(ell(round(x, 1), round(y - ry + 8, 1), round(rx * 0.55, 1), 7, ORANGE, 0))
        o.append(ell(round(x - rx * 0.5, 1), round(y, 1), 4, round(ry * 0.8, 1), INK, 0))
    # head
    o.append(ell(8, -26, 40, 32, HEAD))
    o.append(circ(22, -38, 6, WHITE, 3)); o.append(circ(24, -38, 2.5, INK, 0))
    # double-hooked jaws
    j = jaws
    o.append(limb(f"M42 -24 Q{42 + 46 * j} {-24 + 6} {42 + 40 * j} {-24 + 44}", 11, "#3A2A20"))
    o.append(limb(f"M{42 + 40 * j} {-24 + 44} l-14 -8", 7, "#3A2A20"))
    o.append(limb(f"M40 -8 Q{40 + 40 * j} {-8 + 18} {40 + 30 * j} {-8 + 52}", 11, "#3A2A20"))
    o.append(limb(f"M{40 + 30 * j} {-8 + 52} l-14 -6", 7, "#3A2A20"))
    if antenna:
        a1 = limb("M2 -54 Q20 -92 52 -108", 6, HEAD) + circ(54, -110, 7, ORANGE, 4)
        a2 = limb("M-10 -56 Q0 -96 22 -118", 6, HEAD) + circ(24, -120, 7, ORANGE, 4)
        o.append(g(a1 + a2, mv="antenna"))
    return ''.join(o)


def beetle(antenna=True):
    """adult ground beetle, facing right, ground at y=0, length ~ 330"""
    o = []
    leg = [(-70, -22, -110, 4), (0, -18, -20, 6), (62, -20, 98, 4)]
    for (x, y, tx, ty) in leg:
        o.append(limb(f"M{x} {y} L{(x + tx) / 2 - 10} {y + 22} L{tx} {ty}", 12, LEGC))
    o.append(ell(-20, -48, 138, 50, BEETLE))
    o.append(ell(-30, -62, 100, 22, BEETLE_L, 0))
    o.append(f'<ellipse cx="-20" cy="-48" rx="126" ry="40" fill="none" stroke="{RIM}" stroke-width="7"/>')
    o.append(ell(-20, -48, 138, 50, "none", 6))
    o.append(stroke("M-150 -50 L110 -50", INK, 4))
    o.append(ell(124, -50, 42, 36, BEETLE_D))
    o.append(path("M124 -80 Q150 -50 124 -20", "none", 4))
    o.append(ell(176, -48, 28, 24, "#173F46"))
    o.append(circ(188, -56, 6, WHITE, 3)); o.append(circ(190, -56, 2.4, INK, 0))
    o.append(limb("M196 -38 l24 10 M196 -34 l20 18", 7, "#173F46"))
    if antenna:
        o.append(g(limb("M180 -66 Q210 -110 262 -118", 6, LEGC) + limb("M170 -70 Q184 -116 226 -134", 6, LEGC), mv="antenna"))
    for (x, y, tx, ty) in [(-50, -22, -80, 14), (24, -18, 40, 14), (86, -20, 130, 12)]:
        o.append(limb(f"M{x} {y} L{(x + tx) / 2 + 6} {y + 20} L{tx} {ty}", 12, LEGC))
    return ''.join(o)


def tongue(x0, y0, x1, y1):
    mx = (x0 + x1) / 2; my = (y0 + y1) / 2 - 18
    return limb(f"M{x0} {y0} Q{mx} {my} {x1} {y1}", 18, PINK) + circ(x1, y1, 17, "#C9737A")


# ---------------- backgrounds ----------------
def stars(n=34, seed=3, y1=420):
    import random
    r = random.Random(seed); o = []
    for _ in range(n):
        x = r.randint(60, 1860); y = r.randint(40, y1)
        o.append(f'<circle cx="{x}" cy="{y}" r="{r.choice([2.5, 3, 3.5, 4])}" fill="{WHITE}"/>')
    return g(''.join(o))


def moon(x=1480, y=210, r=74):
    return circ(x, y, r, WHITE) + circ(x - 22, y - 12, 16, "#D8D2C0", 0) + circ(x + 24, y + 22, 11, "#D8D2C0", 0) + circ(x + 18, y - 28, 8, "#D8D2C0", 0)


def reeds(x, base, n=7, h=420, spread=26, seed=1, col=GREEN1, tuft=True):
    import random
    r = random.Random(seed); o = []
    for k in range(n):
        xx = x + (k - n / 2) * spread + r.randint(-8, 8)
        hh = h * r.uniform(0.7, 1.15); bend = r.randint(-60, 60)
        o.append(limb(f"M{xx} {base} Q{xx + bend * 0.2} {base - hh * 0.5} {xx + bend} {base - hh}", 9, col if k % 2 else GREEN2))
        if tuft and k % 3 == 0:
            o.append(ell(xx + bend, base - hh - 22, 12, 36, WOOD2, 5, rot=bend / 4))
    return ''.join(o)


def lilypad(x, y, rx=64, ry=20, col=GREEN2):
    return ell(x, y, rx, ry, col) + path(f"M{x} {y} L{x + rx * 0.9} {y - ry * 0.3}", "none", 4)


def ripples(x, y, n=3, rx=70, ry=14, col="#7FB0B6"):
    return ''.join(stroke(f"M{x - rx - k * 30} {y + k * 16} Q{x} {y - ry + k * 16} {x + rx + k * 30} {y + k * 16}", col, 5) for k in range(n))


def leaf(x, y, w=110, h=48, rot=0, col="#7A5A32", vein=True):
    s = ell(x, y, w, h, col, 5, rot=rot)
    if vein:
        a = math.radians(rot); dx = math.cos(a) * w * 0.8; dy = math.sin(a) * w * 0.8
        s += line(x - dx, y - dy, x + dx, y + dy, INK, 3)
    return s


def litter(seed=2, y0=700, y1=1060, n=22):
    import random
    r = random.Random(seed); o = [rect(-10, y0, 1940, 1090 - y0, "#4A3A28", 0, 6)]
    cols = ["#7A5A32", "#8A6A3A", "#5E4A2E", "#9A7A44", "#6B4F33"]
    for _ in range(n):
        o.append(leaf(r.randint(40, 1880), r.randint(y0 + 30, y1), r.randint(70, 130), r.randint(28, 48), r.randint(-40, 40), r.choice(cols)))
    return ''.join(o)


def grass(x, y, n=5, h=110, col=GREEN2):
    return ''.join(limb(f"M{x + k * 14} {y} Q{x + k * 14 + (k - n / 2) * 10} {y - h * 0.6} {x + k * 14 + (k - n / 2) * 22} {y - h + (k % 2) * 26}", 8, col if k % 2 else GREEN1) for k in range(n))


def fern(x, y, s=1.0, col=GREEN1):
    parts = [limb("M0 0 Q10 -80 60 -150", 8, col)]
    for k in range(1, 6):
        px = 8 + k * 9; py = -k * 26
        parts.append(limb(f"M{px} {py} L{px + 46} {py - 20}", 6, col))
        parts.append(limb(f"M{px} {py} L{px - 40} {py - 22}", 6, GREEN2))
    return g(''.join(parts), at(x, y, s))


def person(x, y, s=1.0, flip=False, skin="#C99A74", shirt="#B5483B", pants="#2B3442", hair="#2A2018", back=False, pose='stand'):
    o = []
    o.append(limb("M-26 -150 L-30 -10", 34, pants)); o.append(limb("M26 -150 L30 -10", 34, pants))
    o.append(rect(-50, -14, 40, 18, "#2A2018", 6, 5)); o.append(rect(10, -14, 40, 18, "#2A2018", 6, 5))
    o.append(path("M-62 -150 L-52 -330 Q0 -352 52 -330 L62 -150Z", shirt))
    o.append(limb("M-58 -320 L-84 -200", 28, shirt)); o.append(limb("M58 -320 L84 -214", 28, shirt))
    o.append(circ(-86, -190, 15, skin, 5)); o.append(circ(86, -204, 15, skin, 5))
    o.append(rect(-14, -366, 28, 40, skin, 6, 5))
    o.append(ell(0, -404, 44, 50, skin))
    o.append(path("M-46 -410 Q-44 -466 4 -462 Q50 -460 46 -408 Q20 -440 -46 -410Z", hair))
    if not back:
        o.append(circ(-16, -404, 3.5, INK, 0)); o.append(circ(16, -404, 3.5, INK, 0)); o.append(stroke("M-10 -386 Q0 -380 10 -386", INK, 4))
    else:
        o.append(ell(0, -412, 44, 44, hair, 0))
    return g(''.join(o), at(x, y, s, flip))
