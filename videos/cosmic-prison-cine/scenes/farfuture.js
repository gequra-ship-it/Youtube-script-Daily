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
// staging pass (2026-10-16): the shot is an ACCELERATING TIME-LAPSE.
//   - a clock of light (no numerals) stands behind the field: a ring of tick points, a hub, a faint hand and a gold comet head
//     whose trail grows with speed; it turns ever faster (rate grows ~40x by `evaporate`, capped so it blurs into a ring, never
//     strobes); five era beads above it light one by one (shot start, dim, decay, evaporate, freeze) with a soft pulse; the whole
//     clock fades out after `freeze` (+10..+20 s: "time loses meaning")
//   - the star field swirls around a vertical axis (differential rotation, inner faster), also accelerating; fast stars draw
//     motion streaks whose length follows their speed
//   - suns burn out one after another and ever faster from `entropy` + 3 s to `dim` + 12 s (the brightest ones flare orange and
//     puff a small planetary-nebula ring); blue giants die first, each with a soft supernova swell and a shock ring
//   - black holes evaporate smallest first, the largest last, each ending in a Hawking flash (rise ~.2 s, fade ~1.2 s), a shock
//     ring and a spray of photons; all done before `freeze`
//   - near-field motes drift in front of the field for depth
(window.MIYA = window.MIYA || { scenes: {} }).scenes.farfuture = function (ctx, p) {
  const { T, sm, rng, cue, points, glow, ctex } = ctx, K = window.MIYA.kit;
  const S = new T.Scene(); const BG0 = new T.Color('#070820'), BG1 = new T.Color('#03040e'), BG2 = new T.Color('#010107'); S.background = BG0.clone();
  const cT = c => c == null ? 1e9 : cue(c);
  const cEn = cT(p.entropy), cDi = cT(p.dim), cDe = cT(p.decay), cEv = cT(p.evaporate), cFr = cT(p.freeze);
  const v3 = (x, y, z) => new T.Vector3(x, y, z);
  const t0 = ctx.t0, t1 = ctx.t1;
  // accelerating clock: rate r(u) = r0 e^(ku) softly capped at rm; F = its integral in revolutions (closed form, seek-safe)
  const tRef = (cEv < 1e8 ? cEv : t0 + .65 * (t1 - t0)), KC = Math.log(40) / Math.max(30, tRef - t0), R0 = .025;
  const Fcap = (tt, rm) => { const uu = Math.max(0, tt - t0); return rm / KC * Math.log((1 + R0 * Math.exp(KC * uu) / rm) / (1 + R0 / rm)); };
  const Rcap = (tt, rm) => { const e = R0 * Math.exp(KC * Math.max(0, tt - t0)); return e / (1 + e / rm); };
  // the field swirls about a vertical axis through SC (inner faster), on the same accelerating clock but capped lower
  const SC = v3(10, 0, -25), omOf = q => .2 * 20 / Math.max(8, Math.hypot(q.x - SC.x, q.z - SC.z));
  const rot = (q, ph, o) => { const dx = q.x - SC.x, dz = q.z - SC.z, c = Math.cos(ph), s = Math.sin(ph); return o.set(SC.x + dx * c - dz * s, q.y, SC.z + dx * s + dz * c); };
  const swAt = tt => Fcap(tt, .35);
  // burn-out schedule: sparse first, then ever faster (cumulative fraction ~ x^3)
  const tS = cEn < 1e8 ? Math.min(cEn + 3, cDi - 8) : cDi - 20, tE = cDi + 12;
  const burnAt = f => cDi < 1e8 ? tS + (tE - tS) * Math.pow(f, 1 / 3) : 1e9;
  // camera-facing motion streaks (copied from lightspeed.js)
  function streaks(par, n, o) { o = o || {}; const g = new T.BufferGeometry(), H = new Float32Array(n * 12), Tl = new Float32Array(n * 12), C = new Float32Array(n * 12), Wd = new Float32Array(n * 4), cr = new Float32Array(n * 8), ix = [];
    for (let i = 0; i < n; i++) { cr.set([0, 0, 0, 1, 1, 0, 1, 1], i * 8); const b = i * 4; ix.push(b, b + 2, b + 1, b + 1, b + 2, b + 3); }
    const ad = (a, k) => { const q = new T.BufferAttribute(a, k); q.setUsage(T.DynamicDrawUsage); g.setAttribute(['aH', 'aT', 'aC', 'aW'][[H, Tl, C, Wd].indexOf(a)], q); };
    ad(H, 3); ad(Tl, 3); ad(C, 3); ad(Wd, 1); g.setAttribute('corner', new T.BufferAttribute(cr, 2)); g.setAttribute('position', new T.BufferAttribute(new Float32Array(n * 12), 3)); g.setIndex(ix);
    const m = new T.ShaderMaterial({ uniforms: { uH: { value: ctx.H }, uMin: { value: o.minPx || 1.6 }, uNear: { value: new T.Vector2(...(o.near || [.5, 4])) } }, transparent: true, depthWrite: false, depthTest: o.depthTest !== false, blending: T.AdditiveBlending, side: T.DoubleSide,
      vertexShader: `attribute vec3 aH, aT, aC; attribute float aW; attribute vec2 corner; uniform float uH, uMin; uniform vec2 uNear; varying vec2 vUv; varying vec3 vC; varying float vCap;
        void main(){ vec3 wH = (modelMatrix * vec4(aH, 1.)).xyz, wT = (modelMatrix * vec4(aT, 1.)).xyz, d = wH - wT; float L = length(d); vec3 dir = L > 1e-5 ? d / L : vec3(1., 0., 0.);
          vec3 P0 = mix(wT, wH, corner.x), V = cameraPosition - P0; float dc = max(length(V), 1e-4);
          float w = max(aW, dc * 2. / (projectionMatrix[1][1] * uH) * uMin); vec3 sd = cross(dir, V); float sl = length(sd); sd = sl > 1e-6 ? sd / sl : vec3(0., 1., 0.);
          vec3 P = P0 + sd * (corner.y - .5) * w + dir * (corner.x - .5) * w;
          vUv = corner; vCap = clamp(w / (L + w), .02, 1.); vC = aC * (aW / w) * smoothstep(uNear.x, uNear.y, dc);
          gl_Position = projectionMatrix * viewMatrix * vec4(P, 1.); }`,
      fragmentShader: `varying vec2 vUv; varying vec3 vC; varying float vCap;
        void main(){ float x = vUv.x, y = abs(vUv.y * 2. - 1.); float a = pow(x, 1.6) * smoothstep(1., 1. - vCap, x) * pow(max(0., 1. - y * y), 2.);
          gl_FragColor = vec4(vC * a, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` });
    const M = new T.Mesh(g, m); M.frustumCulled = false; M.renderOrder = o.order || 0; par.add(M);
    return { mesh: M, set(i, hx, hy, hz, tx, ty, tz, w, r, gg, b) { for (let k = 0; k < 4; k++) { const j = (i * 4 + k) * 3; H[j] = hx; H[j + 1] = hy; H[j + 2] = hz; Tl[j] = tx; Tl[j + 1] = ty; Tl[j + 2] = tz; C[j] = r; C[j + 1] = gg; C[j + 2] = b; Wd[i * 4 + k] = w; } },
      hide(i) { for (let k = 0; k < 4; k++) { const j = (i * 4 + k) * 3; C[j] = C[j + 1] = C[j + 2] = 0; } },
      commit() { ['aH', 'aT', 'aC', 'aW'].forEach(k => g.attributes[k].needsUpdate = true); } }; }

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
  for (let i = 0; i < NSu; i++) { const q = rpos(1); suA.set([q.x, q.y, q.z], i * 3); const w = RS(); suB.push({ q, br: .55 + .8 * Math.pow(RS(), 2), col: w < .5 ? [1, .93, .78] : [1, .98, .92], tb: (RS(), 0), ph: RS() * 6.28 }); }
  { const r = rng(43), ord = suB.map((b, i) => i).sort((a, b) => suB[b].br - suB[a].br); suB.forEach(b => { b.tb = burnAt(r()); b.om = omOf(b.q); });
    ord.slice(0, 40).forEach((i, j) => { suB[i].tb = burnAt((j + .5) / 40 * .85); suB[i].big = j; }); }
  const BIG = suB.map((b, i) => i).filter(i => suB[i].big != null);
  S.add(su);
  // red dwarfs: many, dim
  const NRd = 2600, rd = points(NRd, { size: .75 }), rdA = rd.geometry.attributes.position.array, rdC = rd.geometry.attributes.color.array, rdB = [];
  for (let i = 0; i < NRd; i++) { const q = rpos(1.05); rdA.set([q.x, q.y, q.z], i * 3); rdB.push({ q, br: .35 + .45 * RS(), td: cDe + RS() * 8, om: omOf(q) }); }
  S.add(rd);
  // blue giants -> black holes (first 6) or neutron stars (rest)
  const NBG = 16, bgS = [], RB = rng(51);
  const BHP = [v3(6, 3, -6), v3(9, -10, -16), v3(-4, -8, -22), v3(30, 9, -30), v3(12, 12, -40), v3(-8, 11, -12)];
  for (let i = 0; i < NBG; i++) { const q = i < 6 ? BHP[i] : v3(-20 + RB() * 70, (RB() - .5) * 34, -50 + RB() * 50);
    const h = glow(S, '#bcd2ff', 3.2, 0), c = glow(S, '#f2f6ff', .9, 0); h.position.copy(q); c.position.copy(q);
    bgS.push({ q, h, c, tb: (RB(), 0), ph: RB() * 6.28, om: omOf(q) }); }
  { const r = rng(53), gS = tS - 4, gE = cDi + 4; bgS.forEach(b => { b.tb = cDi < 1e8 ? gS + (gE - gS) * Math.sqrt(r()) : 1e9; }); }
  // neutron-star glint texture (soft 4-point star)
  const spikeT = ctex(128, (g, s) => { g.translate(s / 2, s / 2); for (let k = 0; k < 4; k++) { g.rotate(Math.PI / 2); const gr = g.createLinearGradient(0, 0, s / 2, 0); gr.addColorStop(0, 'rgba(255,255,255,.9)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.beginPath(); g.moveTo(0, -2); g.lineTo(s / 2, 0); g.lineTo(0, 2); g.fill(); } });
  const nsG = bgS.slice(6).map(b => { const m = new T.Sprite(new T.SpriteMaterial({ map: spikeT, color: '#cfeaff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false })); m.position.copy(b.q); S.add(m); return m; });
  // black holes: black sphere + photon ring sprite + faint Hawking glow
  const ringT = ctex(256, (g, s) => { const gr = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.48, 'rgba(255,255,255,0)'); gr.addColorStop(.53, 'rgba(255,240,220,1)'); gr.addColorStop(.6, 'rgba(255,200,140,.28)'); gr.addColorStop(.8, 'rgba(255,170,110,.06)'); gr.addColorStop(1, 'rgba(255,160,100,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); });
  const bhM = new T.MeshBasicMaterial({ color: '#000000' }), bhs = [];
  BHP.forEach((q, i) => { const r0 = .55 + .25 * (i % 3), sph = new T.Mesh(new T.SphereGeometry(1, 32, 16), bhM); sph.position.copy(q); S.add(sph);
    const ring = new T.Sprite(new T.SpriteMaterial({ map: ringT, color: '#ffd9a0', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false })); ring.position.copy(q); S.add(ring);
    const hw = glow(S, '#ffe9cf', 1, 0); hw.position.copy(q);
    bhs.push({ q, r0, sph, ring, hw, om: omOf(q) }); });
  // evaporation order: smallest first, the largest last; spacing and duration shrink (the time-lapse speeds up)
  { const TE = [.5, 3, 5.2, 7, 8.4, 9.4], ED = [5.5, 5, 4.6, 4.3, 4.4, 4.8]; bhs.map((b, i) => i).sort((a, b) => bhs[a].r0 - bhs[b].r0 + (a - b) * 1e-3).forEach((i, k) => { bhs[i].te = cEv + TE[k]; bhs[i].ed = ED[k]; }); }
  // young stars born in the clouds (each ignites at its birth time if that is before "entropy")
  const NY = 36, yS = [], RY = rng(61);
  for (let i = 0; i < NY; i++) { const cl = clouds[i % clouds.length], q = cl.pos.clone().add(v3((RY() - .5) * cl.s * .5, (RY() - .5) * cl.s * .3, (RY() - .5) * 4));
    const h = glow(S, '#d8e4ff', 2.2, 0), c = glow(S, '#ffffff', .7, 0); h.position.copy(q); c.position.copy(q);
    yS.push({ q, h, c, tb: ctx.t0 + 1 + i * 1.6 + RY() * 1.2 }); }

  // ---------------- decay debris: each remnant breaks into faint particles ----------------
  const ND = 3600, db = points(ND, { size: .55 }), dbA = db.geometry.attributes.position.array, dbC = db.geometry.attributes.color.array, dbB = [];
  { const r = rng(71); for (let i = 0; i < ND; i++) { const isS = i % 3 === 0, ix = isS ? (i * 7) % NSu : (i * 13) % NRd, src = isS ? suB[ix] : rdB[ix], u = r() * 2 - 1, th = r() * 6.283, s = Math.sqrt(1 - u * u);
    dbB.push({ src, d: [s * Math.cos(th), u, s * Math.sin(th)], sp: .6 + 1.6 * r(), t0: (isS ? cDe + (ix % 9) : src.td) + r() * .8, w: .5 + .5 * r() }); } }
  db.frustumCulled = false; S.add(db);
  // Hawking photons streaming away from each evaporating black hole
  const NP = 900, ph = points(NP, { size: .4 }), phA = ph.geometry.attributes.position.array, phC = ph.geometry.attributes.color.array, phB = [];
  { const r = rng(81); for (let i = 0; i < NP; i++) { const b = bhs[i % bhs.length], u = r() * 2 - 1, th = r() * 6.283, s = Math.sqrt(1 - u * u);
    const fin = r() < .3; phB.push({ b, d: [s * Math.cos(th), u, s * Math.sin(th)], te: fin ? b.te + b.ed : b.te + Math.pow(r(), .6) * b.ed, sp: fin ? 6 + 4 * r() : 2.5 + 2 * r(), fin }); } }
  ph.frustumCulled = false; S.add(ph);
  // the final soup: extremely faint, even particles, drifting very slowly
  const NQ = 2600, sp = points(NQ, { size: .5 }), spA = sp.geometry.attributes.position.array, spC = sp.geometry.attributes.color.array, spB = [];
  { const r = rng(91); for (let i = 0; i < NQ; i++) spB.push([(r() - .4) * 130, (r() - .5) * 64, -80 + r() * 100, r() * 6.283, r()]); }
  sp.frustumCulled = false; S.add(sp);

  // ---------------- staging FX (2026-10-16) ----------------
  const ringBig = BIG.map(i => { const g = glow(S, '#ffa860', 1, 0), n = new T.Sprite(new T.SpriteMaterial({ map: ringT, color: i % 2 ? '#7fe0d0' : '#ff9cc0', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false })); S.add(n); return { i, g, n }; });
  const gShock = bgS.map(() => { const n = new T.Sprite(new T.SpriteMaterial({ map: ringT, color: '#a8c4ff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false })); S.add(n); return n; });
  const bhFx = bhs.map(() => { const f = glow(S, '#e6efff', 1, 0), n = new T.Sprite(new T.SpriteMaterial({ map: ringT, color: '#cfe0ff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false })); S.add(n); return { f, n }; });
  // motion streaks for the brightest suns and the giants
  const SST = BIG.concat(suB.map((b, i) => i).filter(i => suB[i].big == null && suB[i].br > .9).slice(0, 200)), sStr = streaks(S, SST.length + NBG, { minPx: 1.2, near: [4, 14] });
  // near-field motes (parallax)
  const NMo = 260, mo = points(NMo, { size: .18 }), moA = mo.geometry.attributes.position.array, moC = mo.geometry.attributes.color.array, MOB = [];
  { const r = rng(95); for (let i = 0; i < NMo; i++) { MOB.push([(r() - .3) * 60, (r() - .5) * 30, 22 + r() * 30, r() * 6.283]); const b = .25 + .5 * r(); moC.set([b, b * .9, b * .85], i * 3); } }
  mo.frustumCulled = false; S.add(mo);
  // the clock of light: tick ring, hub, faint hand, comet head + trail, era beads
  const DG = new T.Group(); DG.position.set(8.5, -1, -34); DG.lookAt(0, 2, 66); S.add(DG); const RD = 13;
  const tk = points(72, { size: .7 }), tkA = tk.geometry.attributes.position.array, tkC = tk.geometry.attributes.color.array;
  for (let i = 0; i < 72; i++) { const a = i / 60 * 6.2832, big = i % 5 === 0, rr = big ? RD - .5 : RD; if (i < 60) tkA.set([rr * Math.cos(a), rr * Math.sin(a), 0], i * 3); else { const b = (i - 60) / 12 * 6.2832; tkA.set([(RD - 1.3) * Math.cos(b), (RD - 1.3) * Math.sin(b), 0], i * 3); }
    const v = i >= 60 ? .9 : big ? .7 : .35; tkC.set([v, v * .8, v * .5], i * 3); }
  tk.frustumCulled = false; DG.add(tk);
  const hub = glow(DG, '#ffd28a', 1.6, 0), cHead = glow(DG, '#ffc65a', 3.2, 0), cCore = glow(DG, '#fff4dc', 1, 0), dRing = glow(DG, '#ffcf8a', RD * 2.6, 0);
  const NTR = 240, tr = points(NTR, { size: .55 }), trA = tr.geometry.attributes.position.array, trC = tr.geometry.attributes.color.array; tr.frustumCulled = false; DG.add(tr);
  const hand = streaks(DG, 1, { minPx: 1.2, near: [1, 2] });
  const ERA = [t0, cDi, cDe, cEv, cFr], beads = ERA.map((c, k) => { const a = (110 - k * 10) * Math.PI / 180, b = glow(DG, '#ffc65a', 1.4, 0), pl = glow(DG, '#ffd9a0', 4, 0); b.position.set((RD + 2.6) * Math.cos(a), (RD + 2.6) * Math.sin(a), 0); pl.position.copy(b.position); return { c, b, pl }; });
  const tq = v3(0, 0, 0), tq2 = v3(0, 0, 0);
  const SPR = []; S.traverse(o => { if (o.isSprite) SPR.push(o); });
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
    // accelerating swirl of the whole field (phase per object = om * SW)
    const SW = swAt(t), SW1 = swAt(t - .4);
    clouds.forEach(c => { const k = 1 + .35 * en; rot(c.pos, omOf(c.pos) * SW, c.m.position); c.m.scale.set(c.s * k, c.s * k * .7, 1); c.m.material.opacity = .2 * c.ok * (1 - en) * (.9 + .1 * Math.sin(t * .15 + c.s)); c.m.material.rotation = c.rs * t + c.s; });
    // young stars: ignite (only births before "entropy"), then shine; fade with the dim era
    yS.forEach(y => { const on = y.tb < cEn ? sm(y.tb, y.tb + 2, t) : 0, f = on * (1 - di); rot(y.q, omOf(y.q) * SW, y.h.position); y.c.position.copy(y.h.position); y.h.material.opacity = .35 * f; y.c.material.opacity = .9 * f; });
    // sun-like stars: shine, then swell orange and shrink to a faint white dwarf (one after another, ever faster); dissolve at decay
    for (let i = 0; i < NSu; i++) { const b = suB[i], a = t - b.tb, tw = .9 + .1 * Math.sin(t * .8 + b.ph); let r, g, bl;
      if (a < 0) { r = b.col[0]; g = b.col[1]; bl = b.col[2]; r *= b.br * tw; g *= b.br * tw; bl *= b.br * tw; }
      else { const sw = sm(0, 1.5, a) * (1 - sm(1.5, 4, a)), wd = sm(2, 4.5, a), k = b.br * (1 - wd) + .22 * wd;
        r = (b.col[0] + .1 * sw) * k * (1 + .8 * sw); g = (b.col[1] - .3 * sw) * k * (1 + .8 * sw); bl = (b.col[2] - .5 * sw) * k * (1 + .8 * sw);
        if (wd > 0) { r = r * (1 - wd) + .7 * k * wd; g = g * (1 - wd) + .8 * k * wd; bl = bl * (1 - wd) + 1 * k * wd; } }
      const dd = 1 - sm(0, 3, t - (cDe + (i % 9)));
      suC[i * 3] = r * dd; suC[i * 3 + 1] = g * dd; suC[i * 3 + 2] = bl * dd;
      rot(b.q, b.om * SW, tq); suA[i * 3] = tq.x; suA[i * 3 + 1] = tq.y; suA[i * 3 + 2] = tq.z; }
    su.geometry.attributes.color.needsUpdate = true; su.geometry.attributes.position.needsUpdate = true;
    // the brightest suns: an orange flare and a small planetary-nebula ring as they go
    ringBig.forEach(o => { const b = suB[o.i], a = t - b.tb, dd = 1 - sm(0, 3, t - (cDe + (o.i % 9)));
      if (a < 0 || a > 8) { o.g.material.opacity = 0; o.n.material.opacity = 0; return; }
      rot(b.q, b.om * SW, o.g.position); o.n.position.copy(o.g.position);
      const sw = sm(0, 1.5, a) * (1 - sm(1.5, 4, a)), x = Math.min(1, Math.max(0, (a - 1.4) / 5));
      o.g.material.opacity = .5 * sw * b.br * dd; o.g.scale.setScalar(2 + 4 * sw);
      o.n.material.opacity = a > 1.4 ? .32 * sm(1.4, 1.9, a) * Math.pow(1 - x, 1.4) * dd : 0; o.n.scale.setScalar(.5 + 7 * (1 - Math.pow(1 - x, 2))); });
    // red dwarfs: remain through the dim era, slowly fading; dissolve at decay
    const rf = 1 - .6 * sm(cDi, cDi + 30, t);
    for (let i = 0; i < NRd; i++) { const b = rdB[i], k = b.br * rf * (1 - sm(b.td, b.td + 3, t)); rdC[i * 3] = k; rdC[i * 3 + 1] = k * .42; rdC[i * 3 + 2] = k * .3;
      if (k > 0) { rot(b.q, b.om * SW, tq); rdA[i * 3] = tq.x; rdA[i * 3 + 1] = tq.y; rdA[i * 3 + 2] = tq.z; } }
    rd.geometry.attributes.color.needsUpdate = true; rd.geometry.attributes.position.needsUpdate = true;
    // blue giants: collapse (bright swell + shock ring), then a neutron star glint or a black hole
    bgS.forEach((b, i) => { const a = t - b.tb, sw = sm(-.5, .8, a) * (1 - sm(.8, 2.6, a)), alive = a < .8 ? 1 : 0, tw = .9 + .1 * Math.sin(t * .7 + b.ph);
      rot(b.q, b.om * SW, b.h.position); b.c.position.copy(b.h.position);
      b.h.material.opacity = .45 * tw * alive + .5 * sw; b.h.scale.setScalar(3.2 + 5 * sw); b.c.material.opacity = (.95 * alive + .8 * sw);
      const x = Math.min(1, Math.max(0, (a - .6) / 4.5)), gs = gShock[i]; gs.position.copy(b.h.position);
      gs.material.opacity = a > .5 && x < 1 ? .35 * sm(.5, .9, a) * Math.pow(1 - x, 1.5) : 0; gs.scale.setScalar(1 + 16 * (1 - Math.pow(1 - x, 2)));
      if (i >= 6) { const n = nsG[i - 6], on = sm(1, 2.5, a) * (1 - sm(cDe + (i % 5), cDe + (i % 5) + 3, t)); n.position.copy(b.h.position); n.material.opacity = 1.0 * on * (.75 + .25 * Math.sin(t * 2.1 + b.ph)); n.scale.setScalar(2.4 + .4 * Math.sin(t * 2.1 + b.ph)); } });
    // black holes: appear where the first giants collapsed; at "evaporate" glow hotter, shrink to nothing, end in a Hawking flash
    bhs.forEach((b, i) => { const born = sm(bgS[i].tb + .6, bgS[i].tb + 2.2, t), e = Math.min(1, Math.max(0, (t - b.te) / b.ed)), tend = b.te + b.ed;
      const r = b.r0 * Math.pow(1 - e, .5) * (.4 + .6 * born), gone = e >= 1;
      rot(b.q, b.om * SW, tq); b.sph.position.copy(tq); b.ring.position.copy(tq); b.hw.position.copy(tq);
      b.sph.visible = born > 0 && !gone; b.sph.scale.setScalar(Math.max(1e-3, r));
      b.ring.scale.setScalar(Math.max(1e-3, r * 2 * 1.9)); b.ring.material.opacity = born * (gone ? 0 : .9);
      const hk = e > 0 ? sm(0, .5, e) * (1 - sm(.92, 1, e)) * (.3 + .7 * e) : 0; b.hw.scale.setScalar(.6 + 3.5 * r + 4 * hk); b.hw.material.opacity = 1.1 * hk + (gone ? .45 * Math.exp(-(t - tend) * .8) : 0);
      b.hw.material.color.setRGB(1, .91 + .07 * e, .81 + .19 * e);
      const fx = bhFx[i], fl = t < b.te ? 0 : !gone ? sm(.955, 1, e) : Math.exp(-(t - tend) / 1.2), x = Math.min(1, Math.max(0, (t - tend) / 3));
      fx.f.position.copy(tq); fx.n.position.copy(tq); fx.f.material.opacity = .9 * fl; fx.f.scale.setScalar(3 + 11 * fl);
      fx.n.material.opacity = gone && x < 1 ? .28 * sm(0, .2, t - tend) * Math.pow(1 - x, 1.5) : 0; fx.n.scale.setScalar(1 + 22 * (1 - Math.pow(1 - x, 2))); });
    // debris after decay (each burst starts where its star is now)
    for (let i = 0; i < ND; i++) { const b = dbB[i], a = t - b.t0; let v = 0;
      if (a > 0) { const s = b.sp * (1 - Math.exp(-a * .25)) * 3; rot(b.src.q, b.src.om * SW, tq); dbA[i * 3] = tq.x + b.d[0] * s; dbA[i * 3 + 1] = tq.y + b.d[1] * s; dbA[i * 3 + 2] = tq.z + b.d[2] * s;
        v = .55 * b.w * sm(0, 1.5, a) * Math.exp(-a / 10) * (1 - fr); }
      else dbA[i * 3 + 1] = -9999;
      dbC[i * 3] = v; dbC[i * 3 + 1] = v * .85; dbC[i * 3 + 2] = v * .9; }
    db.geometry.attributes.position.needsUpdate = true; db.geometry.attributes.color.needsUpdate = true;
    // Hawking photons (a faster spray at each final flash)
    for (let i = 0; i < NP; i++) { const b = phB[i], a = t - b.te; let v = 0;
      if (a > 0 && a < 14) { const s = b.sp * a; rot(b.b.q, b.b.om * swAt(b.te), tq); phA[i * 3] = tq.x + b.d[0] * s; phA[i * 3 + 1] = tq.y + b.d[1] * s; phA[i * 3 + 2] = tq.z + b.d[2] * s; v = (b.fin ? 1.5 : 1.1) * Math.exp(-a / (b.fin ? 2.5 : 4)) * sm(0, .3, a); }
      else phA[i * 3 + 1] = -9999;
      phC[i * 3] = v; phC[i * 3 + 1] = v * .92; phC[i * 3 + 2] = v * .8; }
    ph.geometry.attributes.position.needsUpdate = true; ph.geometry.attributes.color.needsUpdate = true;
    // soup: appears with decay, very faint and even, slowest drift at the freeze
    const sv = .32 * de * (1 - .4 * fr) + .05 * ev * (1 - fr);
    for (let i = 0; i < NQ; i++) { const b = spB[i]; spA[i * 3] = b[0] + .25 * Math.sin(t * .02 + b[3]); spA[i * 3 + 1] = b[1] + .2 * Math.cos(t * .017 + b[3]); spA[i * 3 + 2] = b[2];
      const v = sv * (.5 + .5 * b[4]); spC[i * 3] = v * .8; spC[i * 3 + 1] = v * .85; spC[i * 3 + 2] = v; }
    sp.geometry.attributes.position.needsUpdate = true; sp.geometry.attributes.color.needsUpdate = true;
    // motion streaks: head now, tail .4 s back on the swirl clock, so the length follows the speed
    SST.forEach((i, k) => { const b = suB[i]; rot(b.q, b.om * SW, tq); rot(b.q, b.om * SW1, tq2); const L = tq.distanceTo(tq2), f = sm(.15, 1.2, L) * .55;
      if (f <= 0 || suC[i * 3] <= .01) { sStr.hide(k); return; } sStr.set(k, tq.x, tq.y, tq.z, tq2.x, tq2.y, tq2.z, .12, suC[i * 3] * f, suC[i * 3 + 1] * f, suC[i * 3 + 2] * f); });
    bgS.forEach((b, j) => { const k = SST.length + j, al = t - b.tb < .8 ? 1 : 0; rot(b.q, b.om * SW, tq); rot(b.q, b.om * SW1, tq2); const f = sm(.15, 1.2, tq.distanceTo(tq2)) * .6 * al;
      if (f <= 0) { sStr.hide(k); return; } sStr.set(k, tq.x, tq.y, tq.z, tq2.x, tq2.y, tq2.z, .2, .7 * f, .8 * f, 1 * f); });
    sStr.commit();
    // near-field motes
    for (let i = 0; i < NMo; i++) { const b = MOB[i]; moA[i * 3] = b[0] + 1.5 * Math.sin(t * .05 + b[3]); moA[i * 3 + 1] = b[1] + 1 * Math.cos(t * .04 + b[3]); moA[i * 3 + 2] = b[2] + 1.2 * Math.sin(t * .03 + 2 * b[3]); }
    mo.geometry.attributes.position.needsUpdate = true; mo.material.opacity = .5 * (1 - .6 * de) * (1 - .8 * fr);
    // the clock of light: accelerating comet hand, trail grows with speed; era beads; fades away after the freeze
    const dv = sm(t0, t0 + 2.5, t) * (1 - sm(cFr + 10, cFr + 20, t)), F = Fcap(t, 1.5), rate = Rcap(t, 1.5), th = Math.PI / 2 - 6.28318 * (F - Math.floor(F));
    DG.visible = dv > 0;
    if (dv > 0) {
      const hx = RD * Math.cos(th), hy = RD * Math.sin(th);
      cHead.position.set(hx, hy, .05); cCore.position.set(hx, hy, .06); cHead.material.opacity = .7 * dv; cCore.material.opacity = .9 * dv;
      tk.material.opacity = .8 * dv; hub.material.opacity = .45 * dv; dRing.material.opacity = .035 * dv * (.4 + .6 * Math.min(1, rate));
      const span = Math.min(6.1, .3 + 6.28318 * rate * .55), dens = Math.min(1, 1.6 / span);
      for (let j = 0; j < NTR; j++) { const q = j / NTR, a = th + span * q, v = Math.pow(1 - q, 1.5) * dv * (.35 + .65 * dens); trA[j * 3] = RD * Math.cos(a); trA[j * 3 + 1] = RD * Math.sin(a); trA[j * 3 + 2] = .02; trC[j * 3] = v; trC[j * 3 + 1] = v * .78; trC[j * 3 + 2] = v * .42; }
      tr.geometry.attributes.position.needsUpdate = true; tr.geometry.attributes.color.needsUpdate = true;
      hand.set(0, hx * .82, hy * .82, .01, 0, 0, .01, .1, .3 * dv, .25 * dv, .16 * dv); hand.commit();
      beads.forEach(o => { const lit = o.c < 1e8 ? sm(o.c, o.c + .4, t) : 0; o.b.material.opacity = (.18 + .7 * lit) * dv;
        o.pl.material.opacity = o.c < 1e8 ? .45 * sm(o.c, o.c + .3, t) * Math.exp(-Math.max(0, t - o.c - .3) / 1.5) * dv : 0; });
    }
    // skip invisible sprites (software rendering pays for every quad, even at opacity 0)
    SPR.forEach(o => { o.visible = o.material.opacity > .002; });
  } };
};
