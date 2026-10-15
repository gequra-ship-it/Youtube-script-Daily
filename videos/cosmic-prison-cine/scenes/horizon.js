// requires: expanse
// horizon — the cosmic event horizon around us (cosmic-prison-cine S18, S21, S23-S24, S27; written 2026-10-15). Us = the Milky Way,
// a tiny warm glowing point at the centre, among ~700 small galaxies (MIYA.cosmicGal from expanse.js). Distances are in billions of
// light-years: a translucent shell with a fresnel edge glow marks the cosmic event horizon (radius 16), a larger faint sphere the
// observable universe (radius 46). Galaxies are carried outward (accelerating, dark energy); once past the horizon they redden and
// dim — still visible, never reachable.
// params (cues; all optional):
//   shell   S18 the horizon shell fades in around us (absent: the shell is simply there); a light beam fired from us then crawls
//           toward a galaxy beyond it and never arrives (it slows and stalls just inside the shell)
//   cross   galaxies start drifting outward; the ones past the shell redden and fade (a faint red flare as each one crosses)
//   vanish  S21 the drift speeds up: more and more galaxies slip across
//   seen    S23 camera pulls back; the faint outer sphere (observable universe) appears; galaxies between the two spheres turn dim
//           violet (seen but unreachable), nothing shows beyond the outer sphere
//   lost    S24 every galaxy outside the reachable shell dims to grey violet; only the few inside stay gold (and brighten)
//   edge    S27 camera pulls far back and turns; the outer sphere fades, the horizon closes in a little around us: our small
//           reachable bubble is the true edge
//   side    subject offset (default .12)
(window.MIYA = window.MIYA || { scenes: {} }).scenes.horizon = function (ctx, p) {
  const { T, sm, rng, cue, points, glow } = ctx, M = window.MIYA;
  const S = new T.Scene(); S.background = new T.Color('#04061a');
  const cT = c => c == null ? 1e9 : cue(c), on = (c0, d) => sm(c0, c0 + d, ctx.t);
  const cSh = p.shell == null ? -1e9 : cue(p.shell), cCr = cT(p.cross), cVa = cT(p.vanish), cSe = cT(p.seen), cLo = cT(p.lost), cEd = cT(p.edge);
  const RE0 = 16, RO = 46;
  // outward drift (proper distance x G(t)), speeding up at vanish; bounded (x1.73) and independent of the shot span, so later
  // instances of this stage given the earlier cues continue the same state
  const Gof = t => Math.exp(.25 * sm(cCr, cCr + 25, t) + .3 * sm(cVa, cVa + 25, t));

  ctx.stars(S, 3800, 1500, { size: 1.7, opacity: .75, seed: 29 });
  const RN = rng(8); for (let k = 0; k < 4; k++) { const s = glow(S, k % 2 ? '#35287a' : '#1f2c66', 900 + RN() * 400, .14 + RN() * .06); const a = k * 1.6 + RN(); s.position.set(Math.sin(a) * 1300, (RN() - .4) * 600, Math.cos(a) * 1300); }

  // shells: fresnel rim + faint body + broad slow shimmer
  const shellMat = (col, rim) => new T.ShaderMaterial({ uniforms: { uCol: { value: new T.Color(col) }, uRim: { value: new T.Color(rim) }, uOp: { value: 0 }, uT: { value: 0 } },
    vertexShader: 'varying vec3 vN, vV, vP; void main(){ vec4 mv = modelViewMatrix * vec4(position,1.); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); vP = position; gl_Position = projectionMatrix * mv; }',
    fragmentShader: `uniform vec3 uCol, uRim; uniform float uOp, uT; varying vec3 vN, vV, vP;
      void main(){ float f = 1. - abs(dot(normalize(vN), normalize(vV)));
        float sh = .8 + .2 * sin(dot(vP, vec3(2.1, 1.3, -1.7)) + uT * .25) * sin(dot(vP, vec3(-1.1, 2.4, .8)) - uT * .18);
        vec3 c = uCol * .022 * sh + uRim * (pow(f, 4.) * .26 + pow(f, 12.) * .42) * sh;
        gl_FragColor = vec4(c * uOp, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }`, transparent: true, depthWrite: false, blending: T.AdditiveBlending });
  const sg = new T.SphereGeometry(1, 96, 64);
  const shell = new T.Mesh(sg, shellMat('#6a58d8', '#ffc65a')), outer = new T.Mesh(sg, shellMat('#3c4cb0', '#8a9cff'));
  shell.renderOrder = 2; outer.renderOrder = 1; S.add(shell, outer); outer.scale.setScalar(RO);

  // galaxies: index 0 = the Milky Way; the rest spread to r ~ 62, a little denser toward us
  const N = 1000, GF = M.cosmicGal(ctx, N), R1 = rng(41), dir = [], r0 = [], base = [], szs = [];
  for (let i = 0; i < N; i++) {
    const u = R1() * 2 - 1, a = R1() * 6.283, q = Math.sqrt(1 - u * u);
    dir.push([q * Math.cos(a), u * .8, q * Math.sin(a)]);
    r0.push(i === 0 ? 0 : 2.2 + 60 * Math.pow(R1(), 1.25));
    const kind = GF.random(i, R1, .7, 1.6), cu = R1(), br = .5 + .55 * R1();
    const col = kind === 1 ? [1, .8, .55] : cu < .7 ? [1, .84, .58] : cu < .9 ? [.86, .78, 1] : [.92, .9, 1];
    base.push([col[0] * br, col[1] * br, col[2] * br]); }
  GF.shape(0, 1.5, .5, .45, 0, 1.6); S.add(GF.mesh);
  for (let i = 0; i < N * 2; i++) szs.push(0);
  const Qa = GF.mesh.geometry.attributes.iPar; for (let i = 0; i < N * 2; i++) szs[i] = Qa.array[i * 4];
  const us1 = glow(S, '#ffcf8a', 4, .4), us2 = glow(S, '#fff3da', 1.1, .9), us3 = glow(S, '#ffb860', 12, .08);

  // the beam we fire (S18): a photon that slows and stalls just inside the horizon
  const bDir = new T.Vector3(.75, .28, -.6).normalize(), bH = glow(S, '#fff6e0', 1.3, 0), bG = glow(S, '#ffd090', 4, 0), bT = [];
  for (let k = 0; k < 9; k++) bT.push(glow(S, '#ffc070', 1.0 - k * .06, 0));

  // dust in the volume
  const ND = 1400, dust = points(ND, { size: .35, opacity: .8 }), dA = dust.geometry.attributes.position.array, dC = dust.geometry.attributes.color.array;
  { const r = rng(52); for (let i = 0; i < ND; i++) { const u = r() * 2 - 1, a = r() * 6.283, q = Math.sqrt(1 - u * u), rr = 3 + 70 * Math.cbrt(r()); dA.set([q * Math.cos(a) * rr, u * rr * .8, q * Math.sin(a) * rr], i * 3);
    const v = .08 + .12 * r(); dC.set(r() < .5 ? [v, v * .8, v * .55] : [v * .65, v * .6, v], i * 3); } }
  S.add(dust);

  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .5, 6000); ctx.side(cam, p.side == null ? .12 : p.side);
  const RED = [.75, .16, .12], VIO = [.46, .36, .95], GRV = [.42, .4, .6];
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const sh = on(cSh, 3.5), cr = Math.max(on(cCr, 4), on(cVa, 4)), se = on(cSe, 7), lo = on(cLo, 5), ed = on(cEd, 9), G = Gof(t);
    const R = RE0 - 4 * ed;
    const D = (66 + 119 * Math.max(se, .7 * ed) + 40 * ed) * (1 + .03 * Math.sin(u * .05)), az = .3 + u * .006 + .6 * ed, el = .3 + .12 * ed;
    cam.position.set(Math.sin(az) * Math.cos(el) * D, Math.sin(el) * D, Math.cos(az) * Math.cos(el) * D); cam.lookAt(0, 0, 0); cam.updateMatrixWorld();
    shell.scale.setScalar(R); shell.material.uniforms.uOp.value = sh * (1 + .5 * ed); shell.material.uniforms.uT.value = t;
    outer.material.uniforms.uOp.value = se * (1 - ed) * .5; outer.material.uniforms.uT.value = t;
    const gk = Math.pow(D / 66, .55), Q = Qa.array;
    for (let i = 0; i < N; i++) { Q[i * 4] = szs[i] * gk; Q[(N + i) * 4] = szs[N + i] * gk; } Qa.needsUpdate = true;
    // lost colour / brightness by stage: red (just crossed) -> violet (seen, unreachable) -> grey violet (lost) -> dimmer (edge)
    const lc = [0, 1, 2].map(k => (RED[k] * (1 - se) + VIO[k] * se) * (1 - lo) + GRV[k] * lo);
    const lb = (.3 * (1 - se) + .4 * se) * (1 - lo) + .3 * lo - .08 * ed;
    for (let i = 0; i < N; i++) { const d = dir[i], r = r0[i] * G, b = base[i];
      if (i === 0) { GF.set(0, 0, 0, 0, 1.2, .95, .66, 1.6); continue; }
      const x = d[0] * r, y = d[1] * r, z = d[2] * r;
      const L = sm(R * .98, R * 1.2, r) * Math.max(cr, se, lo, ed);
      const fl = cr * Math.exp(-Math.pow((r / R - 1.05) / .04, 2)) * (1 - lo);
      const hide = 1 - sm(RO * .96, RO * 1.04, r) * se;
      const gold = 1 + .25 * lo;
      const k0 = (1 - L) * gold, k1 = L * lb;
      GF.set(i, x, y, z, (b[0] * k0 + lc[0] * k1 + fl * .9) * hide, (b[1] * k0 + lc[1] * k1 + fl * .25) * hide, (b[2] * k0 + lc[2] * k1 + fl * .2) * hide, 1 + fl * 2); }
    GF.flush();
    const uk = Math.pow(D / 66, .7); us1.scale.setScalar(4 * uk); us2.scale.setScalar(1.1 * uk); us3.scale.setScalar(12 * uk);
    // beam: fired 2.5 s after the shell appears; r -> R asymptotically, never crossing
    const tb = t - (p.shell == null ? 1e9 : cSh + 2.5), bv = tb > 0 ? sm(0, 1, tb) * (1 - sm(22, 28, tb)) : 0;
    const rb = R * .975 * (1 - Math.exp(-Math.max(0, tb) / 4.5));
    bH.position.copy(bDir).multiplyScalar(rb); bG.position.copy(bH.position); bH.material.opacity = .95 * bv; bG.material.opacity = .3 * bv;
    const sp = Math.exp(-Math.max(0, tb) / 4.5);   // the tail shortens as the beam stalls
    bT.forEach((s, k) => { s.position.copy(bDir).multiplyScalar(Math.max(0, rb - (.4 + k * .55) * (.25 + sp))); s.material.opacity = bv * .5 * (1 - k / 9); });
  } };
};
