// localgroup — the Local Group in dark intergalactic space: the Milky Way (barred two-arm spiral, ~32k soft star points, bulge,
// dust lanes, pink star-forming knots, two Magellanic-like dwarfs) and the larger, more inclined Andromeda (~42k points, tight
// arms, dust ring, two dwarf companions), plus the small Triangulum spiral. Each disk also carries a smooth light layer (canvas
// image: unresolved starlight with dark dust lanes) under the points. Far background galaxies (soft elliptical glows + faint points)
// fill the sky. Written for cosmic-prison-cine S25-S26, S28-S29 (2026-10-15).
// All star motion happens in the vertex shader from uniforms set from t (seek-safe): rigid disk spin, close approach with tidal
// tails and a bridge, then each star flows to its place in one big elliptical (merger remnant).
// params (cues, all optional):
//   approach  S26: Andromeda and the Milky Way fall toward each other, swing past (tidal tails), a merging glow grows between them.
//             (The 2025 study puts the odds near a coin flip: shown as a close approach that ends in a merge only on `merge`.)
//   merge     they combine into one large elliptical glow ("Milkdromeda"); Triangulum joins it.
//   alone     S28: the camera pulls far back; most background galaxies redden, recede and fade out; the merged galaxy sits alone.
//   erase     S29: the last faint background galaxies dim to nothing; the sky around is empty.
//   merged    any value: start with the merger already done (for a later shot, e.g. S28-S29 after another scene); passing the
//             S26 approach/merge cues again works too (their times are in the past, so the merge is complete)
//   side      subject offset (default .12)
(window.MIYA = window.MIYA || { scenes: {} }).scenes.localgroup = function (ctx, p) {
  const { T, sm, rng, cue, glow } = ctx;
  const S = new T.Scene(); S.background = new T.Color('#03040e');
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), ctx.t);
  const v3 = (x, y, z) => new T.Vector3(x, y, z);

  // ---------------- galaxy specs (local frame: disk in x-z, normal +y) ----------------
  const D2R = Math.PI / 180;
  const SPEC = [
    { name: 'mw', rd: 11, R: 42, arms: 2, pitch: 17 * D2R, sharp: 3, spur: .15, laneOff: -.55, bulge: 4.6, bar: 1.9, nD: 26000, nB: 6000, br: 1, warm: .0 },
    { name: 'm31', rd: 14, R: 58, arms: 2, pitch: 11 * D2R, sharp: 3, spur: .1, laneOff: -.45, bulge: 7, bar: 1, nD: 34000, nB: 8000, br: 1, warm: .15 },
    { name: 'm33', rd: 6, R: 21, arms: 2, pitch: 21 * D2R, sharp: 2, spur: .5, laneOff: -.6, bulge: 1.4, bar: 1, nD: 6500, nB: 500, br: .9, warm: -.1 } ];
  const armAt = (sp, r, th) => { const ps = th - Math.log(Math.max(r, .6) / 3) / Math.tan(sp.pitch);
    const s = Math.cos(sp.arms * ps), a = Math.pow((1 + s) / 2, sp.sharp) + sp.spur * Math.pow((1 + Math.cos(sp.arms * 2 * ps + .7)) / 2, 4) * .6;
    const lane = Math.pow((1 + Math.cos(sp.arms * ps + sp.laneOff)) / 2, 12);
    return [Math.min(1.2, a), lane]; };

  // ---------------- star buffers ----------------
  const NMAX = 95000, P = new Float32Array(NMAX * 3), G = new Float32Array(NMAX), C = new Float32Array(NMAX * 3), Z = new Float32Array(NMAX), TL = new Float32Array(NMAX * 2), EL = new Float32Array(NMAX * 3);
  let n = 0; const R = rng(1234);
  const gauss = () => { let u = 0; for (let k = 0; k < 4; k++) u += R(); return (u - 2) * 1.2247; };
  // elliptical remnant position (triaxial, steep core, extended envelope)
  function ell(i, scale) { const u = R(), rr = Math.min(130, scale * 9 * Math.pow(-Math.log(1 - u * .995), 1.7)), z = R() * 2 - 1, a = R() * 6.283, q = Math.sqrt(1 - z * z);
    EL[i * 3] = rr * q * Math.cos(a); EL[i * 3 + 1] = rr * z * .7; EL[i * 3 + 2] = rr * q * Math.sin(a) * .85; }
  function add(g, x, y, z, col, size, tw, ts, es) { if (n >= NMAX) return; const i = n++;
    P[i * 3] = x; P[i * 3 + 1] = y; P[i * 3 + 2] = z; G[i] = g; C.set(col, i * 3); Z[i] = size; TL[i * 2] = tw; TL[i * 2 + 1] = ts; ell(i, es); }
  SPEC.forEach((sp, g) => {
    // disk: exponential radius, arm modulation by rejection, dust lanes as gaps (the smooth layer carries the dark lane itself)
    let made = 0, guard = 0;
    while (made < sp.nD && guard++ < sp.nD * 30) {
      const r = -sp.rd * Math.log(1 - R() * (1 - Math.exp(-sp.R / sp.rd))), th = R() * 6.283;
      if (r < sp.bulge * .6) continue;
      const [a, lane] = armAt(sp, r, th), acc = (.18 + .82 * a) * (1 - .75 * lane * sm(sp.bulge, sp.bulge * 2.5, r));
      if (R() > acc) continue;
      made++;
      const young = a > .55 && R() < .55, h = (young ? .25 : .55) * (1 + r / sp.R) * gauss() * (sp.R / 42);
      const b = .5 + .7 * Math.pow(R(), 3);
      const col = young ? [.62 * b, .74 * b, 1.0 * b] : [1.0 * b, (.86 - .05 * sp.warm) * b, (.72 - .1 * sp.warm) * b];
      const tw = r > sp.R * .45 ? sm(.45, 1, r / sp.R) * (R() < .6 ? 1 : -.7) : 0;
      add(g, r * Math.cos(th), h, r * Math.sin(th), col, (young ? .34 : .26) * (sp.R / 42 + .3) * .8, tw, Math.min(1.3, r / sp.R + R() * .35), g === 2 ? .5 : 1);
      // star-forming knots (pink HII + blue clusters) on the arm crests
      if (young && a > .85 && R() < .05) { const kk = 6 + (R() * 10 | 0), pink = R() < .6;
        for (let k = 0; k < kk; k++) add(g, r * Math.cos(th) + gauss() * .5, h + gauss() * .12, r * Math.sin(th) + gauss() * .5,
          pink ? [1.0, .38, .55] : [.6, .75, 1.1], .3, tw, Math.min(1.3, r / sp.R), 1); }
    }
    // bulge (+ bar for the Milky Way)
    for (let k = 0; k < sp.nB; k++) { const rr = sp.bulge * .55 * Math.pow(-Math.log(1 - R() * .99), 1.2), z = R() * 2 - 1, a = R() * 6.283, q = Math.sqrt(1 - z * z), b = .55 + .6 * R();
      add(g, rr * q * Math.cos(a) * sp.bar, rr * z * .55, rr * q * Math.sin(a), [.6 * b, .46 * b, .3 * b], .3 * (sp.R / 42 + .3), 0, 0, g === 2 ? .5 : .6); }
  });
  // dwarf companions (in the host's frame, outside the disk)
  const dwarf = (g, cx, cy, cz, sx, sy, sz, nn, col, irr) => { for (let k = 0; k < nn; k++) { let x = gauss() * sx, y = gauss() * sy, z = gauss() * sz;
      if (irr) { x += Math.sin(z * .5) * sx * .6; } const b = .5 + .6 * R(); add(g, cx + x, cy + y, cz + z, [col[0] * b, col[1] * b, col[2] * b], .26, 0, 0, .9); } };
  dwarf(0, 48, 10, 30, 4.2, 2.2, 2.8, 2200, [.8, .85, 1.0], true);     // LMC-like (irregular, bluish)
  dwarf(0, 56, 6, 40, 2.2, 1.4, 1.6, 900, [.85, .88, 1.0], true);     // SMC-like
  dwarf(1, 14, 5, -16, 1.2, 1.0, 1.0, 700, [1.0, .8, .58], false);     // M32-like compact elliptical
  dwarf(1, -48, 16, 40, 4.2, 2.2, 2.0, 1300, [1.0, .84, .66], false);  // M110-like elongated
  const geo = new T.BufferGeometry();
  geo.setAttribute('position', new T.BufferAttribute(P.subarray(0, n * 3), 3)); geo.setAttribute('aGal', new T.BufferAttribute(G.subarray(0, n), 1));
  geo.setAttribute('aCol', new T.BufferAttribute(C.subarray(0, n * 3), 3)); geo.setAttribute('aSize', new T.BufferAttribute(Z.subarray(0, n), 1));
  geo.setAttribute('aTail', new T.BufferAttribute(TL.subarray(0, n * 2), 2)); geo.setAttribute('aEll', new T.BufferAttribute(EL.subarray(0, n * 3), 3));
  const U = { uM: { value: [new T.Matrix4(), new T.Matrix4(), new T.Matrix4()] }, uTA: { value: [v3(0, 0, 0), v3(0, 0, 0), v3(0, 0, 0)] }, uTT: { value: [v3(0, 0, 0), v3(0, 0, 0), v3(0, 0, 0)] },
    uBr: { value: [1, 1, 1] }, uCen: { value: v3(0, 0, 0) }, uMerge: { value: 0 }, uPx: { value: 1000 }, uRot: { value: 0 }, uGm: { value: [0, 0, 0] } };
  const mat = new T.ShaderMaterial({ uniforms: U, transparent: true, depthWrite: false, depthTest: false, blending: T.AdditiveBlending,
    vertexShader: `attribute float aGal; attribute vec3 aCol; attribute float aSize; attribute vec2 aTail; attribute vec3 aEll;
      uniform mat4 uM[3]; uniform vec3 uTA[3]; uniform vec3 uTT[3]; uniform float uBr[3]; uniform float uGm[3]; uniform vec3 uCen; uniform float uPx, uRot;
      varying vec3 vCol; varying float vA;
      void main(){ int g = int(aGal + .5); vec4 w = uM[g] * vec4(position, 1.);
        float k = aTail.x, s = aTail.y;
        if (k > 0.) w.xyz += (uTA[g] * s + uTT[g] * s * s) * k; else w.xyz += (-uTA[g] * s * .55 + uTT[g] * s * .25) * (-k);
        float c = cos(uRot), sn = sin(uRot); vec3 e = vec3(c * aEll.x - sn * aEll.z, aEll.y, sn * aEll.x + c * aEll.z);
        float h = fract(sin(dot(position.xz, vec2(12.9898, 78.233))) * 43758.5453);
        float mm = smoothstep(0., 1., clamp(uGm[g] * 1.5 - h * .5, 0., 1.));
        vec3 pp = mix(w.xyz, uCen + e, mm);
        vec4 mv = viewMatrix * vec4(pp, 1.); gl_Position = projectionMatrix * mv;
        float sz = aSize * uPx / max(1., -mv.z), ps = max(sz, 1.7);
        gl_PointSize = ps; vA = uBr[g] * min(1., sz / ps) * .34 * (1. - .4 * mm);
        vCol = mix(aCol, vec3(1., .84, .66) * (.6 + .5 * h), mm * .65); }`,
    fragmentShader: `varying vec3 vCol; varying float vA;
      void main(){ vec2 q = gl_PointCoord * 2. - 1.; float d = dot(q, q); if (d > 1.) discard;
        float a = exp(-d * 4.5) * (1. - d); gl_FragColor = vec4(vCol * vA * a, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` });
  mat.blending = T.CustomBlending; mat.blendSrc = T.OneFactor; mat.blendDst = T.OneFactor;
  const stars = new T.Points(geo, mat); stars.frustumCulled = false; stars.renderOrder = 2; S.add(stars);

  // ---------------- smooth light layer per disk (unresolved light, dust lanes darker) ----------------
  function diskTex(sp) { const N = 512, c = document.createElement('canvas'); c.width = c.height = N; const g = c.getContext('2d'), im = g.createImageData(N, N), d = im.data, Rm = sp.R * 1.15;
    for (let y = 0; y < N; y++) for (let x = 0; x < N; x++) { const X = ((x + .5) / N * 2 - 1) * Rm, Y = ((y + .5) / N * 2 - 1) * Rm, r = Math.hypot(X / sp.bar, Y) , rr = Math.hypot(X, Y), th = Math.atan2(Y, X);
      const [a, lane] = armAt(sp, rr, th), disk = Math.exp(-rr / sp.rd) * sm(sp.R * 1.12, sp.R * .7, rr);
      let L = disk * (.25 + .75 * a) * (1 - .85 * lane * sm(sp.bulge * .8, sp.bulge * 2.2, rr)), B = Math.exp(-Math.pow(r / (sp.bulge * .85), 1.3)) * 1.4;
      const yb = a * disk * .6, k = (y * N + x) * 4, cl = v => Math.min(255, Math.max(0, Math.pow(v, 1 / 2.2) * 255));
      d[k] = cl(L * .55 + B * .95 + yb * .1); d[k + 1] = cl(L * .52 + B * .72 + yb * .15); d[k + 2] = cl(L * .62 + B * .45 + yb * .4); d[k + 3] = 255; }
    g.putImageData(im, 0, 0); const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; t.anisotropy = 4; return t; }
  const softT = ctx.ctex(256, (g, sz) => { const im = g.createImageData(sz, sz); for (let y = 0; y < sz; y++) for (let x = 0; x < sz; x++) { const X = (x + .5) / sz * 2 - 1, Y = (y + .5) / sz * 2 - 1, d2 = X * X + Y * Y, k = (y * sz + x) * 4;
      im.data[k] = im.data[k + 1] = im.data[k + 2] = 255; im.data[k + 3] = Math.max(0, Math.min(255, (Math.exp(-d2 * 5) * .75 + Math.exp(-d2 * 30) * .25) * (1 - d2) * 255)); } g.putImageData(im, 0, 0); });
  const sglow = (par, col, sc, op) => { const o = glow(par, col, sc, op); o.material.map = softT; return o; };
  const GAL = SPEC.map((sp, g) => { const grp = new T.Group(); S.add(grp);
    const pl = new T.Mesh(new T.PlaneGeometry(sp.R * 2.3, sp.R * 2.3).rotateX(-Math.PI / 2), new T.MeshBasicMaterial({ map: diskTex(sp), transparent: true, opacity: .9, blending: T.AdditiveBlending, depthWrite: false, depthTest: false, side: T.DoubleSide }));
    pl.renderOrder = 1; grp.add(pl);
    const core = sglow(grp, '#ffd9a0', sp.bulge * 5, .35), halo = sglow(grp, '#9fb0ff', sp.R * 2.6, .05);
    [core, halo].forEach(o => { o.material.depthTest = false; o.renderOrder = 1; });
    return { grp, pl, core, halo }; });
  // merger glow (between them late in the approach) and the remnant's smooth light
  const mGlow = sglow(S, '#ffcf8a', 60, 0), eGlow = sglow(S, '#ffd6a0', 260, 0), eCore = sglow(S, '#fff0d8', 40, 0);
  [mGlow, eGlow, eCore].forEach(o => { o.material.depthTest = false; o.renderOrder = 3; });

  // ---------------- far background galaxies: two sets (A fades on `alone`, B on `erase`) ----------------
  const bgA = new T.Group(), bgB = new T.Group(); S.add(bgA, bgB);
  const RB = rng(77), bgList = [];
  const spirTex = ctx.ctex(64, (g, s) => { const im = g.createImageData(s, s); for (let y = 0; y < s; y++) for (let x = 0; x < s; x++) { const X = (x + .5) / s * 2 - 1, Y = (y + .5) / s * 2 - 1, r = Math.hypot(X, Y), th = Math.atan2(Y, X);
      const v = Math.exp(-r * 4) * (.4 + .6 * Math.pow((1 + Math.cos(2 * (th - Math.log(r + .05) * 2.2))) / 2, 2)) * sm(1, .6, r) + Math.exp(-r * r * 60) * .8, k = (y * s + x) * 4;
      im.data[k] = im.data[k + 1] = im.data[k + 2] = 255; im.data[k + 3] = Math.min(255, v * 300); } g.putImageData(im, 0, 0); });
  for (let i = 0; i < 520; i++) { const z = RB() * 2 - 1, a = RB() * 6.283, q = Math.sqrt(1 - z * z), d = v3(q * Math.cos(a), z, q * Math.sin(a)), dist = 3200 + RB() * 2600, keep = RB() < .14;
    const warm = RB() < .55, sp = new T.Sprite(new T.SpriteMaterial({ map: RB() < .25 ? spirTex : ctx.dotTex(), color: warm ? '#ffd9b0' : '#c4cfff', transparent: true, opacity: 1, blending: T.AdditiveBlending, depthWrite: false, depthTest: false, fog: false, rotation: RB() * 6.283 }));
    const s0 = (6 + 22 * Math.pow(RB(), 2.5)) * dist / 3200; sp.scale.set(s0, s0 * (.3 + RB() * .6), 1); sp.position.copy(d).multiplyScalar(dist);
    (keep ? bgB : bgA).add(sp); bgList.push({ sp, d, dist, base: (.25 + .5 * RB()) * (keep ? .8 : 1), keep, s0, sy: sp.scale.y / s0, warm, ph: RB() }); }
  const pts = (nn, seed, op) => { const pp = ctx.points(nn, { size: 1.8, opacity: op, atten: false }), a = pp.geometry.attributes.position.array, c = pp.geometry.attributes.color.array, r = rng(seed);
    for (let i = 0; i < nn; i++) { const z = r() * 2 - 1, an = r() * 6.283, q = Math.sqrt(1 - z * z), dd = 5000 + r() * 1500; a.set([q * Math.cos(an) * dd, z * dd, q * Math.sin(an) * dd], i * 3);
      const b = .3 + .7 * Math.pow(r(), 2), w = r(); c.set(w < .5 ? [b, b * .88, b * .72] : [b * .78, b * .84, b], i * 3); }
    pp.material.depthTest = false; return pp; };
  const fpA = pts(2600, 81, .55), fpB = pts(500, 82, .45); bgA.add(fpA); bgB.add(fpB);

  // ---------------- camera ----------------
  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, 1, 20000); ctx.side(cam, p.side == null ? .12 : p.side);
  const VF = ctx.VERT ? 1.35 : 1;
  const tmpM = new T.Matrix4(), q1 = new T.Quaternion(), q2 = new T.Quaternion(), eu = new T.Euler(), sc1 = v3(1, 1, 1);
  // galaxy placement: masses (for the barycentre) ~ MW 1 : M31 1.3
  const MW0 = v3(-80, -4, 30), M310 = v3(80, 18, -30), M330 = v3(125, 50, -140), mA = 1, mB = 1.3;
  const BC0 = MW0.clone().multiplyScalar(mA).addScaledVector(M310, mB).multiplyScalar(1 / (mA + mB)), REL0 = M310.clone().sub(MW0);
  const relAt = a => { const e = a, ang = 2.5 * e, d = REL0.length() * Math.pow(1 - .9 * e, 1.1) + 12 * Math.sin(Math.PI * e) * 0;
    const dir = REL0.clone().normalize().applyAxisAngle(v3(.18, 1, .1).normalize(), ang); return dir.multiplyScalar(Math.max(14, d)); };
  const tilts = [[.6, .3, .2], [.28, -.5, .42], [.9, .9, .4]];
  const tgt = v3(0, 0, 0), cp = v3(0, 0, 0);
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const cM = p.merge != null ? cue(p.merge) : 1e9, cA = p.approach != null ? cue(p.approach) : 1e9;
    const DA = cA < 1e8 && cM < 1e8 && cM > cA + 4 ? Math.min(16, cM - cA) : 10;
    const MG = p.merged != null && p.merged !== false && p.merged !== 0 ? 1 : 0;
    const m = Math.max(MG, at(p.merge, 6)), al = at(p.alone, 8), er = at(p.erase, 6);
    const a = Math.max(MG, cA < 1e8 ? sm(cA, cA + DA, t) : 0, cM < 1e8 ? sm(cM - 5, cM, t) : 0);
    // positions: inspiral about the barycentre
    const rel = relAt(a), rel2 = relAt(Math.min(1, a + .02)), drift = v3(Math.sin(u * .02) * 3, 0, u * .15);
    const bc = BC0.clone().add(drift);
    const pMW = bc.clone().addScaledVector(rel, -mB / (mA + mB)), pM31 = bc.clone().addScaledVector(rel, mA / (mA + mB));
    const pM33 = M330.clone().add(drift).lerp(pM31.clone().add(v3(70, -30, -60)), a * .5);
    const PS = [pMW, pM31, pM33];
    const k = sm(.3, .85, a) * (1 - .3 * m), A = rel.clone().normalize(), Tn = rel2.clone().sub(rel).normalize();
    for (let g = 0; g < 3; g++) { const [ex, ey, ez] = tilts[g];
      eu.set(ex + (g < 2 ? .3 * a : 0), ey + (g === 0 ? 1 : -1) * .25 * a, ez); q1.setFromEuler(eu);
      q2.setFromAxisAngle(v3(0, 1, 0), -(t * (g === 2 ? .02 : .012)) - g * 1.3); q1.multiply(q2);
      tmpM.compose(PS[g], q1, sc1); U.uM.value[g].copy(tmpM); GAL[g].grp.position.copy(PS[g]); GAL[g].grp.quaternion.copy(q1);
      const sgn = g === 0 ? -1 : 1, L = SPEC[g].R * 1.2, kk = g === 2 ? .15 * k : k;
      U.uTA.value[g].copy(A).multiplyScalar(sgn * L * kk); U.uTT.value[g].copy(Tn).multiplyScalar(-sgn * L * 1.7 * kk); }
    const gm = [m, m, sm(.25, 1, m)]; U.uGm.value = gm;
    const cen = bc.clone(); U.uCen.value.copy(cen); U.uRot.value = t * .01;
    // light layers: fade with tidal disruption and merge; merge glow then remnant glow
    GAL.forEach((G2, g) => { const f = (1 - .55 * (g < 2 ? k : 0)) * (1 - gm[g]); G2.pl.material.opacity = .95 * f; G2.core.material.opacity = .32 * (1 - gm[g] * .9) * (g === 2 ? .6 : 1); G2.halo.material.opacity = .05 * f; });
    mGlow.position.copy(cen); mGlow.material.opacity = .4 * sm(.7, 1, a) * (1 - .6 * m); mGlow.scale.setScalar(40 + 70 * sm(.7, 1, a));
    eGlow.position.copy(cen); eCore.position.copy(cen); eGlow.material.opacity = .3 * m; eCore.material.opacity = .45 * m;
    // background: set A fades (reddens, recedes) on `alone`, set B on `erase`
    bgList.forEach(b => { const f = b.keep ? (1 - er) * (1 - .45 * al) : 1 - sm(b.ph * .6, .4 + b.ph * .6, al), rec = 1 + (b.keep ? .2 * er : .5 * al * b.ph);
      b.sp.material.opacity = b.base * f; b.sp.position.copy(b.d).multiplyScalar(b.dist * rec);
      if (!b.keep && al > 0) b.sp.material.color.setRGB(1, b.warm ? .85 - .3 * al : .8 - .25 * al, b.warm ? .7 - .4 * al : 1 - .55 * al); });
    fpA.material.opacity = .55 * (1 - al); fpB.material.opacity = .45 * (1 - .5 * al) * (1 - er);
    // camera: slow orbit around the barycentre; closer during the merge; far pull-back on `alone`
    const D = (360 - 50 * sm(.3, 1, a) - 20 * m) * VF * (1 + 3.6 * al + .6 * er), az = -.05 + u * .006 + .25 * a, el = .38 + .1 * al;
    tgt.copy(cen).lerp(cen.clone().add(v3(0, 0, 0)), 1);
    cp.set(Math.sin(az) * Math.cos(el), Math.sin(el), Math.cos(az) * Math.cos(el)).multiplyScalar(D).add(tgt);
    cam.position.copy(cp); cam.lookAt(tgt); cam.updateMatrixWorld();
    U.uPx.value = ctx.H / (2 * Math.tan(cam.fov * Math.PI / 360));
    U.uBr.value = [1, 1, .9];
  } };
};
