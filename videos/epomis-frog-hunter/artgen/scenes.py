# -*- coding: utf-8 -*-
import os, sys, math
from lib import *

OUT = os.path.join(os.path.dirname(__file__), '..', 'art')
BG = lambda c: rect(-10, -10, 1940, 1100, c, 0, 0)

def check(x, y, s=1.0):
    return g(limb("M-34 0 L-10 28 L38 -34", 14, "#5E8A45"), at(x, y, s))
def cross(x, y, s=1.0):
    return g(limb("M-30 -30 L30 30 M30 -30 L-30 30", 14, BRICK), at(x, y, s))
def arrow(x1, y1, x2, y2, col=BRICK, w=14):
    a = math.atan2(y2 - y1, x2 - x1); h = 40
    p1 = (x2 - h * math.cos(a - .5), y2 - h * math.sin(a - .5)); p2 = (x2 - h * math.cos(a + .5), y2 - h * math.sin(a + .5))
    return limb(f"M{x1} {y1} L{x2 - 20 * math.cos(a)} {y2 - 20 * math.sin(a)}", w, col) + poly([(x2, y2), p1, p2], col, 5)
def panel(x, y, w, h, fill=PAPER, rx=18):
    return rect(x, y, w, h, fill, rx, 6)
def moon_night(): return BG(NIGHT) + stars() + moon()
def water(y=640, col=TEAL):
    return rect(-10, y, 1940, 1090 - y, col, 0, 6) + ''.join(stroke(f"M{x} {y + 60 + (x % 3) * 40} q40 -14 80 0", "#7FB0B6", 5) for x in range(60, 1900, 230))
def ground(y, col="#6B5A3A"): return rect(-10, y, 1940, 1090 - y, col, 0, 6)
def firefly(x, y): return g(circ(x, y, 9, LAMP, 4), mv="spark")
def mud(y=760): return ground(y, "#5A4630")
def eye_icon(x, y, s=1.0):
    return g(path("M-110 0 Q0 -90 110 0 Q0 90 -110 0Z", WHITE) + circ(0, 0, 44, EYE) + ell(0, 0, 14, 34, INK, 0), at(x, y, s))
def clock(x, y, r=90, hand=40):
    a = math.radians(hand)
    return circ(x, y, r, WHITE) + line(x, y, x, y - r * .6, INK, 8) + line(x, y, x + r * .5 * math.sin(a), y - r * .5 * math.cos(a), INK, 8) + circ(x, y, 8, INK, 0)
def lab_desk():
    return rect(0, 760, 1920, 330, WOOD, 0, 6) + rect(0, 750, 1920, 28, WOOD2, 0, 6)
def tank(x, y, w, h):
    return rect(x, y, w, h, "#CFE4E6", 10, 6) + rect(x + 10, y + h * 0.55, w - 20, h * 0.4 - 8, "#7A5A32", 6, 5) + stroke(f"M{x+30} {y+30} L{x+90} {y+30}", WHITE, 8)
def ruler(x, y, w):
    o = [rect(x, y, w, 56, LAMP, 6, 6)]
    for k in range(0, int(w), 40): o.append(line(x + k + 20, y, x + k + 20, y + (28 if k % 80 == 0 else 18), INK, 4))
    return ''.join(o)

S_ = {}
def sc(name):
    def d(f): S_[name] = f; return f
    return d

@sc('pond')
def _():
    b = moon_night() + water(620) + ripples(900, 760, 3, 90) + reeds(250, 700, 8, 420, 28, 1) + reeds(1600, 700, 8, 380, 28, 4)
    b += lilypad(620, 700) + lilypad(1100, 790, 80, 24) + g(frog(), at(1150, 780, 1.1, True))
    b += firefly(500, 420) + firefly(980, 330) + firefly(1360, 500) + firefly(760, 520)
    return b

@sc('larva')
def _():
    b = BG("#3B2F22") + ground(760, "#5A4630") + litter(5, 770, 860, 8)
    b += reeds(1500, 770, 4, 260, 30, 6, tuft=False) + g(larva(), at(1000, 800, 1.7)) + grass(260, 770, 6, 150)
    return b

@sc('litter')
def _():
    b = BG("#2E3A2C") + litter(7, 520, 880, 30) + fern(260, 640, 1.8) + fern(1650, 660, 1.6)
    b += g(larva(), at(760, 800, 1.2)) + g(frog(), at(1450, 800, 0.9, True))
    b += g(person(1700, 620, .5), '') if False else ''
    return b

