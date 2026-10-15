// parkbeast — a bulky 1850s-style dinosaur restoration statue (horn on the nose) on a small island in a misty park lake at dusk
// (stage), drawn in LOOK C (cine_spec 3A, user decision 2026-10-15): real 3D form, surfaces drawn with light.
//  statue (subject): ONE merged mesh (kit.body trunk/tail/neck/head + four pillar legs, toes, horn and eye bulges), dark solid body
//    with a warm fresnel outline, faint warm mesh lines and a few hundred warm points;
//  world: island and far shore as dark ground with glowing height contours; trees (lumpy canopy blobs on trunks), boulders, reeds and
//    the plinth dark with a cool outline and sparse cool points; the lake is a dark mirror (mirrored, clipped copies of the outlines
//    under a dark rippling surface); dusk sky dark navy-violet with the low sun glowing behind the trees; faint mist, motes, stars.
//  The far-shore trees that would sit behind the text column (left third) at any moment of the shot are left out (seek-safe:
//    decided once from the camera path).
// params (cues): { horn: cue (camera closes in on the head, the horn tip glints), years: cue (the outline turns more golden),
//   wrong: cue (the statue's outline dims and a bright cyan wire-and-points ghost of a slimmer, tail-up modern animal sweeps over it
//   from tail to head), side:.13 }
(window.MIYA = window.MIYA || { scenes: {} }).scenes.parkbeast = function (ctx, p) {
  const { T, sm, cue } = ctx, K = window.MIYA.kit, R = ctx.R, LC = K.lookC;
  const S = new T.Scene(); S.background = new T.Color('#03030b');
  const SUN = new T.Vector3(-.70, .085, -.71).normalize();
  const WARM = '#ffc460', COOLC = '#5f78ff', GHOST = '#7ae8ff';
  // ---------- deterministic 3D value noise ----------
  const hsh = (x, y, z) => { const h = Math.sin(x * 127.1 + y * 311.7 + z * 74.7) * 43758.5453; return h - Math.floor(h); };
  function vn(x, y, z) { const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), fx = x - xi, fy = y - yi, fz = z - zi;
    const u = fx * fx * (3 - 2 * fx), v = fy * fy * (3 - 2 * fy), w = fz * fz * (3 - 2 * fz), L = (a, b, q) => a + (b - a) * q;
    const c = (i, j, k) => hsh(xi + i, yi + j, zi + k);
    return L(L(L(c(0, 0, 0), c(1, 0, 0), u), L(c(0, 1, 0), c(1, 1, 0), u), v), L(L(c(0, 0, 1), c(1, 0, 1), u), L(c(0, 1, 1), c(1, 1, 1), u), v), w); }
  const fbm = (x, y, z) => vn(x, y, z) * .5 + vn(x * 2.1, y * 2.1, z * 2.1) * .25 + vn(x * 4.3, y * 4.3, z * 4.3) * .125 + vn(x * 8.7, y * 8.7, z * 8.7) * .0625;
  // ---------- sky dome (dusk, look C: deep navy zenith, violet band, the sun's warm glow low behind the trees) ----------
  const skyFrag = `uniform vec3 sd; uniform float k; varying vec3 vP;
    void main(){ vec3 d=normalize(vP); float y=abs(d.y); float sa=max(0.,dot(normalize(vec3(d.x,0.,d.z)+1e-5),normalize(vec3(sd.x,0.,sd.z))));
      vec3 zen=vec3(.003,.004,.018), mid=vec3(.018,.014,.05), hor=mix(vec3(.04,.025,.075),vec3(.30,.11,.05),pow(sa,10.));
      vec3 c=mix(hor, mid, smoothstep(0.,.16,y)); c=mix(c,zen,smoothstep(.14,.6,y));
      c+=vec3(1.,.45,.17)*pow(sa,40.)*exp(-max(y,0.)*22.)*1.5*k; c*=mix(1.,.45,1.-k);
      gl_FragColor=vec4(c,1.); }`;
  const skyVert = 'varying vec3 vP; void main(){ vP=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }';
  const skyMat = () => new T.ShaderMaterial({ side: T.BackSide, depthWrite: false, fog: false, uniforms: { sd: { value: SUN }, k: { value: 1 } }, vertexShader: skyVert, fragmentShader: skyFrag });
  const dome = new T.Mesh(new T.SphereGeometry(420, 48, 24), skyMat()); S.add(dome);
  const envS = new T.Scene(); envS.add(new T.Mesh(new T.SphereGeometry(100, 32, 16), skyMat()));
  const ENV = R ? new T.PMREMGenerator(R).fromScene(envS, 0).texture : null;
  const mirror = new T.Group(); mirror.scale.y = -1; S.add(mirror);
  // look C materials; the mirrored copies drop everything above the water plane (world y > 0)
  const clipIt = m => { m.fragmentShader = m.fragmentShader.replace('void main(){', (m.fragmentShader.includes('varying vec3 vW;') ? '' : 'varying vec3 vW; ') + 'void main(){ if(vW.y>.005) discard;'); return m; };
  const rimM = (o, clip) => { const m = LC.rim(o); return clip ? clipIt(m) : m; };
  const contM = (o, clip) => { const m = LC.contour(o); return clip ? clipIt(m) : m; };
  // ---------- geometry helpers ----------
  function curve(keys, col) { return s => { s = Math.min(1, Math.max(0, s)); let i = 0; while (i < keys.length - 2 && s > keys[i + 1][0]) i++;
    const k0 = keys[Math.max(0, i - 1)], k1 = keys[i], k2 = keys[i + 1], k3 = keys[Math.min(keys.length - 1, i + 2)], h = k2[0] - k1[0], x = (s - k1[0]) / h;
    const m1 = (k2[col] - k0[col]) / Math.max(1e-6, k2[0] - k0[0]) * h, m2 = (k3[col] - k1[col]) / Math.max(1e-6, k3[0] - k1[0]) * h, x2 = x * x, x3 = x2 * x;
    return (2 * x3 - 3 * x2 + 1) * k1[col] + (x3 - 2 * x2 + x) * m1 + (-2 * x3 + 3 * x2) * k2[col] + (x3 - x2) * m2; }; }
  // vertical sweep (legs, trunks): f(s) -> [cx, y, cz, rx, rz]; s=0 bottom (closed with a cap), s=1 top
  function sweepY(n, m, f, capTop) { const pos = [], uv = [], idx = [];
    for (let i = 0; i <= n; i++) { const s = i / n, [cx, y, cz, rx, rz] = f(s); for (let j = 0; j < m; j++) { const a = j / m * Math.PI * 2; pos.push(cx + Math.cos(a) * rx, y, cz + Math.sin(a) * rz); uv.push(j / m, s); } }
    for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) { const a = i * m + j, b = i * m + (j + 1) % m, c = (i + 1) * m + j, d = (i + 1) * m + (j + 1) % m; idx.push(a, b, c, b, d, c); }
    const f0 = f(0), cb = pos.length / 3; pos.push(f0[0], f0[1] - .02, f0[2]); uv.push(.5, 0); for (let j = 0; j < m; j++) idx.push(cb, (j + 1) % m, j);
    if (capTop) { const f1 = f(1), ct = pos.length / 3; pos.push(f1[0], f1[1] + .02, f1[2]); uv.push(.5, 1); for (let j = 0; j < m; j++) idx.push(ct, n * m + j, n * m + (j + 1) % m); }
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new T.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals(); return g; }
  function merge(list) { let nv = 0, ni = 0; list = list.map(g => { g = g.index ? g : g.toNonIndexed(); if (!g.index) { const a = []; for (let i = 0; i < g.attributes.position.count; i++) a.push(i); g.setIndex(a); } if (!g.attributes.normal) g.computeVertexNormals(); if (!g.attributes.uv) g.setAttribute('uv', new T.Float32BufferAttribute(new Float32Array(g.attributes.position.count * 2), 2)); nv += g.attributes.position.count; ni += g.index.count; return g; });
    const P = new Float32Array(nv * 3), N = new Float32Array(nv * 3), U = new Float32Array(nv * 2), I = new Uint32Array(ni); let o = 0, oi = 0;
    list.forEach(g => { P.set(g.attributes.position.array, o * 3); N.set(g.attributes.normal.array, o * 3); U.set(g.attributes.uv.array, o * 2); const ix = g.index.array; for (let i = 0; i < ix.length; i++) I[oi + i] = ix[i] + o; o += g.attributes.position.count; oi += ix.length; });
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(P, 3)); g.setAttribute('normal', new T.BufferAttribute(N, 3)); g.setAttribute('uv', new T.BufferAttribute(U, 2)); g.setIndex(new T.BufferAttribute(I, 1)); return g; }
  // ---------- the statue: ONE mesh ----------
  const LB = 10, BY = 2.72;   // body length (tail tip -> snout), height of the body axis above the plinth
  // s, half-width, half-height, axis y offset, axis z offset (tail curls to one side and drops to the ground)
  const KB = [[0, .05, .05, -2.05, 1.35], [.08, .2, .22, -1.95, 1.2], [.17, .4, .43, -1.6, .8], [.27, .74, .78, -.95, .3], [.37, 1.16, 1.18, -.32, .06],
    [.47, 1.48, 1.46, -.02, 0], [.58, 1.56, 1.62, .14, 0], [.66, 1.45, 1.6, .2, 0], [.74, 1.08, 1.14, .12, 0], [.8, .76, .82, .02, 0],
    [.85, .7, .78, -.04, 0], [.91, .6, .64, -.14, 0], [.96, .42, .44, -.24, 0], [.985, .26, .3, -.28, 0], [1, .06, .12, -.3, 0]];
  const bw = curve(KB, 1), bh = curve(KB, 2), by = curve(KB, 3), bz = curve(KB, 4);
  function statueGeo() {
    const b = K.body({ length: LB, seg: 220, ring: 72, belly: .28, ridge: .07, width: s => bw(s) * (1 + .025 * Math.sin(s * 260) * sm(.74, .78, s) * (1 - sm(.84, .87, s))), height: bh });
    b.deform((s, th, base, k) => { const sn = Math.sin(th), g = Math.exp(-Math.pow((sn + .22) / .07, 2)) * sm(.875, .9, s) * (1 - sm(.99, 1, s));   // mouth groove
      const fold = .035 * Math.exp(-Math.pow((s - .47) / .012, 2)) * (sn < .3 ? 1 : .3);   // skin fold behind the shoulder... and the hip
      const fold2 = .03 * Math.exp(-Math.pow((s - .7) / .01, 2));
      const sh = -(g * .09 + fold + fold2);
      return [0, by(s) + base[k * 3 + 1] * sh, bz(s) + base[k * 3 + 2] * sh]; });
    const parts = [b.geo];
    const X = s => (s - .5) * LB;
    // legs: thick pillars, slightly splayed, elbows out like a lizard; rings in horizontal planes from the plinth up into the body
    const RK = [[0, .46], [.05, .54], [.11, .5], [.2, .37], [.32, .35], [.5, .41], [.68, .5], [.86, .62], [1, .6]], rr = curve(RK, 1);
    [[.7, 1, .95, 1.32, .12], [.7, -1, .95, 1.32, .12], [.42, 1, 1.0, 1.38, -.05], [.42, -1, 1.0, 1.38, -.05]].forEach(([s0, sd, zt, zf, fx], li) => {
      const x0 = X(s0), top = by(s0) - .15, rear = li >= 2, sc = rear ? 1.12 : 1;
      parts.push(sweepY(40, 40, s => { const y = -BY + s * (top + BY), q = Math.pow(1 - s, 1.4), knee = Math.sin(Math.PI * s) * .1;
        const r = rr(s) * sc; return [x0 + fx * q + (s < .12 ? .12 * (1 - s / .12) : 0), y, sd * (zt + (zf - zt) * q + knee), r * (s < .12 ? 1.18 : 1), r]; }));
      // toes: three blunt claws at the front of each foot
      for (let k = -1; k <= 1; k++) { const tg = new T.SphereGeometry(.14 * sc, 14, 10); tg.scale(1.6, .75, 1); tg.translate(x0 + fx + .5 * sc + (k === 0 ? .08 : 0), -BY + .1, sd * zf + k * .24 * sc); parts.push(tg); }
    });
    // horn on the nose (lathe), leaning forward
    const hs = .955, hp = [[0, -.12], [.15, -.05], [.15, .06], [.12, .2], [.085, .32], [.045, .43], [.012, .5], [0, .51]].map(([r, h]) => new T.Vector2(r, h));
    const horn = new T.LatheGeometry(hp, 32); horn.scale(1.55, 1.7, 1.55); horn.rotateZ(-.5); horn.translate(X(hs), by(hs) + bh(hs) * .82, 0); parts.push(horn);
    // eye bulges with a brow ridge
    [1, -1].forEach(sd => { const s = .9, e = new T.SphereGeometry(.085, 16, 12); e.translate(X(s), by(s) + bh(s) * .42, sd * bw(s) * .86); parts.push(e);
      const br = new T.SphereGeometry(.12, 16, 10); br.scale(1.6, .45, .9); br.translate(X(s) - .03, by(s) + bh(s) * .62, sd * bw(s) * .78); parts.push(br); });
    const g = merge(parts); g.translate(0, BY, 0); return g;
  }
  const SG = statueGeo();  // ---------- camera path (also used once at build time to keep the text column clear of trees) ----------
  const SIDE = p.side == null ? .13 : p.side, ROT = -.12;
  const A = (c, d, t) => c == null ? 0 : sm(cue(c), cue(c) + d, t);
  function pose(t, cam) { const u = t - ctx.t0, hornK = A(p.horn, 3.5, t) * (1 - A(p.years, 3, t)), yrs = A(p.years, 3, t), wr = A(p.wrong, 2.5, t);
    const a = .5 + u * .021, d = 26 - 7 * sm(0, 7, u) - 4 * hornK + 2 * yrs + 3.5 * wr, hgt = 3.1 + .9 * sm(0, 12, u) + 1.4 * wr;
    const tx = 1.0 + 2.2 * hornK - 1.0 * wr, ty = 2.6 + .4 * hornK + .3 * wr;
    cam.position.set(Math.sin(a) * d + tx * .4, hgt, Math.cos(a) * d); cam.lookAt(tx, ty, 0); cam.updateMatrixWorld();
    return { hornK, yrs, wr }; }
  const cam = new T.PerspectiveCamera(33, ctx.W / ctx.H, .1, 1200); ctx.side(cam, SIDE);
  // ---------- the statue ----------
  const statue = new T.Mesh(SG, rimM({ base: '#040207', rim: WARM, k: 2.8, far: 90, pow: 6.5 }));
  statue.rotation.y = ROT; statue.position.y = .87; S.add(statue);
  const dressS = LC.dress(statue, { points: 700, size: .055, lines: .02, color: '#ffb85a', pointColor: '#ffe3a8', opacity: .8 });
  { const rs = K.rng(37), nv = SG.attributes.position.count, ix = []; for (let i = 0; i < 700; i++) ix.push((rs() * nv) | 0); dressS.points.geometry.setIndex(ix); }   // scattered, not lined up on one ring
  const hornGlow = ctx.glow(statue, '#ffd38a', 1.6, 0); hornGlow.position.set((.955 - .5) * LB + .42, by(.955) + bh(.955) * .82 + .76 + BY, 0);
  // ---------- island, plinth, shore, boulders, trees, reeds ----------
  const islR = a => 9.2 + 1.6 * (vn(Math.cos(a) * 1.4 + 3, Math.sin(a) * 1.4, 1.7) - .5) * 2;
  function islandGeo() { const NR = 44, NA = 128, pos = [], uv = [], idx = [];
    for (let i = 0; i <= NR; i++) for (let j = 0; j < NA; j++) { const a = j / NA * 6.283, q = i / NR, r = q * islR(a) * 1.18, x = Math.cos(a) * r, z = Math.sin(a) * r, e = r / islR(a);
      let y = .62 * (1 - sm(.55, 1.05, e)) + .12 * (fbm(x * .35, 0, z * .35) - .5) * 2 * sm(.15, .5, e) - .5 * sm(.95, 1.18, e) - .05; pos.push(x, y, z); uv.push(x * .08, z * .08); }
    for (let i = 0; i < NR; i++) for (let j = 0; j < NA; j++) { const a = i * NA + j, b = i * NA + (j + 1) % NA, c = (i + 1) * NA + j, d = (i + 1) * NA + (j + 1) % NA; idx.push(a, c, b, b, c, d); }
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new T.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals(); return g; }
  const IG = islandGeo();
  const plG = new T.CylinderGeometry(1, 1.06, 1, 40, 4); plG.translate(0, .5, 0); { const P = plG.attributes.position; for (let i = 0; i < P.count; i++) { const x = P.getX(i), y = P.getY(i), z = P.getZ(i), n = fbm(x * 1.5 + 9, y * 1.5, z * 1.5); const s = 1 + (n - .5) * .45; P.setXYZ(i, x * s, y + (y > .9 ? (n - .5) * .12 : 0), z * s); } plG.scale(5.4, .34, 3.0); plG.computeVertexNormals(); }
  // lumpy sphere (boulders, canopy blobs): indexed, so the outline stays smooth
  function lump(seed, sq, amt) { const g = new T.SphereGeometry(1, 22, 14), P = g.attributes.position;
    for (let i = 0; i < P.count; i++) { const x = P.getX(i), y = P.getY(i), z = P.getZ(i), s = 1 - amt / 2 + amt * fbm(x * 1.3 + seed, y * 1.3, z * 1.3); P.setXYZ(i, x * s, y * s * sq, z * s); } g.computeVertexNormals(); return g; }
  const bG = lump(2, .7, .5), canG = lump(7, .85, .55);
  const rb = K.rng(17), BOUL = []; for (let i = 0; i < 9; i++) { const a = rb() * 6.283, r = 4.6 + rb() * 3.2; BOUL.push([Math.cos(a) * r * 1.15, .2, Math.sin(a) * r * .9, .25 + rb() * .45, rb() * 6]); }
  function shoreGeo() { const NR = 30, NA = 160, pos = [], uv = [], idx = [];
    for (let i = 0; i <= NR; i++) for (let j = 0; j < NA; j++) { const a = j / NA * 6.283, r = 36 + Math.pow(i / NR, 1.6) * 170 + 6 * (vn(Math.cos(a) * 2 + 7, Math.sin(a) * 2, 3) - .5) * 2, x = Math.cos(a) * r, z = Math.sin(a) * r;
      const y = -.4 + 1.2 * sm(0, .12, i / NR) + 2.5 * sm(.2, 1, i / NR) * fbm(x * .03, 1, z * .03); pos.push(x, y, z); uv.push(x * .05, z * .05); }
    for (let i = 0; i < NR; i++) for (let j = 0; j < NA; j++) { const a = i * NA + j, b = i * NA + (j + 1) % NA, c = (i + 1) * NA + j, d = (i + 1) * NA + (j + 1) % NA; idx.push(a, c, b, b, c, d); }
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new T.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals(); return g; }
  const SHG = shoreGeo();
  const trunkG = sweepY(8, 10, s => [Math.sin(s * 2.3) * .15, s, 0, .3 - s * .17, .3 - s * .17], true);
  const rt = K.rng(51), TREES0 = [];
  [[2.8, -7.4, .6]].forEach(([x, z, s]) => TREES0.push([x, .3, z, s, 1]));   // on the island, behind
  const SA = Math.atan2(SUN.z, SUN.x); for (let i = 0; i < 52; i++) { const a = i / 52 * 6.283 + rt() * .1, da = Math.abs(Math.atan2(Math.sin(a - SA), Math.cos(a - SA))); if (da < .16) continue; const r = 52 + rt() * 30; TREES0.push([Math.cos(a) * r, 1.4, Math.sin(a) * r, (1.2 + rt() * 1.1) * (da < .4 ? .7 : 1), 0]); }
  // keep the left text column clear: drop trees whose canopy enters the left 37 % of the frame at any time of the shot
  const TREES = (() => { if (ctx.VERT) return TREES0; const tc = new T.PerspectiveCamera(33, ctx.W / ctx.H, .1, 1200); ctx.side(tc, SIDE); tc.updateProjectionMatrix();
    const v = new T.Vector3(), rgt = new T.Vector3(), up = new T.Vector3(), drop = new Set(), t0 = ctx.t0, t1 = ctx.t1 == null ? t0 + 30 : ctx.t1;
    for (let t = t0; t <= t1 + .01; t += .5) { pose(t, tc); rgt.setFromMatrixColumn(tc.matrixWorld, 0); up.setFromMatrixColumn(tc.matrixWorld, 1);
      TREES0.forEach(([x, y, z, s], i) => { const h = 4.2 * s, cy = y + h * .78 + 2.4 * s;
        for (const [dx, dy] of [[3, 0], [3, 2.6], [3, -2.6], [2, -4.5]]) { v.set(x, cy, z).addScaledVector(rgt, dx * s).addScaledVector(up, dy * s).project(tc);
          if (v.z < 1 && v.x < -.26 && v.x > -1.4 && v.y > -1.1 && v.y < 1.1) drop.add(i); } }); }
    return TREES0.filter((_, i) => !drop.has(i)); })();
  const M4 = new T.Matrix4(), Q = new T.Quaternion(), E = new T.Euler(), V3 = new T.Vector3();
  const BLOB = [];   // canopy blob matrices (shared by the world and its mirror)
  TREES.forEach(([x, y, z, s], i) => { const h = 4.2 * s, rq = K.rng(100 + i), nb = 16;
    for (let b = 0; b < nb; b++) { const u1 = rq() * 2 - 1, a = rq() * 6.283, q = Math.sqrt(1 - u1 * u1), rr2 = Math.pow(rq(), .5), sc = (.75 + rq() * .6) * s * (b === 0 ? 1.6 : 1);
      BLOB.push([new T.Vector3(x + Math.cos(a) * q * rr2 * 2.1 * s, y + h * .8 + 2.0 * s + u1 * rr2 * 2.1 * s, z + Math.sin(a) * q * rr2 * 2.1 * s), new T.Euler(rq() * 6.28, rq() * 6.28, rq() * 6.28), sc, i]); } });
  const COOL = { base: '#020310', rim: COOLC };
  function addWorld(par, clip) {
    const st = clip ? new T.Mesh(SG, rimM({ base: '#040207', rim: WARM, k: 2.2, far: 90, pow: 4.5 }, true)) : null;
    if (st) { st.rotation.y = ROT; st.position.y = .87; par.add(st); }
    const isl = new T.Mesh(IG, contM({ base: '#03040c', line: '#4a5fd0', rim: '#0c1238', spacing: .13, width: .05, far: 70, k: .75 }, clip)); par.add(isl);
    const pl = new T.Mesh(plG, rimM(Object.assign({ k: .8, far: 70, pow: 7 }, COOL), clip)); pl.rotation.y = ROT; pl.position.y = .52; par.add(pl);
    const bm = new T.InstancedMesh(bG, rimM(Object.assign({ k: 1.1, far: 60, pow: 3.5 }, COOL), clip), BOUL.length);
    BOUL.forEach(([x, y, z, s, o], i) => { M4.compose(V3.set(x, y, z), Q.setFromEuler(E.set(o, o * 2, 0)), new T.Vector3(s, s, s)); bm.setMatrixAt(i, M4); }); par.add(bm);
    par.add(new T.Mesh(SHG, contM({ base: '#03040b', line: '#3d4fb8', rim: '#0a0f30', spacing: .42, width: .05, far: 130, k: .6 }, clip)));
    const BL = BLOB, cm = new T.InstancedMesh(canG, rimM({ base: '#02030c', rim: COOLC, k: 1.5, far: 150, pow: 3.5 }, clip), BL.length);
    BL.forEach(([pp, e, sc], k) => { M4.compose(pp, Q.setFromEuler(e), new T.Vector3(sc, sc, sc)); cm.setMatrixAt(k, M4); }); par.add(cm);
    const tr = new T.InstancedMesh(trunkG, rimM({ base: '#02030c', rim: COOLC, k: .9, far: 150, pow: 3 }, clip), TREES.length);
    TREES.forEach(([x, y, z, s], i) => { M4.compose(V3.set(x, y, z), Q.identity(), new T.Vector3(s * 1.1, 4.2 * s, s * 1.1)); tr.setMatrixAt(i, M4); }); par.add(tr);
    if (!clip) {   // reeds along the island's waterline
      const NRd = 420, reedG = new T.ConeGeometry(.03, 1, 5, 1); reedG.translate(0, .5, 0); const rd = new T.InstancedMesh(reedG, rimM({ base: '#02030c', rim: '#7088ff', k: .8, far: 50, pow: 2.5 }), NRd), rr3 = K.rng(71);
      for (let i = 0; i < NRd; i++) { const a = rr3() * 6.283, r = islR(a) * (1.0 + (rr3() - .5) * .14), hh = .5 + rr3() * 1.0; M4.compose(V3.set(Math.cos(a) * r, -.1, Math.sin(a) * r), Q.setFromEuler(E.set((rr3() - .5) * .4, 0, (rr3() - .5) * .4)), new T.Vector3(1, hh, 1)); rd.setMatrixAt(i, M4); }
      par.add(rd); }
  }
  addWorld(S, false); addWorld(mirror, true);
  // sparse cool points on the canopies and boulders (world only)
  { const rp = K.rng(61), cp = canG.attributes.position, pts = [];
    BLOB.forEach(([pp, e, sc]) => { M4.compose(pp, Q.setFromEuler(e), new T.Vector3(sc, sc, sc)); for (let j = 0; j < 2; j++) { V3.fromBufferAttribute(cp, (rp() * cp.count) | 0).applyMatrix4(M4); pts.push(V3.x, V3.y, V3.z); } });
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pts, 3));
    S.add(new T.Points(g, new T.PointsMaterial({ color: '#8fa6ff', size: .12, transparent: true, opacity: .35, blending: T.AdditiveBlending, depthWrite: false, fog: false }))); }
  // ---------- the lake: a dark mirror (the mirrored outlines show through a dark, gently rippling surface) ----------
  const ripN = K.normalMap(K.noise(512, { seed: 91, octaves: 5, sx: 1, sy: 3 }), 3); ripN.repeat.set(26, 26);
  const water = new T.Mesh(new T.PlaneGeometry(600, 600), new T.MeshStandardMaterial({ color: '#020309', roughness: .08, metalness: 0, normalMap: ripN, normalScale: new T.Vector2(.22, .22), transparent: true, opacity: .42, envMap: ENV, envMapIntensity: 1.1, depthWrite: true }));
  water.rotation.x = -Math.PI / 2; S.add(water);
  // ---------- mist, motes, early stars, the sun's glow ----------
  const mT = K.tex(K.noise(256, { seed: 5, octaves: 4 }), true); mT.repeat.set(2, 2);
  const mist = new T.Mesh(new T.PlaneGeometry(140, 140), new T.MeshBasicMaterial({ map: mT, color: '#5d5a92', transparent: true, opacity: .1, blending: T.AdditiveBlending, depthWrite: false, fog: false }));
  mist.rotation.x = -Math.PI / 2; mist.position.y = .45; S.add(mist);
  const motes = K.snow(S, { n: 600, box: [40, 12, 40], size: .06, color: '#ffcf96', opacity: .45, fall: .05, seed: 13 });
  const stars = ctx.stars(S, 900, 380, { size: .9, opacity: .5, seed: 19 }); { const a = stars.geometry.attributes.position.array; for (let i = 0; i < a.length; i += 3) a[i + 1] = 50 + Math.abs(a[i + 1]) * .8; }
  const sunGlow = ctx.glow(S, '#ff9a50', 150, .3); sunGlow.position.copy(SUN).multiplyScalar(300); sunGlow.position.y = 5;
  const sunGlow2 = ctx.glow(S, '#ffb070', 40, .35); sunGlow2.position.copy(SUN).multiplyScalar(300); sunGlow2.position.y = 3;
  // ---------- the ghost: a slimmer, tail-up modern animal in a different tone (cyan): bright edge + wire + dense points ----------
  const KG = [[0, .03, .04, .55, 0], [.15, .16, .2, .5, 0], [.32, .4, .5, .35, 0], [.44, .78, 1.05, .15, 0], [.55, .95, 1.22, 0, 0], [.66, .88, 1.08, -.25, 0],
    [.75, .55, .68, -.4, 0], [.83, .35, .42, -.5, 0], [.9, .32, .44, -.62, 0], [.96, .2, .27, -.72, 0], [1, .04, .07, -.78, 0]];
  const gw = curve(KG, 1), gh = curve(KG, 2), gy = curve(KG, 3), LG = 11.5, GY = 3.05;
  const ghostG = (() => { const b = K.body({ length: LG, seg: 110, ring: 28, belly: .2, width: gw, height: gh }); b.deform((s) => [0, gy(s), 0]);
    const parts = [b.geo], X = s => (s - .5) * LG;
    [[.47, 1, .55, 1.0], [.47, -1, .55, 1.0], [.72, 1, .45, .62], [.72, -1, .45, .62]].forEach(([s0, sd, z0, sc]) => { const x0 = X(s0), top = gy(s0);
      parts.push(sweepY(18, 14, s => { const y = -GY + s * (top + GY), r = (s < .08 ? .28 : .2 + .32 * sm(.35, 1, s)) * sc, kn = Math.sin(Math.PI * s * 1.2) * .3 * (sc < .8 ? -1 : 1); return [x0 + kn, y, sd * z0, r, r * .85]; })); });
    const g = merge(parts); g.translate(0, GY, 0); return g; })();
  const GU = { col: { value: new T.Color(GHOST) }, op: { value: 0 }, rev: { value: -9 }, wire: { value: 0 } };
  const ghostMat = wire => new T.ShaderMaterial({ uniforms: GU, transparent: true, depthWrite: false, depthTest: false, blending: T.AdditiveBlending, wireframe: wire,
    defines: wire ? { WIRE: 1 } : {},
    vertexShader: 'varying vec3 vN; varying vec3 vV; varying float vX; void main(){ vX=position.x; vec4 mv=modelViewMatrix*vec4(position,1.); vN=normalize(normalMatrix*normal); vV=-mv.xyz; gl_Position=projectionMatrix*mv; }',
    fragmentShader: 'uniform vec3 col; uniform float op,rev; varying vec3 vN; varying vec3 vV; varying float vX; void main(){ float f=pow(1.-abs(dot(normalize(vN),normalize(vV))),2.2); float m=smoothstep(rev,rev-1.,vX); float edge=exp(-pow((vX-rev)/.3,2.));\n#ifdef WIRE\n gl_FragColor=vec4(col*(.16+.25*f+edge*.8)*op*m,1.);\n#else\n gl_FragColor=vec4(col*(f*1.7+.03+edge*f*2.5)*op*m,1.);\n#endif\n }' });
  const ghost = new T.Mesh(ghostG, ghostMat(false)); ghost.add(new T.Mesh(ghostG, ghostMat(true)));
  ghost.position.set(.3, 1.0, 0); ghost.rotation.y = ROT; S.add(ghost);
  const gpA = ghostG.attributes.position.array, NGp = 1100, gpts = ctx.points(NGp, { size: .11, color: '#c8f6ff' }), gpp = gpts.geometry.attributes.position.array, gpx = new Float32Array(NGp), rg2 = K.rng(83);
  for (let i = 0; i < NGp; i++) { const v = (rg2() * (gpA.length / 3)) | 0; gpp.set([gpA[v * 3], gpA[v * 3 + 1], gpA[v * 3 + 2]], i * 3); gpx[i] = gpA[v * 3]; }
  gpts.material.depthTest = false; ghost.add(gpts);
  const C_WARM = new T.Color(WARM), C_GOLD = new T.Color('#ffd27a'), C_DIM = new T.Color('#c9a070');
  return { scene: S, camera: cam, draw(t, u) {
    const { hornK, yrs, wr } = pose(t, cam);
    // statue outline: brighter on the horn close-up, more golden at "years", dims under the ghost at "wrong"
    const su = statue.material.uniforms; su.k.value = (2.8 + .5 * hornK + .4 * yrs) * (1 - .45 * wr); su.rim.value.copy(C_WARM).lerp(C_GOLD, yrs * .6).lerp(C_DIM, wr * .5);
    dressS.lines.material.opacity = .02 * (1 - .5 * wr); dressS.points.material.opacity = .8 * (1 - .55 * wr);
    hornGlow.material.opacity = .55 * hornK * (.75 + .25 * Math.sin(t * 2.4));
    dome.material.uniforms.k.value = 1 - .3 * wr; sunGlow.material.opacity = .3 * (1 - .4 * wr); sunGlow2.material.opacity = .35 * (1 - .4 * wr);
    ripN.offset.set(t * .004, t * .011);
    mT.offset.set(t * .006, t * .002); mist.material.opacity = .1 * (.8 + .2 * Math.sin(t * .3));
    motes.update(t, [0, 4, 0]);
    // ghost sweeps in tail -> head, then holds, breathing faintly
    GU.op.value = wr * (.85 + .15 * Math.sin(t * 2.2)); GU.rev.value = -7 + 15 * A(p.wrong, 3.2, t);
    const pc = gpts.geometry.attributes.color.array; for (let i = 0; i < NGp; i++) { const v = wr * (gpx[i] < GU.rev.value ? 1 : 0) * (.35 + .65 * Math.max(0, Math.sin(t * 2.5 + i * 1.7))); pc[i * 3] = pc[i * 3 + 1] = pc[i * 3 + 2] = v; }
    gpts.geometry.attributes.color.needsUpdate = true; ghost.visible = wr > .001;
  } };
};
