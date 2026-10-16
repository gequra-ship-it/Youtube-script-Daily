// parkbeast — a bulky 1850s-style dinosaur restoration statue (concrete, horn on the nose) on a small island in a misty park lake
// at dusk (stage). The statue never moves: ONE merged mesh (kit.body trunk/tail/neck/head + four pillar legs, toes, horn and eye
// bulges merged into the same BufferGeometry). Weathered concrete via a triplanar shader patch (colour stains, drip streaks, moss
// on the upper surfaces, cracks and sculpted scales as a derivative bump), low sun behind it (warm rim, long shadow), cool sky fill,
// planar reflection in the lake (mirrored, clipped copies), ground mist, drifting warm motes, tree line in fog.
// params (cues): { horn: cue (camera closes in on the head, faint warm glint on the horn), years: cue (light turns a little more
//   golden / old), wrong: cue (the warm light cools and a faint glowing ghost of a slimmer, tail-up animal shape sweeps over the
//   statue from tail to head), side:.13 }
(window.MIYA = window.MIYA || { scenes: {} }).scenes.parkbeast = function (ctx, p) {
  const { T, sm, cue } = ctx, K = window.MIYA.kit, R = ctx.R;
  const S = new T.Scene();
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + d, ctx.t);
  if (R) { R.shadowMap.enabled = true; R.shadowMap.type = T.PCFShadowMap; R.localClippingEnabled = true; }
  const CLIP = [new T.Plane(new T.Vector3(0, -1, 0), 0.0)];   // mirrored copies keep only what lies under the water plane
  const SUN = new T.Vector3(-.70, .085, -.71).normalize();
  // stable in motion: tiled textures get max anisotropy; fine normal detail fades with view distance (no shimmer in far pixels)
  const ANI = R ? R.capabilities.getMaxAnisotropy() : 4, aniso = (...ts) => ts.forEach(x => { x.anisotropy = ANI; x.needsUpdate = true; });
  const NFADE = (n, f, lo) => T.ShaderChunk.normal_fragment_maps.replace('mapN.xy *= normalScale;', `mapN.xy *= normalScale * mix(1., ${lo.toFixed(2)}, smoothstep(${n.toFixed(1)}, ${f.toFixed(1)}, length(vViewPosition)));`);
  const fadeN = (m, n, f, lo, key) => { m.onBeforeCompile = sh => { sh.fragmentShader = sh.fragmentShader.replace('#include <normal_fragment_maps>', NFADE(n, f, lo)); }; m.customProgramCacheKey = () => key; return m; };
  // ---------- deterministic 3D value noise ----------
  const hsh = (x, y, z) => { const h = Math.sin(x * 127.1 + y * 311.7 + z * 74.7) * 43758.5453; return h - Math.floor(h); };
  function vn(x, y, z) { const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), fx = x - xi, fy = y - yi, fz = z - zi;
    const u = fx * fx * (3 - 2 * fx), v = fy * fy * (3 - 2 * fy), w = fz * fz * (3 - 2 * fz), L = (a, b, q) => a + (b - a) * q;
    const c = (i, j, k) => hsh(xi + i, yi + j, zi + k);
    return L(L(L(c(0, 0, 0), c(1, 0, 0), u), L(c(0, 1, 0), c(1, 1, 0), u), v), L(L(c(0, 0, 1), c(1, 0, 1), u), L(c(0, 1, 1), c(1, 1, 1), u), v), w); }
  const fbm = (x, y, z) => vn(x, y, z) * .5 + vn(x * 2.1, y * 2.1, z * 2.1) * .25 + vn(x * 4.3, y * 4.3, z * 4.3) * .125 + vn(x * 8.7, y * 8.7, z * 8.7) * .0625;
  // ---------- sky dome (dusk: warm glow low at the sun, violet above, deep navy at the zenith) ----------
  const skyFrag = `uniform vec3 sd; uniform float k; varying vec3 vP; varying vec3 vW; uniform float mir;
    void main(){ vec3 d=normalize(vP); float y=abs(d.y); float sa=max(0.,dot(normalize(vec3(d.x,0.,d.z)+1e-5),normalize(vec3(sd.x,0.,sd.z))));
      vec3 zen=vec3(.006,.010,.032), mid=vec3(.040,.034,.085), hor=vec3(.30,.13,.075);
      vec3 c=mix(hor*mix(.22,1.,pow(sa,2.5)), mid, smoothstep(0.,.22,y)); c=mix(c,zen,smoothstep(.18,.75,y));
      c+=vec3(1.,.48,.20)*pow(sa,30.)*exp(-max(y,0.)*16.)*1.6*k; c*=mix(1.,.35,1.-k);
      gl_FragColor=vec4(c,1.); }`;
  const skyVert = 'varying vec3 vP; varying vec3 vW; void main(){ vP=normalize(position); vW=(modelMatrix*vec4(position,1.)).xyz; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }';
  const skyMat = mir => new T.ShaderMaterial({ side: T.BackSide, depthWrite: false, fog: false, uniforms: { sd: { value: SUN }, k: { value: 1 }, mir: { value: mir } }, vertexShader: skyVert, fragmentShader: skyFrag });
  const dome = new T.Mesh(new T.SphereGeometry(420, 48, 24), skyMat(0)); S.add(dome);
  // environment for reflections = the same sky
  const envS = new T.Scene(); envS.add(new T.Mesh(new T.SphereGeometry(100, 32, 16), skyMat(0)));
  const ENV = R ? new T.PMREMGenerator(R).fromScene(envS, 0).texture : null; S.environment = ENV;
  S.fog = new T.FogExp2('#1d1a28', .021);
  const mirror = new T.Group(); mirror.scale.y = -1; S.add(mirror);
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
  // 1850s-style restoration in the spirit of the Crystal Palace Park Iguanodon (1854), not a replica: a heavy quadruped with a
  // round barrel ribcage (slight sag between shoulders and hips, low row of scutes along the spine), a neck visibly narrower than
  // the chest, a long low lizard head (flat-topped skull tapering to the snout, closed mouth line running back under the eye and
  // turning down at the corner, eye in a raised bony socket under a heavy brow, small horn on top near the snout tip), heavy pillar
  // legs and a thick tapering tail lying and curling on the plinth. The spine is a 3D curve; each cross-section is built in a
  // frame that keeps "up" vertical; the head takes more of s so its features get enough rings.
  // s, x, y, z (axis, metres above the plinth top, x toward the snout), half-width, half-height
  const KB = [[0, -3.25, .13, 2.05, .1, .09], [.07, -4.3, .19, 1.62, .22, .18], [.13, -4.78, .31, .85, .34, .3], [.19, -4.35, .58, .18, .48, .45],
    [.245, -3.55, 1.3, .03, .68, .7], [.3, -2.75, 2.2, 0, .96, 1.02],
    [.37, -1.6, 3.05, 0, 1.3, 1.38], [.44, -.45, 2.86, 0, 1.45, 1.4], [.51, .65, 2.78, 0, 1.5, 1.42], [.58, 1.6, 2.72, 0, 1.38, 1.4], [.64, 2.35, 2.6, 0, 1.0, 1.06],
    [.69, 2.95, 2.4, 0, .64, .7], [.74, 3.5, 2.18, 0, .5, .5], [.78, 3.95, 2.07, 0, .55, .6],
    [.82, 4.35, 2.12, 0, .62, .62], [.87, 4.85, 1.98, 0, .53, .53], [.92, 5.35, 1.88, 0, .42, .42], [.965, 5.8, 1.8, 0, .31, .32], [.99, 6.05, 1.76, 0, .2, .22],
    [.997, 6.12, 1.75, 0, .12, .13], [1, 6.15, 1.745, 0, 0, 0]];
  const cx = curve(KB, 1), cy = curve(KB, 2), cz = curve(KB, 3), bw = curve(KB, 4), bh = curve(KB, 5);
  const frame = s => { const e = .002, a = new T.Vector3(cx(s - e), cy(s - e), cz(s - e)), b = new T.Vector3(cx(s + e), cy(s + e), cz(s + e)), tg = b.sub(a).normalize();
    const up = new T.Vector3(0, 1, 0).addScaledVector(tg, -tg.y).normalize(); return { c: new T.Vector3(cx(s), cy(s), cz(s)), up, sd: new T.Vector3().crossVectors(tg, up) }; };
  const G2 = (a, b) => Math.exp(-a * a - b * b);
  // cross-section offset (outward, metres) for the sculpted features: mouth groove, eye sockets, brows, nostrils, spine scutes, folds
  function relief(s, th) {
    const c = Math.cos(th), sn = Math.sin(th), side = Math.abs(c); let d = 0;
    const m0 = -.1 - .16 * (1 - sm(.815, .87, s));
    d -= .085 * Math.exp(-Math.pow((sn - m0) / .055, 2)) * sm(.808, .826, s) * (1 - sm(.993, 1, s)) * sm(.5, .8, side);
    const ds = (s - .838) / .011, dv = (sn - .4) / .12, r = Math.hypot(ds, dv);
    d += (.05 * Math.exp(-r * r / 2.6) + .06 * Math.exp(-Math.pow((r - 1.05) / .35, 2)) - .045 * Math.exp(-Math.pow((r - .62) / .17, 2)) + .045 * Math.exp(-r * r / .16)) * sm(.35, .6, side);
    d += (.09 * G2((s - .834) / .02, (sn - .66) / .11) + .04 * G2((s - .815) / .03, (sn - .74) / .12)) * sm(.2, .5, side);
    d += .035 * G2((s - .985) / .009, (sn - .45) / .16) * sm(.3, .6, side);
    const a = .07 * sm(.2, .32, s) * (1 - sm(.7, .8, s)), ph = cx(s) / .42;
    d += a * (Math.pow(Math.max(0, Math.sin(ph * 6.2832)), 3) * .8 + .25) * Math.exp(-Math.pow((th - Math.PI / 2) / .11, 2));
    d -= .025 * Math.exp(-Math.pow((s - .64) / .018, 2)) * sm(.6, -.2, sn) + .03 * Math.exp(-Math.pow((s - .375) / .01, 2)) * (sn < .2 ? 1 : .2);
    return d;
  }
  function statueGeo() {
    const b = K.body({ length: 10, seg: 300, ring: 80, belly: 0, ridge: 0, width: bw, height: bh });
    const FR = []; for (let i = 0; i <= 900; i++) FR.push(frame(i / 900));
    b.deform((s, th, base, k) => { const sc = Math.min(1, Math.max(0, s)), w = bw(sc), h = bh(sc), c = Math.cos(th), sn = Math.sin(th), hk = sm(.77, .83, sc);
      const pu = 1 - .42 * hk, q = 1 - .18 * hk;
      let yl = sn >= 0 ? h * Math.pow(sn, pu) : h * sn * (1 - .07 * (1 - hk)), zl = w * Math.sign(c) * Math.pow(Math.abs(c), q);
      const d = relief(sc, th); yl += sn * d; zl += c * d;
      const f = FR[Math.round(sc * 900)];
      return [f.c.x + f.up.x * yl + f.sd.x * zl - base[k * 3], f.c.y + f.up.y * yl + f.sd.y * zl - base[k * 3 + 1], f.c.z + f.up.z * yl + f.sd.z * zl - base[k * 3 + 2]]; });
    const parts = [b.geo];
    // legs: heavy straight pillars (no waist), a little flare at the foot, leaning in so the top stays inside the body; rings in horizontal planes
    const RK = [[0, .6], [.05, .62], [.12, .53], [.3, .49], [.5, .51], [.7, .56], [.88, .6], [1, .56]], rr = curve(RK, 1);
    [[.58, 1, 1.0], [.58, -1, 1.0], [.375, 1, 1.0], [.375, -1, 1.0]].forEach(([s0, sd, zf], li) => {
      const x0 = cx(s0), top = cy(s0) - .1, rear = li >= 2, sc = rear ? 1.1 : 1;
      parts.push(sweepY(36, 40, s => { const r = rr(s) * sc; return [x0 + (rear ? -.06 : .08) * s, -.14 + s * (top + .14), sd * (zf - .38 * s * s), r * (1 + .1 * (1 - sm(0, .14, s))), r]; }, true));
      for (let k = -1; k <= 1; k++) { const tg = new T.SphereGeometry(.15 * sc, 14, 10); tg.scale(1.5, .72, 1.05); tg.translate(x0 + .5 * sc + (k === 0 ? .06 : 0) - .04 * Math.abs(k), .09, sd * zf + k * .26 * sc); parts.push(tg); }
    });
    // small horn on top of the snout near the tip (lathe), leaning forward
    const hs = .955, hp = [[0, -.12], [.16, -.05], [.16, .06], [.13, .2], [.09, .32], [.05, .42], [.015, .5], [0, .51]].map(([r, h]) => new T.Vector2(r, h));
    const horn = new T.LatheGeometry(hp, 28); horn.scale(.72, .6, .66); horn.rotateZ(-.45); horn.translate(cx(hs), cy(hs) + bh(hs) * .93, 0); parts.push(horn);
    return merge(parts);
  }
  const SG = statueGeo();
  // ---------- concrete: triplanar colour / streaks / moss / bump, rim glow ----------
  const CS = 1024, colC = document.createElement('canvas'), hC = document.createElement('canvas'); colC.width = colC.height = hC.width = hC.height = CS;
  const cg = colC.getContext('2d'), hg = hC.getContext('2d');
  cg.fillStyle = '#8d877b'; cg.fillRect(0, 0, CS, CS);
  const n1 = K.noise(512, { seed: 11, octaves: 6 }), n2 = K.noise(512, { seed: 23, octaves: 3, sx: 1, sy: 1 });
  cg.globalCompositeOperation = 'multiply'; cg.globalAlpha = .55; cg.drawImage(n1, 0, 0, CS, CS); cg.globalAlpha = .4; cg.drawImage(n2, 0, 0, CS, CS);
  cg.globalCompositeOperation = 'source-over'; cg.globalAlpha = 1;
  const r1 = K.rng(5); for (let i = 0; i < 9000; i++) { const x = r1() * CS, y = r1() * CS, s = .6 + r1() * 2.2, d = r1() < .55; cg.fillStyle = d ? `rgba(40,36,30,${.25 + r1() * .4})` : `rgba(210,205,190,${.15 + r1() * .3})`; cg.beginPath(); cg.arc(x, y, s, 0, 6.283); cg.fill(); }   // aggregate pits and grains
  for (let i = 0; i < 70; i++) { const x = r1() * CS, y = r1() * CS, rad = 20 + r1() * 90, gr = cg.createRadialGradient(x, y, 0, x, y, rad); const c = r1() < .5 ? '60,52,38' : '120,110,85'; gr.addColorStop(0, `rgba(${c},${.18 + r1() * .2})`); gr.addColorStop(1, `rgba(${c},0)`); cg.fillStyle = gr; cg.fillRect(x - rad, y - rad, rad * 2, rad * 2); }   // stains
  // height: grain + sculpted scales + cracks
  hg.fillStyle = '#808080'; hg.fillRect(0, 0, CS, CS); hg.globalAlpha = .55; hg.drawImage(K.noise(512, { seed: 31, octaves: 6 }), 0, 0, CS, CS); hg.globalAlpha = 1;
  for (let y = 0, row = 0; y < CS + 30; y += 22, row++) for (let x = (row % 2) * 13; x < CS + 30; x += 26) { const jx = x + (r1() - .5) * 6, jy = y + (r1() - .5) * 6, gr = hg.createRadialGradient(jx, jy, 0, jx, jy, 13); gr.addColorStop(0, 'rgba(255,255,255,.22)'); gr.addColorStop(.75, 'rgba(255,255,255,.06)'); gr.addColorStop(1, 'rgba(0,0,0,.22)'); hg.fillStyle = gr; hg.beginPath(); hg.arc(jx, jy, 13, 0, 6.283); hg.fill(); }
  for (let c = 0; c < 26; c++) { let x = r1() * CS, y = r1() * CS, a = r1() * 6.283; const n = 30 + (r1() * 70 | 0), w = .8 + r1() * 1.8; hg.strokeStyle = 'rgba(0,0,0,.95)'; cg.strokeStyle = 'rgba(25,22,18,.85)'; hg.lineWidth = w + 1; cg.lineWidth = w;
    hg.beginPath(); cg.beginPath(); hg.moveTo(x, y); cg.moveTo(x, y); for (let k = 0; k < n; k++) { a += (r1() - .5) * .9; x += Math.cos(a) * 5; y += Math.sin(a) * 5; hg.lineTo(x, y); cg.lineTo(x, y); } hg.stroke(); cg.stroke(); }
  const tC = K.tex(colC, true), tH = K.tex(hC, false), tN = K.normalMap(hC, 2.6);
  // streak texture: vertical drips (sampled stretched on the side projections)
  const stC = document.createElement('canvas'); stC.width = 512; stC.height = 256; const sg = stC.getContext('2d'); sg.fillStyle = '#808080'; sg.fillRect(0, 0, 512, 256);
  for (let i = 0; i < 260; i++) { const x = r1() * 512, w = 1 + r1() * 7, l = 30 + r1() * 220, y = r1() * 256, gr = sg.createLinearGradient(0, y, 0, y + l); const d = r1() < .7; gr.addColorStop(0, d ? 'rgba(20,18,14,.5)' : 'rgba(230,225,210,.3)'); gr.addColorStop(1, 'rgba(128,128,128,0)'); sg.fillStyle = gr; sg.fillRect(x, y, w, l); }
  const tS = K.tex(stC, false); const tM = K.tex(K.noise(256, { seed: 77, octaves: 5 }), false); aniso(tC, tH, tN, tS, tM);
  const U = { tN: { value: tN }, tC: { value: tC }, tH: { value: tH }, tS: { value: tS }, tM: { value: tM }, rimK: { value: .35 }, sunV: { value: new T.Vector3() }, rimC: { value: new T.Color('#ffb36a') }, wet: { value: 0 } };
  function concrete(clip, noRim) {   // noRim: the plinth (its flat top seen at a grazing angle must not glow)
    const m = new T.MeshStandardMaterial({ color: '#ffffff', roughness: .92, metalness: 0, envMapIntensity: .55 }); if (noRim) m.defines = { NO_RIM: '' };
    if (clip) m.clippingPlanes = CLIP;
    m.onBeforeCompile = sh => { Object.assign(sh.uniforms, U);
      sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vOP; varying vec3 vON; varying vec3 vN0; varying vec3 vN1; varying vec3 vN2;').replace('#include <begin_vertex>', '#include <begin_vertex>\nvOP=position; vON=normal; vN0=normalMatrix[0]; vN1=normalMatrix[1]; vN2=normalMatrix[2];');
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>
        varying vec3 vOP; varying vec3 vON; varying vec3 vN0; varying vec3 vN1; varying vec3 vN2; uniform sampler2D tN,tC,tH,tS,tM; uniform float rimK; uniform vec3 sunV,rimC; float gH;
        vec3 tw(){ vec3 b=pow(abs(normalize(vON)),vec3(4.)); return b/(b.x+b.y+b.z); }
        vec3 pnab(vec3 sp, vec3 sn, vec2 dH, float fd){ vec3 sx=dFdx(sp), sy=dFdy(sp); vec3 r1=cross(sy,sn), r2=cross(sn,sx); float det=dot(sx,r1)*fd; vec3 gr=sign(det)*(dH.x*r1+dH.y*r2); return normalize(abs(det)*sn-gr); }`)
        .replace('#include <map_fragment>', `vec3 B=tw(); vec3 N0=normalize(vON); vec2 ux=vOP.zy*.42, uy=vOP.xz*.42, uz=vOP.xy*.42;
          vec3 cc=texture2D(tC,ux).rgb*B.x+texture2D(tC,uy).rgb*B.y+texture2D(tC,uz).rgb*B.z;
          float st=texture2D(tS,vec2(vOP.z*.3,vOP.y*.11)).r*B.x+texture2D(tS,vec2(vOP.x*.3,vOP.y*.11)).r*B.z+.5*B.y;
          float mn=texture2D(tM,(abs(N0.y)>.5?uy:(abs(N0.x)>abs(N0.z)?ux:uz))*.55).r;
          cc*=mix(.55,1.25,st); cc*=mix(.62,1.,smoothstep(.1,1.6,vOP.y));        // drips, grime splashed up from the ground
          cc*=mix(1.,.6,smoothstep(-.2,-.7,N0.y));                                    // dirt under the belly
          float moss=smoothstep(.55,.95,N0.y+mn*.5-.2)*smoothstep(.42,.6,mn);        // moss on the top surfaces
          float moss2=smoothstep(.6,.7,mn)*smoothstep(1.4,.5,vOP.y);                    // and near the ground
          float lich=smoothstep(.24,.14,mn)*.7;                                    // pale lichen spots
          cc=mix(cc,vec3(.16,.2,.07)*(.6+mn),max(moss,moss2)*.85); cc=mix(cc,vec3(.62,.6,.42),lich*.5);
          diffuseColor.rgb*=cc;`)
        .replace('#include <roughnessmap_fragment>', 'float roughnessFactor = roughness;')
        .replace('#include <normal_fragment_maps>', `{ vec3 N0=normalize(vON), Bw=tw(); vec2 ux=vOP.zy*.42, uy=vOP.xz*.42, uz=vOP.xy*.42;
      vec3 tx=texture2D(tN,ux).xyz*2.-1., ty=texture2D(tN,uy).xyz*2.-1., tz=texture2D(tN,uz).xyz*2.-1.;
      float nf=mix(1.,.3,smoothstep(9.,34.,length(vViewPosition))); tx.xy*=nf; ty.xy*=nf; tz.xy*=nf;
      tx=vec3(tx.xy+N0.zy,abs(tx.z)*N0.x); ty=vec3(ty.xy+N0.xz,abs(ty.z)*N0.y); tz=vec3(tz.xy+N0.xy,abs(tz.z)*N0.z);
      vec3 wn=normalize(tx.zyx*Bw.x+ty.xzy*Bw.y+tz.xyz*Bw.z); normal=normalize(mat3(vN0,vN1,vN2)*wn); }`)
        .replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
          #ifndef NO_RIM
          { float fr=pow(1.-max(dot(normal,normalize(vViewPosition)),0.),3.5);
            float side=smoothstep(-.15,.85,dot(normalize(normal.xy+1e-4),normalize(sunV.xy+1e-4)));   // only the edges on the sun's side of the silhouette
            totalEmissiveRadiance+=rimC*fr*rimK*1.5*side*(.35+.65*smoothstep(-.2,.6,-sunV.z)); }
          #endif`);
    };
    m.customProgramCacheKey = () => 'parkbeast-concrete' + (clip ? '-c' : '') + (noRim ? '-n' : '');
    return m;
  }
  const statue = new T.Mesh(SG, concrete(false)); statue.castShadow = statue.receiveShadow = true;
  const ROT = -.12; statue.rotation.y = ROT;
  // ---------- island, plinth rocks, shore, reeds, trees ----------
  const grassC = document.createElement('canvas'); grassC.width = grassC.height = 512; const gg = grassC.getContext('2d'); gg.fillStyle = '#4a5a28'; gg.fillRect(0, 0, 512, 512);
  gg.globalCompositeOperation = 'multiply'; gg.globalAlpha = .6; gg.drawImage(K.noise(512, { seed: 41, octaves: 6 }), 0, 0); gg.globalAlpha = 1; gg.globalCompositeOperation = 'source-over';
  const r2 = K.rng(9); for (let i = 0; i < 9000; i++) { const x = r2() * 512, y = r2() * 512, l = 8 + r2() * 16, b = (r2() - .5) * l * .8;   // soft curved blades lying in all directions (no spikes)
    gg.strokeStyle = `rgba(${45 + r2() * 55 | 0},${58 + r2() * 55 | 0},${24 + r2() * 22 | 0},${.18 + r2() * .3})`; gg.lineWidth = 1.2 + r2(); gg.lineCap = 'round'; gg.beginPath(); gg.moveTo(x, y); gg.quadraticCurveTo(x + b * .3, y - l * .6, x + b, y - l); gg.stroke(); }
  const grassT = K.tex(grassC, true, [10, 10]), grassN = K.normalMap(K.noise(256, { seed: 43, octaves: 5 }), 4); grassN.repeat.set(10, 10); aniso(grassT, grassN);
  const grassMat = clip => { const m = fadeN(new T.MeshLambertMaterial({ map: grassT, normalMap: grassN, normalScale: new T.Vector2(.9, .9), color: '#dcd8bc' }), 6, 30, .15, 'pb-grass' + (clip ? '-c' : '')); if (clip) m.clippingPlanes = CLIP; return m; };
  const islR = a => 9.2 + 1.6 * (vn(Math.cos(a) * 1.4 + 3, Math.sin(a) * 1.4, 1.7) - .5) * 2;
  function islandGeo() { const NR = 44, NA = 128, eMax = 1.18, pos = [], uv = [], idx = [];
    for (let i = 0; i <= NR; i++) for (let j = 0; j < NA; j++) { const a = j / NA * 6.283, q = i / NR, r = q * islR(a) * eMax, x = Math.cos(a) * r, z = Math.sin(a) * r, e = r / islR(a);
      let y = .62 * (1 - sm(.55, 1.05, e)) + .12 * (fbm(x * .35, 0, z * .35) - .5) * 2 * sm(.15, .5, e) - .5 * sm(.95, 1.18, e) - .05; pos.push(x, y, z); uv.push(x * .08, z * .08); }
    for (let i = 0; i < NR; i++) for (let j = 0; j < NA; j++) { const a = i * NA + j, b = i * NA + (j + 1) % NA, c = (i + 1) * NA + j, d = (i + 1) * NA + (j + 1) % NA; idx.push(a, b, c, b, d, c); }
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new T.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals(); return g; }
  const IG = islandGeo();
  // a low rough stone plinth the statue stands on (raised slab with broken edges)
  const plG = new T.CylinderGeometry(1, 1.06, 1, 40, 4); plG.translate(0, .5, 0); { const P = plG.attributes.position; for (let i = 0; i < P.count; i++) { const x = P.getX(i), y = P.getY(i), z = P.getZ(i), n = fbm(x * 1.5 + 9, y * 1.5, z * 1.5); const s = 1 + (n - .5) * .45; P.setXYZ(i, x * s, y + (y > .9 ? (n - .5) * .12 : 0), z * s); } plG.scale(5.4, .34, 3.0); plG.computeVertexNormals(); }
  const rockC = document.createElement('canvas'); rockC.width = rockC.height = 256; const rg = rockC.getContext('2d'); rg.fillStyle = '#5b574f'; rg.fillRect(0, 0, 256, 256); rg.globalCompositeOperation = 'multiply'; rg.drawImage(K.noise(256, { seed: 61, octaves: 6 }), 0, 0); rg.globalCompositeOperation = 'source-over';
  const rockT = K.tex(rockC, true, [3, 1]), rockN = K.normalMap(K.noise(256, { seed: 63, octaves: 6 }), 5); rockN.repeat.set(3, 1); aniso(rockT, rockN);
  const rockMat = clip => { const m = fadeN(new T.MeshStandardMaterial({ map: rockT, normalMap: rockN, roughness: .95, color: '#b8b2a6', envMapIntensity: .4 }), 8, 30, .3, 'pb-rock' + (clip ? '-c' : '')); if (clip) m.clippingPlanes = CLIP; return m; };
  // boulders around the plinth
  const bG = new T.IcosahedronGeometry(1, 3); { const P = bG.attributes.position; for (let i = 0; i < P.count; i++) { const x = P.getX(i), y = P.getY(i), z = P.getZ(i), s = .75 + .5 * fbm(x * 1.3 + 2, y * 1.3, z * 1.3); P.setXYZ(i, x * s, y * s * .85, z * s); } bG.computeVertexNormals(); }
  const rb = K.rng(17), BOUL = []; for (let i = 0; i < 9; i++) { const a = rb() * 6.283, r = 4.6 + rb() * 3.2; BOUL.push([Math.cos(a) * r * 1.15, .42, Math.sin(a) * r * .9, .32 + rb() * .4, rb() * 6]); }
  // shore bank ring around the lake
  function shoreGeo() { const NR = 30, NA = 160, pos = [], uv = [], idx = [];
    for (let i = 0; i <= NR; i++) for (let j = 0; j < NA; j++) { const a = j / NA * 6.283, r = 36 + Math.pow(i / NR, 1.6) * 170 + 6 * (vn(Math.cos(a) * 2 + 7, Math.sin(a) * 2, 3) - .5) * 2, x = Math.cos(a) * r, z = Math.sin(a) * r;
      const y = -.4 + 1.2 * sm(0, .12, i / NR) + 2.5 * sm(.2, 1, i / NR) * fbm(x * .03, 1, z * .03); pos.push(x, y, z); uv.push(x * .05, z * .05); }
    for (let i = 0; i < NR; i++) for (let j = 0; j < NA; j++) { const a = i * NA + j, b = i * NA + (j + 1) % NA, c = (i + 1) * NA + j, d = (i + 1) * NA + (j + 1) % NA; idx.push(a, b, c, b, d, c); }
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new T.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals(); return g; }
  const SHG = shoreGeo();
  // trees: lumpy canopy blobs (displaced icosahedra) on tapered trunks; island trees + a ring along the far shore
  const blobG = new T.PlaneGeometry(1, 1);
  const leafC = document.createElement('canvas'); leafC.width = leafC.height = 256; const lg = leafC.getContext('2d'); const r3 = K.rng(29);
  for (let i = 0; i < 190; i++) { const a = r3() * 6.283, rr = Math.pow(r3(), .7) * 100, x = 128 + Math.cos(a) * rr, y = 128 + Math.sin(a) * rr * .9, sz = 9 + r3() * 12;   // broad leaf clumps (small single leaves crawl in motion)
    lg.fillStyle = `rgb(${30 + r3() * 45 | 0},${42 + r3() * 50 | 0},${16 + r3() * 18 | 0})`; lg.beginPath(); lg.ellipse(x, y, sz, sz * .45, r3() * 6.283, 0, 6.283); lg.fill(); }
  const leafT = K.tex(leafC, true); leafT.wrapS = leafT.wrapT = T.ClampToEdgeWrapping;
  const leafMat = clip => { const m = new T.MeshLambertMaterial({ map: leafT, alphaTest: .5, alphaToCoverage: true, side: T.DoubleSide, color: '#a0aa8c', emissive: '#06080a' }); if (clip) m.clippingPlanes = CLIP; return m; };
  const barkMat = clip => { const m = new T.MeshLambertMaterial({ color: '#2a221b' }); if (clip) m.clippingPlanes = CLIP; return m; };
  const trunkG = sweepY(8, 10, s => [Math.sin(s * 2.3) * .15, s, 0, .3 - s * .17, .3 - s * .17], true);
  const rt = K.rng(51), TREES = [];
  [[-7.6, -2.2, .75], [-6.6, 2.6, .6], [2.8, -7.4, .7]].forEach(([x, z, s]) => TREES.push([x, .3, z, s]));   // on the island, behind
  const SA = Math.atan2(SUN.z, SUN.x); for (let i = 0; i < 52; i++) { const a = i / 52 * 6.283 + rt() * .1, da = Math.abs(Math.atan2(Math.sin(a - SA), Math.cos(a - SA))); if (da < .16) continue; const r = 52 + rt() * 30; TREES.push([Math.cos(a) * r, 1.4, Math.sin(a) * r, (1.2 + rt() * 1.1) * (da < .4 ? .7 : 1)]); }
  function addWorld(par, clip) {
    const st = clip ? new T.Mesh(SG, concrete(true)) : statue; st.rotation.y = ROT; st.position.y = .87; par.add(st);
    const isl = new T.Mesh(IG, grassMat(clip)); isl.receiveShadow = !clip; par.add(isl);
    const pl = new T.Mesh(plG, concrete(clip, true)); pl.rotation.y = ROT; pl.position.y = .52; pl.castShadow = pl.receiveShadow = !clip; par.add(pl);
    const bm = new T.InstancedMesh(bG, rockMat(clip), BOUL.length), M4 = new T.Matrix4(), Q = new T.Quaternion(), E = new T.Euler();
    BOUL.forEach(([x, y, z, s, o], i) => { M4.compose(new T.Vector3(x, y, z), Q.setFromEuler(E.set(o, o * 2, 0)), new T.Vector3(s, s, s)); bm.setMatrixAt(i, M4); }); bm.receiveShadow = !clip; par.add(bm);
    par.add(new T.Mesh(SHG, grassMat(clip)));
    const TR = clip ? TREES.slice(0, 3) : TREES, NBL = 26, nb = TR.length * NBL, bl = new T.InstancedMesh(blobG, leafMat(clip), nb), tr = new T.InstancedMesh(trunkG, barkMat(clip), TR.length); let k = 0;
    TR.forEach(([x, y, z, s], i) => { const h = 4.2 * s; M4.compose(new T.Vector3(x, y, z), Q.identity(), new T.Vector3(s * 1.1, h, s * 1.1)); tr.setMatrixAt(i, M4); const rq = K.rng(100 + i);
      for (let b = 0; b < NBL; b++) { const u1 = rq() * 2 - 1, a = rq() * 6.283, q = Math.sqrt(1 - u1 * u1), rr2 = Math.pow(rq(), .4), sc = (1.8 + rq() * 1.3) * s; M4.compose(new T.Vector3(x + Math.cos(a) * q * rr2 * 2.3 * s, y + h * .78 + 2.4 * s + u1 * rr2 * 2.6 * s, z + Math.sin(a) * q * rr2 * 2.3 * s), Q.setFromEuler(E.set(rq() * 6.28, rq() * 6.28, rq() * 6.28)), new T.Vector3(sc, sc, sc)); bl.setMatrixAt(k++, M4); } });
     par.add(bl, tr);
  }
  const world = new T.Group(); S.add(world); addWorld(world, false); addWorld(mirror, true);
  // ---------- soft grass (user 2026-10-15: "the grass is too spiky" -> kit.grass: lush strand tufts, a soft band on the far shore) ----------
  // ground heights matching islandGeo / shoreGeo, the plinth footprint (rotated ellipse) to keep clear
  const islE = (x, z) => Math.hypot(x, z) / islR(Math.atan2(z, x));
  const islY = (x, z) => { const e = islE(x, z); return .62 * (1 - sm(.55, 1.05, e)) + .12 * (fbm(x * .35, 0, z * .35) - .5) * 2 * sm(.15, .5, e) - .5 * sm(.95, 1.18, e) - .05; };
  const plQ = (x, z) => { const lx = x * Math.cos(ROT) - z * Math.sin(ROT), lz = x * Math.sin(ROT) + z * Math.cos(ROT); return Math.hypot(lx / 5.4, lz / 3.0); };
  const gSun = SUN.toArray();
  // the camera always looks from the +x/+z side (orbit a = .5 .. .95): grass on the far side sits behind the plinth and statue or
  // is tiny, so it is planted thinner there (software GL pays for every tuft fragment, hidden or not)
  const nearSide = (x, z) => .35 + .65 * sm(-6, 2, x * .66 + z * .75);
  const lawn = K.grass(S, { parent: world, seed: 101, n: 330, area: [-11, -11, 11, 11], ground: islY, size: [.95, .4], sun: gSun, wind: .1, thin: [11, 27, .3],
    mask: (x, z) => { const e = islE(x, z), q = plQ(x, z); return sm(.95, .88, e) * sm(1.12, 1.24, q) * nearSide(x, z) * (.62 + .38 * Math.max(sm(1.7, 1.3, q), sm(.6, .85, e))); },
    scale: (x, z) => { const e = islE(x, z), q = plQ(x, z); return (.8 + .55 * fbm(x * .4, 5, z * .4)) * (1 + .7 * sm(1.6, 1.2, q) + .5 * sm(.7, .9, e)); },
    tint: '#d8dcc8', dryTint: '#e0c890', dryFrac: .12, transK: .5, base: .3, splay: .12,
    strands: { n: 620, width: 3.4, hMin: .4, spread: 1.15, root: '#141b0b', tip: '#8e9a55', dry: '#b9a460', dryFrac: .15 } });
  // waterline: taller soft clumps instead of reeds (fine strands, soft tips, warm dry tips that light up against the sun)
  const shoreG = K.grass(S, { parent: world, seed: 131, n: 170, area: [-12.5, -12.5, 12.5, 12.5], ground: (x, z) => Math.max(islY(x, z), -.1), size: [.85, .82], sun: gSun, wind: .13, thin: [12, 28, .35],
    mask: (x, z) => { const e = islE(x, z); return Math.exp(-Math.pow((e - .955) / .035, 2)) * nearSide(x, z); }, receiveShadow: false,
    scale: (x, z) => .7 + .7 * fbm(x * .5, 9, z * .5), tint: '#d0d0b8', dryTint: '#e8cc8c', dryFrac: .3, transK: .6, base: .3, splay: .3,
    strands: { n: 420, width: 3.2, hMin: .45, root: '#121809', tip: '#a39a5a', dry: '#c8ad68', dryFrac: .3, spread: 1.1 } });
  // far shore: a low soft line of grass along the bank (one band, no single blades at that distance)
  const shoreY = (x, z) => { const r = Math.hypot(x, z), a = Math.atan2(z, x), q = Math.pow(Math.max(0, (r - 36 - 6 * (vn(Math.cos(a) * 2 + 7, Math.sin(a) * 2, 3) - .5) * 2) / 170), 1 / 1.6);
    return -.4 + 1.2 * sm(0, .12, q) + 2.5 * sm(.2, 1, q) * fbm(x * .03, 1, z * .03); };
  const bandPath = []; for (let i = 0; i < 260; i++) { const a = i / 260 * 6.283, r = 40.5 + 6 * (vn(Math.cos(a) * 2 + 7, Math.sin(a) * 2, 3) - .5) * 2; bandPath.push([Math.cos(a) * r, Math.sin(a) * r]); }
  const band = K.grass(S, { parent: world, seed: 151, ground: shoreY, sun: gSun, transK: 2.6, trans: '#ffb878', color: '#e0e0cc',
    band: { path: bandPath, closed: true, height: 1.9, rows: 2, rowGap: 1.6, tile: 3.2, strands: { root: '#141a0c', tip: '#a8a870', dry: '#c8b07a', dryFrac: .3 } } });
  // ---------- the lake: dark translucent surface over the mirrored world, rippling highlights ----------
  const ripN = K.normalMap(K.noise(512, { seed: 91, octaves: 5, sx: 1, sy: 3 }), 3); ripN.repeat.set(26, 26); aniso(ripN);
  const water = new T.Mesh(new T.PlaneGeometry(600, 600), fadeN(new T.MeshStandardMaterial({ color: '#04060b', roughness: .09, metalness: 0, normalMap: ripN, normalScale: new T.Vector2(.25, .25), transparent: true, opacity: .52, envMapIntensity: 1.2, depthWrite: true }), 10, 70, .18, 'pb-water'));
  water.rotation.x = -Math.PI / 2; water.receiveShadow = false; S.add(water);
  // ---------- light ----------
  const hemi = new T.HemisphereLight('#7a8598', '#2a2116', .85); S.add(hemi);
  const sun = new T.DirectionalLight('#ffad66', 3.2); sun.position.copy(SUN).multiplyScalar(60); sun.castShadow = true; S.add(sun); S.add(sun.target);
  sun.shadow.mapSize.set(1024, 1024); const sc2 = sun.shadow.camera; sc2.left = -15; sc2.right = 15; sc2.top = 10; sc2.bottom = -6; sc2.near = 20; sc2.far = 110; sun.shadow.bias = -.0015; sun.shadow.normalBias = .09;
  const fill = new T.DirectionalLight("#a4b2c6", 1.5); fill.position.set(26, 18, 34); S.add(fill);
  const lamp = new T.PointLight('#ffc98a', 0, 30, 1.5); lamp.position.set(10, 6, 9); S.add(lamp);   // a warm park lamp off-frame, fades up a little
  // ---------- mist, motes, a few early stars ----------
  const mT = K.tex(K.noise(256, { seed: 5, octaves: 4 }), true); const mists = [];
  [[.45, .16, 0]].forEach(([y, op, o]) => { const m = new T.Mesh(new T.PlaneGeometry(140, 140), new T.MeshBasicMaterial({ map: mT.clone(), color: '#9a8fb0', transparent: true, opacity: op, blending: T.AdditiveBlending, depthWrite: false, fog: false }));
    m.material.map.repeat.set(2, 2); m.material.map.needsUpdate = true; m.rotation.x = -Math.PI / 2; m.position.y = y; m.userData = { o, op }; S.add(m); mists.push(m); });
  const motes = K.snow(S, { n: 1400, box: [40, 12, 40], size: .07, color: '#ffcf96', opacity: .5, fall: .05, seed: 13 });
  const stars = ctx.stars(S, 700, 380, { size: .9, opacity: .4, seed: 19 }); { const a = stars.geometry.attributes.position.array; for (let i = 0; i < a.length; i += 3) a[i + 1] = 60 + Math.abs(a[i + 1]) * .8; }
  const sunGlow = ctx.glow(S, '#ff9a50', 160, .28); sunGlow.position.copy(SUN).multiplyScalar(300); sunGlow.position.y = 6;
  // ---------- the ghost: a slimmer, tail-up shape, glowing outline (x-ray), sweeping in from the tail ----------
  const KG = [[0, .03, .04, .55, 0], [.15, .16, .2, .5, 0], [.32, .4, .5, .35, 0], [.44, .78, 1.05, .15, 0], [.55, .95, 1.22, 0, 0], [.66, .88, 1.08, -.25, 0],
    [.75, .55, .68, -.4, 0], [.83, .35, .42, -.5, 0], [.9, .32, .44, -.62, 0], [.96, .2, .27, -.72, 0], [1, .04, .07, -.78, 0]];
  const gw = curve(KG, 1), gh = curve(KG, 2), gy = curve(KG, 3), LG = 11.5, GY = 3.05;
  const ghostG = (() => { const b = K.body({ length: LG, seg: 160, ring: 40, belly: .2, width: gw, height: gh }); b.deform((s) => [0, gy(s), 0]);
    const parts = [b.geo], X = s => (s - .5) * LG;
    [[.47, 1, .55, 1.0], [.47, -1, .55, 1.0], [.72, 1, .45, .62], [.72, -1, .45, .62]].forEach(([s0, sd, z0, sc]) => { const x0 = X(s0), top = gy(s0);
      parts.push(sweepY(24, 20, s => { const y = -GY + s * (top + GY), r = (s < .08 ? .28 : .2 + .32 * sm(.35, 1, s)) * sc, kn = Math.sin(Math.PI * s * 1.2) * .3 * (sc < .8 ? -1 : 1); return [x0 + kn, y, sd * z0, r, r * .85]; })); });
    const g = merge(parts); g.translate(0, GY, 0); return g; })();
  const GU = { col: { value: new T.Color(ctx.ACC) }, op: { value: 0 }, rev: { value: -9 } };
  const ghost = new T.Mesh(ghostG, new T.ShaderMaterial({ uniforms: GU, transparent: true, depthWrite: false, depthTest: false, blending: T.AdditiveBlending,
    vertexShader: 'varying vec3 vN; varying vec3 vV; varying float vX; void main(){ vX=position.x; vec4 mv=modelViewMatrix*vec4(position,1.); vN=normalize(normalMatrix*normal); vV=-mv.xyz; gl_Position=projectionMatrix*mv; }',
    fragmentShader: 'uniform vec3 col; uniform float op,rev; varying vec3 vN; varying vec3 vV; varying float vX; void main(){ float f=pow(1.-abs(dot(normalize(vN),normalize(vV))),2.6); float m=smoothstep(rev,rev-1.2,vX); float edge=exp(-pow((vX-rev)/.25,2.))*.9; float sl=.75+.25*sin(vX*9.); gl_FragColor=vec4(col*(f*1.3*sl+.05+edge*f*2.)*op*m,1.); }' }));
  ghost.position.set(.3, 1.0, 0); ghost.rotation.y = ROT; S.add(ghost);
  const gpA = ghostG.attributes.position.array, NGp = 900, gpts = ctx.points(NGp, { size: .09, color: ctx.ACC }), gpp = gpts.geometry.attributes.position.array, gpx = new Float32Array(NGp), rg2 = K.rng(83);
  for (let i = 0; i < NGp; i++) { const v = (rg2() * (gpA.length / 3)) | 0; gpp.set([gpA[v * 3], gpA[v * 3 + 1], gpA[v * 3 + 2]], i * 3); gpx[i] = gpA[v * 3]; }
  gpts.material.depthTest = false; ghost.add(gpts);
  // ---------- camera ----------
  const cam = new T.PerspectiveCamera(33, ctx.W / ctx.H, .1, 1200); ctx.side(cam, p.side == null ? .13 : p.side);
  const SUNC = new T.Color('#ffad66'), COOL = new T.Color('#9fb0ff'), GOLD = new T.Color('#ffc070'), tmpV = new T.Vector3();
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const hornK = at(p.horn, 3.5) * (1 - at(p.years, 3)), yrs = at(p.years, 3), wr = at(p.wrong, 2.5);
    // camera: slow orbit from a 3/4 front view across the water; closes in on the head at "horn", rises, then pulls back for the ghost
    const a = .5 + u * .021, d = 26 - 7 * sm(0, 7, u) - 4 * hornK + 2 * yrs + 3.5 * wr, hgt = 3.1 + .9 * sm(0, 12, u) + 1.4 * wr;
    const tx = 1.0 + 3.4 * hornK - 1.0 * wr, ty = 2.6 + .2 * hornK + .3 * wr;
    cam.position.set(Math.sin(a) * d + tx * .4, hgt, Math.cos(a) * d); cam.lookAt(tx, ty, 0); cam.updateMatrixWorld();
    // light: dusk sinks a little; golden at "years"; cools on "wrong"
    const warm = 1 - .65 * wr; sun.intensity = (3.2 + .6 * yrs) * warm; sun.color.copy(SUNC).lerp(GOLD, yrs * .4);
    hemi.intensity = .85 + .1 * wr; hemi.color.set('#7a8598').lerp(COOL, wr * .4);
    lamp.intensity = 55 * sm(ctx.t0 + 2, ctx.t0 + 9, t) * (1 - .6 * wr);
    U.rimK.value = (.35 + .25 * hornK) * warm + .12 * wr; U.rimC.value.copy(SUNC).lerp(COOL, wr * .6);
    U.sunV.value.copy(SUN).transformDirection(cam.matrixWorldInverse);
    dome.material.uniforms.k.value = 1 - .3 * wr; sunGlow.material.opacity = .28 * (1 - .5 * wr);
    S.fog.color.set('#1d1a28').lerp(new T.Color('#141a2c'), wr);
    // water ripples drift
    ripN.offset.set(t * .004, t * .011);
    mists.forEach((m, i) => { m.material.map.offset.set(t * .006 * (i + 1) + m.userData.o, t * .002 + m.userData.o); m.material.opacity = m.userData.op * (.8 + .2 * Math.sin(t * .3 + i)); });
    motes.update(t, [0, 4, 0]);
    lawn.update(t, cam); shoreG.update(t, cam); band.update(t, cam);
    // ghost sweeps in tail -> head, then holds, breathing faintly
    GU.op.value = .85 * wr * (.85 + .15 * Math.sin(t * 2.2)); GU.rev.value = -7 + 15 * at(p.wrong, 3.2);
    const pc = gpts.geometry.attributes.color.array; for (let i = 0; i < NGp; i++) { const v = wr * (gpx[i] < GU.rev.value ? 1 : 0) * (.3 + .7 * Math.max(0, Math.sin(t * 2.5 + i * 1.7))); pc[i * 3] = pc[i * 3 + 1] = pc[i * 3 + 2] = v; }
    gpts.geometry.attributes.color.needsUpdate = true; ghost.visible = wr > .001;
  } };
};
