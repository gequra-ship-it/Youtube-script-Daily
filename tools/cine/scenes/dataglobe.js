// dataglobe — a glowing sphere of points (lat-long dots, bright nodes, arcs) that stays for a whole chapter (stage mode).
// Ported from prototype v2 (2026-10-14). Every effect starts at a cue (a unit id "U007" = unit start, or "U009:standstill" =
// that spoken word); omit a cue to switch the effect off.
// params: { radius:6, side:.08, dots:'#c3ccff', node:'#9fb2ff', flash:'#ffe2a8', bg:['#020309','#140f2e'], bgRamp:[0,30],
//   satellites:cue (far clocks appear, all flashing in step), river:[cueOn,cueOff] (particle band flows round), desync:cue
//   (flashes fall out of step), grid:cue (spacetime grid fades in under it), bend:cue, stretch:cue, crush:cue,
//   slow:[cueFrom,cueTo] (its own rotation/flashes slow nearly to a stop), orbit:.045 (camera turn speed), dist:31 }
(window.MIYA = window.MIYA || { scenes: {} }).scenes.dataglobe = function (ctx, p) {
  const { T, sm, rng, points, stars, glow, cue } = ctx;
  const RAD = p.radius || 6, S = new T.Scene(), G = new T.Group(); S.add(G);
  const bg = (p.bg || ['#020309', '#140f2e']).map(c => new T.Color(c)); S.background = bg[0].clone();
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), ctx.t);
  // lat-long dotted globe
  const gl = []; for (let m = 0; m < 28; m++) for (let k = 0; k < 110; k++) { const a = m / 28 * 6.283, b = k / 110 * Math.PI; gl.push([Math.sin(b) * Math.cos(a), Math.cos(b), Math.sin(b) * Math.sin(a)]); }
  for (let q = 1; q < 12; q++) { const b = q / 12 * Math.PI; for (let k = 0; k < 160; k++) { const a = k / 160 * 6.283; gl.push([Math.sin(b) * Math.cos(a), Math.cos(b), Math.sin(b) * Math.sin(a)]); } }
  const gp = points(gl.length, { size: .13, opacity: .8, color: p.dots || '#c3ccff' }); gl.forEach((v, i) => gp.geometry.attributes.position.array.set([v[0] * RAD, v[1] * RAD, v[2] * RAD], i * 3)); G.add(gp);
  const r1 = rng(3), NN = 240, node = []; for (let i = 0; i < NN; i++) { const u = r1() * 2 - 1, a = r1() * 6.283, q = Math.sqrt(1 - u * u); node.push([q * Math.cos(a) * RAD * 1.01, u * RAD * 1.01, q * Math.sin(a) * RAD * 1.01, r1()]); }
  const np = points(NN, { size: .75 }); node.forEach((v, i) => np.geometry.attributes.position.array.set(v.slice(0, 3), i * 3)); G.add(np);
  const arc = [], r2 = rng(8); for (let i = 0; i < 70; i++) { const a = node[(r2() * NN) | 0], b = node[(r2() * NN) | 0]; const va = new T.Vector3(a[0], a[1], a[2]), vb = new T.Vector3(b[0], b[1], b[2]); if (va.distanceTo(vb) > RAD * 1.15) continue;
    for (let s = 0; s < 24; s++) { const p1 = va.clone().lerp(vb, s / 24).setLength(RAD * 1.02), p2 = va.clone().lerp(vb, (s + 1) / 24).setLength(RAD * 1.02); arc.push(p1.x, p1.y, p1.z, p2.x, p2.y, p2.z); } }
  const ag = new T.BufferGeometry(); ag.setAttribute('position', new T.BufferAttribute(new Float32Array(arc), 3));
  G.add(new T.LineSegments(ag, new T.LineBasicMaterial({ color: '#b8c4ff', transparent: true, opacity: .6, blending: T.AdditiveBlending })));
  const core = glow(G, p.node || '#8f9cff', RAD * 3.2, .2);
  // far clocks
  const r3 = rng(11), NF = 420, far = []; for (let i = 0; i < NF; i++) { const u = r3() * 2 - 1, a = r3() * 6.283, q = Math.sqrt(1 - u * u), r = RAD * 2.2 + r3() * RAD * 5; far.push([q * Math.cos(a) * r, u * r * .6, q * Math.sin(a) * r, r3()]); }
  const fp = points(NF, { size: .55 }); far.forEach((v, i) => fp.geometry.attributes.position.array.set(v.slice(0, 3), i * 3)); S.add(fp);
  // river band
  const r4 = rng(17), NR = 7000, riv = []; for (let i = 0; i < NR; i++) riv.push([r4() * 6.283, RAD * 1.5 + r4() * RAD * .43, (r4() - .5) * .9, r4()]);
  const rp = points(NR, { size: .12, opacity: .9, color: '#ffd79a' }); S.add(rp);
  stars(S, 2600, 220, { size: .5, seed: 5 });
  // spacetime grid
  const GN = 56, GS = RAD * .27, gv = []; for (let i = 0; i < GN; i++) for (let k = 0; k < GN; k++) gv.push([(i - GN / 2 + .5) * GS, (k - GN / 2 + .5) * GS]);
  const gi = []; for (let i = 0; i < GN; i++) for (let k = 0; k < GN; k++) { const n = i * GN + k; if (k < GN - 1) gi.push(n, n + 1); if (i < GN - 1) gi.push(n, n + GN); }
  const gg = new T.BufferGeometry(); gg.setAttribute('position', new T.BufferAttribute(new Float32Array(GN * GN * 3), 3)); gg.setIndex(gi);
  const grid = new T.LineSegments(gg, new T.LineBasicMaterial({ color: '#6f8cff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false })); S.add(grid);
  const cam = new T.PerspectiveCamera(38, ctx.W / ctx.H, .1, 800); ctx.side(cam, p.side == null ? .08 : p.side);
  const C0 = new T.Color(p.node || '#9fb2ff'), CG = new T.Color(p.flash || '#ffe2a8'), Ct = new T.Color();
  const slow = p.slow ? [cue(p.slow[0]), cue(p.slow[1])] : null, des = p.desync != null ? cue(p.desync) : 1e9;
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    // local clock: runs at the local pace (slows down during "slow")
    const P = slow ? 1 - .92 * sm(slow[0], slow[1], t) : 1;
    const loc = !slow || t < slow[0] ? t : slow[0] + (t - slow[0]) * (.55 + .45 * P);
    G.rotation.y = loc * .18; G.rotation.x = .25;
    const dip = at(p.bend, 3.2) * 4.2 + at(p.crush, 1.6) * 2.2; G.position.y = -dip;
    const st = at(p.stretch, .9) * (1 - at(p.crush, 1) * .6), cr = at(p.crush, 1);
    G.scale.set(1 + st * .45, 1 - cr * .35, 1 + st * .2);
    const dsy = sm(des, des + 1.5, t);
    const na = np.geometry.attributes.color.array; for (let i = 0; i < NN; i++) { const ph = loc + node[i][3] * dsy; const f = Math.exp(-((ph % 1 + 1) % 1) * 5); Ct.copy(C0).lerp(CG, f); const k = .35 + .65 * f; na[i * 3] = Ct.r * k; na[i * 3 + 1] = Ct.g * k; na[i * 3 + 2] = Ct.b * k; }
    np.geometry.attributes.color.needsUpdate = true;
    const vis = at(p.satellites, 3.3) * (slow ? 1 - sm(slow[0] + 1, slow[1], t) * .7 : 1); const fa = fp.geometry.attributes.color.array;
    for (let i = 0; i < NF; i++) { const ph = t * (1 + (far[i][3] - .5) * .9 * dsy) + far[i][3] * dsy * 3; const f = Math.exp(-((ph % 1 + 1) % 1) * 4); const k = vis * (.15 + .85 * f); fa[i * 3] = k; fa[i * 3 + 1] = k * .92; fa[i * 3 + 2] = k * .78; }
    fp.geometry.attributes.color.needsUpdate = true;
    const rv = p.river ? at(p.river[0], 2.3) * (1 - at(p.river[1], 3.5)) : 0; const ra = rp.geometry.attributes.position.array, rc = rp.geometry.attributes.color.array;
    if (rv > 0 || u < .1) for (let i = 0; i < NR; i++) { const [a0, r, h, o] = riv[i]; const a = a0 + t * .55 * (p.river ? 1 - at(p.river[1], 3.5) * .8 : 1); const x = Math.cos(a) * r, z = Math.sin(a) * r;
      ra[i * 3] = x; ra[i * 3 + 1] = h + z * .41 - dip; ra[i * 3 + 2] = z * .91; const k = rv * (.4 + .6 * ((o + t * .3) % 1)); rc[i * 3] = rc[i * 3 + 1] = rc[i * 3 + 2] = k; }
    rp.visible = rv > 0; rp.geometry.attributes.position.needsUpdate = true; rp.geometry.attributes.color.needsUpdate = true;
    grid.material.opacity = .28 * at(p.grid, 2.5); grid.visible = grid.material.opacity > 0;
    if (grid.visible) { const ga = gg.attributes.position.array, depth = 1 + dip * 1.9; for (let n = 0; n < GN * GN; n++) { const [x, z] = gv[n]; const r2 = (x / (1 + st * .6)) ** 2 + z * z; ga[n * 3] = x; ga[n * 3 + 1] = -RAD * 1.42 - depth / (1 + r2 / (RAD * RAD * .83)) * 2.2; ga[n * 3 + 2] = z; } gg.attributes.position.needsUpdate = true; }
    core.material.opacity = .16 + .12 * at(p.bend, 4) + .06 * sm(ctx.t0 + 3, ctx.t0 + 20, t);
    const br = p.bgRamp || [0, 30]; S.background.copy(bg[0]).lerp(bg[1], sm(ctx.t0 + br[0], ctx.t0 + br[1], t) * .9);
    const ca = .5 + u * (p.orbit || .045), cd = (p.dist || 31) - u * .15, gr = at(p.grid, 5);
    cam.position.set(Math.sin(ca) * cd, 6 + 3 * gr, Math.cos(ca) * cd); cam.lookAt(0, -dip * .6 - 1.5 * gr, 0);
  } };
};
