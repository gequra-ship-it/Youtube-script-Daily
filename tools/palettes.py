# -*- coding: utf-8 -*-
# Topic palettes for Miya's Lab pictures (2026-10-10, user: "colours were only purple or orange; match the script").
# Each palette gives the three background modes (paper / night / dusk), line colours, a wash colour for transitions and 4 accents.
# A video picks palettes in its config.py:  PAL_DEFAULT = 'sunset'      # legacy videos without PAL_DEFAULT keep the old look; NEW videos must set PAL_DEFAULT (build_audio PLAN=1 warns);  PAL = {'<art_theme>': '<palette name>', ...}
# Rule: choose the palette from what the script is ABOUT (place, material, mood), not from taste. Violet/magenta and orange are
# only allowed when the subject itself is violet/orange (sunset, fire, desert, space nebula). Max 3 palettes per video.
PALETTES = {
    'ocean':   dict(mood='sea, deep sea, rivers, water life',
                    paper=('#dfe6e6', '#1a2b3a'), night=('#04101f', '#0b2236', '#7fd6e0', '#5fe0d0'),
                    dusk=('#f2d9a8', '#7fb3c9', '#2b5877', '#1a2b3a'), wash=('#e3e9e8', '#0a1a2b', '#3c6a80'),
                    accents=('#2f8fa3', '#5ec2b7', '#e8d9a0', '#d9694a')),
    'forest':  dict(mood='forest, jungle, wetland, ponds, plants, insects',
                    paper=('#e3e5d6', '#1d2b1c'), night=('#07140e', '#122a1f', '#9fdca0', '#d8e87a'),
                    dusk=('#e9d9a0', '#8fae6a', '#3b6b4a', '#1d2b1c'), wash=('#e6e8d8', '#0c1d15', '#4b6e4c'),
                    accents=('#3f7d4e', '#8fb86a', '#c9a64a', '#7a5233')),
    'desert':  dict(mood='desert, savanna, heat, ancient dry lands, fire',
                    paper=('#ebe0c8', '#3a2a1a'), night=('#14100f', '#2a1c18', '#f0c070', '#ffd98a'),
                    dusk=('#f6d9a0', '#d9935a', '#8a4a3a', '#3a2a1a'), wash=('#eee3cb', '#1c1411', '#8a5a43'),
                    accents=('#c9833a', '#a9532f', '#e8c27a', '#5f7a6a')),
    'ice':     dict(mood='arctic, glaciers, cold, winter, high mountains',
                    paper=('#e4eaee', '#1b2a38'), night=('#06101c', '#10263a', '#a9dcf2', '#e8f4fb'),
                    dusk=('#e8eef2', '#a9c4d8', '#5c7fa0', '#1b2a38'), wash=('#e6ecf0', '#0c1a2a', '#5f7f98'),
                    accents=('#5c9cc4', '#a9dcf2', '#e8eef2', '#7a8aa0')),
    'lab':     dict(mood='science, medicine, microscopes, chemistry, data',
                    paper=('#e6e8e6', '#1c2326'), night=('#0a1214', '#14262b', '#8fe3d0', '#f2c14e'),
                    dusk=('#eae4d0', '#9ec3c0', '#4c7c80', '#1c2326'), wash=('#e8eae6', '#0d171a', '#4f7578'),
                    accents=('#3f9a96', '#e0a84a', '#d9694a', '#6b7c85')),
    'history': dict(mood='history, old cities, ships, manuscripts, archaeology',
                    paper=('#e8dcc4', '#2e2218'), night=('#13100c', '#241c14', '#e6c98a', '#f2c14e'),
                    dusk=('#f0d6a0', '#c9a068', '#6e5236', '#2e2218'), wash=('#eadfc8', '#1a140e', '#7a5e40'),
                    accents=('#8a5a34', '#b5483b', '#c9a64a', '#5f6b4a')),
    'space':   dict(mood='space, stars, planets, physics, time',
                    paper=('#e3e6ec', '#151a2e'), night=('#050818', '#0d1634', '#cfd8ff', '#f2c14e'),
                    dusk=('#e8d8c0', '#8a7fb0', '#2c2f66', '#151a2e'), wash=('#e5e8ee', '#080c20', '#3c4478'),
                    accents=('#4f6bd6', '#f2c14e', '#8fd6e8', '#c9d4ff')),
    'storm':   dict(mood='war, disasters, grim or heavy topics, weather, industry',
                    paper=('#dcdcd8', '#222428'), night=('#0c0e12', '#1a1e26', '#b8c2d0', '#e0c27a'),
                    dusk=('#d8d4cc', '#8a8f9a', '#454c5c', '#222428'), wash=('#dededa', '#10131a', '#58606e'),
                    accents=('#5c6b80', '#a35a4a', '#c9b27a', '#8a9aa8')),
    'body':    dict(mood='human body, biology of animals, hunting, warm-blooded life, food',
                    paper=('#eadfd6', '#2b1f1f'), night=('#120c10', '#241820', '#e8b0a8', '#f2c14e'),
                    dusk=('#f4d4c0', '#d68f8a', '#7a4a5a', '#2b1f1f'), wash=('#ece1d8', '#1a1014', '#7a5058'),
                    accents=('#b5483b', '#d68f8a', '#e8c27a', '#5f7a8a')),
    # --- cosmic family (space-science videos, STYLE='cosmic'): night is the main mode, glows are bright and saturated ---
    'nebula':  dict(mood='COSMIC: nebulae, star-forming clouds, galaxies, the beauty of space (magenta + teal)',
                    paper=('#e4e2ec', '#17142e'), night=('#050314', '#160a33', '#ffd0f0', '#ff5fc8'),
                    dusk=('#ffd2b8', '#c0509a', '#2a1b6e', '#17142e'), wash=('#e6e3ee', '#08051c', '#5a2a7a'),
                    accents=('#ff5fc8', '#36d6d0', '#8a6bff', '#ffd27a')),
    'aurora':  dict(mood='COSMIC: auras, planetary atmospheres, magnetospheres, solar wind (green + blue)',
                    paper=('#e0eceb', '#10262c'), night=('#02101a', '#06283a', '#b5ffe0', '#46f0b0'),
                    dusk=('#d8f5e0', '#3fc9a0', '#1a4a7a', '#10262c'), wash=('#e2eeec', '#04121c', '#1f6e78'),
                    accents=('#46f0b0', '#4aa8ff', '#b58cff', '#f2f08a')),
    'deepfield': dict(mood='COSMIC: deep space, distant galaxies, black holes, cosmic scale (navy + gold)',
                    paper=('#e2e5ee', '#12182c'), night=('#02030c', '#0a1030', '#e6ecff', '#ffc65a'),
                    dusk=('#f3dcb0', '#6f78c8', '#161c52', '#12182c'), wash=('#e4e7ef', '#040618', '#2a3278'),
                    accents=('#ffc65a', '#6f8cff', '#d6e4ff', '#ff7a5a')),
    'solar':   dict(mood='COSMIC: the Sun, stars, supernovae, solar flares, hot plasma (red-orange + white)',
                    paper=('#efe4d6', '#2a160e'), night=('#0e0504', '#2a0e08', '#ffd9a8', '#ff7a3a'),
                    dusk=('#fff0c8', '#ff9a4a', '#a8281c', '#2a160e'), wash=('#f0e5d6', '#160806', '#a8402a'),
                    accents=('#ff7a3a', '#ffd27a', '#fff4e0', '#4a8cff')),
    'sunset':  dict(mood='ONLY for sunsets, evenings, dreams, fantasy (the old purple/peach look)',
                    paper=('#e5e3dd', '#1b1830'), night=('#0b0a21', '#16142f', '#b9a6ff', '#f2c14e'),
                    dusk=('#f3c290', '#d68673', '#7c4577', '#1b1830'), wash=('#ece4d1', '#14122b', '#5a4562'),
                    accents=('#6b4bd6', '#d64b9a', '#f2c14e', '#d9694a')),
}
DEFAULT = 'sunset'      # legacy videos without PAL_DEFAULT keep the old look; NEW videos must set PAL_DEFAULT (build_audio PLAN=1 warns)

def get(name):
    p = PALETTES[name]; return dict(name=name, **p)

def for_theme(cfg, theme):
    """palette name for an art_theme: cfg.PAL[theme] else cfg.PAL_DEFAULT else 'sunset' (legacy)"""
    pal = getattr(cfg, 'PAL', {}); return pal.get(theme) or getattr(cfg, 'PAL_DEFAULT', None) or DEFAULT

def describe(name):
    p = PALETTES[name]
    return dict(palette=name, paper_base=p['paper'][0], paper_ink=p['paper'][1],
                night_top=p['night'][0], night_bottom=p['night'][1], night_line=p['night'][2], night_glow=p['night'][3],
                dusk_stops=list(p['dusk'][:3]), dusk_ink=p['dusk'][3], accents=list(p['accents']))
