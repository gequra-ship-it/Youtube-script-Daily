// Small reusable scenes (2026-10-14): void (slow star drift, behind data cards and text cards), watch (metal wristwatch close-up),
// clockfield (many clocks across space ticking in step, camera pulls back), river (a river of light across a dark plain),
// cubefield (a field of cubes bent into a gravity well with a chrome ball — heavy: ~180x real time on the render server).
(function () {
  const M = (window.MIYA = window.MIYA || { scenes: {} });

  // void — params: { bg:'#020309', tint:'#140f2e', stars:3000 }
  M.scenes.void = function (ctx, p) {
    const { T } = ctx, S = new T.Scene(); S.background = new T.Color(p.bg || '#020309');
    const st = ctx.stars(S, p.stars || 3000, 200, { seed: 41, size: 1.1 }); const neb = ctx.glow(S, p.tint || '#3b3a8c', 260, .25); neb.position.set(40, 10, -120);
    const cam = new T.PerspectiveCamera(50, ctx.W / ctx.H, .1, 600);
    return { scene: S, camera: cam, draw(t, u) { cam.position.set(0, 0, 0); cam.rotation.set(0, u * .01, 0); st.rotation.y = u * .004; } };
  };

  // shared: a clock head facing +z
  function clockFace(ctx, r, gold) {
    const { T } = ctx, g = new T.Group(), E = ctx.env();
    const metal = new T.MeshStandardMaterial({ color: gold ? '#d9b46a' : '#c9ced8', metalness: 1, roughness: .22, envMap: E, envMapIntensity: 1.2 });
    g.add(new T.Mesh(new T.TorusGeometry(r, r * .11, 24, 96), metal));
    const dial = new T.Mesh(new T.CylinderGeometry(r * .97, r * .97, r * .08, 96), new T.MeshStandardMaterial({ color: '#0b1022', roughness: .55, metalness: .3, envMap: E, envMapIntensity: .4 })); dial.rotation.x = Math.PI / 2; dial.position.z = -r * .05; g.add(dial);
    const tick = new T.MeshStandardMaterial({ color: '#e9e4d6', roughness: .4, metalness: .6, envMap: E });
    for (let i = 0; i < 60; i++) { const big = i % 5 == 0; const b = new T.Mesh(new T.BoxGeometry(r * (big ? .035 : .014), r * (big ? .14 : .06), r * .02), big ? metal : tick); const a = i / 60 * 6.283; b.position.set(Math.sin(a) * r * .83, Math.cos(a) * r * .83, 0); b.rotation.z = -a; g.add(b); }
    const hand = (len, w, mat, z) => { const q = new T.Group(); const m = new T.Mesh(new T.BoxGeometry(w, len, r * .015), mat); m.position.y = len * .42; q.add(m); q.position.z = z; g.add(q); return q; };
    const hh = hand(r * .5, r * .06, metal, r * .02), mh = hand(r * .75, r * .04, metal, r * .035), sh = hand(r * .82, r * .012, new T.MeshStandardMaterial({ color: '#ff7a5a', emissive: '#ff5a3a', emissiveIntensity: .6 }), r * .05);
    return { g, hh, mh, sh, metal };
  }

  // watch — params: { gold:true, side:.12, time:[10,9] (hour, minute at shot start) }
  M.scenes.watch = function (ctx, p) {
    const { T } = ctx, S = new T.Scene(); S.environment = ctx.env(); S.background = new T.Color('#030409');
    const w = clockFace(ctx, 3, p.gold !== false); S.add(w.g);
    const strap = new T.MeshStandardMaterial({ color: '#1b1714', roughness: .85 }); [-1, 1].forEach(s => { const m = new T.Mesh(new T.BoxGeometry(3.2, 7, .5), strap); m.position.set(0, s * 6.6, -.35); S.add(m); });
    const crown = new T.Mesh(new T.CylinderGeometry(.28, .28, .5, 24), w.metal); crown.rotation.z = Math.PI / 2; crown.position.set(3.55, 0, 0); S.add(crown);
    S.add(new T.AmbientLight('#20263a', .4)); const k = new T.SpotLight('#ffe2b0', 900, 60, .5, .6); k.position.set(-8, 10, 14); S.add(k); const rl = new T.PointLight('#6f8cff', 120, 30); rl.position.set(9, -4, 4); S.add(rl);
    const rr = ctx.rng(5); for (let i = 0; i < 26; i++) { const s = ctx.glow(S, i % 3 ? '#ffb860' : '#8fa8ff', 1.5 + rr() * 3, .12 + rr() * .2); s.position.set((rr() - .5) * 60, (rr() - .5) * 34, -25 - rr() * 20); }
    const cam = new T.PerspectiveCamera(30, ctx.W / ctx.H, .1, 300); ctx.side(cam, p.side == null ? .12 : p.side);
    const tm = p.time || [10, 9];
    return { scene: S, camera: cam, draw(t, u) {
      w.sh.rotation.z = -Math.floor(t) / 60 * 6.283; const mins = tm[1] + u / 60; w.mh.rotation.z = -mins / 60 * 6.283; w.hh.rotation.z = -(tm[0] + mins / 60) / 12 * 6.283;
      w.g.rotation.set(-.35 + .05 * Math.sin(u * .3), .28 - .03 * u, 0);
      cam.position.set(1.5 - u * .2, 1.2, 22 - u * .9); cam.lookAt(0, 0, 0);
    } };
  };

  // clockfield — params: { n:140, side:.12, pull:1, bg:['#020309','#140f2e'] }
  // (2026-10-14, after "the clocks feel cut off from the other scenes": same light language as dataglobe / blackhole — solid 3D
  // clocks with a dark smoked body, a glowing gold rim, light-point hour marks and glowing hands, a soft halo each, set in a
  // spiral of clocks with a gold dust river along the arms, navy-violet space and stars. All rims pulse together on every second;
  // the camera starts at one clock and pulls back to show the whole spiral.)
  M.scenes.clockfield = function (ctx, p) {
    const { T, points, stars, glow } = ctx, S = new T.Scene(), E = ctx.env();
    const bg = (p.bg || ['#020309', '#140f2e']).map(c => new T.Color(c)); S.background = bg[0].clone(); S.fog = new T.FogExp2('#06061a', .0042);
    stars(S, 2600, 420, { size: .5, seed: 13 });
    const neb = [['#3a2c8a', 260, .16, [-40, -20, -120]], ['#1d2f7a', 320, .14, [90, 10, -60]], ['#6a3a7a', 180, .08, [10, 30, 60]]];
    neb.forEach(([c, sc, op, ps]) => glow(S, c, sc, op).position.set(ps[0], ps[1], ps[2]));
    const N = p.n || 140, rr = ctx.rng(9), pos = [];
    pos.push([0, 0, 0, .3, 1.1]);   // the hero clock the camera starts on
    for (let i = 1; i < N; i++) { const arm = i % 3, r = 6 + Math.pow(rr(), .7) * 110, a = arm * 2.094 + r * .035 + (rr() - .5) * .5; pos.push([r * Math.cos(a), (rr() - .5) * (4 + r * .07), r * Math.sin(a), rr() * 6.283, .8 + rr() * .5]); }
    const GOLD = new T.Color('#ffc978'), WARM = new T.Color('#fff1d6');
    // parts (unit clock, face along +z, all baked in clock space so one matrix places every part). A real volume, so it still
    // reads as an object when it turns edge-on: deep case with rounded sides and a domed back (lathe), raised bezel, dial recessed
    // inside it, domed crystal, raised hour markers, hands at two heights, crown and bow on top.
    const prof = [[0, -.36], [.5, -.36], [.8, -.32], [.96, -.22], [1.05, -.08], [1.075, .05], [1.06, .15], [1.0, .215], [.95, .2], [.925, .12], [.92, .06]].map(([r, h]) => new T.Vector2(r, h));
    const bodyG = new T.LatheGeometry(prof, 72); bodyG.rotateX(Math.PI / 2);
    const body = new T.MeshStandardMaterial({ color: '#1a1d38', emissive: '#080a22', metalness: 1, roughness: .26, envMap: E, envMapIntensity: .9, side: T.DoubleSide });
    const goldM = new T.MeshStandardMaterial({ color: '#c99a52', metalness: 1, roughness: .22, envMap: E, envMapIntensity: 1.1, emissive: '#3a2408' });
    const crownG = new T.CylinderGeometry(.1, .1, .2, 20); crownG.translate(0, 1.16, 0); const bowG = new T.TorusGeometry(.2, .04, 10, 40); bowG.translate(0, 1.44, 0);
    const rimG = new T.TorusGeometry(.985, .03, 12, 96); rimG.translate(0, 0, .215); const rimM = new T.MeshBasicMaterial({ color: GOLD.clone().multiplyScalar(1.25), transparent: true, blending: T.AdditiveBlending, depthWrite: false });
    const rim2G = new T.TorusGeometry(.91, .01, 8, 96); rim2G.translate(0, 0, .065); const rim2M = new T.MeshBasicMaterial({ color: GOLD.clone().multiplyScalar(1.3), transparent: true, opacity: .6, blending: T.AdditiveBlending, depthWrite: false });
    const secG = new T.BoxGeometry(.022, .8, .012); secG.translate(0, .3, .125); const minG = new T.BoxGeometry(.06, .6, .02); minG.translate(0, .25, .1);
    const handM = new T.MeshBasicMaterial({ color: WARM.clone().multiplyScalar(1.8), transparent: true, blending: T.AdditiveBlending, depthWrite: false });
    const markG = new T.BoxGeometry(.05, .16, .04); const markM = new T.MeshStandardMaterial({ color: '#e8c27a', emissive: '#a8742a', emissiveIntensity: 1.2, metalness: .8, roughness: .3 });
    const domeG = new T.SphereGeometry(1, 40, 10, 0, Math.PI * 2, 0, .42); domeG.rotateX(Math.PI / 2); domeG.translate(0, 0, -Math.cos(.42)); domeG.scale(.93 / Math.sin(.42), .93 / Math.sin(.42), .12 / (1 - Math.cos(.42))); domeG.translate(0, 0, .2);
    const glass = new T.MeshStandardMaterial({ color: '#dfe6ff', metalness: 0, roughness: .04, transparent: true, opacity: .12, envMap: E, envMapIntensity: 2.2, depthWrite: false });
    const bodyI = new T.InstancedMesh(bodyG, body, N), crownI = new T.InstancedMesh(crownG, goldM, N), bowI = new T.InstancedMesh(bowG, goldM, N), rimI = new T.InstancedMesh(rimG, rimM, N), rim2I = new T.InstancedMesh(rim2G, rim2M, N),
      secI = new T.InstancedMesh(secG, handM, N), minI = new T.InstancedMesh(minG, handM, N), markI = new T.InstancedMesh(markG, markM, N * 12), domeI = new T.InstancedMesh(domeG, glass, N);
    // face: dark glass lit from inside (navy centre, violet-blue toward the rim), recessed inside the bezel
    const faceT = ctx.ctex(256, (g, z) => { const r = g.createRadialGradient(z / 2, z / 2, 0, z / 2, z / 2, z / 2); r.addColorStop(0, '#080a1e'); r.addColorStop(.75, '#151a46'); r.addColorStop(.97, '#3a3f8a'); r.addColorStop(1, '#000'); g.fillStyle = r; g.fillRect(0, 0, z, z); });
    const faceG = new T.CircleGeometry(.925, 64); faceG.translate(0, 0, .061); const faceI = new T.InstancedMesh(faceG, new T.MeshBasicMaterial({ map: faceT }), N);
    S.add(bodyI, crownI, bowI, faceI, markI, rimI, rim2I, minI, secI, domeI);
    // hour marks and minute dots as light points (static), halos (one soft sprite-point per clock)
    const MK = 72, mk = points(N * MK, { size: .13, color: '#ffe2b0' }), hal = points(N, { size: 11, opacity: .3, color: '#ffbf70' });
    const ma = mk.geometry.attributes.position.array, mc = mk.geometry.attributes.color.array, ha = hal.geometry.attributes.position.array; S.add(mk, hal);
    const M4 = new T.Matrix4(), Q = new T.Quaternion(), Qh = new T.Quaternion(), V = new T.Vector3(), Sc = new T.Vector3(), E1 = new T.Euler(), Z = new T.Vector3(0, 0, 1), off = new T.Vector3(), pv = new T.Vector3();
    // faces turn (loosely) toward the camera's path above the spiral, so the glowing faces are seen, not the backs
    const ob = new T.Object3D(), QS = pos.map(([x, y, z, o], i) => { ob.position.set(x, y, z); ob.lookAt(Math.sin(.5) * 40 + Math.sin(o * 3) * 25, 45 + Math.cos(o * 2) * 20, Math.cos(.5) * 40 + Math.cos(o * 5) * 25); return ob.quaternion.clone(); });
    const Mm = new T.Matrix4();
    // each clock rocks slowly about its own axis (the turn shows the depth of the case); the hero clock turns a little more
    const AX = pos.map(([, , , o]) => new T.Vector3(Math.sin(o * 7), Math.cos(o * 3), .3 * Math.sin(o * 11)).normalize()), Qw = new T.Quaternion(), Mk = MARKS();
    function MARKS() { const a = []; for (let h = 0; h < 12; h++) { const r = h / 12 * 6.283; a.push(new T.Matrix4().makeRotationZ(-r).setPosition(Math.sin(r) * .76, Math.cos(r) * .76, .08)); } return a; }
    function place(t) { for (let i = 0; i < N; i++) { const [x, y, z, o, s] = pos[i]; Qw.setFromAxisAngle(AX[i], (i ? .35 : .5) * Math.sin(t * .25 + o * 4)); const Qi = QS[i].clone().multiply(Qw); QW[i] = Qi;
      V.set(x, y, z); Sc.set(s, s, s); M4.compose(V, Qi, Sc); [bodyI, crownI, bowI, faceI, rimI, rim2I, domeI].forEach(m => m.setMatrixAt(i, M4));
      for (let h = 0; h < 12; h++) markI.setMatrixAt(i * 12 + h, Mm.multiplyMatrices(M4, Mk[h]));
      for (let k = 0; k < MK; k++) { const hr = k < 12, a = (hr ? k / 12 : (k - 12) / 60) * 6.283, r = hr ? .86 : .87; pv.set(Math.sin(a) * r * s, Math.cos(a) * r * s, .07 * s).applyQuaternion(Qi).add(V);
        ma.set([pv.x, pv.y, pv.z], (i * MK + k) * 3); const c = hr ? 1.6 : .7; mc.set([c, c, c], (i * MK + k) * 3); }
      ha.set([x, y, z], i * 3); }
      [bodyI, crownI, bowI, faceI, rimI, rim2I, domeI, markI].forEach(m => m.instanceMatrix.needsUpdate = true); mk.geometry.attributes.position.needsUpdate = true; }
    const QW = [];
    for (let i = 0; i < N; i++) { const [x, y, z] = pos[i];
      ha.set([x, y, z], i * 3); }
    mk.geometry.attributes.position.needsUpdate = true;
    // gold dust river along the spiral arms
    const ND = 9000, dr = ctx.rng(17), dust = points(ND, { size: .22, opacity: .7, color: '#ffd79a' }), da = dust.geometry.attributes.position.array, dd = []; S.add(dust);
    for (let i = 0; i < ND; i++) dd.push([i % 3, 4 + Math.pow(dr(), .8) * 125, (dr() - .5) * .9, (dr() - .5) * 4, dr()]);
    const core = glow(S, '#ffd8a0', 60, .12), heroGlow = glow(S, '#fff0d0', 5, .35);
    S.add(new T.AmbientLight('#2a2a70', .5)); const kl = new T.DirectionalLight('#ffd9a8', 1.2); kl.position.set(20, 40, 30); S.add(kl); const bl = new T.DirectionalLight('#6f7cff', 1.4); bl.position.set(-30, -10, -20); S.add(bl);
    const cam = new T.PerspectiveCamera(36, ctx.W / ctx.H, .1, 900); ctx.side(cam, p.side == null ? .12 : p.side); const dur = Math.max(1, ctx.t1 - ctx.t0);
    return { scene: S, camera: cam, draw(t, u) {
      place(t); const tick = Math.floor(t) * 6.283 / 60, mn = (t / 60) * 6.283 / 60 + 1.2, beat = Math.exp(-(t % 1) * 5);
      for (let i = 0; i < N; i++) { const [x, y, z, , s] = pos[i]; Sc.set(s, s, s);
        V.set(x, y, z); Qh.setFromAxisAngle(Z, -tick); M4.compose(V, QW[i].clone().multiply(Qh), Sc); secI.setMatrixAt(i, M4);
        Qh.setFromAxisAngle(Z, -mn); M4.compose(V, QW[i].clone().multiply(Qh), Sc); minI.setMatrixAt(i, M4); }
      secI.instanceMatrix.needsUpdate = minI.instanceMatrix.needsUpdate = true;
      rimM.opacity = .55 + .45 * beat; hal.material.opacity = .14 + .16 * beat; heroGlow.material.opacity = .2 + .25 * beat;
      for (let i = 0; i < ND; i++) { const [arm, r, h, w, o] = dd[i]; const a = arm * 2.094 + r * .035 + w * .03 - t * .02 * (60 / (r + 20)); da.set([r * Math.cos(a) + w * Math.sin(a), h * (2 + r * .05) + Math.sin(t * .5 + o * 9) * .3, r * Math.sin(a) - w * Math.cos(a)], i * 3); }
      dust.geometry.attributes.position.needsUpdate = true;
      const k = ctx.sm(0, dur, u) * (p.pull == null ? 1 : p.pull), d = 4.2 + k * 165, ca = .5 + u * .05;
      cam.position.set(Math.sin(ca) * d, 1.2 + k * 70, Math.cos(ca) * d); cam.lookAt(0, 0, 0);
      S.background.copy(bg[0]).lerp(bg[1], .5 + .5 * k);
    } };
  };

  // river — params: { color:'#ffc65a', side:.1, speed:9 }
  M.scenes.river = function (ctx, p) {
    const { T } = ctx, S = new T.Scene(); S.background = new T.Color('#02040c'); S.fog = new T.FogExp2('#050a1c', .012); ctx.stars(S, 2500, 300, { seed: 23 });
    const g = new T.PlaneGeometry(400, 400, 120, 120); g.rotateX(-Math.PI / 2); const P = g.attributes.position;
    for (let i = 0; i < P.count; i++) { const x = P.getX(i), z = P.getZ(i); const rv = Math.exp(-Math.pow(x - 12 * Math.sin(z * .03), 2) / 90); P.setY(i, (Math.sin(x * .05) * Math.cos(z * .04) * 3 + Math.sin(x * .13 + z * .07) * 1.2) * (1 - rv) + 2 - 2.5 * rv); }
    g.computeVertexNormals(); S.add(new T.Mesh(g, new T.MeshStandardMaterial({ color: '#0b0f1a', roughness: .95 }))); S.add(new T.HemisphereLight('#2a3278', '#000000', .6));
    const N = 26000, rr = ctx.rng(21), pts = ctx.points(N, { size: 2.2, atten: false, opacity: .9, fog: true }), ph = new Float32Array(N), of = new Float32Array(N * 2), col = pts.geometry.attributes.color.array, c0 = new T.Color(p.color || '#ffc65a'), c1 = new T.Color('#fff6dc'), ct = new T.Color();
    for (let i = 0; i < N; i++) { ph[i] = rr(); of[i * 2] = (rr() - .5) * 7; of[i * 2 + 1] = rr() * 1.2; ct.copy(c0).lerp(c1, rr() * .8); col.set([ct.r, ct.g, ct.b], i * 3); }
    S.add(pts); const hg = ctx.glow(S, '#ffcf8a', 260, .35); hg.position.set(0, 6, -210);
    const cam = new T.PerspectiveCamera(42, ctx.W / ctx.H, .1, 600); ctx.side(cam, p.side == null ? .1 : p.side); const a = pts.geometry.attributes.position.array, SP = p.speed || 9;
    return { scene: S, camera: cam, draw(t, u) {
      for (let i = 0; i < N; i++) { const z = 150 - ((ph[i] * 360 + u * SP) % 360); a[i * 3] = 12 * Math.sin(z * .03) + of[i * 2]; a[i * 3 + 1] = -.2 + of[i * 2 + 1] * .4; a[i * 3 + 2] = z; }
      pts.geometry.attributes.position.needsUpdate = true; cam.position.set(12 * Math.sin((60 - u * 2) * .03) + 5, 5.5, 60 - u * 2); cam.lookAt(0, 1, -120);
    } };
  };

  // cubefield — params: { nx:48, nz:32, depth:9, bend:cue, crush:cue, slow:[cue,cue], side:.12 }   (keep nx*nz small: heavy)
  M.scenes.cubefield = function (ctx, p) {
    const { T, sm, cue } = ctx, S = new T.Scene(); S.background = new T.Color('#02030c'); S.fog = new T.Fog('#02030c', 45, 110); S.environment = ctx.env();
    const NX = p.nx || 48, NZ = p.nz || 32, N = NX * NZ, box = new T.BoxGeometry(.88, 1, .88); box.translate(0, -.5, 0);
    const cubes = new T.InstancedMesh(box, new T.MeshStandardMaterial({ roughness: .6, metalness: .3, envMapIntensity: .06 }), N); S.add(cubes);
    const base = []; for (let i = 0; i < NX; i++) for (let k = 0; k < NZ; k++) base.push([i - NX / 2 + .5, k - NZ / 2 + .5]);
    const ball = new T.Mesh(new T.SphereGeometry(2.3, 96, 64), new T.MeshStandardMaterial({ color: '#fff', metalness: 1, roughness: .06, envMapIntensity: 1.5 })); S.add(ball);
    const ring = new T.Mesh(new T.TorusGeometry(3.8, .03, 12, 220), new T.MeshBasicMaterial({ color: ctx.ACC })); S.add(ring);
    S.add(new T.AmbientLight('#1d2350', .12)); const kd = new T.DirectionalLight('#c8d4ff', .22); kd.position.set(-20, 30, 10); S.add(kd);
    const pl = new T.PointLight('#ffb860', 520, 32, 1.7); S.add(pl); const bl = new T.PointLight('#6f8cff', 70, 70, 1.4); bl.position.set(22, 8, -14); S.add(bl);
    const cam = new T.PerspectiveCamera(36, ctx.W / ctx.H, .1, 300); ctx.side(cam, p.side == null ? .12 : p.side);
    const M4 = new T.Matrix4(), P3 = new T.Vector3(), S3 = new T.Vector3(), Q0 = new T.Quaternion(), Cc = new T.Color(), NAVY = new T.Color('#0a1030'), BLUE = new T.Color('#6f8cff'), GOLD = new T.Color(ctx.ACC);
    const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + d, ctx.t); const slow = p.slow ? [cue(p.slow[0]), cue(p.slow[1])] : null, DP = p.depth || 9;
    return { scene: S, camera: cam, draw(t, u) {
      ctx.t = t; const depth = 1.5 + at(p.bend, 2) * DP * .45 + at(p.crush, .8) * DP * .55; const sl = slow ? 1 - sm(slow[0], slow[1], t) * .94 : 1;
      const ph = (slow && t > slow[0] ? (slow[0] - ctx.t0) + (t - slow[0]) * sl : u) * 1.7;
      for (let n = 0; n < N; n++) { const [x, z] = base[n]; const r2 = x * x + z * z; const well = -depth / (1 + r2 / 16), wave = .5 * Math.sin(.33 * Math.sqrt(r2) - ph) * Math.exp(-r2 / 1000) * sl;
        P3.set(x, well + wave, z); S3.set(1, 1.2 + Math.max(0, -well) * .15, 1); M4.compose(P3, Q0, S3); cubes.setMatrixAt(n, M4);
        const h = Math.min(1, Math.max(0, -well / (DP + .5))); Cc.copy(NAVY).lerp(BLUE, Math.min(1, h * 1.3) * .45).lerp(GOLD, Math.max(0, h - .45) * 1.8); cubes.setColorAt(n, Cc); }
      cubes.instanceMatrix.needsUpdate = true; cubes.instanceColor.needsUpdate = true;
      const by = 2.8 - depth * .6 + .2 * Math.sin(u * 1.2 * sl); ball.position.set(0, by, 0); ring.position.copy(ball.position); ring.rotation.set(1.2, 0, .3 + u * .3 * sl); pl.position.set(0, by - 1.6, 0);
      const ca = -.7 + u * .07, cr = 36 - u * 1.2, ch = 20 - u * .9; cam.position.set(Math.sin(ca) * cr, ch, Math.cos(ca) * cr); cam.lookAt(0, -2, 0);
    } };
  };
})();
