// warp — a solid starship (lathe hull with bevelled nose, engine block, two engine pods on pylons, a metal field ring on struts,
// lit window strip, panel-lined metal with env reflections, gold rim lights) resting inside an Alcubierre warp bubble. Space is
// drawn as real lensing of a baked sky (cube map): in front of the bubble the starfield is compressed (stars bunch, blueshifted),
// behind it expanded and smeared into streaks (redshifted); a faint bubble rim and a thin equatorial field ring glow. Interstellar
// dust streams past and around the bubble. Written for cosmic-prison-cine S32-S34 (2026-10-15).
// params (cues, all optional):
//   warp      the bubble forms and the ship starts to move (absent: bubble already on and moving from the start)
//   energy    the energy needed: a Jupiter-sized banded sphere appears beside the ship for scale, then dissolves into a stream of
//             light that pours into the field ring (symbol: "at least the mass-energy of Jupiter")
//   snowplow  dust no longer slips past: it piles up on the bubble's front wall and glows hotter and hotter (orange -> white-blue)
//   blast     the ship stops: the bubble drops and the stored particles burst forward in a cone of light (strong brief flash that
//             fades over ~2 s, no strobe)
//   trapped   S34: calm wide view: the camera pulls far back; the ship is a tiny light inside a dark sphere boundary
//   side      subject offset (default .12)
(window.MIYA = window.MIYA || { scenes: {} }).scenes.warp = function (ctx, p) {
  const { T, sm, rng, cue, points, glow } = ctx, Rr = ctx.R, K = window.MIYA.kit, E = ctx.env();
  const v3 = (x, y, z) => new T.Vector3(x, y, z);
  const cu = c => c == null ? null : cue(c);
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), ctx.t);

  // ---------------- baked sky (cube map): faint violet nebula + stars ----------------
  const hsh = (x, y, z) => { let h = (x * 374761393 + y * 668265263 + z * 1274126177) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };
  function vn(x, y, z) { const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), xf = x - xi, yf = y - yi, zf = z - zi;
    const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf), w = zf * zf * (3 - 2 * zf), L = (a, b, k) => a + (b - a) * k;
    return L(L(L(hsh(xi, yi, zi), hsh(xi + 1, yi, zi), u), L(hsh(xi, yi + 1, zi), hsh(xi + 1, yi + 1, zi), u), v), L(L(hsh(xi, yi, zi + 1), hsh(xi + 1, yi, zi + 1), u), L(hsh(xi, yi + 1, zi + 1), hsh(xi + 1, yi + 1, zi + 1), u), v), w); }
  const fbm = (x, y, z, o) => { let s = 0, a = .5, f = 1; for (let k = 0; k < o; k++) { s += a * vn(x * f, y * f, z * f); a *= .5; f *= 2.03; } return s; };
  const sky = new T.Scene(); sky.background = new T.Color('#02030a');
  { const SW = 640, SH = 320, c = document.createElement('canvas'); c.width = SW; c.height = SH; const g = c.getContext('2d'), im = g.createImageData(SW, SH), D = im.data;
    for (let y = 0; y < SH; y++) { const th = (y + .5) / SH * Math.PI, st = Math.sin(th), ct = Math.cos(th);
      for (let x = 0; x < SW; x++) { const ph = (x + .5) / SW * 6.2832, dx = -Math.cos(ph) * st, dy = ct, dz = Math.sin(ph) * st, k = (y * SW + x) * 4;
        const n1 = fbm(dx * 2.2 + 3, dy * 2.2, dz * 2.2, 4), bd = Math.exp(-Math.pow(.2 * dx + .9 * dy - .4 * dz, 2) / .05), v = Math.max(0, n1 - .42) * 1.5 + bd * .35 * n1;
        const col = [.004 + v * .035, .005 + v * .026, .014 + v * .07]; for (let j = 0; j < 3; j++) D[k + j] = Math.min(255, Math.pow(col[j], 1 / 2.2) * 255); D[k + 3] = 255; } }
    g.putImageData(im, 0, 0); const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace;
    sky.add(new T.Mesh(new T.SphereGeometry(900, 64, 32), new T.MeshBasicMaterial({ map: t, side: T.BackSide, depthWrite: false }))); }
  const scol = r => { const t = r(), b = .35 + 1.1 * Math.pow(r(), 3); return t < .25 ? [.7 * b, .8 * b, 1.1 * b] : t < .8 ? [b, .96 * b, .9 * b] : [b, .8 * b, .6 * b]; };
  [[15000, 2.2, 11], [900, 3.6, 13]].forEach(([n, size, seed]) => { const P = points(n, { size, opacity: 1, atten: false }), a = P.geometry.attributes.position.array, c = P.geometry.attributes.color.array, r = rng(seed);
    for (let i = 0; i < n; i++) { const u = r() * 2 - 1, th = r() * 6.283, q = Math.sqrt(1 - u * u); a.set([q * Math.cos(th) * 800, u * 800, q * Math.sin(th) * 800], i * 3); c.set(scol(r), i * 3); } sky.add(P); });
  const cube = new T.WebGLCubeRenderTarget(2048, { generateMipmaps: true, minFilter: T.LinearMipmapLinearFilter, magFilter: T.LinearFilter, colorSpace: T.SRGBColorSpace });
  if (Rr) { const pt = Rr.toneMapping; Rr.toneMapping = T.NoToneMapping; new T.CubeCamera(1, 2000, cube).update(Rr, sky); Rr.toneMapping = pt; }

  // ---------------- main scene ----------------
  const S = new T.Scene(); S.background = new T.Color('#02030a');
  const RB = 9, FWD = v3(1, 0, 0);
  const U = { tO: { value: cube.texture }, uC: { value: v3(0, 0, 0) }, uCam: { value: v3(0, 0, 0) }, uR: { value: RB }, uW: { value: 1 }, uRim: { value: 1 },
    uPInv: { value: new T.Matrix4() }, uCW: { value: new T.Matrix4() }, uF: { value: FWD.clone() }, uB2: { value: 60 }, uB2a: { value: 0 } };
  const lens = new T.Mesh(new T.PlaneGeometry(2, 2), new T.ShaderMaterial({ uniforms: U, depthWrite: false, depthTest: false,
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0., 1.); }',
    fragmentShader: `uniform samplerCube tO; uniform vec3 uC, uCam, uF; uniform float uR, uW, uRim, uB2, uB2a; uniform mat4 uPInv, uCW; varying vec2 vUv;
      void main(){
        vec4 pv = uPInv * vec4(vUv * 2. - 1., 1., 1.); pv /= pv.w;
        vec3 d = normalize((uCW * vec4(pv.xyz, 0.)).xyz), oc = uC - uCam;
        float tca = dot(oc, d), b2 = dot(oc, oc) - tca * tca, R2 = uR * uR;
        vec3 col = textureCube(tO, d).rgb;
        if (tca > 0. && b2 < R2 && uW > 0.) {
          float th = sqrt(R2 - b2); vec3 P = uCam + d * (tca - th), n = (P - uC) / uR;
          float z = dot(n, uF), edge = sqrt(b2) / uR, fall = 1. - smoothstep(.75, 1., edge);
          // f(z) = z + s z^2: compressed ahead (stars bunch), expanded behind (stars stretch)
          float s = 1.3 * uW * fall;
          vec3 dd = normalize(d + uF * s * .55 * z * abs(z) + uF * s * .25 * z);
          if (z < 0.) { vec3 acc = vec3(0.); for (int j = 0; j < 7; j++) acc += textureCube(tO, normalize(dd + uF * (float(j) / 6. - .5) * .16 * (-z) * s)).rgb; col = acc / 7. * 1.6; }
          else col = textureCube(tO, dd).rgb * (1. + .8 * z * s);
          // Doppler-like tint: blue ahead, red behind
          col *= mix(vec3(1.), z > 0. ? vec3(.8, .95, 1.35) : vec3(1.3, .85, .7), abs(z) * s);
          // bubble wall: faint fresnel rim
          col += uRim * uW * (pow(edge, 16.) * .07 + exp(-pow((edge - 1.) / .012, 2.)) * .22) * vec3(.75, .82, 1.);
        }
        // dark boundary sphere ("our local cosmic cell") in the trapped view: faint gold limb
        float B = uB2; if (uB2a > 0. && tca > 0.) { float bb = sqrt(max(0., dot(oc, oc) - tca * tca)) / B;
          if (bb < 1.) col = col * mix(1., .22, uB2a) + uB2a * pow(bb, 40.) * .12 * vec3(1., .8, .5);
          col += uB2a * exp(-pow((bb - 1.) / .004, 2.)) * .3 * vec3(1., .8, .5); }
        gl_FragColor = vec4(col, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  lens.frustumCulled = false; lens.renderOrder = -10; S.add(lens);

  // ---------------- the ship ----------------
  const SHIP = new T.Group(); S.add(SHIP);
  const panel = ctx.ctex(512, (g, s) => { g.fillStyle = '#d9dde6'; g.fillRect(0, 0, s, s); g.globalAlpha = .18; g.drawImage(K.noise(256, { seed: 4, octaves: 3 }), 0, 0, s, s); g.globalAlpha = 1;
    g.strokeStyle = 'rgba(40,46,64,.55)'; g.lineWidth = 2; for (let i = 0; i <= 8; i++) { g.beginPath(); g.moveTo(0, i * s / 8); g.lineTo(s, i * s / 8); g.stroke(); }
    for (let i = 0; i < 16; i++) { const y = (i % 8) * s / 8; g.beginPath(); g.moveTo(i * s / 16 + (i % 2) * 10, y); g.lineTo(i * s / 16 + (i % 2) * 10, y + s / 8); g.stroke(); }
    g.fillStyle = 'rgba(30,34,50,.35)'; g.fillRect(0, s * .46, s, s * .05); });
  panel.wrapS = panel.wrapT = T.RepeatWrapping; panel.repeat.set(3, 1); panel.anisotropy = 4;
  const hullM = new T.MeshStandardMaterial({ map: panel, metalness: .55, roughness: .38, envMap: E, envMapIntensity: .55 });
  const darkM = new T.MeshStandardMaterial({ color: '#2a2e40', metalness: .8, roughness: .3, envMap: E, envMapIntensity: .6 });
  const goldM = new T.MeshStandardMaterial({ color: '#c9a25a', metalness: .9, roughness: .28, envMap: E, envMapIntensity: .8, emissive: '#ffb347', emissiveIntensity: .25 });
  const lit = c => new T.MeshBasicMaterial({ color: new T.Color(c).multiplyScalar(1.6), toneMapped: true });
  const hp = [[0, 4.4], [.18, 4.25], [.42, 3.8], [.66, 3.0], [.86, 1.9], [.98, .6], [1.02, -1.4], [1.14, -1.6], [1.18, -2.5], [1.08, -2.7], [.86, -2.75], [.8, -3.05], [.55, -3.1], [0, -3.1]].map(([r, h]) => new T.Vector2(r, h));
  const hull = new T.Mesh(new T.LatheGeometry(hp, 64).rotateZ(-Math.PI / 2), hullM); SHIP.add(hull);
  // canopy / window strip, dorsal spine
  const canopy = new T.Mesh(new T.SphereGeometry(.42, 32, 16, 0, Math.PI * 2, 0, Math.PI / 2).scale(1.9, .55, .8), new T.MeshStandardMaterial({ color: '#1a2036', metalness: .9, roughness: .08, envMap: E, envMapIntensity: 1.2 }));
  canopy.position.set(2.5, .62, 0); SHIP.add(canopy);
  for (let i = 0; i < 9; i++) { const w = new T.Mesh(new T.BoxGeometry(.16, .07, .03), lit('#ffd28a')); w.position.set(1.6 - i * .32, .2, .99 - Math.max(0, i - 4) * .0); w.lookAt(w.position.x, .2, 3); SHIP.add(w);
    const w2 = w.clone(); w2.position.z = -w.position.z; w2.lookAt(w2.position.x, .2, -3); SHIP.add(w2); }
  const spine = new T.Mesh(K.fin([[0, 0], [2.6, 0], [1.6, .55], [.2, .5]], .14), darkM); spine.position.set(-2.4, .9, 0); SHIP.add(spine);
  // engine pods on pylons
  const podP = [[0, 1.6], [.12, 1.5], [.3, 1.1], [.36, .4], [.36, -1.0], [.42, -1.2], [.4, -1.35], [.28, -1.4], [0, -1.4]].map(([r, h]) => new T.Vector2(r, h));
  const podG = new T.LatheGeometry(podP, 40).rotateZ(-Math.PI / 2);
  const glows = [];
  [-1, 1].forEach(sg => { const pod = new T.Mesh(podG, hullM); pod.position.set(-1.6, -.25, sg * 1.75); SHIP.add(pod);
    const py = new T.Mesh(new T.BoxGeometry(1.2, .12, 1.0), darkM); py.position.set(-1.5, -.15, sg * 1.2); py.rotation.x = sg * .25; SHIP.add(py);
    const nz = new T.Mesh(new T.TorusGeometry(.33, .05, 10, 32).rotateY(Math.PI / 2), goldM); nz.position.set(-3.0, -.25, sg * 1.75); SHIP.add(nz);
    const eg = glow(SHIP, '#ffd69a', 1.2, .8); eg.position.set(-3.1, -.25, sg * 1.75); glows.push(eg); });
  const mainG = glow(SHIP, '#ffe2b0', 2.0, .8); mainG.position.set(-3.2, 0, 0); glows.push(mainG);
  const nozzle = new T.Mesh(new T.CylinderGeometry(.62, .78, .5, 40, 1, true).rotateZ(Math.PI / 2), darkM); nozzle.position.set(-3.25, 0, 0); SHIP.add(nozzle);
  // field ring on four struts (metal, gold inner edge that glows with the field)
  const RING = new T.Group(); RING.position.x = -.4; SHIP.add(RING);
  RING.add(new T.Mesh(new T.TorusGeometry(2.9, .2, 20, 128).rotateY(Math.PI / 2), darkM));
  const ringGlowM = new T.MeshBasicMaterial({ color: new T.Color('#ffc65a'), transparent: true, opacity: .6, blending: T.AdditiveBlending, depthWrite: false });
  RING.add(new T.Mesh(new T.TorusGeometry(2.72, .05, 8, 160).rotateY(Math.PI / 2), ringGlowM));
  for (let k = 0; k < 4; k++) { const a = k / 4 * Math.PI * 2 + Math.PI / 4, st = new T.Mesh(new T.BoxGeometry(.18, 1.85, .12), darkM); st.position.set(0, Math.cos(a) * 1.95, Math.sin(a) * 1.95); st.rotation.x = -a; RING.add(st); }
  SHIP.add(new T.HemisphereLight('#3a4290', '#05040c', .5));
  const key = new T.DirectionalLight('#ffe0b8', 1.6); key.position.set(6, 7, 9); S.add(key);
  const rimL = new T.DirectionalLight('#8fa6ff', 1.4); rimL.position.set(-9, 4, -7); S.add(rimL);
  const fillL = new T.DirectionalLight('#c8d0ff', .25); fillL.position.set(0, -5, 8); S.add(fillL);
  // bubble equator ring (thin) and soft halo
  const eqM = new T.MeshBasicMaterial({ color: '#9fb4ff', transparent: true, opacity: .1, blending: T.AdditiveBlending, depthWrite: false });
  const eq = new T.Mesh(new T.TorusGeometry(RB, .04, 6, 200).rotateY(Math.PI / 2), eqM); S.add(eq);

  // ---------------- Jupiter-sized sphere (energy symbol) ----------------
  const jupT = (() => { const c = document.createElement('canvas'); c.width = 512; c.height = 256; const g = c.getContext('2d');
    const bands = ['#eadcc2', '#d4b48e', '#efe4cc', '#b98d66', '#e6d3b4', '#a87a55', '#f0e7d4', '#c8a07a', '#e0cba8', '#9a6e4f', '#ead9bd', '#cfae8a', '#e9dcc4', '#b28866', '#e4d6bc'];
    const hx = c => [1, 3, 5].map(i => parseInt(c.slice(i, i + 2), 16));
    const im = g.createImageData(512, 256);
    for (let y = 0; y < 256; y++) for (let x = 0; x < 512; x++) { const ph = x / 512 * 6.2832, nv = fbm(Math.cos(ph) * 2.5 + 9, y / 256 * 22, Math.sin(ph) * 2.5, 4), f = y / 256 + (nv - .5) * .05 + .012 * Math.sin(x / 512 * 6.283 * 3 + y * .2);
      const kf = Math.max(0, Math.min(.9999, f)) * bands.length, k0 = Math.floor(kf), fr = sm(.3, .7, kf - k0), c0 = hx(bands[k0]), c1 = hx(bands[Math.min(bands.length - 1, k0 + 1)]), i = (y * 512 + x) * 4;
      for (let j = 0; j < 3; j++) im.data[i + j] = (c0[j] + (c1[j] - c0[j]) * fr) * (.9 + .2 * nv); im.data[i + 3] = 255; }
    g.putImageData(im, 0, 0);
    g.fillStyle = 'rgba(170,80,50,.7)'; g.beginPath(); g.ellipse(330, 165, 26, 13, 0, 0, 6.283); g.fill();
    const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; t.anisotropy = 4; return t; })();
  const jupM = new T.MeshStandardMaterial({ map: jupT, roughness: .9, metalness: 0, transparent: true, opacity: 1, emissive: '#ffb050', emissiveIntensity: 0 });
  const JUP = new T.Mesh(new T.SphereGeometry(13, 64, 32), jupM); JUP.rotation.z = .05; S.add(JUP);
  const jupHalo = glow(S, '#ffcf8a', 38, 0);
  const NE = 1800, est = points(NE, { size: .5, opacity: 1, color: '#ffd08a' }), eA = est.geometry.attributes.position.array, eC = est.geometry.attributes.color.array, eB = [];
  { const r = rng(91); for (let i = 0; i < NE; i++) { const u = r() * 2 - 1, th = r() * 6.283, q = Math.sqrt(1 - u * u); eB.push([q * Math.cos(th), u, q * Math.sin(th), r() * 6.283, r()]); } }
  est.frustumCulled = false; S.add(est);

  // ---------------- dust stream (relative to the ship) + snowplow + blast ----------------
  const ND = 5200, du = points(ND, { size: .28, opacity: 1, color: '#ffffff' }), dA = du.geometry.attributes.position.array, dC = du.geometry.attributes.color.array, dB = [];
  const T0 = ctx.t0 - 20, T1 = ctx.t1 + 1;
  { const r = rng(57); for (let i = 0; i < ND; i++) { const rho = r() < .5 ? Math.sqrt(r()) * RB * .96 : Math.sqrt(r()) * 26, a = r() * 6.283; dB.push({ y: Math.cos(a) * rho * .8, z: Math.sin(a) * rho, rho: rho, s: T0 + (T1 - T0) * r(), w: r(), bx: r() - .5, by: r() - .5, bz: r() - .5 }); } }
  du.frustumCulled = false; S.add(du);
  const pile = points(ND, { size: .5, opacity: 1, color: '#ffffff' }), pA = pile.geometry.attributes.position.array, pC = pile.geometry.attributes.color.array;
  pile.frustumCulled = false; S.add(pile);
  const capG = glow(S, '#ffb060', 14, 0); capG.position.set(RB + .3, 0, 0);
  const coneT = ctx.ctex(128, (g, s) => { const gr = g.createLinearGradient(0, s, 0, 0); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.25, 'rgba(255,230,180,.7)'); gr.addColorStop(1, 'rgba(255,170,90,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); });
  const coneM = new T.ShaderMaterial({ uniforms: { opacity: { value: 0 } }, transparent: true, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide,
    vertexShader: 'varying vec3 vN, vV; varying float vY; void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); vY = uv.y; gl_Position = projectionMatrix * mv; }',
    fragmentShader: `uniform float opacity; varying vec3 vN, vV; varying float vY;
      void main(){ float f = pow(abs(dot(normalize(vN), normalize(vV))), 2.2), g = pow(vY, 1.6) * (1. - smoothstep(.96, 1., vY));
        gl_FragColor = vec4(vec3(1., .82, .58) * pow(f, 2.) * g * opacity * .16, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` });
  coneM.blending = T.CustomBlending; coneM.blendSrc = T.OneFactor; coneM.blendDst = T.OneFactor;
  const cone = new T.Mesh(new T.ConeGeometry(14, 60, 48, 1, true).rotateZ(Math.PI / 2).translate(30 + RB * .8, 0, 0), coneM); S.add(cone);
  const blastG = glow(S, '#fff1d8', 30, 0), blastG2 = glow(S, '#ffc65a', 90, 0); blastG.position.set(RB + 7, 0, 0); blastG2.position.set(RB + 16, 0, 0);
  const shipG = glow(SHIP, '#ffd9a0', 10, 0);   // the ship as a tiny light in the trapped view

  // speed profile: D(t) = integral of v (analytic), seek-safe
  const IS = (a, b, t) => t <= a ? 0 : t >= b ? (b - a) * .5 + (t - b) : (b - a) * (Math.pow((t - a) / (b - a), 3) - Math.pow((t - a) / (b - a), 4) / 2);
  const cW = cu(p.warp), cS = cu(p.snowplow), cB = cu(p.blast), cE = cu(p.energy), cT = cu(p.trapped);
  const V0 = 2.5, V = 34;
  const Dd = t => V0 * t + (V - V0) * (cW == null ? t : IS(cW, cW + 3, t)) - (cB == null ? 0 : (V) * IS(cB - .25, cB + .35, t));

  const cam = new T.PerspectiveCamera(38, ctx.W / ctx.H, .1, 4000); ctx.side(cam, p.side == null ? .12 : p.side);
  const VF = ctx.VERT ? 1.2 : 1, tgt = v3(0, 0, 0);
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const w0 = cW == null ? 1 : sm(cW, cW + 2.5, t), stop = cB == null ? 0 : sm(cB - .1, cB + .5, t), w = w0 * (1 - stop);
    const tr = at(p.trapped, 6), tc = cT == null ? 1e9 : cT;
    U.uW.value = w; U.uRim.value = 1; eqM.opacity = .1 * w; ringGlowM.opacity = .25 + .55 * w;
    goldM.emissiveIntensity = .2 + .5 * w;
    glows.forEach((g, i) => g.material.opacity = (.35 + .4 * w0) * (i === 2 ? 1 : .8));
    SHIP.position.set(0, Math.sin(u * .4) * .12, 0); SHIP.rotation.set(Math.sin(u * .3) * .02, 0, Math.sin(u * .23) * .015);
    // energy: Jupiter fades in (2 s), holds, then dissolves into a stream feeding the ring
    const e = cE == null ? -1e9 : t - cE, ein = sm(0, 2, e), edis = sm(4, 7, e);
    JUP.visible = ein > 0 && edis < 1; jupM.opacity = ein * (1 - edis); jupM.emissiveIntensity = 1.2 * edis; JUP.scale.setScalar(1 - .5 * edis); JUP.rotation.y = t * .03;
    const azJ = .62 + u * .004, JP = v3(-Math.cos(azJ) * 25 - Math.sin(azJ) * 60, 4, Math.sin(azJ) * 25 - Math.cos(azJ) * 60); JUP.position.copy(JP); jupHalo.position.copy(JP); jupHalo.material.opacity = .18 * ein * (1 - edis) + .3 * edis * (1 - edis) * 4 * (1 - sm(6.5, 7.5, e));
    for (let i = 0; i < NE; i++) { const [x, y, z, a, r0] = eB[i], f = Math.max(0, Math.min(1, (e - 4.2 - r0 * 2.6) / 1.6)), on = f > 0 && f < 1;
      const src = JP.clone().add(v3(x, y, z).multiplyScalar(13 * (1 - .5 * edis))), dst = v3(-.4, Math.cos(a) * 2.85, Math.sin(a) * 2.85), sw = Math.sin(f * Math.PI) * 4;
      const q = src.lerp(dst, f * f * (3 - 2 * f)); eA[i * 3] = q.x + sw * Math.cos(a + 1); eA[i * 3 + 1] = q.y + sw * .3; eA[i * 3 + 2] = q.z + sw * Math.sin(a + 1);
      const v = on ? 1.2 * Math.sin(f * Math.PI) : 0; eC[i * 3] = v; eC[i * 3 + 1] = v * .78; eC[i * 3 + 2] = v * .45; }
    est.geometry.attributes.position.needsUpdate = true; est.geometry.attributes.color.needsUpdate = true;
    if (e > 4 && e < 9) ringGlowM.opacity += .6 * Math.sin(Math.PI * sm(4, 9, e));
    // dust: relative stream; flows around the bubble; after `snowplow` the dust inside the bubble's cross-section piles up on the
    // front wall (glowing hotter with time); on `blast` it bursts forward in a cone and fades
    const Dt = Dd(t), DS = cS == null ? 1e12 : Dd(cS), XS = 160, heat = cS == null ? 0 : sm(0, 14, t - cS), bt = cB == null ? -1 : t - cB;
    for (let i = 0; i < ND; i++) { const b = dB[i]; let x, y = b.y, z = b.z, r = 0, g = 0, bl = 0; pA[i * 3 + 1] = -9999; pC[i * 3] = pC[i * 3 + 1] = pC[i * 3 + 2] = 0;
      if (t < b.s) { dA[i * 3 + 1] = -9999; dC[i * 3] = dC[i * 3 + 1] = dC[i * 3 + 2] = 0; continue; }
      const Ds = Dd(b.s); x = XS - (Dt - Ds);
      const xh = b.rho < RB ? Math.sqrt(RB * RB - b.rho * b.rho) : -1e9, pinned = b.rho < RB * .97 && x < xh && Ds + XS - xh > DS;
      if (pinned) {
        // stuck on the front wall, slightly spread over the cap
        x = xh + .15 + b.bx * .3;
        let v = (.9 + 1.6 * heat) * (.6 + .4 * b.w);
        if (bt > 0) { const sp = (30 + 40 * b.w) * bt, dir = v3(1, b.by * .7, b.bz * .7).normalize(); x += dir.x * sp; y += dir.y * sp; z += dir.z * sp; v *= Math.exp(-bt * 1.4) * 1.8; }
        r = v; g = v * (.55 + .4 * heat); bl = v * (.25 + .9 * heat * heat);
        pA[i * 3] = x; pA[i * 3 + 1] = y; pA[i * 3 + 2] = z; pC[i * 3] = r * .7; pC[i * 3 + 1] = g * .7; pC[i * 3 + 2] = bl * .7;
        dA[i * 3 + 1] = -9999; dC[i * 3] = dC[i * 3 + 1] = dC[i * 3 + 2] = 0; continue;
      } else {
        // flow around the bubble (pushed radially out to just beyond the wall)
        const rr = Math.hypot(x, y, z), lim = RB * (1.06 + .04 * b.w) * (w > .05 ? 1 : 0);
        if (rr < lim && rr > 1e-3) { const k = lim / rr; x *= k; y *= k; z *= k; }
        const fade = sm(XS, XS - 30, x) * sm(-90, -60, x), v = (.18 + .3 * b.w) * fade * (.4 + .6 * w0);
        r = v * .95; g = v * .85; bl = v * .75;
      }
      if (x < -120) { dA[i * 3 + 1] = -9999; dC[i * 3] = dC[i * 3 + 1] = dC[i * 3 + 2] = 0; continue; }
      dA[i * 3] = x; dA[i * 3 + 1] = y; dA[i * 3 + 2] = z; const fT = 1 - tr * .9; dC[i * 3] = r * fT; dC[i * 3 + 1] = g * fT; dC[i * 3 + 2] = bl * fT; }
    du.geometry.attributes.position.needsUpdate = true; du.geometry.attributes.color.needsUpdate = true;
    pile.geometry.attributes.position.needsUpdate = true; pile.geometry.attributes.color.needsUpdate = true;
    const capOn = heat * (bt > 0 ? Math.exp(-bt * 2) : 1) * (1 - tr);
    capG.material.opacity = .55 * capOn; capG.material.color.setRGB(1, .6 + .35 * heat, .35 + .6 * heat * heat); capG.scale.setScalar(8 + 10 * heat);
    du.material.size = .28 * (1 + 2.5 * tr);
    // blast flash: rises in .15 s, fades over ~2 s
    const fl = bt > 0 ? sm(0, .15, bt) * Math.exp(-Math.max(0, bt - .15) * 1.5) : 0;
    coneM.uniforms.opacity.value = .9 * fl; cone.scale.set(.6 + .6 * sm(0, 1.5, bt), 1, 1); blastG.material.opacity = .4 * fl; blastG2.material.opacity = .18 * fl;
    // trapped: wide calm view, dark boundary sphere, the ship a tiny light
    U.uB2a.value = tr; U.uB2.value = 70; shipG.material.opacity = .8 * tr;
    // camera: three-quarter view from the front side; a slow drift; pulls back for the blast cone; far back on `trapped`
    const jv = sm(0, 2, e) * (1 - sm(6, 9, e)), d0 = 36 * VF * (1 + .4 * jv) + 10 * sm(0, 1.5, bt) * (1 - tr), D = d0 * (1 + 7.5 * tr), az = .62 + u * .004 - .25 * tr, el = .22 + .12 * tr;
    cam.position.set(Math.sin(az) * Math.cos(el) * D, Math.sin(el) * D, Math.cos(az) * Math.cos(el) * D);
    tgt.set(2 + 3 * sm(0, 1.5, bt) * (1 - tr), 0, 0); cam.lookAt(tgt); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
    U.uCam.value.copy(cam.position); U.uPInv.value.copy(cam.projectionMatrixInverse); U.uCW.value.copy(cam.matrixWorld);
  } };
};
