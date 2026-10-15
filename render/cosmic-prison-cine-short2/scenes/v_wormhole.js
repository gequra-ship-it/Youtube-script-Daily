// wormhole — an Ellis-type wormhole throat floating in deep space, drawn as true gravitational lensing: our sky (navy-violet nebula,
// ~22k stars, far galaxies) is bent around the throat into a bright Einstein ring, and through the sphere-like mouth one sees a
// second, distorted universe (warm amber nebula, dense golden starfield) as a fisheye. Both skies are rendered ONCE into cube maps;
// every frame is one full-screen lens pass (ray direction bent per pixel from the throat's impact parameter) plus soft gold dust
// in front for parallax and a faint halo. Written for cosmic-prison-cine S30-S31 (2026-10-15).
// params (cues, all optional):
//   open      the throat grows open out of nothing (absent: already open at the start)
//   enter     the camera moves toward and into the throat until the other universe fills most of the frame
//   collapse  S31: quantum instability — the rim flickers into slow ripples, light rings run outward, the throat pinches shut to a
//             point, a soft flash fades, and only the unlensed sky remains
//   side      subject offset (default .12)
(window.MIYA = window.MIYA || { scenes: {} }).scenes.wormhole = function (ctx, p) {
  const { T, sm, rng, cue, points } = ctx, Rr = ctx.R;
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), ctx.t);
  const v3 = (x, y, z) => new T.Vector3(x, y, z);

  // ---------------- value noise for the nebula canvases ----------------
  const hsh = (x, y, z) => { let h = (x * 374761393 + y * 668265263 + z * 1274126177) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };
  function vn(x, y, z) { const xi = Math.floor(x), yi = Math.floor(y), zi = Math.floor(z), xf = x - xi, yf = y - yi, zf = z - zi;
    const u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf), w = zf * zf * (3 - 2 * zf), L = (a, b, k) => a + (b - a) * k;
    return L(L(L(hsh(xi, yi, zi), hsh(xi + 1, yi, zi), u), L(hsh(xi, yi + 1, zi), hsh(xi + 1, yi + 1, zi), u), v), L(L(hsh(xi, yi, zi + 1), hsh(xi + 1, yi, zi + 1), u), L(hsh(xi, yi + 1, zi + 1), hsh(xi + 1, yi + 1, zi + 1), u), v), w); }
  const fbm = (x, y, z, o) => { let s = 0, a = .5, f = 1; for (let k = 0; k < o; k++) { s += a * vn(x * f, y * f, z * f); a *= .5; f *= 2.03; } return s; };
  // equirect nebula sphere; fn(dx,dy,dz) -> [r,g,b] linear
  function nebula(fn, seedOff) { const SW = 640, SH = 320, c = document.createElement('canvas'); c.width = SW; c.height = SH; const g = c.getContext('2d'), im = g.createImageData(SW, SH), D = im.data;
    for (let y = 0; y < SH; y++) { const th = (y + .5) / SH * Math.PI, st = Math.sin(th), ct = Math.cos(th);
      for (let x = 0; x < SW; x++) { const ph = (x + .5) / SW * 6.2832, dx = -Math.cos(ph) * st, dy = ct, dz = Math.sin(ph) * st, col = fn(dx, dy, dz), k = (y * SW + x) * 4;
        for (let j = 0; j < 3; j++) D[k + j] = Math.max(0, Math.min(255, Math.pow(Math.max(0, col[j]), 1 / 2.2) * 255)); D[k + 3] = 255; } }
    g.putImageData(im, 0, 0); const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace;
    return new T.Mesh(new T.SphereGeometry(900, 64, 32), new T.MeshBasicMaterial({ map: t, side: T.BackSide, depthWrite: false })); }
  function starSet(sc, n, size, seed, colFn, band) { const P = points(n, { size, opacity: 1, atten: false }), a = P.geometry.attributes.position.array, c = P.geometry.attributes.color.array, r = rng(seed);
    for (let i = 0; i < n; i++) { let x, y, z; do { const u = r() * 2 - 1, th = r() * 6.283, q = Math.sqrt(1 - u * u); x = q * Math.cos(th); y = u; z = q * Math.sin(th); } while (band && Math.abs(band[0] * x + band[1] * y + band[2] * z) > .25 + .6 * r() * r());
      a.set([x * 800, y * 800, z * 800], i * 3); c.set(colFn(r), i * 3); } sc.add(P); return P; }

  // ---------------- our sky (navy-violet) ----------------
  const ours = new T.Scene(); ours.background = new T.Color('#02030a');
  ours.add(nebula((x, y, z) => { const n1 = fbm(x * 2.2 + 3, y * 2.2, z * 2.2, 4), n2 = fbm(x * 5 + 9, y * 5, z * 5, 3), bd = Math.exp(-Math.pow(.3 * x + .8 * y - .5 * z, 2) / .06);
    const v = Math.max(0, n1 - .42) * 1.6 + bd * .5 * n2; return [.004 + v * .035, .005 + v * .025, .014 + v * .065]; }));
  const scol = (r) => { const t = r(), b = .35 + 1.1 * Math.pow(r(), 3); return t < .25 ? [.7 * b, .8 * b, 1.1 * b] : t < .8 ? [b, .96 * b, .9 * b] : [b, .8 * b, .6 * b]; };
  starSet(ours, 14000, 2.2, 11, scol); starSet(ours, 7000, 2.0, 12, scol, [.3, .8, -.5]); starSet(ours, 900, 3.6, 13, scol);
  { const RG = rng(41); for (let i = 0; i < 30; i++) { const u = RG() * 2 - 1, th = RG() * 6.283, q = Math.sqrt(1 - u * u);
    const s = new T.Sprite(new T.SpriteMaterial({ map: ctx.dotTex(), color: RG() < .5 ? '#ffd9a8' : '#bcc8ff', transparent: true, opacity: .5, blending: T.AdditiveBlending, depthWrite: false, rotation: RG() * 3.14 }));
    const s0 = 6 + RG() * 12; s.scale.set(s0, s0 * (.3 + RG() * .5), 1); s.position.set(q * Math.cos(th) * 780, u * 780, q * Math.sin(th) * 780); ours.add(s); } }
  // ---------------- the other universe (warm amber, dense) ----------------
  const other = new T.Scene(); other.background = new T.Color('#0a0503');
  other.add(nebula((x, y, z) => { const n1 = fbm(x * 2 + 7, y * 2 + 1, z * 2, 5), n2 = fbm(x * 6 + 2, y * 6, z * 6 + 4, 3), bd = Math.exp(-Math.pow(.7 * x - .2 * y + .68 * z, 2) / .04);
    const v = Math.max(0, n1 - .47) * 3 + bd * (.25 + 1.1 * Math.max(0, n2 - .35)), dk = sm(.55, .75, n2) * bd;
    return [.008 + v * .2 * (1 - .6 * dk), .004 + v * .11 * (1 - .6 * dk), .008 + v * .035 + .02 * Math.max(0, n2 - .5)]; }));
  const ocol = (r) => { const t = r(), b = .45 + 1.2 * Math.pow(r(), 3); return t < .15 ? [.8 * b, .85 * b, 1.1 * b] : [b, .85 * b, .62 * b]; };
  starSet(other, 9000, 3.0, 21, ocol); starSet(other, 9000, 2.6, 22, ocol, [.7, -.2, .68]); starSet(other, 600, 5, 23, ocol);

  // ---------------- bake both skies into cube maps (once) ----------------
  const mkCube = (sz) => new T.WebGLCubeRenderTarget(sz, { generateMipmaps: true, minFilter: T.LinearMipmapLinearFilter, magFilter: T.LinearFilter, colorSpace: T.SRGBColorSpace });
  const cubeO = mkCube(2048), cubeX = mkCube(1024);
  if (Rr) { const prevT = Rr.toneMapping; Rr.toneMapping = T.NoToneMapping;
    new T.CubeCamera(1, 2000, cubeO).update(Rr, ours); new T.CubeCamera(1, 2000, cubeX).update(Rr, other); Rr.toneMapping = prevT; }

  // ---------------- main scene: lens pass + dust + halo ----------------
  const S = new T.Scene(); S.background = new T.Color('#02030a');
  const C0 = v3(0, 0, 0), A0 = 10;
  const U = { tO: { value: cubeO.texture }, tX: { value: cubeX.texture }, uC: { value: C0.clone() }, uCam: { value: v3(0, 0, 0) }, uA: { value: A0 },
    uPInv: { value: new T.Matrix4() }, uCW: { value: new T.Matrix4() }, uRim: { value: 1 }, uRip: { value: 0 }, uRing: { value: v3(0, 0, 0) }, uTime: { value: 0 }, uXr: { value: new T.Matrix3() } };
  const lens = new T.Mesh(new T.PlaneGeometry(2, 2), new T.ShaderMaterial({ uniforms: U, depthWrite: false, depthTest: false,
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy, 0., 1.); }',
    fragmentShader: `uniform samplerCube tO, tX; uniform vec3 uC, uCam, uRing; uniform float uA, uRim, uRip, uTime; uniform mat4 uPInv, uCW; uniform mat3 uXr; varying vec2 vUv;
      vec3 rot(vec3 v, vec3 k, float a){ return v * cos(a) + cross(k, v) * sin(a) + k * dot(k, v) * (1. - cos(a)); }
      void main(){
        vec4 pv = uPInv * vec4(vUv * 2. - 1., 1., 1.); pv /= pv.w;
        vec3 d = normalize((uCW * vec4(pv.xyz, 0.)).xyz), oc = uC - uCam;
        float tca = dot(oc, d); vec3 pp = oc - d * tca; float b = length(pp), A = max(uA, 1e-4), beta = b / A;
        float front = smoothstep(0., .3 * length(oc), tca);
        vec3 col;
        // slow broad ripples in space during the collapse (shift the impact parameter)
        float rip = uRip * sin(b * .55 - uTime * 3.2) * exp(-b / 40.);
        beta += rip * .06;
        if (tca > 0. && beta < 1.) {
          vec3 ax = normalize(oc), k = cross(ax, d); float kl = length(k); k = kl > 1e-6 ? k / kl : vec3(0., 1., 0.);
          float g = 2.1 * pow(beta, 1.5);
          vec3 dout = rot(ax, k, g);
          col = textureCube(tX, uXr * dout).rgb * 1.15;
          // secondary image of our own sky wrapped close to the rim (light that went around the throat)
          float w2 = smoothstep(.86, .995, beta);
          vec3 kk = normalize(cross(d, oc) + 1e-6); vec3 d2 = rot(d, kk, 3.14159 * (1.15 - beta));
          col = mix(col, textureCube(tO, d2).rgb, w2 * .55);
          col *= .75 + .25 * (1. - pow(beta, 6.));
        } else {
          float al = 1.05 * A * A / (b * b + 1e-4); al = min(al, 3.1) * front;
          vec3 kk = cross(d, oc); float kl = length(kk); kk = kl > 1e-6 ? kk / kl : vec3(0., 1., 0.);
          col = textureCube(tO, rot(d, kk, al)).rgb;
        }
        // Einstein ring rim (gold-white), and light rings running outward in the collapse
        float rim = exp(-pow((beta - 1.) / .014, 2.)) * .9 + .22 * exp(-pow((beta - 1.) / .07, 2.));
        col += uRim * rim * vec3(1., .8, .52) * .9 * front;
        float rr = uRing.x; if (uRing.y > 0.) col += uRing.y * exp(-pow((b - rr) / (1.5 + rr * .08), 2.)) * vec3(.85, .8, 1.) * front;
        gl_FragColor = vec4(col, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  lens.frustumCulled = false; lens.renderOrder = -10; S.add(lens);
  // soft halo around the throat, dust in front of it, collapse flash
  const halo = ctx.glow(S, '#ffcf8a', A0 * 5, .1), flash = ctx.glow(S, '#fff2dc', 6, 0), flash2 = ctx.glow(S, '#ffc65a', 40, 0);
  const ND = 1500, dust = points(ND, { size: .35, opacity: 1, color: '#ffe2b0' }), dA = dust.geometry.attributes.position.array, dC = dust.geometry.attributes.color.array, dB = [];
  { const r = rng(55); for (let i = 0; i < ND; i++) { const z = 14 + r() * 110, rad = 4 + Math.pow(r(), .7) * (14 + z * .5), a = r() * 6.283; dA.set([Math.cos(a) * rad, Math.sin(a) * rad * .7, z], i * 3); dB.push(r()); } }
  dust.frustumCulled = false; S.add(dust);

  // ---------------- camera ----------------
  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .1, 3000); ctx.side(cam, p.side == null ? .12 : p.side);
  const VF = ctx.VERT ? 1.25 : 1, tmp = v3(0, 0, 0);
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const op = p.open != null ? at(p.open, 3) : 1, en = at(p.enter, 7), cl = p.collapse != null ? t - cue(p.collapse) : -1e9;
    // collapse: ripples 0..1.6 s, pinch 1.2..3.4 s, flash at ~3.4 s
    const pinch = sm(1.2, 3.4, cl), ripE = sm(0, .8, cl) * (1 - sm(3.2, 4.2, cl));
    let A = A0 * Math.pow(op, .7) * (1 - pinch) * (1 + .06 * ripE * Math.sin(cl * 5.1) * (1 - pinch));
    U.uA.value = Math.max(0, A); U.uRim.value = (A > .01 ? 1 : 0) * (.8 + .2 * op) * (1 + .5 * ripE);
    U.uRip.value = ripE; U.uTime.value = t;
    const rt = Math.max(0, cl - .3); U.uRing.value.set(A0 * (1 + rt * 7), cl > 0 ? .5 * Math.exp(-rt * .9) * sm(0, .3, cl) * (1 - sm(4.5, 6, cl)) : 0, 0);
    const fl = cl > 3.2 ? Math.exp(-(cl - 3.3) * 1.8) * sm(3.2, 3.4, cl) : 0;
    flash.material.opacity = .9 * fl; flash.scale.setScalar(4 + 10 * fl); flash2.material.opacity = .35 * fl;
    halo.material.opacity = .1 * op * (1 - pinch); halo.scale.setScalar(A0 * 5 * (.3 + .7 * op));
    // the other universe slowly turns inside the mouth (alive), from t only
    const ry = t * .02; U.uXr.value.set(Math.cos(ry), 0, Math.sin(ry), 0, 1, 0, -Math.sin(ry), 0, Math.cos(ry));
    // camera: slow drift; `enter` dollies toward the mouth; `collapse` eases back a little
    const back = sm(0, 4, cl) * .45 * en;
    const dist = (78 - 58 * en * (1 - back)) * VF - u * .12 * (1 - en);
    cam.position.set(-dist * .2 + Math.sin(u * .05) * 1.5, dist * .08 + 2, dist);
    tmp.set(0, 0, 0); cam.lookAt(tmp); cam.updateMatrixWorld(); cam.updateProjectionMatrix();
    U.uCam.value.copy(cam.position); U.uPInv.value.copy(cam.projectionMatrixInverse); U.uCW.value.copy(cam.matrixWorld);
    for (let i = 0; i < ND; i++) { const tw = .5 + .5 * Math.sin(t * (.6 + dB[i]) + dB[i] * 20); const v = (.25 + .5 * dB[i]) * tw; dC[i * 3] = v; dC[i * 3 + 1] = v * .88; dC[i * 3 + 2] = v * .7; }
    dust.geometry.attributes.color.needsUpdate = true;
  } };
};
