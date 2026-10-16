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
//           speed pass 2026-10-16: besides the drifting field, an endless stream of ~380 galaxies is born near us and carried out
//           through the shell (r = r_in * e^(lambda s), s = fract(F(t) * rate_k + phase_k)); slow after cross, accelerating for
//           ~23 s after vanish (with motion streaks that lengthen with speed), then calming down again (from vanish + 23 s) so the
//           later seen / lost / edge shots read clearly. Same cues -> same state in every instance (seek-safe).
//   seen    S23 camera pulls back; the faint outer sphere (observable universe) appears; galaxies between the two spheres turn dim
//           violet (seen but unreachable), nothing shows beyond the outer sphere
//   lost    S24 every galaxy outside the reachable shell dims to grey violet; only the few inside stay gold (and brighten)
//   edge    S27 camera pulls far back and turns; the outer sphere fades, the horizon closes in a little around us: our small
//           reachable bubble is the true edge
//   side    subject offset (default .12)
// fourth staging pass (2026-10-16): each appearance gets its own camera and beat, picked by `view` (optional; absent = inferred:
//   Shorts (VERT) -> 'classic' (the original orbit); else edge -> 'orbit', seen/lost -> 'reach', vanish -> 'slip', shell -> 'ray')
//   'ray'    (c8) the camera starts close to us and pulls back through the field; a faint inner sphere (the 14 Gly Hubble sphere)
//            appears (`hubble`, default shot start + 3.7 s), photons from just beyond it crawl in and reach us, the sphere creeps
//            outward; on the shell the horizon rim flares; the beam is fired on `beam` (default cross + 2.6 s) and the camera
//            chases it toward a galaxy just beyond the horizon: the photon stalls, the galaxy recedes, tick marks between them spread
//            apart; then the camera swings aside to show the whole stalled line.
//   'slip'   (c9b) the camera hangs just outside the horizon and looks along its limb (a curved edge across the frame): galaxies
//            slide over the edge one by one, each leaving a long red streak as it crosses; on `beam` (default vanish + 16.2 s,
//            "faster than we could follow") a photon chases them toward the limb and stalls.
//   'reach'  (c10) "travel anywhere": the camera sweeps fast through the field past home (a fly-by, ~10 s) and ends looking
//            back at us; pulls back on seen; on `ship` (default lost - 4.9 s) a gold light-speed front expands from us and
//            stalls at the horizon, lighting each reachable galaxy as it passes (the 6 %), the rest dim on lost; on `gallery`
//            (default lost + 24.5 s, "look") reticle rings settle on three distant violet galaxies (+0.9 s, +2.1 s: photograph,
//            study) and shrink away on "touch" (gallery + 4.3 s).
//   'orbit'  (c11) a slow orbit that shows the horizon as a sphere: a hard lat-long grid lights on the shell on `wall` (default
//            shot start + 5.3 s, "brick wall") and dissolves into soft glow (+4.5 s, "touch the void"); on `swept` (default
//            edge + 6 s) the galaxies outside are swept outward and fade, the stream speeds up again.
//   'classic' the original single orbit (kept for Short 1).
(window.MIYA = window.MIYA || { scenes: {} }).scenes.horizon = function (ctx, p) {
  const { T, sm, rng, cue, points, glow } = ctx, M = window.MIYA;
  const S = new T.Scene(); S.background = new T.Color('#04061a');
  const cT = c => c == null ? 1e9 : cue(c), on = (c0, d) => sm(c0, c0 + d, ctx.t);
  const cSh = p.shell == null ? -1e9 : cue(p.shell), cCr = cT(p.cross), cVa = cT(p.vanish), cSe = cT(p.seen), cLo = cT(p.lost), cEd = cT(p.edge);
  const RE0 = 16, RO = 46;
  const VIEW = p.view || (ctx.VERT ? 'classic' : p.edge != null ? 'orbit' : (p.seen != null || p.lost != null) ? 'reach' : p.vanish != null ? 'slip' : p.shell != null ? 'ray' : 'classic');
  const VR = VIEW === 'ray', VS = VIEW === 'slip', VC = VIEW === 'reach', VO = VIEW === 'orbit';
  const tBeam = p.beam != null ? cue(p.beam) : VR ? (cCr < 1e8 ? cCr + 2.6 : cSh + 2.5) : VS ? cVa + 16.2 : (p.shell == null ? 1e9 : cSh + 2.5);
  const tHub = VR ? cue(p.hubble, ctx.t0 + 3.7) : 1e9, tShip = VC ? cue(p.ship, cLo < 1e8 ? cLo - 4.9 : 1e9) : 1e9;
  const tGal = VC ? cue(p.gallery, cLo < 1e8 ? cLo + 24.5 : 1e9) : 1e9, tWall = VO ? cue(p.wall, ctx.t0 + 5.3) : 1e9, tSw = VO ? cue(p.swept, cEd < 1e8 ? cEd + 6 : 1e9) : 1e9;
  const bump = (x, a, b) => x <= 0 ? 0 : x < a ? sm(0, a, x) : Math.exp(-(x - a) / b);
  // outward drift (proper distance x G(t)), speeding up at vanish; bounded (x1.73) and independent of the shot span, so later
  // instances of this stage given the earlier cues continue the same state
  const Gof = t => Math.exp(.25 * sm(cCr, cCr + 25, t) + .3 * sm(cVa, cVa + 25, t));

  ctx.stars(S, 3800, 1500, { size: 1.7, opacity: .75, seed: 29 });
  const RN = rng(8); for (let k = 0; k < 4; k++) { const s = glow(S, k % 2 ? '#35287a' : '#1f2c66', 900 + RN() * 400, .14 + RN() * .06); const a = k * 1.6 + RN(); s.position.set(Math.sin(a) * 1300, (RN() - .4) * 600, Math.cos(a) * 1300); }

  // shells: fresnel rim + faint body + broad slow shimmer
  const shellMat = (col, rim) => new T.ShaderMaterial({ uniforms: { uCol: { value: new T.Color(col) }, uRim: { value: new T.Color(rim) }, uOp: { value: 0 }, uT: { value: 0 }, uGrid: { value: 0 } },
    vertexShader: 'varying vec3 vN, vV, vP; void main(){ vec4 mv = modelViewMatrix * vec4(position,1.); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); vP = position; gl_Position = projectionMatrix * mv; }',
    fragmentShader: `uniform vec3 uCol, uRim; uniform float uOp, uT, uGrid; varying vec3 vN, vV, vP;
      void main(){ float f = 1. - abs(dot(normalize(vN), normalize(vV)));
        float sh = .8 + .2 * sin(dot(vP, vec3(2.1, 1.3, -1.7)) + uT * .25) * sin(dot(vP, vec3(-1.1, 2.4, .8)) - uT * .18);
        vec3 c = uCol * .022 * sh + uRim * (pow(f, 4.) * .26 + pow(f, 12.) * .42) * sh;
        if (uGrid > 0.) { vec3 q = normalize(vP); float la = asin(clamp(q.y, -1., 1.)) / .2618, lo = atan(q.z, q.x) / .2618, w = fwidth(la) * 1.4;
          float g = max(1. - smoothstep(0., w, abs(fract(la + .5) - .5)), 1. - smoothstep(0., w / max(.15, sqrt(1. - q.y * q.y)), abs(fract(lo + .5) - .5)));
          c += uRim * g * uGrid * (.18 + .5 * pow(f, 2.)); }
        gl_FragColor = vec4(c * uOp, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }`, transparent: true, depthWrite: false, blending: T.AdditiveBlending });
  const sg = new T.SphereGeometry(1, 96, 64);
  const shell = new T.Mesh(sg, shellMat('#6a58d8', '#ffc65a')), outer = new T.Mesh(sg, shellMat('#3c4cb0', '#8a9cff'));
  shell.renderOrder = 2; outer.renderOrder = 1; S.add(shell, outer); outer.scale.setScalar(RO);
  // view extras: the 14 Gly Hubble sphere (ray), the light-speed reach front (reach)
  const hub = new T.Mesh(sg, shellMat('#4a6ad8', '#a8d4ff')), front = new T.Mesh(sg, shellMat('#c89a3a', '#ffd27a'));
  hub.renderOrder = front.renderOrder = 3; hub.visible = front.visible = false; S.add(hub, front);

  // galaxies: index 0 = the Milky Way; the rest spread to r ~ 62, a little denser toward us
  const N = 1000, NQ = 380, GN = N + NQ, GF = M.cosmicGal(ctx, GN), R1 = rng(41), dir = [], r0 = [], base = [], szs = [];
  for (let i = 0; i < N; i++) {
    const u = R1() * 2 - 1, a = R1() * 6.283, q = Math.sqrt(1 - u * u);
    dir.push([q * Math.cos(a), u * .8, q * Math.sin(a)]);
    r0.push(i === 0 ? 0 : 2.2 + 60 * Math.pow(R1(), 1.25));
    const kind = GF.random(i, R1, .7, 1.6), cu = R1(), br = .5 + .55 * R1();
    const col = kind === 1 ? [1, .8, .55] : cu < .7 ? [1, .84, .58] : cu < .9 ? [.86, .78, 1] : [.92, .9, 1];
    base.push([col[0] * br, col[1] * br, col[2] * br]); }
  GF.shape(0, 1.5, .5, .45, 0, 1.6); S.add(GF.mesh);
  // the stream (instances N..GN-1)
  const R4 = rng(47), QD = [];
  for (let k = 0; k < NQ; k++) { const u = R4() * 2 - 1, a = R4() * 6.283, q = Math.sqrt(1 - u * u);
    const kind = GF.random(N + k, R4, .7, 1.5), cu = R4(), br = .5 + .55 * R4();
    const col = kind === 1 ? [1, .8, .55] : cu < .7 ? [1, .84, .58] : cu < .9 ? [.86, .78, 1] : [.92, .9, 1];
    const rin = 2.6 + 2.4 * R4();
    QD.push([q * Math.cos(a), u * .8, q * Math.sin(a), rin, .8 + .4 * R4(), R4(), col[0] * br, col[1] * br, col[2] * br, Math.log(42 / rin)]); }
  const SK = M.cosmicStreaks(ctx, NQ); S.add(SK.mesh);
  const rateF = x => .03 * sm(cCr, cCr + 5, x) + (x > cVa ? .02 * (Math.exp(Math.min(x - cVa, 23) / 8) - 1) * (1 - sm(cVa + 23, cVa + 38, x)) : 0)
    + (VO ? .045 * sm(tSw, tSw + 3, x) * (1 - sm(tSw + 9, tSw + 16, x)) : 0);
  const Fof = t => M.integ(rateF, cCr, t, .1), fr = x => x - Math.floor(x);
  for (let i = 0; i < GN * 2; i++) szs.push(0);
  const Qa = GF.mesh.geometry.attributes.iPar; for (let i = 0; i < GN * 2; i++) szs[i] = Qa.array[i * 4];
  const us1 = glow(S, '#ffcf8a', 4, .4), us2 = glow(S, '#fff3da', 1.1, .9), us3 = glow(S, '#ffb860', 12, .08);

  // the beam we fire (S18): a photon that slows and stalls just inside the horizon (direction set per view below)
  const bDir = new T.Vector3(.75, .28, -.6).normalize(), bH = glow(S, '#fff6e0', 1.3, 0), bG = glow(S, '#ffd090', 4, 0), bT = [];
  for (let k = 0; k < 9; k++) bT.push(glow(S, '#ffc070', 1.0 - k * .06, 0));
  // ray: photons from just beyond the Hubble sphere that still reach us; tick marks between the stalled beam and its galaxy
  const PH = [], R6 = rng(61); if (VR) for (let k = 0; k < 7; k++) { const u = R6() * 1.4 - .6, a = R6() * 6.283, q = Math.sqrt(1 - u * u);
    PH.push({ d: new T.Vector3(q * Math.cos(a), u * .8, q * Math.sin(a)).normalize(), t: ctx.t0 + .5 + k * .42 + R6() * .2, h: glow(S, '#e4f0ff', .5, 0), tr: [0, 1, 2, 3].map(j => glow(S, '#9fc4ff', .38 - j * .06, 0)) }); }
  const TK = []; if (VR) for (let k = 0; k < 10; k++) TK.push(glow(S, '#bfe0ff', .55, 0));
  // reach: three reticle rings for "look, photograph, study"
  const ringT = ctx.ctex(128, (g, s2) => { g.strokeStyle = 'rgba(255,255,255,.95)'; g.lineWidth = 5; g.beginPath(); g.arc(s2 / 2, s2 / 2, s2 * .4, 0, 6.283); g.stroke();
    g.lineWidth = 4; [[0, -1], [0, 1], [-1, 0], [1, 0]].forEach(([x, y]) => { g.beginPath(); g.moveTo(s2 / 2 + x * s2 * .32, s2 / 2 + y * s2 * .32); g.lineTo(s2 / 2 + x * s2 * .48, s2 / 2 + y * s2 * .48); g.stroke(); }); });
  const RET = VC ? [0, 1, 2].map(() => { const sp = new T.Sprite(new T.SpriteMaterial({ map: ringT, color: '#cdbcff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, depthTest: false })); sp.renderOrder = 6; S.add(sp); return sp; }) : [];
  const RETT = [tGal, tGal + .9, tGal + 2.1], tTouch = tGal + 4.3;

  // dust in the volume
  const ND = 1400, dust = points(ND, { size: .35, opacity: .8 }), dA = dust.geometry.attributes.position.array, dC = dust.geometry.attributes.color.array;
  { const r = rng(52); for (let i = 0; i < ND; i++) { const u = r() * 2 - 1, a = r() * 6.283, q = Math.sqrt(1 - u * u), rr = 3 + 70 * Math.cbrt(r()); dA.set([q * Math.cos(a) * rr, u * rr * .8, q * Math.sin(a) * rr], i * 3);
    const v = .08 + .12 * r(); dC.set(r() < .5 ? [v, v * .8, v * .55] : [v * .65, v * .6, v], i * 3); } }
  S.add(dust);

  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .5, 6000); ctx.side(cam, p.side == null ? .12 : p.side);
  const RED = [.75, .16, .12], VIO = [.46, .36, .95], GRV = [.42, .4, .6];
  const V = (x, y, z) => new T.Vector3(x, y, z), Y = V(0, 1, 0), sph = (az, el, D) => V(Math.sin(az) * Math.cos(el) * D, Math.sin(el) * D, Math.cos(az) * Math.cos(el) * D);
  const Rof = t => RE0 - 4 * sm(cEd, cEd + 9, t);
  const rbOf = t => { const tb = t - tBeam; return Rof(t) * .975 * (1 - Math.exp(-Math.max(0, tb) / (VS ? 2.2 : 4.5))); };
  const upB = Y.clone().addScaledVector(bDir, -bDir.y).normalize(), sdB = new T.Vector3().crossVectors(bDir, upB);
  // slip: the limb point seen from a camera hanging just outside the horizon
  const slipAt = (t, u) => { const az = .5 + u * .022, n = V(Math.sin(az), .22, Math.cos(az)).normalize(), up = Y.clone().addScaledVector(n, -n.y).normalize(), R = Rof(t);
    const d = R * (1.8 - .35 * sm(ctx.t0, ctx.t1, t)), th = Math.acos(R / d); return { p: n.clone().multiplyScalar(d), tg: n.clone().multiplyScalar(R * Math.cos(th)).addScaledVector(up, R * Math.sin(th)) }; };
  if (VS) { const L = slipAt(tBeam + 4, tBeam + 4 - ctx.t0).tg; bDir.copy(L).normalize().applyAxisAngle(Y, .05); upB.copy(Y).addScaledVector(bDir, -bDir.y).normalize(); sdB.crossVectors(bDir, upB); }
  if (VR) { dir[1] = [bDir.x, bDir.y, bDir.z]; r0[1] = 19.5; }
  const dF = V(Math.sin(.55) * Math.cos(.25), Math.sin(.25), Math.cos(.55) * Math.cos(.25));
  // camera per view: { p: position, tg: look-at } as a pure function of t (look-at distance always continuous)
  function camAt(t, u) {
    const se = sm(cSe, cSe + 7, t), ed = sm(cEd, cEd + 9, t);
    const Dc = (66 + 119 * Math.max(se, .7 * ed) + 40 * ed) * (1 + .03 * Math.sin(u * .05)), azc = .3 + u * .006 + .6 * ed, elc = .3 + .12 * ed;
    if (VR) { const k = sm(ctx.t0, (cSh > -1e8 ? cSh : ctx.t0 + 14) + 2, t), pA = sph(-.4 + 1.0 * k + u * .006, .12 + .18 * k, 22 + 46 * k), tA = V(0, 0, 0);
      const ph = bDir.clone().multiplyScalar(rbOf(t)), pC = ph.clone().addScaledVector(bDir, -5).addScaledVector(upB, 6).addScaledVector(sdB, 21), tC = ph.clone().addScaledVector(bDir, 3.5);
      const R = Rof(t), pW = bDir.clone().multiplyScalar(R * .45).addScaledVector(sdB, 36).addScaledVector(upB, 14), tW = bDir.clone().multiplyScalar(R * .95);
      const wc = sm(tBeam - 1, tBeam + 2, t), ww = sm(tBeam + 6, tBeam + 11, t);
      return { p: pA.lerp(pC, wc).lerp(pW, ww), tg: tA.lerp(tC, wc).lerp(tW, ww) }; }
    if (VS) return slipAt(t, u);
    if (VC) { const f = sm(ctx.t0 - .8, ctx.t0 + 9.6, t), sdF = new T.Vector3().crossVectors(dF, Y).normalize(), pF = dF.clone().multiplyScalar(-32 + 44 * f).addScaledVector(sdF, 6).addScaledVector(Y, 2.2), tF = V(0, 0, 0);
      const D2 = Dc * (1 - .42 * sm(tShip - 1.5, tShip + 2.5, t) * (1 - sm(cLo + 5, cLo + 11, t))) + 70 * sm(cLo + 9.5, cLo + 19, t), az = azc + .35 * sm(cLo + 19.5, cLo + 28, t), pS = sph(az, elc, D2), wS = sm(cSe, cSe + 7, t);
      return { p: pF.lerp(pS, wS), tg: tF.lerp(V(0, 0, 0), wS) }; }
    if (VO) { const az = 2.2 + u * .045, el = .45 - .32 * sm(ctx.t0, ctx.t0 + 14, t) + .3 * sm(ctx.t0 + 14, ctx.t1 + 2, t), D = 150 + 45 * ed - 70 * sm(tSw + 1, ctx.t1 + 1, t);
      return { p: sph(az, el, D), tg: V(0, 0, 0) }; }
    return { p: sph(azc, elc, Dc), tg: V(0, 0, 0) }; }
  const nA = VR || VS || VC ? 2 : 14, nB = VR || VS || VC ? 6 : 30;
  let RETI = null;
  function pickRet() { const c0 = camAt(tGal + .5, tGal + .5 - ctx.t0); cam.position.copy(c0.p); cam.lookAt(c0.tg); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
    const G0 = Gof(tGal), v = new T.Vector3(), cand = [];
    for (let i = 2; i < N; i++) { const r = r0[i] * G0; if (r < 23 || r > RO * .88) continue; v.set(dir[i][0] * r, dir[i][1] * r, dir[i][2] * r).project(cam);
      if (v.z > 1 || v.x < -.05 || v.x > .8 || v.y < -.55 || v.y > .4) continue; cand.push([base[i][0] + base[i][1], i, v.x, v.y]); }
    cand.sort((a, b) => b[0] - a[0]); const out = [];
    for (const c of cand) { if (out.every(o => Math.hypot(o[2] - c[2], (o[3] - c[3]) * .56) > .32)) out.push(c); if (out.length === 3) break; }
    return out.map(o => o[1]); }
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    if (VC && !RETI && tGal < 1e8) RETI = pickRet();
    const sh = on(cSh, 3.5), cr = Math.max(on(cCr, 4), on(cVa, 4)), se = on(cSe, 7), lo = on(cLo, 5), ed = on(cEd, 9), G = Gof(t);
    const R = RE0 - 4 * ed;
    const cs = camAt(t, u); cam.position.copy(cs.p); cam.lookAt(cs.tg); cam.updateMatrixWorld();
    const D = cam.position.length(), pxW = 2 * Math.tan(cam.fov * Math.PI / 360) / ctx.H;
    const shF = VR ? 1 + .9 * bump(t - cSh, .35, 1.6) : 1, gv = VO ? sm(tWall, tWall + .4, t) * (1 - sm(tWall + 3.2, tWall + 4.8, t)) : 0, soft = VO ? .5 * bump(t - tWall - 3.6, 1, 2.5) : 0;
    shell.scale.setScalar(R); shell.material.uniforms.uOp.value = sh * (1 + .5 * ed) * shF * (1 + soft); shell.material.uniforms.uT.value = t; shell.material.uniforms.uGrid.value = gv * 1.6;
    outer.material.uniforms.uOp.value = se * (1 - ed) * .5; outer.material.uniforms.uT.value = t;
    // ray: the Hubble sphere (14 Gly) appears, creeps outward, fades as the true horizon shows up
    hub.visible = VR && t > tHub && t < cSh + 4.5;
    if (hub.visible) { hub.scale.setScalar(14 + 1.4 * sm(tHub + 3.8, tHub + 6.8, t)); hub.material.uniforms.uOp.value = .38 * sm(tHub, tHub + 2, t) * (1 - sm(cSh - .5, cSh + 4, t)); hub.material.uniforms.uT.value = t; }
    // reach: the light-speed front from us, stalling at the horizon
    const rf = R * .985 * (1 - Math.exp(-Math.max(0, t - tShip) / 2.6)); front.visible = VC && t > tShip;
    if (front.visible) { front.scale.setScalar(Math.max(.05, rf)); front.material.uniforms.uOp.value = 1.4 * sm(tShip, tShip + .3, t) * (1 - .75 * sm(tShip + 5, tShip + 12, t)); front.material.uniforms.uT.value = t; }
    const gk = Math.pow(D / 66, .55), Q = Qa.array;
    for (let i = 0; i < GN * 2; i++) Q[i * 4] = szs[i] * gk; Qa.needsUpdate = true;
    // lost colour / brightness by stage: red (just crossed) -> violet (seen, unreachable) -> grey violet (lost) -> dimmer (edge)
    const lc = [0, 1, 2].map(k => (RED[k] * (1 - se) + VIO[k] * se) * (1 - lo) + GRV[k] * lo);
    const lb = (.3 * (1 - se) + .4 * se) * (1 - lo) + .3 * lo - .08 * ed;
    const swE = VO ? sm(tSw, tSw + 9, t) : 0, cp = cam.position;
    const retK = RETI ? RETI.map((i, k) => sm(RETT[k], RETT[k] + .25, t) * (1 - sm(tTouch, tTouch + 1.5, t))) : null;
    for (let i = 0; i < N; i++) { const d = dir[i], b = base[i]; let r = r0[i] * G;
      if (i === 0) { GF.set(0, 0, 0, 0, 1.2, .95, .66, 1.6); continue; }
      let fsw = 0; if (swE > 0) { const o = sm(R * 1.05, R * 1.5, r); r *= 1 + 1.8 * swE * swE * o; fsw = 1.6 * swE * (1 - swE) * o; }
      const x = d[0] * r, y = d[1] * r, z = d[2] * r;
      const L = sm(R * .98, R * 1.2, r) * Math.max(cr, se, lo, ed);
      const fl = cr * Math.exp(-Math.pow((r / R - 1.05) / .04, 2)) * (1 - lo) + fsw;
      const hide = (1 - sm(RO * .96, RO * 1.04, r) * se) * sm(nA, nB, Math.hypot(x - cp.x, y - cp.y, z - cp.z));
      let gold = 1 + .25 * lo, fx = 0;
      if (VC && t > tShip) { const lit = sm(r - .4, r + .4, rf), pu = lit * Math.exp(-Math.pow((rf - r) / .9, 2)); gold *= 1 + .6 * lit; fx = 1.4 * pu; }
      const k0 = (1 - L) * gold * (VR && i === 1 ? 1.8 : 1), k1 = L * lb * (VR && i === 1 ? 3 : 1) * (retK ? 1 + 1.2 * ((RETI[0] === i ? retK[0] : 0) + (RETI[1] === i ? retK[1] : 0) + (RETI[2] === i ? retK[2] : 0)) : 1);
      GF.set(i, x, y, z, (b[0] * k0 + lc[0] * k1 + fl * .9 + fx) * hide, (b[1] * k0 + lc[1] * k1 + fl * .25 + fx * .8) * hide, (b[2] * k0 + lc[2] * k1 + fl * .2 + fx * .45) * hide, 1 + fl * 2 + fx); }
    // stream: same colouring by stage; the crossing flare widens with speed (each one lasts >= ~0.3 s, no sparkle)
    const swV = VO ? sm(tSw, tSw + 2, t) * (1 - sm(tSw + 12, tSw + 17, t)) : 0;
    const calm = 1 - .45 * sm(cVa + 23, cVa + 40, t) * (1 - swV), Tb = .35, Ft = Fof(t), Fb = Fof(t - Tb), Fl = VS ? Fof(t - 1.6) : Fb, rt0 = rateF(t), act = Math.max(cr, se, lo, ed);
    for (let k = 0; k < NQ; k++) { const d = QD[k], j = N + k, b = [d[6], d[7], d[8]];
      const LAM = d[9], s = fr(Ft * d[4] + d[5]), st = Math.max(0, s - (Ft - Fb) * d[4]), r = d[3] * Math.exp(LAM * s), rq = d[3] * Math.exp(LAM * st);
      const dc = Math.hypot(d[0] * r - cp.x, d[1] * r - cp.y, d[2] * r - cp.z);
      const vis = sm(0, .1, s) * (1 - sm(.8, 1, s)) * sm(nA, nB, dc) * calm, v = LAM * r * rt0 * d[4];
      const L = sm(R * .98, R * 1.2, r) * act, wr = Math.max(.04, v * .3 / R);
      const fl = cr * Math.exp(-Math.pow((r / R - 1.05) / wr, 2)) * (1 - lo) * .04 / wr, hide = (1 - sm(RO * .96, RO * 1.04, r) * se) * vis;
      let gold = 1 + .25 * lo, fx = 0;
      if (VC && t > tShip) { const lit = sm(r - .4, r + .4, rf); gold *= 1 + .6 * lit; fx = 1.4 * lit * Math.exp(-Math.pow((rf - r) / .9, 2)); }
      const k0 = (1 - L) * gold, k1 = L * lb;
      const cR = (b[0] * k0 + lc[0] * k1 + fl * .9 + fx) * hide, cG = (b[1] * k0 + lc[1] * k1 + fl * .25 + fx * .8) * hide, cB = (b[2] * k0 + lc[2] * k1 + fl * .2 + fx * .45) * hide;
      GF.set(j, d[0] * r, d[1] * r, d[2] * r, cR, cG, cB, 1 + fl * 2 + fx);
      // slip: every galaxy crossing the edge leaves a long red streak (tail 1.6 s back)
      const cb = VS ? cr * Math.exp(-Math.pow((r / R - 1.12) / .14, 2)) * hide : 0;
      const sk = Math.max(.4 * sm(.6, 3, v), .7 * cb);
      if (sk < .002 || hide < .002) { SK.hide(k); continue; }
      if (cb > .01) { const rl = d[3] * Math.exp(LAM * Math.max(0, s - (Ft - Fl) * d[4]));
        SK.set(k, d[0] * r, d[1] * r, d[2] * r, d[0] * rl, d[1] * rl, d[2] * rl, cR * sk + .5 * cb, cG * sk + .1 * cb, cB * sk + .08 * cb, 2.8, .7 * sk, .1 * sk, .07 * sk); continue; }
      SK.set(k, d[0] * r, d[1] * r, d[2] * r, d[0] * rq, d[1] * rq, d[2] * rq, cR * sk, cG * sk, cB * sk, 2.6, .35 * sk * hide, .28 * sk * hide, .6 * sk * hide); }
    GF.flush(); SK.flush();
    // us: glows (ray: each incoming photon that arrives lights us up a little)
    let arr = 0;
    PH.forEach(ph => { const s2 = (t - ph.t) / 7, on2 = s2 > 0 && s2 < 1, rr = (15.1 + .9 * Math.sin(Math.PI * sm(0, .45, s2))) * (1 - sm(.3, 1, s2)), a = on2 ? .9 * sm(0, .08, s2) * (1 - sm(.93, 1, s2)) * (1 - sm(tHub + 9, tHub + 11, t)) : 0;
      arr += bump(t - ph.t - 7, .2, 1.1); ph.h.visible = a > 0; ph.h.position.copy(ph.d).multiplyScalar(rr); ph.h.material.opacity = a;
      const sp = Math.abs(1 - sm(.3, 1, s2)) + .2; ph.tr.forEach((g2, j) => { g2.visible = a > 0; g2.position.copy(ph.d).multiplyScalar(rr + (j + 1) * .35 * sp * (s2 > .4 ? 1 : -1)); g2.material.opacity = a * .4 * (1 - j / 4); }); });
    const uk = Math.pow(D / 66, .7) * (1 + .5 * Math.min(1, arr)); us1.scale.setScalar(4 * uk); us2.scale.setScalar(1.1 * uk); us3.scale.setScalar(12 * uk); us1.material.opacity = .4 * (1 + .8 * Math.min(1, arr));
    // beam: r -> R asymptotically, never crossing
    const tb = t - tBeam, bv = tb > 0 ? sm(0, VR ? .3 : 1, tb) * (1 - sm(VR || VS ? 30 : 22, VR || VS ? 36 : 28, tb)) : 0;
    const rb = rbOf(t), bs = VR || VS ? .5 : 1;
    bH.position.copy(bDir).multiplyScalar(rb); bG.position.copy(bH.position); bH.material.opacity = .95 * bv; bG.material.opacity = .3 * bv;
    bH.scale.setScalar(1.3 * bs); bG.scale.setScalar(4 * bs);
    const sp = Math.exp(-Math.max(0, tb) / 4.5);   // the tail shortens as the beam stalls
    bT.forEach((s, k) => { s.position.copy(bDir).multiplyScalar(Math.max(0, rb - (.4 + k * .55) * (.25 + sp) * bs)); s.material.opacity = bv * .5 * (1 - k / 9); s.scale.setScalar((1 - k * .06) * bs); });
    // ray: tick marks between the stalled photon and the receding galaxy beyond the horizon spread apart
    if (VR) { const rg = r0[1] * G, tv = sm(tBeam + 1.5, tBeam + 3, t) * (1 - sm(tBeam + 30, tBeam + 36, t));
      TK.forEach((g2, k) => { g2.visible = tv > 0; g2.position.copy(bDir).multiplyScalar(rb + (rg - rb) * (k + 1) / 11); g2.material.opacity = .5 * tv; g2.scale.setScalar(.3 + .15 * gk); }); }
    // reach: reticle rings on three distant galaxies ("look, photograph, study"), shrinking away on "touch"
    if (RETI) RET.forEach((sp2, k) => { const i = RETI[k], a = retK[k] || 0; sp2.visible = i != null && a > .002; if (!sp2.visible) return; const r = r0[i] * G;
      sp2.position.set(dir[i][0] * r, dir[i][1] * r, dir[i][2] * r); const dd = sp2.position.distanceTo(cp);
      sp2.scale.setScalar(dd * pxW * 92 * (1.7 - .7 * sm(RETT[k], RETT[k] + .5, t)) * (1 - .45 * sm(tTouch, tTouch + 1.5, t))); sp2.material.opacity = .9 * a; });
  } };
};
