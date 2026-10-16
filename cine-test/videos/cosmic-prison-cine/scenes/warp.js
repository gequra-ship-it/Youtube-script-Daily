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
// speed pass (2026-10-16): when `warp` engages, hyperspace star streaks rush past around the bubble: an endless recycling stream whose
// speed (and streak length) climbs in two stages over ~18 s, so the jump past light speed is felt; they thin out while the snowplow
// glows, decelerate to dots and fade on `blast`, and are gone in the `trapped` wide view.
// gravity escape (2026-10-16): before `warp` the ship hangs low in a planet's gravity well: a spacetime grid sheet with a deep dent
// where a rim-lit ocean planet rests, the sheet rising behind the ship. From ~1.8 s before the cue the ship climbs (nose up) and the
// sheet under it is pulled up into a straining peak (glowing warm); on release it snaps back, a ripple wave runs out across the sheet
// and a soft flash rises (0.2 s) and fades (~1.5 s); the planet and its well fall away below and behind (accelerating, slingshot),
// lensed by the forming bubble, and are gone ~7 s after the release, long before `energy` / `snowplow`.
// aftermath pass (2026-10-16), all after `blast` and only when the shot runs long enough after it: the camera swings round to look
// past the drifting, slowly tumbling ship (engines dim) at a destination planet ahead; the blast's radiation front (a forward shell)
// sweeps over it: its facing side flares, a flash rises and fades, its atmosphere is torn off downstream. Then a looming barrier,
// the 'stone wall' (a vast slate surface with faint cells), fades in beyond it while the camera pushes slowly toward it; each
// escape route is a bolt of light fired from the ship that strikes the wall and spreads a ripple ring; on `voice` the whole wall
// pulses once; on `trapped` it fades and the existing wide view takes over.
//   wall      the first bolt hits the wall (default blast + 10.6 s; the wall needs it >= 3 s before the shot end)
//   hits      list of cues for further bolts (default: three spread between `wall` and `trapped` / shot end)
//   voice     the whole wall pulses (default trapped - 0.5 s)
//   escape    the release moment (default: the warp cue + 1.2 s); escape: false turns the gravity well off. Needs `warp`.
(window.MIYA = window.MIYA || { scenes: {} }).scenes.warp = function (ctx, p) {
  const { T, sm, rng, cue, points, glow } = ctx, Rr = ctx.R, K = window.MIYA.kit, E = ctx.env();
  const v3 = (x, y, z) => new T.Vector3(x, y, z);
  const cu = c => c == null ? null : cue(c);
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), ctx.t);

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
    uPInv: { value: new T.Matrix4() }, uCW: { value: new T.Matrix4() }, uF: { value: FWD.clone() }, uB2: { value: 60 }, uB2a: { value: 0 },
    uPC: { value: v3(0, -1e4, 0) }, uPR: { value: 1 }, uWA: { value: 0 }, uWT: { value: 0 }, uWX: { value: 1e4 }, uWC: { value: v3(0, 0, 0) }, uWH: { value: [0, 1, 2, 3, 4, 5].map(() => new T.Vector4(0, 0, -1e4, 0)) }, uWP: { value: v3(0, -1e4, 0) }, uPA: { value: 0 }, uPT: { value: 0 }, uPM: { value: null }, uSun: { value: v3(-.62, .5, -.6).normalize() } };
  // well planet albedo (equirect, baked once): ocean, land, cloud
  U.uPM.value = (() => { const PW = 512, PH = 256, c = document.createElement('canvas'); c.width = PW; c.height = PH; const g = c.getContext('2d'), im = g.createImageData(PW, PH), D = im.data;
    const mx = (a, b, k) => a.map((v, i) => v + (b[i] - v) * k);
    for (let y = 0; y < PH; y++) { const la = ((y + .5) / PH - .5) * Math.PI, cy = Math.sin(la), cr = Math.cos(la);
      for (let x = 0; x < PW; x++) { const lo = ((x + .5) / PW - .5) * 6.2832, qx = Math.cos(lo) * cr, qz = Math.sin(lo) * cr, k = ((PH - 1 - y) * PW + x) * 4;
        const ld = fbm(qx * 3.1 + 5, cy * 3.1, qz * 3.1, 3), cl = fbm(qx * 5.2, cy * 5.2 + 3, qz * 5.2, 4);
        let a = mx([.025, .07, .16], [.16, .15, .1], sm(.5, .56, ld)); a = mx(a, [.6, .65, .72], sm(.5, .74, cl) * .8);
        for (let j = 0; j < 3; j++) D[k + j] = Math.min(255, Math.pow(a[j], 1 / 2.2) * 255); D[k + 3] = 255; } }
    g.putImageData(im, 0, 0); const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; t.wrapS = T.RepeatWrapping; return t; })();
  const lensP = { uniforms: U, depthWrite: false, depthTest: false,
    vertexShader: `uniform mat4 uPInv, uCW; uniform vec3 uCam, uWC, uWP; uniform float uWA, uWT, uWX; uniform vec4 uWH[6]; varying vec2 vUv, vWr;
      void ring(vec2 p, vec2 c, float r, float amp, float k, float w, inout float h, inout vec2 g){ vec2 q = p - c; float d = max(length(q), 1e-3), x = d - r, en = exp(-x * x / (w * w));
        float s = sin(x * k), co = cos(x * k); h += amp * s * en; g += amp * en * (k * co - 2. * x / (w * w) * s) * q / d; }
      void main(){ vUv = uv; gl_Position = vec4(position.xy, 0., 1.); vWr = vec2(0.);
        if (uWA > 0.) { vec4 pv = uPInv * vec4(uv * 2. - 1., 1., 1.); pv /= pv.w; vec3 d = normalize((uCW * vec4(pv.xyz, 0.)).xyz);
          if (d.x > 1e-4) { vec3 P = uCam + d * ((uWX - uCam.x) / d.x); vec2 p = vec2(P.z - uWC.z, P.y - uWC.y); float h = 0.; vec2 g = vec2(0.);
            for (int k = 0; k < 6; k++) { vec4 q = uWH[k]; float a = uWT - q.z; if (a > 0. && a < 13. && q.w > 0.) ring(p, q.xy, a * 34., q.w * exp(-a * .45) * smoothstep(0., .4, a), .35, 14., h, g); }
            float pa = uWT - uWP.x; if (pa > 0. && pa < 10. && uWP.z > 0.) ring(p, vec2(0.), pa * 70., 1.4 * exp(-pa * .5) * smoothstep(0., .5, pa), .2, 30., h, g);
            vWr = vec2(h, dot(g, vec2(-.6, .8))); } } }`,
    fragmentShader: `uniform samplerCube tO; uniform sampler2D uPM; uniform float uWA, uWT, uWX; uniform vec3 uWC, uWP; uniform vec4 uWH[6]; uniform vec3 uC, uCam, uF, uPC, uSun; uniform float uR, uW, uRim, uB2, uB2a, uPR, uPA, uPT; uniform mat4 uPInv, uCW; varying vec2 vUv;
      // the gravity-well planet (ray from ro along rd, over background bg): ocean + land + cloud, lit from behind (crescent), blue air limb
      vec3 planet(vec3 ro, vec3 rd, vec3 bg){
        #ifndef PLANET
        return bg;
        #else
        if (uPA <= 0.) return bg;
        vec3 oc = uPC - ro; float tc = dot(oc, rd); if (tc <= 0.) return bg;
        float b2 = dot(oc, oc) - tc * tc, R2 = uPR * uPR; if (b2 > R2 * 1.45) return bg; float bb = sqrt(max(b2, 0.)) / uPR; vec3 col = bg;
        if (b2 < R2) { vec3 n = normalize(ro + rd * (tc - sqrt(R2 - b2)) - uPC), q = vec3(n.x * cos(uPT) - n.z * sin(uPT), n.y, n.x * sin(uPT) + n.z * cos(uPT));
          vec3 alb = texture2D(uPM, vec2(atan(q.z, q.x) * .1591549 + .5, asin(clamp(q.y, -1., 1.)) * .3183099 + .5)).rgb;
          float l = dot(n, uSun), fr = pow(1. - max(0., dot(n, -rd)), 2.5);
          vec3 pc = alb * (max(0., l) * 1.5 + .025) + fr * vec3(.25, .45, 1.) * (.06 + .75 * smoothstep(-.25, .6, l));
          col = mix(bg, pc, uPA); }
        vec3 nd = normalize(ro + rd * tc - uPC);
        col += uPA * exp(-abs(bb - 1.) * (bb > 1. ? 22. : 60.)) * vec3(.35, .55, 1.) * (.04 + .5 * smoothstep(-.3, .7, dot(nd, uSun)));
        return col;
        #endif
      }
      // the stone wall: plane x = uWX; ripples come per vertex (grid lens quad), the hex blocks per pixel
      varying vec2 vWr;
      // returns colour + coverage; where the wall is fully opaque the sky lookups are skipped (they cost the most here)
      vec4 wall(vec3 ro, vec3 rd){
        if (uWA <= 0. || rd.x <= 1e-4) return vec4(0.); float tt = (uWX - ro.x) / rd.x; if (tt <= 0.) return vec4(0.);
        vec3 P = ro + rd * tt; vec2 p = vec2(P.z - uWC.z, P.y - uWC.y); float fall = smoothstep(460., 230., length(p * vec2(.75, 1.))); if (fall <= 0.) return vec4(0.);
        float h = vWr.x, sh = vWr.y;
        // basalt-like hex blocks (cheap arithmetic; a texture lookup here cost ~0.4 s/frame on the software renderer)
        vec2 hp = p / 22., hs2 = vec2(1., 1.7320508), ha = mod(hp, hs2) - hs2 * .5, hb = mod(hp - hs2 * .5, hs2) - hs2 * .5, gv = dot(ha, ha) < dot(hb, hb) ? ha : hb;
        float hd = max(dot(abs(gv), vec2(.5, .8660254)), abs(gv.x)), lines = smoothstep(.43, .5, hd), grain = .55 + .45 * fract(sin(dot(hp - gv, vec2(12.9898, 78.233))) * 43758.5453);
        vec3 col = vec3(.035, .034, .048) * grain + vec3(.1, .09, .13) * lines * .35 + vec3(.55, .6, 1.) * max(0., sh) * 2.6 + vec3(1., .8, .55) * abs(h) * .08 + vec3(.5, .55, .9) * lines * abs(h) * .25;
        return vec4(col, uWA * fall); }
      void main(){
        vec4 pv = uPInv * vec4(vUv * 2. - 1., 1., 1.); pv /= pv.w;
        vec3 d = normalize((uCW * vec4(pv.xyz, 0.)).xyz), oc = uC - uCam;
        float tca = dot(oc, d), b2 = dot(oc, oc) - tca * tca, R2 = uR * uR;
        vec4 wv = wall(uCam, d); vec3 col = wv.rgb;
        if (wv.a < .999) { col = planet(uCam, d, textureCube(tO, d).rgb);
        if (tca > 0. && b2 < R2 && uW > 0.) {
          float th = sqrt(R2 - b2); vec3 P = uCam + d * (tca - th), n = (P - uC) / uR;
          float z = dot(n, uF), edge = sqrt(b2) / uR, fall = 1. - smoothstep(.75, 1., edge);
          // f(z) = z + s z^2: compressed ahead (stars bunch), expanded behind (stars stretch)
          float s = 1.3 * uW * fall;
          vec3 dd = normalize(d + uF * s * .55 * z * abs(z) + uF * s * .25 * z);
          if (z < 0.) { vec3 acc = vec3(0.); for (int j = 0; j < 7; j++) acc += textureCube(tO, normalize(dd + uF * (float(j) / 6. - .5) * .16 * (-z) * s)).rgb; col = planet(uCam, d, acc / 7. * 1.6); }
          else col = planet(uCam, d, textureCube(tO, dd).rgb * (1. + .8 * z * s));
          // Doppler-like tint: blue ahead, red behind
          col *= mix(vec3(1.), z > 0. ? vec3(.8, .95, 1.35) : vec3(1.3, .85, .7), abs(z) * s);
          // bubble wall: faint fresnel rim
          col += uRim * uW * (pow(edge, 16.) * .07 + exp(-pow((edge - 1.) / .012, 2.)) * .22) * vec3(.75, .82, 1.);
        }
        col = mix(col, wv.rgb, wv.a); }
        // dark boundary sphere ("our local cosmic cell") in the trapped view: faint gold limb
        float B = uB2; if (uB2a > 0. && tca > 0.) { float bb = sqrt(max(0., dot(oc, oc) - tca * tca)) / B;
          if (bb < 1.) col = col * mix(1., .22, uB2a) + uB2a * pow(bb, 40.) * .12 * vec3(1., .8, .5);
          col += uB2a * exp(-pow((bb - 1.) / .004, 2.)) * .3 * vec3(1., .8, .5); }
        gl_FragColor = vec4(col, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` };
  // two builds of the lens: with the gravity-well planet (only while it is visible) and without it (cheaper)
  const lensM0 = new T.ShaderMaterial(lensP), lensM1 = new T.ShaderMaterial(Object.assign({ defines: { PLANET: 1 } }, lensP));
  const lens = new T.Mesh(new T.PlaneGeometry(2, 2, 96, 54), lensM0);
  lens.frustumCulled = false; lens.renderOrder = -10; S.add(lens);
  // the lens follows the camera actually rendered (after the camera director's move), so sky, planet and meshes line up
  lens.onBeforeRender = (r, sc, c) => { c.updateMatrixWorld(); U.uCam.value.setFromMatrixPosition(c.matrixWorld); U.uPInv.value.copy(c.projectionMatrixInverse); U.uCW.value.copy(c.matrixWorld); };

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

  // hyperspace streaks: particle k sits on a cylinder (radius rho, angle a) and recycles along x: s = fract(Fh(t) / LX + f_k)
  const NH = 700, hyp = streaks(S, NH, { minPx: 1.5, near: [8, 24] }), hB = [], HX1 = 260, LX = 430;
  { const r = rng(77); for (let i = 0; i < NH; i++) { const rho = 11 + 64 * Math.pow(r(), 1.35), a = r() * 6.283, tp = r(), br = .45 + .75 * Math.pow(r(), 1.5);
    const col = tp < .7 ? [.72, .84, 1] : tp < .9 ? [.72, .6, 1] : [1, .8, .5]; hB.push({ y: Math.cos(a) * rho, z: Math.sin(a) * rho, f: r(), c: col.map(x => x * br) }); } }
  // speed profile: D(t) = integral of v (analytic), seek-safe
  const IS = (a, b, t) => t <= a ? 0 : t >= b ? (b - a) * .5 + (t - b) : (b - a) * (Math.pow((t - a) / (b - a), 3) - Math.pow((t - a) / (b - a), 4) / 2);
  const cW = cu(p.warp), cS = cu(p.snowplow), cB = cu(p.blast), cE = cu(p.energy), cT = cu(p.trapped);
  const V0 = 2.5, V = 34;
  const HA = 110, HB = 210, cB0 = cB == null ? 1e9 : cB;
  const Fh = t => cW == null ? (HA + HB) * t : HA * IS(cW, cW + 4, t) + HB * IS(cW + 3, cW + 18, t) - (HA + HB) * IS(cB0 - .25, cB0 + .6, t);
  const Vh = t => cW == null ? (HA + HB) * (1 - sm(cB0 - .25, cB0 + .6, t)) : Math.max(0, HA * sm(cW, cW + 4, t) + HB * sm(cW + 3, cW + 18, t) - (HA + HB) * sm(cB0 - .25, cB0 + .6, t));
  const Dd = t => V0 * t + (V - V0) * (cW == null ? t : IS(cW, cW + 3, t)) - (cB == null ? 0 : (V) * IS(cB - .25, cB + .35, t));

  // ---------------- gravity escape: spacetime grid sheet (line segments, height a pure function of t) + well planet (in the lens) ----
  // sheet height around the well centre (local r): Y0 - A a / sqrt(r^2 + a^2); a straining peak under the ship before the release,
  // a ripple ring from the ship's point after it. Lines hidden behind the planet are discarded in the shader (ray-sphere test).
  const GW = p.escape !== false && p.escape !== 0 && cW != null, tR = GW ? (p.escape != null && p.escape !== true ? cue(p.escape) : cW + 1.2) : 1e9, tC0 = tR - 3;
  const WC = v3(-15, ctx.VERT ? -14 : -3, -26.4), GF = ctx.VERT ? 40 : 50, Y0 = 10, WA = 25.5, Wa = 16, PR = 6.5, GL = 62, GS = 4, GN = Math.round(2 * GL / GS) + 1, GD = 1.5, GM = Math.round(2 * GL / GD) + 1;
  const wh = r => Y0 - WA * Wa / Math.sqrt(r * r + Wa * Wa);
  const SL = v3(0, 0, 0).sub(WC), PL = v3(0, wh(0) + PR - 1.5, 0);
  let grid = null, gPos, gCol, gXZ;
  if (GW) { const nv = GN * GM * 2, ix = []; gPos = new Float32Array(nv * 3); gCol = new Float32Array(nv * 3); gXZ = new Float32Array(nv * 2); let k = 0;
    for (let dir = 0; dir < 2; dir++) for (let i = 0; i < GN; i++) { const a = -GL + i * GS;
      for (let j = 0; j < GM; j++) { const b = -GL + j * GD; gXZ[k * 2] = dir ? b : a; gXZ[k * 2 + 1] = dir ? a : b; if (j && a * a + b * b <= GL * GL && a * a + (b - GD) * (b - GD) <= GL * GL) ix.push(k - 1, k); k++; } }
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(gPos, 3).setUsage(T.DynamicDrawUsage)); g.setAttribute('color', new T.BufferAttribute(gCol, 3).setUsage(T.DynamicDrawUsage)); g.setIndex(ix);
    const gm = new T.ShaderMaterial({ uniforms: { uPC: U.uPC, uPR: U.uPR }, transparent: true, depthWrite: false, blending: T.AdditiveBlending,
      vertexShader: 'attribute vec3 color; varying vec3 vC, vW; void main(){ vC = color; vW = (modelMatrix * vec4(position, 1.)).xyz; gl_Position = projectionMatrix * viewMatrix * vec4(vW, 1.); }',
      fragmentShader: `uniform vec3 uPC; uniform float uPR; varying vec3 vC, vW;
        void main(){ vec3 rd = vW - cameraPosition; float L = length(rd); rd /= L; vec3 oc = uPC - cameraPosition; float tc = dot(oc, rd), b2 = dot(oc, oc) - tc * tc;
          if (b2 < uPR * uPR && tc - sqrt(uPR * uPR - b2) < L - .3) discard;
          gl_FragColor = vec4(vC * smoothstep(6., 22., L) * smoothstep(92., 66., L), 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` });
    grid = new T.LineSegments(g, gm); grid.frustumCulled = false; grid.renderOrder = -5; S.add(grid); }
  const escG = glow(S, '#fff0d6', 46, 0), escG2 = glow(S, '#ffc65a', 10, 0);
  // ---------------- aftermath (2026-10-16): destination planet, radiation front, stone wall + escape bolts ----------------
  const tW0 = p.wall != null ? cue(p.wall) : (cB == null ? 1e9 : cB + 10.6), tEnd = cT != null && cT < ctx.t1 ? cT : ctx.t1;
  const AF = cB != null && cB + 7 < ctx.t1, WL = AF && tW0 + 3 < ctx.t1;
  const tHits = WL ? [tW0].concat(p.hits != null ? [].concat(p.hits).map(c => cue(c)) : [0, 1, 2].map(k => tW0 + (tEnd - 1.5 - tW0) * (k + 1) / 3.4)) : [];
  const tVo = p.voice != null ? cue(p.voice) : tEnd - .5;
  const PP = v3(78, 7, -30), PRD = 8, XW = 165, WCn = v3(XW, 0, -20);
  const dstT = ctx.ctex(256, (g, sz) => { const im = g.createImageData(sz, sz); for (let y = 0; y < sz; y++) for (let x = 0; x < sz; x++) { const ph = x / sz * 6.2832, n = fbm(Math.cos(ph) * 2 + 4, y / sz * 5, Math.sin(ph) * 2, 4), k = (y * sz + x) * 4, sea = n < .5;
      const c = sea ? [30, 52, 92] : [120 + 90 * (n - .5), 96 + 60 * (n - .5), 70]; for (let j = 0; j < 3; j++) im.data[k + j] = c[j] * (.8 + .4 * n); im.data[k + 3] = 255; } g.putImageData(im, 0, 0); });
  const dstM = new T.MeshStandardMaterial({ map: dstT, roughness: .85, metalness: 0, emissive: '#ff9a50', emissiveIntensity: 0 });
  const DST = new T.Mesh(new T.SphereGeometry(PRD, 64, 32), dstM); DST.position.copy(PP); DST.visible = false; S.add(DST);
  const hotM = new T.ShaderMaterial({ uniforms: { uI: { value: 0 }, uD: { value: v3(-1, 0, 0) } }, transparent: true, depthWrite: false, blending: T.AdditiveBlending,
    vertexShader: 'varying vec3 vN, vV; void main(){ vN = normalize(mat3(modelMatrix) * normal); vec4 w = modelMatrix * vec4(position, 1.); vV = normalize(cameraPosition - w.xyz); gl_Position = projectionMatrix * viewMatrix * w; }',
    fragmentShader: `uniform float uI; uniform vec3 uD; varying vec3 vN, vV;
      void main(){ float f = max(0., dot(normalize(vN), uD)), rim = pow(1. - abs(dot(normalize(vN), normalize(vV))), 2.);
        gl_FragColor = vec4(vec3(1., .62, .3) * uI * (pow(f, 1.5) * .9 + rim * .5 * (.3 + f)), 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` });
  const HOT = new T.Mesh(new T.SphereGeometry(PRD * 1.06, 48, 24), hotM); HOT.position.copy(PP); HOT.visible = false; S.add(HOT);
  const dstG = glow(S, '#ffe0b0', 34, 0); dstG.position.copy(PP); dstG.visible = false;
  const NA = 1400, atm = points(NA, { size: .45, opacity: 1, color: '#ffd8a8' }), aA = atm.geometry.attributes.position.array, aC = atm.geometry.attributes.color.array, aB = [];
  { const r = rng(123); for (let i = 0; i < NA; i++) { let x, y, z; do { x = r() * 2 - 1; y = r() * 2 - 1; z = r() * 2 - 1; } while (x * x + y * y + z * z > 1 || x > .1); const l = Math.hypot(x, y, z) || 1; aB.push([x / l, y / l, z / l, .5 + r(), r() * .6, r()]); } }
  atm.frustumCulled = false; atm.visible = false; S.add(atm);
  // radiation front: forward half-shell growing from the bubble's nose
  const frM = new T.ShaderMaterial({ uniforms: { uO: { value: 0 } }, transparent: true, depthWrite: false, blending: T.AdditiveBlending, side: T.DoubleSide,
    vertexShader: 'varying vec3 vN, vV, vL; void main(){ vL = normal; vN = normalize(mat3(modelMatrix) * normal); vec4 w = modelMatrix * vec4(position, 1.); vV = normalize(cameraPosition - w.xyz); gl_Position = projectionMatrix * viewMatrix * w; }',
    fragmentShader: `uniform float uO; varying vec3 vN, vV, vL;
      void main(){ float rim = pow(1. - abs(dot(normalize(vN), normalize(vV))), 3.), fw = smoothstep(.15, .75, vL.x);
        gl_FragColor = vec4(vec3(1., .78, .5) * uO * fw * (rim * .9 + .05), 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` });
  const FRONT = new T.Mesh(new T.SphereGeometry(1, 64, 32), frM); FRONT.position.set(RB, 0, 0); FRONT.visible = false; S.add(FRONT);
  // the stone wall: a vast plane facing the ship, cells + grain, ripple rings from the bolt impacts, one global pulse
  const NHT = 6, hitV = U.uWH.value;
  // the wall is drawn inside the full-screen lens pass (ray-plane hit at x = XW), so it adds no extra full-screen layer
  U.uWX.value = XW; U.uWC.value.copy(WCn);
  const bolts = streaks(S, NHT, { minPx: 2.4, near: [4, 12] }); bolts.mesh.visible = false;
  const hitG = []; for (let k = 0; k < NHT; k++) { const g = glow(S, '#dfe6ff', 30, 0); g.visible = false; hitG.push(g); }
  const hitP = tHits.map((_, k) => { const a = k * 2.4 + .7, r = k ? 45 + 25 * (k % 2) : 0; return [Math.cos(a) * r, Math.sin(a) * r * .8 + (k ? 0 : 6)]; });
  const camA = v3(0, 0, 0), camB = v3(0, 0, 0), tgA = v3(0, 0, 0), tgB = v3(0, 0, 0), tq = v3(0, 0, 0);
  const cam = new T.PerspectiveCamera(38, ctx.W / ctx.H, .1, 4000); ctx.side(cam, p.side == null ? .12 : p.side);
  const VF = ctx.VERT ? 1.2 : 1, tgt = v3(0, 0, 0);
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const w0 = cW == null ? 1 : sm(cW, cW + 2.5, t), stop = cB == null ? 0 : sm(cB - .1, cB + .5, t), w = w0 * (1 - stop);
    const tr = at(p.trapped, 6), tc = cT == null ? 1e9 : cT;
    U.uW.value = w; U.uRim.value = 1; eqM.opacity = .1 * w; ringGlowM.opacity = .25 + .55 * w;
    goldM.emissiveIntensity = .2 + .5 * w;
    glows.forEach((g, i) => g.material.opacity = (.35 + .4 * w0) * (i === 2 ? 1 : .8) * (cB == null || !(cB + 7 < ctx.t1) ? 1 : 1 - .75 * sm(cB + .5, cB + 3, t) * (1 - .3 * Math.max(0, Math.sin((t - cB) * 2.1 + i)))));
    SHIP.position.set(0, Math.sin(u * .4) * .12, 0); SHIP.rotation.set(Math.sin(u * .3) * .02, 0, Math.sin(u * .23) * .015);
    // aftermath: the stopped ship drifts helpless, slowly tumbling (pure function of the time since the blast)
    const ab = AF ? Math.max(0, t - cB - .6) : 0, drift = AF ? sm(cB + .3, cB + 4, t) : 0;
    if (AF) { SHIP.rotation.x += drift * (.045 * ab + .05 * Math.sin(ab * .35)); SHIP.rotation.z += drift * (-.012 * ab + .04 * Math.sin(ab * .27)); SHIP.position.y -= drift * .06 * ab; }
    // gravity escape: climb (the well drops away under the ship), strain peak, release ripple, slingshot fall, flash
    const gA = GW ? 1 - sm(tR + 3, tR + 7, t) : 0;
    if (GW) { const climb = sm(tC0, tR + .4, t), rel = sm(tR, tR + .35, t), tau = t - tR;
      SHIP.rotation.z += .09 * sm(tC0, tR, t) * (1 - sm(tR, tR + 2.5, t)); glows.forEach(g => g.material.opacity += .35 * climb * (1 - rel));
      const ox = -36 * IS(tR, tR + 3.5, t), oy = -7 * climb - 55 * IS(tR, tR + 3.5, t), oz = -10 * IS(tR, tR + 3.5, t);
      const cx = WC.x + ox, cy = WC.y + oy, cz = WC.z + oz;
      U.uPC.value.set(cx + PL.x, cy + PL.y, cz + PL.z); U.uPR.value = PR; U.uPA.value = gA; lens.material = gA > 0 ? lensM1 : lensM0; U.uPT.value = t * .02 + .03 * IS(tR, tR + 3, t);
      if (grid) { grid.visible = gA > 0;
        if (gA > 0) { const sx = SL.x - ox, sz = SL.z - oz, sy = SL.y - oy, rsh = Math.hypot(sx, sz), hs0 = wh(rsh), st = Math.max(0, sy - 4.2 - hs0) * Math.min(1, climb * 2) * (1 - rel),
            sg2 = Math.pow(5.5 - 2 * climb * (1 - rel), 2), front = 24 * Math.max(0, tau), ramp = tau > 0 ? sm(0, .25, tau) * Math.exp(-tau / 2.4) : 0;
          for (let k = 0, n = gXZ.length / 2; k < n; k++) { const x = gXZ[k * 2], z = gXZ[k * 2 + 1], r = Math.sqrt(x * x + z * z); if (r > GL + 1) continue;
            const dx = x - sx, dz = z - sz, q2 = dx * dx + dz * dz, pk = st > 0 && q2 < 9 * sg2 ? st * Math.exp(-q2 / sg2) : 0, ex = x - SL.x, ez = z - SL.z, dq = Math.sqrt(ex * ex + ez * ez) - front;
            const rip = ramp > 0 && dq * dq < 400 ? ramp * 1.6 * Math.sin(dq * .55) * Math.exp(-dq * dq / 60) : 0, br = .15 * Math.sin(r * .35 - t * 1.4) * Math.exp(-r / 30);
            const gy = cy + wh(r) + pk + rip + br; gPos[k * 3] = cx + x; gPos[k * 3 + 1] = gy; gPos[k * 3 + 2] = cz + z;
            const fo = Math.exp(-Math.pow(r / GF, 2)) * gA * (1 - sm(WC.y + 2 + oy, WC.y + 7 + oy, gy - pk)), hot = Math.min(1, pk / 6) + Math.min(1, Math.abs(rip) * .8), v = .16 * fo * (1 + 3.2 * hot);
            gCol[k * 3] = v * (.55 + .6 * hot); gCol[k * 3 + 1] = v * (.62 + .25 * hot); gCol[k * 3 + 2] = v * (1.1 - .55 * hot); }
          grid.geometry.attributes.position.needsUpdate = true; grid.geometry.attributes.color.needsUpdate = true; } }
      const fl = tau > 0 ? sm(0, .2, tau) * Math.exp(-Math.max(0, tau - .2) / 1.1) : 0;
      escG.material.opacity = .4 * fl; escG.position.set(1, -1, 0); escG.scale.setScalar(17 + 6 * sm(0, 1.5, tau)); escG2.material.opacity = .5 * fl + .1 * climb * (1 - rel); escG2.position.set(-3.4, 0, 0);
      escG.visible = fl > 0; escG2.visible = escG2.material.opacity > 0;
    } else { U.uPA.value = 0; lens.material = lensM0; escG.visible = escG2.visible = false; if (grid) grid.visible = false; }
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
    // hyperspace streaks: envelope rises with the bubble, thins while the snowplow glows, fades after the stop and in the trapped view
    { const env = (cW == null ? 1 : sm(cW + .2, cW + 1.8, t)) * (1 - .45 * heat) * (1 - stop * sm(cB0, cB0 + 1.2, t)) * (1 - tr), vh = Vh(t), F = Fh(t) / LX, hl = Math.min(34, vh * .09), gain = env * (.55 + .45 * sm(0, 200, vh));
      for (let i = 0; i < NH; i++) { const h = hB[i]; if (gain <= 0) { hyp.hide(i); continue; } const ss = ((F + h.f) % 1 + 1) % 1, x = HX1 - ss * LX, k = gain * sm(0, .12, ss) * sm(1, .8, ss);
        hyp.set(i, x, h.y, h.z, x + hl, h.y, h.z, .12, h.c[0] * k, h.c[1] * k, h.c[2] * k); }
      hyp.commit(); hyp.mesh.visible = gain > 0; }
    const capOn = heat * (bt > 0 ? Math.exp(-bt * 2) : 1) * (1 - tr);
    capG.material.opacity = .55 * capOn; capG.material.color.setRGB(1, .6 + .35 * heat, .35 + .6 * heat * heat); capG.scale.setScalar(8 + 10 * heat);
    du.material.size = .28 * (1 + 2.5 * tr);
    // blast flash: rises in .15 s, fades over ~2 s
    const fl = bt > 0 ? sm(0, .15, bt) * Math.exp(-Math.max(0, bt - .15) * 1.5) : 0;
    coneM.uniforms.opacity.value = .9 * fl; cone.scale.set(.6 + .6 * sm(0, 1.5, bt), 1, 1); blastG.material.opacity = .4 * fl; blastG2.material.opacity = .18 * fl;
    // trapped: wide calm view, dark boundary sphere, the ship a tiny light
    U.uB2a.value = tr; U.uB2.value = 70; shipG.material.opacity = .8 * tr;
    // aftermath: radiation front, destination planet hit, stone wall, bolts
    const tHit = AF ? cB + 4.8 : 1e9, hz = t - tHit;
    { const fo = AF ? sm(-.1, .3, bt) * (1 - sm(5.4, 8, bt)) : 0; FRONT.visible = fo > 0; if (fo > 0) { FRONT.scale.setScalar(4 + 12.6 * Math.max(0, bt) + 1.2 * bt * bt * .1); frM.uniforms.uO.value = .55 * fo; } }
    const dv = AF ? sm(cB + .8, cB + 3.2, t) * (1 - tr) : 0; DST.visible = HOT.visible = dv > 0; DST.rotation.y = t * .03;
    if (dv > 0) { const hi = hz > 0 ? sm(0, .3, hz) * (.12 + .88 * Math.exp(-hz / 2)) : 0; hotM.uniforms.uI.value = .75 * hi * dv; dstM.emissiveIntensity = .22 * hi; dstM.opacity = 1;
      DST.scale.setScalar(dv); HOT.scale.setScalar(dv); const fl2 = hz > 0 ? sm(0, .2, hz) * Math.exp(-Math.max(0, hz - .2) / 1.2) : 0; dstG.visible = fl2 > 0; dstG.material.opacity = .5 * fl2; dstG.scale.setScalar(26 + 20 * sm(0, 1.5, hz)); }
    else dstG.visible = false;
    atm.visible = dv > 0 && hz > 0;
    if (atm.visible) { for (let i = 0; i < NA; i++) { const b = aB[i], tl = Math.max(0, hz - b[4]), d = tl * (5 + 9 * b[3]) * (1 - .25 * Math.min(1, tl / 8)), sp = 1 + tl * .12;
        aA[i * 3] = PP.x + b[0] * PRD * 1.04 * sp + d; aA[i * 3 + 1] = PP.y + b[1] * PRD * 1.04 * sp + d * .08 * (b[5] - .5); aA[i * 3 + 2] = PP.z + b[2] * PRD * 1.04 * sp + d * .1 * (b[5] - .5);
        const v = dv * sm(0, .3, tl) * Math.exp(-tl / (3 + 3 * b[5])) * (.6 + .6 * b[3]); aC[i * 3] = v; aC[i * 3 + 1] = v * .7; aC[i * 3 + 2] = v * .45; }
      atm.geometry.attributes.position.needsUpdate = true; atm.geometry.attributes.color.needsUpdate = true; }
    const wa = WL ? sm(tW0 - 3.5, tW0 - .6, t) * (1 - tr) : 0; U.uWA.value = wa; U.uWT.value = t;
    bolts.mesh.visible = false;
    for (let k = 0; k < NHT; k++) { const th = tHits[k], hg = hitG[k];
      if (!WL || th == null) { hitV[k].set(0, 0, -1e4, 0); hg.visible = false; bolts.hide(k); continue; }
      const [py, pz] = hitP[k]; hitV[k].set(-pz, py, th, k ? .8 : 1.1);
      const tb = t - (th - 1.1), sx = 4, ex = XW - .5; if (tb > 0 && tb < 1.1 + .4 && wa > 0) { bolts.mesh.visible = true;
        const hpos = Math.min(1, Math.pow(tb / 1.1, 1.6)), tpos = Math.max(0, Math.pow(Math.max(0, tb - .25) / 1.1, 1.6)), hx = sx + (ex - sx) * hpos, tx = sx + (ex - sx) * Math.min(1, tpos), k2 = sm(0, .15, tb) * (1 - sm(1.1, 1.5, tb)) * 1.6;
        const Y = q => q * py, Z = q => WCn.z * q + q * (-pz);
        bolts.set(k, hx, Y(hpos), Z(hpos), tx, Y(Math.min(1, tpos)), Z(Math.min(1, tpos)), .5, .85 * k2, .9 * k2, 1.2 * k2); } else bolts.hide(k);
      const ha = t - th, hf = ha > 0 ? sm(0, .15, ha) * Math.exp(-Math.max(0, ha - .15) / 1.1) : 0; hg.visible = hf > 0 && wa > 0; hg.material.opacity = .55 * hf * wa; hg.position.set(XW - 1, py, WCn.z - pz); hg.scale.setScalar(26 + 30 * sm(0, 1.2, ha)); }
    bolts.commit(); U.uWP.value.set(tVo, 0, WL ? 1 : 0);
    // camera: three-quarter view from the front side; a slow drift; pulls back for the blast cone; far back on `trapped`
    const jv = sm(0, 2, e) * (1 - sm(6, 9, e)), d0 = 36 * VF * (1 + .4 * jv) + 10 * sm(0, 1.5, bt) * (1 - tr), D = d0 * (1 + 7.5 * tr), az = .62 + u * .004 - .25 * tr, el = .22 + .12 * tr;
    cam.position.set(Math.sin(az) * Math.cos(el) * D, Math.sin(el) * D, Math.cos(az) * Math.cos(el) * D);
    tgt.set(2 + 3 * sm(0, 1.5, bt) * (1 - tr), 0, 0);
    // aftermath camera: swing round behind the ship to look at the planet and the wall, then push slowly toward the wall
    if (AF) { const kb = sm(cB + 1.2, cB + 5.5, t) * (1 - tr), tau = Math.max(0, t - cB - 1.2), pw = WL ? IS(tW0 - 3, tW0 + 4, t) : 0;
      if (kb > 0) { camB.set(-38 * VF + .3 * tau + 1.1 * pw, 9 + .05 * tau, 34 * VF - .2 * tau - .25 * pw); tgB.set((ctx.VERT ? 20 : 36) + .5 * tau + 1.2 * pw, 0, -10);
        camA.copy(cam.position); tgA.copy(tgt); const kk = kb * kb * (3 - 2 * kb);
        const dl = (camA.length() * (1 - kk) + camB.length() * kk) * (1 + .22 * Math.sin(Math.PI * kk)); cam.position.lerpVectors(camA, camB, kk).setLength(dl); tgt.lerpVectors(tgA, tgB, kk); } }
    cam.lookAt(tgt); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
    U.uCam.value.copy(cam.position); U.uPInv.value.copy(cam.projectionMatrixInverse); U.uCW.value.copy(cam.matrixWorld);
  } };
};
