// cosmicweb — the 3D cosmic web (S06, S08) and the Boötes Void / cosmic shoreline (S39-S40).
// Built once from a seeded Voronoi foam: ~70k soft galaxy points (warm gold, violet, white) sit on the walls, filaments and nodes
// between empty cells; clusters glow at the nodes (a separate soft layer), a diffuse glow layer lights the filaments; one cell is
// a huge supervoid (additively weighted, so it is round) holding exactly 60 lonely galaxies, and one side of its rim is a dense,
// bright wall (the "shoreline"). Our home spiral galaxy sits on a filament with a small Local Group around it (a second large
// spiral, a small one, dwarfs). Every layer is one Points draw call with a soft sprite; points never get smaller than ~1.6 px
// (dimmer instead, energy kept), so nothing crawls or flickers when the camera moves. Symbolic scale.
// params:
//   look    — 'web' (default) or 'void' (the camera floats inside the supervoid: a few lonely galaxies, the walls far away)
//   zoom    — cue (S06): the camera pulls back from one spiral galaxy, past the Local Group, out to the whole web
//             (default for look 'web' with no zoom: the pull-back starts 0.3 s into the shot)
//   speck   — cue (S08): far zoom-out, the whole web shrinks to a dust-like patch in black
//   shore   — cue (S40, look 'void'): the camera turns and drifts toward the bright wall of galaxies at the void's edge
//   recede  — cue (S40 "the shoreline is receding"): the far galaxies drift outward and go dark one by one
//   side (.12)
// 2026-10-16 staging pass (no new params): before the zoom the camera slowly orbits the home galaxy; on the pull-back the real web
//   galaxies that pass the camera are drawn as motion streaks (screen length capped, kept off the title block), a fly-through; speck:
//   a warm glint marks home with one slow ring, dust specks drift close to the lens; void: lone galaxies turn slowly; shore: the
//   camera glides along the wall and edges toward it, and a slow wave of light runs along the shoreline (then softer every 16 s).
(window.MIYA = window.MIYA || { scenes: {} }).scenes.cosmicweb = function (ctx, p) {
  const { T, sm, rng, cue, dotTex } = ctx;
  const S = new T.Scene(); S.background = new T.Color('#02030a');
  const v3 = (x, y, z) => new T.Vector3(x, y, z);
  const vf = f => { if (!ctx.VERT) return f; const h = 2 * Math.atan(Math.tan(f * Math.PI / 360) * 16 / 9 * .62); return 2 * Math.atan(Math.tan(h / 2) * ctx.H / ctx.W) * 180 / Math.PI; };
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), ctx.t);
  const LOOK = p.look === 'void' ? 'void' : 'web';

  // motion streaks (copied from lightspeed.js, 2026-10-16 speed pass): camera-facing quads billboarded in the vertex shader, bright
  // head, fading tail, width never below minPx pixels (thinner ones dim instead). set(i, head, tail, width, rgb) each frame from t only.
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
  // ---------------- sky ----------------
  const skyU = { uK: { value: 1 } };
  const sky = new T.Mesh(new T.SphereGeometry(1, 40, 20), new T.ShaderMaterial({ uniforms: skyU, side: T.BackSide, depthWrite: false, depthTest: false,
    vertexShader: `varying vec3 vD; void main(){ vD = position; vec4 q = projectionMatrix * vec4(mat3(viewMatrix) * position, 1.0); gl_Position = vec4(q.xy, q.w * .99999, q.w); }`,
    fragmentShader: `varying vec3 vD; uniform float uK; void main(){ vec3 d = normalize(vD);
      vec3 c = mix(vec3(.006,.006,.018), vec3(.016,.014,.042), .5 + .5 * d.y) * uK + vec3(.002,.002,.005);
      gl_FragColor = vec4(c, 1.);
      #include <tonemapping_fragment>
      #include <colorspace_fragment>
    }` }));
  sky.frustumCulled = false; sky.renderOrder = -10; S.add(sky);

  // ---------------- soft point material (min pixel size with energy kept, near fade, recede) ----------------
  const shared = { uScale: { value: 1000 }, uRec: { value: 0 }, uVC: { value: new T.Vector3() }, uRV: { value: 60 } };
  const swU = { uSwD: { value: new T.Vector3(1, 0, 0) }, uSwP: { value: 0 }, uSwA: { value: 0 } };   // shoreline light sweep (2026-10-16)
  function ptsMat(op, minPx, maxPx, near, sweep) { return new T.ShaderMaterial({ transparent: true, depthWrite: false, blending: T.AdditiveBlending,
    uniforms: { uScale: shared.uScale, uRec: shared.uRec, uVC: shared.uVC, uRV: shared.uRV, uSwD: swU.uSwD, uSwP: swU.uSwP, uSwA: swU.uSwA, uSw: { value: sweep ? 1 : 0 }, uOp: { value: op }, uMin: { value: minPx }, uMax: { value: maxPx }, uNear: { value: near || 0 } },
    vertexShader: `attribute vec3 color; attribute float size; attribute float rnd; uniform float uScale, uMin, uMax, uOp, uRec, uNear, uRV, uSwP, uSwA, uSw; uniform vec3 uVC, uSwD;
      varying vec3 vC; varying float vA;
      void main(){ vec3 p = position; float far = 0.;
        if (uRec > 0.) { vec3 o = p - uVC; far = smoothstep(uRV * .92, uRV * 1.3, length(o)); p = uVC + o * (1. + .35 * uRec * far); }
        vec4 mv = modelViewMatrix * vec4(p, 1.); float z = max(-mv.z, 1e-5), ps = size * uScale / z, a = uOp;
        if (ps < uMin) { a *= ps * ps / (uMin * uMin); ps = uMin; }
        if (ps > uMax) { a *= uMax / ps; ps = uMax; }
        if (uNear > 0.) a *= smoothstep(uNear * .4, uNear, z);
        if (uSw > 0.) a *= 1. + uSwA * exp(-pow((dot(p - uVC, uSwD) - uSwP) / 9., 2.));
        a *= 1. - far * smoothstep(rnd - .12, rnd, uRec * 1.12);
        vC = color; vA = a; gl_PointSize = ps; gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `varying vec3 vC; varying float vA; void main(){ vec2 q = gl_PointCoord - .5; float r2 = dot(q, q) * 4.; float a = exp(-r2 * 3.2) * (1. - smoothstep(.7, 1., r2));
      gl_FragColor = vec4(vC * a * vA, 1.);
      #include <tonemapping_fragment>
      #include <colorspace_fragment>
    }` }); }
  function layer(arr, mat) { const n = arr.length / 8, g = new T.BufferGeometry(), P = new Float32Array(n * 3), C = new Float32Array(n * 3), Z = new Float32Array(n), R = new Float32Array(n);
    for (let i = 0; i < n; i++) { const k = i * 8; P.set([arr[k], arr[k + 1], arr[k + 2]], i * 3); C.set([arr[k + 3], arr[k + 4], arr[k + 5]], i * 3); Z[i] = arr[k + 6]; R[i] = arr[k + 7]; }
    g.setAttribute('position', new T.BufferAttribute(P, 3)); g.setAttribute('color', new T.BufferAttribute(C, 3)); g.setAttribute('size', new T.BufferAttribute(Z, 1)); g.setAttribute('rnd', new T.BufferAttribute(R, 1));
    const o = new T.Points(g, mat); o.frustumCulled = false; S.add(o); return o; }

  // ---------------- the web: seeded Voronoi foam, rejection-sampled ----------------
  const R0 = rng(p.seed || 17), RW = 200, seeds = [];
  let VC = v3(95, 18, -55); const VW = 34, RV = 55;                 // supervoid seed, its weight, its rough radius
  while (seeds.length < 110) { const s = v3((R0() * 2 - 1) * 250, (R0() * 2 - 1) * 250, (R0() * 2 - 1) * 250); if (s.length() < 260 && s.distanceTo(VC) > RV + 12) seeds.push(s); }
  seeds.push(VC.clone()); const NSd = seeds.length, VI = NSd - 1, sx = new Float32Array(NSd * 3); seeds.forEach((s, i) => sx.set([s.x, s.y, s.z], i * 3));
  let SH = v3(-.2, -.85, .45).normalize();                          // direction of the bright shoreline wall (from the void centre; below the camera)
  const GOLD = [1, .78, .44], VIO = [.6, .52, 1], WHT = [.88, .9, 1];
  const gal = [], glo = [], clu = [], shoreG = [];
  const MAXN = 64000; let tries = 0, best = null;
  const SW = i => i === VI ? VW : 0, NB4 = new Int32Array(4), ND4 = new Float64Array(4);
  function near4(x, y, z) { ND4.fill(1e9); NB4.fill(-1);
    for (let s = 0; s < NSd; s++) { const dx = x - sx[s * 3], dy = y - sx[s * 3 + 1], dz = z - sx[s * 3 + 2], d = Math.sqrt(dx * dx + dy * dy + dz * dz) - SW(s);
      if (d < ND4[3]) { let k = 3; while (k > 0 && d < ND4[k - 1]) { ND4[k] = ND4[k - 1]; NB4[k] = NB4[k - 1]; k--; } ND4[k] = d; NB4[k] = s; } } }
  // move P onto the (weighted) bisector plane of seeds a and b
  function proj(P, a, b) { const ax = sx[a * 3], ay = sx[a * 3 + 1], az = sx[a * 3 + 2]; let nx = sx[b * 3] - ax, ny = sx[b * 3 + 1] - ay, nz = sx[b * 3 + 2] - az;
    const Ln = Math.sqrt(nx * nx + ny * ny + nz * nz); nx /= Ln; ny /= Ln; nz /= Ln; const off = (Ln + SW(a) - SW(b)) / 2, tt = (P[0] - ax) * nx + (P[1] - ay) * ny + (P[2] - az) * nz - off;
    P[0] -= nx * tt; P[1] -= ny * tt; P[2] -= nz * tt; }
  const gauss = () => (R0() + R0() + R0() - 1.5) * 1.15;
  while (gal.length / 8 < MAXN && tries < 400000) { tries++;
    const P = [(R0() * 2 - 1) * RW, (R0() * 2 - 1) * RW, (R0() * 2 - 1) * RW]; if (P[0] * P[0] + P[1] * P[1] + P[2] * P[2] > RW * RW) continue;
    near4(P[0], P[1], P[2]); const s1 = NB4[0], s2 = NB4[1], s3 = NB4[2], s4 = NB4[3], q = R0(), kind = q < .5 ? 0 : q < .88 ? 1 : 2;   // wall, filament, node
    for (let it = 0; it < (kind ? 6 : 1); it++) { proj(P, s1, s2); if (kind) proj(P, s1, s3); if (kind === 2) proj(P, s1, s4); }
    const th = kind === 0 ? 1.1 : kind === 1 ? 1.5 : 2.6; P[0] += gauss() * th; P[1] += gauss() * th; P[2] += gauss() * th;
    const x = P[0], y = P[1], z = P[2], rr = Math.sqrt(x * x + y * y + z * z);
    near4(x, y, z); const set = kind === 0 ? [s1, s2] : kind === 1 ? [s1, s2, s3] : [s1, s2, s3, s4];
    if (set.indexOf(NB4[0]) < 0 || set.indexOf(NB4[1]) < 0) continue;
    if (R0() > sm(RW, RW - 45, rr)) continue;
    // the supervoid's rim facing SH is the bright "shoreline"
    let shore = 0; if (set.indexOf(VI) >= 0) { const ox = x - VC.x, oy = y - VC.y, oz = z - VC.z, ol = Math.sqrt(ox * ox + oy * oy + oz * oz) || 1; shore = sm(.35, .8, (ox * SH.x + oy * SH.y + oz * SH.z) / ol); }
    if (set.indexOf(VI) >= 0 && kind === 0 && shore < .2 && R0() < .5) continue;
    const tp = R0(), col = shore > .3 ? (tp < .85 ? GOLD : WHT) : tp < .55 ? GOLD : tp < .82 ? VIO : WHT;
    const br = (kind === 0 ? .32 + .45 * R0() : kind === 1 ? .55 + .8 * Math.pow(R0(), 2) : .8 + 1.1 * Math.pow(R0(), 2)) * (1 + .7 * shore);
    const isShore = set.indexOf(VI) >= 0 && shore > .3, A = isShore ? shoreG : gal;
    A.push(x, y, z, col[0] * br, col[1] * br, col[2] * br, .3 + .3 * R0(), R0());
    if (isShore) for (let k = 0; k < 2; k++) shoreG.push(x + gauss() * 2.2, y + gauss() * 2.2, z + gauss() * 2.2, col[0] * br, col[1] * br, col[2] * br, .3 + .3 * R0(), R0());
    if (kind && R0() < .05) glo.push(x, y, z, .08, .06, .12, 4 + 4 * R0(), R0());
    if (shore > .3 && R0() < .06) glo.push(x, y, z, .12, .09, .05, 5 + 4 * R0(), R0());
    if (kind === 2 && R0() < .05) clu.push(x, y, z, .5, .36, .2, 3 + 3 * R0(), R0());
    if (!best && kind === 1 && rr < 50 && v3(x, y, z).distanceTo(VC) > RV + 30) best = v3(x, y, z);
  }
  // our home sits on a filament: shift everything so that spot is the origin
  const HOME = best || v3(0, 0, 0);
  for (const A of [gal, glo, clu, shoreG]) for (let k = 0; k < A.length; k += 8) { A[k] -= HOME.x; A[k + 1] -= HOME.y; A[k + 2] -= HOME.z; }
  VC = VC.sub(HOME); shared.uVC.value.copy(VC);
  // the supervoid's 60 lonely galaxies
  // true radius of the supervoid cell along a direction (march until another seed is nearest)
  const rayR = d => { const c = VC.clone().add(HOME); for (let r = 4; r < 160; r += 1) { near4(c.x + d.x * r, c.y + d.y * r, c.z + d.z * r); if (NB4[0] !== VI) return r; } return 160; };
  const RSH = rayR(SH); let RVm = 0; for (let k = 0; k < 14; k++) { const a = k * 2.4, zz = 1 - 2 * (k + .5) / 14, q = Math.sqrt(1 - zz * zz); RVm += rayR(v3(q * Math.cos(a), zz, q * Math.sin(a))) / 14; }
  shared.uRV.value = RVm;
  const lone = [], RL = rng(23);
  for (let i = 0; i < 60; i++) { let o; do { o = v3(RL() * 2 - 1, RL() * 2 - 1, RL() * 2 - 1); } while (o.length() > 1 || o.length() < .05); const ol = o.length(); o.normalize(); o.multiplyScalar(ol * .85 * (rayR(o) - 4)).add(VC);
    lone.push(o); const c = RL() < .6 ? GOLD : WHT; gal.push(o.x, o.y, o.z, c[0] * 1.4, c[1] * 1.4, c[2] * 1.4, .5, 2); }
  const galL = layer(gal, ptsMat(1, 1.7, 5, 0)), shoreL = layer(shoreG, ptsMat(1, 1.7, 4.5, 0, true)), gloL = layer(glo, ptsMat(.5, 2, 26, 30)), cluL = layer(clu, ptsMat(.6, 2, 22, 30));
  // lonely galaxies seen up close inside the void: small oval sprites with a spiral smudge
  const lgT = ctx.ctex(128, (g, s) => { g.translate(s / 2, s / 2); const r = g.createRadialGradient(0, 0, 0, 0, 0, s / 2); r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(.12, 'rgba(255,240,220,.7)'); r.addColorStop(.5, 'rgba(200,190,255,.12)'); r.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = r; g.fillRect(-s / 2, -s / 2, s, s);
    g.strokeStyle = 'rgba(255,235,210,.22)'; g.lineWidth = 5; for (let a = 0; a < 2; a++) { g.beginPath(); for (let k = 0; k < 40; k++) { const th = k / 40 * 4 + a * Math.PI, rr = 6 + k * 1.15; k ? g.lineTo(Math.cos(th) * rr, Math.sin(th) * rr) : g.moveTo(Math.cos(th) * rr, Math.sin(th) * rr); } g.stroke(); } });
  const loneS = lone.map((o, i) => { const sp = new T.Sprite(new T.SpriteMaterial({ map: lgT, color: i % 3 ? '#ffe0b0' : '#d8d4ff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, rotation: RL() * 6.283 }));
    const s = .9 + RL() * 1.2; sp.scale.set(s, s * (.35 + .6 * RL()), 1); sp.position.copy(o); S.add(sp); return sp; });

  // ---------------- home spiral galaxy + Local Group (stars + a soft glow layer, each one draw call) ----------------
  function spiral(arr, c, nrm, R, n, seed, sz, glowArr) { const r = rng(seed), a = new T.Vector3(1, 0, 0); if (Math.abs(nrm.x) > .9) a.set(0, 1, 0);
    const e1 = a.clone().addScaledVector(nrm, -a.dot(nrm)).normalize(), e2 = new T.Vector3().crossVectors(nrm, e1);
    for (let i = 0; i < n; i++) { let x, y, z, col;
      if (r() < .2) { const q = Math.abs(r() + r() + r() - 1.5) * .22; const an = r() * 6.283; x = q * Math.cos(an) * 1.3; y = q * Math.sin(an) * .7; z = (r() + r() - 1) * .07 * (1 - q * 3); col = [1, .78, .48]; }
      else { const arm = Math.floor(r() * 2), rr = .1 + Math.pow(r(), .85) * .9, an = arm * Math.PI + Math.log(rr / .1) / Math.tan(.3) + (r() - .5) * .7 / (.35 + rr);
        x = rr * Math.cos(an); y = rr * Math.sin(an); z = (r() + r() - 1) * .02; const tp = r(); col = tp < .5 ? [.7, .76, 1] : tp < .78 ? [.76, .64, 1] : [1, .86, .62]; }
      const br = .5 + .9 * Math.pow(r(), 2), w = c.clone().addScaledVector(e1, x * R).addScaledVector(e2, y * R).addScaledVector(nrm, z * R);
      arr.push(w.x, w.y, w.z, col[0] * br * .3, col[1] * br * .3, col[2] * br * .3, sz * (.7 + .6 * r()), 0);
      if (glowArr && r() < .06) glowArr.push(w.x, w.y, w.z, col[0] * .08, col[1] * .08, col[2] * .08, sz * 14, 0); } }
  const home = [], homeG = [], HN = v3(.2, 1, .35).normalize();
  spiral(home, v3(0, 0, 0), HN, .25, 16000, 41, .0018, homeG);
  spiral(home, v3(1.35, .45, -.9), v3(-.5, .7, .4).normalize(), .3, 7000, 42, .0028, homeG);      // the big neighbour
  spiral(home, v3(.9, -.35, -.2), v3(.4, .8, -.3).normalize(), .09, 1500, 43, .0022, homeG);       // a small spiral
  { const r = rng(44); for (let d = 0; d < 26; d++) { const c = v3(r() * 2 - 1, r() * 2 - 1, r() * 2 - 1).multiplyScalar(1.6), s = .015 + .03 * r();
    for (let i = 0; i < 120; i++) { const q = v3(r() + r() - 1, r() + r() - 1, r() + r() - 1).multiplyScalar(s).add(c); home.push(q.x, q.y, q.z, .9, .82, .7, .003, 0); } } }
  const homeL = layer(home, ptsMat(1, 1.7, 9, 0)), homeGL = layer(homeG, ptsMat(.4, 2, 120, 0));
  const homeCore = ctx.glow(S, '#ffcf8a', .22, .5), andCore = ctx.glow(S, '#ffd9a8', .22, .35); andCore.position.set(1.35, .45, -.9);

  // ---------------- camera ----------------
  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .01, 1e5); ctx.side(cam, p.side == null ? .12 : p.side);
  function blend(a, b, w) { if (w <= 0) return a; if (w >= 1) return b;
    const d = Math.exp(Math.log(a.d) + (Math.log(b.d) - Math.log(a.d)) * w), k = Math.abs(b.d - a.d) > 1e-6 ? (d - a.d) / (b.d - a.d) : w;
    return { t: a.t.clone().lerp(b.t, Math.min(1, Math.max(0, k))), dir: a.dir.clone().lerp(b.dir, w).normalize(), d, fov: a.fov + (b.fov - a.fov) * w }; }
  const D0 = HN.clone().multiplyScalar(.62).add(v3(.55, .1, .55)).normalize();
  const WC = HOME.clone().negate(), zoomC = p.zoom != null ? p.zoom : (LOOK === 'web' && p.speck == null ? ctx.t0 + .3 : null);
  const LD0 = v3(.6, .15, -.8).normalize();
  const atT = (c, d, tt) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), tt);
  const TG = new T.Vector3().crossVectors(SH, v3(1, 0, 0)).normalize(), tSh = p.shore != null ? cue(p.shore) : 1e9, tSp = p.speck != null ? cue(p.speck) : 1e9;
  // camera state as a pure function of time (also sampled at build time to find the galaxies the zoom flies past)
  function camState(t) { const u = t - ctx.t0;
    const wZ = zoomC == null ? 1 : sm(cue(zoomC), cue(zoomC) + 8, t), wS = atT(p.speck, 6.5, t), wSh = atT(p.shore, 8, t);
    let st;
    if (LOOK === 'web') {
      const ang = u * .012, webDir = v3(Math.cos(.9 + ang), .42, Math.sin(.9 + ang)).normalize();
      // (2026-10-16) before the pull-back the camera slowly orbits the home galaxy (same tilt to its disc), never a frozen frame
      st = { t: v3(0, 0, 0), dir: D0.clone().applyAxisAngle(HN, u * .008), d: .85, fov: 40 };
      st = blend(st, { t: WC, dir: webDir, d: 650 - 40 * sm(cue(zoomC || 0) + 10, cue(zoomC || 0) + 60, t), fov: 42 }, wZ);
      st = blend(st, { t: WC.clone().multiplyScalar(.6), dir: webDir, d: 5200, fov: 38 }, wS);
    } else {
      // inside the supervoid: float in from near its edge toward the middle, slowly turning; "shore" turns to the bright wall
      const drift = sm(0, 40, u), yaw = u * .01, ld = LD0.clone().applyAxisAngle(v3(0, 1, 0), yaw);
      const pos = VC.clone().addScaledVector(LD0, -RVm * .3 * (1 - drift)).add(v3(0, 3 * Math.sin(u * .05), 0));
      st = { t: pos.clone().addScaledVector(ld, 40), dir: ld.clone().negate(), d: 40, fov: 46 };
      // shoreline: from inside the void near its rim, look along the wall (tangent), tilted a little toward it; (2026-10-16) the
      // camera now glides along the wall faster and edges toward it, so the near wall galaxies slide past with parallax
      const sd = TG.clone().multiplyScalar(Math.cos(.42)).addScaledVector(SH, Math.sin(.42)).normalize(), gl = sm(tSh, tSh + 40, t);
      const sp = VC.clone().addScaledVector(SH, RSH * .4 + 7 * sm(tSh + 2, tSh + 30, t)).addScaledVector(TG, -RSH * .25 + 22 * gl);
      st = blend(st, { t: sp.clone().addScaledVector(sd, 40), dir: sd.clone().negate(), d: 40, fov: 50 }, wSh);
    }
    st.wZ = wZ; st.wS = wS; st.wSh = wSh; return st; }
  const camPos = t => { const s = camState(t); return s.t.clone().addScaledVector(s.dir, s.d); };

  // ---------------- fly-through streaks (2026-10-16): the real web galaxies that pass close to the camera on the pull-back are
  // also drawn as motion streaks (tail = where the galaxy appeared a moment ago), so the zoom reads as a flight through the filaments
  const STK = []; let NST = 0, fly = null;
  if (LOOK === 'web' && zoomC != null) { const z0 = cue(zoomC), z1 = Math.min(ctx.t1 + .5, z0 + 14), NSP = 140, cps = [], cds = [];
    for (let k = 0; k <= NSP; k++) { const s = camState(z0 + (z1 - z0) * k / NSP); cps.push(s.t.clone().addScaledVector(s.dir, s.d)); cds.push(s.d); }
    const cand = [];
    for (let i = 0; i < gal.length; i += 8) { const x = gal[i], y = gal[i + 1], z = gal[i + 2]; let best = 1e9;
      for (let k = 0; k <= NSP; k++) { if (cds[k] < 2) continue; const c = cps[k], dd = Math.sqrt((x - c.x) ** 2 + (y - c.y) ** 2 + (z - c.z) ** 2) / cds[k]; if (dd < best) best = dd; }
      if (best < .35) cand.push([best, i]); }
    cand.sort((a, b) => a[0] - b[0]); cand.slice(0, 1800).forEach(([, i]) => STK.push(i)); NST = STK.length;
    if (NST) fly = streaks(S, NST, { minPx: 1.6, near: [.4, 2] }); }

  // ---------------- speck payoff: our home marked by a soft warm glint and one slow ring as the web shrinks to a speck; dust
  // specks of the same apparent size drift past close to the lens ("a speck of dust")
  const ringT = ctx.ctex(256, (g, s) => { const gr = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.78, 'rgba(255,255,255,0)'); gr.addColorStop(.9, 'rgba(255,255,255,.85)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); });
  const glint = ctx.glow(S, ctx.ACC, 1, 0), spRing = new T.Sprite(new T.SpriteMaterial({ map: ringT, color: ctx.ACC, transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, depthTest: false })); S.add(spRing);
  glint.material.depthTest = false; glint.renderOrder = spRing.renderOrder = 5;
  const NMO = 60, mo = ctx.points(NMO, { size: 1, opacity: 1, color: '#ffffff' }), moA = mo.geometry.attributes.position.array, moC = mo.geometry.attributes.color.array, moB = [];
  { const r = rng(91); for (let i = 0; i < NMO; i++) moB.push([r() * 2 - .7, r() * 2 - 1, .02 + r() * .05, r(), r() * 6.283]); } mo.frustumCulled = false; mo.renderOrder = 6; S.add(mo);
  const loneR = loneS.map(s => s.material.rotation), vt = new T.Vector3(), vt2 = new T.Vector3();
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const st = camState(t), wZ = st.wZ, wS = st.wS, wSh = st.wSh, wR = p.recede == null ? 0 : sm(cue(p.recede), cue(p.recede) + 26, t);
    cam.position.copy(st.t).addScaledVector(st.dir, st.d); cam.lookAt(st.t);
    cam.near = Math.max(.002, st.d * .002); cam.far = Math.max(1000, st.d * 6 + 900); cam.fov = vf(st.fov); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    const pxW = 2 * Math.tan(cam.fov * Math.PI / 360) / ctx.H;
    shared.uScale.value = ctx.H / (2 * Math.tan(cam.fov * Math.PI / 360)); shared.uRec.value = wR;
    // layer visibility by scale: home galaxy close up, the web once we are out past the Local Group, glow layers dim for the speck
    const ld = Math.log(st.d), webV = LOOK === 'void' ? 1 : sm(Math.log(2.5), Math.log(30), ld);
    galL.material.uniforms.uOp.value = webV * (1 - .7 * wSh); galL.visible = webV > .001;
    shoreL.material.uniforms.uOp.value = webV * (1 + .5 * wSh); shoreL.visible = webV > .001;
    gloL.material.uniforms.uOp.value = .5 * webV * (1 - .7 * wS) * (1 + .6 * wSh); cluL.material.uniforms.uOp.value = .6 * webV * (1 - .5 * wS);
    gloL.visible = cluL.visible = webV > .001;
    const homeV = LOOK === 'void' ? 0 : 1 - sm(Math.log(8), Math.log(60), ld);
    homeL.material.uniforms.uOp.value = homeV; homeGL.material.uniforms.uOp.value = .4 * homeV; homeL.visible = homeGL.visible = homeV > .001;
    homeCore.material.opacity = .5 * homeV * (1 - sm(Math.log(1), Math.log(6), ld)); andCore.material.opacity = .35 * homeV * (1 - sm(Math.log(3), Math.log(12), ld));
    skyU.uK.value = 1 - .8 * wS;
    loneS.forEach((s, i) => { const d = s.position.distanceTo(cam.position); s.material.opacity = (LOOK === 'void' ? .85 : .5) * sm(140, 45, d) * sm(1.2, 4, d); s.material.rotation = loneR[i] + t * (i % 2 ? .012 : -.009); });
    // fly-through streaks: tail = where the galaxy was seen .18 s ago; drawn only when the motion on screen is long enough to read
    if (fly) { const v = cam.position.clone().sub(camPos(t - .18)), on = webV * (LOOK === 'web' ? 1 - wS : 0);
      fly.mesh.visible = on > .002 && v.length() > 1e-4;
      if (fly.mesh.visible) { for (let j = 0; j < NST; j++) { const i = STK[j]; vt.set(gal[i], gal[i + 1], gal[i + 2]); const dc = vt.distanceTo(cam.position);
          const lp = v.length() / Math.max(1e-6, dc * pxW), cl = Math.min(1, 150 / Math.max(lp, 1e-6));   // screen length capped near 150 px
          let k = on * sm(4, 22, lp) * Math.min(1, 40 / (lp * cl) + .3) * .55;
          if (k > .003) { vt2.copy(vt).project(cam); k *= sm(-.62, -.12, vt2.x) * sm(-.9, -.6, vt2.y); }
          vt2.copy(vt).addScaledVector(v, cl);
          if (k < .003) { fly.hide(j); continue; }
          fly.set(j, vt.x, vt.y, vt.z, vt2.x, vt2.y, vt2.z, Math.min(.5, 2.6 * dc * pxW), gal[i + 3] * k, gal[i + 4] * k, gal[i + 5] * k); }
        fly.commit(); } }
    // speck: the glint fades up (rise .6 s) once the web is small, breathes gently; one ring opens slowly around it
    { const g0 = tSp + 4.6, gv = LOOK === 'web' ? sm(g0, g0 + .6, t) : 0, rr = (t - g0 - .3) / 3.2, dh = cam.position.length();
      glint.visible = gv > 0; glint.position.set(0, 0, 0); glint.scale.setScalar(dh * pxW * 22 * (1 + .12 * Math.sin(t * 1.6))); glint.material.opacity = .75 * gv * (.85 + .15 * Math.sin(t * 1.6));
      spRing.visible = gv > 0 && rr > 0 && rr < 1; if (spRing.visible) { spRing.position.set(0, 0, 0); spRing.scale.setScalar(dh * pxW * (30 + 260 * Math.sqrt(rr))); spRing.material.opacity = .3 * sm(0, .08, rr) * (1 - sm(.3, 1, rr)); }
      const mv = LOOK === 'web' ? sm(tSp + 2.5, tSp + 6, t) : sm(ctx.t0 + 1, ctx.t0 + 5, t) * .6;
      mo.visible = mv > 0;
      if (mo.visible) { const fw = st.dir.clone().negate(), rt = new T.Vector3().crossVectors(fw, v3(0, 1, 0)).normalize(), up = new T.Vector3().crossVectors(rt, fw), zf = Math.max(cam.near * 3, st.d * .02);
        const th = Math.tan(cam.fov * Math.PI / 360), asp = ctx.W / ctx.H;
        for (let i = 0; i < NMO; i++) { const b = moB[i], z = zf * (1 + 2.5 * b[3]), xx = ((b[0] + t * .006 * (.5 + b[3]) + 1) % 2) - 1, yy = b[1] + .04 * Math.sin(t * .2 + b[4]);
          vt.copy(cam.position).addScaledVector(fw, z).addScaledVector(rt, xx * th * asp * z).addScaledVector(up, yy * th * z);
          moA[i * 3] = vt.x; moA[i * 3 + 1] = vt.y; moA[i * 3 + 2] = vt.z;
          const sx = .62 + xx * .5, al = mv * sm(.3, .45, sx) * sm(-1, -.7, yy) * (1 - sm(.85, 1, Math.abs(xx))) * (.4 + .6 * b[2] / .07) * .7;
          moC[i * 3] = al; moC[i * 3 + 1] = al * .9; moC[i * 3 + 2] = al * .78; }
        mo.material.size = zf * th * 2 / ctx.H * 5 * 1.6; mo.geometry.attributes.position.needsUpdate = true; mo.geometry.attributes.color.needsUpdate = true; } }
    // shoreline: once the camera has turned, a slow wave of light runs along the wall ("the tide"), then a softer one every 16 s
    if (LOOK === 'void' && p.shore != null) { const ts = t - tSh - 4, n = Math.floor(ts / 16), f = ts / 16 - n;
      swU.uSwD.value.copy(TG); swU.uSwP.value = -RSH * 1.1 + RSH * 2.4 * f; swU.uSwA.value = ts > 0 ? (n === 0 ? 2.2 : 1.1) * Math.sin(Math.PI * f) * wSh : 0; }
  } };
};
