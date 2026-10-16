// observatory — a real night sky (Milky Way band with dust lanes and nebula glow, ~24k stars) over a dark hill with a solid 3D
// observatory: a thick drum with a door, a ribbed metal dome with a real slit (outer + inner shell + slit walls, glowing edges),
// a sliding shutter and a telescope inside. Starlight streams down into the slit. On "telescopes" the dome turns and the shutter
// opens fully; on "rockets" a rocket lifts off from the far plain on a glowing exhaust trail; the camera then tilts up after it into
// the void, and on "edge" pushes in toward the deep starfield (faint galaxies appear). Written for cosmic-prison-cine (2026-10-14).
// params (cues): { glow (slit light + starlight stream), widen (camera rises, wider sky), scope (dome turns, shutter opens),
//   rocket (lift-off), follow (camera tilts up after the rocket), edge (push into the deep field), side:.12,
//   close (optional, added 2026-10-15 for S47 "before dark energy closes the shutters": the shutter slides back down, a second
//          leaf stowed on the back comes over the top, the slit seals, the inner light and the starlight stream fade),
//   night (optional, added 2026-10-15 for the ending S53-S54: the camera slowly rises from the hill into the full star field,
//          faint galaxies show in the deep sky) }
// Without close/night the scene is unchanged (the second leaf is only built when close is given).
// 2026-10-16 staging pass (no new params): launch = ignition flash + anamorphic streak + shock ring on the ground, steam/smoke puffs
//   blasted sideways along the flame trench and billowing up (lit orange from below), a hot core streak behind the nozzle, a smooth
//   continuous contrail ribbon + swelling trail particles, a tiny smooth rumble of the look-at point, a faster follow (2.6 s), a max-Q
//   vapour halo; edge = 70 more faint galaxies emerging one by one and a slow creeping zoom to the shot end. Calm shots (close/night):
//   drifting airglow bands, stronger scintillation, scheduled slow meteors, a satellite fading into Earth's shadow, bokeh motes.
(window.MIYA = window.MIYA || { scenes: {} }).scenes.observatory = function (ctx, p) {
  const { T, sm, rng, cue, points, glow } = ctx, K = window.MIYA.kit, E = ctx.env();
  const S = new T.Scene(); S.background = new T.Color('#0f1128');
  const FOGC = new T.Color('#0d0d26'); S.fog = new T.FogExp2(FOGC, .0019);
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), ctx.t);
  const v3 = (x, y, z) => new T.Vector3(x, y, z);
  const h1 = k => { const s = Math.sin(k * 12.9898 + 4.1) * 43758.5453; return s - Math.floor(s); };
  const atT = (c, d, tt) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), tt);
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
  // continuous billboarded ribbon (the rocket's contrail): n sample points, each with position, tangent, width, colour; soft across
  // its width, never thinner than minPx pixels (dimmer instead). No per-segment fade, so it reads as one unbroken trail.
  function ribbon(par, n, o) { o = o || {}; const g = new T.BufferGeometry(), P = new Float32Array(n * 6), D = new Float32Array(n * 6), Wd = new Float32Array(n * 2), C = new Float32Array(n * 6), sd = new Float32Array(n * 2), ix = [];
    for (let i = 0; i < n; i++) { sd[i * 2] = -1; sd[i * 2 + 1] = 1; if (i < n - 1) { const a = i * 2; ix.push(a, a + 1, a + 2, a + 2, a + 1, a + 3); } }
    [['position', P, 3], ['aD', D, 3], ['aW', Wd, 1], ['aC', C, 3]].forEach(([k, a, s]) => { const q = new T.BufferAttribute(a, s); q.setUsage(T.DynamicDrawUsage); g.setAttribute(k, q); });
    g.setAttribute('side', new T.BufferAttribute(sd, 1)); g.setIndex(ix);
    const m = new T.ShaderMaterial({ uniforms: { uH: { value: ctx.H }, uMin: { value: o.minPx || 1.5 } }, transparent: true, depthWrite: false, blending: T.AdditiveBlending, side: T.DoubleSide,
      vertexShader: `attribute vec3 aD, aC; attribute float aW, side; uniform float uH, uMin; varying vec3 vC; varying float vY;
        void main(){ vec3 V = cameraPosition - position; float dc = max(length(V), 1e-3); float w = max(aW, dc * 2. / (projectionMatrix[1][1] * uH) * uMin);
          vec3 s = cross(aD, V); float sl = length(s); s = sl > 1e-6 ? s / sl : vec3(1., 0., 0.);
          vC = aC * (aW / w); vY = side; gl_Position = projectionMatrix * viewMatrix * vec4(position + s * side * w * .5, 1.); }`,
      fragmentShader: `varying vec3 vC; varying float vY; void main(){ float a = exp(-vY * vY * 3.) * (1. - vY * vY); gl_FragColor = vec4(vC * a, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` });
    const M = new T.Mesh(g, m); M.frustumCulled = false; M.renderOrder = o.order || 0; par.add(M);
    return { mesh: M, set(i, p, d, w, r, gg, b) { for (let k = 0; k < 2; k++) { const j = (i * 2 + k) * 3; P[j] = p.x; P[j + 1] = p.y; P[j + 2] = p.z; D[j] = d.x; D[j + 1] = d.y; D[j + 2] = d.z; C[j] = r; C[j + 1] = gg; C[j + 2] = b; Wd[i * 2 + k] = w; } },
      commit() { ['position', 'aD', 'aW', 'aC'].forEach(k => g.attributes[k].needsUpdate = true); } }; }

  // ---------------- sky: equirect canvas made once (Milky Way band, core, dust lanes, airglow) ----------------
  const A0 = v3(-.25, .55, -1).normalize(), G0 = v3(.62, .1, -1).normalize();       // band passes A0 and its bright core G0
  const NRM = new T.Vector3().crossVectors(A0, G0).normalize();
  const hsh = (x, y, z) => { let h = (x * 374761393 + y * 668265263 + z * 1274126177) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };
  function vn(x, y, z) { const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), xf = x - xi, yf = y - yi, zf = z - zi;
    const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf), w = zf * zf * (3 - 2 * zf); const L = (a, b, k) => a + (b - a) * k;
    return L(L(L(hsh(xi, yi, zi), hsh(xi + 1, yi, zi), u), L(hsh(xi, yi + 1, zi), hsh(xi + 1, yi + 1, zi), u), v),
      L(L(hsh(xi, yi, zi + 1), hsh(xi + 1, yi, zi + 1), u), L(hsh(xi, yi + 1, zi + 1), hsh(xi + 1, yi + 1, zi + 1), u), v), w); }
  const fbm = (x, y, z, o) => { let s = 0, a = .5, f = 1; for (let k = 0; k < o; k++) { s += a * vn(x * f, y * f, z * f); a *= .5; f *= 2.03; } return s; };
  const PH0 = Math.PI * 1.5 - 1.65, PHL = 3.3, THL = Math.PI / 2 + .12, SW = 2048, SH = 1024, sc = document.createElement('canvas'); sc.width = SW; sc.height = SH;
  { const g = sc.getContext('2d'), im = g.createImageData(SW, SH), D = im.data;
    for (let py = 0; py < SH; py++) { const th = (py + .5) / SH * THL, st = Math.sin(th), ct = Math.cos(th);
      for (let px = 0; px < SW; px++) { const ph = PH0 + (px + .5) / SW * PHL, dx = -Math.cos(ph) * st, dy = ct, dz = Math.sin(ph) * st;
        // base: deep navy-violet, a little lighter toward the horizon (airglow), black below
        const hz = Math.exp(-Math.abs(dy) * 7), up = Math.max(0, dy);
        let r = .006 + .03 * hz, gg = .007 + .022 * hz, b = .02 + .05 * hz + .008 * up;
        if (dy < 0) { r *= .6; gg *= .6; b *= .6; }
        const bl = Math.asin(dx * NRM.x + dy * NRM.y + dz * NRM.z), ab = Math.abs(bl);
        if (ab < .62) { const cg = Math.acos(Math.min(1, dx * G0.x + dy * G0.y + dz * G0.z));
          const n1 = fbm(dx * 3.2 + 9, dy * 3.2, dz * 3.2, 4), n2 = fbm(dx * 9 + 3, dy * 9 + 1, dz * 9, 3);
          const core = Math.exp(-cg * cg / .11), wid = .13 + .1 * core;
          let band = Math.exp(-(bl * bl) / (wid * wid)) * (.35 + .9 * n1) * (.55 + .9 * core) + .25 * Math.exp(-(bl * bl) / (.4 * .4)) * n1;
          const lane = Math.exp(-Math.pow((bl - .015 + (n1 - .5) * .07) / (.022 + .03 * core), 2)) * sm(.35, .7, n2 + .15);
          band *= 1 - .82 * lane; band *= .75 + .5 * n2;
          const warm = Math.min(1, core * 1.4 + .15);
          band = Math.pow(band, 1.35) * .55; r += band * (.20 + .3 * warm); gg += band * (.20 + .18 * warm); b += band * (.30 + .02 * warm);
          // pink / violet emission knots along the band
          const kn = Math.max(0, fbm(dx * 14 + 5, dy * 14, dz * 14 + 2, 2) - .58) * 3 * Math.exp(-(bl * bl) / .01);
          r += kn * .12; gg += kn * .025; b += kn * .09; }
        // faint violet nebula far off-band (upper left), blue on the right
        const neb = up > .05 ? Math.max(0, vn(dx * 2 + 1, dy * 2 + 7, dz * 2) - .55) * up : 0;
        r += neb * .06; gg += neb * .03; b += neb * .14;
        const k = (py * SW + px) * 4, cl = v => Math.max(0, Math.min(255, Math.pow(v, 1 / 2.2) * 255));
        D[k] = cl(r); D[k + 1] = cl(gg); D[k + 2] = cl(b); D[k + 3] = 255; } }
    g.putImageData(im, 0, 0); }
  const skyT = new T.CanvasTexture(sc); skyT.colorSpace = T.SRGBColorSpace;
  const sky = new T.Mesh(new T.SphereGeometry(1500, 96, 48, PH0, PHL, 0, THL), new T.MeshBasicMaterial({ map: skyT, side: T.BackSide, fog: false, depthWrite: false }));
  sky.renderOrder = -2; S.add(sky);
  const skyK = sky.material.color;
  // airglow (2026-10-16 staging pass): faint teal / violet bands low over the horizon, slowly drifting and rippling (additive, subtle)
  const agU = { uT: { value: 0 }, uK: { value: 1 } };
  const airglow = new T.Mesh(new T.SphereGeometry(1450, 64, 24, 0, Math.PI * 2, 0, Math.PI / 2 + .05), new T.ShaderMaterial({ uniforms: agU, side: T.BackSide, transparent: true, depthWrite: false, blending: T.AdditiveBlending, fog: false,
    vertexShader: `varying vec3 vD; void main(){ vD = position; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }`,
    fragmentShader: `varying vec3 vD; uniform float uT, uK;
      float hh(vec3 p){ return fract(sin(dot(p, vec3(12.9898, 78.233, 37.719))) * 43758.5453); }
      float vn(vec3 p){ vec3 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f);
        return mix(mix(mix(hh(i), hh(i + vec3(1., 0., 0.)), f.x), mix(hh(i + vec3(0., 1., 0.)), hh(i + vec3(1., 1., 0.)), f.x), f.y),
                   mix(mix(hh(i + vec3(0., 0., 1.)), hh(i + vec3(1., 0., 1.)), f.x), mix(hh(i + vec3(0., 1., 1.)), hh(i + vec3(1., 1., 1.)), f.x), f.y), f.z); }
      void main(){ vec3 d = normalize(vD); float el = d.y;
        float band = smoothstep(-.01, .06, el) * exp(-pow((el - .13) / .13, 2.));
        vec3 q = d * vec3(4., 10., 4.) + vec3(uT * .015, 0., uT * .024);
        float n = vn(q) * .65 + vn(q * 2.1 + 3.) * .35;
        float wv = .5 + .5 * sin(d.x * 16. + d.z * 11. + n * 5. + uT * .07);
        float a = band * (.3 + .7 * n) * (.55 + .45 * wv) * uK * .75;
        vec3 c = mix(vec3(.022, .05, .055), vec3(.05, .026, .065), smoothstep(.1, .28, el)) * a;
        gl_FragColor = vec4(c, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  airglow.renderOrder = -2; S.add(airglow);

  // ---------------- stars: field + band-concentrated, three size classes, twinkle ----------------
  const R1 = rng(7), U = v3(0, 0, 0), BX = new T.Vector3().crossVectors(NRM, A0).normalize();
  const starSets = [], SR = 1400;
  function addStars(n, size, band, seed) { const r = rng(seed), P = points(n, { size, opacity: 1, atten: false }), a = P.geometry.attributes.position.array, c = P.geometry.attributes.color.array, base = new Float32Array(n * 4);
    for (let i = 0; i < n; i++) { let d;
      if (band) { const lon = r() * 6.283, lat = (r() + r() + r() - 1.5) * .16 * (r() < .3 ? 2.4 : 1); d = A0.clone().multiplyScalar(Math.cos(lon)).addScaledVector(BX, Math.sin(lon)).multiplyScalar(Math.cos(lat)).addScaledVector(NRM, Math.sin(lat)); }
      else { const u = r() * 2 - 1, th = r() * 6.283, q = Math.sqrt(1 - u * u); d = v3(q * Math.cos(th), u, q * Math.sin(th)); }
      if (d.y < -.05) d.y = -d.y;   // keep stars above the horizon
      a.set([d.x * SR, d.y * SR, d.z * SR], i * 3);
      const tmp = r(), br = .5 + 1.1 * Math.pow(r(), 2.5), hz = sm(-.02, .18, d.y);
      const col = tmp < .2 ? [.75, .82, 1] : tmp < .75 ? [1, .97, .92] : [1, .84, .62];
      base.set([col[0] * br * hz, col[1] * br * hz, col[2] * br * hz, r() * 6.283], i * 4); }
    P.material.depthWrite = false; P.renderOrder = -1; S.add(P); starSets.push({ P, c, base, n }); return P; }
  addStars(7000, 2.0, false, 11); addStars(16000, 1.8, true, 12); addStars(1500, 3.2, false, 13); addStars(1600, 3.0, true, 14); addStars(150, 5.5, false, 15);
  // deep-field galaxies (appear on "edge"): small tilted elliptical glows far off
  // (2026-10-16) 70 more, smaller and fainter, that emerge one after another through the rest of the "edge" shot (vastness)
  const gal = [], RG = rng(41); for (let i = 0; i < 110; i++) { const d = v3(RG() - .5, .35 + RG() * .9, -.6 - RG() * .8).normalize();
    const sp = new T.Sprite(new T.SpriteMaterial({ map: ctx.dotTex(), color: RG() < .5 ? '#ffd9a8' : '#bcc8ff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, fog: false, rotation: RG() * 3.14 }));
    const s0 = (8 + RG() * 18) * (i < 40 ? 1 : .55); sp.scale.set(s0, s0 * (.3 + RG() * .5), 1); sp.position.copy(d.multiplyScalar(1350)); sp.renderOrder = -1; S.add(sp); gal.push([sp, RG(), i < 40 ? -1 : (i - 40) / 70]); }

  // ---------------- terrain: hilltop plateau, slopes, far plain and mountain ridges ----------------
  const hN = (x, z) => fbm(x * .02 + 50, 0, z * .02 + 50, 4);
  const H = (x, z) => { const r = Math.hypot(x, z), rr = Math.max(0, r - 7);
    let h = -42 * (1 - Math.exp(-rr * rr / 4200)) + (hN(x, z) - .5) * 3 * sm(8, 30, r);
    h += sm(520, 700, r) * (30 + 70 * fbm(x * .006 + 3, 1, z * .006, 4)) * (z < 0 ? 1 : .6);
    const dp = (x + 147) ** 2 + (z + 275) ** 2; h += 32 * Math.exp(-dp / 6000); return h; };
  const tg = new T.PlaneGeometry(1800, 1800, 200, 200); tg.rotateX(-Math.PI / 2);
  { const P = tg.attributes.position; for (let i = 0; i < P.count; i++) P.setY(i, H(P.getX(i), P.getZ(i))); tg.computeVertexNormals(); }
  const grnd = K.noise(256, { seed: 3, octaves: 3 }), grT = K.tex(grnd, true, [90, 90]);   // no per-pixel octaves (stable in motion, 3A)
  
  const terrain = new T.Mesh(tg, new T.MeshLambertMaterial({ color: '#232540', map: grT }));
  S.add(terrain);

  // ---------------- observatory ----------------
  const OB = new T.Group(); S.add(OB);
  const concrete = new T.MeshStandardMaterial({ side: T.DoubleSide, color: '#c3c8da', roughness: .8, metalness: 0, map: (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const g = c.getContext('2d'); g.fillStyle = '#d8dbe4'; g.fillRect(0, 0, 256, 256); g.globalAlpha = .22; g.drawImage(K.noise(256, { seed: 8, octaves: 3 }), 0, 0); g.globalAlpha = 1;
    g.fillStyle = 'rgba(60,64,80,.55)'; [64, 128, 192].forEach(y => g.fillRect(0, y, 256, 2)); for (let x = 0; x < 256; x += 64) g.fillRect(x, 0, 2, 256); g.fillStyle = 'rgba(30,30,40,.25)'; g.fillRect(0, 240, 256, 16); const ct = K.tex(c, true, [8, 1]); return ct; })() });
  const metal = new T.MeshStandardMaterial({ color: '#d4d8e4', metalness: .15, roughness: .38, side: T.DoubleSide });
  const darkIn = new T.MeshStandardMaterial({ color: '#2a2433', roughness: .8, metalness: .2, side: T.DoubleSide });
  const WARM = new T.Color('#ffc27a'), ACC = new T.Color(ctx.ACC);
  const addM = (g, m, par) => { const o = new T.Mesh(g, m); (par || OB).add(o); return o; };
  // plinth + drum (real wall thickness via lathe: outer wall, top lip, inner wall)
  addM(new T.CylinderGeometry(5.0, 5.3, .6, 72), concrete).position.y = .3;
  const drumP = [[3.82, .6], [4.0, .6], [4.02, .75], [4.02, 3.9], [4.12, 4.0], [4.12, 4.18], [3.82, 4.18]].map(([r, h]) => new T.Vector2(r, h));
  addM(new T.LatheGeometry(drumP, 96), concrete);
  addM(new T.CircleGeometry(3.83, 48).rotateX(-Math.PI / 2).translate(0, 3.6, 0), darkIn);   // observing floor
  // door (front, recessed frame + panel with a warm light seam) and a lit window strip
  const DOOR = new T.Group(); OB.add(DOOR);
  addM(new T.BoxGeometry(1.7, 2.6, .35), concrete, DOOR).position.set(0, 1.9, 0);
  addM(new T.BoxGeometry(1.25, 2.25, .1), new T.MeshStandardMaterial({ color: '#3a3f55', metalness: .6, roughness: .45, roughness: .45 }), DOOR).position.set(0, 1.78, .2);
  const seamM = new T.MeshBasicMaterial({ color: WARM.clone().multiplyScalar(1.6) });
  addM(new T.BoxGeometry(1.3, .04, .04), seamM, DOOR).position.set(0, .66, .24);
  addM(new T.BoxGeometry(.04, 2.2, .04), seamM, DOOR).position.set(.06, 1.78, .26);
  DOOR.position.set(0, 0, 4.02); DOOR.rotation.y = 0;
  const DPIV = new T.Group(); DPIV.add(DOOR); OB.add(DPIV); DPIV.rotation.y = .32;   // door faces the camera's side
  const dg = glow(OB, '#ffc27a', 3.2, .35); dg.position.set(Math.sin(.32) * 4.8, 1.6, Math.cos(.32) * 4.8);
  // dome: param  x = r sinB (across the slit), y = r cosB sinG, z = r cosB cosG  (G=0 front horizon, the slit runs G 0..GM)
  const DR = 4.15, TH = .14, B0 = Math.asin(.85 / DR), GM = 1.95;
  function domeGeo(pieces, slitWalls) { const pos = [], nor = [], idx = [];
    const P = (r, b, g) => [r * Math.sin(b), r * Math.cos(b) * Math.sin(g), r * Math.cos(b) * Math.cos(g)];
    function patch(r, b0, b1, g0, g1, nb, ng, inward) { const s = pos.length / 3;
      for (let i = 0; i <= nb; i++) for (let j = 0; j <= ng; j++) { const b = b0 + (b1 - b0) * i / nb, g = g0 + (g1 - g0) * j / ng, q = P(r, b, g), l = inward ? -1 / r : 1 / r; pos.push(...q); nor.push(q[0] * l, q[1] * l, q[2] * l); }
      for (let i = 0; i < nb; i++) for (let j = 0; j < ng; j++) { const a = s + i * (ng + 1) + j, b = a + ng + 1; inward ? idx.push(a, a + 1, b, b, a + 1, b + 1) : idx.push(a, b, a + 1, a + 1, b, b + 1); } }
    function wall(f, n, nrm) { const s = pos.length / 3; for (let k = 0; k <= n; k++) { const [o, i2] = f(k / n); pos.push(...o, ...i2); const nn = nrm(k / n); nor.push(...nn, ...nn); }
      for (let k = 0; k < n; k++) { const a = s + k * 2; idx.push(a, a + 1, a + 2, a + 2, a + 1, a + 3); } }
    pieces.forEach(([b0, b1, g0, g1, nb, ng]) => { if (slitWalls !== 2) patch(DR, b0, b1, g0, g1, nb, ng, false); if (slitWalls !== 1) patch(DR - TH, b0, b1, g0, g1, nb, ng, true); });
    if (slitWalls === 1) { [B0, -B0].forEach(b => wall(k => [P(DR, b, k * GM), P(DR - TH, b, k * GM)], 40, k => { const g = k * GM, sb = Math.sin(Math.abs(b)), cb = Math.cos(b); return b > 0 ? [-cb, sb * Math.sin(g), sb * Math.cos(g)] : [cb, sb * Math.sin(g), sb * Math.cos(g)]; }));
      wall(k => [P(DR, -B0 + 2 * B0 * k, GM), P(DR - TH, -B0 + 2 * B0 * k, GM)], 8, () => [0, -Math.cos(GM), Math.sin(GM)]); }
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('normal', new T.Float32BufferAttribute(nor, 3)); g.setIndex(idx); return g; }
  const DOME = new T.Group(); DOME.position.y = 4.18; OB.add(DOME);
  const PI2 = Math.PI / 2;
  const DP = [[B0, PI2, 0, Math.PI, 30, 72], [-PI2, -B0, 0, Math.PI, 30, 72], [-B0, B0, GM, Math.PI, 6, 30]];
  DOME.add(new T.Mesh(domeGeo(DP, 1), metal));
  const innerM = new T.MeshStandardMaterial({ color: '#1e1b2a', roughness: .7, metalness: .3, side: T.DoubleSide, emissive: '#ff9a4a', emissiveIntensity: 0 });
  DOME.add(new T.Mesh(domeGeo(DP, 2), innerM));
  // ribs (meridian seams) on the outer shell and a base ring
  const ribM = new T.MeshStandardMaterial({ color: '#e2e6f0', metalness: .3, roughness: .3 });
  for (let k = 1; k < 12; k++) { const b = -PI2 + k / 12 * Math.PI; if (Math.abs(b) < B0 + .05) continue;
    const pts = []; for (let j = 0; j <= 40; j++) { const g = j / 40 * Math.PI; pts.push(v3((DR + .02) * Math.sin(b), (DR + .02) * Math.cos(b) * Math.sin(g), (DR + .02) * Math.cos(b) * Math.cos(g))); }
    DOME.add(new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pts), 40, .045, 6, false), ribM)); }
  DOME.add(new T.Mesh(new T.TorusGeometry(DR + .05, .1, 10, 120).rotateX(PI2), ribM));
  const rimGlow = new T.Mesh(new T.TorusGeometry(DR + .08, .028, 8, 160).rotateX(PI2).translate(0, -.08, 0), new T.MeshBasicMaterial({ color: ACC.clone().multiplyScalar(1.1), transparent: true, opacity: .7, blending: T.AdditiveBlending, depthWrite: false }));
  DOME.add(rimGlow);
  // glowing slit edges (light leaking from inside)
  const edgeM = new T.MeshBasicMaterial({ color: WARM.clone().multiplyScalar(1.4), transparent: true, opacity: .5, blending: T.AdditiveBlending, depthWrite: false });
  [B0, -B0].forEach(b => { const pts = []; for (let j = 0; j <= 40; j++) { const g = j / 40 * GM; pts.push(v3((DR + .01) * Math.sin(b), (DR + .01) * Math.cos(b) * Math.sin(g), (DR + .01) * Math.cos(b) * Math.cos(g))); }
    DOME.add(new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pts), 40, .035, 6, false), edgeM)); });
  // shutter: a thick curved panel over the slit, slides back over the top (rotation about the dome's x axis)
  const SHD = 1.25, shG = (() => { const pos = [], nor = [], idx = [], b0 = B0 + .06, R0 = DR + .1;
    const pa = (r, inward) => { const s = pos.length / 3, nb = 6, ng = 30; for (let i = 0; i <= nb; i++) for (let j = 0; j <= ng; j++) { const b = -b0 + 2 * b0 * i / nb, g = SHD * j / ng, q = [r * Math.sin(b), r * Math.cos(b) * Math.sin(g), r * Math.cos(b) * Math.cos(g)], l = inward ? -1 / r : 1 / r; pos.push(...q); nor.push(q[0] * l, q[1] * l, q[2] * l); }
      for (let i = 0; i < nb; i++) for (let j = 0; j < ng; j++) { const a = s + i * (ng + 1) + j, b = a + ng + 1; inward ? idx.push(a, a + 1, b, b, a + 1, b + 1) : idx.push(a, b, a + 1, a + 1, b, b + 1); } };
    pa(R0, false); pa(R0 - .1, true); const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('normal', new T.Float32BufferAttribute(nor, 3)); g.setIndex(idx); return g; })();
  const SHUT = new T.Group(); DOME.add(SHUT); SHUT.add(new T.Mesh(shG, metal));
  [B0 + .06, -B0 - .06].forEach(b => { const pts = []; for (let j = 0; j <= 20; j++) { const g = j / 20 * SHD; pts.push(v3((DR + .1) * Math.sin(b), (DR + .1) * Math.cos(b) * Math.sin(g), (DR + .1) * Math.cos(b) * Math.cos(g))); }
    SHUT.add(new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pts), 20, .05, 6, false), ribM)); });
  // second shutter leaf (only built for "close"): stowed over the back of the dome, slides over the top to seal the slit
  const LEAF = p.close != null ? new T.Group() : null, LFD = .78;
  if (LEAF) { DOME.add(LEAF); const lg = shG.clone(), lp = lg.attributes.position, sk = LFD / SHD, Rl = 1.03;
    for (let i = 0; i < lp.count; i++) { const x = lp.getX(i), y = lp.getY(i), z = lp.getZ(i), g = Math.atan2(y, z) * sk, rr = Math.hypot(y, z) * Rl;
      lp.setXYZ(i, x * Rl, rr * Math.sin(g), rr * Math.cos(g)); } lg.computeVertexNormals(); LEAF.add(new T.Mesh(lg, metal));
    [B0 + .06, -B0 - .06].forEach(b => { const pts = []; for (let j = 0; j <= 12; j++) { const g = j / 12 * LFD; pts.push(v3((DR + .1) * Rl * Math.sin(b), (DR + .1) * Rl * Math.cos(b) * Math.sin(g), (DR + .1) * Rl * Math.cos(b) * Math.cos(g))); }
      LEAF.add(new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(pts), 12, .05, 6, false), ribM)); }); }
  // telescope: pier, fork, open tube with wall thickness, dew cap, glowing aperture ring
  const TEL = new T.Group(); DOME.add(TEL); TEL.position.set(0, -.2, 0);
  addM(new T.CylinderGeometry(.35, .5, 1.2, 24), concrete, TEL).position.y = -.75;
  const fork = new T.MeshStandardMaterial({ color: '#2b2f45', metalness: .7, roughness: .35, envMap: E, envMapIntensity: .4 });
  [-.62, .62].forEach(x => addM(new T.BoxGeometry(.14, 1.1, .35), fork, TEL).position.set(x, .25, 0));
  const TUBE = new T.Group(); TUBE.position.y = .55; TEL.add(TUBE);
  const tubeP = [[.38, -1.4], [.48, -1.4], [.5, -1.2], [.5, 1.6], [.56, 1.62], [.56, 2.2], [.5, 2.2], [.5, 1.7], [.44, 1.6], [.44, -1.3], [.38, -1.3]].map(([r, h]) => new T.Vector2(r, h));
  addM(new T.LatheGeometry(tubeP, 48), new T.MeshStandardMaterial({ color: '#e6e8f0', metalness: .4, roughness: .3, envMap: E, envMapIntensity: .5, side: T.DoubleSide }), TUBE);
  addM(new T.TorusGeometry(.53, .03, 8, 64).rotateX(PI2).translate(0, 2.2, 0), new T.MeshBasicMaterial({ color: ACC.clone().multiplyScalar(1.5), transparent: true, blending: T.AdditiveBlending, depthWrite: false }), TUBE);
  const mirror = addM(new T.CircleGeometry(.43, 40).rotateX(-PI2).translate(0, -1.2, 0), new T.MeshBasicMaterial({ color: '#ffe3b0' }), TUBE);
  
  const inGlow = glow(DOME, '#ffbb70', 9, 0); inGlow.position.set(0, 1.6, 1.4);
  // path lights down the slope toward the camera
  const postM = new T.MeshStandardMaterial({ color: '#2a2d40', roughness: .6, metalness: .4 });
  for (let k = 0; k < 4; k++) { const z = 6.5 + k * 3.2, x = 2.2 + k * 1.1 + Math.sin(k) * .4, y = H(x, z);
    addM(new T.CylinderGeometry(.04, .05, .55, 8), postM).position.set(x, y + .27, z);
    const s = glow(OB, '#ffc98a', .9, .45); s.position.set(x, y + .58, z); const s2 = glow(OB, '#ff9a50', .3, .9); s2.position.set(x, y + .58, z); }

  // ---------------- starlight stream into the slit ----------------
  const NS = 700, sl = points(NS, { size: .16, opacity: 1, color: '#ffe8c0' }), slA = sl.geometry.attributes.position.array, slC = sl.geometry.attributes.color.array, slB = [];
  { const r = rng(61); for (let i = 0; i < NS; i++) slB.push([r(), (r() - .5) * 2, (r() - .5) * 2, r()]); } DOME.add(sl); sl.frustumCulled = false;

  // ---------------- rocket ----------------
  const ROCK = new T.Group(); S.add(ROCK);
  const rp = [[0, 0], [.95, 0], [1.05, .3], [1.05, 13], [1.0, 13.3], [1.0, 17], [.95, 17.6], [.8, 19.5], [.5, 21], [.15, 22], [0, 22.2]].map(([r, h]) => new T.Vector2(r, h));
  const hullT = ctx.ctex(256, (g, s) => { g.fillStyle = '#e8eaf0'; g.fillRect(0, 0, s, s); g.fillStyle = '#1c1f2c'; [[.14, .03], [.56, .02], [.74, .015]].forEach(([y, h]) => g.fillRect(0, s * (1 - y - h), s, s * h)); g.fillStyle = 'rgba(40,44,60,.25)'; for (let i = 0; i < 8; i++) g.fillRect(i / 8 * s, 0, 1.5, s); });
  const hull = new T.MeshStandardMaterial({ fog: false, map: hullT, metalness: .35, roughness: .4, envMap: E, envMapIntensity: .5 });
  ROCK.add(new T.Mesh(new T.LatheGeometry(rp, 40), hull));
  const finG = K.fin([[0, 0], [2.0, 0], [2.6, -.6], [2.4, -1.4], [0, -.2]], .22);
  for (let k = 0; k < 4; k++) { const f = new T.Mesh(finG, new T.MeshStandardMaterial({ fog: false, color: '#2a2e40', metalness: .6, roughness: .4, envMap: E, envMapIntensity: .4 })); const a = k / 4 * 6.283 + .4;
    f.position.set(Math.cos(a) * 1.7, 2.0, Math.sin(a) * 1.7); f.rotation.set(0, -a, PI2); ROCK.add(f); }
  addM(new T.CylinderGeometry(.55, .85, 1.1, 24, 1, true), new T.MeshStandardMaterial({ color: '#3a3a48', metalness: .9, roughness: .3, side: T.DoubleSide }), ROCK).position.y = -.5;
  // flame: two nested additive cones + glows; a light that washes the smoke and ground
  const flameT = ctx.ctex(128, (g, s) => { const gr = g.createLinearGradient(0, 0, 0, s); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(.15, 'rgba(255,224,160,1)'); gr.addColorStop(.5, 'rgba(255,150,60,.55)'); gr.addColorStop(1, 'rgba(255,90,40,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); });
  const flM = o => new T.MeshBasicMaterial({ map: flameT, transparent: true, opacity: o, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide, fog: false });
  const fl1 = new T.Mesh(new T.ConeGeometry(1.0, 9, 24, 1, true).rotateX(Math.PI).translate(0, -5.5, 0), flM(.9)), fl2 = new T.Mesh(new T.ConeGeometry(1.8, 16, 24, 1, true).rotateX(Math.PI).translate(0, -9, 0), flM(.45));
  ROCK.add(fl1, fl2); const fg1 = glow(ROCK, '#fff0d0', 9, 0), fg2 = glow(ROCK, '#ffb060', 40, 0); fg1.position.y = fg2.position.y = -2;
  
  [fl1, fl2, fg1, fg2].forEach(o => o.renderOrder = 3);
  const PAD = v3(-147, 0, -275); PAD.y = H(PAD.x, PAD.z); ROCK.scale.setScalar(1.15);
  const padG = glow(S, '#ffb060', 60, 0); padG.position.copy(PAD).add(v3(0, 4, 0));
  const tR = p.rocket != null ? cue(p.rocket) : 1e9;
  // (2026-10-16 third pass) the opening shot (rocket given, not close / night) gets the hook staging; cues default from the old ones
  const INTRO = p.rocket != null && p.close == null && p.night == null;
  const tTr = INTRO ? (p.trails != null ? cue(p.trails) : (p.widen != null ? cue(p.widen) : ctx.t0 + 7.9)) : 1e9, tLn = INTRO ? (p.lines != null ? cue(p.lines) : tTr + 1.6) : 1e9;
  const tBm = INTRO ? (p.beam != null ? cue(p.beam) : tR - 5.3) : 1e9, tFb = INTRO ? (p.fireball != null ? cue(p.fireball) : ctx.t0 + 3.6) : 1e9;
  const tWl = INTRO && (p.wall != null || p.edge != null) ? (p.wall != null ? cue(p.wall) : cue(p.edge) + 7.95) : 1e9, tCg = tWl < 1e8 ? (p.cage != null ? cue(p.cage) : tWl + 6) : 1e9;
  // the rocket meets the wall: from 1 s before the touch it decelerates smoothly (C1) and creeps to a stop, pressing on the barrier
  const yP0 = tau => 3.2 * tau * tau + 1.2 * tau * tau * tau, tauD = tWl < 1e8 ? tWl - 1 - tR : 1e9, KW = .55, yDd = yP0(Math.min(tauD, 1e3)), vDd = 6.4 * tauD + 3.6 * tauD * tauD;
  const yP = tau => tau <= tauD ? yP0(tau) : yDd + vDd * KW * (1 - Math.exp(-(tau - tauD) / KW));
  const pathY = y => v3(PAD.x - y * .06, PAD.y + 3 + y, PAD.z - 1.1 * y * y / (y + 160));
  const path0 = tau => pathY(yP0(Math.max(0, tau)));
  const path = tau => pathY(yP(Math.max(0, tau)));   // smooth pitch-over (was min(1, y/160): a kink in the trail, 2026-10-16)
  // exhaust trail (particles left along the path; each drifts and fades with age) and the smoke cloud at the pad
  // (2026-10-16) the trail particles carry their own world size (they swell with age) with a pixel floor / ceiling, so particles near
  // the camera no longer balloon into a white band; emission times are half even in time, half even along the path (no gaps late on)
  const TSPAN = 30, yOf = tt => 3.2 * tt * tt + 1.2 * tt * tt * tt, yInv = y => { let a = 0, b = TSPAN; for (let k = 0; k < 40; k++) { const m = (a + b) / 2; yOf(m) < y ? a = m : b = m; } return (a + b) / 2; };
  const NT = 3600, trG = new T.BufferGeometry(), trA = new Float32Array(NT * 3), trC = new Float32Array(NT * 3), trS = new Float32Array(NT), trB = [];
  { const r = rng(71); for (let i = 0; i < NT; i++) { const o = r(); trB.push([i % 2 ? o * TSPAN : yInv(Math.pow(o, 1.15) * yOf(TSPAN)), r() - .5, r() - .5, r() - .5, r()]); } }
  trG.setAttribute('position', new T.BufferAttribute(trA, 3)); trG.setAttribute('color', new T.BufferAttribute(trC, 3)); trG.setAttribute('size', new T.BufferAttribute(trS, 1));
  const trU = { uScale: { value: 1000 } };
  const tr = new T.Points(trG, new T.ShaderMaterial({ uniforms: trU, transparent: true, depthWrite: false, blending: T.AdditiveBlending,
    vertexShader: `attribute vec3 color; attribute float size; uniform float uScale; varying vec3 vC;
      void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.); float z = max(-mv.z, .1), ps = size * uScale / z, a = 1.;
        if (ps < 1.6) { a = ps * ps / 2.56; ps = 1.6; } if (ps > 22.) { a = 22. / ps; ps = 22.; }
        vC = color * a; gl_PointSize = ps; gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `varying vec3 vC; void main(){ vec2 q = gl_PointCoord - .5; float r2 = dot(q, q) * 4.; gl_FragColor = vec4(vC * exp(-r2 * 3.) * (1. - smoothstep(.7, 1., r2)), 1.);
      #include <tonemapping_fragment>
      #include <colorspace_fragment>
    }` }));
  S.add(tr); tr.frustumCulled = false; tr.renderOrder = 2;
  // contrail ribbon (smoke column left along the path, widening with age, moonlit; warm near the flame) + the hot core streak
  const NRB = 140, cTrail = ribbon(S, NRB, { minPx: 1.4, order: 2 }), core = streaks(S, 2, { minPx: 2, near: [1, 3], order: 4 });
  // launch steam / smoke (2026-10-16): puffs shot out sideways along the flame trench and up in a column, slowing by drag, rising and
  // swelling, lit orange from below by the flame early on, moonlit grey-violet later. Each puff's emission time is fixed, so its
  // state is a pure function of t (no recycling needed: the launch is one event).
  const puffT = ctx.ctex(128, (g, s) => { const r = rng(90); for (let k = 0; k < 10; k++) { const a = r() * 6.283, d = r() * s * .17, x = s / 2 + Math.cos(a) * d, y = s / 2 + Math.sin(a) * d, rr = s * (.2 + .12 * r());
    const gr = g.createRadialGradient(x, y, 0, x, y, rr); gr.addColorStop(0, 'rgba(255,255,255,.5)'); gr.addColorStop(.6, 'rgba(255,255,255,.18)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); } });
  const NSm = 600, smG = new T.BufferGeometry(), smA = new Float32Array(NSm * 3), smC = new Float32Array(NSm * 4), smZ = new Float32Array(NSm), smR = new Float32Array(NSm), smB = [];
  const TAX = v3(.89, 0, -.46);
  { const r = rng(73); for (let i = 0; i < NSm; i++) { const lat = r() < .55, sgn = r() < .5 ? -1 : 1, an = (r() - .5) * (lat ? .9 : 6.283);
    const dir = lat ? TAX.clone().multiplyScalar(sgn).applyAxisAngle(v3(0, 1, 0), an) : v3(Math.cos(an), 0, Math.sin(an));
    smB.push({ te: -.9 + 12 * Math.pow(r(), 1.7), lat, dir, v0: lat ? 30 + 34 * r() : 7 + 13 * r(), td: lat ? 1.4 + .8 * r() : 2 + r(), up: lat ? .6 + 1.6 * r() : 2 + 3.5 * r(), y0: lat ? r() * 2 : r() * 10, s0: 3 + 3 * r(), life: 13 + 9 * r(), ph: r() * 6.283, w: r() });
    smR[i] = r() * 6.283; } }
  smG.setAttribute('position', new T.BufferAttribute(smA, 3)); smG.setAttribute('col', new T.BufferAttribute(smC, 4)); smG.setAttribute('sz', new T.BufferAttribute(smZ, 1)); smG.setAttribute('rot', new T.BufferAttribute(smR, 1));
  const smU = { uScale: { value: 1000 }, uTex: { value: puffT }, uFog: { value: FOGC }, uDen: { value: S.fog.density } };
  const smk = new T.Points(smG, new T.ShaderMaterial({ uniforms: smU, transparent: true, depthWrite: false,
    vertexShader: `attribute vec4 col; attribute float sz, rot; uniform float uScale, uDen; uniform vec3 uFog; varying vec4 vC; varying float vR;
      void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.); float z = max(-mv.z, .1), ps = sz * uScale / z, a = col.a;
        if (ps < 2.) { a *= ps * ps / 4.; ps = 2.; } if (ps > 150.) { a *= 150. / ps; ps = 150.; }
        float f = 1. - exp(-pow(uDen * z, 2.)); vC = vec4(mix(col.rgb, uFog, f), a); vR = rot; gl_PointSize = ps; gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `uniform sampler2D uTex; varying vec4 vC; varying float vR;
      void main(){ vec2 q = gl_PointCoord - .5; float c = cos(vR), s = sin(vR); q = mat2(c, -s, s, c) * q; float a = texture2D(uTex, q + .5).a * vC.a; if (a < .003) discard;
        gl_FragColor = vec4(vC.rgb, a);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  S.add(smk); smk.frustumCulled = false; smk.renderOrder = 1;
  // ignition: a flash at the pad (rise .25 s, fade ~1.8 s) with a short anamorphic streak, a shock ring racing out over the ground,
  // the pad glow swells (no extra scene light: too costly here); max-Q: a brief white vapour halo around the rocket
  const flash1 = glow(S, '#fff3dc', 120, 0), flashA = glow(S, '#ffd6a8', 1, 0); flash1.position.copy(PAD).add(v3(0, 6, 0)); flashA.position.copy(flash1.position);
  const ringM = new T.MeshBasicMaterial({ map: ctx.ctex(256, (g, s) => { const gr = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.72, 'rgba(255,220,180,0)'); gr.addColorStop(.9, 'rgba(255,225,190,.9)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); }),
    transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, fog: false, side: T.DoubleSide });
  const shRing = new T.Mesh(new T.PlaneGeometry(1, 1).rotateX(-PI2), ringM); shRing.position.copy(PAD).add(v3(0, 1.5, 0)); S.add(shRing);
  const vapor = glow(ROCK, '#eef2ff', 10, 0); vapor.position.y = 9; vapor.renderOrder = 3;

  // ---------------- meteor, dust, lights ----------------
  const met = new T.Mesh(new T.PlaneGeometry(1, 1), new T.MeshBasicMaterial({ map: ctx.ctex(256, (g, s) => { const gr = g.createLinearGradient(0, 0, s, 0); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.9, 'rgba(220,230,255,.9)'); gr.addColorStop(1, 'rgba(255,255,255,1)'); g.fillStyle = gr; g.fillRect(0, s * .47, s, s * .06); }),
    transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, fog: false, side: T.DoubleSide })); S.add(met);
  // (2026-10-16) life for the calm shots: slow meteors on a fixed schedule (2 slots), a satellite gliding over, soft bokeh motes
  // drifting close to the lens (world-fixed, so they sweep with every camera turn)
  const mets = streaks(S, 2, { minPx: 1.8, near: [50, 120], order: -1 });
  const sat = glow(S, '#e8ecff', 1, 0); sat.renderOrder = -1;
  const NBK = 46, bk = points(NBK, { size: .3, opacity: 1, color: '#ffffff' }), bkA = bk.geometry.attributes.position.array, bkC = bk.geometry.attributes.color.array, bkB = [];
  { const r = rng(83); for (let i = 0; i < NBK; i++) bkB.push([r() * 14 - 7, r() * 8 - 4, r() * 14 - 7, r(), r() * 6.283]); } bk.frustumCulled = false; bk.renderOrder = 5; S.add(bk);
  const CALM = p.close != null || p.night != null;
  const dust = K.snow(S, { n: 1600, box: [60, 30, 60], size: .1, opacity: .5, color: '#ffd9a0', fall: .05, seed: 9 });
  S.add(new T.HemisphereLight('#4a4f9a', '#06050e', .55));
  const moon = new T.DirectionalLight('#9aa8ff', .55); moon.position.set(-30, 40, -60); S.add(moon);
  const fill = new T.DirectionalLight('#ffd2a0', .12); fill.position.set(40, 20, 40); S.add(fill);
  const key = new T.DirectionalLight('#aab4ff', .9); key.position.set(-25, 30, 45); S.add(key);

  const cam = new T.PerspectiveCamera(42, ctx.W / ctx.H, .1, 60000); ctx.side(cam, p.side == null ? .12 : p.side);
  const PSC = Math.atan2(8, 24), tgt = new T.Vector3(), cp = new T.Vector3(), ft = new T.Vector3();
  const mcp = new T.Vector3(), mft = new T.Vector3(), mtg = new T.Vector3(), vt = new T.Vector3(), Y1 = v3(0, 1, 0);
  const tE = p.edge != null ? cue(p.edge) : 1e9, RM = 1000;
  // camera as a pure function of time (also used to pin meteors / the satellite to the sky seen at their mid time). Begins looking up
  // at the sky, tilts down onto the observatory, rises a little on "widen", on "follow" tilts up after the rocket, on "edge" pushes
  // toward the deep field. The look-at point keeps the plain target's distance (the camera director pivots on it).
  function camAt(tt, oCp, oFt, oTg) {
    const uu = tt - ctx.t0, wd = atT(p.widen, 4, tt), intro = sm(0, 6.5, uu), fo = atT(p.follow, 2.6, tt), ed = atT(p.edge, 3.5, tt), nt = atT(p.night, 16, tt), tau = tt - tR;
    // long shots with the new cues: the slow dolly eases out instead of running into the dome (old cues: unchanged)
    const ue = (p.close != null || p.night != null) ? 30 * (1 - Math.exp(-uu / 30)) : uu;
    oCp.set(8.5 - ue * .1 - 2 * wd, 1.0 + .8 * intro + 2.2 * wd + .1 * Math.sin(uu * .3), 25 - ue * .2 + 5 * wd);
    if (nt > 0) { oCp.y += 16 * nt; oCp.z += 8 * nt; oCp.x -= 3 * nt; }
    // INTRO: open on the dome, tilt up into the Milky Way ("look up"), hold on the sky (fireball, star trails, constellations), tilt back
    // down onto the dome as the telescope beam comes on
    const lift = INTRO ? 17 * sm(.15, 3.2, uu) * (1 - sm(tBm - 1.9 - ctx.t0, tBm + .6 - ctx.t0, uu)) : 16 * (1 - intro);
    oTg.set(-.5 + 1.5 * wd, 4.4 + lift + 1.5 * wd, 0); oFt.copy(oTg);
    const D = oTg.distanceTo(oCp);
    if (tau > 0 && fo > 0) { const rq = path(tau + .3), dq = rq.distanceTo(oCp);
      const lk = rq.clone().add(v3(0, dq * .08 * (1 - ed), 0)).lerp(oCp.clone().addScaledVector(A0.clone().add(v3(.05, .16, 0)).normalize(), dq), .55 * ed);
      const yp = q => { const d = q.clone().sub(oCp).normalize(); return [Math.atan2(d.x, -d.z), Math.asin(d.y)]; };
      const [y0, p0] = yp(oTg), [y1, p1] = yp(lk), yw = y0 + (y1 - y0) * fo * (.35 + .65 * ed), pt = p0 + (p1 - p0) * fo;
      oFt.copy(oCp).add(v3(Math.sin(yw) * Math.cos(pt), Math.sin(pt), -Math.cos(yw) * Math.cos(pt)).multiplyScalar(D)); }   // same distance as the plain target: a sudden 25 -> 100 jump made the camera director jump (2026-10-16)
    if (nt > 0) { const d0 = oFt.clone().sub(oCp).normalize(), d1 = A0.clone().add(v3(.3, .3, 0)).normalize(); oFt.copy(oCp).addScaledVector(d0.lerp(d1, sm(.1, 1, nt)).normalize(), D); }
    return { wd, fo, ed, nt, D };
  }
  const basis = (c, f) => { const fw = f.clone().sub(c).normalize(), rt = new T.Vector3().crossVectors(fw, Y1).normalize(); return [fw, rt, new T.Vector3().crossVectors(rt, fw)]; };
  // ---------------- third staging pass (2026-10-16), opening shot only (INTRO) ----------------
  // fireball: a bright green-white bolide with fragments and a glowing train, pinned to the sky seen at its mid time
  // star trails: arcs around a celestial pole placed in the sky view, growing like a time-lapse stack (each arc ends at its star)
  // constellations: Little Dipper (Polaris at the pole), Big Dipper, Cassiopeia; lines draw themselves star to star
  // beam: a soft volumetric light beam out of the telescope that sweeps the sky as the dome turns ("explore every corner")
  // barrier: a vast geodesic hexagon lattice (sphere around us) that flashes into view where the rocket touches it, a ripple racing
  //   across the sky; on "cage" the whole lattice shows, shimmering, and the view widens
  let FX = null;
  if (INTRO) {
    const RS = 1380, tanV = Math.tan(21 * Math.PI / 180), tanH = tanV * ctx.W / ctx.H;
    const skyDir = (tt, x, y) => { camAt(tt, mcp, mft, mtg); const [fw, rt, uv] = basis(mcp, mft), sx = (x - .5) * 2 - 2 * (p.side == null ? .12 : p.side) * (ctx.VERT ? 0 : 1);
      return fw.clone().addScaledVector(rt, sx * tanH).addScaledVector(uv, (.5 - y) * 2 * tanV).normalize(); };
    // pole + local basis on the sky
    const PL = skyDir(tTr + 2.5, .68, .27); camAt(tTr + 2.5, mcp, mft, mtg); const [, rt0, uv0] = basis(mcp, mft);
    const pr = rt0.clone().addScaledVector(PL, -rt0.dot(PL)).normalize(), pu = new T.Vector3().crossVectors(pr, PL).normalize().multiplyScalar(-1);
    if (pu.dot(uv0) < 0) pu.negate();
    const dOf = (x, y) => PL.clone().addScaledVector(pr, Math.tan(x * Math.PI / 180)).addScaledVector(pu, Math.tan(y * Math.PI / 180)).normalize();
    const CON = [
      { s: .75, o: [0, 0], st: [[0, 0], [-3.5, 2], [-5.5, 4.5], [-6.5, 8], [-11, 9.5], [-12, 12.5], [-8, 11]], ln: [[0, 1], [1, 2], [2, 3], [3, 4], [4, 5], [5, 6], [6, 3]], t: 0 },
      { s: .75, o: [-5, -13], st: [[0, 0], [-1, -5.5], [-8, -6.5], [-8.5, -1.5], [-15, -.5], [-20.5, -1.5], [-27, -5]], ln: [[0, 1], [1, 2], [2, 3], [3, 0], [3, 4], [4, 5], [5, 6]], t: 1.0 },
      { s: .6, o: [6, 2], st: [[0, 0], [5, -4], [9, -1], [14, -4], [18, 1]], ln: [[0, 1], [1, 2], [2, 3], [3, 4]], t: 2.0 }];
    const cStars = [], cLines = [];
    CON.forEach(c => { const base = cStars.length; c.st.forEach(([x, y], k) => cStars.push({ d: dOf(c.o[0] + x * c.s, c.o[1] + y * c.s), b: k === 0 && c.t === 0 ? 1.5 : 1, t: tLn + c.t + .25 * k }));
      c.ln.forEach(([a, b], k) => cLines.push({ a: base + a, b: base + b, t0: tLn + c.t + .22 * k })); });
    cStars.forEach(cs => { const l = cLines.filter(q => q.a === cStars.indexOf(cs) || q.b === cStars.indexOf(cs)); cs.t = l.length ? Math.min(...l.map(q => q.t0)) - .1 : cs.t; });
    const cSpr = cStars.map(cs => { const g = glow(S, '#fff4e0', 1, 0); g.position.copy(cs.d).multiplyScalar(RS); g.renderOrder = -1; return g; });
    const cL = streaks(S, cLines.length, { minPx: 1.3, near: [0, 1], order: -1 });
    // star-trail arcs (bright classes + a third of the faint field + the constellation stars)
    const tl = []; starSets.forEach(({ P, base, n }, si) => { const a = P.geometry.attributes.position.array; for (let i = 0; i < n; i++) { if (si < 2) continue; const k = i * 4; tl.push([a[i * 3] / SR, a[i * 3 + 1] / SR, a[i * 3 + 2] / SR, base[k], base[k + 1], base[k + 2]]); } });
    cStars.forEach(cs => tl.push([cs.d.x, cs.d.y, cs.d.z, 1.3, 1.25, 1.15]));
    const NSG = 28, tg = new T.BufferGeometry(), tpA = new Float32Array(tl.length * NSG * 6), tsA = new Float32Array(tl.length * NSG * 2), tcA = new Float32Array(tl.length * NSG * 6);
    tl.forEach((q, i) => { for (let j = 0; j < NSG; j++) for (let e = 0; e < 2; e++) { const v = (i * NSG + j) * 2 + e; tpA.set([q[0], q[1], q[2]], v * 3); tsA[v] = (j + e) / NSG; tcA.set([q[3], q[4], q[5]], v * 3); } });
    tg.setAttribute('position', new T.BufferAttribute(tpA, 3)); tg.setAttribute('aS', new T.BufferAttribute(tsA, 1)); tg.setAttribute('aC', new T.BufferAttribute(tcA, 3));
    const trU = { uP: { value: PL }, uA: { value: 0 }, uOp: { value: 0 } };
    const trl = new T.LineSegments(tg, new T.ShaderMaterial({ uniforms: trU, transparent: true, depthWrite: false, blending: T.AdditiveBlending,
      vertexShader: `attribute float aS; attribute vec3 aC; uniform vec3 uP; uniform float uA, uOp; varying vec3 vC;
        void main(){ vec3 d = normalize(position); float a = aS * uA, c = cos(a), s = sin(a); vec3 r = d * c + cross(uP, d) * s + uP * dot(uP, d) * (1. - c);
          vC = aC * uOp * (1.05 - .35 * aS); gl_Position = projectionMatrix * viewMatrix * vec4(r * ${RS}., 1.); }`,
      fragmentShader: `varying vec3 vC; void main(){ gl_FragColor = vec4(vC, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
    trl.frustumCulled = false; trl.renderOrder = -1; S.add(trl);
    // fireball path on the sky
    const fA = skyDir(tFb + .6, .82, .14).multiplyScalar(RM), fB = skyDir(tFb + .6, .4, .5).multiplyScalar(RM), fbS = streaks(S, 8, { minPx: 1.8, near: [50, 120], order: -1 });
    const fbG = glow(S, '#e8fff0', 1, 0); fbG.renderOrder = -1; const fragD = []; { const r = rng(97); for (let k = 0; k < 6; k++) fragD.push([r() - .5, r() - .5, .55 + .4 * r()]); }
    // beam out of the telescope (TUBE local +y), soft across its width, fading along its length, drifting motes
    const BL = 700, bmU = { uOp: { value: 0 }, uT: { value: 0 } };
    const beam = new T.Mesh(new T.CylinderGeometry(60, .45, BL, 40, 1, true).translate(0, 2.2 + BL / 2, 0), new T.ShaderMaterial({ uniforms: bmU, transparent: true, depthWrite: false, blending: T.AdditiveBlending, side: T.DoubleSide,
      vertexShader: `varying float vH; varying vec3 vN, vV; void main(){ vH = (position.y - 2.2) / ${BL}.; vec4 mv = modelViewMatrix * vec4(position, 1.); vN = normalize(normalMatrix * normal); vV = normalize(-mv.xyz); gl_Position = projectionMatrix * mv; }`,
      fragmentShader: `uniform float uOp, uT; varying float vH; varying vec3 vN, vV;
        void main(){ float f = pow(abs(dot(normalize(vN), normalize(vV))), 2.2), h = clamp(vH, 0., 1.);
          float m = .78 + .22 * sin(h * 90. - uT * 2.3) * sin(h * 37. + uT * 1.1);
          vec3 c = mix(vec3(1., .86, .62), vec3(.62, .74, 1.), smoothstep(0., .5, h)) * f * pow(1. - h, 1.7) * smoothstep(0., .004, h) * m * uOp * .3;
          gl_FragColor = vec4(c, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` }));
    beam.renderOrder = 3; TUBE.add(beam); const bmF = glow(TUBE, '#fff0d6', 4, 0); bmF.position.y = 2.4; bmF.renderOrder = 4;
    // barrier
    let bar = null, barU = null, CW = null, flW = null;
    if (tWl < 1e8) { const tw = tWl - tR, ax = path0(tauD + .05).sub(path0(tauD)).normalize(); CW = path(tw).addScaledVector(ax, 22.2 * 1.15); const RB = CW.length();
      const g = new T.IcosahedronGeometry(RB, 15), np = g.attributes.position.count, pa = g.attributes.position.array, B = new Float32Array(np * 3), C0 = new Float32Array(np * 3), C1 = new Float32Array(np * 3), C2 = new Float32Array(np * 3);
      for (let f = 0; f < np / 3; f++) for (let k = 0; k < 3; k++) { const v = f * 3 + k; B[v * 3 + k] = 1; for (let q = 0; q < 3; q++) { C0[v * 3 + q] = pa[f * 9 + q]; C1[v * 3 + q] = pa[f * 9 + 3 + q]; C2[v * 3 + q] = pa[f * 9 + 6 + q]; } }
      g.setAttribute('aB', new T.BufferAttribute(B, 3)); g.setAttribute('aP0', new T.BufferAttribute(C0, 3)); g.setAttribute('aP1', new T.BufferAttribute(C1, 3)); g.setAttribute('aP2', new T.BufferAttribute(C2, 3));
      barU = { uC: { value: CW.clone().normalize() }, uK: { value: new T.Color(ctx.ACC) }, uT: { value: -9 }, uCage: { value: 0 }, uTime: { value: 0 } };
      bar = new T.Mesh(g, new T.ShaderMaterial({ uniforms: barU, transparent: true, depthWrite: false, blending: T.AdditiveBlending, side: T.DoubleSide,
        vertexShader: `attribute vec3 aB, aP0, aP1, aP2; varying vec3 vB, vD, vQ0, vQ1, vQ2;
          void main(){ vB = aB; vD = normalize(position); vQ0 = normalize(aP0); vQ1 = normalize(aP1); vQ2 = normalize(aP2); gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }`,
        fragmentShader: `uniform vec3 uC, uK; uniform float uT, uCage, uTime; varying vec3 vB, vD, vQ0, vQ1, vQ2;
          float hh(vec3 p){ return fract(sin(dot(p, vec3(12.9898, 78.233, 37.719))) * 43758.5453); }
          void main(){ vec3 b = vB; float m1 = max(b.x, max(b.y, b.z)), m3 = min(b.x, min(b.y, b.z)), m2 = b.x + b.y + b.z - m1 - m3, e = m1 - m2, fw = max(fwidth(e), 1e-5);
            float line = 1. - smoothstep(fw * .5, fw * 2., e);
            vec3 cc = b.x >= m1 ? vQ0 : (b.y >= m1 ? vQ1 : vQ2); float cr = hh(floor(cc * 300.));
            float ang = acos(clamp(dot(normalize(vD), uC), -1., 1.)), fr = uT * .42;
            float ring = uT > 0. ? exp(-pow((ang - fr) / .07, 2.)) * exp(-uT * .16) : 0.;
            float lit = uT > 0. ? step(ang, fr) * exp(-(fr - ang) * 4.5) * (.35 + .65 * cr) * exp(-uT * .15) : 0.;
            float rr = mod(max(uT, 0.), 1.9), ring2 = uT > 1.9 ? exp(-pow((ang - rr * .5) / .05, 2.)) * .4 * exp(-rr * .9) : 0.;
            float pre = smoothstep(-1.1, 0., uT) * (1. - smoothstep(0., .8, uT)) * exp(-ang / .05);
            float hot = uT > 0. ? exp(-ang / .045) * (.35 + .65 * exp(-uT * .7)) : 0.;
            float cage = uCage * (.42 + .25 * sin(uTime * 1.2 + cr * 6.283 + ang * 3.)) + .012 * smoothstep(1.5, 4., uT);
            float rise = smoothstep(0., .22, uT); ring *= rise; lit *= rise; hot *= rise;
            float I = line * (ring * 1.5 + lit * .5 + ring2 + pre * 1.4 + hot * 1.6 + cage) + (1. - line) * (ring * .1 + hot * .25 + uCage * .03) * (.4 + .6 * cr);
            vec3 col = mix(vec3(.4, .62, 1.), uK, clamp(hot * 1.2 + pre, 0., 1.));
            gl_FragColor = vec4(col * I, 1.);
            #include <tonemapping_fragment>
            #include <colorspace_fragment>
          }` }));
      bar.frustumCulled = false; bar.renderOrder = -1; S.add(bar);
      flW = glow(S, '#fff3dc', 1, 0); flW.position.copy(CW); flW.renderOrder = 3; }
    const vA = new T.Vector3(), vB = new T.Vector3();
    FX = { draw(t) {
      // star trails
      const tx = Math.min(1, Math.max(0, (t - tTr) / 5.5)), trO = sm(tTr, tTr + 1, t) * (1 - sm(tBm - 1.6, tBm + .6, t));
      trl.visible = trO > 0; trU.uA.value = .42 * tx * tx * tx * (tx * (tx * 6 - 15) + 10) + .03 * sm(tTr, tTr + .5, t); trU.uOp.value = 1.0 * trO;
      // constellations
      const lnO = 1 - sm(tBm - 1.6, tBm + .6, t);
      cStars.forEach((cs, k) => { const a = sm(cs.t, cs.t + .3, t) * lnO; cSpr[k].visible = a > 0; cSpr[k].scale.setScalar(RS * 2 * tanV / ctx.H * (9 + 6 * cs.b) * (1 + .08 * Math.sin(t * 2.3 + k))); cSpr[k].material.opacity = .85 * a; });
      cLines.forEach((q, k) => { const g = sm(q.t0, q.t0 + .35, t), a = g * lnO; if (a <= 0) { cL.hide(k); return; }
        vA.copy(cStars[q.a].d).multiplyScalar(RS); vB.copy(cStars[q.b].d).multiplyScalar(RS); const hd = vA.clone().lerp(vB, g);
        cL.set(k, hd.x, hd.y, hd.z, vA.x, vA.y, vA.z, RS * 2 * tanV / ctx.H * 2.4, 1.0 * a, .82 * a, .5 * a); });
      cL.commit();
      // fireball: 1.15 s across, accelerating slightly; flare near the end; fragments; the train lingers ~2.5 s
      const fs = (t - tFb) / 1.15, live = fs > 0 && fs < 1, fe = Math.min(1, Math.max(0, fs)), hp = fe * (.8 + .2 * fe);
      const hd = fA.clone().lerp(fB, hp), dir = fB.clone().sub(fA).normalize(), L = fA.distanceTo(fB);
      const bri = live ? sm(0, .12, fs) * (.6 + .4 * fs + 1.4 * sm(.66, .78, fs) * (1 - sm(.8, 1, fs))) * (1 - sm(.9, 1, fs)) : 0;
      if (bri > 0) fbS.set(0, hd.x, hd.y, hd.z, hd.x - dir.x * L * .2, hd.y - dir.y * L * .2, hd.z - dir.z * L * .2, RM * .003, 1.5 * bri, 1.9 * bri, 1.4 * bri); else fbS.hide(0);
      const trn = fs > 0 ? sm(0, .15, fs) * (1 - sm(1, 3.2, fs)) * .22 : 0;
      if (trn > 0) { const tp = fA.clone().lerp(fB, Math.max(.05, hp * .15)); fbS.set(1, hd.x, hd.y, hd.z, tp.x, tp.y, tp.z, RM * .006, .35 * trn, .9 * trn, .6 * trn); } else fbS.hide(1);
      for (let k = 0; k < 6; k++) { const fq = (fs - .8) / .5, f = fragD[k]; if (fq <= 0 || fq >= 1) { fbS.hide(2 + k); continue; }
        const pp = fA.clone().lerp(fB, .8 * (.8 + .16)).addScaledVector(dir, L * .25 * fq * f[2]).add(vA.set(f[0], f[1], 0).multiplyScalar(L * .05 * fq)), b2 = (1 - fq) * .9;
        fbS.set(2 + k, pp.x, pp.y, pp.z, pp.x - dir.x * L * .03, pp.y - dir.y * L * .03, pp.z - dir.z * L * .03, RM * .001, 1.4 * b2, 1.1 * b2, .6 * b2); }
      fbS.commit(); fbG.visible = bri > 0; if (bri > 0) { fbG.position.copy(hd); fbG.scale.setScalar(RM * 2 * tanV / ctx.H * (60 + 110 * bri)); fbG.material.opacity = .6 * Math.min(1, bri); }
      // beam (comes on at "beam", gone before the launch)
      const bo = sm(tBm, tBm + .5, t) * (1 - sm(tR - 2.6, tR - 1.6, t)); beam.visible = bo > 0; bmU.uOp.value = bo; bmU.uT.value = t;
      const bf = sm(tBm - .15, tBm + .1, t) * (1 - sm(tBm + .1, tBm + 1.4, t)); bmF.visible = bf > 0; bmF.material.opacity = .8 * bf; bmF.scale.setScalar(4 + 10 * bf);
      // barrier
      if (bar) { const ut = t - tWl; barU.uT.value = ut; barU.uCage.value = sm(tCg, tCg + 2.6, t); barU.uTime.value = t; bar.visible = ut > -1.2;
        const fl = sm(-.1, .1, ut) * (1 - sm(.1, 1.8, ut)); flW.visible = fl > 0; flW.material.opacity = .9 * fl; flW.scale.setScalar(CW.length() * (.05 + .1 * sm(-.1, 1, ut))); }
    } };
  }
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const { wd, fo, ed, nt, D } = camAt(t, cp, ft, tgt), tau = t - tR;
    const g1 = at(p.glow, 2.5), sc1 = at(p.scope, 2.2), cl = at(p.close, 6);
    // launch rumble: a tiny, smooth (2-3 Hz sines) wobble of the look-at point right after ignition, gone within ~7 s
    const rb = tR < 1e8 ? sm(-.4, .3, tau) * (1 - sm(1.5, 7, tau)) : 0;
    if (rb > 0) { const [, rt, uv] = basis(cp, ft), a = .0016 * D * rb;
      ft.addScaledVector(rt, a * (Math.sin(t * 19.1) * .6 + Math.sin(t * 12.7 + 1.3) * .4)).addScaledVector(uv, a * (Math.sin(t * 16.3 + .7) * .6 + Math.sin(t * 9.9 + 2.1) * .4)); }
    cam.position.copy(cp);
    // dome: slit first faces left-back, on "telescopes" it turns toward the camera side; shutter opens fully
    const bmK = INTRO ? Math.min(1, Math.max(0, (t - tBm) / Math.max(1, (p.scope != null ? cue(p.scope) : tBm + 4) + 2.2 - tBm))) : 0, swp = Math.pow(Math.sin(Math.PI * bmK), 2), bmO = INTRO ? sm(tBm - .3, tBm + .5, t) : 0;
    DOME.rotation.y = PSC + 1.75 - 1.6 * sc1 + .04 * Math.sin(u * .2) - .8 * swp;
    SHUT.rotation.x = -(0.55 + .45 * g1 + (GM - 1.0) * (sc1 + .6 * bmO * (1 - sc1)));
    if (LEAF) { const c1 = sm(0, .7, cl), c2 = sm(.3, 1, cl); SHUT.rotation.x *= 1 - c1; LEAF.rotation.x = -(2.36 - (2.36 - (SHD - .04)) * c2); }
    const el = .7 + .2 * g1 - .15 * sc1 + (cl > 0 ? (1.45 - (.7 + .2 * g1 - .15 * sc1)) * cl : 0) + .3 * swp; TUBE.quaternion.setFromUnitVectors(v3(0, 1, 0), v3(0, Math.sin(el), Math.cos(el)));
    const lit = (.25 + .75 * g1) * (1 - .85 * cl); innerM.emissiveIntensity = .035 * lit; inGlow.material.opacity = .3 * lit + .15 * sc1; edgeM.opacity = .25 + .55 * lit;
    mirror.material.color.setRGB(1 * lit + .2, .89 * lit + .15, .69 * lit + .1);
    rimGlow.material.opacity = .45 + .25 * g1;
    // starlight stream: points flow from the sky down into the slit and the telescope mouth
    const dir = v3(0, Math.sin(el), Math.cos(el)), mouth = dir.clone().multiplyScalar(2.6).add(v3(0, .35, 0)), sk = (.9 * g1 + .4 * sc1) * (1 - cl);
    for (let i = 0; i < NS; i++) { const [o, a, b, w] = slB[i], f = (o + t * .22 * (1 + w)) % 1, d = (1 - f) * 34; const spread = .2 + (1 - f) * 2.6;
      slA[i * 3] = mouth.x + dir.x * d + a * spread; slA[i * 3 + 1] = mouth.y + dir.y * d + b * spread * .4; slA[i * 3 + 2] = mouth.z + dir.z * d + b * spread;
      const v = sk * Math.sin(Math.PI * f) * (.4 + .6 * w); slC[i * 3] = v; slC[i * 3 + 1] = v * .92; slC[i * 3 + 2] = v * .75; }
    sl.geometry.attributes.position.needsUpdate = true; sl.geometry.attributes.color.needsUpdate = true;
    // stars twinkle (the bright classes scintillate more, two beating frequencies)
    starSets.forEach(({ P, c, base, n }, si) => { const am = si >= 2 ? .3 : .18;
      for (let i = 0; i < n; i++) { const k = i * 4, ph = base[k + 3], tw = 1 - am + am * Math.sin(t * (1.3 + (ph % 1) * 2) + ph * 7) * (si >= 2 ? .6 + .4 * Math.sin(t * .7 + ph * 3) : 1); c[i * 3] = base[k] * tw; c[i * 3 + 1] = base[k + 1] * tw; c[i * 3 + 2] = base[k + 2] * tw; } P.geometry.attributes.color.needsUpdate = true; });
    // deep field: the first 40 galaxies come with the push, the rest emerge one by one through the rest of the shot
    const edL = p.edge != null ? sm(tE + 1, ctx.t1 - 1, t) : 0;
    gal.forEach(([sp, o, st]) => { const e = st < 0 ? ed : .8 * sm(st * .85, st * .85 + .15, edL); sp.material.opacity = Math.max(e, .8 * nt) * (.25 + .35 * o); });
    skyK.setScalar(1 + .25 * Math.max(ed, .6 * nt) + .1 * edL); agU.uT.value = t;
    // meteor (one, early)
    const mt = (t - 4.6) / .8; met.visible = !INTRO && mt > 0 && mt < 1;
    if (met.visible) { const a = v3(-380, 820, -1000), b = v3(-640, 620, -980), m = a.clone().lerp(b, mt); met.position.copy(m); met.scale.set(160 * Math.min(1, mt * 3), 6, 1); met.lookAt(0, 0, 0); met.rotateZ(Math.atan2(b.y - a.y, b.x - a.x) + Math.PI); met.material.opacity = Math.sin(Math.PI * mt) * .9; }
    // slow meteors (2 slots on fixed periods, ~80% of slots fire), pinned to the sky seen at their mid time, in the right part of the frame
    const th = .38, asp = ctx.W / ctx.H;
    for (let j = 0; j < 2; j++) { const P = [13.7, 21.3][j], ph = [5.1, 14.4][j], kk = Math.floor((t + ph) / P), tm0 = kk * P - ph, s = (t - tm0) / 1.8;
      const ok = s < 1 && h1(kk * 7.1 + j * 31) < .8 && (CALM ? t > ctx.t0 + 3 : (t > ctx.t0 + 7 && t < tR - 2.5));
      if (!ok) { mets.hide(j); continue; }
      camAt(tm0 + .9, mcp, mft, mtg); const [fw, rt, uv] = basis(mcp, mft), hx = h1(kk * 3.3 + j * 5), hy = h1(kk * 5.7 + j * 9), ha = h1(kk * 2.1 + j * 13);
      const X0 = (-.05 + .5 * hx) * th * asp, Y0 = (.5 + .28 * hy) * th, an = -(.2 + .4 * ha), sg = hx > .5 ? -1 : 1, L = (.2 + .15 * hy) * th * RM;
      const dv = rt.clone().multiplyScalar(Math.cos(an) * sg).addScaledVector(uv, Math.sin(an)), base = mcp.clone().addScaledVector(fw, RM).addScaledVector(rt, X0 * RM).addScaledVector(uv, Y0 * RM);
      const hd = base.clone().addScaledVector(dv, L * s), tl = hd.clone().addScaledVector(dv, -L * .4 * Math.min(1, s * 2.5)), br = Math.pow(Math.sin(Math.PI * s), .8) * (.7 + .6 * h1(kk * 9.9 + j));
      mets.set(j, hd.x, hd.y, hd.z, tl.x, tl.y, tl.z, RM * .0018, 1.4 * br, 1.5 * br, 1.8 * br); }
    mets.commit();
    // a satellite glides over in the calm shots and fades into Earth's shadow
    { const ts0 = ctx.t0 + 5, s = (t - ts0) / 26; sat.visible = CALM && s > 0 && s < 1;
      if (sat.visible) { camAt(ts0 + 13, mcp, mft, mtg); const [fw, rt, uv] = basis(mcp, mft);
        sat.position.copy(mcp).addScaledVector(fw, RM).addScaledVector(rt, (.8 - .7 * s) * th * asp * RM).addScaledVector(uv, (.62 - .3 * s) * th * RM);
        sat.scale.setScalar(RM * 2 * th / ctx.H * 7); sat.material.opacity = .7 * sm(0, .06, s) * (1 - sm(.72, .95, s)); } }
    // rocket
    ROCK.visible = !((p.night != null || p.close != null) && p.rocket == null); const live = ROCK.visible && tau > -1.2;
    tr.visible = smk.visible = core.mesh.visible = live; cTrail.mesh.visible = live && tau > .1;
    const flash = sm(-.25, .05, tau) * (1 - sm(.05, 1.9, tau)), rs = sm(-.05, .25, tau) * (1 - sm(.4, 2.8, tau));
    flash1.material.opacity = .7 * flash; flashA.material.opacity = .35 * flash; flashA.scale.set(260 + 160 * sm(-.25, 1.5, tau), 5, 1); flash1.visible = flashA.visible = flash > 0;
    shRing.visible = rs > 0; ringM.opacity = .5 * rs; { const rr = 10 + 200 * (1 - Math.exp(-Math.max(0, tau) / 1.1)); shRing.scale.set(rr, 1, rr); }
    if (ROCK.visible) { const ign = sm(-1.2, 0, tau), q = path(tau), tq = Math.min(tau, tauD), q2 = q.clone().add(path0(tq + .05).sub(path0(tq))); ROCK.position.copy(q);
      const dv = q2.clone().sub(q); if (dv.lengthSq() > 1e-6) ROCK.quaternion.setFromUnitVectors(v3(0, 1, 0), dv.normalize()); else ROCK.quaternion.identity();
      const ax = v3(0, 1, 0).applyQuaternion(ROCK.quaternion), noz = q.clone().addScaledVector(ax, -1.5);
      const fk = .85 + .15 * Math.sin(t * 37) * Math.sin(t * 23);
      fl1.material.opacity = .95 * ign * fk; fl2.material.opacity = .45 * ign * fk; fl1.scale.set(1, .6 + .4 * ign + .25 * sm(0, 4, tau), 1); fl2.scale.set(1 + sm(0, 6, tau) * .6, .6 + .8 * sm(0, 4, tau), 1 + sm(0, 6, tau) * .6);
      fg1.material.opacity = .9 * ign * fk; fg2.material.opacity = .32 * ign;
      const dist = cam.position.distanceTo(q), grow = Math.max(1, dist / 900); fg1.scale.setScalar(9 * grow); fg2.scale.setScalar(40 * grow);
      padG.material.opacity = (.5 * ign + .35 * flash) * (1 - sm(2, 8, tau));
      vapor.material.opacity = .45 * sm(5.4, 5.8, tau) * (1 - sm(6, 7.8, tau)); vapor.scale.setScalar(10 * grow);
      if (live) {
        // hot core streak (length follows the speed) and a wider warm glow streak behind the nozzle
        const c1 = path(Math.max(0, tau - .3)), c2 = path(Math.max(0, tau - .7));
        core.set(0, noz.x, noz.y, noz.z, c1.x, c1.y, c1.z, 2.4, 3 * ign * fk, 2.2 * ign * fk, 1.3 * ign * fk);
        core.set(1, noz.x, noz.y, noz.z, c2.x, c2.y, c2.z, 7, .9 * ign, .5 * ign, .25 * ign); core.commit();
        // trail particles: particle i was emitted at te after lift-off, drifts and swells with age
        const span = Math.max(0, Math.min(tau, TSPAN));
        for (let i = 0; i < NT; i++) { const [te, a, b, c, w] = trB[i]; let v = 0;
          if (te < span) { const age = tau - te, e = path(te), sp2 = .6 + age * (1.2 + w * 1.5);
            trA[i * 3] = e.x + a * sp2 + age * 1.5; trA[i * 3 + 1] = e.y + b * sp2 - age * 2; trA[i * 3 + 2] = e.z + c * sp2;
            v = 1.3 * Math.exp(-age * .3) * (age < .25 ? 1.6 : 1) * (.5 + .5 * w); trS[i] = .8 + age * .7; }
          else { trA[i * 3 + 1] = -9999; trS[i] = 0; }
          trC[i * 3] = v; trC[i * 3 + 1] = v * (.72 + .2 * Math.exp(-tau + te)); trC[i * 3 + 2] = v * (.45 + .3 * Math.exp(-tau + te)); }
        ['position', 'color', 'size'].forEach(k => trG.attributes[k].needsUpdate = true);
        // contrail ribbon: from the oldest kept point up to just behind the nozzle; moonlit smoke, warm where it is young
        if (tau > .1) { const ta = Math.max(0, tau - TSPAN), tb = tau - .08;
          for (let i = 0; i < NRB; i++) { const te = ta + (tb - ta) * Math.pow(i / (NRB - 1), .7), age = tau - te, e = path(te), e2 = path(te + .05).sub(e).normalize();
            e.x += age * 1.5; e.y -= age * 2;
            const sm1 = Math.exp(-age / 14) / (1 + age * .12), wm = Math.exp(-age * 1.3) * ign, fade = sm(0, .25, age) * sm(0, 2, te + 1);
            cTrail.set(i, e, e2, 1.6 + age * 1.1, (.34 * sm1 + 1.3 * wm) * fade, (.36 * sm1 + .75 * wm) * fade, (.48 * sm1 + .38 * wm) * fade); }
          cTrail.commit(); }
        // launch steam / smoke
        for (let i = 0; i < NSm; i++) { const B = smB[i], age = tau - B.te;
          if (age > 0 && age < B.life) {
            const dr = B.v0 * B.td * (1 - Math.exp(-age / B.td)), bu = B.up * age * (1 + age * .04), sw = Math.sin(age * .35 + B.ph) * age * .35;
            const x = PAD.x + B.dir.x * dr + B.dir.z * sw + age * .8, z = PAD.z + B.dir.z * dr - B.dir.x * sw, dp = (x - PAD.x) ** 2 + (z - PAD.z) ** 2;
            const yb = B.lat ? PAD.y - 32 * (1 - Math.exp(-dp / 6000)) + 1.2 : PAD.y + 1, y = yb + B.y0 + bu;
            smA[i * 3] = x; smA[i * 3 + 1] = y; smA[i * 3 + 2] = z;
            smZ[i] = (B.s0 + 7 * Math.sqrt(age) * (B.lat ? 1 : 1.3)) * 1.3;
            const L = ign * (1 - sm(1.5, 9, tau)) * Math.exp(-Math.max(0, y - PAD.y) / 12) * Math.exp(-dr / 45) + flash * .8, bb = .75 + .35 * B.w;
            smC[i * 4] = .25 * bb + 1.5 * L * 1.4; smC[i * 4 + 1] = .26 * bb + .85 * L * 1.4; smC[i * 4 + 2] = .35 * bb + .42 * L * 1.4;
            smC[i * 4 + 3] = sm(0, .3, age) * (1 - sm(B.life * .55, B.life, age)) * (.58 + .3 * B.w); }
          else { smC[i * 4 + 3] = 0; smZ[i] = 0; } }
        ['position', 'col', 'sz'].forEach(k => smG.attributes[k].needsUpdate = true); } }
    cam.lookAt(ft);
    // fov: on "edge" the push keeps creeping in slowly to the end of the shot (the deep field opens up)
    const edZ = p.edge != null ? sm(tE + 3, ctx.t1 + 4, t) : 0;
    cam.fov = 42 - 4 * wd + 4 * fo - 10 * ed + 10 * nt - 5 * edZ + 13 * (tCg < 1e8 ? sm(tCg - .4, tCg + 3.2, t) : 0);
    if (ctx.VERT) { const h = 2 * Math.atan(Math.tan(cam.fov * Math.PI / 360) * 16 / 9 * .62); cam.fov = 2 * Math.atan(Math.tan(h / 2) * ctx.H / ctx.W) * 180 / Math.PI; }   // Shorts: same vertical fit as ctx.side()
    cam.updateProjectionMatrix(); cam.updateMatrixWorld();
    const scl = ctx.H / (2 * Math.tan(cam.fov * Math.PI / 360)); trU.uScale.value = smU.uScale.value = scl;
    dust.update(t, [cp.x - 10, cp.y + 4, cp.z - 20]);
    if (FX) FX.draw(t);
    // bokeh motes near the lens: world-fixed in a box that follows the view, slow drift, kept off the title block and caption band
    { const fw = ft.clone().sub(cp).normalize(), cx = cp.x + fw.x * 6, cy = cp.y + fw.y * 6, cz = cp.z + fw.z * 6, wr = (v, sz) => ((v % sz) + sz * 1.5) % sz - sz / 2, kb = CALM ? .16 : .08;
      for (let i = 0; i < NBK; i++) { const b = bkB[i];
        vt.set(cx + wr(b[0] + Math.sin(t * .05 + b[4]) * 1.2 - cx, 14), cy + wr(b[1] + t * .035 * (.4 + b[3]) - cy, 8), cz + wr(b[2] + Math.cos(t * .04 + b[4]) * 1.2 - cz, 14));
        bkA[i * 3] = vt.x; bkA[i * 3 + 1] = vt.y; bkA[i * 3 + 2] = vt.z;
        const d = vt.distanceTo(cp); let al = sm(1.8, 3.5, d) * (1 - sm(7, 9.5, d)) * (.5 + .5 * Math.sin(t * .3 + b[4]));
        if (al > 0) { vt.project(cam); al *= sm(-.5, -.1, vt.x) * sm(-.8, -.55, vt.y); }
        const v = al * kb * (.6 + .4 * b[3]); bkC[i * 3] = v; bkC[i * 3 + 1] = v * .86; bkC[i * 3 + 2] = v * .66; }
      bk.geometry.attributes.position.needsUpdate = true; bk.geometry.attributes.color.needsUpdate = true; }
  } };
};
