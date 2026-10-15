// requires: expanse
// supernova — a Type Ia supernova as a standard candle, and dark energy (cosmic-prison-cine S19-S20; written 2026-10-15).
// A distant realistic spiral galaxy (tilted disc: two winding arms with spurs, dust lanes on their inner edges, pink star-forming
// knots, blue clusters, a warm bulge; disc thickness from ~7000 3D star points, a 3D bulge cloud and offset glow layers), turning
// very slowly among small background galaxies (MIYA.cosmicGal from expanse.js). One point in an outer arm flares into a supernova:
// bright point, soft halo, gentle bloom and faint diffraction spikes, rising over ~1.6 s and fading over many seconds (no strobe).
// params (cues; all optional — without them the galaxy simply turns):
//   flare  the supernova flares
//   dim    S19 a second flare at the same spot is fainter than expected: a pale ghost ring shows the size/brightness it "should"
//          have had, and the galaxy slips a little farther away (it is farther than a slowing universe would allow)
//   dark   S20 a faint violet dark-energy haze fills the space between the galaxies and pushes everything apart, ever faster
//   side   subject offset (default .12)
(window.MIYA = window.MIYA || { scenes: {} }).scenes.supernova = function (ctx, p) {
  const { T, sm, rng, cue, points, glow, ctex } = ctx, M = window.MIYA, K = M.kit;
  const S = new T.Scene(); S.background = new T.Color('#05071a');
  const cT = c => c == null ? 1e9 : cue(c), on = (c0, d) => sm(c0, c0 + d, ctx.t);
  const cFl = cT(p.flare), cDm = cT(p.dim), cDk = cT(p.dark);
  ctx.stars(S, 2600, 900, { size: 1.3, opacity: .55, seed: 61 });
  const RN = rng(9); for (let k = 0; k < 3; k++) { const s = glow(S, k % 2 ? '#30267a' : '#1f2b66', 700 + RN() * 300, .15); s.position.set((RN() - .3) * 900, (RN() - .5) * 400, -800); }

  // ---------------- galaxy texture (1024, canvas rows = -y of the disc plane) ----------------
  const hs = (x, y, s) => { let h = (x * 374761393 + y * 668265263 + s * 1442695041) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };
  const vn = (x, y, s) => { const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi, u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
    const a = hs(xi, yi, s), b = hs(xi + 1, yi, s), cc = hs(xi, yi + 1, s), d = hs(xi + 1, yi + 1, s); return a + (b - a) * u + (cc - a) * v + (a - b - cc + d) * u * v; };
  const ss = (a, b, x) => { x = Math.min(1, Math.max(0, (x - a) / (b - a))); return x * x * (3 - 2 * x); };
  const PITCH = .3, OFF = .8, armPh = (r, th) => 2 * (th - Math.log(Math.max(.02, r)) / Math.tan(PITCH)) + OFF;
  const armAt = (x, y) => { const r = Math.hypot(x, y), th = Math.atan2(y, x), n1 = vn(x * 6 + 3, y * 6, 1) * .6 + vn(x * 12, y * 12 + 5, 2) * .4;
    const ph = armPh(r, th + (n1 - .5) * .35); return [r, ph, n1, Math.pow(.5 + .5 * Math.cos(ph), 3.5) + .25 * Math.pow(.5 + .5 * Math.cos(2 * ph + n1 * 3), 6)]; };
  const GSZ = 1024, gc = document.createElement('canvas'); gc.width = gc.height = GSZ;
  { const g = gc.getContext('2d'), im = g.createImageData(GSZ, GSZ), D = im.data, enc = v => Math.max(0, Math.min(255, Math.pow(Math.min(1, v), 1 / 2.2) * 255));
    for (let py = 0; py < GSZ; py++) for (let px = 0; px < GSZ; px++) {
      const x = (px + .5) / GSZ * 2 - 1, y = (py + .5) / GSZ * 2 - 1, [r, ph, n1, arm] = armAt(x, y);
      if (r > 1) { const i = (py * GSZ + px) * 4; D[i] = D[i + 1] = D[i + 2] = 0; D[i + 3] = 255; continue; }
      const n2 = vn(x * 28, y * 28, 3), n3 = vn(x * 64, y * 64, 4);
      const ar = ss(.07, .2, r), disc = Math.exp(-r / .23);
      const lane = Math.pow(.5 + .5 * Math.cos(ph - .6), 16) * ss(.1, .3, r) * (.6 + .6 * n2);
      const lane2 = Math.max(0, n2 - .55) * 1.6 * ss(.15, .4, r) * (1 - Math.min(1, arm));
      const L = disc * (.16 + 1.7 * arm * ar * (.5 + .8 * n2)), dust = Math.max(.08, 1 - .85 * lane - .5 * lane2);
      const hii = Math.max(0, n3 - .72) * 7 * arm * ar * disc, blu = Math.max(0, n2 - .6) * 3 * arm * ar * disc;
      const bul = Math.exp(-((r / .075) ** 2)) * .9 + Math.exp(-r / .05) * .3 + Math.exp(-((r / .16) ** 2)) * .3, w = Math.min(1, r / .5), edge = 1 - ss(.75, .99, r);
      const R = ((L * (1.05 - .3 * w)) + blu * .55 + hii) * dust + bul, G = ((L * (.88 - .1 * w)) + blu * .7 + hii * .38) * dust + bul * .8, B = ((L * (.68 + .26 * w)) + blu + hii * .62) * dust + bul * .55;
      const i = (py * GSZ + px) * 4; D[i] = enc(R * edge * .8); D[i + 1] = enc(G * edge * .8); D[i + 2] = enc(B * edge * .8); D[i + 3] = 255; }
    g.putImageData(im, 0, 0); }
  const gtx = new T.CanvasTexture(gc); gtx.colorSpace = T.SRGBColorSpace; gtx.anisotropy = 8;

  const GR = 11, TILT = new T.Group(), DISC = new T.Group(); TILT.add(DISC); S.add(TILT);
  TILT.rotation.set(-1.02, .12, .4);
  const planeM = (op) => new T.MeshBasicMaterial({ map: gtx, transparent: true, opacity: op, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide });
  DISC.add(new T.Mesh(new T.PlaneGeometry(GR * 2, GR * 2), planeM(1)));
  [-.16, .16].forEach(z => { const m = new T.Mesh(new T.PlaneGeometry(GR * 2, GR * 2), planeM(.22)); m.position.z = z; m.scale.setScalar(.97); DISC.add(m); });
  // 3D star points following the arms (disc thickness), and a 3D bulge
  const NS = 7000, st = points(NS, { size: .075, opacity: 1 }), sA = st.geometry.attributes.position.array, sC = st.geometry.attributes.color.array;
  { const r = rng(71); let i = 0, guard = 0; while (i < NS && guard++ < 200000) { const rr = -Math.log(1 - r() * .985) * .24, th = r() * 6.283; if (rr > .98) continue;
      const x = rr * Math.cos(th), y = rr * Math.sin(th), a = armAt(x, y)[3], acc = .12 + .9 * a * ss(.07, .2, rr); if (r() > acc) continue;
      const zt = (r() + r() + r() - 1.5) * .22 * (1 - .4 * rr); sA.set([x * GR, -y * GR, zt], i * 3);
      const w = Math.min(1, rr / .45), v = .35 + .5 * r(); sC.set([v * (1 - .4 * w), v * (.86 - .1 * w), v * (.7 + .4 * w)], i * 3); i++; } }
  DISC.add(st);
  const NB = 2200, bp = points(NB, { size: .08, opacity: 1 }), bA = bp.geometry.attributes.position.array, bC = bp.geometry.attributes.color.array;
  { const r = rng(73); for (let i = 0; i < NB; i++) { const gs = () => (r() + r() + r() + r() - 2) * .9; bA.set([gs() * 1.25, gs() * 1.25, gs() * .85], i * 3); const v = .3 + .35 * r(); bC.set([v, v * .82, v * .58], i * 3); } }
  DISC.add(bp);
  const bg1 = glow(DISC, '#ffcf8a', 5.5, .26), bg2 = glow(DISC, '#ffe6c0', 2.0, .3), halo = glow(DISC, '#8a7cff', 34, .05);

  // ---------------- the supernova (in an outer arm, r ~ .56) ----------------
  const snR = .56, snTh = Math.log(snR) / Math.tan(PITCH) - OFF / 2 + Math.PI + .06;   // arm crest (cos(ph)=1), in canvas coordinates
  const SN = new T.Group(); SN.position.set(snR * Math.cos(snTh) * GR, -snR * Math.sin(snTh) * GR, .05); DISC.add(SN);
  const spikeT = ctex(256, (g, s) => { g.translate(s / 2, s / 2); for (let k = 0; k < 4; k++) { g.rotate(Math.PI / 2); const gr = g.createLinearGradient(0, 0, s / 2, 0); gr.addColorStop(0, 'rgba(255,255,255,.9)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.beginPath(); g.moveTo(0, -3); g.lineTo(s / 2, 0); g.lineTo(0, 3); g.fill(); } });
  const ringT = ctex(256, (g, s) => { const gr = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.72, 'rgba(255,255,255,.06)'); gr.addColorStop(.84, 'rgba(255,255,255,.9)'); gr.addColorStop(.9, 'rgba(255,255,255,.12)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); });
  const spr = (map, col) => { const m = new T.Sprite(new T.SpriteMaterial({ map, color: col, transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false })); SN.add(m); return m; };
  const snBloom = spr(ctx.dotTex(), '#ffb070'), snHalo = spr(ctx.dotTex(), '#ffe2b0'), snSpk = spr(spikeT, '#fff2dc'), snCore = spr(ctx.dotTex(), '#ffffff'), ghost = spr(ringT, '#cbbcff');
  const lc = (tau, pk) => tau <= 0 ? 0 : pk * sm(0, 1.6, tau) * (tau < 1.6 ? 1 : .85 * Math.exp(-(tau - 1.6) / 5.5) + .15 * Math.exp(-(tau - 1.6) / 30));

  // ---------------- background galaxies + dark-energy haze ----------------
  const NG = 150, GF = M.cosmicGal(ctx, NG), R1 = rng(81), gpos = [], gcol = [];
  for (let i = 0; i < NG; i++) { let x, y, z; do { x = (R1() - .45) * 260; y = (R1() - .5) * 130; z = -30 - R1() * 380; } while (Math.abs(x) < 26 && Math.abs(y) < 16 && z > -90);
    gpos.push([x, y, z]); const kind = GF.random(i, R1, 1.6, 4.2), cu = R1(), br = .9 + .9 * R1(); const c = kind === 1 ? [1, .8, .55] : cu < .55 ? [1, .85, .62] : [.8, .75, 1]; gcol.push([c[0] * br, c[1] * br, c[2] * br]); }
  S.add(GF.mesh);
  const cloudT = (() => { const c = K.noise(256, { seed: 4, octaves: 3 }), g = c.getContext('2d'); g.globalCompositeOperation = 'destination-in'; const gr = g.createRadialGradient(128, 128, 0, 128, 128, 128); gr.addColorStop(0, 'rgba(0,0,0,1)'); gr.addColorStop(.55, 'rgba(0,0,0,.5)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, 256, 256);
    const t2 = new T.CanvasTexture(c); t2.colorSpace = T.SRGBColorSpace; return t2; })();
  const NH = 16, haze = [], R2 = rng(91);
  for (let k = 0; k < NH; k++) { const m = new T.Sprite(new T.SpriteMaterial({ map: cloudT, color: k % 3 ? '#6a4fd8' : '#4a3bb0', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, rotation: R2() * 6.28 }));
    const s = 45 + R2() * 55; m.scale.set(s, s * (.6 + .4 * R2()), 1); S.add(m); haze.push([m, (R2() - .4) * 150, (R2() - .5) * 70, -20 - R2() * 160, (R2() - .5) * .02, .5 + .5 * R2()]); }
  const ND = 900, dust = points(ND, { size: .22, opacity: .8 }), dA = dust.geometry.attributes.position.array, dC = dust.geometry.attributes.color.array, d0 = [];
  { const r = rng(95); for (let i = 0; i < ND; i++) { d0.push([(r() - .45) * 120, (r() - .5) * 60, 25 - r() * 160]); const v = .08 + .14 * r(); dC.set(r() < .5 ? [v, v * .8, v * .55] : [v * .65, v * .6, v], i * 3); } }
  S.add(dust);

  const cam = new T.PerspectiveCamera(38, ctx.W / ctx.H, .1, 3000); ctx.side(cam, p.side == null ? .12 : p.side);
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const dm = on(cDm, 4), dkq = sm(cDk, cDk + 30, t), dk = on(cDk, 5), e = .6 * dkq * dkq + .04 * dk;
    // galaxy: slow turn; slips back a little at "dim", recedes with the expansion at "dark"
    DISC.rotation.z = -t * .006;
    TILT.position.set(3 * dkq, 0, -7 * dm - 34 * dkq * dkq);
    cam.position.set(2.5 * Math.sin(u * .015), 4.5 + .6 * Math.sin(u * .011), 40 + 10 * dk); cam.lookAt(0, -.5, TILT.position.z * .3);
    // supernova light (first flare = the expected candle, second at "dim" = fainter than expected)
    const L = lc(t - cFl, 1) + lc(t - cDm, .45), sq = Math.sqrt(L);
    snCore.scale.setScalar(.35 + 1.1 * sq); snCore.material.opacity = Math.min(1, L * 1.3);
    snHalo.scale.setScalar(1.6 + 4.4 * sq); snHalo.material.opacity = .4 * L;
    snBloom.scale.setScalar(15); snBloom.material.opacity = .09 * L;
    snSpk.scale.setScalar(7.5 * sq); snSpk.material.opacity = .3 * L;
    ghost.scale.setScalar(6.6); ghost.material.opacity = dm * (1 - .7 * dk) * (.38 + .08 * Math.sin(t * 1.1));
    // background galaxies pushed apart (away from the main galaxy, ever faster)
    for (let i = 0; i < NG; i++) { const q = gpos[i], c = gcol[i], x = q[0] * (1 + e), y = q[1] * (1 + e), z = q[2] - 60 * e + (q[2] + 40) * e * .5;
      const f = Math.exp(-Math.max(0, -z - 150) / 500); GF.set(i, x, y, z, c[0] * f, c[1] * f, c[2] * f, 1); }
    GF.flush();
    haze.forEach(([m, x, y, z, rs, ok]) => { m.position.set(x * (1 + e), y * (1 + e), z - 30 * e); m.material.rotation = rs * t + x; m.material.opacity = .2 * dk * ok * (.85 + .15 * Math.sin(t * .2 + x)); });
    for (let i = 0; i < ND; i++) { const q = d0[i]; dA[i * 3] = q[0] * (1 + e); dA[i * 3 + 1] = q[1] * (1 + e); dA[i * 3 + 2] = q[2] - 20 * e; }
    dust.geometry.attributes.position.needsUpdate = true;
  } };
};
