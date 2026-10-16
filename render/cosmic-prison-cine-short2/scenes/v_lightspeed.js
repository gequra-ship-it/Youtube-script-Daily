// lightspeed — light as a pulse racing along a long glowing track through space, past a solid starship that can never catch it
// (S04-S05). Drawn in the ship's own frame: the ship holds its place on the track while the track beads, dust and stars stream back;
// every light pulse leaves the ship at the same speed however hard the engine burns (true: light always moves at c relative to you).
// Ship: lathe hull with panel texture, gold-lit section rings, habitat ring with spokes, two radiator wings (heat glow rises with
// power), engine bell with a glowing throat and a blue-white plume. Rim light comes from the light wall ahead.
// params (cues, all optional):
//   limit    — the first pulse streaks past from behind and races ahead; a faint wall of light stands ahead of the ship (the limit);
//              afterwards a pulse passes every ~7 s (calm, no strobe). Default: pulses start 2 s into the shot.
//   push     — the engine flares harder and harder; stars ahead crowd and blue-shift slightly (aberration), the track streams faster,
//              an energy glow swells around the ship toward white, but the wall stays exactly as far ahead
//   infinite — glow saturates near white, the plume is at its longest, the ship strains (slow, small tremor), still behind
//   exit     — (default: 3.5 s before the shot ends) BOOST: the engine flares white, the plume doubles, an anamorphic flare and a glow
//              burst; the track beads and dust smear into long light streaks; the ship accelerates away from the camera, shrinks
//              and vanishes into the ring / light wall ahead (soft flash there) just before the transition
// speed cues: dust and track beads are drawn as motion streaks whose length follows the flow speed (cruise < push < infinite < boost)
//   side (.1)
(window.MIYA = window.MIYA || { scenes: {} }).scenes.lightspeed = function (ctx, p) {
  const { T, sm, rng, cue, dotTex } = ctx, K = window.MIYA.kit, E = ctx.env();
  const S = new T.Scene(); S.background = new T.Color('#03040d');
  const v3 = (x, y, z) => new T.Vector3(x, y, z);
  const vf = f => { if (!ctx.VERT) return f; const h = 2 * Math.atan(Math.tan(f * Math.PI / 360) * 16 / 9 * .62); return 2 * Math.atan(Math.tan(h / 2) * ctx.H / ctx.W) * 180 / Math.PI; };
  const ACC = new T.Color(ctx.ACC);
  const tL = cue(p.limit, ctx.t0 + 2), tP = cue(p.push, 1e9), tI = cue(p.infinite, 1e9), tX = cue(p.exit, ctx.t1 - 3.5);
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
  // integral of smoothstep ramp from a over d seconds, evaluated at t (seek-safe distance travelled)
  const ism = (a, d, t) => { const x = (t - a) / d; if (x <= 0) return 0; if (x >= 1) return d * (x - .5); return d * (x * x * x - x * x * x * x / 2); };

  // ---------------- sky: nebula gradient + stars with relativistic aberration / Doppler tint ----------------
  const sky = new T.Mesh(new T.SphereGeometry(1, 40, 20), new T.ShaderMaterial({ side: T.BackSide, depthWrite: false, depthTest: false, uniforms: { uB: { value: 0 } },
    vertexShader: `varying vec3 vD; void main(){ vD = position; vec4 q = projectionMatrix * vec4(mat3(viewMatrix) * position, 1.0); gl_Position = vec4(q.xy, q.w * .99999, q.w); }`,
    fragmentShader: `varying vec3 vD; uniform float uB; void main(){ vec3 d = normalize(vD);
      vec3 c = mix(vec3(.008,.008,.024), vec3(.02,.016,.05), .5 + .5 * d.y);
      c += vec3(.05,.03,.09) * exp(-pow(d.y - .1 * d.z, 2.) / .05) * .6;
      c += vec3(.25,.4,.9) * .05 * uB * exp(-(1. - d.x) * 6.);
      c += vec3(1.,.75,.4) * .035 * exp(-(1. - d.x) * 14.);
      gl_FragColor = vec4(c, 1.);
      #include <tonemapping_fragment>
      #include <colorspace_fragment>
    }` }));
  sky.frustumCulled = false; sky.renderOrder = -10; S.add(sky);
  const NS = 3600, sg = new T.BufferGeometry(), sp = new Float32Array(NS * 3), sc = new Float32Array(NS * 3), ss = new Float32Array(NS);
  { const r = rng(7); for (let i = 0; i < NS; i++) { const u = r() * 2 - 1, th = r() * 6.283, q = Math.sqrt(1 - u * u); sp.set([q * Math.cos(th), u, q * Math.sin(th)], i * 3);
    const tp = r(), br = .3 + .9 * Math.pow(r(), 2.4), col = tp < .25 ? [.75, .82, 1] : tp < .8 ? [1, .96, .9] : [1, .82, .62]; sc.set(col.map(x => x * br), i * 3); ss[i] = 2.2 + (r() < .08 ? 1.8 : 0); } }
  sg.setAttribute('position', new T.BufferAttribute(sp, 3)); sg.setAttribute('col', new T.BufferAttribute(sc, 3)); sg.setAttribute('sz', new T.BufferAttribute(ss, 1));
  const starU = { uB: { value: 0 } };
  const stars = new T.Points(sg, new T.ShaderMaterial({ uniforms: starU, transparent: true, depthWrite: false, depthTest: false, blending: T.AdditiveBlending,
    vertexShader: `attribute vec3 col; attribute float sz; uniform float uB; varying vec3 vC;
      void main(){ vec3 d = normalize(position); float c = d.x, cp = (c + uB) / (1. + uB * c), s = sqrt(max(0., 1. - cp * cp));
        vec2 yz = d.yz / max(1e-5, length(d.yz)) * s; vec3 dp = vec3(cp, yz);
        float g = 1. / sqrt(1. - uB * uB), D = 1. / (g * (1. - uB * cp));
        vec3 sh = D > 1. ? vec3(.72, .88, 1.35) : vec3(1.25, .82, .62); vC = col * mix(vec3(1.), sh, clamp(abs(D - 1.) * .5, 0., 1.)) * clamp(pow(D, .9), .35, 2.2);
        vec4 q = projectionMatrix * vec4(mat3(viewMatrix) * dp, 1.); gl_Position = vec4(q.xy, q.w * .99999, q.w); gl_PointSize = sz * clamp(sqrt(D), .85, 1.5); }`,
    fragmentShader: `varying vec3 vC; void main(){ float r = length(gl_PointCoord - .5) * 2.; float a = smoothstep(1., 0., r); a *= a; gl_FragColor = vec4(vC * a, 1.);
      #include <tonemapping_fragment>
      #include <colorspace_fragment>
    }` }));
  stars.frustumCulled = false; stars.renderOrder = -9; S.add(stars);

  // ---------------- the track, its beads, the light wall ----------------
  const TY = -3.4, WX = 58;                          // track height under the ship, wall distance ahead
  const stripT = ctx.ctex(64, (g, s) => { const gr = g.createLinearGradient(0, 0, 0, s); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.5, 'rgba(255,255,255,1)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); });
  const addM = (g, m, par) => { const o = new T.Mesh(g, m); (par || S).add(o); return o; };
  const glowM = (col, op, map) => new T.MeshBasicMaterial({ color: col, map: map || stripT, transparent: true, opacity: op, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide, fog: false });
  const TRACK = new T.Group(); S.add(TRACK); TRACK.position.y = TY;
  const trM1 = glowM(new T.Color('#ffd590').multiplyScalar(1.1), .8), trM2 = glowM(new T.Color('#8a7cff'), .18);
  [0, Math.PI / 2].forEach(r => { addM(new T.PlaneGeometry(WX + 600, .22).translate((WX - 600) / 2, 0, 0).rotateX(r), trM1, TRACK); addM(new T.PlaneGeometry(WX + 600, 2.6).translate((WX - 600) / 2, 0, 0).rotateX(r), trM2, TRACK); });
  const NB = 70, BSP = 9, bg = new T.BufferGeometry(), ba = new Float32Array(NB * 3), bc = new Float32Array(NB * 3);
  bg.setAttribute('position', new T.BufferAttribute(ba, 3)); bg.setAttribute('color', new T.BufferAttribute(bc, 3));
  const beads = new T.Points(bg, new T.PointsMaterial({ size: .9, map: dotTex(), vertexColors: true, transparent: true, blending: T.AdditiveBlending, depthWrite: false }));
  beads.frustumCulled = false; TRACK.add(beads);
  const wallT = ctx.ctex(256, (g, s) => { const gr = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.25, 'rgba(255,255,255,.45)'); gr.addColorStop(.7, 'rgba(255,255,255,.12)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); });
  const wallM = glowM(new T.Color('#ffe2b0'), 0, wallT), wall = addM(new T.PlaneGeometry(60, 60).rotateY(Math.PI / 2), wallM); wall.position.set(WX, TY + 4, 0);
  const wallM2 = glowM(new T.Color('#9d8cff'), 0, wallT), wall2 = addM(new T.PlaneGeometry(130, 130).rotateY(Math.PI / 2), wallM2); wall2.position.set(WX + 4, TY + 4, 0);
  const wallRingM = glowM(ACC.clone().multiplyScalar(1.3), 0, null); wallRingM.map = null;
  const wallRing = addM(new T.TorusGeometry(11, .05, 8, 120).rotateY(Math.PI / 2), wallRingM); wallRing.position.set(WX, TY, 0);

  // ---------------- light pulses: a bright head + a long tail on crossed strips ----------------
  const tailT = ctx.ctex(256, (g, s) => { const gr = g.createLinearGradient(0, 0, s, 0); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.85, 'rgba(255,255,255,.5)'); gr.addColorStop(1, 'rgba(255,255,255,1)'); g.fillStyle = gr; g.fillRect(0, 0, s, s);
    const v = g.createLinearGradient(0, 0, 0, s); v.addColorStop(0, 'rgba(0,0,0,1)'); v.addColorStop(.5, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,1)'); g.globalCompositeOperation = 'destination-out'; g.fillStyle = v; g.fillRect(0, 0, s, s); });
  const CREL = 210, PER = 7, NPU = 3, pulses = [];
  for (let k = 0; k < NPU; k++) { const G = new T.Group(); TRACK.add(G); const m = glowM(new T.Color(2.2, 2.0, 1.6), 1, tailT);
    [0, Math.PI / 2].forEach(r => addM(new T.PlaneGeometry(46, 1.3).translate(-23, 0, 0).rotateX(r), m, G));
    const h1 = ctx.glow(G, new T.Color(3, 2.8, 2.4), 2.2, 1), h2 = ctx.glow(G, new T.Color('#ffc874'), 9, .45); pulses.push({ G, m, h1, h2 }); }

  // ---------------- the starship ----------------
  const SHIP = new T.Group(), HULL = new T.Group(); S.add(SHIP); SHIP.add(HULL);
  const RIMU = { value: new T.Vector3(1, 0, 0) };
  function rim(m, k) { m.onBeforeCompile = sh => { sh.uniforms.uL = RIMU; sh.uniforms.uRim = { value: new T.Color('#ffd49a').multiplyScalar(k) };
    sh.fragmentShader = 'uniform vec3 uL; uniform vec3 uRim;\n' + sh.fragmentShader.replace('#include <emissivemap_fragment>',
      '#include <emissivemap_fragment>\n{ float fr = 1.0 - abs(dot(normal, normalize(vViewPosition))); totalEmissiveRadiance += uRim * pow(fr, 2.5) * smoothstep(-0.1, 0.8, dot(normal, uL)); }'); };
    m.customProgramCacheKey = () => 'lsrim'; return m; }
  const panT = ctx.ctex(512, (g, s) => { g.fillStyle = '#b9bfcc'; g.fillRect(0, 0, s, s); const r = rng(5);
    for (let i = 0; i < 26; i++) { g.fillStyle = r() < .5 ? 'rgba(70,76,92,.18)' : 'rgba(255,255,255,.12)'; g.fillRect(Math.floor(r() * 8) * 64, Math.floor(r() * 8) * 64, 64 * (1 + Math.floor(r() * 2)), 64); }
    g.fillStyle = 'rgba(40,44,58,.7)'; for (let x = 0; x < s; x += 64) g.fillRect(x, 0, 3, s); for (let y = 0; y < s; y += 128) g.fillRect(0, y, s, 3); });
  panT.wrapS = panT.wrapT = T.RepeatWrapping; panT.repeat.set(4, 2); panT.anisotropy = 8;
  const hullM = rim(new T.MeshStandardMaterial({ map: panT, color: '#9da3b2', metalness: .8, roughness: .36, envMap: E, envMapIntensity: .32 }), 1.4);
  const darkM = rim(new T.MeshStandardMaterial({ color: '#2b2e3a', metalness: .7, roughness: .4, envMap: E, envMapIntensity: .35 }), 1.0);
  const nozM = rim(new T.MeshStandardMaterial({ color: '#5a5862', metalness: .9, roughness: .3, envMap: E, envMapIntensity: .5, side: T.DoubleSide }), 1.0);
  const radM = rim(new T.MeshStandardMaterial({ color: '#3a3d4a', metalness: .65, roughness: .4, emissive: '#ff5a22', emissiveIntensity: 0, envMap: E, envMapIntensity: .3 }), .9);
  const goldM = new T.MeshBasicMaterial({ color: ACC.clone().multiplyScalar(1.4) });
  const prof = [[0, -9], [1.2, -9], [2.0, -8.6], [2.05, -8.3], [2.05, -5.1], [1.95, -4.9], [1.7, -4.8], [1.6, -1.1], [1.78, -.9], [1.78, .9], [1.55, 1.1], [1.45, 4.6], [1.2, 6.6], [.75, 8.1], [.25, 8.95], [0, 9.1]].map(([r, y]) => new T.Vector2(r, y));
  const hullG = new T.LatheGeometry(prof, 64).rotateZ(-Math.PI / 2); addM(hullG, hullM, HULL);
  [[-4.85, 1.98], [-.95, 1.8], [.95, 1.8], [-8.5, 2.06]].forEach(([x, r]) => addM(new T.TorusGeometry(r, .035, 6, 72).rotateY(Math.PI / 2).translate(x, 0, 0), goldM, HULL));
  addM(new T.TorusGeometry(3.5, .36, 14, 80).rotateY(Math.PI / 2), hullM, HULL);
  addM(new T.TorusGeometry(3.5, .06, 6, 96).rotateY(Math.PI / 2).translate(.37, 0, 0), goldM, HULL);
  for (let k = 0; k < 4; k++) { const a = k / 4 * 6.283 + .785, o = addM(new T.CylinderGeometry(.13, .13, 1.75, 10), darkM, HULL); o.position.set(0, 2.6 * Math.cos(a), 2.6 * Math.sin(a)); o.rotation.x = a; }
  // radiator wings (real thickness) with gold edge lines
  [-1, 1].forEach(sd => { const W = new T.Group(); HULL.add(W); W.position.set(-6.7, 0, sd * 2.0); W.rotation.x = sd * .25;
    addM(new T.BoxGeometry(4.6, .1, 3.6).translate(0, 0, sd * 1.8), radM, W);
    for (let k = 0; k < 5; k++) addM(new T.BoxGeometry(4.6, .16, .07).translate(0, 0, sd * (.35 + k * .75)), darkM, W);
    addM(new T.BoxGeometry(4.7, .05, .05).translate(0, .07, sd * 3.6), goldM, W); });
  // engine bell (open, thin wall) with a glowing throat
  const bell = [[.75, -9], [.9, -9.6], [1.25, -10.6], [1.75, -11.6], [1.95, -11.9]].map(([r, y]) => new T.Vector2(r, y));
  addM(new T.LatheGeometry(bell, 48).rotateZ(-Math.PI / 2), nozM, HULL);
  const throatM = new T.MeshBasicMaterial({ color: new T.Color(1.2, 1.5, 2.2), side: T.DoubleSide });
  addM(new T.CircleGeometry(.9, 32).rotateY(-Math.PI / 2).translate(-9.55, 0, 0), throatM, HULL);
  // antenna mast and nav lights
  addM(new T.CylinderGeometry(.05, .05, 1.6, 8).translate(0, 2.2, 0), darkM, HULL).position.x = 3.2;
  const navG = ctx.glow(HULL, '#ffc65a', .8, .8); navG.position.set(3.2, 3.05, 0);
  // plume: nested additive cones (length and brightness follow engine power)
  const plT = ctx.ctex(128, (g, s) => { const gr = g.createLinearGradient(0, 0, 0, s); gr.addColorStop(1, 'rgba(255,255,255,1)'); gr.addColorStop(.75, 'rgba(190,215,255,.75)'); gr.addColorStop(0, 'rgba(120,140,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); });
  const plM = o => new T.MeshBasicMaterial({ map: plT, color: '#a9c0ff', transparent: true, opacity: o, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide, fog: false });
  const pl1 = addM(new T.ConeGeometry(.75, 1, 32, 1, true).translate(0, .5, 0).rotateZ(Math.PI / 2), plM(.8), HULL), pl2 = addM(new T.ConeGeometry(1.3, 1, 32, 1, true).translate(0, .5, 0).rotateZ(Math.PI / 2), plM(.35), HULL);
  pl1.position.x = pl2.position.x = -11.7;
  // after rotateZ the cone runs from the nozzle (x=0) to its tip at x=-1: scale.x is the plume length
  const engG1 = ctx.glow(HULL, new T.Color(1.6, 1.9, 2.6), 5, .7), engG2 = ctx.glow(HULL, '#6f8cff', 16, .25); engG1.position.x = engG2.position.x = -12;
  // energy bubble around the ship
  const bub1 = ctx.glow(SHIP, '#9fb4ff', 30, 0), bub2 = ctx.glow(SHIP, '#ffffff', 16, 0); bub1.position.x = bub2.position.x = 1;
  const bow = ctx.glow(SHIP, '#cfe0ff', 6, 0); bow.position.x = 10;

  // ---------------- dust streaming back (seek-safe), lights ----------------
  const ND = 900, dg = new T.BufferGeometry(), da = new Float32Array(ND * 3), dB = [];
  dg.setAttribute('position', new T.BufferAttribute(da, 3)); { const r = rng(11); for (let i = 0; i < ND; i++) dB.push([r() * 160, (r() - .5) * 40, (r() - .5) * 60]); }
  const dust = streaks(S, ND, { minPx: 1.4, near: [3, 12] }), bstr = streaks(TRACK, NB, { minPx: 2 });
  // boost: white-blue flare at the nozzle, a horizontal anamorphic streak, a gold flash where the ship meets the light wall
  const bF1 = ctx.glow(HULL, new T.Color(2.2, 2.4, 3), 8, 0), bF2 = ctx.glow(HULL, '#7f9cff', 30, 0), bAna = ctx.glow(HULL, '#bcd0ff', 1, 0);
  bF1.position.x = bF2.position.x = bAna.position.x = -12.2;
  const wFl = ctx.glow(S, new T.Color(2.4, 2.1, 1.6), 30, 0), wFl2 = ctx.glow(S, '#ffc65a', 90, 0); wFl.position.set(WX - 1, 0, 0); wFl2.position.set(WX, 0, 0);
  const key = new T.DirectionalLight('#ffe2b8', 2.2); key.position.set(60, 18, -10); S.add(key);
  const fill = new T.DirectionalLight('#9aa6c4', .55); fill.position.set(-20, 10, 30); S.add(fill);
  S.add(new T.HemisphereLight('#39407a', '#07070f', .5));
  const engL = new T.PointLight('#8fb0ff', 0, 60, 1.5); engL.position.set(-14, 0, 0); S.add(engL);

  const cam = new T.PerspectiveCamera(36, ctx.W / ctx.H, .1, 3000); ctx.side(cam, p.side == null ? .1 : p.side);
  return { scene: S, camera: cam, draw(t, u) {
    // engine power: cruise 0, rises on "push" (each step costs more: slow approach), saturates on "infinite"
    const ePush = sm(tP, tP + 16, t), eInf = sm(tI, tI + 6, t), e = .7 * ePush + .3 * eInf;
    const beta = .25 + .3 * ePush + .1 * eInf;                       // aberration strength (symbolic, subtle)
    starU.uB.value = beta; sky.material.uniforms.uB.value = beta;
    // track flow: distance travelled = integral of the visual speed (seek-safe)
    // exit / boost: b = burn (rises over .45 s), X = the ship's run ahead (accelerating), kv = ship still visible (shrinks into the ring)
    const xb = t - tX, b = sm(0, .45, xb), sx = Math.max(0, (xb - .35) / 2.65), X = 100 * Math.pow(sx, 2.5), kv = 1 - sm(55, 95, X);
    const vel = 14 + 22 * sm(tP, tP + 16, t) + 10 * sm(tI, tI + 6, t) + 70 * sm(tX + .2, tX + 2.4, t);
    const dist = 14 * (t - ctx.t0) + 22 * ism(tP, 16, t) + 10 * ism(tI, 6, t) + 70 * ism(tX + .2, 2.2, t);
    // streak length = distance flowed in the last ~0.1 s (beads) / 0.06 s (dust): grows with speed, always longer than the bead gap at speed
    const bL = Math.min(40, vel * (.06 + .05 * b)), dL = Math.min(14, vel * 1.15 * (.05 + .03 * b)), sb = sm(16, 60, vel);
    for (let i = 0; i < NB; i++) { const x = WX - (((i * BSP + dist) % (NB * BSP)) + NB * BSP) % (NB * BSP); ba.set([x, 0, 0], i * 3);
      const v = (.55 + .25 * ePush) * sm(WX, WX - 30, x) * sm(-500, -380, x); bc.set([v * (1 - .5 * sb), v * .8 * (1 - .5 * sb), v * .5 * (1 - .5 * sb)], i * 3);
      const sv = v * (.35 + .5 * sm(14, 40, vel) + .6 * b); bstr.set(i, x, 0, 0, Math.min(WX, x + bL), 0, 0, .22, sv, sv * .82, sv * .55); }
    bg.attributes.position.needsUpdate = true; bg.attributes.color.needsUpdate = true; bstr.commit();
    const dv = .8 * (.55 + .75 * sm(14, 50, vel));
    for (let i = 0; i < ND; i++) { const [x0, y, z] = dB[i], x = 60 - (((x0 + dist * 1.15) % 160) + 160) % 160, f = dv * sm(60, 48, x) * sm(-100, -88, x);
      dust.set(i, x, y, z, x + dL, y, z, .1, f, f * .86, f * .68); }
    dust.commit();
    // pulses (same speed relative to the ship, always)
    const lw = sm(tL + .8, tL + 3, t);
    pulses.forEach((P, k) => { const n = Math.floor((t - tL) / PER) - k; const tp = tL + n * PER; const x = -280 + CREL * (t - tp);
      const on = n >= 0 && t >= tp && x < WX + 2; P.G.visible = on; if (!on) return;
      P.G.position.x = x; const f = sm(-280, -200, x) * (1 - sm(WX - 25, WX, x)); P.m.opacity = f; P.h1.material.opacity = f; P.h2.material.opacity = .45 * f; });
    let hit = 0; { const tp = tL + Math.floor((t - tL) / PER) * PER, ta = tp + (WX + 280) / CREL; if (t >= ta && t - tL >= 0) hit = Math.exp(-(t - ta) * 1.4); }
    wallM.opacity = (.24 + .06 * Math.sin(t * .5) + .14 * hit) * lw; wallM2.opacity = (.07 + .05 * eInf) * lw; wallRingM.opacity = (.12 + .15 * hit) * lw;
    trM1.opacity = .45 + .25 * lw + .15 * ePush;
    // ship: straining tremor only on "infinite" (slow, small); engine plume and the energy bubble follow power
    SHIP.position.x = X; HULL.scale.setScalar(Math.max(.001, kv)); engL.position.x = X - 14;
    const tr = .05 * eInf * (1 - b); HULL.position.set(0, tr * Math.sin(t * 3.7) * Math.sin(t * 1.3), tr * Math.sin(t * 2.9 + 1));
    HULL.rotation.x = .02 * Math.sin(u * .4);
    const fl = 1 + .04 * Math.sin(t * 13) * Math.sin(t * 7.7);
    pl1.scale.set((3 + 9 * e) * fl * (1 + 1.1 * b), 1 + .1 * b, 1 + .1 * b); pl2.scale.set((5 + 15 * e) * fl * (1 + 1.5 * b), 1 + .2 * e + .2 * b, 1 + .2 * e + .2 * b);
    pl1.material.opacity = .3 + .25 * e + .15 * b; pl2.material.opacity = .1 + .12 * e + .05 * b;
    engG1.scale.setScalar(3.5 + 5 * e + 1.5 * b); engG1.material.opacity = .5 + .3 * e; engG2.scale.setScalar(10 + 16 * e + 6 * b); engG2.material.opacity = .14 + .12 * e + .04 * b;
    engL.intensity = 12 + 90 * e + 160 * b; throatM.color.setRGB(1.2 + 1.6 * e + 2 * b, 1.5 + 1.4 * e + 2 * b, 2.2 + 1 * e + 1.5 * b);
    const bfl = b * (1 + .05 * Math.sin(t * 17) * Math.sin(t * 9.3));
    bF1.material.opacity = .4 * bfl; bF1.scale.setScalar(4 + 2.5 * b); bF2.material.opacity = .12 * bfl; bF2.scale.setScalar(18 + 10 * b);
    bAna.material.opacity = .4 * bfl; bAna.scale.set(70 * b + 1, 1.2, 1);
    // flash where the ship meets the light wall: rises ~.2 s, fades over ~1.2 s
    const xe = Math.pow(.62, .4) * 2.65 + .35, wf = sm(55, 70, X) * Math.exp(-Math.max(0, xb - xe) * .9);
    wFl.material.opacity = .4 * wf; wFl.scale.setScalar(14 + 22 * wf); wFl2.material.opacity = .14 * wf;
    radM.emissiveIntensity = .35 * e;
    const bw = .55 * ePush + .45 * eInf; bub1.material.opacity = .1 * bw; bub1.scale.setScalar(20 + 10 * bw);
    bub2.material.opacity = .14 * bw * bw; bub2.scale.setScalar(12 + 8 * bw); bub2.material.color.setRGB(.75 + .25 * bw, .82 + .18 * bw, 1);
    bub1.material.opacity *= kv; bub2.material.opacity *= kv;
    bow.material.opacity = .3 * bw * kv; bow.scale.setScalar(3 + 4 * bw);
    // camera: behind and to the side, the track converging on the wall ahead; drifts in slowly, lowers a little under power
    const k = sm(0, 25, u);
    cam.position.set(-41 + 3 * k - 2 * e, 9.5 - 1.5 * k - 1 * e, 21.5 - 1.5 * k);
    // exit: the look-at point glides forward after the ship (continuous), the lens widens a touch with the boost
    cam.lookAt(5 + 2 * e + 16 * sm(tX + .3, tX + 3.2, t), -1.5 + .8 * sm(tX + .3, tX + 3.2, t), 0);
    cam.fov = vf(34 + 3 * e + 3 * b); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    RIMU.value.set(1, .25, 0).normalize().transformDirection(cam.matrixWorldInverse);
  } };
};
