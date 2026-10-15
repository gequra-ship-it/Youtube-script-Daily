// expanse — Hubble's expanding universe (cosmic-prison-cine S09-S17, written 2026-10-15). One stage: a field of ~520 small
// realistic galaxies (spirals with arms, bulge and dust lanes, barred spirals, ellipticals, lenticulars; gold / lavender light,
// each with a round core glow so it keeps body when seen edge-on) floating just above a faint glowing spacetime grid, with the
// Milky Way ("us") as a warm point at the centre. Everything is placed in comoving coordinates times a scale factor a(t), so the
// galaxies are carried apart by the grid (they do not move through it). The grid is log-periodic: as a(t) doubles, new lines fade
// in between the old ones ("new cubic light-years of empty space keep appearing").
// params (all cues, every one optional; without cues the field is simply still):
//   static    S09 nothing moves (the default state; kept for symmetry, no effect)
//   redshift  S10 three light-wave ribbons travel from galaxies at three distances to us; their wavelength stretches and the colour
//             shifts from blue-white toward red, more for the farther galaxy
//   stretch   S11 the grid itself starts to expand: lines spread, new lines appear, galaxies are carried apart (ribbons fade out)
//   law       S12-S14 motion trails behind every galaxy, length proportional to its distance from us (Hubble's law)
//   fast      S15-S16 a red "light speed" ring appears on the grid (the Hubble distance); beyond it galaxies glow red and the part of
//             each trail longer than the light-speed length turns red
//   treadmill S17 one photon (bright point + short tail) runs toward us from just beyond the ring; the grid stretches under it so it
//             barely advances, then it is dragged back; the camera moves in on it
//   side      subject offset (default .12)
// Also defines MIYA.cosmicGal(ctx, n) — an instanced galaxy field (one draw call, pixel-size clamp against shimmer) shared by
// horizon.js and supernova.js (they pull this file in with "// requires: expanse").
(function () {
  const M = (window.MIYA = window.MIYA || { scenes: {} }); M.scenes = M.scenes || {};

  // ---------------- galaxy atlas (4 x 2 tiles of 256 px): 5 spirals, elliptical, lenticular, soft core ----------------
  function atlasCanvas() {
    const TS = 256, c = document.createElement('canvas'); c.width = TS * 4; c.height = TS * 2;
    const g = c.getContext('2d'), im = g.createImageData(TS * 4, TS * 2), D = im.data;
    const hs = (x, y, s) => { let h = (x * 374761393 + y * 668265263 + s * 1442695041) | 0; h = Math.imul(h ^ (h >>> 13), 1274126177); return ((h ^ (h >>> 16)) >>> 0) / 4294967296; };
    const vn = (x, y, s) => { const xi = Math.floor(x), yi = Math.floor(y), xf = x - xi, yf = y - yi, u = xf * xf * (3 - 2 * xf), v = yf * yf * (3 - 2 * yf);
      const a = hs(xi, yi, s), b = hs(xi + 1, yi, s), cc = hs(xi, yi + 1, s), d = hs(xi + 1, yi + 1, s); return a + (b - a) * u + (cc - a) * v + (a - b - cc + d) * u * v; };
    const ss = (a, b, x) => { x = Math.min(1, Math.max(0, (x - a) / (b - a))); return x * x * (3 - 2 * x); };
    const SPEC = [{ arms: 2, pitch: .32, lane: .7, bar: 0, flo: .2 }, { arms: 2, pitch: .45, lane: .9, bar: 0, flo: .35 }, { arms: 2, pitch: .38, lane: .6, bar: 1, flo: .2 },
      { arms: 3, pitch: .42, lane: .4, bar: 0, flo: .8 }, { arms: 2, pitch: .24, lane: .8, bar: 0, flo: .15 }, { ell: 1 }, { len: 1 }, { core: 1 }];
    const enc = v => Math.max(0, Math.min(255, Math.pow(Math.min(1, v), 1 / 2.2) * 255));
    for (let k = 0; k < 8; k++) { const sp = SPEC[k], ox = (k % 4) * TS, oy = Math.floor(k / 4) * TS;
      for (let py = 0; py < TS; py++) for (let px = 0; px < TS; px++) {
        const x = (px + .5) / TS * 2 - 1, y = (py + .5) / TS * 2 - 1, r = Math.hypot(x, y), th = Math.atan2(y, x);
        let R = 0, G = 0, B = 0; const edge = 1 - ss(.7, .97, r);
        if (sp.core) { const v = Math.exp(-r * r / .05) + .3 * Math.exp(-r * r / .22); R = G = B = v; }
        else if (sp.ell) { const v = Math.exp(-Math.pow(r / .1, .55) * 2.0) * 1.4; R = v; G = v * .84; B = v * .64; }
        else if (sp.len) { const v = Math.exp(-r / .15) * .7 + Math.exp(-((r / .08) ** 2)) * .9; R = v; G = v * .86; B = v * .7; }
        else {
          const lr = Math.log(Math.max(.03, r)), ph = sp.arms * (th - lr / Math.tan(sp.pitch)) + k;
          const n1 = vn(x * 9 + k * 7, y * 9, k), n2 = vn(x * 22, y * 22 + k * 3, k + 9);
          let arm = Math.pow(.5 + .5 * Math.cos(ph), 3 + 2 * (1 - sp.flo));
          arm = arm * (1 - sp.flo) + sp.flo * arm * (.4 + 1.2 * n1);
          const lane = Math.pow(.5 + .5 * Math.cos(ph - .75), 14) * sp.lane * ss(.08, .25, r);
          const disc = Math.exp(-r / .24), ar = ss(sp.bar ? .2 : .06, sp.bar ? .32 : .18, r);
          const L = disc * (.18 + 1.5 * arm * ar * (.55 + .9 * n2)) * (1 - .75 * lane);
          const knots = Math.max(0, n2 - .62) * 10 * arm * ar * disc;
          let bar = 0; if (sp.bar) { const a = .5, cx = x * Math.cos(a) + y * Math.sin(a), cy = -x * Math.sin(a) + y * Math.cos(a); bar = Math.exp(-((cx / .26) ** 2) - (cy / .05) ** 2) * .8; }
          const bul = Math.exp(-((r / .085) ** 2)) * 1.4 + Math.exp(-r / .05) * .5 + bar, w = Math.min(1, r / .45);
          R = L * (1 - .3 * w) + knots * .95 + bul; G = L * (.9 - .15 * w) + knots * .7 + bul * .82; B = L * (.75 + .3 * w) + knots + bul * .55;
        }
        const i = ((oy + py) * TS * 4 + ox + px) * 4; D[i] = enc(R * edge); D[i + 1] = enc(G * edge); D[i + 2] = enc(B * edge); D[i + 3] = 255; } }
    g.putImageData(im, 0, 0); return c;
  }

  // ---------------- instanced galaxy field ----------------
  // api: shape(i, size, rot, inc, tile, core) ; set(i, x, y, z, r, g, b, coreK) ; flush() ; random(i, rnd, sMin, sMax) -> kind
  //   tile 0-4 spirals, 5 elliptical, 6 lenticular; inc = minor/major axis (cos of inclination); colours are linear light (additive)
  M.cosmicGal = function (ctx, n, o) {
    o = o || {}; const T = ctx.T;
    if (!M._galAtlas) { const tx = new T.CanvasTexture(atlasCanvas()); tx.colorSpace = T.SRGBColorSpace; tx.anisotropy = 4; M._galAtlas = tx; }
    const N2 = n * 2, g = new T.InstancedBufferGeometry();
    g.setAttribute('position', new T.Float32BufferAttribute([-.5, -.5, 0, .5, -.5, 0, .5, .5, 0, -.5, .5, 0], 3)); g.setIndex([0, 1, 2, 0, 2, 3]);
    const P = new Float32Array(N2 * 3), Q = new Float32Array(N2 * 4), C = new Float32Array(N2 * 3);
    const aP = new T.InstancedBufferAttribute(P, 3), aQ = new T.InstancedBufferAttribute(Q, 4), aC = new T.InstancedBufferAttribute(C, 3);
    aP.setUsage(T.DynamicDrawUsage); aC.setUsage(T.DynamicDrawUsage);
    g.setAttribute('iPos', aP); g.setAttribute('iPar', aQ); g.setAttribute('iCol', aC); g.instanceCount = N2;
    const mat = new T.ShaderMaterial({ uniforms: { map: { value: M._galAtlas }, uH: { value: ctx.H }, uMin: { value: o.minPx || 2.4 } },
      vertexShader: `attribute vec3 iPos; attribute vec4 iPar; attribute vec3 iCol; uniform float uH, uMin; varying vec2 vUv; varying vec3 vCol;
        void main(){ vec4 mv = modelViewMatrix * vec4(iPos, 1.);
          float px = iPar.x * projectionMatrix[1][1] * .5 * uH / max(.001, -mv.z);
          float k = max(1., uMin / max(px, 1e-4)); float inc = max(iPar.z, 1.6 / max(px * k, 1e-3));
          vec2 c = position.xy; c.y *= inc; float cr = cos(iPar.y), sr = sin(iPar.y);
          mv.xy += vec2(c.x * cr - c.y * sr, c.x * sr + c.y * cr) * iPar.x * k;
          vCol = iCol / (k * k) * (iPar.z / inc);
          vec2 tc = vec2(mod(iPar.w, 4.), floor(iPar.w / 4.));
          vUv = vec2((tc.x + position.x + .5) / 4., (1. - tc.y) * .5 + (position.y + .5) * .5);
          gl_Position = projectionMatrix * mv; if (dot(iCol, vec3(1.)) < 1e-5) gl_Position = vec4(2., 2., 2., 1.); }`,
      fragmentShader: `uniform sampler2D map; varying vec2 vUv; varying vec3 vCol;
        void main(){ gl_FragColor = vec4(texture2D(map, vUv).rgb * vCol, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`,
      transparent: true, depthWrite: false, blending: T.AdditiveBlending });
    const mesh = new T.Mesh(g, mat); mesh.frustumCulled = false;
    const WARM = [1, .82, .58];
    return { mesh, n, P, C,
      shape(i, size, rot, inc, tile, core) { Q.set([size, rot, inc, tile], i * 4); Q.set([size * (tile === 5 ? .55 : .42), rot, 1, 7], (n + i) * 4); aQ.needsUpdate = true; this._core = this._core || new Float32Array(n); this._core[i] = core == null ? 1 : core; },
      set(i, x, y, z, r, gg, b, coreK) { P[i * 3] = P[(n + i) * 3] = x; P[i * 3 + 1] = P[(n + i) * 3 + 1] = y; P[i * 3 + 2] = P[(n + i) * 3 + 2] = z;
        C[i * 3] = r; C[i * 3 + 1] = gg; C[i * 3 + 2] = b; const ck = (coreK == null ? 1 : coreK) * (this._core ? this._core[i] : 1) * .55, lum = (r + gg + b) / 3;
        C[(n + i) * 3] = ck * (lum * WARM[0] * .6 + r * .4); C[(n + i) * 3 + 1] = ck * (lum * WARM[1] * .6 + gg * .4); C[(n + i) * 3 + 2] = ck * (lum * WARM[2] * .6 + b * .4); },
      flush() { aP.needsUpdate = true; aC.needsUpdate = true; },
      random(i, rnd, sMin, sMax) { const u = rnd(), sz = sMin + (sMax - sMin) * Math.pow(rnd(), 1.6), rot = rnd() * 6.283;
        if (u < .7) { this.shape(i, sz, rot, Math.max(.17, rnd()), Math.floor(rnd() * 5), 1); return 0; }
        if (u < .88) { this.shape(i, sz * .8, rot, .55 + .45 * rnd(), 5, .6); return 1; }
        this.shape(i, sz * .85, rot, Math.max(.2, rnd() * .8), 6, .8); return 2; } };
  };
  // integral of smoothstep(a, b, x) dx from -inf to x (for expansion rates that switch on smoothly; closed form keeps it seek-safe)
  M.ismooth = (a, b, x) => { if (x <= a) return 0; if (x >= b) return (b - a) / 2 + (x - b); const q = (x - a) / (b - a); return (b - a) * (q * q * q - q * q * q * q / 2); };

  // ---------------- the scene ----------------
  M.scenes.expanse = function (ctx, p) {
    const { T, sm, rng, cue, points, glow } = ctx;
    const S = new T.Scene(); S.background = new T.Color('#05071a');
    const cT = c => c == null ? 1e9 : cue(c);
    const cR = cT(p.redshift), cS = cT(p.stretch), cL = cT(p.law), cF = cT(p.fast), cM = cT(p.treadmill);
    const on = (c0, d) => sm(c0, c0 + d, ctx.t);
    // expansion: a(t) = exp(sum of long smooth ramps) — bounded (x3.9 in all) and independent of the shot span, so a second
    // instance of this stage (e.g. after the S13 data card) given the same cues continues exactly where the first one stopped
    const W = [[cS, 30, .45], [cL, 35, .3], [cF, 35, .35], [cM, 25, .25]];
    const aOf = t => Math.exp(W.reduce((s, [c, d, w]) => s + w * sm(c, c + d, t), 0));

    ctx.stars(S, 2400, 700, { size: 1.3, opacity: .55, seed: 17 });
    // far nebula haze (violet / blue), few large sprites
    const RN = rng(5); for (let k = 0; k < 4; k++) { const s = glow(S, k % 2 ? '#3b2f86' : '#22306e', 380 + RN() * 200, .16 + RN() * .08); const a = -1.2 + k * .9 + RN() * .4; s.position.set(Math.sin(a) * 600, 40 + RN() * 160, -Math.cos(a) * 600 - 100); }

    // grid: log-periodic comoving lattice, distance fade, light-speed ring, warm centre, brighter under the photon
    const gridM = new T.ShaderMaterial({ uniforms: { uA: { value: 1 }, uBase: { value: 4 }, uRing: { value: 30 }, uRingA: { value: 0 }, uCam: { value: new T.Vector3() }, uPh: { value: new T.Vector2() }, uPhA: { value: 0 } },
      vertexShader: 'varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position,1.); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }',
      fragmentShader: `uniform float uA, uBase, uRing, uRingA, uPhA; uniform vec3 uCam; uniform vec2 uPh; varying vec3 vW;
        float lines(vec2 p, float sp){ vec2 q = p / sp; vec2 w = fwidth(q); vec2 d = abs(fract(q + .5) - .5); vec2 l = 1. - smoothstep(w * .35, w * 1.25, d);
          return max(l.x, l.y) * (1. - smoothstep(.06, .22, max(w.x, w.y))); }
        void main(){ float lev = log2(uA), f = fract(lev), s1 = uBase * exp2(f);
          float g = max(lines(vW.xz, s1), f * lines(vW.xz, s1 * .5));
          float r = length(vW.xz), dc = length(vW - uCam);
          float fall = exp(-r / 75.) * (1. - smoothstep(140., 260., dc));
          float ph = uPhA * exp(-pow(length(vW.xz - uPh) / 7., 2.));
          vec3 col = vec3(.30, .36, 1.) * g * (.075 + .3 * ph) * fall + vec3(.22, .18, .55) * .05 * exp(-r / 45.);
          float fr = fwidth(r), rd = abs(r - uRing);
          col += vec3(1., .36, .2) * uRingA * (exp(-pow(rd / (.1 + fr), 2.)) * .9 + exp(-rd / 1.4) * .1) * fall;
          col += vec3(1., .76, .4) * .3 * exp(-r * r / 5.);
          gl_FragColor = vec4(col, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`, transparent: true, depthWrite: false, blending: T.AdditiveBlending });
    const grid = new T.Mesh(new T.PlaneGeometry(900, 900).rotateX(-Math.PI / 2), gridM); grid.renderOrder = -1; S.add(grid);

    // camera basis at build (az0) to place the special galaxies on the screen side
    const az0 = .45, Rv = new T.Vector3(Math.cos(az0), 0, -Math.sin(az0)), Fv = new T.Vector3(-Math.sin(az0), 0, -Math.cos(az0));
    const N = 1000, GF = M.cosmicGal(ctx, N + 1), R1 = rng(23), chi = [], base = [];
    const SRC = [[10, 2], [4, 17], [20, 30]];   // three ribbon sources: (right, forward) in camera basis
    for (let i = 0; i < N; i++) { let x, z;
      if (i < 3) { x = Rv.x * SRC[i][0] + Fv.x * SRC[i][1]; z = Rv.z * SRC[i][0] + Fv.z * SRC[i][1]; }
      else { const rr = 3.5 + 72 * Math.sqrt(R1()), a = R1() * 6.283; x = Math.cos(a) * rr; z = Math.sin(a) * rr; }
      const y = .6 + 4.2 * Math.pow(R1(), 1.5);
      const kind = GF.random(i, R1, .9, 2.6); if (i < 3) GF.shape(i, 1.7, R1() * 6.28, .5 + .2 * i, i === 2 ? 2 : 0, 1);
      const cu = R1(), br = .45 + .6 * R1(), col = kind === 1 ? [1, .8, .55] : cu < .5 ? [1, .86, .64] : cu < .82 ? [.8, .74, 1] : [.86, .9, 1];
      chi.push([x, y, z]); base.push([col[0] * br, col[1] * br, col[2] * br]); }
    GF.shape(N, 2.3, .6, .42, 0, 1.4); S.add(GF.mesh);   // the Milky Way at the centre
    const us1 = glow(S, '#ffcf8a', 5.5, .32), us2 = glow(S, '#fff0d0', 1.3, .85); us1.position.set(0, 1.3, 0); us2.position.set(0, 1.3, 0);

    // dust carried with the expansion
    const ND = 900, dust = points(ND, { size: .16, opacity: .8 }), dA = dust.geometry.attributes.position.array, dC = dust.geometry.attributes.color.array, dChi = [];
    { const r = rng(31); for (let i = 0; i < ND; i++) { const rr = 2 + 75 * Math.sqrt(r()), a = r() * 6.283; dChi.push([Math.cos(a) * rr, .2 + 7 * r(), Math.sin(a) * rr]); const v = .12 + .2 * r(), w = r() < .5;
      dC.set(w ? [v, v * .8, v * .55] : [v * .7, v * .6, v], i * 3); } }
    dust.frustumCulled = false; S.add(dust);

    // trails: camera-facing quads behind each galaxy, pointing back toward us; gold, red beyond the light-speed length
    const trG = new T.BufferGeometry(), trP = new Float32Array(N * 4 * 3), trA = new Float32Array(N * 4 * 4), idx = [];
    for (let i = 0; i < N; i++) { const b = i * 4; idx.push(b, b + 1, b + 2, b + 2, b + 1, b + 3); }
    trG.setAttribute('position', new T.BufferAttribute(trP, 3)); trG.setAttribute('aT', new T.BufferAttribute(trA, 4)); trG.setIndex(idx);
    const trM = new T.ShaderMaterial({ uniforms: { uLc: { value: 1e4 } },
      vertexShader: 'attribute vec4 aT; varying vec4 vT; void main(){ vT = aT; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }',
      fragmentShader: `uniform float uLc; varying vec4 vT;
        void main(){ float a = vT.x, L = max(vT.z, 1e-3), s = a / uLc; float fade = pow(max(0., 1. - a / L), 1.3) * exp(-vT.y * vT.y * 2.6);
          vec3 col = mix(vec3(1., .78, .42), vec3(1., .26, .14), smoothstep(.92, 1.08, s));
          gl_FragColor = vec4(col * fade * vT.w, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`, transparent: true, depthWrite: false, blending: T.AdditiveBlending, side: T.DoubleSide });
    const trails = new T.Mesh(trG, trM); trails.frustumCulled = false; S.add(trails);

    // redshift ribbons (vertical strips from a source galaxy to us; a glowing wave whose wavelength grows along the way)
    const ribM = [], ribs = [];
    for (let k = 0; k < 3; k++) {
      const m = new T.ShaderMaterial({ uniforms: { uZ: { value: [.15, .5, 1.2][k] }, uL: { value: 10 }, uW: { value: 2 }, uT: { value: 0 }, uFront: { value: 0 }, uOp: { value: 0 } },
        vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position,1.); }',
        fragmentShader: `uniform float uZ, uL, uW, uT, uFront, uOp; varying vec2 vUv;
          void main(){ float s = vUv.x, lam0 = 1.7, xw = s * uL, yw = (vUv.y - .5) * uW;
            float phi = (uL / lam0) * log(1. + uZ * s) / uZ, A = .42;
            float y = A * sin(6.2832 * (phi - uT)), sl = A * cos(6.2832 * (phi - uT)) * 6.2832 / (lam0 * (1. + uZ * s));
            float d = abs(yw - y) / sqrt(1. + sl * sl);
            float I = exp(-pow(d / .045, 2.)) + .3 * exp(-pow(d / .16, 2.));
            float sh = clamp(uZ * s / 1.2, 0., 1.);
            vec3 col = sh < .5 ? mix(vec3(.62, .74, 1.), vec3(1., .78, .38), sh * 2.) : mix(vec3(1., .78, .38), vec3(1., .24, .12), sh * 2. - 1.);
            float m = smoothstep(uFront, uFront - .04, s) * smoothstep(0., .03, s) * smoothstep(1., .96, s);
            gl_FragColor = vec4(col * I * m * uOp * .75, 1.);
            #include <tonemapping_fragment>
            #include <colorspace_fragment>
          }`, transparent: true, depthWrite: false, blending: T.AdditiveBlending, side: T.DoubleSide });
      const r = new T.Mesh(new T.PlaneGeometry(1, 1).translate(.5, 0, 0), m); r.frustumCulled = false; r.matrixAutoUpdate = false; S.add(r); ribs.push(r); ribM.push(m); }

    // the treadmill photon
    const phDir = new T.Vector3().addScaledVector(Rv, .85).addScaledVector(Fv, .55).normalize();
    const ph1 = glow(S, '#fff6e0', 2.0, 0), ph2 = glow(S, '#ffd08a', 7, 0), phT = [];
    for (let k = 0; k < 14; k++) phT.push(glow(S, '#ffc070', 1.5 - k * .07, 0));
    // faint path on the grid from the photon to us
    const pathT = ctx.ctex(64, (g, s) => { const gr = g.createLinearGradient(0, 0, 0, s); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.5, 'rgba(255,255,255,1)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); });
    const path = new T.Mesh(new T.PlaneGeometry(1, 1).translate(.5, 0, 0).rotateX(-Math.PI / 2), new T.MeshBasicMaterial({ map: pathT, color: '#ffc070', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide }));
    S.add(path);

    const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .1, 3000); ctx.side(cam, p.side == null ? .12 : p.side);
    const RH = 30, KAP = .14, tgt = new T.Vector3(), v = new T.Vector3(), w = new T.Vector3(), e1 = new T.Vector3(), mb = new T.Matrix4();
    return { scene: S, camera: cam, draw(t, u) {
      ctx.t = t;
      const A = aOf(t), rs = on(cR, 2), st = on(cS, 3), lw = on(cL, 3), fs = on(cF, 3), tm = on(cM, 3);
      // camera: slow orbit, pulls back as space grows (galaxies themselves keep their size); moves in on the photon at treadmill
      const D = 46 * Math.pow(A, .7) * (1 - .32 * tm), az = az0 + u * .003 + .08 * Math.sin(u * .02), el = .43 - .06 * tm;
      tm > 0 ? tgt.copy(phDir).multiplyScalar(11 * tm).setY(1.5) : tgt.set(0, 1.5, 0);
      cam.position.set(tgt.x + Math.sin(az) * Math.cos(el) * D, tgt.y + Math.sin(el) * D, tgt.z + Math.cos(az) * Math.cos(el) * D); cam.lookAt(tgt);
      cam.updateMatrixWorld();
      gridM.uniforms.uA.value = A; gridM.uniforms.uCam.value.copy(cam.position); gridM.uniforms.uRingA.value = fs * (1 - .4 * tm);
      // galaxies
      const Lc = KAP * RH; trM.uniforms.uLc.value = Lc + (1 - fs) * 400;
      const trailK = lw * (1 - .7 * tm);
      for (let i = 0; i < N; i++) { const c = chi[i], x = c[0] * A, z = c[2] * A, y = c[1], rr = Math.hypot(x, z);
        const dc = Math.hypot(x - cam.position.x, y - cam.position.y, z - cam.position.z);
        let f = Math.exp(-Math.max(0, dc - D * 1.1) / (D * 1.3)) * sm(3, 9, dc) * (1 - .35 * tm);
        const red = fs * sm(RH * .96, RH * 1.12, rr), b = base[i];
        f *= 1 + .25 * red;
        GF.set(i, x, y, z, (b[0] * (1 - red) + red * 1.0) * f, (b[1] * (1 - red) + red * .3) * f, (b[2] * (1 - red) + red * .2) * f, 1);
        // trail
        const L = KAP * rr * trailK, o = i * 12, oa = i * 16;
        if (L < .02 || f < .01) { trA.fill(0, oa, oa + 16); continue; }
        const dx = x / rr, dz = z / rr; v.set(x - cam.position.x, y - cam.position.y, z - cam.position.z); e1.set(dx, 0, dz); w.crossVectors(e1, v).normalize();
        const hw = .22, tw = .11, tx = x - dx * L, tz = z - dz * L;
        trP.set([x + w.x * hw, y + w.y * hw, z + w.z * hw, x - w.x * hw, y - w.y * hw, z - w.z * hw, tx + w.x * tw, y + w.y * tw, tz + w.z * tw, tx - w.x * tw, y - w.y * tw, tz - w.z * tw], o);
        const I0 = Math.min(1, f * 1.3) * .34;
        trA.set([0, 1, L, I0, 0, -1, L, I0, L, 1, L, I0, L, -1, L, I0], oa); }
      GF.set(N, 0, 1.3, 0, 1.15, .92, .62, 1.4); GF.flush();
      trG.attributes.position.needsUpdate = true; trG.attributes.aT.needsUpdate = true;
      for (let i = 0; i < ND; i++) { const c = dChi[i]; dA[i * 3] = c[0] * A; dA[i * 3 + 1] = c[1]; dA[i * 3 + 2] = c[2] * A; }
      dust.geometry.attributes.position.needsUpdate = true;
      // ribbons: reveal from the source toward us (staggered), then fade once the grid starts to stretch
      const ribOp = rs * (1 - sm(cS + 2, cS + 10, t));
      for (let k = 0; k < 3; k++) { const m = ribM[k].uniforms, c = chi[k], sx = c[0] * A, sz = c[2] * A, sy = c[1];
        v.set(-sx, 1.3 - sy, -sz); const L = v.length(); v.normalize(); e1.set(0, 1, 0); w.crossVectors(v, e1).normalize(); e1.crossVectors(w, v);
        mb.makeBasis(v.clone().multiplyScalar(L), e1.clone().multiplyScalar(2.2), w); mb.setPosition(sx, sy, sz); ribs[k].matrix.copy(mb);
        m.uL.value = L; m.uW.value = 2.2; m.uT.value = (t - cR) * .45; m.uFront.value = Math.min(1.06, Math.max(0, (t - cR - k * 1.5) / 7)) * 1.06; m.uOp.value = ribOp;
        ribs[k].visible = ribOp > .002; }
      // photon: runs toward us at c, but the stretching grid under it first holds it, then carries it back
      const tau = t - cM, phv = tm > 0;
      const rp = RH * 1.12 - 2.2 * sm(0, 6, tau) + 11 * Math.pow(sm(5, 26, tau), 1.4);
      const px = phDir.x * rp, pz = phDir.z * rp; gridM.uniforms.uPh.value.set(px, pz); gridM.uniforms.uPhA.value = tm;
      ph1.position.set(px, 1.5, pz); ph2.position.copy(ph1.position); ph1.material.opacity = phv ? .95 * tm : 0; ph2.material.opacity = phv ? .32 * tm : 0;
      phT.forEach((s, k) => { const d = .4 + k * .45; s.position.set(px + phDir.x * d, 1.5, pz + phDir.z * d); s.material.opacity = phv ? tm * .55 * (1 - k / 14) : 0; });
      path.position.set(px, .06, pz); path.rotation.y = Math.atan2(pz, -px); path.scale.set(rp, 1, .9); path.material.opacity = phv ? .22 * tm : 0;
    } };
  };
})();
