// curvature — the shape of space, drawn as one glowing surface whose curvature changes in the vertex shader (true geometry, not
// a crossfade): a large smooth dark-navy sphere ("balloon") with a soft gold grid of latitudes/meridians and a cool backlit rim; a
// small abstract traveller (a gold light point with a fading trail, NOT an ant) walks a great circle and comes back to its start
// beacon: finite, but no edge. On `flat` the radius grows without bound, so the sphere unrolls into an infinite flat glowing grid
// sheet reaching to a fogged horizon. On `phantom` the traveller walks toward a bright edge line that keeps receding faster than
// it walks, while the grid ahead stretches (new space opening). Dust and fog for depth. Written for cosmic-prison-cine S35-S38
// (2026-10-15).
// params (cues, all optional):
//   balloon   S36: the traveller sets off around the sphere (absent: it walks from the start of the shot)
//   flat      S37: the sphere unrolls into the infinite flat sheet (radius -> infinity over ~6 s); camera moves down to the sheet
//   phantom   S38: the bright 'edge' line appears ahead; the traveller walks toward it; it recedes faster; the grid ahead stretches
//   open      (optional cue) S38 "new space opening ahead": a light wave runs ahead of the traveller (never reaching the edge),
//             expansion streaks rush toward the edge and the stretch accelerates (default: phantom + 7.0 s)
//   side      subject offset (default .12)
// Second staging pass (2026-10-16): the balloon inflates through the curved phase (radius x0.78 -> x1 by "flat") with galaxies
// fixed to the surface sliding apart; each time the traveller comes home the beacon flashes and a ring of light runs out over
// the surface; a light ray launches 3.4 s before the traveller's 2nd return ("travel straight...") along another great circle
// and arrives home together with it (bigger flash: "...back where you started"); the flat sheet carries slow ripples from the
// traveller; 260 more galaxies bloom out to the horizon at flat + 8.8 s ("infinite volume, endless galaxies"); phantom = edge
// flare on the cue, step pulses, and the "open" beat above. The edge glow is dimmed over the left text column.
(window.MIYA = window.MIYA || { scenes: {} }).scenes.curvature = function (ctx, p) {
  const { T, sm, rng, cue, points, glow } = ctx, K = window.MIYA.kit;
  const v3 = (x, y, z) => new T.Vector3(x, y, z);
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), ctx.t);
  const BG = new T.Color('#05061a');
  const S = new T.Scene(); S.background = BG;
  ctx.stars(S, 2500, 1800, { seed: 9, size: 1.3, opacity: .6 });

  // ---------------- the surface: polar mesh in plane coordinates, curved in the vertex shader ----------------
  const R0 = 20, rings = [];
  for (let r = 0; r <= 72; r += .36) rings.push(r);
  let rr = 72; while (rr < 3200) { rr *= 1.05; rings.push(rr); }
  const NS = 192, NR = rings.length, pos = new Float32Array(NR * (NS + 1) * 3), idx = [];
  for (let i = 0; i < NR; i++) for (let j = 0; j <= NS; j++) { const a = j / NS * Math.PI * 2, k = (i * (NS + 1) + j) * 3; pos[k] = Math.cos(a) * rings[i]; pos[k + 1] = 0; pos[k + 2] = Math.sin(a) * rings[i]; }
  for (let i = 0; i < NR - 1; i++) for (let j = 0; j < NS; j++) { const a = i * (NS + 1) + j, b = a + NS + 1; idx.push(a, a + 1, b, b, a + 1, b + 1); }
  const geo = new T.BufferGeometry(); geo.setAttribute('position', new T.BufferAttribute(pos, 3)); geo.setIndex(idx);
  const U = { uT: { value: 0 }, uRip: { value: 0 }, uSrc: { value: new T.Vector2() }, uPr: { value: 0 }, uPa: { value: 0 }, uWx: { value: 0 }, uWa: { value: 0 }, uW: { value: ctx.VERT ? 0 : ctx.W },
    uK: { value: 1 / R0 }, uM: { value: 0 }, uFog: { value: .004 }, uBg: { value: BG.clone() }, uAcc: { value: new T.Color(ctx.ACC) },
    uXt: { value: 0 }, uXe: { value: 1e6 }, uEdge: { value: 0 }, uStr: { value: 0 }, uLight: { value: v3(-.5, .35, -.8).normalize() } };
  const surf = new T.Mesh(geo, new T.ShaderMaterial({ uniforms: U, side: T.DoubleSide,
    vertexShader: `uniform float uK, uT, uRip; uniform vec2 uSrc; varying vec2 vP; varying vec3 vW, vN; varying float vH;
      void main(){ vec2 q = position.xz; float r = length(q); vec2 dir = r > 1e-5 ? q / r : vec2(1., 0.);
        vec3 w, n;
        vH = 0.;
        if (uK < 1e-6) { float dd = length(q - uSrc); vH = uRip * sin(dd * .35 - uT * 2.2) * exp(-dd / 70.); w = vec3(q.x, vH * .45, q.y); n = vec3(0., 1., 0.); }
        else { float th = min(r * uK, 3.14159265); w = vec3(dir.x * sin(th) / uK, (cos(th) - 1.) / uK, dir.y * sin(th) / uK); n = vec3(dir.x * sin(th), cos(th), dir.y * sin(th)); }
        vP = q; vW = (modelMatrix * vec4(w, 1.)).xyz; vN = n; gl_Position = projectionMatrix * viewMatrix * vec4(vW, 1.); }`,
    fragmentShader: `uniform float uK, uM, uFog, uXt, uXe, uEdge, uStr, uPr, uPa, uWx, uWa, uW; uniform vec3 uBg, uAcc, uLight; varying vec2 vP; varying vec3 vW, vN; varying float vH;
      float gridLine(float c, float w){ float fw = max(fwidth(c), 1e-4); float d = abs(fract(c - .5) - .5) / fw; return (1. - smoothstep(w * .5, w * .5 + 1., d)) * (1. - smoothstep(.12, .45, fw)); }
      void main(){
        vec3 V = normalize(cameraPosition - vW), N = normalize(vN); if (dot(N, V) < 0.) N = -N;
        float r = length(vP), R = 1. / max(uK, 1e-6);
        // polar grid (latitudes / meridians) on the sphere, square grid on the sheet
        float lat = gridLine(r / (3.14159265 * R / 12.), .9);
        float ph = atan(vP.y, vP.x) / 6.2831853 * 24.; float fw = fwidth(ph); if (fw > 12.) fw = 0.;
        float mer = (1. - smoothstep(.45, 1.45, abs(fract(ph - .5) - .5) / max(fw, 1e-4))) * (1. - smoothstep(.12, .45, fw)) * smoothstep(.0, 4., r);
        float pol = max(lat, mer);
        // square grid; ahead of the traveller it stretches in the phantom phase (new space opening up)
        float gx = vP.x > uXt ? uXt + (vP.x - uXt) / (1. + uStr) : vP.x;
        float sq = max(gridLine(gx / 4., 1.), gridLine(vP.y / 4., 1.));
        float g = mix(pol, sq, smoothstep(.15, .85, uM));
        // material: dark navy, backlit rim (fresnel weighted toward the light behind), soft key
        float fr = pow(1. - max(0., dot(N, V)), 3.), back = .45 + .55 * max(0., dot(-V, uLight));
        vec3 base = vec3(.012, .016, .05) + vec3(.03, .04, .1) * max(0., dot(N, normalize(vec3(.3, 1., .4))));
        vec3 col = base + vec3(.35, .45, 1.) * fr * back * .55 * (1. - .7 * uM);
        col += uAcc * g * (.32 + .25 * fr) * (1. + .55 * max(vH, 0.));
        // homecoming ring running out over the surface from the beacon, and the light wave on the sheet in the phantom phase
        float dr = r - uPr; col += vec3(1., .85, .6) * uPa * exp(-dr * dr / .8) * (1.2 + g);
        float dw = vP.x - uWx; col += vec3(1., .88, .65) * uWa * (uW > 0. ? mix(.35, 1., smoothstep(.3 * uW, .55 * uW, gl_FragCoord.x)) : 1.) * exp(-dw * dw / 2.) * (.6 + 1.5 * g);
        // the phantom edge: a bright line across the sheet, plus a soft glow before it
        float lft = uW > 0. ? mix(.3, 1., smoothstep(.3 * uW, .55 * uW, gl_FragCoord.x)) : 1.;
        float de = vP.x - uXe; col += uEdge * lft * (exp(-de * de / 1.2) * vec3(1., .86, .6) * 2.2 + exp(-abs(de) / 9.) * vec3(.5, .45, .35) * .25);
        float dist = length(cameraPosition - vW), f = 1. - exp(-pow(dist * uFog, 1.6));
        col = mix(col, vec3(.03, .03, .075) + uEdge * vec3(.04, .03, .015), f);
        gl_FragColor = vec4(col, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  surf.frustumCulled = false; S.add(surf);
  // map plane coords -> world (same maths as the shader) for the traveller
  const mapP = (x, z, k, lift) => { const r = Math.hypot(x, z), dx = r > 1e-5 ? x / r : 1, dz = r > 1e-5 ? z / r : 0;
    if (k < 1e-6) return v3(x, lift, z); const th = Math.min(r * k, Math.PI), n = v3(dx * Math.sin(th), Math.cos(th), dz * Math.sin(th));
    return v3(dx * Math.sin(th) / k, (Math.cos(th) - 1) / k, dz * Math.sin(th) / k).addScaledVector(n, lift); };

  // ---------------- traveller: gold light + trail + start beacon ----------------
  const NT = 240, trail = points(NT, { size: .32, opacity: 1, color: '#ffffff' }), tA = trail.geometry.attributes.position.array, tC = trail.geometry.attributes.color.array;
  trail.material.depthTest = true; trail.frustumCulled = false; S.add(trail);
  const head = glow(S, '#fff0d0', 1.5, 1), halo = glow(S, '#ffc65a', 4, .3);
  head.material.depthTest = halo.material.depthTest = true;
  const beacon = new T.Mesh(new T.TorusGeometry(1.1, .09, 10, 64).rotateX(Math.PI / 2), new T.MeshBasicMaterial({ color: new T.Color(ctx.ACC).multiplyScalar(1.4), transparent: true, opacity: .9, blending: T.AdditiveBlending, depthWrite: false }));
  beacon.position.set(0, .05, 0); S.add(beacon); const bGlow = glow(S, '#ffc65a', 4, .3); bGlow.position.set(0, .3, 0);
  // the phantom edge: a vertical light curtain at the edge line
  const curT = ctx.ctex(128, (g, s) => { const gr = g.createLinearGradient(0, s, 0, 0); gr.addColorStop(0, 'rgba(255,230,180,1)'); gr.addColorStop(.35, 'rgba(255,200,120,.35)'); gr.addColorStop(1, 'rgba(255,180,90,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); });
  const curM = new T.MeshBasicMaterial({ map: curT, transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide, fog: false });
  const curtain = new T.Mesh(new T.PlaneGeometry(4000, 10).rotateY(Math.PI / 2).translate(0, 5, 0), curM); S.add(curtain);
  const dust = K.snow(S, { n: 900, box: [90, 40, 90], size: .18, opacity: .45, color: '#ffe0b0', fall: .04, seed: 21 });

  // galaxies: small tilted spiral sprites; the first 70 sit on the sphere at fixed angles (slide apart as it inflates), 260 more
  // are scattered over the flat sheet and bloom on "endless galaxies"
  const galT = ctx.ctex(128, (g, s) => { const im = g.createImageData(s, s); for (let y = 0; y < s; y++) for (let x = 0; x < s; x++) { const u = (x + .5) / s * 2 - 1, v = (y + .5) / s * 2 - 1, r = Math.hypot(u, v), th = Math.atan2(v, u);
      const arm = Math.pow(.5 + .5 * Math.cos(2 * (th - Math.log(Math.max(.05, r)) * 2.2)), 2), L = Math.max(0, (Math.exp(-r * 4) * 1.4 + arm * Math.exp(-r * 3.2) * .9) * (1 - r)), k = (y * s + x) * 4;
      im.data[k] = 255 * Math.min(1, L * 1.05); im.data[k + 1] = 255 * Math.min(1, L * .92); im.data[k + 2] = 255 * Math.min(1, L * .8); im.data[k + 3] = 255 * Math.min(1, L); } g.putImageData(im, 0, 0); });
  const GN1 = 70, GN2 = 260, gals = [];
  { const r = rng(41), GC = ['#fff0dc', '#cfe0ff', '#ffd9b0', '#e8d8ff'];
    for (let i = 0; i < GN1 + GN2; i++) { const m = new T.Sprite(new T.SpriteMaterial({ map: galT, color: GC[i % 4], transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, rotation: r() * 6.283 }));
      const sz = (i < GN1 ? 2.6 : 3.4) * (.6 + .8 * r()); m.scale.set(sz, sz * (.45 + .5 * r()), 1); S.add(m);
      if (i < GN1) gals.push({ m, th: .22 + 2.6 * Math.sqrt(r()), ph: r() * 6.283, sph: 1 });
      else { const rr = 30 + 1400 * Math.pow(r(), 1.4), a = r() * 6.283; gals.push({ m, x: Math.cos(a) * rr, z: Math.sin(a) * rr, rr, sph: 0 }); } } }
  // camera-facing streaks (copied from lightspeed.js) for the light ray and the expansion rush
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
  const ism = (a, d, t) => { const x = (t - a) / d; if (x <= 0) return 0; if (x >= 1) return d * (x - .5); return d * (x * x * x - x * x * x * x / 2); };
  const env = (a, rise, fall) => a <= 0 ? 0 : sm(0, rise, a) * Math.exp(-Math.max(0, a - rise) / fall);
  const NRY = 48, ray = streaks(S, NRY, { minPx: 2 }), rayHead = glow(S, '#fff4e0', 2.4, 0); rayHead.material.depthTest = true;
  const NX = 180, rush = streaks(S, NX, { minPx: 1.5 }), xB = [];
  { const r = rng(43); for (let i = 0; i < NX; i++) xB.push([r(), (r() * 2 - 1) * 26, .2 + 2.2 * r(), .6 + .8 * r(), r()]); }
  const PSI2 = [Math.cos(-.3), Math.sin(-.3)];
  const ripY = (x, z, t, a) => { if (a <= 0) return 0; const dd = Math.hypot(x - U.uSrc.value.x, z - U.uSrc.value.y); return a * Math.sin(dd * .35 - t * 2.2) * Math.exp(-dd / 70) * .45; };

  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .1, 6000); ctx.side(cam, p.side == null ? .12 : p.side);
  const VF = ctx.VERT ? 1.3 : 1, tgt = v3(0, 0, 0), cp = v3(0, 0, 0);
  const PSI = [Math.cos(.62), Math.sin(.62)], cBal = p.balloon != null ? cue(p.balloon) : ctx.t0, LAP = 10, SPD_F = 3.2;
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const m = at(p.flat, 6), ph = at(p.phantom, 2.5), cF = p.flat != null ? cue(p.flat) : 1e9, cP = p.phantom != null ? cue(p.phantom) : 1e9;
    const tEnd = cF < 1e8 ? cF : ctx.t1, Rb = R0 * (.78 + .22 * sm(ctx.t0, tEnd, t));
    const k = m >= 1 ? 0 : (1 / Rb) * Math.pow(1 - m, 3), R = k > 0 ? 1 / k : 1e9;
    U.uK.value = k; U.uM.value = m; U.uFog.value = .006 + .006 * m;
    // traveller: laps on the sphere (from the start beacon at the top pole), fades during the unrolling, then walks straight on
    const L = 2 * Math.PI * Rb, tb = t - cBal;
    let x0, onS = 1;
    if (m <= 0) x0 = tb <= 0 ? 0 : ((tb / LAP) % 1) * L;
    else onS = 0;
    const tf = t - (cF + 6.2), xf = Math.max(0, tf) * SPD_F, tp = Math.max(0, t - cP);
    const rip = sm(cF + 6, cF + 9, t) * (1 - .5 * ph); U.uT.value = t; U.uRip.value = rip; U.uSrc.value.set(xf, 0);
    const vis = m <= 0 ? (tb > -.5 ? 1 : .6) : sm(.02, 0, m) + sm(0, 1.5, tf);
    const posAt = s => { if (onS) { const xs = ((s + Math.PI * Rb) % L + L) % L - Math.PI * Rb; return mapP(xs * PSI[0], xs * PSI[1], 1 / Rb, .35); } const q = mapP(Math.max(0, s), 0, k, .35); q.y += ripY(q.x, q.z, t, k > 0 ? 0 : rip); return q; };
    const xs = onS ? x0 : xf, H = posAt(xs);
    const step = onS ? 0 : Math.pow(.5 + .5 * Math.sin(t * 6.2832 * 1.4), 8) * sm(cF + 6.5, cF + 8, t);
    head.position.copy(H); halo.position.copy(H); head.material.opacity = vis; halo.material.opacity = .3 * vis * (1 + .9 * step); halo.scale.setScalar(4 * (1 + .25 * step)); head.material.depthTest = halo.material.depthTest = !!onS;
    for (let i = 0; i < NT; i++) { const s = xs - i * (onS ? .32 : .09), q = (onS ? (tb - i * .32 / (L / LAP) > 0) : s > 0) ? posAt(s) : null;
      if (!q) { tA[i * 3 + 1] = -1e5; continue; } tA.set([q.x, q.y, q.z], i * 3); const v = vis * Math.pow(1 - i / NT, 1.6) * .9; tC.set([v, v * .82, v * .55], i * 3); }
    trail.geometry.attributes.position.needsUpdate = true; trail.geometry.attributes.color.needsUpdate = true;
    // homecoming: each return of the traveller (and the light ray on the 2nd lap) flashes the beacon and sends a ring of light out
    const nL = Math.floor(tb / LAP), age = tb - nL * LAP, pa = nL >= 1 ? (nL === 2 ? 1.6 : 1) * sm(0, .15, age) * Math.exp(-age / 1.6) * (1 - sm(LAP - 1.2, LAP - .2, age)) * (1 - m) : 0;
    U.uPa.value = pa * .8; U.uPr.value = age * 9;
    beacon.material.opacity = Math.min(1, .9 * (1 - m) * (1 + .6 * pa)); bGlow.material.opacity = .3 * (1 - m) * (1 + .5 * Math.sin(t * 2)) + .35 * pa; bGlow.scale.setScalar(4 * (1 + 1.2 * pa));
    // the light ray: a great circle in 3.4 s, launched so that it comes home together with the traveller's 2nd return
    const tR = cBal + 2 * LAP - 3.4, aR = t - tR, rayOn = aR > 0 && aR < 4.6 && m <= 0;
    ray.mesh.visible = rayOn; rayHead.visible = rayOn;
    if (rayOn) { const sh = L * Math.min(aR, 3.4) / 3.4, fo = 1 - sm(3.4, 4.5, aR), sp = .24 * L / NRY;
      const rp = s2 => { const xs = ((s2 + Math.PI * Rb) % L + L) % L - Math.PI * Rb; return mapP(xs * PSI2[0], xs * PSI2[1], 1 / Rb, .5); };
      for (let i = 0; i < NRY; i++) { const s1 = sh - i * sp, s2 = s1 - sp * 1.05; if (s2 < 0) { ray.hide(i); continue; } const a1 = rp(s1), a2 = rp(s2), v = Math.pow(1 - i / NRY, 1.5) * fo * sm(0, .2, aR) * 1.3;
        ray.set(i, a1.x, a1.y, a1.z, a2.x, a2.y, a2.z, .45, v * 1.6, v * 1.45, v * 1.1); }
      ray.commit(); const hp = rp(sh); rayHead.position.copy(hp); rayHead.material.opacity = fo * sm(0, .2, aR); }
    // galaxies: on the sphere at fixed angles (slide apart as it inflates); on the sheet they bloom outward on "endless galaxies"
    const tG = cF + 8.8;
    gals.forEach(g => { if (g.sph) { const r = g.th * Rb, q = mapP(r * Math.cos(g.ph), r * Math.sin(g.ph), k, .3); if (k <= 0) q.y += ripY(q.x, q.z, t, rip); g.m.position.copy(q); g.m.material.opacity = .8 * (1 - .4 * ph); return; }
      if (k > 0) { g.m.visible = false; return; } const a0 = tG + g.rr / 450, op = .6 * sm(a0, a0 + 1.4, t); g.m.visible = op > .003;
      if (g.m.visible) { g.m.position.set(g.x, .3 + ripY(g.x, g.z, t, rip), g.z); g.m.material.opacity = op * (1 - .4 * ph); } });
    // phantom edge: starts 26 ahead, recedes faster than the walk; grid ahead stretches
    const tO = p.open != null ? cue(p.open) : cP + 7, oo = sm(tO, tO + 2, t), efl = env(t - cP, .3, 2);
    const xt = xf, xe = xt + 26 + 9 * tp + .6 * tp * tp + 6 * ism(tO, 2, t);
    U.uXt.value = ph > 0 ? xt : 1e6; U.uXe.value = xe; U.uEdge.value = ph * (1 + 1.2 * efl); U.uStr.value = .22 * tp + .3 * ism(tO, 2, t);
    curtain.position.set(xe, 0, 0); curM.opacity = .2 * ph * (1 + efl);
    const aO = t - tO; U.uWx.value = xt + 3 + 20 * (1 - Math.exp(-Math.max(0, aO) / 1.3)); U.uWa.value = env(aO, .3, 1.8) * .9 * ph;
    // expansion rush: streaks race from the traveller toward the receding edge, faster after "open" (length grows with speed)
    rush.mesh.visible = ph > 0;
    if (ph > 0) { const F = .15 * tp + .6 * ism(tO, 2, t), vS = .15 + .6 * oo, span = xe - xt - 2;
      for (let i = 0; i < NX; i++) { const b = xB[i], s0 = F * b[3] + b[0], s1 = s0 - Math.floor(s0), x = xt + 2 + s1 * span, len = Math.min(16, vS * span * .22 * b[3]) + .3;
        const v = Math.sin(Math.PI * s1) * ph * (.22 + .5 * oo) * b[3] * .6, y = b[2] + ripY(x, b[1], t, rip);
        rush.set(i, x, y, b[1], x - len, y, b[1], .12, v, v * .86, v * .62); }
      rush.commit(); }
    // camera: balloon = three-quarter view of the sphere from above; flat = low over the sheet, toward the horizon; phantom =
    // behind the traveller looking at the receding edge
    const az = .55 + u * .01, el = .42, Db = 80 * VF;
    const bal = v3(Math.sin(az) * Math.cos(el) * Db, -Rb + Math.sin(el) * Db, Math.cos(az) * Math.cos(el) * Db), balT = v3(0, -Rb - 3.5, 0);
    const fl = v3(xf - 18 * VF, 9 * VF, 26 * VF), flT = v3(xf + 30, 0, -12);
    const phP = v3(xt - 16 * VF, 5.5 * VF, 7 * VF), phT = v3(xt + 34, 1, -2);
    const mm = sm(0, 1, m);
    cp.copy(bal).lerp(fl, mm).lerp(phP, ph); tgt.copy(balT).lerp(flT, mm).lerp(phT, ph);
    cam.position.copy(cp); cam.lookAt(tgt);
    dust.update(t, [cp.x, cp.y, cp.z - 20]);
  } };
};
