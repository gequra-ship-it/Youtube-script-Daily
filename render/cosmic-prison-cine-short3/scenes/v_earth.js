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
// Second staging pass (2026-10-16), all on the existing cues: clouds drift visibly, city lights shimmer, a three-layer aurora
// (green curtains with a rose top) circles both poles on the night side, the atmosphere swells softly on each cue, near-field
// motes drift in front of the camera and stretch into radial streaks whenever the camera rushes in or out (their speed follows
// the camera's log-distance rate), a lens flare when the Sun clears the limb. Payoffs: grain = atmosphere swell at the cue, then
// sonar pings around the pale blue dot once it is a dot; oasis = swell + the orbit lines draw themselves on one after another
// with a comet head (from cue + 5.5 s), each planet glints on "planets, moons" (cue + 12.4 s), and a brightening wave runs
// through the neighbouring stars on "vast beyond imagination" (cue + 31 s); mind = pings from the dot on the cue, then on arrival
// at the night side (cue + 9..13 s) the city lights and aurora brighten and the sunrise flare blooms at the limb.
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
  const eU = { day: { value: TX.day }, night: { value: TX.night }, cloud: { value: TX.cloud }, ocean: { value: TX.ocean }, sunPos: { value: SUN }, cOff: { value: 0 }, city: { value: 1 }, uT: { value: 0 } };
  const earthM = new T.ShaderMaterial({ uniforms: eU,
    vertexShader: `varying vec2 vUv; varying vec3 vN; varying vec3 vP;
      void main() { vUv = uv; vN = normalize(mat3(modelMatrix) * normal); vec4 w = modelMatrix * vec4(position, 1.); vP = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `uniform sampler2D day, night, cloud, ocean; uniform vec3 sunPos; uniform float cOff, city, uT; varying vec2 vUv; varying vec3 vN; varying vec3 vP;
      void main() { vec3 N = normalize(vN), L = normalize(sunPos - vP), V = normalize(cameraPosition - vP); float nl = dot(N, L);
        vec3 d = texture2D(day, vUv).rgb; float cs = texture2D(cloud, vUv + vec2(cOff + .002, -.002)).r, oc = texture2D(ocean, vUv).r;
        float dif = smoothstep(-.03, .12, nl) * (.1 + .9 * max(nl, 0.));
        vec3 sunC = mix(vec3(1., .55, .32), vec3(1., .96, .9), smoothstep(.0, .18, nl));
        vec3 col = d * sunC * dif * 1.8 * (1. - .5 * cs);
        vec3 H = normalize(L + V); float nh = max(dot(N, H), 0.), gl = oc * (1. - cs) * smoothstep(0., .15, nl);
        col += sunC * gl * (pow(nh, 90.) * 2.2 + pow(nh, 12.) * .06);
        float nf = smoothstep(.05, -.14, nl); float shim = .75 + .5 * (texture2D(cloud, vUv * 7. + vec2(uT * .004, uT * .0025)).g - .55) / .45;
        col += texture2D(night, vUv).rgb * nf * (1. - .8 * cs) * 1.1 * city * shim;
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
  const aU = { sunPos: { value: SUN }, uB: { value: 1 } };
  const atmo = new T.Mesh(new T.SphereGeometry(1.1, 128, 64), new T.ShaderMaterial({ uniforms: aU, side: T.BackSide, transparent: true, depthWrite: false, blending: T.AdditiveBlending,
    vertexShader: `varying vec3 vN; varying vec3 vP; varying vec3 vNv;
      void main() { vN = normalize(mat3(modelMatrix) * normal); vNv = normalize(normalMatrix * normal); vec4 w = modelMatrix * vec4(position, 1.); vP = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
    fragmentShader: `uniform vec3 sunPos; uniform float uB; varying vec3 vN; varying vec3 vP; varying vec3 vNv;
      void main() { vec3 L = normalize(sunPos - vP), Vd = normalize(vP - cameraPosition); float k = clamp(-vNv.z / .42, 0., 1.);
        float a = pow(k, 3.2), sw = smoothstep(-.45, .6, dot(normalize(vN), L)), fwd = pow(max(dot(Vd, L), 0.), 5.);
        vec3 col = (vec3(.28, .55, 1.) * a * (sw * 1.1 + .04) + vec3(.75, .8, 1.) * a * fwd * 4.5) * uB;
        gl_FragColor = vec4(col, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  S.add(atmo);
  // aurora: three additive shells inside the tilted group (curtains with rays; green low, rose high), night side only. Each shell
  // is only the two polar bands (partial spheres), so it costs little fill; latitude comes from the object-space normal.
  const auU = { sunPos: { value: SUN }, uT: { value: 0 }, uA: { value: 1 } }, auroras = [];
  const auG = (() => { const a = new T.SphereGeometry(1, 128, 6, 0, 6.2832, .2, .48), b = new T.SphereGeometry(1, 128, 6, 0, 6.2832, Math.PI - .68, .48), n = a.attributes.position.count;
    const g = new T.BufferGeometry(), P = new Float32Array((n + b.attributes.position.count) * 3), N = new Float32Array(P.length); P.set(a.attributes.position.array); P.set(b.attributes.position.array, n * 3); N.set(a.attributes.normal.array); N.set(b.attributes.normal.array, n * 3);
    g.setAttribute('position', new T.BufferAttribute(P, 3)); g.setAttribute('normal', new T.BufferAttribute(N, 3)); g.setIndex([...a.index.array, ...Array.from(b.index.array, i => i + n)]); return g; })();
  [[1.012, 0, .9], [1.022, .5, .55], [1.034, 1, .3]].forEach(([sc, ly, op]) => {
    const m = new T.Mesh(auG, new T.ShaderMaterial({ uniforms: Object.assign({ uL: { value: ly }, uO: { value: op } }, auU), transparent: true, depthWrite: false, blending: T.AdditiveBlending,
      vertexShader: `varying vec3 vO; varying vec3 vN; varying vec3 vP;
        void main() { vO = normal; vN = normalize(mat3(modelMatrix) * normal); vec4 w = modelMatrix * vec4(position, 1.); vP = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
      fragmentShader: `uniform vec3 sunPos; uniform float uT, uA, uL, uO; varying vec3 vO; varying vec3 vN; varying vec3 vP;
        void main() { vec3 o = normalize(vO); float lat = asin(clamp(o.y, -1., 1.)), al = abs(lat), lon = atan(-o.z, o.x) + 3.14159265;
          float wav = .035 * sin(lon * 5. + uT * .13 + sign(lat) * 1.7) + .02 * sin(lon * 11. - uT * .21);
          float band = exp(-pow((al - 1.15 - .025 * uL - wav) / (.03 + .015 * uL), 2.));
          float cur = (.7 + .3 * sin(lon * 40. + 3. * sin(lon * 7. + uT * .3) + uT * .6)) * (.8 + .2 * sin(lon * 97. - uT * .9)) * (lat < 0. ? .4 : 1.);
          vec3 N = normalize(vN), L = normalize(sunPos - vP), V = normalize(cameraPosition - vP);
          float night = smoothstep(.18, -.08, dot(N, L)), fr = pow(1. - abs(dot(N, V)), 1.5);
          vec3 col = mix(vec3(.2, .9, .5), vec3(.85, .35, .7), uL) * band * cur * night * (.25 + 1.1 * fr) * uA * uO * .7;
          gl_FragColor = vec4(col, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` }));
    m.scale.setScalar(sc); EG.add(m); auroras.push(m); });
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

  // ---------------- near-field motes / streaks (camera space, scaled with the near plane so they always sit just in front) ----------------
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
    const M2 = new T.Mesh(g, m); M2.frustumCulled = false; M2.renderOrder = o.order || 0; par.add(M2);
    return { mesh: M2, set(i, hx, hy, hz, tx, ty, tz, w, r, gg, b) { for (let k = 0; k < 4; k++) { const j = (i * 4 + k) * 3; H[j] = hx; H[j + 1] = hy; H[j + 2] = hz; Tl[j] = tx; Tl[j + 1] = ty; Tl[j + 2] = tz; C[j] = r; C[j + 1] = gg; C[j + 2] = b; Wd[i * 4 + k] = w; } },
      hide(i) { for (let k = 0; k < 4; k++) { const j = (i * 4 + k) * 3; C[j] = C[j + 1] = C[j + 2] = 0; } },
      commit() { ['aH', 'aT', 'aC', 'aW'].forEach(k => g.attributes[k].needsUpdate = true); } }; }
  const NEAR = new T.Group(); S.add(NEAR);
  const NMT = 240, motes = streaks(NEAR, NMT, { minPx: 1.4, near: [0, 1e-6], depthTest: false, order: 20 }), mB = [];
  { const r = rng(61); for (let i = 0; i < NMT; i++) { const a = r() * 6.283, rr = 1.2 + 10 * Math.sqrt(r()); mB.push([Math.cos(a) * rr * 1.5, Math.sin(a) * rr, r(), .6 + .8 * r(), .5 + .5 * r(), r() * 6.283]); } }
  // lens flare (screen-space ghosts along the line Sun -> centre, an anamorphic streak at the Sun)
  const ringT = ctex(128, (g, s) => { const r = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2); r.addColorStop(0, 'rgba(255,255,255,0)'); r.addColorStop(.7, 'rgba(255,255,255,.08)');
    r.addColorStop(.88, 'rgba(255,255,255,.9)'); r.addColorStop(.95, 'rgba(255,255,255,.2)'); r.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = r; g.fillRect(0, 0, s, s); });
  const scrSpr = (map, col) => { const m = new T.Sprite(new T.SpriteMaterial({ map, color: col, transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, depthTest: false, sizeAttenuation: false })); m.renderOrder = 21; S.add(m); return m; };
  const GH = [[.35, .05, '#ffd9a0', 0], [.62, .025, '#9cc4ff', 1], [1.05, .09, '#ffb27a', 1], [1.35, .035, '#c8a0ff', 0], [1.75, .14, '#8fd0ff', 1]].map(([k, sz, c, rg]) => [scrSpr(rg ? ringT : ctx.dotTex(), c), k, sz]);
  const ana = scrSpr(ctx.dotTex(), '#ffe2c0');
  // sonar ping rings around the pale blue dot, comet heads that draw the orbit lines on
  const pings = [0, 1].map(() => scrSpr(ringT, '#9cc4ff'));
  const heads = PL.map(() => { const m = new T.Sprite(new T.SpriteMaterial({ map: starT, color: '#fff0d0', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, sizeAttenuation: false })); m.scale.set(.03, .03, 1); S.add(m); return m; });
  const env = (a, rise, fall) => a <= 0 ? 0 : sm(0, rise, a) * Math.exp(-Math.max(0, a - rise) / fall);
  const nbT = nb.map(([sp]) => sp.position.distanceTo(SUN));

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
  // the camera story as a pure function of t: sets dir / tgt, returns the distance
  const story = (t, u) => { let d;
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
    return d; };
  const scr = new T.Vector3(), tA = new T.Vector3(), tB = new T.Vector3();
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const lnPrev = Math.log(story(t - .05, u - .05)), d = story(t, u), lnV = (Math.log(d) - lnPrev) / .05;
    cp.copy(tgt).addScaledVector(dir, d); cam.position.copy(cp);
    cam.up.copy(UP); cam.lookAt(tgt);
    const de = cp.length();   // distance to Earth
    cam.near = Math.max(.02, Math.min(de - 1.2, de * .02) * .5); cam.far = Math.max(de * 8, 4e4) + 2 * de; cam.fov = FOV0; cam.updateProjectionMatrix();
    SKY.position.copy(cp); SKY.scale.setScalar(cam.far * .5 / 1000);   // always behind everything, inside the far plane
    // Earth turns; clouds drift a little faster
    earth.rotation.y = t * .012; clouds.rotation.y = earth.rotation.y; const cOff = -t * .0018; eU.cOff.value = cOff; cU.cOff.value = cOff; eU.uT.value = t;
    // globe vs pale-blue-dot sprite
    const pxR = (1 / de) / Math.tan(FOV0 * Math.PI / 360) * ctx.H / 2;
    EG.visible = atmo.visible = pxR > .6; dot.material.opacity = (1 - sm(3, 14, pxR)) * .75; dot2.material.opacity = (1 - sm(3, 14, pxR)) * .9;
    dot.scale.set(.016, .016, 1); dot2.scale.set(.004, .004, 1);
    // payoff envelopes (flashes rise >= .4 s and fade over >= 2 s)
    const cueT = cG != null ? cG : cO != null ? cO : cM, sw = cueT == null ? 0 : env(t - cueT, .45, 2.4);
    const arrive = cM != null ? sm(cM + 9, cM + 13, t) : 0;
    eU.city.value = 1 + .5 * arrive + .25 * sw; aU.uB.value = 1 + .45 * sw + .15 * arrive;
    auU.uT.value = t; auU.uA.value = .85 + .5 * arrive + .3 * sw + .15 * Math.sin(t * .37);
    // sonar pings around the pale blue dot: from the "mind" cue, or once the "grain" pull-back has made Earth a dot
    const tP = cM != null ? cM : cG != null ? cG + 7.5 : null, dotOp = 1 - sm(3, 14, pxR);
    pings.forEach((pg, i) => { if (tP == null || t < tP + i * 1.6) { pg.visible = false; return; } const a = ((t - tP - i * 1.6) % 3.6), q = a / 3.6;
      pg.visible = dotOp > .01; pg.position.copy(EG.position); pg.scale.set(.02 + .11 * q, .02 + .11 * q, 1); pg.material.opacity = sm(0, .15, q) * (1 - q) * (1 - q) * .55 * dotOp; });
    moon.visible = de < 6000;
    // layers by distance
    const fOrb = (cM != null ? 0 : 1) * sm(60, 400, de) * (1 - sm(1.6e4, 6e4, de)), fNb = sm(2500, 14000, de) * (1 - sm(9e4, 2.4e5, de)), fGal = sm(2e4, 2.2e5, de);
    // oasis: each orbit line draws itself on (from cue + 5.5 s, staggered), a comet head at the tip; other shots: drawn already
    orbits.forEach((o, i) => { o.material.opacity = fOrb * (i === 2 ? .35 : .22); const hd = heads[i];
      if (cO == null) { o.geometry.setDrawRange(0, Infinity); hd.visible = false; return; }
      const a0 = cO + 5.5 + i * .45, k = sm(a0, a0 + 2.6, t), n = Math.max(0, Math.min(257, Math.floor(k * 256) + 1)); o.geometry.setDrawRange(0, k > 0 ? n : 0);
      const ho = fOrb * (k > 0 && k < 1 ? 1 : 0) + fOrb * env(t - a0 - 2.6, .05, .8) * (k >= 1 ? 1 : 0); hd.visible = ho > .005;
      if (hd.visible) { const pa = o.geometry.attributes.position, j = Math.min(256, n - 1); hd.position.set(pa.getX(j), pa.getY(j), pa.getZ(j)); hd.material.opacity = ho * .9; } });
    planets.forEach(([sp, r, a0, w], i) => { const a = a0 + t * .004 * w; sp.position.copy(SUN).addScaledVector(OX, Math.cos(a) * r).addScaledVector(OY, Math.sin(a) * r);
      const gl = cO != null ? env(t - (cO + 12.4 + i * .3), .25, 1.4) : 0; sp.scale.set(PL[i < 2 ? i : i + 1][2] * 1.7 * (1 + 1.6 * gl), PL[i < 2 ? i : i + 1][2] * 1.7 * (1 + 1.6 * gl), 1);
      sp.material.opacity = Math.min(1, (cM != null ? 0 : 1) * sm(40, 300, de) * (1 - sm(3e4, 9e4, de)) * (1 + 1.2 * gl)); });
    const sunF = 1 - .7 * sm(3e4, 2e5, de); sun1.material.opacity = sunF; sun2.material.opacity = .5 * sunF; sun3.material.opacity = .12 * sunF * (1 - sm(5e3, 5e4, de)); sun4.material.opacity = .06 * (1 - sm(40, 400, de));
    nb.forEach(([sp, o], i) => { const wv = cO != null ? env(t - (cO + 31 + nbT[i] / 4e4), .4, 2) : 0; sp.material.opacity = Math.min(1, fNb * o * (.78 + .22 * Math.sin(t * (1.3 + (i % 7) * .23) + i)) * (1 + 1.5 * wv)); });
    nf.material.opacity = fNb * .9; galM.opacity = fGal * .9; gs.material.opacity = fGal * .7;
    sky.material.opacity = .7 * (1 - .75 * fGal);
    // near-field motes: camera space, depth in units of the near plane; s = fract(F + phase) with F following log-distance
    // (pull-back -> they recede into the frame, approach -> they rush toward the camera); streak length = distance in .2 s
    NEAR.position.copy(cp); NEAR.quaternion.copy(cam.quaternion); NEAR.scale.setScalar(cam.near * 2);
    const F = .3 * Math.log(d) + .004 * t, vS = .3 * lnV + .004, sp = Math.min(1, Math.abs(lnV) / .9), tH = Math.tan(FOV0 * Math.PI / 360), asp = ctx.W / ctx.H;
    for (let i = 0; i < NMT; i++) { const b = mB[i], s0 = F * b[3] + b[2], s = s0 - Math.floor(s0), z = 2.5 + 40 * s, ds = Math.max(-.35, Math.min(.35, vS * b[3] * .2)), z2 = 2.5 + 40 * Math.max(0, Math.min(1, s - ds));
      const x = b[0] + .15 * Math.sin(t * .2 * b[4] + b[5]), y = b[1] + .15 * Math.cos(t * .17 * b[4] + b[5]), sx = x / z / (tH * asp);
      const v = Math.sin(Math.PI * s) * (.1 + .32 * sp) * b[4] * (sx < -.25 ? .3 : 1) * (Math.abs(sx) > 1.1 || Math.abs(y / z / tH) > 1.1 ? 0 : 1);
      if (v <= .002) { motes.hide(i); continue; }
      motes.set(i, x, y, -z, x, y, -z2, .008, .75 * v, .85 * v, v); }
    motes.commit();
    // lens flare when the Sun is on screen and clear of Earth's disc
    scr.copy(SUN).project(cam); const sunDir = tA.copy(SUN).sub(cp).normalize(), ang = Math.acos(Math.max(-1, Math.min(1, sunDir.dot(tB.copy(cp).negate().normalize())))), ar = Math.asin(Math.min(1, 1.02 / de));
    const onS = scr.z < 1 && Math.abs(scr.x) < 1.2 && Math.abs(scr.y) < 1.2 ? 1 : 0, clear = sm(ar * .99, ar * 1.06 + .002, ang) * onS * (1 - sm(3e4, 2e5, de));
    const fG = clear * (.55 + .7 * (cM != null ? env(t - (cM + 11.5), .6, 3) + .4 * arrive : 0) + .3 * sw);
    GH.forEach(([g, k, sz]) => { const nx = scr.x * (1 - 2 * k), ny = scr.y * (1 - 2 * k); g.visible = fG > .01; if (!g.visible) return;
      g.position.set(nx, ny, .5).unproject(cam); g.scale.set(sz, sz, 1); g.material.opacity = fG * .16 * (nx < -.3 ? .3 : 1); });
    ana.visible = fG > .01; if (ana.visible) { ana.position.set(scr.x, scr.y, .5).unproject(cam); ana.scale.set(.38, .007, 1); ana.material.opacity = fG * .3; }
  } };
};
