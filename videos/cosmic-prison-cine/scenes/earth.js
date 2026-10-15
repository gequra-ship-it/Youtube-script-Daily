// earth — a realistic Earth backlit by the Sun (cosmic-prison-cine S45, S49-S51; written 2026-10-15). Procedural globe (no real map
// asset): continents with deserts, forests, ice caps, shallow shelves; day/night terminator with a warm edge, city lights on the
// night side as soft warm specks, ocean sun glint, a separate cloud shell that casts soft shadows, a thin blue atmosphere rim that
// glows strongest toward the Sun (forward scattering), the Moon nearby, the Sun behind. The same world continues outward at
// symbolic scale: the Solar System (Sun, faint gold orbit lines, planets as small glowing points), the neighbouring stars, and the
// Milky Way disc. No text, no labels.
// Each cue drives the camera; a shot normally gets ONE of them (the scene picks its camera story from the cue it is given):
//   grain  S45 "a tiny grain of sand": from close, the camera pulls very far back (past the Moon, the orbits, the neighbouring
//          stars) until Earth is a pale blue dot, a tiny grain inside the Milky Way
//   oasis  S49-50 "our local realm ... vast beyond imagination": the camera rises from Earth over the Solar System (planets as small
//          glowing points on faint orbit lines), then farther out among the neighbouring stars
//   mind   S51 "a pale blue dot": the shot opens far out on the pale blue dot in the void and returns close to Earth's night side
//          (city lights, the backlit atmosphere ring)
//   side   subject offset (default .12)
// Without a cue: a slow drift close to Earth (half lit, city lights on the night half, the Moon to the right).
(window.MIYA = window.MIYA || { scenes: {} }).scenes.earth = function (ctx, p) {
  const { T, sm, rng, cue, glow, ctex } = ctx, M = window.MIYA, K = M.kit;
  const S = new T.Scene(); S.background = new T.Color('#03040d');
  const v3 = (x, y, z) => new T.Vector3(x, y, z);
  const cT = c => c == null ? null : cue(c);
  const cG = cT(p.grain), cO = cT(p.oasis), cM = cT(p.mind);

  // ---------------- textures (made once per page, shared by every earth shot) ----------------
  if (!M._earthTex) {
    const hs = (x, y, z) => { let h = (x * 374761393 + y * 668265263 + z * 1274126177) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };
    const vn = (x, y, z) => { const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), xf = x - xi, yf = y - yi, zf = z - zi;
      const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf), w = zf * zf * (3 - 2 * zf), L = (a, b, k) => a + (b - a) * k;
      return L(L(L(hs(xi, yi, zi), hs(xi + 1, yi, zi), u), L(hs(xi, yi + 1, zi), hs(xi + 1, yi + 1, zi), u), v),
        L(L(hs(xi, yi, zi + 1), hs(xi + 1, yi, zi + 1), u), L(hs(xi, yi + 1, zi + 1), hs(xi + 1, yi + 1, zi + 1), u), v), w); };
    const fbm = (x, y, z, o) => { let s = 0, a = .5, f = 1, n = 0; for (let k = 0; k < o; k++) { s += a * vn(x * f, y * f, z * f); n += a; a *= .5; f *= 2.03; } return s / n; };
    const ss = (a, b, x) => { x = Math.min(1, Math.max(0, (x - a) / (b - a))); return x * x * (3 - 2 * x); };
    const W2 = 2048, H2 = 1024, mk = () => { const c = document.createElement('canvas'); c.width = W2; c.height = H2; return c; };
    const cd = mk(), cn = mk(), cc = mk(), co = document.createElement('canvas'); co.width = 1024; co.height = 512;
    const gd = cd.getContext('2d'), gn = cn.getContext('2d'), gc = cc.getContext('2d'), go = co.getContext('2d');
    const id = gd.createImageData(W2, H2), inn = gn.createImageData(W2, H2), ic = gc.createImageData(W2, H2), io = go.createImageData(1024, 512);
    const enc = v => Math.max(0, Math.min(255, Math.pow(Math.max(0, v), 1 / 2.2) * 255));
    for (let py = 0; py < H2; py++) { const lat = Math.PI / 2 - (py + .5) / H2 * Math.PI, cl = Math.cos(lat), y = Math.sin(lat);
      for (let px = 0; px < W2; px++) { const lon = (px + .5) / W2 * 2 * Math.PI, x = cl * Math.cos(lon), z = -cl * Math.sin(lon);
        const wx = fbm(x * 1.7 + 11, y * 1.7, z * 1.7, 3) - .5, wy = fbm(x * 1.7, y * 1.7 + 7, z * 1.7, 3) - .5;
        const h = fbm(x * 1.35 + wx * 1.3, y * 1.35 + wy * 1.3, z * 1.35, 6) - .53 + .04 * Math.abs(y);   // > 0 land
        const m = fbm(x * 2.4 + 3, y * 2.4 + 3, z * 2.4, 3), al = Math.abs(lat);
        let r, g, b;
        if (h > 0) { const dry = ss(.12, .42, al) * (1 - ss(.55, .75, al)) * ss(.45, .62, 1 - m), cold = ss(.9, 1.15, al), hi = ss(.06, .16, h);
          const n2 = fbm(x * 18, y * 18, z * 18, 2);
          r = .05 + .02 * n2; g = .09 + .04 * n2; b = .03;                                   // forest
          r += (.15 - r) * (1 - m) * .5; g += (.15 - g) * (1 - m) * .4; b += (.07 - b) * (1 - m) * .4;   // grass / steppe
          r += (.46 + .1 * n2 - r) * dry; g += (.34 + .06 * n2 - g) * dry; b += (.2 - b) * dry;          // desert
          r += (.26 - r) * cold * .7; g += (.25 - g) * cold * .7; b += (.22 - b) * cold * .7;             // tundra
          r += (.3 - r) * hi * .5; g += (.27 - g) * hi * .5; b += (.24 - b) * hi * .5;                    // mountains
          const ice = ss(1.12, 1.22, al + (m - .5) * .15); r += (.85 - r) * ice; g += (.88 - g) * ice; b += (.92 - b) * ice;
          // city lights: clustered, near coasts and in temperate bands, never on ice/desert
          const cluster = ss(.55, .75, fbm(x * 7 + 5, y * 7, z * 7, 3)), speck = Math.max(0, vn(x * 150, y * 150 + 3, z * 150) - .62) / .38, speck2 = Math.max(0, vn(x * 420 + 9, y * 420, z * 420) - .7) / .3;
          const coast = 1 - ss(0, .05, h), pop = (cluster * (.25 + .75 * coast) * (speck * speck * 1.2 + speck2 * .5) + coast * speck2 * .35) * (1 - ice) * (1 - .9 * dry) * (1 - ss(.95, 1.1, al));
          const k = (py * W2 + px) * 4, L2 = Math.min(1, pop * .9); inn.data[k] = enc(L2 * 1.0); inn.data[k + 1] = enc(L2 * .66); inn.data[k + 2] = enc(L2 * .32); inn.data[k + 3] = 255; }
        else { const sh = ss(-.05, 0, h), deep = .6 + .4 * fbm(x * 4, y * 4, z * 4, 2);
          r = .004 + .02 * sh; g = .02 * deep + .07 * sh; b = .07 * deep + .12 * sh;
          const ice = ss(1.3, 1.4, al + (m - .5) * .2); r += (.8 - r) * ice; g += (.85 - g) * ice; b += (.9 - b) * ice;
          const k = (py * W2 + px) * 4; inn.data[k] = inn.data[k + 1] = inn.data[k + 2] = 0; inn.data[k + 3] = 255;
          if ((py & 1) === 0 && (px & 1) === 0) { const ko = ((py >> 1) * 1024 + (px >> 1)) * 4; io.data[ko] = io.data[ko + 1] = io.data[ko + 2] = 255 * (1 - ice); io.data[ko + 3] = 255; } }
        if (h > 0 && (py & 1) === 0 && (px & 1) === 0) { const ko = ((py >> 1) * 1024 + (px >> 1)) * 4; io.data[ko] = io.data[ko + 1] = io.data[ko + 2] = 0; io.data[ko + 3] = 255; }
        const k = (py * W2 + px) * 4; id.data[k] = enc(r); id.data[k + 1] = enc(g); id.data[k + 2] = enc(b); id.data[k + 3] = 255;
        // clouds: banded, swirled fBm (r = cover, g = inner thickness shading)
        const sw = fbm(x * 2 + 1, y * 2, z * 2 + 9, 2) - .5, band = .5 + .5 * Math.cos(lat * 6.3 + sw * 3);
        const cv = fbm(x * 4.2 + sw * 1.4, y * 6.5, z * 4.2 + sw * 1.4, 6) * (.75 + .35 * band) - .02 * (1 - ss(.0, .25, al));
        const cover = ss(.5, .68, cv), th = fbm(x * 16 + 2, y * 16, z * 16, 3);
        ic.data[k] = cover * 255; ic.data[k + 1] = 255 * (.55 + .45 * th); ic.data[k + 2] = 0; ic.data[k + 3] = 255; } }
    gd.putImageData(id, 0, 0); gn.putImageData(inn, 0, 0); gc.putImageData(ic, 0, 0); go.putImageData(io, 0, 0);
    const tx = (c, srgb) => { const t2 = new T.CanvasTexture(c); t2.colorSpace = srgb ? T.SRGBColorSpace : T.NoColorSpace; t2.anisotropy = 8; t2.wrapS = T.RepeatWrapping; return t2; };
    // moon: grey with dark maria and soft crater spots
    const mc = document.createElement('canvas'); mc.width = 512; mc.height = 256; { const g = mc.getContext('2d'), im = g.createImageData(512, 256);
      for (let py = 0; py < 256; py++) { const lat = Math.PI / 2 - (py + .5) / 256 * Math.PI, cl = Math.cos(lat), y = Math.sin(lat);
        for (let px = 0; px < 512; px++) { const lon = (px + .5) / 512 * 6.283, x = cl * Math.cos(lon), z = -cl * Math.sin(lon);
          const mar = ss(.5, .6, fbm(x * 1.8 + 4, y * 1.8, z * 1.8, 4)), cr = fbm(x * 14, y * 14, z * 14, 3), v = (.62 - .3 * mar) * (.85 + .3 * cr), k = (py * 512 + px) * 4;
          im.data[k] = enc(v * .97); im.data[k + 1] = enc(v * .95); im.data[k + 2] = enc(v * .92); im.data[k + 3] = 255; } }
      g.putImageData(im, 0, 0); }
    M._earthTex = { day: tx(cd, true), night: tx(cn, true), cloud: tx(cc, false), ocean: tx(co, false), moon: tx(mc, true) };
  }
  const TX = M._earthTex;

  // ---------------- geometry of the world (Earth at the origin, radius 1; symbolic distances) ----------------
  const SUND = v3(-.88, .14, -.45).normalize(), SUN = SUND.clone().multiplyScalar(400);   // the Sun: behind Earth, to the left
  const UP = v3(0, 1, 0), NORB = UP.clone().addScaledVector(SUND, -UP.dot(SUND)).normalize();   // orbital plane contains Sun and Earth
  const OX = SUND.clone().negate(), OY = new T.Vector3().crossVectors(NORB, OX).normalize();     // in-plane axes (OX: Sun -> Earth)
  const sunCol = new T.Color('#fff1dc');

  const EG = new T.Group(); EG.rotation.z = .41; S.add(EG);   // axial tilt
  const sphere = new T.SphereGeometry(1, 160, 80);
  const eU = { day: { value: TX.day }, night: { value: TX.night }, cloud: { value: TX.cloud }, ocean: { value: TX.ocean }, sunPos: { value: SUN }, cOff: { value: 0 }, city: { value: 1 } };
  const earthM = new T.ShaderMaterial({ uniforms: eU,
    vertexShader: `varying vec2 vUv; varying vec3 vN; varying vec3 vP;
      void main() { vUv = uv; vN = normalize(mat3(modelMatrix) * normal); vec4 w = modelMatrix * vec4(position, 1.); vP = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `uniform sampler2D day, night, cloud, ocean; uniform vec3 sunPos; uniform float cOff, city; varying vec2 vUv; varying vec3 vN; varying vec3 vP;
      void main() { vec3 N = normalize(vN), L = normalize(sunPos - vP), V = normalize(cameraPosition - vP); float nl = dot(N, L);
        vec3 d = texture2D(day, vUv).rgb; float cs = texture2D(cloud, vUv + vec2(cOff + .002, -.002)).r, oc = texture2D(ocean, vUv).r;
        float dif = smoothstep(-.03, .12, nl) * (.1 + .9 * max(nl, 0.));
        vec3 sunC = mix(vec3(1., .55, .32), vec3(1., .96, .9), smoothstep(.0, .18, nl));
        vec3 col = d * sunC * dif * 1.8 * (1. - .5 * cs);
        vec3 H = normalize(L + V); float nh = max(dot(N, H), 0.), gl = oc * (1. - cs) * smoothstep(0., .15, nl);
        col += sunC * gl * (pow(nh, 90.) * 2.2 + pow(nh, 12.) * .06);
        float nf = smoothstep(.05, -.14, nl); col += texture2D(night, vUv).rgb * nf * (1. - .8 * cs) * 1.1 * city;
        float fr = pow(1. - max(dot(N, V), 0.), 2.6), sf = smoothstep(-.3, .5, nl);
        col += vec3(.25, .5, 1.) * fr * (sf * .9 + .02);
        col = mix(col, vec3(.2, .38, .8) * dif, .08 * sf);
        gl_FragColor = vec4(col, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` });
  const earth = new T.Mesh(sphere, earthM); EG.add(earth);
  const cU = { cloud: { value: TX.cloud }, sunPos: { value: SUN }, cOff: { value: 0 } };
  const cloudM = new T.ShaderMaterial({ uniforms: cU, transparent: true, depthWrite: false,
    vertexShader: earthM.vertexShader,
    fragmentShader: `uniform sampler2D cloud; uniform vec3 sunPos; uniform float cOff; varying vec2 vUv; varying vec3 vN; varying vec3 vP;
      void main() { vec3 N = normalize(vN), L = normalize(sunPos - vP), V = normalize(cameraPosition - vP); float nl = dot(N, L);
        vec4 c = texture2D(cloud, vUv + vec2(cOff, 0.)); float a = c.r;
        float dif = smoothstep(-.06, .18, nl) * (.15 + .85 * max(nl, 0.));
        vec3 sunC = mix(vec3(1., .72, .55), vec3(1.), smoothstep(.0, .2, nl));
        vec3 col = vec3(.92, .94, 1.) * sunC * dif * (.45 + .55 * c.g) * .95 + vec3(.004, .006, .012);
        float fr = 1. - max(dot(N, V), 0.); a *= 1. - .5 * pow(fr, 4.);
        gl_FragColor = vec4(col, a * .95);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` });
  const clouds = new T.Mesh(sphere, cloudM); clouds.scale.setScalar(1.008); EG.add(clouds);
  const aU = { sunPos: { value: SUN } };
  const atmo = new T.Mesh(new T.SphereGeometry(1.1, 128, 64), new T.ShaderMaterial({ uniforms: aU, side: T.BackSide, transparent: true, depthWrite: false, blending: T.AdditiveBlending,
    vertexShader: `varying vec3 vN; varying vec3 vP; varying vec3 vNv;
      void main() { vN = normalize(mat3(modelMatrix) * normal); vNv = normalize(normalMatrix * normal); vec4 w = modelMatrix * vec4(position, 1.); vP = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `uniform vec3 sunPos; varying vec3 vN; varying vec3 vP; varying vec3 vNv;
      void main() { vec3 L = normalize(sunPos - vP), Vd = normalize(vP - cameraPosition); float k = clamp(-vNv.z / .42, 0., 1.);
        float a = pow(k, 3.2), sw = smoothstep(-.45, .6, dot(normalize(vN), L)), fwd = pow(max(dot(Vd, L), 0.), 5.);
        vec3 col = vec3(.28, .55, 1.) * a * (sw * 1.1 + .04) + vec3(.75, .8, 1.) * a * fwd * 4.5;
        gl_FragColor = vec4(col, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  S.add(atmo);
  // pale-blue-dot sprite (constant screen size) for when the globe gets smaller than a few pixels
  const dotM = new T.SpriteMaterial({ map: ctx.dotTex(), color: '#9cc4ff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, depthTest: false, sizeAttenuation: false });
  const dot = new T.Sprite(dotM); S.add(dot); const dot2 = new T.Sprite(dotM.clone()); dot2.material.color.set('#e8f2ff'); S.add(dot2);
  // Moon
  const MOON = v3(5.8, .6, -5.5), moon = new T.Mesh(new T.SphereGeometry(.27, 64, 32), new T.MeshStandardMaterial({ map: TX.moon, roughness: .95, metalness: 0 }));
  moon.position.copy(MOON); S.add(moon);
  const sunL = new T.DirectionalLight('#fff1dc', 2.6); sunL.position.copy(SUN); S.add(sunL); S.add(new T.AmbientLight('#2a3060', .08));
  // Sun: glow sprites at constant screen size (hidden behind Earth by the depth test when Earth covers it)
  const sunSpr = (col, s, op) => { const m = new T.Sprite(new T.SpriteMaterial({ map: ctx.dotTex(), color: col, transparent: true, opacity: op, blending: T.AdditiveBlending, depthWrite: false, sizeAttenuation: false })); m.scale.set(s, s, 1); m.position.copy(SUN); S.add(m); return m; };
  const sun1 = sunSpr('#ffffff', .035, 1), sun2 = sunSpr('#ffe2a8', .12, .5), sun3 = sunSpr('#ffc65a', .38, .12), sun4 = sunSpr('#ffd9a0', 1.7, .05);

  // ---------------- Solar System (symbolic radii), neighbouring stars, Milky Way ----------------
  const starT = ctex(64, (g, s) => { const r = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2); r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(.1, 'rgba(255,255,255,.85)'); r.addColorStop(.22, 'rgba(255,255,255,.22)'); r.addColorStop(.5, 'rgba(255,255,255,.04)'); r.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = r; g.fillRect(0, 0, s, s); });
  const PL = [[160, '#c8c2b8', .006, .7], [290, '#ffe0a8', .009, 2.2], [400, '#9cc4ff', 0, 0], [600, '#ff9a6a', .007, 4.1], [1100, '#f0d0a0', .014, 5.3], [1700, '#ffd98a', .012, 1.2], [2400, '#a8f0ff', .009, 3.3], [3000, '#7fa6ff', .009, .4]];
  const orbits = [], planets = [];
  PL.forEach(([r, col, s, a0], i) => { const pts = []; for (let k = 0; k <= 256; k++) { const a = k / 256 * 6.2832; pts.push(SUN.clone().addScaledVector(OX, Math.cos(a) * r).addScaledVector(OY, Math.sin(a) * r)); }
    const ln = new T.Line(new T.BufferGeometry().setFromPoints(pts), new T.LineBasicMaterial({ color: i === 2 ? '#9cc4ff' : '#ffc65a', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false }));
    S.add(ln); orbits.push(ln);
    if (s) { const sp = new T.Sprite(new T.SpriteMaterial({ map: starT, color: col, transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, sizeAttenuation: false })); sp.scale.set(s * 1.7, s * 1.7, 1); S.add(sp); planets.push([sp, r, a0, 1 / Math.pow(r / 400, 1.5)]); } });
  // neighbouring stars around the Sun (bright with halos) + a faint field
  const RN = rng(17), nb = [], NBC = ['#fff4e0', '#ffd9a0', '#ffb27a', '#cfdcff', '#ffe8c8'];
  for (let i = 0; i < 70; i++) { const u = RN() * 2 - 1, th = RN() * 6.283, q = Math.sqrt(1 - u * u), r = 9000 + Math.pow(RN(), .7) * 80000;
    const pos = SUN.clone().add(v3(q * Math.cos(th), u * .55, q * Math.sin(th)).multiplyScalar(r));
    const sp = new T.Sprite(new T.SpriteMaterial({ map: starT, color: NBC[i % 5], transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, sizeAttenuation: false }));
    const s = .012 + .03 * Math.pow(RN(), 2); sp.scale.set(s, s, 1); sp.position.copy(pos); S.add(sp); nb.push([sp, .6 + .4 * RN()]); }
  const NF = 5000, nf = ctx.points(NF, { size: 1.6, atten: false }), nfA = nf.geometry.attributes.position.array, nfC = nf.geometry.attributes.color.array;
  for (let i = 0; i < NF; i++) { const u = RN() * 2 - 1, th = RN() * 6.283, q = Math.sqrt(1 - u * u), r = 12000 + Math.pow(RN(), .8) * 2.2e5; nfA.set([SUN.x + q * Math.cos(th) * r, SUN.y + u * r * .4, SUN.z + q * Math.sin(th) * r], i * 3);
    const v = .25 + .5 * RN(), w = RN(); nfC.set(w < .3 ? [v * .8, v * .85, v] : w < .7 ? [v, v * .95, v * .85] : [v, v * .78, v * .55], i * 3); }
  nf.material.opacity = 0; S.add(nf);
  // Milky Way disc: the plane passes through the Sun; Earth (the Sun) sits in an outer arm
  const NG = v3(.18, 1, .22).normalize(), GR = 2.6e5, GX = new T.Vector3().crossVectors(NG, v3(0, 0, 1)).normalize(), GY = new T.Vector3().crossVectors(NG, GX);
  const GC = v3(0, 0, 0).addScaledVector(GX, 1.45e5).addScaledVector(GY, .4e5);
  if (!M._earthGal) { const N = 1024, c = document.createElement('canvas'); c.width = c.height = N; const g = c.getContext('2d'), im = g.createImageData(N, N);
    const hs = (x, y) => { let h = (x * 374761393 + y * 668265263) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };
    const vn = (x, y) => { const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi, u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf), a = hs(xi, yi), b = hs(xi + 1, yi), cc = hs(xi, yi + 1), d = hs(xi + 1, yi + 1); return a + (b - a) * u + (cc - a) * v + (a - b - cc + d) * u * v; };
    const enc = v => Math.max(0, Math.min(255, Math.pow(Math.min(1, v), 1 / 2.2) * 255));
    for (let py = 0; py < N; py++) for (let px = 0; px < N; px++) { const x = (px + .5) / N * 2 - 1, y = (py + .5) / N * 2 - 1, r = Math.hypot(x, y), th = Math.atan2(y, x), k = (py * N + px) * 4;
      if (r > 1) { im.data[k] = im.data[k + 1] = im.data[k + 2] = 0; im.data[k + 3] = 255; continue; }
      const n1 = vn(x * 7, y * 7) * .6 + vn(x * 15 + 3, y * 15) * .4, ph = 2 * (th - Math.log(Math.max(.03, r)) / Math.tan(.24)) + (n1 - .5) * .7;
      const arm = Math.pow(.5 + .5 * Math.cos(ph), 3) + .2 * Math.pow(.5 + .5 * Math.cos(2 * ph + n1 * 3), 5), lane = Math.pow(.5 + .5 * Math.cos(ph - .55), 14) * (r > .12 ? 1 : 0);
      const disc = Math.exp(-r / .28), bar = Math.exp(-(((x * .8 + y * .6) / .22) ** 2) - (((-x * .6 + y * .8) / .07) ** 2)), bul = Math.exp(-((r / .1) ** 2));
      const L = disc * (.15 + 1.6 * arm * (.5 + .7 * vn(x * 30, y * 30))) * (1 - .75 * lane) + .9 * bul + .5 * bar, w = Math.min(1, r / .5), edge = 1 - Math.min(1, Math.max(0, (r - .8) / .2));
      const hii = Math.pow(Math.max(0, vn(x * 40, y * 40) * .5 + vn(x * 23 + 7, y * 23) * .5 - .62), 2) * 12 * arm * disc;
      im.data[k] = enc((L * (1.05 - .35 * w) + hii) * edge * .5); im.data[k + 1] = enc((L * (.86 - .1 * w) + hii * .4) * edge * .5); im.data[k + 2] = enc((L * (.66 + .34 * w) + hii * .6) * edge * .5); im.data[k + 3] = 255; }
    g.putImageData(im, 0, 0); M._earthGal = new T.CanvasTexture(c); M._earthGal.colorSpace = T.SRGBColorSpace; M._earthGal.anisotropy = 8; }
  const galM = new T.MeshBasicMaterial({ map: M._earthGal, transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide });
  const gal = new T.Mesh(new T.PlaneGeometry(2 * GR, 2 * GR), galM); gal.position.copy(GC); gal.lookAt(GC.clone().add(NG)); S.add(gal);
  const NGS = 9000, gs = ctx.points(NGS, { size: 1.5, atten: false }), gsA = gs.geometry.attributes.position.array, gsC = gs.geometry.attributes.color.array;
  { const r = rng(29); for (let i = 0; i < NGS; i++) { const rr = -Math.log(1 - r() * .98) * .3, th = r() * 6.283; if (rr > 1) { gsA.set([GC.x, GC.y, GC.z], i * 3); continue; }
    const ph = 2 * (th - Math.log(Math.max(.03, rr)) / Math.tan(.24)), arm = Math.pow(.5 + .5 * Math.cos(ph), 3); if (r() > .15 + .85 * arm) { gsA.set([GC.x, GC.y, GC.z], i * 3); gsC.set([0, 0, 0], i * 3); continue; }
    const q = GC.clone().addScaledVector(GX, rr * Math.cos(th) * GR).addScaledVector(GY, rr * Math.sin(th) * GR).addScaledVector(NG, (r() + r() + r() - 1.5) * 4000 * (1 - .5 * rr)); gsA.set([q.x, q.y, q.z], i * 3);
    const v = .3 + .5 * r(), w = Math.min(1, rr / .5); gsC.set([v * (1 - .3 * w), v * (.85 - .05 * w), v * (.65 + .35 * w)], i * 3); } }
  gs.material.opacity = 0; S.add(gs);
  // sky at infinity (follows the camera): stars + faint violet nebula glows
  const SKY = new T.Group(); S.add(SKY); const sky = ctx.stars(SKY, 4500, 1000, { size: 1.15, opacity: .7, seed: 37 }); S.remove(sky); SKY.add(sky);
  [['#2a2470', -700, 250, -500, 1400], ['#1d2a66', 600, -100, -700, 1200], ['#3a2a6a', -200, 500, 700, 1000]].forEach(([c, x, y, z, s]) => { const g = glow(SKY, c, s, .18); g.position.set(x, y, z); });

  // ---------------- camera story ----------------
  const cam = new T.PerspectiveCamera(35, ctx.W / ctx.H, .05, 1e5); ctx.side(cam, p.side == null ? .12 : p.side);
  const FOV0 = cam.fov;
  const N = (x, y, z) => v3(x, y, z).normalize();
  const PERP = new T.Vector3().crossVectors(SUND, UP).normalize();                        // horizontal, across the Sun line
  const CLOSE = { dir: N(-.42, .2, 1), d: 4.7, tgt: v3(0, 0, 0) };
  const GRAIN = { dir: NG.clone().multiplyScalar(.85).add(v3(.3, 0, .55)).normalize(), d: 6.2e5, tgt: GC.clone().multiplyScalar(.3) };
  const OAS1 = { dir: NORB.clone().multiplyScalar(.75).addScaledVector(OX, .55).addScaledVector(OY, -.25).normalize(), d: 5600, tgt: SUN.clone().addScaledVector(OX, 420) };
  const OAS2 = { dir: NORB.clone().multiplyScalar(.55).addScaledVector(OX, .5).addScaledVector(OY, -.65).normalize(), d: 1.5e5, tgt: SUN.clone() };
  const FAR = { dir: PERP.clone().negate().addScaledVector(SUND, .45).addScaledVector(UP, .25).normalize(), d: 320, tgt: v3(0, 0, 0) };
  const NIGHT = { dir: SUND.clone().negate().addScaledVector(PERP, -.16).addScaledVector(UP, .13).normalize(), d: 3.7, tgt: v3(0, -.1, 0) };
  const dir = new T.Vector3(), tgt = new T.Vector3(), cp = new T.Vector3(), tmp = new T.Vector3();
  const mix = (A, B, k, kt) => { dir.copy(A.dir).lerp(B.dir, k).normalize(); const ld = Math.log(A.d) + (Math.log(B.d) - Math.log(A.d)) * k; tgt.copy(A.tgt).lerp(B.tgt, kt == null ? k : kt); return Math.exp(ld); };
  const ease = x => x * x * x * (x * (x * 6 - 15) + 10);
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t; let d;
    if (cG != null) {   // grain: close, then the long pull back
      const g = ease(Math.min(1, Math.max(0, (t - cG) / 16))), d0 = CLOSE.d + .012 * Math.max(0, Math.min(t, cG) - ctx.t0);
      const lnd = Math.log(d0) + (Math.log(GRAIN.d) - Math.log(d0)) * g;
      dir.copy(CLOSE.dir).lerp(GRAIN.dir, sm(.15, .9, g)).normalize(); tgt.copy(CLOSE.tgt).lerp(GRAIN.tgt, sm(Math.log(3e3), Math.log(GRAIN.d), lnd)); d = Math.exp(lnd); }
    else if (cO != null) {   // oasis: rise over the Solar System, then out among the neighbouring stars
      const o1 = ease(Math.min(1, Math.max(0, (t - cO) / 14))), o2 = ease(Math.min(1, Math.max(0, (t - cO - 15) / 20)));
      const c0 = { dir: CLOSE.dir, d: CLOSE.d + .01 * Math.max(0, Math.min(t, cO) - ctx.t0), tgt: CLOSE.tgt };
      if (o2 <= 0) { const lnd = Math.log(c0.d) + (Math.log(OAS1.d) - Math.log(c0.d)) * o1; mix(c0, OAS1, sm(0, .8, o1), sm(Math.log(20), Math.log(OAS1.d), lnd)); d = Math.exp(lnd); }
      else d = mix(OAS1, OAS2, o2);
      dir.applyAxisAngle(NORB, .01 * Math.max(0, t - cO)); }
    else if (cM != null) {   // mind: from the pale blue dot back to the night side
      const m = ease(Math.min(1, Math.max(0, (t - cM) / 13)));
      const f0 = { dir: FAR.dir, d: FAR.d * (1 - .002 * Math.min(u, 60)), tgt: FAR.tgt };
      d = mix(f0, NIGHT, m); d *= 1 - .02 * sm(0, 20, t - cM - 13); }
    else { d = mix(CLOSE, CLOSE, 0); d += .01 * u; dir.applyAxisAngle(UP, -.002 * u); }
    cp.copy(tgt).addScaledVector(dir, d); cam.position.copy(cp);
    cam.up.copy(UP); cam.lookAt(tgt);
    const de = cp.length();   // distance to Earth
    cam.near = Math.max(.02, Math.min(de - 1.2, de * .02) * .5); cam.far = Math.max(de * 8, 4e4) + 2 * de; cam.fov = FOV0; cam.updateProjectionMatrix();
    SKY.position.copy(cp); SKY.scale.setScalar(cam.far * .5 / 1000);   // always behind everything, inside the far plane
    // Earth turns; clouds drift a little faster
    earth.rotation.y = t * .012; clouds.rotation.y = earth.rotation.y; const cOff = -t * .0006; eU.cOff.value = cOff; cU.cOff.value = cOff;
    // globe vs pale-blue-dot sprite
    const pxR = (1 / de) / Math.tan(FOV0 * Math.PI / 360) * ctx.H / 2;
    EG.visible = atmo.visible = pxR > .6; dot.material.opacity = (1 - sm(3, 14, pxR)) * .75; dot2.material.opacity = (1 - sm(3, 14, pxR)) * .9;
    dot.scale.set(.016, .016, 1); dot2.scale.set(.004, .004, 1); eU.city.value = 1;
    moon.visible = de < 6000;
    // layers by distance
    const fOrb = (cM != null ? 0 : 1) * sm(60, 400, de) * (1 - sm(1.6e4, 6e4, de)), fNb = sm(2500, 14000, de) * (1 - sm(9e4, 2.4e5, de)), fGal = sm(2e4, 2.2e5, de);
    orbits.forEach((o, i) => o.material.opacity = fOrb * (i === 2 ? .35 : .22));
    planets.forEach(([sp, r, a0, w]) => { const a = a0 + t * .004 * w; sp.position.copy(SUN).addScaledVector(OX, Math.cos(a) * r).addScaledVector(OY, Math.sin(a) * r); sp.material.opacity = (cM != null ? 0 : 1) * sm(40, 300, de) * (1 - sm(3e4, 9e4, de)); });
    const sunF = 1 - .7 * sm(3e4, 2e5, de); sun1.material.opacity = sunF; sun2.material.opacity = .5 * sunF; sun3.material.opacity = .12 * sunF * (1 - sm(5e3, 5e4, de)); sun4.material.opacity = .06 * (1 - sm(40, 400, de));
    nb.forEach(([sp, o]) => sp.material.opacity = fNb * o);
    nf.material.opacity = fNb * .9; galM.opacity = fGal * .9; gs.material.opacity = fGal * .7;
    sky.material.opacity = .7 * (1 - .75 * fGal);
  } };
};