@sc('groundbeetles')
def _():
    b = BG(PAPER)
    for i, x in enumerate((130, 700, 1270)):
        b += panel(x, 160, 520, 640, "#E9DCBC")
    b += g(beetle(), at(260, 440, .9)) + g(ell(0, 0, 40, 28, GREEN2) , at(560, 360)) + arrow(520, 520, 330, 520, BRICK)
    b += g(beetle(), at(830, 440, .9)) + g(ell(0, 0, 40, 28, GREEN2), at(1130, 360)) + arrow(780, 520, 1010, 520, "#5E8A45")
    b += g(beetle(), at(1400, 440, .9)) + g(frog(), at(1720, 760, .55, True)) + arrow(1700, 560, 1480, 560, BRICK) + cross(1560, 330, 1.4)
    b += g(larva(), at(400, 740, .6)) + g(larva(), at(970, 740, .6)) + g(larva(), at(1540, 740, .6))
    return b

@sc('lab')
def _():
    b = BG("#D5CDB8") + lab_desk() + tank(300, 400, 700, 340) + g(frog(), at(480, 700, .6)) + g(larva(), at(860, 705, .55))
    b += rect(1180, 560, 90, 200, "#4A4A4A", 6, 6) + rect(1130, 470, 190, 100, "#2B3442", 12, 6) + circ(1225, 520, 30, "#7FB0B6", 6)
    b += g(person(1560, 760, .75, True), '') + stroke("M1130 520 L1000 520", INK, 4)
    return b

@sc('hunter')
def _():
    b = BG(PAPER) + panel(150, 140, 1620, 700, "#E9DCBC")
    b += g(larva(), at(1150, 620, 1.9)) + ruler(300, 740, 480)
    for (x, y) in ((1180, 250), (1480, 360), (720, 300)): b += circ(x, y, 24, BRICK, 5) + circ(x, y, 8, WHITE, 0)
    b += line(1180, 274, 1100, 440, BRICK, 5) + line(1480, 384, 1330, 560, BRICK, 5) + line(720, 324, 800, 450, BRICK, 5)
    return b

@sc('frogeye')
def _():
    b = BG(DAY) + ground(780, GREEN1) + g(frog(), at(520, 790, 1.7)) + grass(1300, 790, 6, 140)
    b += panel(980, 190, 760, 430, "#F4ECD6")
    b += g(ell(0, 0, 22, 16, ORANGE), at(1090, 280)) + check(1250, 285) + g(ell(0, 0, 70, 50, ORANGE), at(1090, 420)) + cross(1250, 420) + g(ell(0, 0, 22, 16, ORANGE), at(1090, 540)) + check(1250, 540)
    b += arrow(1420, 290, 1620, 290, INK, 10) + arrow(1420, 540, 1620, 540, INK, 10) + stroke("M1420 420 L1620 420", INK, 8)
    return b

@sc('lure')
def _():
    b = BG("#3B2F22") + mud(740) + litter(9, 760, 870, 10) + g(frog(), at(1250, 780, 1.4, True))
    b += g(larva(wave=1.2), at(800, 780, 1.4)) + firefly(800, 380) + arrow(740, 420, 620, 340, LAMP, 8)
    return b

@sc('frogview')
def _():
    b = BG("#232C3A") + circ(960, 470, 330, "#2F3B4E") + circ(960, 470, 230, "#3A495F")
    b += eye_icon(960, 470, 2.4) if False else ''
    b += stroke("M960 100 L960 840 M520 470 L1400 470", LAMP, 6) + f'<circle cx="960" cy="470" r="150" fill="none" stroke="{LAMP}" stroke-width="6"/>'
    b += g(ell(0, 0, 26, 18, ORANGE), at(1130, 380), ) + g(ell(0, 0, 90, 60, ORANGE), at(740, 600)) + g(ell(0, 0, 26, 18, ORANGE), at(1180, 640))
    b += arrow(1130, 370, 1270, 330, WHITE, 8)
    return b

@sc('strike')
def _():
    b = BG("#3B2F22") + mud(740) + litter(10, 760, 870, 10) + g(frog(open_=True), at(1250, 790, 1.5, True))
    b += tongue(1090, 640, 400, 770) + g(larva(wave=2), at(780, 780, 1.5)) + arrow(780, 560, 640, 600, LAMP, 8)
    b += ripples(430, 820, 2, 60, 10, "#8A6A45")
    return b

@sc('grab')
def _():
    b = BG("#3B2F22") + mud(760) + g(frog(open_=True), at(1000, 800, 2.0, True)) + g(larva(jaws=1.0), at(1010, 600, 1.1, False, 8))
    b += circ(700, 450, 16, BRICK, 4) + arrow(520, 420, 680, 450, BRICK, 8)
    return b

@sc('feed')
def _():
    b = BG("#3B2F22") + mud(780) + g(frog(), at(1000, 800, 2.0, True)) + g(larva(), at(1000, 650, .8, False, 20))
    b += g(circ(0, 0, 12, LAMP, 4), at(560, 420)) + g(circ(0, 0, 12, LAMP, 4), at(1500, 400))
    return b

