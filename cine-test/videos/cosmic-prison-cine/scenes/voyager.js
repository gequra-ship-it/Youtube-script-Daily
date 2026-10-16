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
// jdt / sdt (numbers, s): shift the Jupiter / Saturn flyby later than its cue (default 0)
// jlead / slead (numbers, s): how long before closest approach Jupiter / Saturn start fading in (default 9 / 5)
// params (cues, all optional): { launch (a short sun glint across the dish), far, proxima, galaxy, side: .14 }
// Defaults: without cues the probe stays in its slow close-up orbit (a complete shot on its own).
// speed pass (2026-10-16): during the `far` pull-back, dust/star streaks spread log-evenly along the way (8 to 2500 units out, so
// the stream looks the same at every scale) rush in from the frame edges and shrink toward the probe; each streak is the motion of
// its point relative to the camera over the last 0.07 s (longer when the camera moves faster), eased in and out with the move.
// In the close-up a sparse layer of soft motes drifts slowly across the view (near parallax for depth).
// attention pass (2026-10-16, all new params optional cues; absent = the old behaviour):
//   flyin   — landing time of a fast fly-in from deep space (starts at the shot start): the camera rushes in from ~700 units
//             with the probe silhouetted against the Sun (screen-space lens flare + ghosts), streaks whooshing past
//   jupiter / saturn — closest-approach times of the Grand Tour: the camera swings round to a chase view behind the probe,
//             Jupiter (bands, Great Red Spot) grows from a disc and whips past huge while the path bends (slingshot: the chase
//             camera turns with the heading), then Saturn and its lit, shadowed rings sweep by; speed streaks stream past the
//             probe; after Saturn the camera completes the 360 deg turn back to the hero close-up (exactly the old pose)
//   oort    — after `far`, keep pulling back until the Sun's faint Oort-cloud shell (its outer gravitational grip) surrounds it
//   lapse   — dive onto the Sun-Proxima line and time-lapse along it: one ring per millennium (73), each ring pulses as the
//             camera passes it, accelerating (pulses pour past), field stars streak by; Voyager's glint barely creeps
//   zoom    — accelerating log zoom-out from Proxima through local star layers to the full Milky Way (galaxy cue = landing,
//             Sun in a spiral arm); a 4.2-ly scale ring around the Sun shrinks to a speck, a 100,000-ly ring draws round the disc
//   edge    — the camera turns across the disc toward the rim and the dark beyond
//   flare   — lens-flare strength outside the fly-in (default .5 when flyin is set, else 0)
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
  // with the zoom cue the arm pattern is turned so the Sun sits inside a spiral arm (the Orion arm)
  const ARMPH = p.zoom == null ? 0 : Math.atan2(-.1, .53) - Math.log(Math.hypot(.53, .1) / .12) / Math.tan(.23);
  function galaxy(n, sz, seed, glowLayer) { const g = new T.BufferGeometry(), a = new Float32Array(n * 3), c = new Float32Array(n * 3), r = rng(seed);
    for (let i = 0; i < n; i++) { let x, y, z, col;
      if (r() < (glowLayer ? .25 : .17)) { const rr = Math.abs((r() + r() + r() - 1.5)) * .2, ang = r() * 6.283; x = rr * Math.cos(ang) * 1.4; y = rr * Math.sin(ang) * .7; z = (r() + r() - 1) * .05 * (1 - rr * 3);
        const ca = Math.cos(.45), sa = Math.sin(.45), xx = x * ca - y * sa; y = x * sa + y * ca; x = xx; col = [.8, .6, .36]; }
      else { const arm = Math.floor(r() * 4), rr = .1 + Math.pow(r(), .75) * .92, disc = r() < .2, ang = ARMPH + arm * Math.PI / 2 + Math.log(rr / .12) / Math.tan(.23) + (disc ? r() * 6.283 : (r() + r() - 1) * (glowLayer ? .5 : .55) / (.4 + rr));
        x = rr * Math.cos(ang); y = rr * Math.sin(ang); z = (r() + r() - 1) * .018; const tp = r(); col = tp < .45 ? [.72, .78, 1] : tp < .75 ? [.78, .66, 1] : [1, .85, .62]; }
      const br = (glowLayer ? .35 + .3 * r() : .3 + .7 * Math.pow(r(), 2.5)) * (1.2 - .7 * Math.min(1, Math.hypot(x, y)));
      const w = GC.clone().addScaledVector(GA, x * RG).addScaledVector(GB, y * RG).addScaledVector(NG, z * RG); a.set([w.x, w.y, w.z], i * 3); c.set([col[0] * br, col[1] * br, col[2] * br], i * 3); }
    g.setAttribute('position', new T.BufferAttribute(a, 3)); g.setAttribute('color', new T.BufferAttribute(c, 3));
    const P = new T.Points(g, new T.PointsMaterial({ size: sz, map: dotTex(), vertexColors: true, transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, sizeAttenuation: true }));
    P.frustumCulled = false; S.add(P); return P; }
  const galS = galaxy(60000, RG * .011, 31, false), galG = galaxy(4000, RG * .11, 32, true);
  const galCore = sprite(new T.Color('#ffcf8a'), 0); galCore.position.copy(GC);


  // ---------------- dust, lights ----------------
  const has = k => p[k] != null, cu = k => cue(p[k]), c01 = x => Math.min(1, Math.max(0, x));
  // log-spaced streak stream along an axis (points r0..r1 out, spread f * r around it); run() draws each point's motion relative to
  // the camera over the last 0.07 s, visible only while the camera passes it at a distance comparable to its own scale
  function mkStream(axis, r0, r1, n, seed) { const s = streaks(S, n, { minPx: 1.4, near: [0, 1e-4] }), B = [], r = rng(seed);
    const a1 = new T.Vector3().crossVectors(axis, UP).normalize(), a2 = new T.Vector3().crossVectors(axis, a1).normalize();
    for (let i = 0; i < n; i++) { const rr = Math.exp(Math.log(r0) + (Math.log(r1) - Math.log(r0)) * r()), f = .2 + 1.2 * Math.pow(r(), .8), a = r() * 6.283, tp = r(), br = .5 + .7 * r();
      const P = axis.clone().multiplyScalar(rr).addScaledVector(a1, Math.cos(a) * f * rr).addScaledVector(a2, Math.sin(a) * f * rr);
      B.push({ P, r: rr, c: (tp < .6 ? [1, .88, .7] : tp < .85 ? [.78, .84, 1] : [.8, .68, 1]).map(x => x * br) }); }
    return { s, run(env, cA, dv) { s.mesh.visible = env > 0; if (!(env > 0)) return; const L = Math.max(1e-6, dv.length());
      for (let i = 0; i < n; i++) { const b = B[i], dc = b.P.distanceTo(cA), q = dc / b.r, k = env * sm(.25, .7, q) * sm(7, 2.5, q);
        if (k <= 0) { s.hide(i); continue; } const dl = Math.min(1, dc * .6 / L);
        s.set(i, b.P.x, b.P.y, b.P.z, b.P.x + dv.x * dl, b.P.y + dv.y * dl, b.P.z + dv.z * dl, b.r * .004, b.c[0] * k, b.c[1] * k, b.c[2] * k); }
      s.commit(); } }; }
  const FDIR = V.clone().multiplyScalar(.4).addScaledVector(SD, .6).normalize().negate();
  const pbStream = mkStream(FDIR, 8, has('oort') ? 30000 : 2500, has('oort') ? 760 : 520, 17);
  const FI = has('flyin') ? Math.max(ctx.t0 + 1, cu('flyin')) : null, FIDIR = SD.clone().negate().lerp(V.clone().negate(), .3).normalize();
  const fiStream = FI == null ? null : mkStream(FIDIR, 12, 760, 380, 41);
  const NMO = 160, motes = streaks(S, NMO, { minPx: 1.6, near: [1.5, 5] }), moB = [], MBX = [34, 20, 34];
  { const r = rng(23); for (let i = 0; i < NMO; i++) moB.push([r() * MBX[0], r() * MBX[1], r() * MBX[2], .6 + .8 * r(), r()]); }
  const dust = K.snow(S, { n: 700, box: [40, 26, 40], size: .07, opacity: .45, color: '#ffdcae', fall: .02, seed: 9 });
  const sunL = new T.DirectionalLight('#fff0d8', 3.2); sunL.position.copy(SD).multiplyScalar(50); S.add(sunL);
  const fillL = new T.DirectionalLight('#9aa6c0', .8); S.add(fillL);
  S.add(new T.HemisphereLight('#3a4270', '#07080f', .45));

  // soft points with a pixel size clamped to [2, max] (smaller ones dim instead, so nothing shimmers or balloons near the lens)
  function cpoints(pos, col, o) { const g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(pos, 3)); g.setAttribute('color', new T.BufferAttribute(col, 3));
    const U = { uS: { value: o.size }, uMax: { value: o.max || 4 }, uH: { value: ctx.H }, uO: { value: 0 }, uNear: { value: o.near || 0 }, uMap: { value: dotTex() } };
    const P = new T.Points(g, new T.ShaderMaterial({ uniforms: U, transparent: true, depthWrite: false, blending: T.AdditiveBlending,
      vertexShader: `attribute vec3 color; uniform float uS, uMax, uH, uO, uNear; varying vec3 vC;
        void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.); float z = max(-mv.z, 1e-4), px = uS * uH * .5 * projectionMatrix[1][1] / z;
          vC = color * uO * min(1., px / 2.) * smoothstep(uNear * .4, uNear, z) * step(0., -mv.z); gl_PointSize = clamp(px, 2., uMax); gl_Position = projectionMatrix * mv; }`,
      fragmentShader: `uniform sampler2D uMap; varying vec3 vC;
        void main(){ float a = texture2D(uMap, gl_PointCoord).r; gl_FragColor = vec4(vC * a, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` }));
    P.frustumCulled = false; S.add(P); return { P, U }; }
  // Oort cloud: a thick faint shell of icy specks around the Sun (oort cue)
  let oortP = null;
  if (has('oort')) { const n = 3600, a = new Float32Array(n * 3), c = new Float32Array(n * 3), r = rng(51);
    for (let i = 0; i < n; i++) { const uu = r() * 2 - 1, th = r() * 6.283, q = Math.sqrt(1 - uu * uu), rr = 6000 + 7000 * Math.pow(r(), .6), br = .3 + .7 * r();
      a.set([SUN.x + rr * q * Math.cos(th), SUN.y + rr * uu, SUN.z + rr * q * Math.sin(th)], i * 3); c.set([.6 * br, .76 * br, br], i * 3); }
    oortP = cpoints(a, c, { size: 60, max: 3, near: 900 }); }
  // local star layers for the zoom-out (10 ly .. 14,000 ly around the Sun; flattened into the disc beyond ~300 ly)
  const LAYR = [1e5, 6e5, 3.6e6, 2.2e7, 1.3e8], layers = [];
  if (has('zoom')) LAYR.forEach((Ri, li) => { const n = 1500, a = new Float32Array(n * 3), c = new Float32Array(n * 3), r = rng(80 + li), hz = Math.min(Ri, 2.9e6);
    for (let i = 0; i < n; i++) { const ang = r() * 6.283, rr = Ri * Math.sqrt(r()), z = (r() + r() + r() - 1.5) * hz * .8, tp = r(), br = .35 + .9 * Math.pow(r(), 2.2);
      const w = GA.clone().multiplyScalar(Math.cos(ang) * rr).addScaledVector(GB, Math.sin(ang) * rr).addScaledVector(NG, z);
      a.set([w.x, w.y, w.z], i * 3); const col = tp < .25 ? [.72, .8, 1] : tp < .8 ? [1, .95, .88] : [1, .78, .55]; c.set(col.map(x => x * br), i * 3); }
    layers.push(Object.assign(cpoints(a, c, { size: Ri * .004, max: 3.2, near: Ri * .05 }), { Ri })); });

  // ---------------- Grand Tour (jupiter / saturn cues): heading turns at each slingshot, chase camera, planets ----------------
  const TJ = has('jupiter') ? cu('jupiter') + (+p.jdt || 0) : null, TS = TJ != null && has('saturn') ? cu('saturn') + (+p.sdt || 0) : null, TOUR = TJ != null, SG = -1, D3 = Math.PI * 2 / 3;
  const TR = TOUR ? { i0: Math.max((FI || ctx.t0) + .3, TJ - 6), i1: TJ - 3.4, o0: (TS || TJ) + 1.8, o1: Math.min((TS || TJ) + 5.6, has('far') ? cu('far') - .4 : ctx.t1) } : null;
  const heading = tt => TOUR ? D3 * sm(TJ - 1.7, TJ + 1.7, tt) + (TS != null ? D3 * sm(TS - 1.7, TS + 1.7, tt) : 0) : 0;
  // camera orbit about the probe: swing in to the chase view, turn with the heading, then finish the full turn (back to the hero pose)
  // PH0 sets the initial heading so both planets show their day side while they pass (checked with the Sun direction SD)
  const PH0 = Math.PI / 2, HT = D3 * (TS != null ? 2 : 1), OUT = SG * Math.PI * 2 - (SG * D3 + PH0 + SG * HT);
  const tourTheta = tt => TOUR ? (SG * D3 + PH0) * sm(TR.i0, TR.i1, tt) + SG * heading(tt) + OUT * sm(TR.o0, TR.o1, tt) : 0;
  const velDir = (tt, out) => out.copy(V).applyAxisAngle(UP, SG * (D3 + heading(tt)) + PH0);
  function hsh(x, y) { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); }
  function vnp(x, y, P) { const i = Math.floor(x), j = Math.floor(y), f = x - i, g = y - j, u = f * f * (3 - 2 * f), v = g * g * (3 - 2 * g), i0 = ((i % P) + P) % P, i1 = (i0 + 1) % P;
    return (hsh(i0, j) * (1 - u) + hsh(i1, j) * u) * (1 - v) + (hsh(i0, j + 1) * (1 - u) + hsh(i1, j + 1) * u) * v; }
  const fbm = (x, y, P) => vnp(x, y, P) * .5 + vnp(x * 2, y * 2, P * 2) * .25 + vnp(x * 4, y * 4, P * 4) * .15 + vnp(x * 8, y * 8, P * 8) * .1;
  function planetTex(jup) { const Wt = 1024, Ht = 512, cv = document.createElement('canvas'); cv.width = Wt; cv.height = Ht; const g = cv.getContext('2d'), im = g.createImageData(Wt, Ht), d = im.data;
    const mix = (a, b, k) => [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, a[2] + (b[2] - a[2]) * k];
    for (let y = 0; y < Ht; y++) for (let x = 0; x < Wt; x++) { const lat = (.5 - (y + .5) / Ht) * Math.PI, lon = (x + .5) / Wt * 6.2832, X = x / Wt;
      const warp = (fbm(X * 8, y / Ht * 24, 8) - .5) * (jup ? .09 : .04), b = lat + warp + (jup ? .025 * Math.sin(lon * 5 + lat * 30) * fbm(X * 4, y / Ht * 6, 4) : 0);
      const z = .5 + .5 * Math.cos(b * (jup ? 14 : 11) + 1.3 * Math.sin(b * 5)), fine = fbm(X * 64, y / Ht * 260, 64);
      let c = jup ? mix([.6, .4, .28], [.95, .89, .79], Math.pow(z, 1.4)) : mix([.76, .64, .45], [.93, .85, .67], z);
      if (jup && Math.abs(b) < .1) c = mix(c, [.92, .78, .6], .5);
      c = mix(c, jup ? [.58, .54, .52] : [.64, .66, .62], sm(.95, 1.35, Math.abs(lat)));
      const k = (jup ? .84 : .92) + (jup ? .32 : .16) * fine; c = c.map(q => q * k);
      if (jup) { let dl = lon - 4.0; dl -= Math.round(dl / 6.2832) * 6.2832; const ex = dl / .22, ey = (lat + .38) / .085, e = ex * ex + ey * ey;
        if (e < 2.4) { const sw = fbm(X * 40 + e * 1.5, y / Ht * 80, 40); c = mix(c, [.97, .9, .8], .55 * sm(2.4, 1.5, e) * sm(.9, 1.3, e)); c = mix(c, [.78 + .1 * sw, .38, .24], sm(1.25, .5, e)); } }
      const o = (y * Wt + x) * 4; d[o] = 255 * Math.min(1, c[0]); d[o + 1] = 255 * Math.min(1, c[1]); d[o + 2] = 255 * Math.min(1, c[2]); d[o + 3] = 255; }
    g.putImageData(im, 0, 0); const t = new T.CanvasTexture(cv); t.colorSpace = T.SRGBColorSpace; t.anisotropy = 8; return t; }
  function planetMat(tex, atm) { return new T.ShaderMaterial({ uniforms: { uMap: { value: tex }, uSun: { value: SD }, uAtm: { value: new T.Color(atm) }, uF: { value: 1 } },
    vertexShader: `varying vec2 vUv; varying vec3 vN, vW; void main(){ vUv = uv; vN = normalize(mat3(modelMatrix) * normal); vec4 w = modelMatrix * vec4(position, 1.); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `uniform sampler2D uMap; uniform vec3 uSun, uAtm; uniform float uF; varying vec2 vUv; varying vec3 vN, vW;
      void main(){ vec3 n = normalize(vN), v = normalize(cameraPosition - vW); float l = dot(n, uSun), mu = max(dot(n, v), 0.);
        vec3 c = texture2D(uMap, vUv).rgb; float dif = smoothstep(-.06, .45, l) * (.4 + .6 * max(l, 0.));
        vec3 col = c * dif * 2.2 * mix(.7, 1., pow(mu, .35)) + c * .01 + uAtm * pow(1. - mu, 3.) * smoothstep(-.15, .4, l) * .8;
        gl_FragColor = vec4(col * uF, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }); }
  function ringMat(R) { return new T.ShaderMaterial({ uniforms: { uSun: { value: SD }, uC: { value: new T.Vector3() }, uR: { value: R }, uN: { value: new T.Vector3(0, 1, 0) }, uF: { value: 1 } },
    transparent: true, depthWrite: false, side: T.DoubleSide,
    vertexShader: `varying vec3 vL, vW; void main(){ vL = position; vec4 w = modelMatrix * vec4(position, 1.); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `uniform vec3 uSun, uC, uN; uniform float uR, uF; varying vec3 vL, vW;
      float h1(float x){ return fract(sin(x * 91.7) * 43758.5); }
      void main(){ float r = length(vL) / uR;
        float d = .14 * smoothstep(1.24, 1.3, r) * (1. - smoothstep(1.5, 1.53, r));
        d += .9 * smoothstep(1.52, 1.56, r) * (1. - smoothstep(1.93, 1.95, r)) * (.8 + .2 * sin(r * 160.));
        d += .6 * smoothstep(2.02, 2.04, r) * (1. - smoothstep(2.25, 2.27, r)) * (1. - .85 * exp(-pow((r - 2.21) / .006, 2.)));
        d *= .7 + .6 * h1(floor(r * 300.));
        vec3 toC = uC - vW; float tt = dot(toC, uSun), sh = tt > 0. ? smoothstep(uR * .97, uR * 1.02, length(toC - uSun * tt)) : 1.;
        vec3 col = vec3(.86, .77, .62) * (.3 + .7 * abs(dot(uN, uSun))) * (.08 + .92 * sh) * 1.7;
        gl_FragColor = vec4(col * uF, clamp(d, 0., 1.) * uF);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }); }
  const PL = [], vtmp = new T.Vector3();
  function mkPlanet(jup, R, tc, b, v, beta) { const G = new T.Group(); S.add(G); G.visible = false; const m = planetMat(planetTex(jup), jup ? '#c9a77a' : '#e3cf98');
    const ball = new T.Mesh(new T.SphereGeometry(R, 128, 64), m); G.add(ball);
    const VE = velDir(tc, new T.Vector3()), N = new T.Vector3().crossVectors(UP, VE).normalize().multiplyScalar(SG);
    const C = N.clone().multiplyScalar(b * Math.cos(beta)).addScaledVector(UP, -b * Math.sin(beta));
    const AX = jup ? UP.clone().addScaledVector(VE, -.05).normalize() : UP.clone().multiplyScalar(Math.cos(.47)).addScaledVector(VE, -Math.sin(.47)).normalize();
    G.quaternion.setFromUnitVectors(v3(0, 1, 0), AX);
    let ring = null; if (!jup) { ring = new T.Mesh(new T.RingGeometry(1.24 * R, 2.27 * R, 256, 1), ringMat(R)); ring.rotation.x = -Math.PI / 2; G.add(ring); ring.material.uniforms.uN.value.copy(AX); }
    const o = { G, ball, ring, m, R, tc, v, C, f0: jup ? (p.jlead != null ? +p.jlead : 9) : (p.slead != null ? +p.slead : 5), spin: 0 }; PL.push(o);
    // Jupiter: turn the Great Red Spot (texture longitude 4.0, local direction (-cos, 0, sin)) toward the probe 1.2 s before closest approach
    if (jup) { const d = planetPos(o, tc - 1.2, new T.Vector3()).negate().applyQuaternion(G.quaternion.clone().invert()); o.spin = Math.atan2(d.x, d.z) - Math.atan2(-Math.cos(4), Math.sin(4)) - (tc - 1.2) * .1; } }
  function planetPos(o, tt, out) { out.copy(o.C); const n = 48, h = (tt - o.tc) / n; for (let i = 0; i < n; i++) { velDir(o.tc + (i + .5) * h, vtmp); out.addScaledVector(vtmp, -o.v * h); } return out; }
  if (TOUR) { mkPlanet(true, 110, TJ, 260, 210, .2); if (TS != null) mkPlanet(false, 88, TS, 360, 200, .5); }
  // the chase camera looks toward each planet as it whips past: extra yaw (and pitch, for a planet below) that follows the planet's
  // real direction minus a margin, so it sweeps huge across the frame instead of leaving it; eased in and out around closest approach
  const lkP = v3(0, 0, 0), lkV = v3(0, 0, 0), lkN = v3(0, 0, 0), lkA = v3(0, 0, 0);
  function lookAt2(tt) { let yaw = 0, pit = 0;
    for (const o of PL) { const w = sm(o.tc - 5, o.tc - 3, tt) * (1 - sm(o.tc + .2, o.tc + 2.6, tt)); if (w <= 0) continue;
      planetPos(o, tt, lkP); velDir(tt, lkV); lkN.crossVectors(UP, lkV).normalize().multiplyScalar(SG);
      const fw = lkP.dot(lkV), sd = lkP.dot(lkN), dn = -lkP.dot(UP);
      yaw += w * Math.min(1.3, Math.max(0, Math.atan2(sd, fw) - .42)); pit += w * Math.min(.8, Math.max(0, Math.atan2(dn, Math.hypot(fw, sd)) - .18)); }
    return [yaw, pit]; }
  // speed streaks streaming past the probe during the tour (recycling: s = fract(F(t) + f_k), F accelerates around each flyby)
  const ism = (a, b, x) => { if (x <= a) return 0; if (x >= b) return (b - a) / 2 + (x - b); const w = (x - a) / (b - a); return (b - a) * (w * w * w - w * w * w * w / 2); };
  const tsF = tt => .45 * tt + (TOUR ? 1.1 * (ism(TJ - 2.5, TJ - .5, tt) - ism(TJ + 1, TJ + 3, tt)) + (TS != null ? 1.1 * (ism(TS - 2.5, TS - .5, tt) - ism(TS + 1, TS + 3, tt)) : 0) : 0);
  const tsR = tt => .45 + (TOUR ? 1.1 * (sm(TJ - 2.5, TJ - .5, tt) - sm(TJ + 1, TJ + 3, tt)) + (TS != null ? 1.1 * (sm(TS - 2.5, TS - .5, tt) - sm(TS + 1, TS + 3, tt)) : 0) : 0);
  const NTS = 420, tsS = TOUR ? streaks(S, NTS, { minPx: 1.3, near: [3, 10] }) : null, tsB = [];
  if (TOUR) { const r = rng(61); for (let i = 0; i < NTS; i++) { const tp = r(); tsB.push({ f: r(), rad: 2.6 + 42 * Math.pow(r(), 1.5), a: r() * 6.283, br: .35 + .8 * r(), c: tp < .55 ? [1, .9, .75] : [.75, .85, 1] }); } }
  const TEND = TOUR ? (has('far') ? cu('far') : (TS || TJ) + 6) : 0;

  // ---------------- journey (lapse cue): one ring per millennium along the Sun-Proxima line, field stars streaking by ----------------
  const PB1 = new T.Vector3().crossVectors(PD, UP).normalize(), PB2 = new T.Vector3().crossVectors(PB1, PD).normalize();
  const NT = PD.clone().multiplyScalar(-.78).addScaledVector(UP, .5).addScaledVector(PB1, -.38).normalize();
  const L0 = has('lapse') ? cu('lapse') : null, Z0 = has('zoom') ? cu('zoom') : null;
  const LZ = L0 == null ? 0 : (Z0 != null ? Z0 : has('galaxy') ? cu('galaxy') - 8 : ctx.t1);
  const sLapse = tt => L0 == null ? 0 : .006 + .964 * (1 - Math.cos(Math.PI * Math.pow(c01((tt - L0 - 2.2) / Math.max(1, LZ - .1 - L0 - 2.2)), 1.6))) / 2;
  const NRING = 73, RSEG = 40, RRAD = GAP / NRING * .36, ringS = L0 == null ? null : streaks(S, NRING * RSEG, { minPx: 1.3, near: [60, 300] }), ringTP = [];
  if (L0 != null) { let k = 0; for (let j = 0; j < NRING; j++) { const f = (j + 1) / NRING; while (k < 2000 && sLapse(L0 + (LZ - L0) * k / 2000) < f) k++; ringTP.push(k >= 2000 ? 1e9 : L0 + (LZ - L0) * k / 2000); } }
  const NLF = 1400, lfS = L0 == null ? null : streaks(S, NLF, { minPx: 1.4, near: [200, 900] }), lfB = [];
  if (L0 != null) { const r = rng(71); for (let i = 0; i < NLF; i++) { const f = -.06 + 1.12 * r(), rad = 420 + 6500 * Math.pow(r(), .9), a = r() * 6.283, tp = r(), br = .4 + .8 * Math.pow(r(), 2);
      lfB.push({ P: PD.clone().multiplyScalar(f * GAP).addScaledVector(PB1, Math.cos(a) * rad).addScaledVector(PB2, Math.sin(a) * rad), c: (tp < .3 ? [.75, .82, 1] : tp < .8 ? [1, .95, .88] : [1, .78, .55]).map(x => x * br) }); } }
  // scale rings (zoom cue): 4.2 ly around the Sun (shrinks to a speck), then 100,000 ly across the disc (drawn on the galaxy cue)
  const SRS = 128, srS = Z0 == null ? null : streaks(S, SRS * 2, { minPx: 1.5, near: [0, 1e-4] });

  // ---------------- lens flare: ghosts on the line from the Sun through the frame centre, projected in the shader (so the camera
  // director's later move keeps it on the Sun); fades as the Sun leaves the frame or hides behind a planet ----------------
  const FLE = [[0, .5, 1, .45, .3, .16, 0], [0, .14, 1, 1, .88, .72, 0], [0, .02, 34, .85, .66, .46, 0], [0, .01, 70, .35, .5, 1, 0],
    [.3, .05, 1, .22, .4, .85, 0], [.48, .1, 1, .5, .42, .7, 1], [.6, .028, 1, .85, .55, .28, 0], [.78, .16, 1, .4, .6, .55, 1], [1.02, .07, 1, .75, .42, .18, 0], [1.25, .24, 1, .4, .45, .7, 1], [1.4, .04, 1, .55, .75, 1, 0]];
  const flU = { uSun: { value: SUN }, uAsp: { value: ctx.W / ctx.H }, uI: { value: 0 } };
  const FLB = p.flare != null ? +p.flare : FI != null ? .3 : 0;
  if (FI != null || FLB > 0) { const n = FLE.length, g = new T.BufferGeometry(), cr = [], e = [], c = [], ix = [];
    FLE.forEach((q, i) => { [[-1, -1], [1, -1], [-1, 1], [1, 1]].forEach(k => { cr.push(k[0], k[1]); e.push(q[0], q[1], q[2], q[6]); c.push(q[3], q[4], q[5]); }); const b = i * 4; ix.push(b, b + 1, b + 2, b + 2, b + 1, b + 3); });
    g.setAttribute('position', new T.BufferAttribute(new Float32Array(n * 12), 3)); g.setAttribute('corner', new T.Float32BufferAttribute(cr, 2)); g.setAttribute('aE', new T.Float32BufferAttribute(e, 4)); g.setAttribute('aC', new T.Float32BufferAttribute(c, 3)); g.setIndex(ix);
    const fl = new T.Mesh(g, new T.ShaderMaterial({ uniforms: flU, transparent: true, depthTest: false, depthWrite: false, blending: T.AdditiveBlending,
      vertexShader: `attribute vec2 corner; attribute vec4 aE; attribute vec3 aC; uniform vec3 uSun; uniform float uAsp, uI; varying vec2 vUv; varying vec3 vC; varying float vT;
        void main(){ vec4 s = projectionMatrix * viewMatrix * vec4(uSun, 1.); vUv = corner; vT = aE.w;
          if (s.w <= 0. || uI <= 0.) { vC = vec3(0.); gl_Position = vec4(0., 0., 2., 1.); return; }
          vec2 n = s.xy / s.w; float e = max(abs(n.x), abs(n.y));
          vC = aC * uI * (1. - smoothstep(.85, 1.35, e)) * (aE.x > 0. ? .5 + .5 * (1. - smoothstep(0., 1.2, length(n))) : 1.);
          gl_Position = vec4(n * (1. - 2. * aE.x) + corner * vec2(aE.y * aE.z / uAsp, aE.y), 0., 1.); }`,
      fragmentShader: `varying vec2 vUv; varying vec3 vC; varying float vT;
        void main(){ float r = length(vUv), a = vT < .5 ? exp(-r * r * 5.) * (1. - smoothstep(.8, 1., r)) : exp(-pow((r - .8) / .06, 2.)) * .1 + exp(-r * r * 3.) * .03;
          gl_FragColor = vec4(vC * a, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` }));
    fl.frustumCulled = false; fl.renderOrder = 50; S.add(fl); }

  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .1, 1e5); ctx.side(cam, p.side == null ? .14 : p.side);
  const tmp = new T.Vector3();
  // camera state = target + direction * distance; each cue blends toward a new state (distance in log space; the target follows
  // in proportion to the distance, so the old subject stays in frame while the camera backs away)
  function blend(a, b, w) { if (w <= 0) return a; if (w >= 1) return b;
    const d = Math.exp(Math.log(a.d) + (Math.log(b.d) - Math.log(a.d)) * w), k = Math.abs(b.d - a.d) > 1e-6 ? (d - a.d) / (b.d - a.d) : w;
    return { t: a.t.clone().lerp(b.t, k), dir: a.dir.clone().lerp(b.dir, w).normalize(), d, fov: a.fov + (b.fov - a.fov) * w }; }
  const MID = PD.clone().multiplyScalar(GAP * .4), NV = V.clone().negate().addScaledVector(PD, V.dot(PD)).normalize().addScaledVector(PD, -.3).normalize();
  const GDIR = NG.clone().multiplyScalar(Math.cos(.95)).addScaledVector(GA, Math.sin(.95)).normalize();
  const EDT = GC.clone().addScaledVector(GA, -1.6 * RG).addScaledVector(NG, -.1 * RG), EDD = GA.clone().addScaledVector(NG, .45).normalize();
  const atT = (c, d, tt) => c == null ? 0 : sm(cue(c), cue(c) + d, tt);
  const G1 = has('galaxy') ? cu('galaxy') + .9 : ctx.t1;
  // galaxy weight: the old 9 s ease from the galaxy cue, or (zoom cue) an accelerating log zoom from `zoom` that lands on the galaxy cue
  const wGal = tt => Z0 == null ? atT(p.galaxy, 9, tt) : Math.pow(sm(0, 1, c01((tt - Z0) / Math.max(1, G1 - Z0))), 1.5);
  function camState(tt) { const uu = tt - ctx.t0, oa = .22 * Math.sin(uu * .045) - .12 + uu * .006, ob = .06 * Math.sin(uu * .06);
    const cd = V.clone().negate().applyAxisAngle(UP, oa).applyAxisAngle(RT, ob).normalize();
    if (TOUR) { const lk = lookAt2(tt); cd.applyAxisAngle(UP, tourTheta(tt) + SG * lk[0]); if (lk[1] > 0) cd.applyAxisAngle(lkA.crossVectors(cd, UP).normalize(), lk[1]); }
    let q = { t: UP.clone().multiplyScalar(-.7), dir: cd, d: 15 - 1.2 * sm(0, 30, uu), fov: 40 };
    if (FI != null) { const x = c01((tt - ctx.t0) / (FI - ctx.t0)), e = 1 - Math.pow(1 - x, 2.4);
      q.d = Math.exp(Math.log(700) + (Math.log(q.d) - Math.log(700)) * e); q.dir = FIDIR.clone().lerp(cd, sm(.1, 1, x)).normalize(); q.fov = 40 + 10 * (1 - sm(0, 1, x)); }
    q = blend(q, { t: v3(0, 0, 0), dir: FDIR, d: 1500, fov: 38 }, atT(p.far, 6.5, tt));
    if (has('oort')) q = blend(q, { t: SUN.clone().multiplyScalar(.55), dir: FDIR.clone().applyAxisAngle(UP, -.03 * Math.max(0, tt - cu('oort'))), d: 90000, fov: 38 }, atT(p.oort, 6, tt));
    q = blend(q, { t: MID, dir: NV, d: 66000, fov: 38 }, atT(p.proxima, 6.5, tt));
    if (L0 != null) q = blend(q, { t: PROX.clone().multiplyScalar(sLapse(tt)), dir: NT, d: 2600, fov: 42 }, atT(p.lapse, 2.8, tt));
    q = blend(q, { t: GC.clone().lerp(v3(0, 0, 0), .25), dir: GDIR, d: 3.3 * RG, fov: 38 }, wGal(tt));
    if (has('edge')) q = blend(q, { t: EDT, dir: EDD, d: 1.6 * RG, fov: 40 }, atT(p.edge, 4.6, tt));
    return q; }
  const camPos = (tt, out) => { const q = camState(tt); return out.copy(q.t).addScaledVector(q.dir, q.d); };
  const cA = v3(0, 0, 0), cB = v3(0, 0, 0), dv = v3(0, 0, 0), ax1 = v3(0, 0, 0), ax2 = v3(0, 0, 0), vel = v3(0, 0, 0), plc = v3(0, 0, 0), sdir = v3(0, 0, 0);
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const wF = at(p.far, 6.5), wP = at(p.proxima, 6.5), wG = wGal(t), wO = has('oort') ? at(p.oort, 6) : 0, wE = has('edge') ? at(p.edge, 4.6) : 0;
    const gl = p.launch == null ? 0 : Math.max(0, Math.sin(Math.PI * Math.min(1, Math.max(0, (t - cue(p.launch)) / 1.6))));
    const st = camState(t);
    cam.position.copy(st.t).addScaledVector(st.dir, st.d); cam.lookAt(st.t);
    const D = Math.max(1, cam.position.length());
    cam.near = Math.max(.05, D * .004); cam.far = Math.max(2000, st.d * 6 + 5e4); cam.fov = vf(st.fov); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    SKYG.position.copy(cam.position); SKYG.scale.setScalar(cam.near * 40);
    // rim light direction in view space
    RIMU.value.copy(SD).transformDirection(cam.matrixWorldInverse);
    fillL.position.copy(cam.position).add(v3(0, 6, 0)).normalize().multiplyScalar(30);
    // probe: real meshes while big enough on screen, a glint once it is only a few pixels
    const px = 4 * ctx.H / (2 * Math.tan(cam.fov * Math.PI / 360) * D), meshOn = px > (FI != null ? 5 : 10);
    const nearK = FI != null ? sm(75, 45, D) : 1;
    PROBE.visible = meshOn; dust.points.visible = D < 60 || (FI != null && D < 75);
    if (FI != null) dust.points.material.opacity = .45 * nearK;
    const gk = sm(30, 12, px) * (1 - .85 * wG);
    const creep = L0 == null ? 0 : .0035 * sm(L0, LZ, t);
    glint.material.opacity = gk; glint.scale.setScalar(Math.max(1, cam.position.distanceTo(tmp.copy(PROX).multiplyScalar(creep))) * .011 * (1 + .3 * wP)); glint.position.copy(PROX).multiplyScalar(creep);
    rtgGlow.forEach((s, i) => s.material.opacity = .12 + .03 * Math.sin(t * .7 + i));
    dishGlint.material.opacity = .7 * gl; dishGlint.scale.setScalar(1 + 2 * gl);
    // sun: constant angular size (small and very bright), turns into a star point, then a gold marker in the galaxy view
    const sd = cam.position.distanceTo(SUN), gsun = 1 - wG;
    sunCore.scale.setScalar(sd * .012 * (1 - .45 * wF) * gsun); sunHalo.scale.setScalar(sd * .1 * (1 - .55 * wF) * gsun); sunWide.scale.setScalar(sd * (.32 + .9 * (1 - wF)) * (1 - .6 * wF) * gsun);
    sunHalo.material.opacity = .55 * gsun; sunWide.material.opacity = .16 * (1 - .5 * wP) * gsun;
    sunMark.position.copy(SUN).multiplyScalar(.5); sunMark.material.opacity = wG; sunMark.scale.setScalar(cam.position.distanceTo(SUN) * .014); sunMarkH.position.copy(sunMark.position); sunMarkH.material.opacity = .35 * wG; sunMarkH.scale.setScalar(cam.position.distanceTo(SUN) * .05);
    skyU.uH.value = (1 - .7 * wF) * (1 - wP);
    // Proxima: an ordinary faint star until the camera turns toward it (and swells as the time-lapse arrives)
    const pdist = cam.position.distanceTo(PROX), pk = (.45 + .55 * wP) * (1 - wG), sL = sLapse(t), arr = L0 == null ? 0 : sm(.75, .97, sL) * (1 - wG);
    proxS.scale.setScalar(pdist * .0065 * (1 + .4 * wP + 1.5 * arr)); proxH.scale.setScalar(pdist * .03 * (1 + 1.2 * arr)); proxS.material.opacity = .9 * pk; proxH.material.opacity = .28 * pk * (.3 + .7 * wP) * (1 + 1.5 * arr);
    // dotted path: the travelled part (gold) barely leaves the probe; ghost dots mark the rest; gone in the galaxy view
    // (lapse cue: the line draws itself out to Proxima after the proxima cue, brighter)
    const pv = wP * (1 - sm(.0, .35, wG)), done = L0 == null ? .012 + .02 * sm(cue(p.proxima, 1e9) + 2, cue(p.proxima, 1e9) + 40, t) : .004 + creep;
    const rev = L0 == null ? 1 : sm(cue(p.proxima, 1e9) + .8, cue(p.proxima, 1e9) + 5.2, t), pb = L0 == null ? .05 : .16; path.material.size = L0 == null ? 3.4 : 4.4;
    for (let i = 0; i < NPATH; i++) { const f = (i + .5) / NPATH, vis = pv * sm(rev + .02, rev - .01, f) * (1 + 3 * Math.exp(-Math.pow((f - rev) / .015, 2)) * (rev < 1 ? 1 : 0)); tmp.copy(PROX).multiplyScalar(f); pa.set([tmp.x, tmp.y, tmp.z], i * 3); pc[i * 3] = pb * vis; pc[i * 3 + 1] = pb * .9 * vis; pc[i * 3 + 2] = pb * vis; }
    const NG2 = 18; for (let j = 0; j < NG2; j++) { const f = done * (j + .5) / NG2, i = j; tmp.copy(PROX).multiplyScalar(f); pa.set([tmp.x, tmp.y, tmp.z], i * 3); const v = pv * (1.5 - .7 * j / NG2); pc[i * 3] = v; pc[i * 3 + 1] = v * .7; pc[i * 3 + 2] = v * .26; }
    pg.attributes.position.needsUpdate = true; pg.attributes.color.needsUpdate = true; path.visible = pv > .001;
    // galaxy disc fades in only once the camera is far enough for its points to be small
    const gv = sm(Math.log(RG * .15), Math.log(RG * 1.1), Math.log(st.d));
    galS.material.opacity = .75 * gv; galG.material.opacity = .2 * gv; galS.visible = galG.visible = gv > .001;
    galCore.material.opacity = .5 * gv; galCore.scale.setScalar(RG * .55);
    stars.forEach(s => s.material.opacity = 1 - .85 * gv); skyU.uK.value = 1 - gv;
    if (dust.points.visible) dust.update(t, [0, 0, 0]);
    // fly-in / pull-back streaks (their tails are the camera's own motion over the last 0.07 s)
    const fe = FI == null ? 0 : sm(0, .06, (t - ctx.t0) / (FI - ctx.t0)) * (1 - sm(.7, 1, (t - ctx.t0) / (FI - ctx.t0)));
    const pe = p.far == null ? 0 : sm(0, .12, wF) * (1 - (has('oort') ? sm(.8, 1, wO) : sm(.8, 1, wF))) * (1 - wP);
    const le = L0 == null ? 0 : sm(L0 + 1.5, L0 + 3, t) * (1 - sm(LZ - .3, LZ + 1.2, t));
    if (fe > 0 || pe > 0 || le > 0) { camPos(t, cA); camPos(t - .07, cB); dv.copy(cA).sub(cB); }
    if (fiStream) fiStream.run(fe, cA, dv);
    pbStream.run(pe, cA, dv);
    // close-up motes: slow drift through a box around the probe, faded at the box faces so wrapping never pops
    const me = (1 - sm(.02, .25, wF)) * nearK; motes.mesh.visible = me > 0 && D < 75;
    if (motes.mesh.visible) { for (let i = 0; i < NMO; i++) { const m = moB[i], c = [0, 0, 0];
        for (let j = 0; j < 3; j++) { const vj = [.32, .05, -.14][j] * m[3], x = (((m[j] + vj * t) % MBX[j]) + MBX[j]) % MBX[j]; c[j] = x - MBX[j] / 2; m[5 + j] = sm(0, 3, x) * sm(MBX[j], MBX[j] - 3, x); }
        const k = me * .5 * m[3] * m[5] * m[6] * m[7] * (.7 + .3 * Math.sin(t * .5 + m[4] * 9));
        motes.set(i, c[0], c[1], c[2], c[0] - .25 * m[3], c[1] - .04, c[2] + .1, .05, k, k * .88, k * .7); }
      motes.commit(); }
    // Grand Tour: planets on their bent relative paths, speed streaks along the current heading
    let occ = 1; sdir.copy(SUN).sub(cam.position); const sdl = sdir.length(); sdir.divideScalar(sdl);
    for (const o of PL) { const f = sm(o.tc - o.f0, o.tc - o.f0 + 1.3, t) * (1 - sm(o.tc + 3.5, o.tc + 5, t)); o.G.visible = f > 0; if (!o.G.visible) continue;
      planetPos(o, t, o.G.position); o.m.uniforms.uF.value = f; o.ball.rotation.y = t * .1 + o.spin;
      if (o.ring) { o.ring.material.uniforms.uF.value = f; o.ring.material.uniforms.uC.value.copy(o.G.position); }
      plc.copy(o.G.position).sub(cam.position); const tq = plc.dot(sdir); if (tq > 0 && tq < sdl) occ *= sm(o.R * .97, o.R * 1.08, plc.addScaledVector(sdir, -tq).length()); }
    if (tsS) { const te = (.55 * sm(TR.i0, TR.i1 - .5, t) + .45 * sm(TJ - 2.6, TJ - 1, t)) * (1 - sm(TEND - 2, TEND + .3, t)); tsS.mesh.visible = te > 0;
      if (te > 0) { velDir(t, vel); ax1.copy(UP); ax2.crossVectors(vel, UP).normalize(); const F = tsF(t), len = tsR(t) * 140 * .085;
        for (let i = 0; i < NTS; i++) { const b = tsB[i], s = ((F + b.f) % 1 + 1) % 1, al = 70 * (1 - 2 * s), ca = Math.cos(b.a) * b.rad, sa = Math.sin(b.a) * b.rad;
          const hx = vel.x * al + ax1.x * ca + ax2.x * sa, hy = vel.y * al + ax1.y * ca + ax2.y * sa, hz = vel.z * al + ax1.z * ca + ax2.z * sa, k0 = te * b.br * sm(0, .1, s) * sm(1, .9, s);
          const ex = cam.position.x - hx, ey = cam.position.y - hy, ez = cam.position.z - hz, tq = Math.min(len, Math.max(0, ex * vel.x + ey * vel.y + ez * vel.z));
          const k = k0 * sm(4, 11, Math.hypot(ex - vel.x * tq, ey - vel.y * tq, ez - vel.z * tq));
          tsS.set(i, hx, hy, hz, hx + vel.x * len, hy + vel.y * len, hz + vel.z * len, .05, b.c[0] * k, b.c[1] * k, b.c[2] * k); }
        tsS.commit(); } }
    // lens flare: strong during the fly-in, `flare` strength afterwards, gone once the Sun is only a star
    if (FI != null || FLB > 0) flU.uI.value = (FI != null ? 1.2 - (1.2 - FLB) * sm(FI - 1, FI + 2, t) : FLB) * (1 - wP) * (1 - .5 * wF) * (1 - wO) * occ;
    // Oort shell: fades in with the oort pull-back, stays faint over the journey, gone in the zoom-out
    if (oortP) { const o = wO * (1 - .55 * sm(0, 1, wP)) * (1 - sm(0, .15, wG)); oortP.P.visible = o > 0; oortP.U.uO.value = .9 * o; }
    // millennium rings: faint until the camera passes, then a pulse (rise .25 s, decay ~.9 s)
    if (ringS) { const rb = pv * sm(cue(p.proxima, 1e9) + 3, cue(p.proxima, 1e9) + 6, t) * (1 - sm(0, .3, wG)); ringS.mesh.visible = rb > 0;
      if (rb > 0) { for (let j = 0; j < NRING; j++) { const tp = ringTP[j], pu = sm(tp - .25, tp, t) * Math.exp(-Math.max(0, t - tp) / .9), k = rb * (.16 + 1.8 * pu), f = (j + 1) / NRING;
          const cx = PD.x * f * GAP, cy = PD.y * f * GAP, cz = PD.z * f * GAP, rr = RRAD * (1 + .25 * pu);
          for (let q = 0; q < RSEG; q++) { const a0 = (q - .35) / RSEG * 6.2832, a1 = (q + 1.35) / RSEG * 6.2832, c0 = Math.cos(a0) * rr, s0 = Math.sin(a0) * rr, c1 = Math.cos(a1) * rr, s1 = Math.sin(a1) * rr;
            ringS.set(j * RSEG + q, cx + PB1.x * c1 + PB2.x * s1, cy + PB1.y * c1 + PB2.y * s1, cz + PB1.z * c1 + PB2.z * s1, cx + PB1.x * c0 + PB2.x * s0, cy + PB1.y * c0 + PB2.y * s0, cz + PB1.z * c0 + PB2.z * s0, 6, k, k * .78, k * .42); } }
        ringS.commit(); } }
    if (lfS) { lfS.mesh.visible = le > 0;
      if (le > 0) { for (let i = 0; i < NLF; i++) { const b = lfB[i], dc = b.P.distanceTo(cA), k = le * sm(18000, 7000, dc);
          if (k <= 0) { lfS.hide(i); continue; } lfS.set(i, b.P.x, b.P.y, b.P.z, b.P.x + dv.x, b.P.y + dv.y, b.P.z + dv.z, 7, b.c[0] * k, b.c[1] * k, b.c[2] * k); }
        lfS.commit(); } }
    // zoom-out: star layers around the Sun, scale rings
    if (layers.length) { const zo = sm(Z0 - .4, Z0 + .8, t), lD = Math.log(D);
      layers.forEach(L => { const o = zo * sm(Math.log(L.Ri * .06), Math.log(L.Ri * .25), lD) * (1 - sm(Math.log(L.Ri * 5), Math.log(L.Ri * 18), lD)); L.P.visible = o > 0; L.U.uO.value = o; }); }
    if (srS) { const ka = sm(Z0 + .3, Z0 + 1.8, t) * sm(3 * GAP, 7 * GAP, D) * (1 - sm(G1 - 2.5, G1, t)) * .55, sw = has('galaxy') ? sm(cu('galaxy') - .2, cu('galaxy') + 1.8, t) : 0, kb = sw > 0 ? .45 * sm(0, .1, sw) * (1 - .6 * wE) : 0;
      srS.mesh.visible = ka > 0 || kb > 0;
      if (srS.mesh.visible) { for (let q = 0; q < SRS; q++) { const a0 = q / SRS * 6.2832, a1 = (q + 1) / SRS * 6.2832;
          srS.set(q, GA.x * Math.cos(a1) * GAP + GB.x * Math.sin(a1) * GAP, GA.y * Math.cos(a1) * GAP + GB.y * Math.sin(a1) * GAP, GA.z * Math.cos(a1) * GAP + GB.z * Math.sin(a1) * GAP,
            GA.x * Math.cos(a0) * GAP + GB.x * Math.sin(a0) * GAP, GA.y * Math.cos(a0) * GAP + GB.y * Math.sin(a0) * GAP, GA.z * Math.cos(a0) * GAP + GB.z * Math.sin(a0) * GAP, GAP * .006, ka, ka * .75, ka * .35);
          const on = sm(q / SRS - .01, q / SRS + .01, sw) * kb, R1 = RG * 1.02, b0 = -2.6;
          srS.set(SRS + q, GC.x + (GA.x * Math.cos(a1 + b0) + GB.x * Math.sin(a1 + b0)) * R1, GC.y + (GA.y * Math.cos(a1 + b0) + GB.y * Math.sin(a1 + b0)) * R1, GC.z + (GA.z * Math.cos(a1 + b0) + GB.z * Math.sin(a1 + b0)) * R1,
            GC.x + (GA.x * Math.cos(a0 + b0) + GB.x * Math.sin(a0 + b0)) * R1, GC.y + (GA.y * Math.cos(a0 + b0) + GB.y * Math.sin(a0 + b0)) * R1, GC.z + (GA.z * Math.cos(a0 + b0) + GB.z * Math.sin(a0 + b0)) * R1, RG * .004, on, on * .8, on * .45); }
        srS.commit(); } }
  } };
};
