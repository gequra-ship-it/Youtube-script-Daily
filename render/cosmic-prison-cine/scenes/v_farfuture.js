// farfuture — deep time in one patch of a galaxy (cosmic-prison-cine S41-S44; written 2026-10-15). A slow stage: a rich 3D star
// field (sun-like stars, a few blue giants with halos, thousands of dim red dwarfs) inside a galaxy region with a warm core glow,
// pink-gold gas clouds with young stars being born in them. Then the stars age, era by era, calmly (no strobe):
//   entropy    S41 the gas clouds thin out and fade; star birth stops (no new young stars ignite after this cue)
//   dim        S42 sun-like stars swell orange and burn out into faint white-dwarf points; blue giants collapse into a few
//              neutron-star glints (slow soft pulse) and black holes (small black spheres with thin glowing photon-ring rims);
//              the red dwarfs remain and slowly fade; the core glow dims
//   decay      S43 matter dissolves: every remnant point breaks into a few faint particles that drift and fade; only the black
//              holes remain
//   evaporate  S43 the black holes glow faintly (Hawking radiation, symbolic: hotter as they shrink), shrink to nothing one by one
//              and leave faint photons streaming away
//   freeze     S44 near-black: a thin, even soup of extremely faint particles drifting very slowly; silence
//   side       subject offset (default .12)
// Without cues the scene is a living star field with gas clouds and star birth.
(window.MIYA = window.MIYA || { scenes: {} }).scenes.farfuture = function (ctx, p) {
  const { T, sm, rng, cue, points, glow, ctex } = ctx, K = window.MIYA.kit;
  const S = new T.Scene(); const BG0 = new T.Color('#070820'), BG1 = new T.Color('#03040e'), BG2 = new T.Color('#010107'); S.background = BG0.clone();
  const cT = c => c == null ? 1e9 : cue(c);
  const cEn = cT(p.entropy), cDi = cT(p.dim), cDe = cT(p.decay), cEv = cT(p.evaporate), cFr = cT(p.freeze);
  const v3 = (x, y, z) => new T.Vector3(x, y, z);

  // ---------------- far background: distant stars + the galaxy's warm core glow + dust band ----------------
  const far = ctx.stars(S, 3500, 700, { size: 1.0, opacity: .5, seed: 23 });
  const core = glow(S, '#ffcf8a', 520, .16), core2 = glow(S, '#ff9fb8', 260, .1), band = glow(S, '#5a4bc0', 900, .12);
  core.position.set(260, 60, -560); core2.position.set(250, 55, -540); band.position.set(80, 20, -650);

  // ---------------- gas clouds (pink-gold, soft noise sprites) ----------------
  const cloudT = (() => { const c = K.noise(256, { seed: 12, octaves: 3 }), g = c.getContext('2d'); g.globalCompositeOperation = 'destination-in';
    const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128); gr.addColorStop(0, 'rgba(0,0,0,1)'); gr.addColorStop(.5, 'rgba(0,0,0,.55)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
    const t2 = new T.CanvasTexture(c); t2.colorSpace = T.SRGBColorSpace; return t2; })();
  const RC = rng(31), clouds = [], CC = ['#ff8fb4', '#ffb48a', '#ffc65a', '#c27ad8', '#ff7aa0'];
  for (let k = 0; k < 16; k++) { const m = new T.Sprite(new T.SpriteMaterial({ map: cloudT, color: CC[k % 5], transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, rotation: RC() * 6.28 }));
    const s = 16 + RC() * 26, pos = v3(-10 + RC() * 55, (RC() - .5) * 26, -45 + RC() * 40); m.position.copy(pos); m.scale.set(s, s * (.55 + .4 * RC()), 1); S.add(m);
    clouds.push({ m, s, pos, ok: .5 + .5 * RC(), rs: (RC() - .5) * .01 }); }

  // ---------------- stars (3D points in a slab around the subject) ----------------
  const RS = rng(41), rpos = (spread) => v3((RS() - .38) * 120 * spread, (RS() - .5) * 56 * spread, -70 + RS() * 85);
  // sun-like stars
  const NSu = 700, su = points(NSu, { size: 1.0 }), suA = su.geometry.attributes.position.array, suC = su.geometry.attributes.color.array, suB = [];
  for (let i = 0; i < NSu; i++) { const q = rpos(1); suA.set([q.x, q.y, q.z], i * 3); const w = RS(); suB.push({ q, br: .55 + .8 * Math.pow(RS(), 2), col: w < .5 ? [1, .93, .78] : [1, .98, .92], tb: cDi + RS() * 10, ph: RS() * 6.28 }); }
  S.add(su);
  // red dwarfs: many, dim
  const NRd = 2600, rd = points(NRd, { size: .75 }), rdA = rd.geometry.attributes.position.array, rdC = rd.geometry.attributes.color.array, rdB = [];
  for (let i = 0; i < NRd; i++) { const q = rpos(1.05); rdA.set([q.x, q.y, q.z], i * 3); rdB.push({ q, br: .35 + .45 * RS(), td: cDe + RS() * 8 }); }
  S.add(rd);
  // blue giants -> black holes (first 6) or neutron stars (rest)
  const NBG = 16, bgS = [], RB = rng(51);
  const BHP = [v3(6, 3, -6), v3(9, -10, -16), v3(-4, -8, -22), v3(30, 9, -30), v3(12, 12, -40), v3(-8, 11, -12)];
  for (let i = 0; i < NBG; i++) { const q = i < 6 ? BHP[i] : v3(-20 + RB() * 70, (RB() - .5) * 34, -50 + RB() * 50);
    const h = glow(S, '#bcd2ff', 3.2, 0), c = glow(S, '#f2f6ff', .9, 0); h.position.copy(q); c.position.copy(q);
    bgS.push({ q, h, c, tb: cDi + .3 + RB() * 5, ph: RB() * 6.28 }); }
  // neutron-star glint texture (soft 4-point star)
  const spikeT = ctex(128, (g, s) => { g.translate(s / 2, s / 2); for (let k = 0; k < 4; k++) { g.rotate(Math.PI / 2); const gr = g.createLinearGradient(0, 0, s / 2, 0); gr.addColorStop(0, 'rgba(255,255,255,.9)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.beginPath(); g.moveTo(0, -2); g.lineTo(s / 2, 0); g.lineTo(0, 2); g.fill(); } });
  const nsG = bgS.slice(6).map(b => { const m = new T.Sprite(new T.SpriteMaterial({ map: spikeT, color: '#cfeaff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false })); m.position.copy(b.q); S.add(m); return m; });
  // black holes: black sphere + photon ring sprite + faint Hawking glow
  const ringT = ctex(256, (g, s) => { const gr = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.48, 'rgba(255,255,255,0)'); gr.addColorStop(.53, 'rgba(255,240,220,1)'); gr.addColorStop(.6, 'rgba(255,200,140,.28)'); gr.addColorStop(.8, 'rgba(255,170,110,.06)'); gr.addColorStop(1, 'rgba(255,160,100,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); });
  const bhM = new T.MeshBasicMaterial({ color: '#000000' }), bhs = [];
  BHP.forEach((q, i) => { const r0 = .55 + .25 * (i % 3), sph = new T.Mesh(new T.SphereGeometry(1, 32, 16), bhM); sph.position.copy(q); S.add(sph);
    const ring = new T.Sprite(new T.SpriteMaterial({ map: ringT, color: '#ffd9a0', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false })); ring.position.copy(q); S.add(ring);
    const hw = glow(S, '#ffe9cf', 1, 0); hw.position.copy(q);
    bhs.push({ q, r0, sph, ring, hw, te: cEv + i * 1.7 + (i % 2) * .6 }); });
  const EVD = 7;   // seconds a black hole takes to evaporate (after its own start te)
  // young stars born in the clouds (each ignites at its birth time if that is before "entropy")
  const NY = 36, yS = [], RY = rng(61);
  for (let i = 0; i < NY; i++) { const cl = clouds[i % clouds.length], q = cl.pos.clone().add(v3((RY() - .5) * cl.s * .5, (RY() - .5) * cl.s * .3, (RY() - .5) * 4));
    const h = glow(S, '#d8e4ff', 2.2, 0), c = glow(S, '#ffffff', .7, 0); h.position.copy(q); c.position.copy(q);
    yS.push({ q, h, c, tb: ctx.t0 + 1 + i * 1.6 + RY() * 1.2 }); }

  // ---------------- decay debris: each remnant breaks into faint particles ----------------
  const ND = 3600, db = points(ND, { size: .55 }), dbA = db.geometry.attributes.position.array, dbC = db.geometry.attributes.color.array, dbB = [];
  { const r = rng(71); for (let i = 0; i < ND; i++) { const isS = i % 3 === 0, ix = isS ? (i * 7) % NSu : (i * 13) % NRd, src = isS ? suB[ix] : rdB[ix], u = r() * 2 - 1, th = r() * 6.283, s = Math.sqrt(1 - u * u);
    dbB.push({ q: src.q, d: [s * Math.cos(th), u, s * Math.sin(th)], sp: .6 + 1.6 * r(), t0: (isS ? cDe + (ix % 9) : src.td) + r() * .8, w: .5 + .5 * r() }); } }
  db.frustumCulled = false; S.add(db);
  // Hawking photons streaming away from each evaporating black hole
  const NP = 900, ph = points(NP, { size: .4 }), phA = ph.geometry.attributes.position.array, phC = ph.geometry.attributes.color.array, phB = [];
  { const r = rng(81); for (let i = 0; i < NP; i++) { const b = bhs[i % bhs.length], u = r() * 2 - 1, th = r() * 6.283, s = Math.sqrt(1 - u * u);
    phB.push({ b, d: [s * Math.cos(th), u, s * Math.sin(th)], te: b.te + Math.pow(r(), .6) * EVD, sp: 2.5 + 2 * r() }); } }
  ph.frustumCulled = false; S.add(ph);
  // the final soup: extremely faint, even particles, drifting very slowly
  const NQ = 2600, sp = points(NQ, { size: .5 }), spA = sp.geometry.attributes.position.array, spC = sp.geometry.attributes.color.array, spB = [];
  { const r = rng(91); for (let i = 0; i < NQ; i++) spB.push([(r() - .4) * 130, (r() - .5) * 64, -80 + r() * 100, r() * 6.283, r()]); }
  sp.frustumCulled = false; S.add(sp);

  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .1, 2000); ctx.side(cam, p.side == null ? .12 : p.side);
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const en = sm(cEn, cEn + 10, t), di = sm(cDi, cDi + 12, t), de = sm(cDe, cDe + 10, t), fr = sm(cFr, cFr + 8, t), ev = sm(cEv, cEv + 4, t);
    const dark = Math.max(di * .5, de);
    S.background.copy(BG0).lerp(BG1, dark).lerp(BG2, fr);
    // camera: a slow drift through the region, pulling back a little as the eras pass
    cam.position.set(4 * Math.sin(u * .012) - 2, 2 + 1.5 * Math.sin(u * .009), 62 + u * .04 + 6 * de);
    cam.lookAt(2, 0, -12);
    far.material.opacity = .5 * (1 - .55 * di) * (1 - .8 * de) * (1 - .9 * fr);
    core.material.opacity = .16 * (1 - .6 * di) * (1 - de); core2.material.opacity = .1 * (1 - en) * (1 - de); band.material.opacity = .12 * (1 - .5 * di) * (1 - .9 * de);
    clouds.forEach(c => { const k = 1 + .35 * en; c.m.scale.set(c.s * k, c.s * k * .7, 1); c.m.material.opacity = .2 * c.ok * (1 - en) * (.9 + .1 * Math.sin(t * .15 + c.s)); c.m.material.rotation = c.rs * t + c.s; });
    // young stars: ignite (only births before "entropy"), then shine; fade with the dim era
    yS.forEach(y => { const on = y.tb < cEn ? sm(y.tb, y.tb + 2, t) : 0, f = on * (1 - di); y.h.material.opacity = .35 * f; y.c.material.opacity = .9 * f; });
    // sun-like stars: shine, then (dim) swell orange and shrink to a faint white dwarf; white dwarfs dissolve at decay
    for (let i = 0; i < NSu; i++) { const b = suB[i], a = t - b.tb, tw = .9 + .1 * Math.sin(t * .8 + b.ph); let r, g, bl;
      if (a < 0) { r = b.col[0]; g = b.col[1]; bl = b.col[2]; r *= b.br * tw; g *= b.br * tw; bl *= b.br * tw; }
      else { const sw = sm(0, 1.5, a) * (1 - sm(1.5, 4, a)), wd = sm(2, 4.5, a), k = b.br * (1 - wd) + .22 * wd;
        r = (b.col[0] + .1 * sw) * k * (1 + .8 * sw); g = (b.col[1] - .3 * sw) * k * (1 + .8 * sw); bl = (b.col[2] - .5 * sw) * k * (1 + .8 * sw);
        if (wd > 0) { r = r * (1 - wd) + .7 * k * wd; g = g * (1 - wd) + .8 * k * wd; bl = bl * (1 - wd) + 1 * k * wd; } }
      const dd = 1 - sm(0, 3, t - (cDe + (i % 9)));
      suC[i * 3] = r * dd; suC[i * 3 + 1] = g * dd; suC[i * 3 + 2] = bl * dd; }
    su.geometry.attributes.color.needsUpdate = true;
    // red dwarfs: remain through the dim era, slowly fading; dissolve at decay
    const rf = 1 - .6 * sm(cDi, cDi + 30, t);
    for (let i = 0; i < NRd; i++) { const b = rdB[i], k = b.br * rf * (1 - sm(b.td, b.td + 3, t)); rdC[i * 3] = k; rdC[i * 3 + 1] = k * .42; rdC[i * 3 + 2] = k * .3; }
    rd.geometry.attributes.color.needsUpdate = true;
    // blue giants: collapse (bright swell), then a neutron star glint or a black hole
    bgS.forEach((b, i) => { const a = t - b.tb, sw = sm(-.5, .8, a) * (1 - sm(.8, 2.6, a)), alive = a < .8 ? 1 : 0, tw = .9 + .1 * Math.sin(t * .7 + b.ph);
      b.h.material.opacity = .45 * tw * alive + .5 * sw; b.h.scale.setScalar(3.2 + 5 * sw); b.c.material.opacity = (.95 * alive + .8 * sw);
      if (i >= 6) { const n = nsG[i - 6], on = sm(1, 2.5, a) * (1 - sm(cDe + (i % 5), cDe + (i % 5) + 3, t)); n.material.opacity = 1.0 * on * (.75 + .25 * Math.sin(t * 2.1 + b.ph)); n.scale.setScalar(2.4 + .4 * Math.sin(t * 2.1 + b.ph)); } });
    // black holes: appear where the first giants collapsed; at "evaporate" glow faintly, shrink to nothing
    bhs.forEach((b, i) => { const born = sm(bgS[i].tb + .6, bgS[i].tb + 2.2, t), e = Math.min(1, Math.max(0, (t - b.te) / EVD));
      const r = b.r0 * Math.pow(1 - e, .5) * (.4 + .6 * born), gone = e >= 1;
      b.sph.visible = born > 0 && !gone; b.sph.scale.setScalar(Math.max(1e-3, r));
      b.ring.scale.setScalar(Math.max(1e-3, r * 2 * 1.9)); b.ring.material.opacity = born * (gone ? 0 : .9);
      const hk = e > 0 ? sm(0, .5, e) * (1 - sm(.92, 1, e)) * (.3 + .7 * e) : 0; b.hw.scale.setScalar(.6 + 3.5 * r + 4 * hk); b.hw.material.opacity = 1.1 * hk + (gone ? .45 * Math.exp(-(t - b.te - EVD) * .8) : 0); });
    // debris after decay
    for (let i = 0; i < ND; i++) { const b = dbB[i], a = t - b.t0; let v = 0;
      if (a > 0) { const s = b.sp * (1 - Math.exp(-a * .25)) * 3; dbA[i * 3] = b.q.x + b.d[0] * s; dbA[i * 3 + 1] = b.q.y + b.d[1] * s; dbA[i * 3 + 2] = b.q.z + b.d[2] * s;
        v = .55 * b.w * sm(0, 1.5, a) * Math.exp(-a / 10) * (1 - fr); }
      else dbA[i * 3 + 1] = -9999;
      dbC[i * 3] = v; dbC[i * 3 + 1] = v * .85; dbC[i * 3 + 2] = v * .9; }
    db.geometry.attributes.position.needsUpdate = true; db.geometry.attributes.color.needsUpdate = true;
    // Hawking photons
    for (let i = 0; i < NP; i++) { const b = phB[i], a = t - b.te; let v = 0;
      if (a > 0 && a < 14) { const s = b.sp * a; phA[i * 3] = b.b.q.x + b.d[0] * s; phA[i * 3 + 1] = b.b.q.y + b.d[1] * s; phA[i * 3 + 2] = b.b.q.z + b.d[2] * s; v = 1.1 * Math.exp(-a / 4) * sm(0, .3, a); }
      else phA[i * 3 + 1] = -9999;
      phC[i * 3] = v; phC[i * 3 + 1] = v * .92; phC[i * 3 + 2] = v * .8; }
    ph.geometry.attributes.position.needsUpdate = true; ph.geometry.attributes.color.needsUpdate = true;
    // soup: appears with decay, very faint and even, slowest drift at the freeze
    const sv = .32 * de * (1 - .4 * fr) + .05 * ev * (1 - fr);
    for (let i = 0; i < NQ; i++) { const b = spB[i]; spA[i * 3] = b[0] + .25 * Math.sin(t * .02 + b[3]); spA[i * 3 + 1] = b[1] + .2 * Math.cos(t * .017 + b[3]); spA[i * 3 + 2] = b[2];
      const v = sv * (.5 + .5 * b[4]); spC[i * 3] = v * .8; spC[i * 3 + 1] = v * .85; spC[i * 3 + 2] = v; }
    sp.geometry.attributes.position.needsUpdate = true; sp.geometry.attributes.color.needsUpdate = true;
  } };
};
