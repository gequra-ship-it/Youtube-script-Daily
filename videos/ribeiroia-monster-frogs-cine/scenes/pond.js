// pond — a pond edge at macro scale with a realistic frog sitting on a wet stone at the water line (stage). Shared by
// epomis-frog-hunter-v2-cine (night) and ribeiroia-monster-frogs-cine (day); keep both copies identical.
// The frog is ONE mesh: body, head, folded hind legs, front legs, toes and the tongue are one BufferGeometry. The body is an
// implicit surface (smooth union of ellipsoids and round cones, meshed once with surface nets), the jaw opens and the throat
// breathes by deforming that mesh, and the tongue is a tube of extra vertices in the same geometry, stretched out to the insect
// and back. Only the eyes are separate small spheres. Water: planar reflection (half-resolution mirror pass with an oblique near
// plane) distorted by ripples; seen from below it shows the Snell window. Reeds, cattails and grass sway in the vertex shader.
// params:
//   mode: 'night' | 'day'
//   night look (2026-10-15): backlit by the moon, weak front fill, moonlit rim on the frog, low mist over the water.
//   night cues: insect (a firefly drifts in), moves (it darts in front of the frog), tongue (the strike), reveal (camera pulls back
//               over the pond)
//   day cues:   flies (dragonflies drift through the reeds), still (the ripples die away), wide (camera rises for the calm wide view),
//               sink (camera sinks below the surface: dark water, light shafts, tadpoles)
//   side: .12 (subject offset to the right; the left third holds the HUD text)
(window.MIYA = window.MIYA || { scenes: {} }).scenes.pond = function (ctx, p) {
  const { T, sm, cue } = ctx, K = window.MIYA.kit, NIGHT = p.mode !== 'day', R = ctx.R;
  const at = (c, d, t) => c == null ? 0 : sm(cue(c), cue(c) + d, t);
  const S = new T.Scene();
  const hash = (i, j, k) => { const s = Math.sin(i * 127.1 + j * 311.7 + k * 74.7) * 43758.5453; return s - Math.floor(s); };
  const n3 = (x, y, z) => { const i = Math.floor(x), j = Math.floor(y), k = Math.floor(z), fx = x - i, fy = y - j, fz = z - k, ux = fx * fx * (3 - 2 * fx), uy = fy * fy * (3 - 2 * fy), uz = fz * fz * (3 - 2 * fz);
    const L = (a, b, t) => a + (b - a) * t;
    return L(L(L(hash(i, j, k), hash(i + 1, j, k), ux), L(hash(i, j + 1, k), hash(i + 1, j + 1, k), ux), uy), L(L(hash(i, j, k + 1), hash(i + 1, j, k + 1), ux), L(hash(i, j + 1, k + 1), hash(i + 1, j + 1, k + 1), ux), uy), uz); };
  const fbm = (x, y, z) => n3(x, y, z) * .55 + n3(x * 2.1, y * 2.1, z * 2.1) * .3 + n3(x * 4.3, y * 4.3, z * 4.3) * .15;
  const col = h => new T.Color(h);

  // ---------------- palette / atmosphere ----------------
  const PAL = NIGHT ? { fog: '#0a0e26', fogD: .03, skyTop: '#050820', skyMid: '#141a4a', skyHor: '#363a78', deep: '#01020a', hemiS: '#6878e0', hemiG: '#141020', hemiI: .75,
      key: '#b4c4ff', keyI: 3.6, sunDir: [-.36, .17, -1], env: .05 }
    : { fog: '#56646c', fogD: .02, skyTop: '#1e4a70', skyMid: '#5f8098', skyHor: '#f2b46a', deep: '#06160f', hemiS: '#b8d4ec', hemiG: '#3a3218', hemiI: .8,
      key: '#ffd49a', keyI: 2.6, keyDir: [-.55, .6, .6], sunDir: [-.3, .1, -1], env: .28 };
  const FOGC = col(PAL.fog), UWC = col('#062420');
  S.fog = new T.FogExp2(FOGC.clone(), PAL.fogD);
  const SUN = new T.Vector3(...PAL.sunDir).normalize();
  const hemi = new T.HemisphereLight(PAL.hemiS, PAL.hemiG, PAL.hemiI); S.add(hemi);
  const key = new T.DirectionalLight(PAL.key, PAL.keyI); key.position.set(...(PAL.keyDir || PAL.sunDir)).normalize().multiplyScalar(50); S.add(key);
  if (!NIGHT) { const rim = new T.DirectionalLight('#ffb060', 2.4); rim.position.copy(SUN).multiplyScalar(50); S.add(rim); }
  const fill = new T.DirectionalLight(NIGHT ? '#8a7cff' : '#8fb4ff', NIGHT ? .3 : .45);   // night: weak front fill, the frog reads as a backlit silhouette fill.position.set(10, 12, 30); S.add(fill);
  const ENV = ctx.env();   // image light only on small glossy parts (eyes, dragonflies): IBL on large areas is slow in software GL
  // sky dome (moon or low sun glow toward SUN)
  const dome = new T.Mesh(new T.SphereGeometry(600, 48, 24), new T.ShaderMaterial({ side: T.BackSide, depthWrite: false, fog: false,
    uniforms: { top: { value: col(PAL.skyTop) }, mid: { value: col(PAL.skyMid) }, hor: { value: col(PAL.skyHor) }, sun: { value: SUN }, glow: { value: col(NIGHT ? '#4a4c9a' : '#ffb860') }, gk: { value: NIGHT ? .5 : 1.3 } },
    vertexShader: 'varying vec3 vP; void main(){ vP=normalize(position); vec4 p=projectionMatrix*modelViewMatrix*vec4(position,1.); gl_Position=p.xyww; }',
    fragmentShader: `uniform vec3 top,mid,hor,sun,glow; uniform float gk; varying vec3 vP;
      void main(){ float y=vP.y; vec3 c = y>0.? mix(hor,mid,smoothstep(0.,.12,y)) : hor; c = mix(c, top, smoothstep(.1,.7,y));
        float g=max(dot(vP,sun),0.); c += glow*gk*(pow(g,6.)*.35+pow(g,40.)*.6);
        gl_FragColor=vec4(c,1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  dome.renderOrder = 10; dome.frustumCulled = false; S.add(dome);
  if (NIGHT) {
    // stars (upper sky only) and the moon with a halo
    const NS = 2600, st = ctx.points(NS, { size: 1.3, opacity: .85, color: '#d6dcff', atten: false }), sa = st.geometry.attributes.position.array, sc = st.geometry.attributes.color.array, r0 = K.rng(12);
    for (let i = 0; i < NS; i++) { const u = .03 + Math.pow(r0(), 1.3) * .97, th = r0() * 6.283, q = Math.sqrt(1 - u * u); sa.set([q * Math.cos(th) * 500, u * 500, q * Math.sin(th) * 500], i * 3); const b = .25 + Math.pow(r0(), 4) * 1.2; sc.set([b, b, b * 1.05], i * 3); }
    st.material.fog = false; S.add(st);
    const mt = ctx.ctex(512, (g, z) => { g.fillStyle = '#fff6e0'; g.fillRect(0, 0, z, z); const nz = K.noise(256, { seed: 33, octaves: 5, sx: 2, sy: 2 }); g.globalAlpha = .45; g.globalCompositeOperation = 'multiply'; g.drawImage(nz, 0, 0, z, z); g.globalAlpha = 1;
      const rr = K.rng(8); g.fillStyle = 'rgba(120,115,130,.35)'; for (let i = 0; i < 9; i++) { g.beginPath(); g.ellipse(rr() * z, z * .3 + rr() * z * .4, 20 + rr() * 70, 15 + rr() * 40, rr() * 3, 0, 6.283); g.fill(); } });
    const moon = new T.Mesh(new T.SphereGeometry(9, 48, 32), new T.MeshBasicMaterial({ map: mt, color: new T.Color(2.2, 2.15, 2.0), fog: false }));
    moon.position.copy(SUN).multiplyScalar(420); moon.lookAt(0, 0, 0); S.add(moon);
    const h1 = ctx.glow(S, '#9fb0ff', 150, .32), h2 = ctx.glow(S, '#fff0d0', 48, .5); h1.position.copy(moon.position); h2.position.copy(moon.position);
  } else {
    const sunG = ctx.glow(S, '#ffd9a0', 120, .55), sunC = ctx.glow(S, '#fff4e0', 26, .95); sunG.position.copy(SUN).multiplyScalar(420); sunC.position.copy(sunG.position);
  }

  // ---------------- terrain: bank behind and right of the frog, pond bottom under the water ----------------
  const shoreZ = x => -1.25 - 26 * sm(-.8, -5, x) + 10 * sm(-14, -26, x);   // bank right behind the frog, open water to the far shore on the left
  const ground = (x, z) => { const zs = shoreZ(x), zz = z - zs - 1.25 + .35 * Math.sin(x * .45) + .2 * Math.sin(x * 1.3), sh = Math.min(1, sm(-.6, -1.9, zz) + sm(1.8, 5, x) * sm(3, -.5, z));
    const bot = -.6 - 2 * sm(-.5, 2.5, zz) - 1.2 * sm(-3, -9, x), bank = .4 + .3 * (fbm(x * .5, 0, z * .5) - .5) + .9 * sm(-4, -14, z); return bot + (bank - bot) * sh; };
  const gG = new T.PlaneGeometry(70, 40, 120, 72); gG.rotateX(-Math.PI / 2); gG.translate(-8, 0, -14);
  { const P = gG.attributes.position, C = new Float32Array(P.count * 3), mud = col(NIGHT ? '#1a1814' : '#2e2618'), wet = col('#0e0d0a'), grass = col(NIGHT ? '#12201a' : '#2c3a18'), moss = col(NIGHT ? '#1a2a1c' : '#45502a'), c = new T.Color();
    for (let i = 0; i < P.count; i++) { const x = P.getX(i), z = P.getZ(i), y = ground(x, z); P.setY(i, y); const n = fbm(x * 1.3, 2, z * 1.3);
      c.copy(wet).lerp(mud, sm(-.05, .12, y)).lerp(grass, sm(.15, .45, y) * (.6 + .4 * n)).lerp(moss, sm(.55, .8, n) * sm(.1, .3, y) * .6); if (y < -.05) c.multiplyScalar(.6); C.set([c.r, c.g, c.b], i * 3); }
    gG.setAttribute('color', new T.BufferAttribute(C, 3)); gG.computeVertexNormals(); }
  const groundM = new T.MeshLambertMaterial({ vertexColors: true });
  const gMesh = new T.Mesh(gG, groundM); S.add(gMesh); gMesh.layers.set(1);   // layer 1 = not drawn in the reflection pass

  // the stone the frog sits on: displaced sphere, wet dark rock with moss on top
  const rockG = new T.SphereGeometry(1, 96, 64); { const P = rockG.attributes.position, C = new Float32Array(P.count * 3), c = new T.Color(), r1 = col(NIGHT ? '#2c2c36' : '#3a3630'), r2 = col('#141418'), mo = col(NIGHT ? '#20321e' : '#4a5a26');
    for (let i = 0; i < P.count; i++) { const v = new T.Vector3(P.getX(i), P.getY(i), P.getZ(i)); const d = 1 + .3 * (fbm(v.x * 1.4 + 3, v.y * 1.4, v.z * 1.4) - .5) + .07 * (n3(v.x * 6, v.y * 6, v.z * 6) - .5) + .025 * (n3(v.x * 18, v.y * 18, v.z * 18) - .5);
      v.multiplyScalar(d); v.y = v.y > .55 ? .55 + (v.y - .55) * .3 : v.y; P.setXYZ(i, v.x * 1.25, v.y * (v.y < 0 ? .95 : .5), v.z * 1.0);
      const n = fbm(v.x * 3, v.y * 3, v.z * 3); c.copy(r2).lerp(r1, n).lerp(mo, sm(.25, .5, v.y) * sm(.45, .65, n)); C.set([c.r, c.g, c.b], i * 3); }
    rockG.setAttribute('color', new T.BufferAttribute(C, 3)); rockG.computeVertexNormals(); }
  const rock = new T.Mesh(rockG, new T.MeshLambertMaterial({ vertexColors: true })); rock.position.set(.05, -.05, -.15); S.add(rock);
  const ROCKTOP = .22;

  // ---------------- frog: ONE mesh ----------------
  const prims = [];
  const addE = (c, r, pitch, k, tag) => { const cp = Math.cos(pitch || 0), sp = Math.sin(pitch || 0);
    prims.push({ tag, k, bx: c[0], by: c[1], bz: c[2], br: Math.max(...r), f(x, y, z) { const dx = x - c[0], dy = y - c[1], dz = z - c[2]; const qx = (dx * cp + dy * sp) / r[0], qy = (-dx * sp + dy * cp) / r[1], qz = dz / r[2];
      const k0 = Math.sqrt(qx * qx + qy * qy + qz * qz), k1 = Math.sqrt(qx * qx / (r[0] * r[0]) + qy * qy / (r[1] * r[1]) + qz * qz / (r[2] * r[2])); return k1 < 1e-9 ? -Math.min(...r) : k0 * (k0 - 1) / k1; } }); };
  const addC = (a, b, ra, rb, k, tag) => { const bx = b[0] - a[0], by = b[1] - a[1], bz = b[2] - a[2], bb = bx * bx + by * by + bz * bz;
    prims.push({ tag, k, a, b, bx: (a[0] + b[0]) / 2, by: (a[1] + b[1]) / 2, bz: (a[2] + b[2]) / 2, br: Math.sqrt(bb) / 2 + Math.max(ra, rb),
      h(x, y, z) { return Math.min(1, Math.max(0, ((x - a[0]) * bx + (y - a[1]) * by + (z - a[2]) * bz) / bb)); },
      f(x, y, z) { const h = this.h(x, y, z), px = x - a[0] - bx * h, py = y - a[1] - by * h, pz = z - a[2] - bz * h; return Math.sqrt(px * px + py * py + pz * pz) - (ra + (rb - ra) * h); } }); };
  // body and head (x forward, y up, z to the frog's left; only z >= 0 is defined, the field is mirrored)
  addE([-.04, .29, 0], [.41, .19, .25], .42, 0, 'body');
  addE([.33, .42, 0], [.23, .125, .21], .12, .09, 'head');
  addE([.52, .415, 0], [.12, .075, .125], .05, .05, 'head');
  addE([.32, .36, 0], [.2, .075, .18], .1, .06, 'chin');
  addE([.37, .52, .115], [.07, .062, .068], 0, .035, 'lid');
  addC([.28, .5, .13], [-.12, .43, .15], .014, .01, .04, 'ridge');
  // hind leg folded beside the body: thigh forward, shin back, foot forward on the ground, five long toes
  addC([-.3, .21, .15], [.02, .15, .33], .1, .066, .045, 'thigh');
  addC([.03, .14, .35], [-.31, .075, .38], .062, .042, .03, 'shin');
  addC([-.31, .06, .38], [-.02, .03, .46], .042, .028, .025, 'foot');
  [[-.55, .13], [-.25, .17], [0, .21], [.28, .19], [.55, .14]].forEach(([a, L]) => { const s = [-.02, .028, .46], e = [s[0] + Math.cos(a) * L, .018, s[2] + Math.sin(a) * L];
    addC(s, e, .017, .011, .012, 'toe'); addE(e, [.016, .011, .016], 0, .008, 'toe'); });
  // front leg: upper arm down, forearm forward, four short fingers
  addC([.22, .26, .15], [.17, .12, .235], .052, .042, .03, 'arm');
  addC([.17, .12, .235], [.3, .028, .225], .042, .03, .02, 'arm');
  [[-.5, .06], [-.15, .085], [.2, .08], [.55, .06]].forEach(([a, L]) => { const s = [.3, .024, .225], e = [s[0] + Math.cos(a) * L, .016, s[2] + Math.sin(a) * L];
    addC(s, e, .014, .01, .01, 'finger'); addE(e, [.014, .01, .014], 0, .006, 'finger'); });
  const smin = (a, b, k) => { if (k <= 0) return Math.min(a, b); const h = Math.max(k - Math.abs(a - b), 0) / k; return Math.min(a, b) - h * h * k * .25; };
  function field(x, y, z, want) {
    z = Math.abs(z); let d = 1e9, best = 1e9, bp = null;
    for (let i = 0; i < prims.length; i++) { const P = prims[i], dx = x - P.bx, dy = y - P.by, dz = z - P.bz, bd = Math.sqrt(dx * dx + dy * dy + dz * dz) - P.br;
      if (bd > d + P.k) continue;
      const di = bd > P.k + .04 ? bd : P.f(x, y, z); d = smin(d, di, P.k); if (want && di < best) { best = di; bp = P; } }
    if (Math.abs(d) < .02 && y > .18) d -= .0028 * (n3(x * 55, y * 55, z * 55) - .5) + .0022 * (n3(x * 120, y * 120, z * 120) - .5);
    return want ? [d, bp] : d;
  }
  function frogGeo(h) {
    const X0 = -.62, Y0 = -.03, nx = Math.ceil(1.45 / h) + 1, ny = Math.ceil(.7 / h) + 1, nzh = Math.ceil(.62 / h), nz = nzh * 2 + 1, Z0 = -nzh * h;
    const F = new Float32Array(nx * ny * nz), id = (i, j, k) => i + nx * (j + ny * k);
    const B = 4, mg = B * h * 1.2 + .004;   // blocks of 4^3 points far from the surface take the block-centre value
    for (let kb = nzh; kb < nz; kb += B) for (let jb = 0; jb < ny; jb += B) for (let ib = 0; ib < nx; ib += B) {
      const dc = field(X0 + (ib + 1.5) * h, Y0 + (jb + 1.5) * h, Z0 + (kb + 1.5) * h), far = Math.abs(dc) > mg;
      for (let k = kb; k < Math.min(nz, kb + B); k++) for (let j = jb; j < Math.min(ny, jb + B); j++) for (let i = ib; i < Math.min(nx, ib + B); i++) {
        const v = far ? dc : field(X0 + i * h, Y0 + j * h, Z0 + k * h); F[id(i, j, k)] = v; F[id(i, j, nz - 1 - k)] = v; } }
    // surface nets
    const vs = [], cell = new Int32Array(nx * ny * nz).fill(-1), E = [[0, 1], [2, 3], [4, 5], [6, 7], [0, 2], [1, 3], [4, 6], [5, 7], [0, 4], [1, 5], [2, 6], [3, 7]], cv = new Float32Array(8);
    for (let k = 0; k < nz - 1; k++) for (let j = 0; j < ny - 1; j++) for (let i = 0; i < nx - 1; i++) {
      let m = 0; for (let c = 0; c < 8; c++) { const v = F[id(i + (c & 1), j + ((c >> 1) & 1), k + ((c >> 2) & 1))]; cv[c] = v; if (v < 0) m |= 1 << c; }
      if (m === 0 || m === 255) continue; let sx = 0, sy = 0, sz = 0, n = 0;
      for (const [a, b] of E) { if ((cv[a] < 0) === (cv[b] < 0)) continue; const t = cv[a] / (cv[a] - cv[b]); sx += (a & 1) + ((b & 1) - (a & 1)) * t; sy += ((a >> 1) & 1) + (((b >> 1) & 1) - ((a >> 1) & 1)) * t; sz += ((a >> 2) & 1) + (((b >> 2) & 1) - ((a >> 2) & 1)) * t; n++; }
      cell[id(i, j, k)] = vs.length / 3; vs.push(X0 + (i + sx / n) * h, Y0 + (j + sy / n) * h, Z0 + (k + sz / n) * h); }
    const ix = [], quad = (a, b, c, d, flip) => { if (a < 0 || b < 0 || c < 0 || d < 0) return; if (flip) ix.push(a, b, c, a, c, d); else ix.push(a, c, b, a, d, c); };
    for (let k = 1; k < nz - 1; k++) for (let j = 1; j < ny - 1; j++) for (let i = 1; i < nx - 1; i++) { const v0 = F[id(i, j, k)] < 0;
      if ((F[id(i + 1, j, k)] < 0) !== v0) quad(cell[id(i, j - 1, k - 1)], cell[id(i, j, k - 1)], cell[id(i, j, k)], cell[id(i, j - 1, k)], v0);
      if ((F[id(i, j + 1, k)] < 0) !== v0) quad(cell[id(i - 1, j, k - 1)], cell[id(i - 1, j, k)], cell[id(i, j, k)], cell[id(i, j, k - 1)], v0);
      if ((F[id(i, j, k + 1)] < 0) !== v0) quad(cell[id(i - 1, j - 1, k)], cell[id(i, j - 1, k)], cell[id(i, j, k)], cell[id(i - 1, j, k)], v0); }
    // normals from the field gradient, colours from the nearest part
    const nv = vs.length / 3, N = new Float32Array(nv * 3), C = new Float32Array(nv * 3), e = h * .6, c = new T.Color();
    const cD1 = col('#3a5020'), cD2 = col('#5a5626'), cSpot = col('#141c0c'), cHalo = col('#9aa858'), cBelly = col('#d8cfa4'), cLip = col('#2a1012'), cLipU = col('#b4b878'), cTym = col('#3e301a'), cToe = col('#8c8a5c'), cIn = col('#b8a656'), cRidge = col('#a08a44');
    for (let q = 0; q < nv; q++) { const x = vs[q * 3], y = vs[q * 3 + 1], z = vs[q * 3 + 2];
      let gx = field(x + e, y, z) - field(x - e, y, z), gy = field(x, y + e, z) - field(x, y - e, z), gz = field(x, y, z + e) - field(x, y, z - e); const l = Math.hypot(gx, gy, gz) || 1; gx /= l; gy /= l; gz /= l; N.set([gx, gy, gz], q * 3);
      const [, P] = field(x, y, z, true), az = Math.abs(z), tg = P ? P.tag : 'body', nn = fbm(x * 6 + 1, y * 6, az * 6);
      c.copy(cD1).lerp(cD2, nn);
      const sp = fbm(x * 10 + 7, y * 10, az * 10 + (z < 0 ? 3.1 : 0)); if (tg !== 'toe' && tg !== 'finger') { c.lerp(cHalo, sm(.56, .6, sp) * (1 - sm(.6, .63, sp)) * .5); c.lerp(cSpot, sm(.6, .64, sp)); }
      if (tg === 'ridge') c.lerp(cRidge, .55);
      if (P && P.h && (tg === 'thigh' || tg === 'shin' || tg === 'foot')) { const hh = P.h(x, y, az); c.lerp(cSpot, sm(.25, .55, Math.sin(hh * Math.PI * (tg === 'foot' ? 3 : 4) + (tg === 'shin' ? 1 : 0))) * .85); c.lerp(cIn, sm(.1, -.6, gy) * .6); }
      if (tg === 'toe' || tg === 'finger') c.copy(cToe).lerp(cD1, .3);
      c.lerp(cBelly, sm(-.15, -.6, gy) * sm(.32, .2, y) * (tg === 'body' || tg === 'chin' || tg === 'head' ? 1 : .4));
      const ym = mouthY(x); if (x > .2 && (tg === 'head' || tg === 'chin')) { c.lerp(cLipU, sm(.008, .014, y - ym) * (1 - sm(.024, .034, y - ym)) * .6); c.lerp(cLip, 1 - sm(.002, .006, Math.abs(y - ym))); }
      const tdx = x - .235, tdy = y - .455; if (az > .1 && tdx * tdx + tdy * tdy < .04 * .04) c.lerp(cTym, .8);
      C.set([c.r, c.g, c.b], q * 3); }
    // fix triangle winding against the field normal
    for (let t = 0; t < ix.length; t += 3) { const a = ix[t] * 3, b = ix[t + 1] * 3, d = ix[t + 2] * 3;
      const ux = vs[b] - vs[a], uy = vs[b + 1] - vs[a + 1], uz = vs[b + 2] - vs[a + 2], wx = vs[d] - vs[a], wy = vs[d + 1] - vs[a + 1], wz = vs[d + 2] - vs[a + 2];
      const fx = uy * wz - uz * wy, fy = uz * wx - ux * wz, fz = ux * wy - uy * wx; if (fx * N[a] + fy * N[a + 1] + fz * N[a + 2] < 0) { const s = ix[t + 1]; ix[t + 1] = ix[t + 2]; ix[t + 2] = s; } }
    return { pos: new Float32Array(vs), N, C, ix, nv };
  }
  function mouthY(x) { return .392 + .012 * sm(.45, .62, x) - .03 * sm(.3, .2, x); }
  // tongue: TN rings of TM vertices appended to the frog geometry
  const TN = 36, TM = 12;
  function buildFrog(h, withTongue) {
    const g0 = frogGeo(h), nt = withTongue ? (TN + 1) * TM : 0, nv = g0.nv + nt;
    const pos = new Float32Array(nv * 3), nor = new Float32Array(nv * 3), cl = new Float32Array(nv * 3); pos.set(g0.pos); nor.set(g0.N); cl.set(g0.C);
    const ix = g0.ix.slice(), tc = col('#d0505e'), tc2 = col('#f08890');
    if (withTongue) { for (let i = 0; i <= TN; i++) for (let j = 0; j < TM; j++) { const k = g0.nv + i * TM + j; const c = tc.clone().lerp(tc2, i / TN * .6); cl.set([c.r, c.g, c.b], k * 3); }
      for (let i = 0; i < TN; i++) for (let j = 0; j < TM; j++) { const a = g0.nv + i * TM + j, b = g0.nv + i * TM + (j + 1) % TM, c = a + TM, d = b + TM; ix.push(a, b, c, b, d, c); } }
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(pos, 3)); g.setAttribute('normal', new T.BufferAttribute(nor, 3)); g.setAttribute('color', new T.BufferAttribute(cl, 3)); g.setIndex(ix);
    return { g, nb: g0.nv, base: g0.pos, baseN: g0.N };
  }
  const skinM = new T.MeshStandardMaterial({ vertexColors: true, roughness: .38, metalness: 0 });
  const rimDir = { value: new T.Vector3() };   // moon direction in view space, set each frame: the rim lights only the edges that face the moon
  if (NIGHT) skinM.onBeforeCompile = sh => { sh.uniforms.rimDir = rimDir; sh.fragmentShader = 'uniform vec3 rimDir;\n' + sh.fragmentShader.replace('#include <emissivemap_fragment>',
    '#include <emissivemap_fragment>\n float fr = pow(1.0 - clamp(abs(dot(normal, normalize(vViewPosition))), 0.0, 1.0), 2.5); totalEmissiveRadiance += vec3(.5, .58, .9) * fr * smoothstep(.0, .6, dot(normal, rimDir)) * .6;'); };
  const F0 = buildFrog(.0088, true), frogMesh = new T.Mesh(F0.g, skinM); frogMesh.frustumCulled = false;
  const frog = new T.Group(); frog.add(frogMesh); S.add(frog);
  // eyes: glossy spheres with a gold iris and a horizontal pupil (the only separate parts)
  const eyeT = ctx.ctex(512, (g, z) => { g.fillStyle = '#0a0806'; g.fillRect(0, 0, z, z); const cx = z * .25, cy = z * .5, r = z * .15;
    const gr = g.createRadialGradient(cx, cy, r * .2, cx, cy, r); gr.addColorStop(0, '#f2c860'); gr.addColorStop(.6, '#c8902c'); gr.addColorStop(.92, '#6a4412'); gr.addColorStop(1, '#1a1008'); g.fillStyle = gr;
    g.save(); g.translate(cx, cy); g.scale(1, 2); g.beginPath(); g.arc(0, 0, r, 0, 6.283); g.fill(); g.restore();
    const rr = K.rng(3); g.strokeStyle = 'rgba(60,30,8,.55)'; g.lineWidth = 1.5; for (let i = 0; i < 90; i++) { const a = rr() * 6.283, r1 = r * (.3 + rr() * .3); g.beginPath(); g.moveTo(cx + Math.cos(a) * r1, cy + Math.sin(a) * r1 * 2); g.lineTo(cx + Math.cos(a) * r * .95, cy + Math.sin(a) * r * 1.9); g.stroke(); }
    g.fillStyle = '#020101'; g.save(); g.translate(cx, cy); g.scale(1, 2); g.beginPath(); g.ellipse(0, 0, r * .55, r * .22, 0, 0, 6.283); g.fill(); g.restore(); });
  const eyeM = new T.MeshStandardMaterial({ envMap: ENV, map: eyeT, emissiveMap: eyeT, emissive: new T.Color(NIGHT ? '#ffb040' : '#000000'), emissiveIntensity: NIGHT ? .35 : 0, roughness: .08, envMapIntensity: NIGHT ? .5 : .8 });
  function makeEyes(parent) { const es = [1, -1].map(sd => { const e = new T.Mesh(new T.SphereGeometry(.058, 32, 24), eyeM); const dir = new T.Vector3(.45, .35, sd * .82).normalize(); e.quaternion.setFromUnitVectors(new T.Vector3(0, 0, 1), dir); e.position.set(.385, .535, sd * .122); parent.add(e); return e; }); return es; }
  const eyes = makeEyes(frog);
  frog.position.set(0, ROCKTOP, 0);
  const FWD = NIGHT ? [-.88, .47] : [-.8, .6]; frog.rotation.y = Math.atan2(-FWD[1], FWD[0]);
  // distant companions on the shore: a lower-resolution copy of the same mesh
  const F1 = NIGHT ? buildFrog(.016, false) : null, mates = [];
  if (NIGHT) [[-2.6, -2.1, .8, 2.0], [2.7, -2.5, .8, -2.4]].forEach(([x, z, s, ry]) => { const g = new T.Group(); g.add(new T.Mesh(F1.g, skinM)); makeEyes(g); g.position.set(x, Math.max(.03, ground(x, z)) + .01, z); g.scale.setScalar(s); g.rotation.y = ry; S.add(g); mates.push(g); });
  // deformation lists: jaw (below the mouth line, in front of the hinge) and throat (breathing)
  const HX = .27, HY = .4, jaw = [], fp = F0.g.attributes.position.array, fn = F0.g.attributes.normal.array;
  for (let q = 0; q < F0.nb; q++) { const x = F0.base[q * 3], y = F0.base[q * 3 + 1], z = F0.base[q * 3 + 2];
    const wj = sm(mouthY(x) + .006, mouthY(x) - .006, y) * sm(.24, .34, x) * sm(.22, .3, y), wt = sm(.16, .26, x) * (1 - sm(.4, .5, x)) * sm(.34, .26, y) * sm(.16, .24, y) * sm(.2, .05, Math.abs(z)) * sm(0, -.5, F0.baseN[q * 3 + 1]);
    if (wj > 0 || wt > 0) jaw.push([q, wj, wt]); }
  const TA = new T.Vector3(.585, .392, 0);   // tongue root, front of the lower jaw (frog space)
  function frogPose(t, jawA, tongue) {   // tongue: null or {e (0..1 extension), tip: Vector3 in frog space}
    const br = .008 * Math.max(0, Math.sin(t * 6.2)) * (1 - jawA * 3);
    for (const [q, wj, wt] of jaw) { let x = F0.base[q * 3], y = F0.base[q * 3 + 1], z = F0.base[q * 3 + 2], nx = F0.baseN[q * 3], ny = F0.baseN[q * 3 + 1];
      const a = -jawA * wj, ca = Math.cos(a), sa = Math.sin(a), dx = x - HX, dy = y - HY; x = HX + dx * ca - dy * sa; y = HY + dx * sa + dy * ca; const nx2 = nx * ca - ny * sa, ny2 = nx * sa + ny * ca;
      y -= br * wt; z *= 1 + br * wt * 3; fp[q * 3] = x; fp[q * 3 + 1] = y; fp[q * 3 + 2] = z; fn[q * 3] = nx2; fn[q * 3 + 1] = ny2; }
    const o = F0.nb, ca = Math.cos(-jawA * .7), sa = Math.sin(-jawA * .7), ax = HX + (TA.x - HX) * ca - (TA.y - HY) * sa, ay = HY + (TA.x - HX) * sa + (TA.y - HY) * ca - .012;
    const A = new T.Vector3(ax, ay, 0), e = tongue ? tongue.e : 0;
    if (e < .01) { for (let k = o; k < o + (TN + 1) * TM; k++) { fp[k * 3] = ax - .05; fp[k * 3 + 1] = ay; fp[k * 3 + 2] = 0; } }
    else { const B = tongue.tip, D = B.clone().sub(A), L = D.length() * e, dir = D.normalize(), up = new T.Vector3(0, 1, 0), side = new T.Vector3().crossVectors(dir, up).normalize(), nrm = new T.Vector3().crossVectors(side, dir);
      const P = new T.Vector3(), Pn = new T.Vector3(), Tg = new T.Vector3(), S2 = new T.Vector3(), N2 = new T.Vector3();
      const pt = (s, out) => out.copy(A).addScaledVector(dir, L * s).addScaledVector(nrm, Math.sin(Math.PI * s) * L * .12 * (1 - e * .5));
      for (let i = 0; i <= TN; i++) { const s = i / TN; pt(s, P); pt(Math.min(1, s + .01), Pn); pt(Math.max(0, s - .01), Tg); Tg.subVectors(Pn, Tg).normalize();
        S2.crossVectors(Tg, nrm).normalize(); N2.crossVectors(S2, Tg).normalize();
        const cap = s > .9 ? Math.sqrt(Math.max(0, 1 - Math.pow((s - .9) / .1, 2))) : 1, r = (.022 + .018 * sm(.6, .9, s)) * cap * (s < .04 ? .7 + s * 7.5 : 1);
        for (let j = 0; j < TM; j++) { const th = j / TM * 6.283, cx = Math.cos(th), cy = Math.sin(th), k = o + i * TM + j;
          fp[k * 3] = P.x + (S2.x * cx + N2.x * cy) * r; fp[k * 3 + 1] = P.y + (S2.y * cx + N2.y * cy) * r * .7; fp[k * 3 + 2] = P.z + (S2.z * cx + N2.z * cy) * r;
          const nn = s > .98 ? Tg : null; fn[k * 3] = nn ? nn.x : S2.x * cx + N2.x * cy; fn[k * 3 + 1] = nn ? nn.y : S2.y * cx + N2.y * cy; fn[k * 3 + 2] = nn ? nn.z : S2.z * cx + N2.z * cy; } } }
    F0.g.attributes.position.needsUpdate = true; F0.g.attributes.normal.needsUpdate = true;
    return A;
  }

  // ---------------- swaying plants (instanced; sway in the vertex shader from the world height above the water) ----------------
  const uT = { value: 0 }, sways = [];
  function swayMat(m, amp, freq, abs) {
    m.onBeforeCompile = sh => { sh.uniforms.uT = uT; sh.uniforms.uA = { value: amp }; sh.uniforms.uF = { value: freq };
      sh.vertexShader = 'uniform float uT, uA, uF;\n' + sh.vertexShader.replace('#include <project_vertex>', `
        vec4 wp = modelMatrix * instanceMatrix * vec4(transformed, 1.0);
        vec3 ip = (modelMatrix * instanceMatrix[3]).xyz;
        float hh = max(wp.y - ${abs ? '0.0' : 'max(ip.y, 0.0)'}, 0.0);
        float sw = sin(uT * uF + ip.x * .37 + ip.z * .23) + .45 * sin(uT * uF * 2.17 + ip.x * 1.3 - ip.z * .7);
        wp.x += sw * hh * hh * uA; wp.z += .4 * cos(uT * uF * .8 + ip.z * .5) * hh * hh * uA;
        vec4 mvPosition = viewMatrix * wp; gl_Position = projectionMatrix * mvPosition;`); };
    m.customProgramCacheKey = () => 'sway' + !!abs; return m; }
  // leaf blade with a folded (V) cross-section so it has structure from every side
  function bladeGeo(len, wid, bend, seg) { const g = new T.BufferGeometry(), P = [], I = []; for (let i = 0; i <= seg; i++) { const s = i / seg, w = wid * (1 - Math.pow(s, 1.6)) + .002, y = s * len, x = bend * s * s * len, f = w * .35;
      P.push(x - w, y, -f * .2, x, y, f, x + w, y, -f * .2); }
    for (let i = 0; i < seg; i++) { const a = i * 3; I.push(a, a + 3, a + 1, a + 1, a + 3, a + 4, a + 1, a + 4, a + 2, a + 2, a + 4, a + 5); }
    g.setAttribute('position', new T.Float32BufferAttribute(P, 3)); g.setIndex(I); g.computeVertexNormals(); return g; }
  const r2 = K.rng(21), M4 = new T.Matrix4(), Q4 = new T.Quaternion(), V4 = new T.Vector3(), S4 = new T.Vector3(), E4 = new T.Euler();
  const reedPts = []; // [x,z,height]
  const inFrame = (x, z) => z > -1 && z < 3.5 && x > -2.4 && x < 1.6;   // keep the frog's surroundings clear
  for (let i = 0; i < 300; i++) { const cl = r2(); let x, z, hs = 1;
    if (cl < .45) { x = -1.5 + r2() * 12; z = -1.3 - Math.pow(r2(), .8) * 5; } else if (cl < .65) { x = 2.5 + r2() * 8; z = -1 + r2() * 1.6; }
    else { x = -30 + r2() * 28; z = shoreZ(x) - .2 - r2() * 3; hs = .75; }
    if (inFrame(x, z)) continue; reedPts.push([x, z, (1.8 + r2() * 3.4) * hs]); }
  const leafG = bladeGeo(1, .045, .25, 10), NL = reedPts.length * 4, leafI = new T.InstancedMesh(leafG, swayMat(new T.MeshLambertMaterial({ color: NIGHT ? '#1c2c22' : '#3a5626', side: T.DoubleSide }), .006, .9), NL);
  const stemG = new T.CylinderGeometry(.018, .028, 1, 6, 6); stemG.translate(0, .5, 0); const NSt = Math.floor(reedPts.length * .45);
  const stemI = new T.InstancedMesh(stemG, swayMat(new T.MeshLambertMaterial({ color: NIGHT ? '#22301e' : '#5a6a32' }), .006, .9, true), NSt);
  const headG = new T.CapsuleGeometry(.07, .5, 4, 10); const headI = new T.InstancedMesh(headG, swayMat(new T.MeshLambertMaterial({ color: NIGHT ? '#2a1a12' : '#5a3a1e' }), .006, .9, true), NSt);
  { let li = 0; reedPts.forEach(([x, z, hgt], n) => { const gy = ground(x, z) - .1;
      for (let k = 0; k < 4; k++) { const L = hgt * (.55 + r2() * .55) + (gy < 0 ? -gy : 0); E4.set((r2() - .5) * .25, r2() * 6.28, (r2() - .5) * .3); Q4.setFromEuler(E4); V4.set(x + (r2() - .5) * .3, gy, z + (r2() - .5) * .3); S4.set(1 + r2(), L, 1 + r2()); M4.compose(V4, Q4, S4); leafI.setMatrixAt(li++, M4); }
      if (n < NSt) { const L = hgt * 1.1 + (gy < 0 ? -gy : 0); Q4.identity(); V4.set(x, gy, z); S4.set(1, L, 1); M4.compose(V4, Q4, S4); stemI.setMatrixAt(n, M4); V4.set(x, gy + L - .2, z); S4.set(1, 1, 1); M4.compose(V4, Q4, S4); headI.setMatrixAt(n, M4); } });
    leafI.count = li; }
  S.add(leafI, stemI, headI);
  // grass on the bank and a few foreground tufts
  const grassG = bladeGeo(1, .012, .35, 5), NGr = 1400, grassI = new T.InstancedMesh(grassG, swayMat(new T.MeshLambertMaterial({ color: NIGHT ? '#1a2a1c' : '#5a7a30', side: T.DoubleSide }), .05, 1.6), NGr);
  { let gi = 0; for (let i = 0; i < NGr * 3 && gi < NGr; i++) { const x = -14 + r2() * 22, z = -6 + r2() * 9, y = ground(x, z); if (y < .02 || (x > -1.2 && x < 1.3 && z > -.9)) continue;
      E4.set((r2() - .5) * .5, r2() * 6.28, (r2() - .5) * .5); Q4.setFromEuler(E4); V4.set(x, y - .02, z); const L = .25 + r2() * .55; S4.set(1, L, 1); M4.compose(V4, Q4, S4); grassI.setMatrixAt(gi++, M4); } grassI.count = gi; }
  S.add(grassI); grassI.layers.set(1);
  // lily pads: real thickness, notch, slightly cupped
  const padG = new T.CylinderGeometry(1, 1, .025, 40, 1, false, .25, 6.03); { const P = padG.attributes.position; for (let i = 0; i < P.count; i++) { const x = P.getX(i), z = P.getZ(i), r = Math.hypot(x, z); P.setY(i, P.getY(i) + r * r * .04); } padG.computeVertexNormals(); }
  const padT = ctx.ctex(256, (g, z) => { g.fillStyle = NIGHT ? '#0e1c12' : '#3e6a2a'; g.fillRect(0, 0, z, z); g.strokeStyle = 'rgba(0,0,0,.35)'; g.lineWidth = 2; for (let k = 0; k < 18; k++) { const a = k / 18 * 6.283; g.beginPath(); g.moveTo(z / 2, z / 2); g.lineTo(z / 2 + Math.cos(a) * z / 2, z / 2 + Math.sin(a) * z / 2); g.stroke(); } });
  const padI = new T.InstancedMesh(padG, new T.MeshLambertMaterial({ map: padT }), 9);
  { const rp = K.rng(44); for (let i = 0; i < 9; i++) { let x = -9 + rp() * 6.5, z = -1.2 + rp() * 4, s = .3 + rp() * .35; if (i === 0) { x = -2.6; z = -2.1; s = .62; } Q4.setFromEuler(E4.set(0, rp() * 6.28, 0)); V4.set(x, .012, z); S4.set(s, 1, s); M4.compose(V4, Q4, S4); padI.setMatrixAt(i, M4); } }
  S.add(padI); padI.layers.set(1);
  // far shore: one dark tree-line silhouette strip (cheap: a single unlit band with a ragged top)
  { const NTS = 720, P = [], I = [], rt2 = K.rng(71); for (let i = 0; i <= NTS; i++) { const a = Math.PI * (.05 + 1.05 * i / NTS), r = 95, x = -Math.cos(a) * r - 5, z = -Math.sin(a) * r * .9 - 4;
      const hh = 3 + 3 * fbm(i * .05, 1, 0) + 3 * Math.pow(Math.abs(Math.sin(i * .9 + rt2() * 2)), 3) + 1.5 * rt2(); P.push(x, -2, z, x, hh, z); if (i < NTS) { const b = i * 2; I.push(b, b + 2, b + 1, b + 1, b + 2, b + 3); } }
    const tg = new T.BufferGeometry(); tg.setAttribute('position', new T.Float32BufferAttribute(P, 3)); tg.setIndex(I);
    var trees = new T.Mesh(tg, new T.MeshBasicMaterial({ color: NIGHT ? '#04060e' : '#1a2418', side: T.DoubleSide })), blobs = trees; S.add(trees); }

  // ---------------- water ----------------
  const RW = Math.round(ctx.W / 3), RH = Math.round(ctx.H / 3), rt = new T.WebGLRenderTarget(RW, RH, { colorSpace: T.SRGBColorSpace }); rt.isXRRenderTarget = true;   // same tone-mapped program variants as the screen pass (one compile per material); holds display values
  const mcam = new T.PerspectiveCamera(), texM = new T.Matrix4();
  const rings = []; for (let i = 0; i < 4; i++) rings.push(new T.Vector4(0, 0, -99, 0));
  const waterM = new T.ShaderMaterial({ side: T.DoubleSide, fog: true, lights: false, toneMapped: false,
    uniforms: T.UniformsUtils.merge([T.UniformsLib.fog, { tR: { value: null }, mR: { value: new T.Matrix4() }, uT: { value: 0 }, uAmp: { value: 1 }, deep: { value: col(PAL.deep) }, fogD: { value: col(PAL.fog) },
      win: { value: col(NIGHT ? '#4a5aa0' : '#b8d8b0') }, uw: { value: col('#03140f') }, rings: { value: rings } }]),
    vertexShader: `varying vec3 vW;
      #include <fog_pars_vertex>
      void main(){ vec4 w = modelMatrix*vec4(position,1.); vW=w.xyz; vec4 mvPosition = viewMatrix*w; gl_Position=projectionMatrix*mvPosition;
      #include <fog_vertex>
      }`,
    fragmentShader: `uniform sampler2D tR; uniform mat4 mR; uniform float uT,uAmp; uniform vec3 deep,win,uw,fogD; uniform vec4 rings[4]; varying vec3 vW;
      #include <fog_pars_fragment>
      vec2 wave(vec2 p){ vec2 g=vec2(0.);
        g += .010*vec2(.8,.6)*cos(dot(p,vec2(.8,.6))*2.1+uT*1.3);
        g += .008*vec2(-.5,.86)*cos(dot(p,vec2(-.5,.86))*3.3+uT*1.7);
        g += .005*vec2(.95,-.3)*cos(dot(p,vec2(.95,-.3))*6.1+uT*2.3);
        g += .003*vec2(.2,.98)*cos(dot(p,vec2(.2,.98))*11.+uT*3.1);
        g *= uAmp;
        for(int i=0;i<4;i++){ vec4 r=rings[i]; if(r.z<0.) continue; vec2 d=p-r.xy; float l=length(d)+1e-4; float a=r.z, f=l-a*.55;
          g += r.w*exp(-a*.9)*exp(-f*f*6.)*cos(f*26.)*d/l*.05; }
        return g; }
      void main(){ vec2 g=wave(vW.xz); vec3 N=normalize(vec3(-g.x,1.,-g.y)); vec3 V=normalize(cameraPosition-vW); vec3 c;
        if(gl_FrontFacing){ vec4 pc=mR*vec4(vW.x,0.,vW.z,1.); pc.xy += N.xz*.5*pc.w*.25; vec3 rf=texture2DProj(tR,pc).rgb;
          float f=.02+.98*pow(1.-max(dot(N,V),0.),5.); c=mix(sqrt(deep), rf, clamp(f*1.05+.08,0.,1.)); }
        else { vec3 d=-V; float k=smoothstep(.42,.62,d.y); float rip=.5+.5*sin(vW.x*9.+g.x*300.+uT*1.5)*sin(vW.z*8.-g.y*300.+uT*1.1); c=sqrt(mix(uw, win*(.7+.6*rip), k)); }
        #ifdef USE_FOG
          float fogF = 1.0 - exp( - fogDensity * fogDensity * vFogDepth * vFogDepth );
          c = mix(c, gl_FrontFacing ? sqrt(fogD) : pow(fogColor, vec3(1./2.2)) * .8, fogF);
        #endif
        gl_FragColor=vec4(c,1.);   // display space: the reflection target already holds tone-mapped sRGB
      }` });
  const water = new T.Mesh(new T.PlaneGeometry(900, 900), waterM); water.rotation.x = -Math.PI / 2; water.frustumCulled = false; water.renderOrder = -1; S.add(water);
  function mirror(cam) {
    mcam.copy(cam); mcam.layers.set(0); mcam.position.set(cam.position.x, -cam.position.y, cam.position.z);
    const tgt = new T.Vector3(0, 0, -1).applyQuaternion(cam.quaternion).add(cam.position); tgt.y = -tgt.y; const up = new T.Vector3(0, 1, 0).applyQuaternion(cam.quaternion); up.y = -up.y;
    mcam.up.copy(up); mcam.lookAt(tgt); mcam.updateMatrixWorld(); mcam.projectionMatrix.copy(cam.projectionMatrix);
    texM.set(.5, 0, 0, .5, 0, .5, 0, .5, 0, 0, .5, .5, 0, 0, 0, 1); texM.multiply(mcam.projectionMatrix); texM.multiply(mcam.matrixWorldInverse); waterM.uniforms.mR.value.copy(texM);
    // oblique near plane = the water surface (iq/Lengyel, as in three's Reflector)
    const pl = new T.Plane(new T.Vector3(0, 1, 0), 0); pl.applyMatrix4(mcam.matrixWorldInverse); const cp = new T.Vector4(pl.normal.x, pl.normal.y, pl.normal.z, pl.constant), pm = mcam.projectionMatrix, q = new T.Vector4();
    q.x = (Math.sign(cp.x) + pm.elements[8]) / pm.elements[0]; q.y = (Math.sign(cp.y) + pm.elements[9]) / pm.elements[5]; q.z = -1; q.w = (1 + pm.elements[10]) / pm.elements[14];
    cp.multiplyScalar(2 / cp.dot(q)); pm.elements[2] = cp.x; pm.elements[6] = cp.y; pm.elements[10] = cp.z + 1 - .003; pm.elements[14] = cp.w; mcam.projectionMatrixInverse.copy(pm).invert();
    water.visible = false; const old = R.getRenderTarget(); R.setRenderTarget(rt); R.clear(); R.render(S, mcam); R.setRenderTarget(old); water.visible = true; waterM.uniforms.tR.value = rt.texture;
  }

  // ---------------- night mist: thin drifting sheets just above the water ----------------
  const mists = [];
  if (NIGHT) for (let i = 0; i < 5; i++) { const nz = K.noise(256, { seed: 40 + i, octaves: 4, sx: 3, sy: 3 }), mt = K.tex(nz, true, [2, 2]);
    const m = new T.Mesh(new T.PlaneGeometry(36, 30), new T.MeshBasicMaterial({ map: mt, color: '#7d8fd0', transparent: true, opacity: .1 - i * .012, blending: T.AdditiveBlending, depthWrite: false, fog: false }));
    m.rotation.x = -Math.PI / 2; m.position.set(-4, .06 + i * .07, -8); m.renderOrder = 2; S.add(m); mists.push(m); }
  // ---------------- night life: fireflies and the prey ----------------
  const NF = NIGHT ? 220 : 0, ff = NIGHT ? ctx.points(NF, { size: .11, color: '#f0f080' }) : null, ffd = [];
  if (NIGHT) { const rf = K.rng(91); for (let i = 0; i < NF; i++) { const near = i < 40; ffd.push([near ? -4 + rf() * 7 : -18 + rf() * 28, near ? .3 + rf() * 1.6 : .3 + rf() * 4, near ? -3.5 + rf() * 2.8 : -12 + rf() * 10, rf() * 6.28, .5 + rf() * .8, rf()]); } S.add(ff); }
  const ffHalo = NIGHT ? ctx.points(1, { size: .01, opacity: 0 }) : null;
  // the prey: a firefly, ONE mesh (body + wing covers + wings merged), lantern glow and a small warm light
  let prey = null;
  if (NIGHT) { const wings = [1, -1].map(sd => { const w = K.fin([[0, 0], [.03, .04], [.12, .05], [.2, .02], [.21, -.01], [.12, -.02], [.03, -.015]].map(([x, y]) => [-x, y]), .004); w.rotateX(Math.PI / 2); w.translate(.0, .025, sd * .06); w.userData.v = .3; return w; });
    const pb = K.body({ length: .26, seg: 30, ring: 12, belly: .1, extra: wings, width: s => .02 + .035 * Math.pow(Math.sin(Math.PI * Math.min(1, s * 1.05)), .7), height: s => .02 + .03 * Math.pow(Math.sin(Math.PI * Math.min(1, s * 1.05)), .7) });
    const pt = ctx.ctex(64, (g, z) => { const gr = g.createLinearGradient(0, 0, z, 0); gr.addColorStop(0, '#f8ff9a'); gr.addColorStop(.32, '#e8f070'); gr.addColorStop(.36, '#2a1c14'); gr.addColorStop(.8, '#3a2618'); gr.addColorStop(.86, '#c86040'); gr.addColorStop(1, '#201410'); g.fillStyle = gr; g.fillRect(0, 0, z, z); });
    const pm = new T.Mesh(pb.geo, new T.MeshStandardMaterial({ map: pt, emissiveMap: pt, emissive: new T.Color('#ffffff'), emissiveIntensity: .6, roughness: .5 }));
    const grp = new T.Group(); grp.add(pm); grp.scale.setScalar(.75); S.add(grp);
    const gl1 = ctx.glow(grp, '#e8ff80', 1.2, .5), gl2 = ctx.glow(grp, '#fff4b0', .35, .9); gl1.position.x = gl2.position.x = -.09;
    const pl = new T.PointLight('#f0e070', 0, 3, 1.5); grp.add(pl); pl.position.x = -.1;
    prey = { grp, pb, gl1, gl2, pl }; }

  // ---------------- day life: dragonflies ----------------
  const flies = [];
  if (!NIGHT) {
    const bodyT = ctx.ctex(256, (g, z) => { const gr = g.createLinearGradient(0, 0, z, 0); gr.addColorStop(0, '#0a2a5a'); gr.addColorStop(.7, '#1e6ac0'); gr.addColorStop(.72, '#2a6a3a'); gr.addColorStop(.9, '#3a8a40'); gr.addColorStop(.93, '#1a3a8a'); gr.addColorStop(1, '#1a3a8a'); g.fillStyle = gr; g.fillRect(0, 0, z, z);
      g.fillStyle = 'rgba(5,10,20,.8)'; for (let k = 0; k < 9; k++) g.fillRect(k / 9 * .7 * z, 0, 3, z); });
    for (let f = 0; f < 3; f++) {
      const wing = (x0, L, W, sd) => { const w = K.fin([[0, 0], [L * .15, W * .5], [L * .6, W * .55], [L * .95, W * .35], [L, 0], [L * .7, -W * .25], [L * .2, -W * .3]], .006); w.rotateX(Math.PI / 2); w.rotateY(-sd * Math.PI / 2); w.translate(x0, .03, sd * (L / 2 + .02)); w.userData.v = .5; return w; };
      const ws = [wing(.22, .4, .09, 1), wing(.22, .4, .09, -1), wing(.13, .38, .1, 1), wing(.13, .38, .1, -1)];
      const prof = s => s > .92 ? .055 * Math.sin(Math.PI * Math.min(1, (s - .92) / .08 * .5 + .5)) + .01 : s > .76 ? .04 : .013 + .005 * Math.sin(s * 40);
      const db = K.body({ length: .9, seg: 70, ring: 10, belly: .05, extra: ws, width: s => prof(s), height: s => prof(s) * (s > .92 ? .8 : 1) });
      const nbI = 70 * 10 * 6; db.geo.addGroup(0, nbI, 0); db.geo.addGroup(nbI, db.geo.index.count - nbI, 1);
      const dm = new T.Mesh(db.geo, [new T.MeshStandardMaterial({ envMap: ENV, map: bodyT, metalness: .6, roughness: .28, envMapIntensity: 1 }),
        new T.MeshStandardMaterial({ envMap: ENV, color: '#e8f0ff', transparent: true, opacity: .25, roughness: .1, metalness: .3, side: T.DoubleSide, depthWrite: false, envMapIntensity: 1.5 })]);
      dm.frustumCulled = false; const grp = new T.Group(); grp.add(dm); S.add(grp); flies.push({ grp, db, ph: f * 2.1 });
    }
  }

  // ---------------- underwater (day): tadpoles, specks, light shafts ----------------
  const tads = [];
  let shafts = null, specks = null;
  if (!NIGHT) {
    const tt = ctx.ctex(256, (g, z) => { const gr = g.createLinearGradient(0, 0, z, 0); gr.addColorStop(0, '#3a3a22'); gr.addColorStop(.55, '#4a4428'); gr.addColorStop(.62, '#2a2414'); gr.addColorStop(1, '#2e2a18'); g.fillStyle = gr; g.fillRect(0, 0, z, z);
      const rr = K.rng(5); for (let i = 0; i < 260; i++) { g.fillStyle = `rgba(${rr() < .5 ? '200,170,90' : '10,8,4'},${.3 + rr() * .4})`; g.beginPath(); g.arc(rr() * z, rr() * z, 1 + rr() * 2.5, 0, 6.283); g.fill(); } });
    tt.flipY = false;
    [[1, 0], [.8, 1], [.65, 2]].forEach(([sc, n]) => {
      const legs = n === 0 ? [1, -1].map(sd => { const l = K.fin([[0, 0], [.08, .02], [.16, -.01], [.2, .03], [.22, -.02], [.15, -.03], [.06, -.025]], .018); l.rotateX(Math.PI / 2); l.rotateY(sd * .9); l.translate(-.08, -.07, sd * .12); l.userData.v = .7; return l; }) : [];
      const env = s => Math.pow(Math.sin(Math.PI * Math.min(1, Math.max(0, (s - .56) / .44))), .6);   // ovoid head-body
      const tH = s => (.012 + .12 * Math.pow(Math.min(1, s / .6), .8)) * (1 - sm(.6, .8, s)), tW = s => .006 + .03 * Math.min(1, s / .6);   // tail muscle + fin, tapering to a point
      const tb = K.body({ length: 1.1, seg: 90, ring: 24, belly: .25, extra: legs, width: s => Math.max(tW(s), .17 * env(s)), height: s => Math.max(tH(s), .02 + .13 * env(s)) });
      const tm = new T.Mesh(tb.geo, new T.MeshStandardMaterial({ map: tt, roughness: .35, envMapIntensity: .5 }));
      const grp = new T.Group(); grp.add(tm); grp.scale.setScalar(sc);
      [1, -1].forEach(sd => { const e = new T.Mesh(new T.SphereGeometry(.035, 16, 12), new T.MeshStandardMaterial({ envMap: ENV, color: '#050403', roughness: .05, envMapIntensity: 1 })); e.position.set(.4, .07, sd * .125); grp.add(e); });
      S.add(grp); tads.push({ grp, tb, n }); });
    shafts = K.shafts(S, { n: 12, top: 0, height: 7, width: .7, spread: 14, depth: 12, opacity: .32, color: '#c8f0b0', seed: 4 }); shafts.group.position.set(-1, 0, 1);
    specks = K.snow(S, { n: 1800, box: [10, 4, 10], size: .03, opacity: .5, fall: .02, color: '#d8f0c0' });
  }

  // ---------------- camera ----------------
  const cam = new T.PerspectiveCamera(NIGHT ? 36 : 38, ctx.W / ctx.H, .03, 1500); ctx.side(cam, p.side == null ? .12 : p.side); cam.layers.enable(1);
  function path(keys) { return t => { const n = keys.length; if (t <= keys[0][0]) return keys[0][1]; if (t >= keys[n - 1][0]) return keys[n - 1][1];
    let i = 0; while (keys[i + 1][0] < t) i++; const [t0, a] = keys[i], [t1, b] = keys[i + 1], u = (t - t0) / (t1 - t0), pa = keys[Math.max(0, i - 1)], pb = keys[Math.min(n - 1, i + 2)];
    const h00 = 2 * u * u * u - 3 * u * u + 1, h10 = u * u * u - 2 * u * u + u, h01 = -2 * u * u * u + 3 * u * u, h11 = u * u * u - u * u;
    return a.map((v, j) => { const m0 = i > 0 ? (b[j] - pa[1][j]) / (t1 - pa[0]) * (t1 - t0) : 0, m1 = i + 2 < n ? (pb[1][j] - a[j]) / (pb[0] - t0) * (t1 - t0) : 0; return h00 * v + h10 * m0 + h01 * b[j] + h11 * m1; }); }; }
  const T0 = ctx.t0, T1 = ctx.t1;
  let camPath;
  if (NIGHT) { const cI = cue(p.insect, T0 + 6), cT = cue(p.tongue, T0 + 11.5), cR = cue(p.reveal, T0 + 14);
    camPath = path([[T0, [2.2, 1.15, 6.2, -.3, .5, -.4]], [cI, [1.25, .7, 3.6, -.45, .52, -.1]], [cT - 1.2, [1.0, .66, 3.05, -.5, .46, 0]], [cT + 1.5, [.9, .64, 2.95, -.55, .46, 0]],
      [cR + .5, [.95, .68, 3.1, -.55, .48, -.05]], [T1, [2.9, 2.0, 8.4, -1.4, .7, -.8]]]); }
  else { const cF = cue(p.flies, T0 + 6), cS = cue(p.still, T0 + 11), cW = cue(p.wide, T0 + 13), cK = cue(p.sink, T0 + 16);
    camPath = path([[T0, [4.6, .75, 4.4, .6, .55, -.6]], [cF, [1.9, .7, 4.2, -.3, .55, -.3]], [cS, [.9, .6, 3.4, -.5, .48, -.1]], [cW, [.8, .62, 3.3, -.55, .5, 0]],
      [cK, [1.3, 1.1, 5.0, -.8, .45, -.4]], [cK + 1.1, [.9, .1, 4.4, -.9, -.15, .4]], [cK + 2.2, [.6, -1.1, 4.3, -1.0, -.6, 1.6]], [T1, [.3, -1.3, 3.8, -1.4, -.35, 1.5]]]); }

  const tmpV = new T.Vector3(), tip = new T.Vector3();
  return { scene: S, camera: cam, draw(t, u) {
    uT.value = t; waterM.uniforms.uT.value = t;
    mists.forEach((m, i) => { m.material.map.offset.set(t * .006 * (i + 1), t * .004 * (2 - i * .3)); });
    const c = camPath(t); cam.position.set(c[0], c[1], c[2]); cam.lookAt(c[3], c[4], c[5]); cam.updateMatrixWorld();
    rimDir.value.copy(key.position).normalize().transformDirection(cam.matrixWorldInverse);
    const under = cam.position.y < 0;
    // atmosphere above / below the surface
    if (under) { S.fog.color.copy(UWC); S.fog.density = .2; hemi.intensity = .25; key.intensity = PAL.keyI * .25; }
    else { S.fog.color.copy(FOGC); S.fog.density = PAL.fogD; hemi.intensity = PAL.hemiI; key.intensity = PAL.keyI; }
    dome.visible = !under; S.background = under ? UWC : null;
    // water: gentle wind ripples; the day water goes still on the cue
    const still = NIGHT ? 0 : at(p.still, 2.5, t); waterM.uniforms.uAmp.value = NIGHT ? .9 : 1.0 - .93 * still;
    const RS = NIGHT ? [[-1.3, 1.2, 3.1, 0], [-3, -.4, 4.3, 1.2], [.9, .6, 3.7, 2.1], [-6, 1, 5.2, .4], [-2.2, 2.6, 4.7, 3.3]] : [[-1.4, 1.0, 3.4, 0], [-3.2, -.2, 4.1, 1.5], [1.2, .8, 3.9, 2.7]];
    for (let i = 0; i < 4; i++) { const r = RS[i]; if (!r) { rings[i].z = -99; continue; } const age = ((t - r[3]) % r[2] + r[2]) % r[2]; rings[i].set(r[0], r[1], age, NIGHT ? .7 : (1 - still)); }
    // frog: breathing, a slight lean before the strike, the tongue
    let jawA = 0, tg = null;
    if (NIGHT) {
      const cI = cue(p.insect, T0 + 6), cM = cue(p.moves, T0 + 10), cT = cue(p.tongue, T0 + 11.5);
      const k = t - cT, ext = k < 0 ? 0 : k < .2 ? sm(0, .2, k) : k < .3 ? 1 : 1 - sm(.3, .62, k);
      jawA = k < -.05 ? 0 : k < .62 ? .2 * sm(-.05, .06, k) * (1 - sm(.5, .66, k)) : 0;
      frog.rotation.z = -.07 * sm(cT - 1.2, cT - .2, t) * (1 - sm(cT + .5, cT + 1.5, t)) + .012 * Math.sin(t * .7);
      frog.updateMatrixWorld();
      // prey path (frog space -> world): drifts in, hovers, darts in front of the frog, then rides the tongue home
      const strikeP = new T.Vector3(.9, .62, -.08), hover = new T.Vector3(1.0 + .1 * Math.sin(t * 1.7), .88 + .08 * Math.sin(t * 2.3), .12 + .2 * Math.sin(t * 1.1)), far = new T.Vector3(.1 + .2 * Math.sin(t), 1.25 + .1 * Math.sin(t * 1.3), -1.3);
      const lp = far.clone().lerp(hover, sm(cI, cI + 3.5, t)).lerp(strikeP.clone().add(new T.Vector3(.04 * Math.sin(t * 9), .03 * Math.sin(t * 11), 0)), sm(cM, cM + .9, t));
      const caught = k >= .2; let A;
      if (caught) { A = frogPose(t, jawA, { e: ext, tip: strikeP }); tip.copy(A).lerp(strikeP, ext); } else { const tipL = lp.clone(); A = frogPose(t, jawA, ext > 0 ? { e: ext, tip: tipL } : null); tip.copy(lp); }
      const pw = frog.localToWorld(tip.clone()); prey.grp.position.copy(pw);
      const gone = caught && ext < .25; prey.grp.visible = !gone && t > cI - .5;
      const fl = (.55 + .45 * Math.pow(Math.max(0, Math.sin(t * 2.6)), 3)) * sm(cI - .5, cI + 1, t);
      prey.gl1.material.opacity = .45 * fl; prey.gl2.material.opacity = .9 * fl; prey.pl.intensity = gone ? 0 : 7 * fl; prey.grp.lookAt(frog.localToWorld(new T.Vector3(.4, .45, 0))); prey.grp.rotateY(-Math.PI / 2);
      prey.pb.deform((s, th, base, kk) => { if (th >= 0) return [0, 0, 0]; const z = base[kk * 3 + 2], a = .7 * Math.sin(t * 60) * (caught ? 0 : 1); return [0, Math.abs(z) * Math.sin(a), Math.sign(z) * Math.abs(z) * (Math.cos(a) - 1)]; });
      // eyes pull in as it swallows
      const sw = sm(cT + .6, cT + .9, t) * (1 - sm(cT + 1.6, cT + 2.2, t)); eyes.forEach(e => { e.position.y = .535 - .028 * sw; });
      // fireflies
      const fa = ff.geometry.attributes.position.array, fc = ff.geometry.attributes.color.array;
      for (let i = 0; i < NF; i++) { const [x, y, z, ph, sp, o] = ffd[i]; const px = x + Math.sin(t * .23 * sp + ph) * .8, py = y + Math.sin(t * .31 * sp + ph * 2) * .3, pz = z + Math.cos(t * .19 * sp + ph) * .6;
        const b = Math.pow(Math.max(0, Math.sin(t * (1 + o) + ph * 3)), 6) * (.4 + o); fa.set([px, py, pz], i * 3); fc.set([b * 1.2, b * 1.3, b * .55], i * 3); }
      ff.geometry.attributes.position.needsUpdate = ff.geometry.attributes.color.needsUpdate = true;
    } else {
      frog.rotation.z = .01 * Math.sin(t * .6); frogPose(t, 0, null);
      const cF = cue(p.flies, T0 + 6);
      flies.forEach((f, i) => { const tt = t - cF + 1.5 - i * .9, q = Math.max(0, tt);
        const P = s => new T.Vector3(-1.6 + i * 1.1 + s * .38 + .5 * Math.sin(s * .7 + f.ph), .75 + i * .3 + .15 * Math.sin(s * 1.3 + f.ph) + .08 * Math.sin(s * 3.1), -.9 - i * .9 + .5 * Math.sin(s * .5 + f.ph * 2));
        const a = P(q), b = P(q + .08); f.grp.position.copy(a); f.grp.visible = tt > 0; tmpV.subVectors(b, a); if (tmpV.lengthSq() > 1e-8) { f.grp.lookAt(b); f.grp.rotateY(-Math.PI / 2); }
        f.db.deform((s, th, base, k) => { if (th >= 0) return [0, .01 * Math.sin(s * 3 + t * 2) * (1 - s), 0]; const x = base[k * 3], z = base[k * 3 + 2], az = Math.abs(z), front = x > .19 ? 0 : 1.6;
          const a = .55 * Math.sin(t * 52 + front + f.ph); return [0, az * Math.sin(a), Math.sign(z) * az * (Math.cos(a) - 1)]; }); });
      tads.forEach((td, i) => { const sw = t * (4.5 + i) + i; const C = [[-1.45, -.72, 1.65], [-1.75, -.95, 2.0], [-2.0, -.52, .7]][i], v = [.13, .1, .16][i], P = s => { const q = (s - 20) * v + .06 * Math.sin(s * .9 + i); return new T.Vector3(C[0] + .8 * q, C[1] + .05 * Math.sin(s * .7 + i * 2), C[2] - .6 * q + .04 * Math.sin(s * 1.1 + i)); };
        const a = P(t), b = P(t + .05); td.grp.position.copy(a); td.grp.lookAt(b); td.grp.rotateY(-Math.PI / 2); td.grp.visible = cam.position.y < .4;
        td.tb.deform((s, th, base, k) => [0, 0, .09 * Math.pow(1 - Math.min(s, .9), 2) * Math.sin(sw - (1 - s) * 7)]); });
      if (shafts) { shafts.update(t, under ? 1 : 0); shafts.group.visible = under; specks.update(t, [cam.position.x, -1.5, cam.position.z]); specks.points.visible = under; }
    }
    // planar reflection (only when the camera is above the water)
    if (!under) mirror(cam);
  } };
};