@sc('tricksters')
def _():
    b = BG(NIGHT) + stars(20, 5, 300) + rect(-10, 600, 1940, 500, TEAL, 0, 6)
    ang = g(ell(0, 0, 130, 100, "#4B4B4F") + path("M80 -30 L150 40 L80 20Z", WHITE, 5) + stroke("M60 -90 Q110 -190 170 -190", INK, 6) + circ(170, -190, 14, LAMP, 4) + circ(70, -30, 14, WHITE, 4), at(330, 780, 1.1))
    tur = g(ell(0, 0, 160, 90, "#5E6B4A") + ell(-10, -20, 110, 40, "#78885A", 0) + ell(170, 14, 62, 40, "#6E7A52") + path("M200 10 L240 36 L200 36Z", PINK, 4), at(880, 770, 1.1))
    b += ang + tur + g(larva(), at(1650, 790, .8)) + g(ell(0,0,16,16,LAMP), at(340, 630))
    return b

@sc('labnote')
def _():
    b = BG("#D5CDB8") + lab_desk() + rect(460, 250, 1000, 600, "#F4ECD6", 10, 6)
    for k in range(7): b += line(540, 330 + k * 70, 1380 - (k % 3) * 120, 330 + k * 70, "#8A8A8A", 8)
    b += g(person(1600, 780, .8, True), '') + g(larva(), at(1000, 830, .6)) + rect(260, 520, 130, 230, "#CFE4E6", 10, 6)
    return b

@sc('stages')
def _():
    b = BG(PAPER) + panel(110, 200, 1700, 600, "#E9DCBC")
    b += g(larva(), at(470, 440, .55)) + g(larva(), at(520, 580, .7)) + g(larva(), at(590, 740, .85))
    b += g(ell(0, 0, 70, 38, "#C9A56E"), at(960, 600)) + g(ell(0, 0, 18, 18, ORANGE), at(960, 600))
    b += arrow(740, 610, 840, 610, INK, 8) + arrow(1070, 610, 1170, 610, INK, 8) + g(beetle(), at(1500, 700, .8))
    return b

@sc('adult')
def _():
    b = BG("#2E3A2C") + litter(11, 600, 880, 24) + fern(300, 700, 1.8) + g(beetle(), at(1000, 760, 2.4)) + grass(1650, 760, 6, 160)
    return b

@sc('shelter')
def _():
    b = rect(0, 0, 960, 1080, DAY, 0, 0) + rect(960, 0, 960, 1080, NIGHT, 0, 0) + stars(16, 8, 400).replace('<g>', '<g transform="translate(0 0)">')
    b += circ(480, 220, 78, LAMP) + line(960, 0, 960, 1080, INK, 8)
    b += ground(760, "#5A4630") + leaf(440, 680, 180, 60, -6, "#7A5A32") + g(larva(), at(560, 810, 1.0)) + moon(1440, 220, 70)
    b += g(beetle(), at(1500, 810, 1.3)) + reeds(1760, 780, 3, 260, 24, 3)
    return b

@sc('bite')
def _():
    b = BG(NIGHT2) + ground(770, GREEN1) + g(frog(), at(1100, 790, 1.9, True)) + g(beetle(), at(560, 790, 1.1)) + arrow(790, 640, 900, 640, BRICK, 10)
    return b

@sc('still')
def _():
    b = BG(PAPER) + panel(130, 180, 740, 640, "#E9DCBC") + panel(1050, 180, 740, 640, "#E9DCBC")
    b += clock(500, 440, 150, 0) + g(larva(), at(650, 740, .6)) + clock(1420, 440, 150, 160) + g(frog(), at(1550, 760, .6, True))
    b += g(circ(0, 0, 10, LAMP), at(960, 480)) + arrow(880, 490, 1040, 490, INK, 8)
    return b

@sc('wetland')
def _():
    b = BG(DAY) + rect(-10, 560, 1940, 600, TEAL, 0, 6) + reeds(300, 640, 7, 380, 28, 2) + reeds(1500, 640, 7, 340, 28, 5)
    for x in (450, 800, 1150):
        b += g(circ(0, 0, 90, WHITE) + circ(0, 0, 60, "#F4ECD6", 4), at(x, 780))
    b += g(frog(), at(450, 790, .35)) + g(beetle(), at(800, 790, .3)) + g(larva(), at(1220, 800, .35)) + lilypad(1600, 760, 90, 24)
    return b

@sc('amphibians')
def _():
    b = BG(GREEN1) + ground(760, "#4A3A28")
    b += g(frog(), at(300, 770, .8)) + g(toad(), at(760, 770, .8)) + g(frog(col=BRICK, dark="#8E3A30", light="#D07A6A"), at(1180, 770, .75, True)) + g(toad(), at(1520, 770, .7, True))
    b += g(frog(col="#5E8A8C", dark="#3E6A6C", light="#8FB3B0"), at(960, 520, .5)) 
    return b

