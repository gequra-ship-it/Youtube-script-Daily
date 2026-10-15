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
//   side      subject offset (default .12)
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
  const U = { uK: { value: 1 / R0 }, uM: { value: 0 }, uFog: { value: .004 }, uBg: { value: BG.clone() }, uAcc: { value: new T.Color(ctx.ACC) },
    uXt: { value: 0 }, uXe: { value: 1e6 }, uEdge: { value: 0 }, uStr: { value: 0 }, uLight: { value: v3(-.5, .35, -.8).normalize() } };
  const surf = new T.Mesh(geo, new T.ShaderMaterial({ uniforms: U, side: T.DoubleSide,
    vertexShader: `uniform float uK; varying vec2 vP; varying vec3 vW, vN;
      void main(){ vec2 q = position.xz; float r = length(q); vec2 dir = r > 1e-5 ? q / r : vec2(1., 0.);
        vec3 w, n;
        if (uK < 1e-6) { w = vec3(q.x, 0., q.y); n = vec3(0., 1., 0.); }
        else { float th = min(r * uK, 3.14159265); w = vec3(dir.x * sin(th) / uK, (cos(th) - 1.) / uK, dir.y * sin(th) / uK); n = vec3(dir.x * sin(th), cos(th), dir.y * sin(th)); }
        vP = q; vW = (modelMatrix * vec4(w, 1.)).xyz; vN = n; gl_Position = projectionMatrix * viewMatrix * vec4(vW, 1.); }`,
    fragmentShader: `uniform float uK, uM, uFog, uXt, uXe, uEdge, uStr; uniform vec3 uBg, uAcc, uLight; varying vec2 vP; varying vec3 vW, vN;
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
        col += uAcc * g * (.32 + .25 * fr);
        // the phantom edge: a bright line across the sheet, plus a soft glow before it
        float de = vP.x - uXe; col += uEdge * (exp(-de * de / 1.2) * vec3(1., .86, .6) * 2.2 + exp(-abs(de) / 9.) * vec3(.5, .45, .35) * .25);
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

  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .1, 6000); ctx.side(cam, p.side == null ? .12 : p.side);
  const VF = ctx.VERT ? 1.3 : 1, tgt = v3(0, 0, 0), cp = v3(0, 0, 0);
  const PSI = [Math.cos(.62), Math.sin(.62)], cBal = p.balloon != null ? cue(p.balloon) : ctx.t0, LAP = 10, SPD_F = 3.2;
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const m = at(p.flat, 6), ph = at(p.phantom, 2.5), cF = p.flat != null ? cue(p.flat) : 1e9, cP = p.phantom != null ? cue(p.phantom) : 1e9;
    const k = m >= 1 ? 0 : (1 / R0) * Math.pow(1 - m, 3), R = k > 0 ? 1 / k : 1e9;
    U.uK.value = k; U.uM.value = m; U.uFog.value = .006 + .006 * m;
    // traveller: laps on the sphere (from the start beacon at the top pole), fades during the unrolling, then walks straight on
    const L = 2 * Math.PI * R0, tb = t - cBal;
    let x0, onS = 1;
    if (m <= 0) x0 = tb <= 0 ? 0 : ((tb / LAP) % 1) * L;
    else onS = 0;
    const tf = t - (cF + 6.2), xf = Math.max(0, tf) * SPD_F, tp = Math.max(0, t - cP);
    const vis = m <= 0 ? (tb > -.5 ? 1 : .6) : sm(.02, 0, m) + sm(0, 1.5, tf);
    const posAt = s => { if (onS) { const xs = ((s + Math.PI * R0) % L + L) % L - Math.PI * R0; return mapP(xs * PSI[0], xs * PSI[1], 1 / R0, .35); } return mapP(Math.max(0, s), 0, k, .35); };
    const xs = onS ? x0 : xf, H = posAt(xs);
    head.position.copy(H); halo.position.copy(H); head.material.opacity = vis; halo.material.opacity = .3 * vis; head.material.depthTest = halo.material.depthTest = !!onS;
    for (let i = 0; i < NT; i++) { const s = xs - i * (onS ? .32 : .09), q = (onS ? (tb - i * .32 / (L / LAP) > 0) : s > 0) ? posAt(s) : null;
      if (!q) { tA[i * 3 + 1] = -1e5; continue; } tA.set([q.x, q.y, q.z], i * 3); const v = vis * Math.pow(1 - i / NT, 1.6) * .9; tC.set([v, v * .82, v * .55], i * 3); }
    trail.geometry.attributes.position.needsUpdate = true; trail.geometry.attributes.color.needsUpdate = true;
    beacon.material.opacity = .9 * (1 - m); bGlow.material.opacity = .3 * (1 - m) * (1 + .5 * Math.sin(t * 2));
    // phantom edge: starts 26 ahead, recedes faster than the walk; grid ahead stretches
    const xt = xf, xe = xt + 26 + 9 * tp + .6 * tp * tp;
    U.uXt.value = ph > 0 ? xt : 1e6; U.uXe.value = xe; U.uEdge.value = ph; U.uStr.value = .22 * tp;
    curtain.position.set(xe, 0, 0); curM.opacity = .3 * ph;
    // camera: balloon = three-quarter view of the sphere from above; flat = low over the sheet, toward the horizon; phantom =
    // behind the traveller looking at the receding edge
    const az = .55 + u * .01, el = .42, Db = 80 * VF;
    const bal = v3(Math.sin(az) * Math.cos(el) * Db, -R0 + Math.sin(el) * Db, Math.cos(az) * Math.cos(el) * Db), balT = v3(0, -R0 - 3.5, 0);
    const fl = v3(xf - 18 * VF, 9 * VF, 26 * VF), flT = v3(xf + 30, 0, -12);
    const phP = v3(xt - 16 * VF, 5.5 * VF, 7 * VF), phT = v3(xt + 34, 1, -2);
    const mm = sm(0, 1, m);
    cp.copy(bal).lerp(fl, mm).lerp(phP, ph); tgt.copy(balT).lerp(flT, mm).lerp(phT, ph);
    cam.position.copy(cp); cam.lookAt(tgt);
    dust.update(t, [cp.x, cp.y, cp.z - 20]);
  } };
};
