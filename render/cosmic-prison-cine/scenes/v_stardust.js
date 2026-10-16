// stardust — "the calcium in your bones, the iron in your blood ... forged inside stars" (cosmic-prison-cine S52; written
// 2026-10-15). A lone standing person seen from behind (ONE smooth faceless merged mesh, dark navy, a warm rim only on the edges that
// face the star, a cool neutral fill) on a dark plain under the stars, looking up at a dying red giant high in the sky: a glowing
// orange core with slow granulation, nested shells of gas (gold, rose, teal) and soft halos. Gentle, no strobe.
// params (cues; all optional):
//   forge   the star sheds its shells: new shells lift off the core one after another and drift outward, fading (the core
//           shrinks and turns whiter, on its way to a white dwarf)
//   flow    its glowing dust (gold, teal and rose specks: calcium, iron, oxygen — symbolic colours, no labels) streams across space
//           in a soft swirling river down to the person and flows into the figure
//   within  the figure glows softly from within (warm inner light, specks of the same three colours inside it), still looking up
//   burst   (optional cue) the moment the star explodes on "forge": a soft white flash, a shockwave ring racing out, ejecta
//           streaking outward, the light washing over the plain and the figure (default: forge + 1.0 s)
//   side    subject offset (default .12)
// Second staging pass (2026-10-16): forge = supernova (flash, shockwave rings, decelerating ejecta streaks, a blast shell);
// flow = the element river accelerates (its front speeds up, the specks speed up, element streaks stretch with their speed);
// within = specks swirl around the figure and settle into it one after another, a warm bloom and a ground ring of light.
// Near-field warm bokeh motes drift in front of the plain for depth.
// Without cues: the dying star with its old shells above the person, stars, faint dust.
(window.MIYA = window.MIYA || { scenes: {} }).scenes.stardust = function (ctx, p) {
  const { T, sm, rng, cue, glow, ctex } = ctx, K = window.MIYA.kit;
  const S = new T.Scene(); S.background = new T.Color('#070820'); S.fog = new T.FogExp2('#0a0a24', .012);
  const v3 = (x, y, z) => new T.Vector3(x, y, z);
  const cT = c => c == null ? 1e9 : cue(c);
  const cF = cT(p.forge), cL = cT(p.flow), cW = cT(p.within), tX = p.burst != null ? cue(p.burst) : cF + 1.0;
  const GOLD = new T.Color('#ffc65a'), TEAL = new T.Color('#5ff0dc'), ROSE = new T.Color('#ff7aa6'), COLS = [GOLD, TEAL, ROSE];

  // points with a clamped pixel size (soft dots; never sub-pixel, never huge near the camera)
  const ptsM = (minPx, maxPx, depthTest) => new T.ShaderMaterial({ transparent: true, depthWrite: false, depthTest: depthTest !== false, blending: T.AdditiveBlending,
    uniforms: { uS: { value: ctx.H / 2 }, uSize: { value: .1 }, uMin: { value: minPx }, uMax: { value: maxPx }, uOp: { value: 1 } },
    vertexShader: `attribute vec3 col; attribute float sz; varying vec3 vC; uniform float uS, uSize, uMin, uMax;
      void main() { vC = col; vec4 mv = modelViewMatrix * vec4(position, 1.); gl_Position = projectionMatrix * mv; float s = uSize * sz * uS / -mv.z;
        gl_PointSize = clamp(s, uMin, uMax); vC *= min(1., s / uMin * .5 + .5); }`,
    fragmentShader: `varying vec3 vC; uniform float uOp; void main() { vec2 q = gl_PointCoord - .5; float r = dot(q, q) * 4.; float a = exp(-r * 3.2) * (1. - smoothstep(.8, 1., r));
      gl_FragColor = vec4(vC * a * uOp, 1.);
      #include <colorspace_fragment>
      }` });
  const mkPts = (n, m) => { const g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(new Float32Array(n * 3), 3)); g.setAttribute('col', new T.BufferAttribute(new Float32Array(n * 3), 3)); g.setAttribute('sz', new T.BufferAttribute(new Float32Array(n).fill(1), 1));
    const o = new T.Points(g, m); o.frustumCulled = false; return o; };
  // camera-facing streaks (copied from lightspeed.js): set(i, head xyz, tail xyz, width, r, g, b)
  function streaks(par, n, o) { o = o || {}; const g = new T.BufferGeometry(), H = new Float32Array(n * 12), Tl = new Float32Array(n * 12), C = new Float32Array(n * 12), Wd = new Float32Array(n * 4), cr = new Float32Array(n * 8), ix = [];
    for (let i = 0; i < n; i++) { cr.set([0, 0, 0, 1, 1, 0, 1, 1], i * 8); const b = i * 4; ix.push(b, b + 2, b + 1, b + 1, b + 2, b + 3); }
    const ad = (a, k) => { const q = new T.BufferAttribute(a, k); q.setUsage(T.DynamicDrawUsage); g.setAttribute(['aH', 'aT', 'aC', 'aW'][[H, Tl, C, Wd].indexOf(a)], q); };
    ad(H, 3); ad(Tl, 3); ad(C, 3); ad(Wd, 1); g.setAttribute('corner', new T.BufferAttribute(cr, 2)); g.setAttribute('position', new T.BufferAttribute(new Float32Array(n * 12), 3)); g.setIndex(ix);
    const m = new T.ShaderMaterial({ uniforms: { uH: { value: ctx.H }, uMin: { value: o.minPx || 1.6 }, uNear: { value: new T.Vector2(...(o.near || [.5, 4])) } }, transparent: true, depthWrite: false, depthTest: o.depthTest !== false, blending: T.AdditiveBlending, side: T.DoubleSide, fog: false,
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
  // integral of a smoothstep ramp from a over d seconds, evaluated at t (seek-safe distance travelled)
  const ism = (a, d, t) => { const x = (t - a) / d; if (x <= 0) return 0; if (x >= 1) return d * (x - .5); return d * (x * x * x - x * x * x * x / 2); };
  const ringTex = (inner) => ctex(256, (g, s) => { const r = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2);
    r.addColorStop(0, 'rgba(255,255,255,0)'); r.addColorStop(inner, 'rgba(255,255,255,.06)'); r.addColorStop(.86, 'rgba(255,255,255,.35)'); r.addColorStop(.93, 'rgba(255,255,255,1)');
    r.addColorStop(.97, 'rgba(255,255,255,.25)'); r.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = r; g.fillRect(0, 0, s, s); });

  // ---------------- sky ----------------
  ctx.stars(S, 3200, 500, { size: 1.15, opacity: .7, seed: 53 });
  [['#2a2470', -260, 120, -420, 520], ['#3a2264', 220, 60, -440, 420], ['#1d2a66', 0, 220, -400, 600]].forEach(([c, x, y, z, s]) => { const g = glow(S, c, s, .2); g.position.set(x, y, z); });

  // ---------------- the dying star ----------------
  const STAR = v3(5, 18.5, -78), SR = 3.2;
  const gran = K.tex(K.noise(256, { seed: 21, octaves: 4 }), false); gran.anisotropy = 8;
  const coreU = { map: { value: gran }, uT: { value: 0 }, uHot: { value: 0 } };
  const core = new T.Mesh(new T.SphereGeometry(SR, 64, 32), new T.ShaderMaterial({ uniforms: coreU, fog: false,
    vertexShader: `varying vec2 vUv; varying vec3 vN; varying vec3 vV; void main() { vUv = uv; vN = normalize(normalMatrix * normal); vec4 mv = modelViewMatrix * vec4(position, 1.); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `uniform sampler2D map; uniform float uT, uHot; varying vec2 vUv; varying vec3 vN; varying vec3 vV;
      void main() { float mu = max(dot(normalize(vN), vV), 0.), g = texture2D(map, vUv * vec2(2., 1.) + vec2(uT * .004, 0.)).r, g2 = texture2D(map, vUv * vec2(5., 2.5) - vec2(uT * .006, uT * .002)).r;
        vec3 cool = vec3(1.6, .55, .22), hot = vec3(1.7, 1.55, 1.45), c = mix(cool, hot, uHot);
        float limb = .35 + .65 * pow(mu, .55); gl_FragColor = vec4(c * limb * (.75 + .35 * g + .2 * g2), 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  core.position.copy(STAR); S.add(core);
  const h1 = glow(S, '#ff9a5a', SR * 4.5, .32), h2 = glow(S, '#ffc65a', SR * 10, .1), h3 = glow(S, '#ff7aa6', SR * 20, .04);
  [h1, h2, h3].forEach(h => h.position.copy(STAR));
  // supernova: flash glows, two camera-facing shockwave rings, ejecta streaks
  const fx1 = glow(S, '#fff6e8', SR * 6, 0), fx2 = glow(S, '#ffd9a0', SR * 22, 0); [fx1, fx2].forEach(h => { h.position.copy(STAR); h.material.fog = false; });
  const rTex = ringTex(.55), rings = [0, .45].map((d, i) => { const m = new T.Mesh(new T.PlaneGeometry(2, 2), new T.MeshBasicMaterial({ map: rTex, color: i ? '#ff9ac0' : '#ffe6c0', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, fog: false }));
    m.position.copy(STAR); S.add(m); return { m, d }; });
  const NE = 420, ej = streaks(S, NE, { minPx: 1.4, near: [.5, 2] }), eB = [];
  { const r = rng(57); for (let i = 0; i < NE; i++) { const u = r() * 2 - 1, th = r() * 6.283, q = Math.sqrt(1 - u * u); eB.push([q * Math.cos(th), u, q * Math.sin(th) * .6, 5 + 13 * Math.pow(r(), 1.5), i % 3, .5 + .5 * r(), r() * .25]); } }
  // shells: wispy additive spheres (fresnel rim x noise); 3 old ones always there, 5 new ones shed on "forge"
  const wisp = K.tex(K.noise(256, { seed: 33, octaves: 3 }), false); wisp.anisotropy = 8;
  const shellM = (col) => new T.ShaderMaterial({ transparent: true, depthWrite: false, blending: T.AdditiveBlending, side: T.DoubleSide, fog: false,
    uniforms: { map: { value: wisp }, uC: { value: new T.Color(col) }, uOp: { value: 0 }, uOff: { value: new T.Vector2() } },
    vertexShader: `varying vec2 vUv; varying vec3 vN; varying vec3 vV; void main() { vUv = uv; vN = normalize(normalMatrix * normal); vec4 mv = modelViewMatrix * vec4(position, 1.); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `uniform sampler2D map; uniform vec3 uC; uniform float uOp; uniform vec2 uOff; varying vec2 vUv; varying vec3 vN; varying vec3 vV;
      void main() { float mu = abs(dot(normalize(vN), vV)), rim = pow(1. - mu, 1.8) * .7 + .06, n = texture2D(map, vUv * vec2(2., 1.) + uOff).r, n2 = texture2D(map, vUv * vec2(4., 2.) - uOff).r;
        float w = smoothstep(.3, .85, n * .65 + n2 * .45); gl_FragColor = vec4(uC * rim * w * uOp, 1.);
        #include <colorspace_fragment>
      }` });
  const shG = new T.SphereGeometry(1, 64, 32), shells = [];
  const SC = ['#ffb46a', '#ff7aa6', '#5ff0dc', '#ffc65a', '#ff8f7a', '#7fe8d8', '#ffd090', '#ff86b0'];
  for (let i = 0; i < 8; i++) { const m = new T.Mesh(shG, shellM(SC[i])); m.position.copy(STAR); m.rotation.set(i * 1.3, i * .7, i * 2.1); S.add(m);
    m.position.add(v3(Math.sin(i * 2.3) * .8, Math.cos(i * 1.7) * .6, 0)); shells.push({ m, ax: [1 + .08 * Math.sin(i * 3.1), .9 + .06 * Math.cos(i * 2.2), 1], old: i < 3, t0: i < 3 ? -1 : tX + (i - 3) * 1.9, r0: i < 3 ? [6.5, 9.5, 13][i] : SR * 1.05, ph: i * 1.7 }); }

  // ---------------- ground + the person ----------------
  const gN = K.noise(256, { seed: 6, octaves: 3 }), gT = K.tex(gN, true, [40, 40]); gT.anisotropy = 8;
  const ground = new T.Mesh(new T.CircleGeometry(220, 96).rotateX(-Math.PI / 2), new T.MeshLambertMaterial({ color: '#1a1b38', map: gT })); S.add(ground);
  const FIG = v3(1.05, 0, 0);
  function merge(list) { let n = 0; const gs = list.map(([g, m]) => { const q = (g.index ? g.toNonIndexed() : g.clone()); q.applyMatrix4(m); n += q.attributes.position.count; return q; });
    const pos = new Float32Array(n * 3), nor = new Float32Array(n * 3); let o = 0;
    gs.forEach(g => { pos.set(g.attributes.position.array, o * 3); nor.set(g.attributes.normal.array, o * 3); o += g.attributes.position.count; });
    const out = new T.BufferGeometry(); out.setAttribute('position', new T.BufferAttribute(pos, 3)); out.setAttribute('normal', new T.BufferAttribute(nor, 3)); return out; }
  // one standing figure (faceless, arms down, head tipped back a little: looking up), height ~1.75, faces -z — ONE merged geometry
  // (same construction as the never-eat-human-meat figures)
  const figGeo = (() => { const V = v3, L = [];
    const limb = (a, b, r0, r1) => { const d = b.clone().sub(a), len = d.length(), g = new T.CylinderGeometry(r1, r0, len, 16, 1, true);
      L.push([g, new T.Matrix4().compose(a.clone().add(b).multiplyScalar(.5), new T.Quaternion().setFromUnitVectors(V(0, 1, 0), d.normalize()), V(1, 1, 1))]);
      [[a, r0], [b, r1]].forEach(([q, r]) => L.push([new T.SphereGeometry(r, 16, 12), new T.Matrix4().makeTranslation(q.x, q.y, q.z)])); };
    const tp = [[0, .86], [.165, .9], [.17, .98], [.145, 1.08], [.16, 1.22], [.19, 1.36], [.17, 1.44], [.08, 1.5], [.055, 1.53], [.055, 1.58], [0, 1.6]].map(([r, h]) => new T.Vector2(r, h));
    L.push([new T.LatheGeometry(tp, 24), new T.Matrix4().makeScale(1, 1, .62)]);
    L.push([new T.SphereGeometry(.105, 20, 16), new T.Matrix4().compose(V(0, 1.668, .03), new T.Quaternion().setFromEuler(new T.Euler(-.35, 0, 0)), V(.88, 1.08, .95))]);
    L.push([new T.SphereGeometry(.112, 18, 12, 0, 6.283, 0, 2.0), new T.Matrix4().compose(V(0, 1.668, .045), new T.Quaternion().setFromEuler(new T.Euler(-.35, 0, 0)), V(.95, 1.2, 1.0))]);
    const sx = .2;
    limb(V(sx - .02, 1.4, 0), V(sx + .03, 1.13, .02), .055, .045); limb(V(sx + .03, 1.13, .02), V(sx + .02, .87, -.03), .043, .034);
    limb(V(-sx + .02, 1.4, 0), V(-sx - .03, 1.13, .02), .055, .045); limb(V(-sx - .03, 1.13, .02), V(-sx - .02, .87, -.03), .043, .034);
    [sx + .02, -sx - .02].forEach(x => L.push([new T.SphereGeometry(.045, 12, 8), new T.Matrix4().compose(V(x, .82, -.03), new T.Quaternion(), V(.8, 1.3, .7))]));
    limb(V(.09, .9, 0), V(.1, .48, .01), .075, .055); limb(V(.1, .48, .01), V(.1, .07, .03), .052, .04);
    limb(V(-.09, .9, 0), V(-.1, .48, .01), .075, .055); limb(V(-.1, .48, .01), V(-.1, .07, .03), .052, .04);
    [.1, -.1].forEach(x => L.push([new T.SphereGeometry(.06, 12, 8), new T.Matrix4().compose(V(x, .045, -.05), new T.Quaternion(), V(.75, .6, 1.7))]));
    return merge(L); })();
  // material: dark navy, rim toward the star (view-space light position), soft inner light on "within"
  const rimLP = { value: new T.Vector3() }, inner = { value: 0 }, flashU = { value: 0 };
  const figM = new T.MeshStandardMaterial({ color: '#2c3150', roughness: .75, metalness: .05 });
  figM.onBeforeCompile = sh => { sh.uniforms.rimL = rimLP; sh.uniforms.uIn = inner; sh.uniforms.uFlash = flashU;
    sh.fragmentShader = 'uniform vec3 rimL; uniform float uIn, uFlash;\n' + sh.fragmentShader.replace('#include <emissivemap_fragment>',
      `#include <emissivemap_fragment>
      vec3 rLv = normalize(rimL + vViewPosition);
      float fr = pow(1.0 - abs(dot(normalize(normal), normalize(vViewPosition))), 2.6);
      vec2 rN = normal.xy / max(1e-4, length(normal.xy)), rS = rLv.xy / max(1e-4, length(rLv.xy));
      float rw = smoothstep(-.25, .75, dot(rN, rS)) * (.35 + .65 * smoothstep(-.4, .5, dot(normal, rLv)));
      totalEmissiveRadiance += vec3(1., .79, .54) * fr * rw * 1.1 * (1. + uFlash * 2.2);
      totalEmissiveRadiance += vec3(1., .66, .34) * uIn * (.01 + .045 * pow(1. - fr, 2.)) + vec3(.35, .9, .85) * uIn * .02 * fr;`); };
  figM.customProgramCacheKey = () => 'stardustFig';
  const fig = new T.Mesh(figGeo, figM); fig.position.copy(FIG); S.add(fig);
  const figGlow = glow(S, '#ffcf8a', 2.6, 0); figGlow.position.copy(FIG).add(v3(0, 1.2, -.7));
  const bloom = glow(S, '#ffd9a0', 6, 0); bloom.position.copy(FIG).add(v3(0, 1.1, -.4));
  // ground ring of light on "within"
  const gRing = new T.Mesh(new T.PlaneGeometry(2, 2).rotateX(-Math.PI / 2), new T.MeshBasicMaterial({ map: ringTex(.6), color: '#ffc884', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, fog: false }));
  gRing.position.copy(FIG).add(v3(0, .02, 0)); S.add(gRing);
  // lights: cool neutral fill, faint warm key from the star, a sky hemisphere
  S.add(new T.HemisphereLight('#6a76a8', '#0b0a18', .85));
  const key = new T.DirectionalLight('#ffb07a', .5); key.position.copy(STAR); S.add(key);
  const fill = new T.DirectionalLight('#9aa8c8', .35); fill.position.set(6, 4, 10); S.add(fill);

  // ---------------- the dust river (star -> figure) ----------------
  const P0 = STAR.clone().add(v3(-1, -3, 4)), P1 = v3(16, 17, -46), P2 = v3(4, 5, -14), P3 = FIG.clone().add(v3(0, 1.28, -.12));
  const bez = (s, o) => { const a = 1 - s; return o.set(0, 0, 0).addScaledVector(P0, a * a * a).addScaledVector(P1, 3 * a * a * s).addScaledVector(P2, 3 * a * s * s).addScaledVector(P3, s * s * s); };
  const NR = 4600, riv = mkPts(NR, ptsM(1.3, 4.5)), rA = riv.geometry.attributes.position.array, rC = riv.geometry.attributes.col.array, rZ = riv.geometry.attributes.sz.array, rB = [];
  { const r = rng(91); for (let i = 0; i < NR; i++) { rB.push([r(), r() * 6.283, Math.sqrt(r()), .6 + .8 * r(), i % 3, r()]); rZ[i] = .6 + .9 * r(); } }
  riv.material.uniforms.uSize.value = .32; S.add(riv);
  const NK = 300, rs = streaks(S, NK, { minPx: 1.3, near: [.6, 3] }), kB = [];
  { const r = rng(95); for (let i = 0; i < NK; i++) kB.push([r(), r() * 6.283, Math.sqrt(r()) * .8, .8 + .6 * r(), i % 3, r()]); }
  const rivPos = (s, b, o) => { bez(s, o); const sp = (.15 + 3.8 * Math.pow(1 - s, 1.4)) * b[2], an = b[1] + s * 9 + ctx.t * .25 * (b[5] - .5);
    return o.set(o.x + Math.cos(an) * sp, o.y + Math.sin(an) * sp * .7, o.z + Math.sin(an + 1.3) * sp * .5); };
  // inner specks (inside the figure, seen through it on "within")
  const NI = 700, inn = mkPts(NI, ptsM(1.2, 3, false)), iA = inn.geometry.attributes.position.array, iC = inn.geometry.attributes.col.array, iB = [];
  { const r = rng(93), fp = figGeo.attributes.position; for (let i = 0; i < NI; i++) { const k = Math.floor(r() * fp.count), x = fp.getX(k), y = fp.getY(k), z = fp.getZ(k), f = .25 + .5 * r();
    const cx = Math.abs(x) > .13 && y < .95 ? Math.sign(x) * .1 : Math.abs(x) > .17 ? Math.sign(x) * (.2 + (y - 1.4) * -.05) : 0;   // limb axes (legs / arms) or the body axis
    iB.push([FIG.x + cx + (x - cx) * f, y, FIG.z + z * f, r() * 6.283, i % 3]); } }
  inn.material.uniforms.uSize.value = .02; inn.renderOrder = 5; S.add(inn);
  // settling specks: swirl around the figure on "within" and settle into it one after another (each at its own delay)
  const NQ = 320, stl = mkPts(NQ, ptsM(1.3, 4, false)), qA = stl.geometry.attributes.position.array, qC = stl.geometry.attributes.col.array, qB = [];
  { const r = rng(97), fp = figGeo.attributes.position; for (let i = 0; i < NQ; i++) { const k = Math.floor(r() * fp.count), f = .3 + .5 * r();
    qB.push([FIG.x + fp.getX(k) * f, fp.getY(k), FIG.z + fp.getZ(k) * f, r() * 6.283, i % 3, r() * 4.2, .55 + .7 * r(), r()]); } }
  stl.material.uniforms.uSize.value = .03; stl.renderOrder = 6; S.add(stl);
  // near-field warm bokeh motes (parallax depth in front of the plain; kept to the right two thirds of the frame)
  const NB = 50, bok = mkPts(NB, ptsM(3, 14)), bA = bok.geometry.attributes.position.array, bC = bok.geometry.attributes.col.array, bZ = bok.geometry.attributes.sz.array, bB = [];
  { const r = rng(99); for (let i = 0; i < NB; i++) { bB.push([r(), r(), r(), r() * 6.283, .4 + .6 * r(), i % 3]); bZ[i] = .7 + .8 * r(); } }
  bok.material.uniforms.uSize.value = .05; S.add(bok);
  // faint ambient dust in the air
  const dust = K.snow(S, { n: 900, box: [30, 14, 30], size: .05, opacity: .45, color: '#ffd9a0', fall: .03, seed: 7 });

  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .05, 1500); ctx.side(cam, p.side == null ? .12 : p.side);
  const tmp = new T.Vector3(), tmp2 = new T.Vector3();
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const fl = sm(cL, cL + 7, t), wi = sm(cW, cW + 4, t), fo = sm(cF, cF + 3, t);
    // camera: low behind the person, drifting slowly closer; on "within" it eases in a little more
    cam.position.set(.2 + .25 * Math.sin(u * .05), 1.2 + .05 * Math.sin(u * .07), 6.4 - u * .008);
    cam.lookAt(.6, 2.0 + .15 * wi, -10);
    cam.updateMatrixWorld(); rimLP.value.copy(STAR).applyMatrix4(cam.matrixWorldInverse);
    // supernova on "forge" (burst): flash (rise .25 s, fade ~1.6 s), two shockwave rings, decelerating ejecta streaks
    const aX = t - tX, fe = aX <= 0 ? 0 : sm(0, .25, aX) * Math.exp(-Math.max(0, aX - .25) / 1.6);
    const aL = t - cL, fl2 = aL <= 0 ? 0 : sm(0, .3, aL) * Math.exp(-Math.max(0, aL - .3) / 1.5);
    fx1.material.opacity = .7 * fe + .22 * fl2; fx1.scale.setScalar(SR * (5 + 4 * sm(0, 2, aX)));
    fx2.material.opacity = .2 * fe + .05 * fl2; fx1.visible = fx1.material.opacity > .002; fx2.visible = fx2.material.opacity > .002;
    flashU.value = fe; key.intensity = .5 + 2.2 * fe;
    rings.forEach(({ m, d }, i) => { const a = aX - d; if (a <= 0 || a > 12) { m.visible = false; return; } m.visible = true;
      const r = SR + (i ? 17 : 22) * (1 - Math.exp(-a / 2.4)); m.scale.set(r, r, 1); m.quaternion.copy(cam.quaternion);
      m.material.opacity = sm(0, .2, a) * Math.exp(-a / 2.2) * (i ? .45 : .8); });
    ej.mesh.visible = aX > 0 && aX < 14.5;
    if (ej.mesh.visible) for (let i = 0; i < NE; i++) { const b = eB[i], a = aX - b[6]; if (a <= 0 || a > 14) { ej.hide(i); continue; }
      const tau = 2.6, dist = b[3] * tau * (1 - Math.exp(-a / tau)), vel = b[3] * Math.exp(-a / tau), len = .25 + vel * .45, r0 = SR * .9 + dist;
      const v = sm(0, .12, a) * Math.exp(-a / 3.2) * b[5] * 1.6, c = COLS[b[4]], w = 1 - sm(0, 1.5, a);
      ej.set(i, STAR.x + b[0] * r0, STAR.y + b[1] * r0, STAR.z + b[2] * r0, STAR.x + b[0] * Math.max(SR * .9, r0 - len), STAR.y + b[1] * Math.max(SR * .9, r0 - len), STAR.z + b[2] * Math.max(SR * .9, r0 - len),
        .14, (c.r + (1.2 - c.r) * w) * v, (c.g + (1.15 - c.g) * w) * v, (c.b + (1.05 - c.b) * w) * v); }
    if (ej.mesh.visible) ej.commit();
    // star: granulation turns; after the blast the core shrinks and grows whiter (toward a white dwarf)
    const hot = sm(tX + .5, tX + 10, t); coreU.uT.value = t; coreU.uHot.value = Math.max(hot, fe); core.scale.setScalar(1 - .45 * hot);
    h1.material.opacity = .32 + .08 * fo; h1.material.color.set(hot > .5 ? '#ffd9b0' : '#ff9a5a');
    h2.material.opacity = .1 + .04 * fo;
    shells.forEach(s => { const m = s.m.material.uniforms; m.uOff.value.set(t * .002 + s.ph, s.ph * .3);
      if (s.old) { const r = s.r0 * (1 + .002 * u); s.m.scale.set(r * s.ax[0], r * s.ax[1], r); m.uOp.value = [.22, .16, .12][shells.indexOf(s)] * (1 - .3 * fo); }
      else { const a = t - s.t0; if (a <= 0) { s.m.visible = false; return; } s.m.visible = true; const r = s.r0 + 13 * (1 - Math.exp(-a / 9)); s.m.scale.set(r * s.ax[0], r * s.ax[1], r); m.uOp.value = sm(0, 2, a) * (.35 * Math.exp(-a / 12) + .05); } });
    // river: each particle moves along the path; the front reaches the figure ~6 s after "flow"
    // accelerating: the front speeds up (reaches the figure ~6.2 s after "flow"), the specks speed up over 1-7 s, slow down on "within"
    const run = Math.max(0, t - cL), front = Math.min(1.05, Math.pow(run / 6.2, 1.25));
    const F = .03 * run + .07 * ism(1, 6, run) - .05 * ism(cW - cL, 4, run), vF = .03 + .07 * sm(1, 7, run) - .05 * sm(cW - cL, cW - cL + 4, run);
    for (let i = 0; i < NR; i++) { const b = rB[i], s = (b[0] + F * b[3]) % 1, k = i * 3; let v = 0;
      if (run > 0 && s < front) { bez(s, tmp); const sp = (.15 + 3.8 * Math.pow(1 - s, 1.4)) * b[2], an = b[1] + s * 9 + t * .25 * (b[5] - .5);
        rA[k] = tmp.x + Math.cos(an) * sp; rA[k + 1] = tmp.y + Math.sin(an) * sp * .7; rA[k + 2] = tmp.z + Math.sin(an + 1.3) * sp * .5;
        v = (.45 + .55 * b[5]) * sm(0, .04, s) * (1 - sm(front - .06, front, s) * .7) * (s > .97 ? (1 - s) / .03 : 1) * (.8 + .2 * Math.sin(t * 1.3 + b[1] * 5)); }
      else rA[k + 1] = -999;
      const c = COLS[b[4]]; rC[k] = c.r * v; rC[k + 1] = c.g * v; rC[k + 2] = c.b * v; }
    riv.geometry.attributes.position.needsUpdate = true; riv.geometry.attributes.col.needsUpdate = true;
    riv.material.uniforms.uOp.value = .9 * (1 - .4 * wi);
    // element streaks along the river: length grows with speed
    rs.mesh.visible = run > 0;
    if (run > 0) for (let j = 0; j < NK; j++) { const b = kB[j], s = (b[0] + F * b[3] * 1.25) % 1;
      if (run <= 0 || s >= front) { rs.hide(j); continue; }
      const ds = Math.min(.08, Math.max(.004, vF * b[3] * 1.25 * .7)); rivPos(s, b, tmp); rivPos(Math.max(0, s - ds), b, tmp2);
      const v = (.5 + .6 * b[5]) * sm(0, .05, s) * (1 - sm(front - .06, front, s) * .7) * (s > .96 ? (1 - s) / .04 : 1) * (1 - .5 * wi) * (.22 + .7 * sm(.04, .45, s)), c = COLS[b[4]];
      rs.set(j, tmp.x, tmp.y, tmp.z, tmp2.x, tmp2.y, tmp2.z, .045, c.r * v, c.g * v, c.b * v); }
    if (run > 0) rs.commit();
    // the figure: the dust arriving warms it, then it glows from within
    inner.value = .25 * fl * sm(cL + 4, cL + 8, t) + .75 * wi;
    figGlow.material.opacity = .1 * fl + .18 * wi; figGlow.scale.setScalar(2.4 + .8 * wi);
    for (let i = 0; i < NI; i++) { const b = iB[i], k = i * 3, tw = .6 + .4 * Math.sin(t * .9 + b[3] * 3);
      iA[k] = b[0] + .004 * Math.sin(t * .5 + b[3]); iA[k + 1] = b[1] + .004 * Math.cos(t * .4 + b[3]); iA[k + 2] = b[2];
      const v = (.35 * fl * sm(cL + 4, cL + 8, t) + .9 * wi) * tw * .6, c = COLS[b[4]]; iC[k] = c.r * v; iC[k + 1] = c.g * v; iC[k + 2] = c.b * v; }
    inn.geometry.attributes.position.needsUpdate = true; inn.geometry.attributes.col.needsUpdate = true;
    // settling: each speck swirls in from above/around the figure and eases into its place inside
    stl.visible = t > cW - 1.3;
    if (stl.visible) for (let i = 0; i < NQ; i++) { const b = qB[i], ts = cW + b[5], k = i * 3, ap = sm(ts - 1.2, ts - .4, t);
      if (ap <= 0) { qA[k + 1] = -999; qC[k] = qC[k + 1] = qC[k + 2] = 0; continue; }
      const e = sm(ts, ts + 2.2, t), o = 1 - e, an = b[3] + t * 1.1 * (b[7] > .5 ? 1 : -1), R = (.45 + .8 * b[6]) * o;
      qA[k] = b[0] + Math.cos(an) * R; qA[k + 1] = b[1] + (1.3 * b[6] + .3 * Math.sin(an * 2 + b[3])) * o * o; qA[k + 2] = b[2] + Math.sin(an) * R * .8;
      const v = ap * (.32 + .9 * o) * (.6 + .4 * Math.sin(t * .9 + b[3] * 3)), c = COLS[b[4]]; qC[k] = c.r * v; qC[k + 1] = c.g * v; qC[k + 2] = c.b * v; }
    stl.geometry.attributes.position.needsUpdate = true; stl.geometry.attributes.col.needsUpdate = true;
    // warm bloom and a ground ring of light on "within"
    const aW = t - cW, bl = aW <= 0 ? 0 : sm(0, .5, aW) * Math.exp(-Math.max(0, aW - .5) / 2.5);
    bloom.material.opacity = .4 * bl; bloom.scale.setScalar(3.6 + 1.4 * sm(0, 3, aW)); bloom.visible = bloom.material.opacity > .004;
    figGlow.visible = figGlow.material.opacity > .002;
    { const a = aW - .2; if (a <= 0) gRing.visible = false; else { gRing.visible = true; const r = .3 + 1.7 * (1 - Math.exp(-a / 1.4)); gRing.scale.set(r, 1, r); gRing.material.opacity = sm(0, .25, a) * Math.exp(-a / 1.6) * .45; gRing.visible = a < 9; } }
    // bokeh motes: camera-relative, slow rise + sway, faded in/out over their cycle (seek-safe recycling)
    for (let i = 0; i < NB; i++) { const b = bB[i], k = i * 3, s = (b[1] + t * .01 * b[4]) % 1, dz = 1.3 + 3.2 * b[2];
      bA[k] = cam.position.x + (-.25 + 2.3 * b[0]) * dz * .42 + .12 * Math.sin(t * .13 * b[4] + b[3]); bA[k + 1] = cam.position.y + (-.75 + 1.5 * s) * dz * .38; bA[k + 2] = cam.position.z - dz;
      const v = .16 * Math.sin(Math.PI * s) * (.6 + .4 * Math.sin(t * .4 + b[3])), c = COLS[b[5]]; bC[k] = c.r * v; bC[k + 1] = c.g * v; bC[k + 2] = c.b * v; }
    bok.geometry.attributes.position.needsUpdate = true; bok.geometry.attributes.col.needsUpdate = true;
    dust.update(t, [cam.position.x, cam.position.y + 2, cam.position.z - 10]);
  } };
};