@sc('evolve')
def _():
    b = BG(PAPER) + panel(110, 180, 1700, 640, "#E9DCBC")
    b += g(beetle(), at(380, 560, .8)) + g(beetle(antenna=False), at(950, 560, .8)) + g(beetle(), at(1470, 560, .8))
    b += arrow(640, 470, 700, 470, INK, 10) + arrow(1210, 470, 1270, 470, INK, 10)
    b += g(larva(), at(380, 780, .55)) + g(larva(), at(950, 780, .6)) + g(frog(), at(1550, 780, .5, True))
    return b

@sc('reflex')
def _():
    b = BG(NIGHT2) + ground(780, "#4A3A28") + g(frog(), at(450, 790, 1.5)) + g(larva(), at(1250, 800, 1.2, True)) + arrow(940, 500, 1100, 500, LAMP, 12)
    b += stroke("M900 420 L1000 330 L980 460 L1090 380", LAMP, 8)
    return b

@sc('ladder')
def _():
    b = BG(PAPER)
    for k, (x, y, w) in enumerate(((180, 640, 420), (620, 480, 420), (1060, 320, 420), (1440, 180, 340))):
        b += rect(x, y, w, 120, "#C9A56E", 8, 6)
    b += g(frog(), at(1580, 190, .35)) + g(toad(), at(260, 650, .55)) + g(larva(), at(780, 490, .6)) + g(beetle(), at(1260, 330, .5))
    return b

@sc('question')
def _():
    b = BG("#232C3A") + moon(960, 280, 100)
    b += g(larva(), at(1000, 760, 1.5)) + g(frog(), at(500, 770, .9)) + stroke("M870 480 Q900 400 960 420 Q1040 440 990 520 Q960 560 960 600", LAMP, 16) + circ(960, 650, 10, LAMP, 0)
    return b

@sc('map')
def _():
    b = BG("#9FC6D6")
    b += poly([(200, 400), (500, 260), (900, 240), (1300, 300), (1700, 420), (1650, 640), (1300, 700), (1000, 620), (800, 760), (500, 700), (260, 560)], "#C9B77A", 6)
    b += poly([(900, 360), (1100, 360), (1100, 520), (900, 520)], "#8FA35A", 6)
    b += circ(1000, 440, 26, BRICK, 5) + line(1000, 466, 1280, 700, BRICK, 5) + panel(1230, 560, 480, 280, "#F4ECD6")
    b += g(beetle(), at(1470, 780, .5)) + arrow(1240, 560, 1040, 470, BRICK, 6)
    b += g(beetle(), at(380, 520, .35)) + g(beetle(), at(700, 580, .3)) + g(beetle(), at(1500, 520, .3))
    return b

@sc('recap')
def _():
    b = BG(PAPER)
    for x in (130, 700, 1270): b += panel(x, 180, 520, 640, "#E9DCBC")
    b += g(larva(), at(500, 560, .85)) + g(frog(), at(1000, 700, .8)) + g(beetle(), at(1500, 520, .8))
    b += eye_icon(430, 300, .8) + g(circ(0,0,14,BRICK,4), at(960, 300)) + arrow(780, 700, 560, 720, INK, 8)
    return b

@sc('pondnight')
def _():
    b = moon_night() + water(640) + ripples(600, 780, 3, 90) + reeds(1700, 720, 6, 380, 28, 7) + reeds(220, 720, 6, 380, 28, 9)
    b += lilypad(1000, 740) + g(frog(), at(1300, 790, 1.0, True)) + firefly(700, 430) + firefly(1100, 360)
    return b

@sc('ending')
def _():
    b = BG("#2B3442") + lab_desk() + rect(1360, 300, 24, 460, "#4A4A4A", 6, 5) + g(path("M-80 0 L80 0 L50 -90 L-50 -90Z", "#3E7F8C") + circ(0, 10, 40, LAMP, 5), at(1372, 300)) 
    b += g(g(circ(0, 0, 150, LAMP, 0, 'opacity="0.18"'), mv="lamp"), at(1372, 360)) + rect(380, 300, 520, 400, "#F4ECD6", 10, 6) + g(larva(), at(1000, 760, .8)) + g(beetle(), at(560, 600, .6))
    return b

if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    only = sys.argv[1:]
    for name, f in S_.items():
        if only and name not in only: continue
        # lamp mv on ending
        s = svg(f())
        if name == 'ending': s = s.replace('<circle cx="0" cy="10"', '<g id="mv-lamp"><circle cx="0" cy="10"', 1) if False else s
        open(os.path.join(OUT, name + '.svg'), 'w').write(s)
    print(len(S_), 'scenes')
