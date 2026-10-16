// voyager — a realistic Voyager-style probe drifting through dark space (S02-S03), backlit by a small, distant, very bright Sun
// (warm halo, glowing rims on the sun-facing edges, faint heliosphere glow in the sky). Parts: white high-gain dish with thickness,
// back ribs and hoop, Cassegrain subreflector on four struts + feed horn; ten-sided bus with louvred bays and a gold foil collar;
// propellant tank and thrusters; RTG boom with three finned cylinders (faint warm heat glow); long magnetometer boom with a sensor
// at its tip; science boom with the scan platform (cameras, instrument boxes). No logos, no text.
// Then the scale changes symbolically (one exponential camera move per cue, seek-safe):
//   far      — the camera pulls straight back: the probe shrinks to a tiny glint beside the Sun, which becomes a bright star
//   proxima  — the camera swings sideways: the enormous empty gulf toward one distant reddish star (Proxima); a gold dotted path
//              leaves the probe toward it and barely starts (ghost dots mark the rest of the way)
//   galaxy   — pull far back until a Milky Way disc fills the frame; the whole path vanishes inside one gold point
// params (cues, all optional): { launch (a short sun glint across the dish), far, proxima, galaxy, side: .14 }
// Defaults: without cues the probe stays in its slow close-up orbit (a complete shot on its own).
// speed pass (2026-10-16): during the `far` pull-back, dust/star streaks spread log-evenly along the way (8 to 2500 units out, so
// the stream looks the same at every scale) rush in from the frame edges and shrink toward the probe; each streak is the motion of
// its point relative to the camera over the last 0.07 s (longer when the camera moves faster), eased in and out with the move.
// In the close-up a sparse layer of soft motes drifts slowly across the view (near parallax for depth).
(window.MIYA = window.MIYA || { scenes: {} }).scenes.voyager = function (ctx, p) {
  const { T, sm, rng, cue, dotTex } = ctx, K = window.MIYA.kit, E = ctx.env();
  const S = new T.Scene(); S.background = new T.Color('#02030a');
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), ctx.t);
  const v3 = (x, y, z) => new T.Vector3(x, y, z);
  const vf = f => { if (!ctx.VERT) return f; const h = 2 * Math.atan(Math.tan(f * Math.PI / 360) * 16 / 9 * .62); return 2 * Math.atan(Math.tan(h / 2) * ctx.H / ctx.W) * 180 / Math.PI; };

  // ---------------- motion streaks (2026-10-16 speed pass): n camera-facing quads, billboarded in the vertex shader so the camera
  // director's later move keeps them facing the lens; a head bright, tail fading; width never below minPx pixels (thinner streaks dim
  // instead, so far ones never shimmer); fades out close to the camera. set(i, head, tail, width, rgb) each frame from t only.
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
  // ---------------- frame of reference: camera start, sun direction, Proxima direction, galaxy plane ----------------
  const C0 = v3(6.4, -1.6, 8.6), V = C0.clone().negate().normalize();           // V: initial view direction (toward the probe)
  const RT = new T.Vector3().crossVectors(V, v3(0, 1, 0)).normalize(), UP = new T.Vector3().crossVectors(RT, V).normalize();
  const SD = V.clone().addScaledVector(UP, .6).addScaledVector(RT, -.95).normalize();   // ~48 deg off the view: grazing backlight   // sun: up-left behind the probe
  const SUN = SD.clone().multiplyScalar(1600);
  const PD = RT.clone().multiplyScalar(.92).addScaledVector(V, .34).addScaledVector(UP, -.08).normalize(), GAP = 40000;
  const PROX = PD.clone().multiplyScalar(GAP);
  const NG = UP.clone().addScaledVector(V, .12).normalize();                      // galactic plane normal
  const GA = PD.clone().addScaledVector(NG, -PD.dot(NG)).normalize(), GB = new T.Vector3().crossVectors(NG, GA);
  const RG = GAP * 50000 / 4.2, GC = GA.clone().multiplyScalar(-.53 * RG).addScaledVector(GB, .1 * RG);   // Sun 26,000 ly out

  // ---------------- sky: one shader sphere at infinity (navy gradient, faint Milky Way band, heliosphere glow) ----------------
  const skyU = { uS: { value: SD }, uN: { value: NG }, uK: { value: 1 }, uH: { value: 1 } };
  const sky = new T.Mesh(new T.SphereGeometry(1, 48, 24), new T.ShaderMaterial({ uniforms: skyU, side: T.BackSide, depthWrite: false, depthTest: false,
    vertexShader: `varying vec3 vD; void main(){ vD = position; vec4 q = projectionMatrix * vec4(mat3(viewMatrix) * position, 1.0); gl_Position = vec4(q.xy, q.w * .99999, q.w); }`,
    fragmentShader: `varying vec3 vD; uniform vec3 uS, uN; uniform float uK, uH;
      float h3(vec3 p){ p = fract(p * .3183099 + .1); p *= 17.; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
      float n3(vec3 x){ vec3 i = floor(x), f = fract(x); f = f * f * (3. - 2. * f);
        return mix(mix(mix(h3(i), h3(i + vec3(1,0,0)), f.x), mix(h3(i + vec3(0,1,0)), h3(i + vec3(1,1,0)), f.x), f.y),
                   mix(mix(h3(i + vec3(0,0,1)), h3(i + vec3(1,0,1)), f.x), mix(h3(i + vec3(0,1,1)), h3(i + vec3(1,1,1)), f.x), f.y), f.z); }
      void main(){ vec3 d = normalize(vD);
        vec3 c = mix(vec3(.003,.004,.012), vec3(.008,.008,.024), .5 + .5 * d.y);
        float b = dot(d, uN), band = exp(-b * b / .03) * (.45 + .55 * n3(d * 3.1)) * (.6 + .4 * n3(d * 7.3 + 4.));
        c += vec3(.04, .034, .062) * band * uK;
        float th = acos(clamp(dot(d, uS), -1., 1.));
        c += vec3(1., .72, .38) * (.05 * exp(-th * th / .05) + .016 * exp(-th * th / .6)) * uH;
        float shell = smoothstep(.55, 1.05, th) * smoothstep(1.9, 1.15, th) * (.5 + .5 * n3(d * 2.2 + 9.));
        c += vec3(.28, .22, .55) * .016 * shell * uH;
        gl_FragColor = vec4(c, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  sky.frustumCulled = false; sky.renderOrder = -10; S.add(sky);
  // stars on a unit sphere that rides with the camera (no parallax, like real far stars); soft points >= 2 px (no crawl)
  const SKYG = new T.Group(); S.add(SKYG);
  function starLayer(n, size, seed, band) { const g = new T.BufferGeometry(), a = new Float32Array(n * 3), c = new Float32Array(n * 3), r = rng(seed);
    for (let i = 0; i < n; i++) { let d;
      if (band) { const ang = r() * 6.283, lat = (r() + r() + r() - 1.5) * .14; d = GA.clone().multiplyScalar(Math.cos(ang)).addScaledVector(GB, Math.sin(ang)).multiplyScalar(Math.cos(lat)).addScaledVector(NG, Math.sin(lat)); }
      else { const u = r() * 2 - 1, th = r() * 6.283, q = Math.sqrt(1 - u * u); d = v3(q * Math.cos(th), u, q * Math.sin(th)); }
      a.set([d.x, d.y, d.z], i * 3); const tp = r(), br = .35 + .9 * Math.pow(r(), 2.2), col = tp < .25 ? [.75, .82, 1] : tp < .8 ? [1, .96, .9] : [1, .82, .6];
      c.set([col[0] * br, col[1] * br, col[2] * br], i * 3); }
    g.setAttribute('position', new T.BufferAttribute(a, 3)); g.setAttribute('color', new T.BufferAttribute(c, 3));
    const P = new T.Points(g, new T.PointsMaterial({ size, map: dotTex(), vertexColors: true, transparent: true, blending: T.AdditiveBlending, depthWrite: false, depthTest: false, sizeAttenuation: false }));
    P.frustumCulled = false; P.renderOrder = -9; SKYG.add(P); return P; }
  const stars = [starLayer(2600, 2.2, 3, false), starLayer(2600, 2.0, 4, true), starLayer(260, 3.6, 5, false)];

  // ---------------- the probe ----------------
  const PROBE = new T.Group(); S.add(PROBE);
  const RIMU = { value: new T.Vector3() };
  function rim(m, k, col) { m.onBeforeCompile = sh => { sh.uniforms.uL = RIMU; sh.uniforms.uRim = { value: new T.Color(col || '#ffd08a').multiplyScalar(k) };
    sh.fragmentShader = 'uniform vec3 uL; uniform vec3 uRim;\n' + sh.fragmentShader.replace('#include <emissivemap_fragment>',
      '#include <emissivemap_fragment>\n{ float fr = 1.0 - abs(dot(normal, normalize(vViewPosition))); totalEmissiveRadiance += uRim * pow(fr, 1.3) * smoothstep(-0.35, 0.6, dot(normal, uL)); }'); };
    m.customProgramCacheKey = () => 'vgrim'; return m; }
  const dishM = rim(new T.MeshStandardMaterial({ color: '#d6d8df', roughness: .58, metalness: .08, envMap: E, envMapIntensity: .18, side: T.DoubleSide }), 3.2);
  const metM = rim(new T.MeshStandardMaterial({ color: '#a9afbd', roughness: .34, metalness: .85, envMap: E, envMapIntensity: .35 }), 2.6);
  const darkM = rim(new T.MeshStandardMaterial({ color: '#4a4e5c', roughness: .5, metalness: .6, envMap: E, envMapIntensity: .3 }), 1.0);
  const foilN = K.normalMap(K.noise(256, { seed: 21, octaves: 3 }), 6); foilN.repeat.set(3, 1);
  const foilM = rim(new T.MeshStandardMaterial({ color: '#c99a48', roughness: .28, metalness: 1, envMap: E, envMapIntensity: .55, normalMap: foilN }), 1.2);
  const louT = ctx.ctex(256, (g, s) => { g.fillStyle = '#4a4e5c'; g.fillRect(0, 0, s, s); g.fillStyle = '#2a2d36'; g.fillRect(14, 22, s - 28, s - 44);
    for (let k = 0; k < 8; k++) { const y = 30 + k * 25; g.fillStyle = '#9aa0b0'; g.fillRect(20, y, s - 40, 12); g.fillStyle = '#5c6070'; g.fillRect(20, y + 12, s - 40, 4); }
    g.fillStyle = '#6a6e7c'; g.fillRect(0, 0, s, 6); g.fillRect(0, s - 6, s, 6); });
  louT.anisotropy = 8; louT.repeat.set(10, 1); louT.wrapS = T.RepeatWrapping;
  const busM = rim(new T.MeshStandardMaterial({ map: louT, roughness: .42, metalness: .7, envMap: E, envMapIntensity: .35, flatShading: true }), 1.1);
  const add = (g, m, par) => { const o = new T.Mesh(g, m); (par || PROBE).add(o); return o; };
  function rod(a, b, r, m, par) { const d = b.clone().sub(a), o = add(new T.CylinderGeometry(r, r, d.length(), 8), m, par);
    o.position.copy(a).addScaledVector(d, .5); o.quaternion.setFromUnitVectors(v3(0, 1, 0), d.normalize()); return o; }
  // high-gain dish (opens toward +Y; local frame), focal length FL, real shell thickness, rolled rim
  const FL = 1.55, DR = 1.83, yP = r => r * r / (4 * FL);
  { const pr = []; for (let i = 0; i <= 20; i++) { const r = DR * i / 20; pr.push(new T.Vector2(r, yP(r) - .08 - .02 * (1 - i / 20))); }
    pr.push(new T.Vector2(DR + .04, yP(DR) - .04), new T.Vector2(DR + .04, yP(DR) + .02));
    for (let i = 20; i >= 0; i--) { const r = DR * i / 20; pr.push(new T.Vector2(Math.max(r, .0001), yP(r))); }
    add(new T.LatheGeometry(pr, 96), dishM); }
  for (let k = 0; k < 16; k++) { const a = k / 16 * 6.283, pts = [];   // back ribs
    for (let j = 0; j <= 10; j++) { const r = .3 + 1.45 * j / 10; pts.push(v3(r * Math.cos(a), yP(r) - .12, r * Math.sin(a))); }
    add(new T.TubeGeometry(new T.CatmullRomCurve3(pts), 10, .028, 6, false), metM); }
  add(new T.TorusGeometry(1.15, .03, 8, 64).rotateX(Math.PI / 2).translate(0, yP(1.15) - .12, 0), metM);
  add(new T.TorusGeometry(.42, .04, 8, 40).rotateX(Math.PI / 2).translate(0, yP(.42) - .12, 0), metM);
  for (let k = 0; k < 4; k++) { const a = k / 4 * 6.283 + .4; rod(v3(.95 * Math.cos(a), yP(.95), .95 * Math.sin(a)), v3(.13 * Math.cos(a), 1.02, .13 * Math.sin(a)), .022, metM); }
  { const sp = [[0, 1.08], [.14, 1.07], [.24, 1.03], [.25, 1.0], [.12, .98], [0, .97]].map(([r, h]) => new T.Vector2(r, h)); add(new T.LatheGeometry(sp, 32), metM); }
  add(new T.CylinderGeometry(.07, .14, .4, 20).translate(0, .2, 0), darkM);
  // foil collar + ten-sided bus with louvred bays, tank and thrusters below
  add(new T.CylinderGeometry(.38, .42, .3, 24).translate(0, -.22, 0), foilM);
  add(new T.CylinderGeometry(.92, .92, .47, 10).translate(0, -.6, 0), busM);
  add(new T.CylinderGeometry(.95, .95, .04, 10).translate(0, -.36, 0), darkM);
  add(new T.CylinderGeometry(.95, .95, .04, 10).translate(0, -.84, 0), darkM);
  add(new T.SphereGeometry(.4, 24, 12, 0, 6.283, Math.PI / 2, Math.PI / 2).translate(0, -.84, 0), foilM);
  for (let k = 0; k < 4; k++) { const a = k / 4 * 6.283 + .8; add(new T.CylinderGeometry(.03, .07, .16, 10).translate(.62 * Math.cos(a), -.94, .62 * Math.sin(a)), darkM); }
  // RTG boom (+X): a two-rod truss, three finned RTG cylinders in tandem, faint warm heat glow
  const ra = v3(.88, -.6, 0), rb = v3(3.5, -1.05, .35), rdir = rb.clone().sub(ra).normalize();
  rod(ra.clone().add(v3(0, .08, 0)), rb.clone().add(v3(0, .08, 0)), .025, metM); rod(ra.clone().add(v3(0, -.08, 0)), rb.clone().add(v3(0, -.08, 0)), .025, metM);
  for (let k = 0; k < 6; k++) { const s0 = k / 6, s1 = (k + 1) / 6; rod(ra.clone().lerp(rb, s0).add(v3(0, .08, 0)), ra.clone().lerp(rb, s1).add(v3(0, -.08, 0)), .012, metM); }
  const rtgM = new T.MeshStandardMaterial({ color: '#3a3c46', roughness: .5, metalness: .6, envMap: E, envMapIntensity: .3, emissive: '#ff7a3a', emissiveIntensity: .05 });
  rim(rtgM, 1.0);
  const rtgs = [];
  for (let k = 0; k < 3; k++) { const G = new T.Group(); PROBE.add(G); G.position.copy(ra.clone().lerp(rb, .45 + k * .22)); G.quaternion.setFromUnitVectors(v3(0, 1, 0), rdir);
    add(new T.CylinderGeometry(.17, .17, .48, 20), rtgM, G); add(new T.CylinderGeometry(.19, .19, .04, 20).translate(0, .25, 0), metM, G); add(new T.CylinderGeometry(.19, .19, .04, 20).translate(0, -.25, 0), metM, G);
    for (let f = 0; f < 6; f++) { const a = f / 6 * 6.283; const fin = add(new T.BoxGeometry(.13, .44, .018), rtgM, G); fin.position.set(.23 * Math.cos(a), 0, .23 * Math.sin(a)); fin.rotation.y = -a; }
    rtgs.push(G); }
  // science boom (-X) with the scan platform
  const sa = v3(-.88, -.5, 0), sb = v3(-2.5, -.55, .3);
  rod(sa.clone().add(v3(0, .07, .05)), sb.clone().add(v3(0, .07, .05)), .03, metM); rod(sa.clone().add(v3(0, -.07, -.05)), sb.clone().add(v3(0, -.07, -.05)), .03, metM);
  const PLAT = new T.Group(); PROBE.add(PLAT); PLAT.position.copy(sb); PLAT.rotation.set(.2, -.5, .1);
  add(new T.BoxGeometry(.5, .32, .42), darkM, PLAT).position.set(-.15, 0, 0);
  add(new T.BoxGeometry(.3, .22, .3), foilM, PLAT).position.set(-.15, .27, 0);
  const camA = add(new T.CylinderGeometry(.08, .09, .62, 18).rotateZ(Math.PI / 2), metM, PLAT); camA.position.set(.33, .06, .08);
  const camB = add(new T.CylinderGeometry(.07, .075, .34, 16).rotateZ(Math.PI / 2), metM, PLAT); camB.position.set(.2, -.1, -.12);
  add(new T.BoxGeometry(.22, .2, .24), metM, PLAT).position.set(-.15, -.06, .3);
  // magnetometer boom: long thin mast with collar rings and a sensor canister at the tip
  const ma = v3(-.6, -.75, -.55), md = v3(-.45, -.18, -.87).normalize(), mb = ma.clone().addScaledVector(md, 12.5);
  rod(ma, mb, .035, metM); add(new T.CylinderGeometry(.16, .16, .4, 16), darkM).position.copy(ma);
  for (let k = 1; k < 13; k++) { const ring = add(new T.TorusGeometry(.05, .015, 6, 12), metM); ring.position.copy(ma).addScaledVector(md, k); ring.quaternion.setFromUnitVectors(v3(0, 0, 1), md); }
  { const c = add(new T.CylinderGeometry(.09, .09, .3, 14), darkM); c.position.copy(mb); c.quaternion.setFromUnitVectors(v3(0, 1, 0), md); }
  PROBE.quaternion.setFromUnitVectors(v3(0, 1, 0), SD);               // the dish faces Earth, i.e. (from out here) the Sun
  PROBE.quaternion.premultiply(new T.Quaternion().setFromAxisAngle(SD, p.roll == null ? 2.3 : +p.roll));
  PROBE.updateMatrixWorld(true);
  // sun-catching lip: a thin additive ring on the dish rim, bright where the sunlit inside of the dish shows over the lip
  { const g = new T.TorusGeometry(DR + .045, .028, 8, 160).rotateX(Math.PI / 2).translate(0, yP(DR) + .02, 0), P = g.attributes.position, col = new Float32Array(P.count * 3);
    const sp = V.clone().negate().applyQuaternion(PROBE.quaternion.clone().invert()); sp.y = 0; sp.normalize();   // the near lip, which shows on the Sun's side of the silhouette
    for (let i = 0; i < P.count; i++) { const rx = P.getX(i), rz = P.getZ(i), l = Math.hypot(rx, rz) || 1, b = Math.pow(Math.max(0, (rx * sp.x + rz * sp.z) / l), 1.6) * 2.2; col.set([b, b * .78, b * .5], i * 3); }
    g.setAttribute('color', new T.BufferAttribute(col, 3));
    add(g, new T.MeshBasicMaterial({ vertexColors: true, transparent: true, blending: T.AdditiveBlending, depthWrite: false })); }
  const rtgGlow = rtgs.map(G => { const s = ctx.glow(PROBE, '#ff9a55', .9, .12); s.position.copy(G.position); return s; });
  const dishGlint = ctx.glow(PROBE, '#fff3dc', 3, 0); dishGlint.position.set(-DR * .7, yP(DR) + .05, DR * .7);

  // ---------------- sun, glints, Proxima, path ----------------
  const sprite = (col, op) => { const s = new T.Sprite(new T.SpriteMaterial({ map: dotTex(), color: col, transparent: true, opacity: op, blending: T.AdditiveBlending, depthWrite: false, fog: false })); S.add(s); return s; };
  const sunCore = sprite(new T.Color(4, 3.7, 3.2), 1), sunHalo = sprite(new T.Color('#ffc874'), .55), sunWide = sprite(new T.Color('#ff9c50'), .22);
  [sunCore, sunHalo, sunWide].forEach(s => s.position.copy(SUN));
  const glint = sprite(new T.Color(2.2, 1.9, 1.4), 0), proxS = sprite(new T.Color(2.2, .8, .45), .8), proxH = sprite(new T.Color('#ff5a3a'), .25);
  proxS.position.copy(PROX); proxH.position.copy(PROX);
  const NPATH = 260, pg = new T.BufferGeometry(), pa = new Float32Array(NPATH * 3), pc = new Float32Array(NPATH * 3);
  pg.setAttribute('position', new T.BufferAttribute(pa, 3)); pg.setAttribute('color', new T.BufferAttribute(pc, 3));
  const path = new T.Points(pg, new T.PointsMaterial({ size: 3.4, map: dotTex(), vertexColors: true, transparent: true, blending: T.AdditiveBlending, depthWrite: false, sizeAttenuation: false }));
  path.frustumCulled = false; S.add(path);
  const sunMark = sprite(new T.Color(2.6, 1.7, .6), 0), sunMarkH = sprite(new T.Color('#ffb347'), 0);
  // ---------------- Milky Way disc (galaxy cue): stars + diffuse glow, one draw call each ----------------
  function galaxy(n, sz, seed, glowLayer) { const g = new T.BufferGeometry(), a = new Float32Array(n * 3), c = new Float32Array(n * 3), r = rng(seed);
    for (let i = 0; i < n; i++) { let x, y, z, col;
      if (r() < (glowLayer ? .25 : .17)) { const rr = Math.abs((r() + r() + r() - 1.5)) * .2, ang = r() * 6.283; x = rr * Math.cos(ang) * 1.4; y = rr * Math.sin(ang) * .7; z = (r() + r() - 1) * .05 * (1 - rr * 3);
        const ca = Math.cos(.45), sa = Math.sin(.45), xx = x * ca - y * sa; y = x * sa + y * ca; x = xx; col = [.8, .6, .36]; }
      else { const arm = Math.floor(r() * 4), rr = .1 + Math.pow(r(), .75) * .92, disc = r() < .2, ang = arm * Math.PI / 2 + Math.log(rr / .12) / Math.tan(.23) + (disc ? r() * 6.283 : (r() + r() - 1) * (glowLayer ? .5 : .55) / (.4 + rr));
        x = rr * Math.cos(ang); y = rr * Math.sin(ang); z = (r() + r() - 1) * .018; const tp = r(); col = tp < .45 ? [.72, .78, 1] : tp < .75 ? [.78, .66, 1] : [1, .85, .62]; }
      const br = (glowLayer ? .35 + .3 * r() : .3 + .7 * Math.pow(r(), 2.5)) * (1.2 - .7 * Math.min(1, Math.hypot(x, y)));
      const w = GC.clone().addScaledVector(GA, x * RG).addScaledVector(GB, y * RG).addScaledVector(NG, z * RG); a.set([w.x, w.y, w.z], i * 3); c.set([col[0] * br, col[1] * br, col[2] * br], i * 3); }
    g.setAttribute('position', new T.BufferAttribute(a, 3)); g.setAttribute('color', new T.BufferAttribute(c, 3));
    const P = new T.Points(g, new T.PointsMaterial({ size: sz, map: dotTex(), vertexColors: true, transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, sizeAttenuation: true }));
    P.frustumCulled = false; S.add(P); return P; }
  const galS = galaxy(60000, RG * .011, 31, false), galG = galaxy(4000, RG * .11, 32, true);
  const galCore = sprite(new T.Color('#ffcf8a'), 0); galCore.position.copy(GC);

  // ---------------- dust, lights ----------------
  // pull-back streaks (log-spaced along the far direction) and close-up drifting motes
  const FDIR = V.clone().multiplyScalar(.4).addScaledVector(SD, .6).normalize().negate();
  const NPB = 520, pbs = streaks(S, NPB, { minPx: 1.4, near: [0, 1e-4] }), pbB = [];
  { const r = rng(17), a1 = new T.Vector3().crossVectors(FDIR, UP).normalize(), a2 = new T.Vector3().crossVectors(FDIR, a1).normalize();
    for (let i = 0; i < NPB; i++) { const rr = Math.exp(Math.log(8) + (Math.log(2500) - Math.log(8)) * r()), f = .2 + 1.2 * Math.pow(r(), .8), a = r() * 6.283, tp = r(), br = .5 + .7 * r();
      const P = FDIR.clone().multiplyScalar(rr).addScaledVector(a1, Math.cos(a) * f * rr).addScaledVector(a2, Math.sin(a) * f * rr);
      pbB.push({ P, r: rr, c: (tp < .6 ? [1, .88, .7] : tp < .85 ? [.78, .84, 1] : [.8, .68, 1]).map(x => x * br) }); } }
  const NMO = 160, motes = streaks(S, NMO, { minPx: 1.6, near: [1.5, 5] }), moB = [], MBX = [34, 20, 34];
  { const r = rng(23); for (let i = 0; i < NMO; i++) moB.push([r() * MBX[0], r() * MBX[1], r() * MBX[2], .6 + .8 * r(), r()]); }
  const dust = K.snow(S, { n: 700, box: [40, 26, 40], size: .07, opacity: .45, color: '#ffdcae', fall: .02, seed: 9 });
  const sunL = new T.DirectionalLight('#fff0d8', 3.2); sunL.position.copy(SD).multiplyScalar(50); S.add(sunL);
  const fillL = new T.DirectionalLight('#9aa6c0', .8); S.add(fillL);
  S.add(new T.HemisphereLight('#3a4270', '#07080f', .45));

  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .1, 1e5); ctx.side(cam, p.side == null ? .14 : p.side);
  const tmp = new T.Vector3();
  // camera state = target + direction * distance; each cue blends toward a new state (distance in log space; the target follows
  // in proportion to the distance, so the old subject stays in frame while the camera backs away)
  function blend(a, b, w) { if (w <= 0) return a; if (w >= 1) return b;
    const d = Math.exp(Math.log(a.d) + (Math.log(b.d) - Math.log(a.d)) * w), k = Math.abs(b.d - a.d) > 1e-6 ? (d - a.d) / (b.d - a.d) : w;
    return { t: a.t.clone().lerp(b.t, k), dir: a.dir.clone().lerp(b.dir, w).normalize(), d, fov: a.fov + (b.fov - a.fov) * w }; }
  const MID = PD.clone().multiplyScalar(GAP * .4), NV = V.clone().negate().addScaledVector(PD, V.dot(PD)).normalize().addScaledVector(PD, -.3).normalize();
  const GDIR = NG.clone().multiplyScalar(Math.cos(.95)).addScaledVector(GA, Math.sin(.95)).normalize();
  const atT = (c, d, tt) => c == null ? 0 : sm(cue(c), cue(c) + d, tt);
  function camPos(tt, out) { const uu = tt - ctx.t0, oa = .22 * Math.sin(uu * .045) - .12 + uu * .006, ob = .06 * Math.sin(uu * .06);
    const cd = V.clone().negate().applyAxisAngle(UP, oa).applyAxisAngle(RT, ob).normalize();
    let q = { t: UP.clone().multiplyScalar(-.7), dir: cd, d: 15 - 1.2 * sm(0, 30, uu), fov: 40 };
    q = blend(q, { t: v3(0, 0, 0), dir: FDIR.clone(), d: 1500, fov: 38 }, atT(p.far, 6.5, tt));
    q = blend(q, { t: MID, dir: NV, d: 66000, fov: 38 }, atT(p.proxima, 6.5, tt));
    return out.copy(q.t).addScaledVector(q.dir, q.d); }
  const cA = v3(0, 0, 0), cB = v3(0, 0, 0), dv = v3(0, 0, 0);
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const wF = at(p.far, 6.5), wP = at(p.proxima, 6.5), wG = at(p.galaxy, 9), gl = p.launch == null ? 0 : Math.max(0, Math.sin(Math.PI * Math.min(1, Math.max(0, (t - cue(p.launch)) / 1.6))));
    // close orbit: slow drift around the probe (shows the depth of the dish and booms)
    const oa = .22 * Math.sin(u * .045) - .12 + u * .006, ob = .06 * Math.sin(u * .06);
    const cdir = V.clone().negate().applyAxisAngle(UP, oa).applyAxisAngle(RT, ob).normalize();
    let st = { t: UP.clone().multiplyScalar(-.7), dir: cdir, d: 15 - 1.2 * sm(0, 30, u), fov: 40 };
    st = blend(st, { t: v3(0, 0, 0), dir: V.clone().multiplyScalar(.4).addScaledVector(SD, .6).normalize().negate(), d: 1500, fov: 38 }, wF);
    st = blend(st, { t: MID, dir: NV, d: 66000, fov: 38 }, wP);
    st = blend(st, { t: GC.clone().lerp(v3(0, 0, 0), .25), dir: GDIR, d: 3.3 * RG, fov: 38 }, wG);
    cam.position.copy(st.t).addScaledVector(st.dir, st.d); cam.lookAt(st.t);
    const D = Math.max(1, cam.position.length());
    cam.near = Math.max(.05, D * .004); cam.far = Math.max(2000, st.d * 6 + 5e4); cam.fov = vf(st.fov); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    SKYG.position.copy(cam.position); SKYG.scale.setScalar(cam.near * 40);
    // rim light direction in view space
    RIMU.value.copy(SD).transformDirection(cam.matrixWorldInverse);
    fillL.position.copy(cam.position).add(v3(0, 6, 0)).sub(cam.position.clone().normalize().multiplyScalar(0)).normalize().multiplyScalar(30);
    // probe: real meshes while big enough on screen, a glint once it is only a few pixels
    const px = 4 * ctx.H / (2 * Math.tan(cam.fov * Math.PI / 360) * D), meshOn = px > 10;
    PROBE.visible = meshOn; dust.points.visible = D < 60;
    const gk = sm(30, 12, px) * (1 - .85 * wG);
    glint.material.opacity = gk; glint.scale.setScalar(D * .011 * (1 + .3 * wP)); glint.position.set(0, 0, 0);
    rtgGlow.forEach((s, i) => s.material.opacity = .12 + .03 * Math.sin(t * .7 + i));
    dishGlint.material.opacity = .7 * gl; dishGlint.scale.setScalar(1 + 2 * gl);
    // sun: constant angular size (small and very bright), turns into a star point, then a gold marker in the galaxy view
    const sd = cam.position.distanceTo(SUN), gsun = 1 - wG;
    sunCore.scale.setScalar(sd * .012 * (1 - .45 * wF) * gsun); sunHalo.scale.setScalar(sd * .1 * (1 - .55 * wF) * gsun); sunWide.scale.setScalar(sd * (.32 + .9 * (1 - wF)) * (1 - .6 * wF) * gsun);
    sunHalo.material.opacity = .55 * gsun; sunWide.material.opacity = .16 * (1 - .5 * wP) * gsun;
    sunMark.position.copy(SUN).multiplyScalar(.5); sunMark.material.opacity = wG; sunMark.scale.setScalar(cam.position.distanceTo(SUN) * .014); sunMarkH.position.copy(sunMark.position); sunMarkH.material.opacity = .35 * wG; sunMarkH.scale.setScalar(cam.position.distanceTo(SUN) * .05);
    skyU.uH.value = (1 - .7 * wF) * (1 - wP);
    // Proxima: an ordinary faint star until the camera turns toward it
    const pdist = cam.position.distanceTo(PROX), pk = (.45 + .55 * wP) * (1 - wG);
    proxS.scale.setScalar(pdist * .0065 * (1 + .4 * wP)); proxH.scale.setScalar(pdist * .03); proxS.material.opacity = .9 * pk; proxH.material.opacity = .28 * pk * (.3 + .7 * wP);
    // dotted path: the travelled part (gold) barely leaves the probe; ghost dots mark the rest; gone in the galaxy view
    const pv = wP * (1 - sm(.0, .35, wG)), done = .012 + .02 * sm(cue(p.proxima, 1e9) + 2, cue(p.proxima, 1e9) + 40, t);
    for (let i = 0; i < NPATH; i++) { const f = (i + .5) / NPATH; tmp.copy(PROX).multiplyScalar(f); pa.set([tmp.x, tmp.y, tmp.z], i * 3); pc.set([.05 * pv, .045 * pv, .05 * pv], i * 3); }
    const NG2 = 18; for (let j = 0; j < NG2; j++) { const f = done * (j + .5) / NG2, i = j; tmp.copy(PROX).multiplyScalar(f); pa.set([tmp.x, tmp.y, tmp.z], i * 3); const v = pv * (1.5 - .7 * j / NG2); pc.set([v, v * .7, v * .26], i * 3); }
    pg.attributes.position.needsUpdate = true; pg.attributes.color.needsUpdate = true; path.visible = pv > .001;
    // galaxy disc fades in only once the camera is far enough for its points to be small
    const gv = sm(Math.log(RG * .15), Math.log(RG * 1.1), Math.log(st.d));
    galS.material.opacity = .75 * gv; galG.material.opacity = .2 * gv; galS.visible = galG.visible = gv > .001;
    galCore.material.opacity = .5 * gv; galCore.scale.setScalar(RG * .55);
    stars.forEach(s => s.material.opacity = 1 - .85 * gv); skyU.uK.value = 1 - gv;
    if (dust.points.visible) dust.update(t, [0, 0, 0]);
    // pull-back streaks: only while the `far` move runs (eased), each point fades in once the camera has passed it and out as it
    // shrinks toward the vanishing point; tail = where the point was relative to the camera 0.07 s ago
    const pe = p.far == null ? 0 : sm(0, .12, wF) * (1 - sm(.8, 1, wF)) * (1 - wP);
    pbs.mesh.visible = pe > 0;
    if (pe > 0) { camPos(t, cA); camPos(t - .07, cB); dv.copy(cA).sub(cB);
      for (let i = 0; i < NPB; i++) { const b = pbB[i], dc = b.P.distanceTo(cA), q = dc / b.r, k = pe * sm(.25, .7, q) * sm(7, 2.5, q);
        if (k <= 0) { pbs.hide(i); continue; } const dl = Math.min(1, dc * .6 / Math.max(1e-6, dv.length()));
        pbs.set(i, b.P.x, b.P.y, b.P.z, b.P.x + dv.x * dl, b.P.y + dv.y * dl, b.P.z + dv.z * dl, b.r * .004, b.c[0] * k, b.c[1] * k, b.c[2] * k); }
      pbs.commit(); }
    // close-up motes: slow drift through a box around the probe, faded at the box faces so wrapping never pops
    const me = 1 - sm(.02, .25, wF); motes.mesh.visible = me > 0 && D < 60;
    if (motes.mesh.visible) { for (let i = 0; i < NMO; i++) { const m = moB[i], c = [0, 0, 0];
        for (let j = 0; j < 3; j++) { const vj = [.32, .05, -.14][j] * m[3], x = (((m[j] + vj * t) % MBX[j]) + MBX[j]) % MBX[j]; c[j] = x - MBX[j] / 2; m[5 + j] = sm(0, 3, x) * sm(MBX[j], MBX[j] - 3, x); }
        const k = me * .5 * m[3] * m[5] * m[6] * m[7] * (.7 + .3 * Math.sin(t * .5 + m[4] * 9));
        motes.set(i, c[0], c[1], c[2], c[0] - .25 * m[3], c[1] - .04, c[2] + .1, .05, k, k * .88, k * .7); }
      motes.commit(); }
  } };
};
