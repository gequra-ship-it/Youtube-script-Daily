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
//             speed pass 2026-10-16: from here an endless stream of ~240 extra galaxies is born near us and carried out across the
//             grid ever faster (r = r_in * e^(lambda s), s = fract(F(t) * rate_k + phase_k); speed grows with distance, so they crawl
//             inside the ring and race beyond it, where they and their motion streaks turn red); they leave the view and respawn
//   treadmill S17 one photon (bright point + short tail) runs toward us from just beyond the ring; the grid stretches under it so it
//             barely advances, then it is dragged back; the camera moves in on it
//             (the stream keeps going but slows and dims a little, so the photon stays the thing to watch)
//   side      subject offset (default .12)
// Hubble staging pass 2026-10-16 (user: "the galaxy visuals are boring"): optional beats for the discovery chapter. Every one is
// off when its cue is absent, so shots without them (the law / faster-than-light chapters, the Shorts) are drawn exactly as before.
//   freeze    a frozen, eerily still universe: cold tint, a slow push in, the view behind a frosted pane of glass (a sheen sweeps
//             over it ~7.4 s later, on "static")
//   travel    a traveller crawls from us to the far edge of the grid, speeding up, arriving 6.3 s later ("...reach the edge")
//   shatter   the pane cracks (a first small crack 1.2 s before), then breaks into shards that fly off 0.35 s later; colour returns
//   scope     the 100-inch Hooker telescope builds up from the grid at the centre (open truss tube, mirror cell, English yoke);
//             3.7 s later faint light from four galaxies runs into the tube, down to the mirror (glint) and back up to the focus;
//             it dissolves again 10-13.5 s after the cue
//   shook     a gentle tremor of the view and a pulse ring through the grid
//   burst     every galaxy starts receding at once: flash, a shock shell and a pulse ring run out from the centre; the extra
//             expansion keeps going until the balloon beat, which hides its reset (so the next shot continues seamlessly)
//   spectrum  a big spectrum band (laboratory spectrum above, the galaxy's below, dark absorption lines) fed by a beam from a galaxy
//             through a prism;  shift: the galaxy's lines slide toward the red end (with guide lines from the rest positions)
//   ribOff    fade the redshift ribbons out from this cue (default: as before, after `stretch`)
//   siren     Doppler: a galaxy races away from us, emitting wave rings — bunched (blue) ahead, stretched (red) behind, toward us
//   farther   recession trails on every galaxy, length proportional to its distance (while the galaxies really recede)
//   everywhere pulse rings spread from several galaxies at once (every galaxy sees the others recede)
//   balloon   a translucent balloon inflates with galaxies on its skin moving apart (the field fades back behind it)
//   horror    the camera sinks toward the fabric and the frame darkens at the edges (on "horror", ~2.9 s later)
//   bullets   three galaxies shoot over the grid like bullets with long streaks, then dissolve ("not like bullets")
//   fabric    close-up on a 3D lattice of space around us with three galaxies on its nodes; the lattice stretches, the cells widen and
//             new lines fade in between the old ones; the camera pulls back out over the last 4.7 s of the shot
//   living    light pulses run outward through the lattice ("a living fabric")
//   cubes     glowing new cubes of space pop in between us and the galaxies, pushing them apart
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
  // integral of rate(x) dx from a to t (trapezoid on a fixed grid anchored at a, so it is a pure, continuous function of t:
  // seek-safe progress F(t) for recycled streams whose speed changes in any smooth way)
  M.integ = (f, a, t, h) => { if (!(t > a)) return 0; h = h || .1; const n = Math.floor((t - a) / h); let s = 0, y0 = f(a);
    for (let k = 1; k <= n; k++) { const y1 = f(a + k * h); s += (y0 + y1) * .5 * h; y0 = y1; }
    const x = a + n * h, d = t - x; return d > 0 ? s + (y0 + f(t)) * .5 * d : s; };

  // ---------------- motion streaks (speed pass 2026-10-16) ----------------
  // One instanced draw: each streak is a screen-space ribbon from a head point to a tail point (world coordinates), constant width
  // in pixels, a soft round cap at the head, fading toward the tail; colour blends head -> tail (additive light). Built in the vertex
  // shader from the real render camera, so the camera director's moves after draw() keep the streaks aligned.
  // api: set(i, hx, hy, hz, tx, ty, tz, r, g, b, px, r2, g2, b2) ; hide(i) ; flush()   (r..b linear light; px = full width in pixels)
  M.cosmicStreaks = function (ctx, n) {
    const T = ctx.T, g = new T.InstancedBufferGeometry();
    g.setAttribute('position', new T.Float32BufferAttribute([0, -1, 0, 0, 1, 0, 1, -1, 0, 1, 1, 0], 3)); g.setIndex([0, 2, 1, 1, 2, 3]);
    const H = new Float32Array(n * 3), Tl = new Float32Array(n * 3), C = new Float32Array(n * 4), C2 = new Float32Array(n * 3);
    const at = (a, k) => { const b = new T.InstancedBufferAttribute(a, k); b.setUsage(T.DynamicDrawUsage); return b; };
    const aH = at(H, 3), aT = at(Tl, 3), aC = at(C, 4), aC2 = at(C2, 3);
    g.setAttribute('iH', aH); g.setAttribute('iT', aT); g.setAttribute('iC', aC); g.setAttribute('iC2', aC2); g.instanceCount = n;
    const mat = new T.ShaderMaterial({ uniforms: { uRes: { value: new T.Vector2(ctx.W, ctx.H) } },
      vertexShader: `attribute vec3 iH, iT, iC2; attribute vec4 iC; uniform vec2 uRes; varying vec3 vC; varying float vAl, vLen, vHw, vAc;
        void main(){ vec4 ch = projectionMatrix * modelViewMatrix * vec4(iH, 1.), ct = projectionMatrix * modelViewMatrix * vec4(iT, 1.);
          vAl = 0.; vLen = 0.; vHw = 1.; vAc = 0.; vC = vec3(0.);
          if (ch.w < .05 || ct.w < .05 || dot(iC.rgb, vec3(1.)) < 1e-5) { gl_Position = vec4(2., 2., 2., 1.); return; }
          vec2 hr = uRes * .5, sh = ch.xy / ch.w * hr, st = ct.xy / ct.w * hr, d = st - sh; float len = length(d);
          vec2 dn = len > .01 ? d / len : vec2(1., 0.), nr = vec2(-dn.y, dn.x); float hw = max(.6, iC.w * .5), s = position.x;
          vec4 c = mix(ch, ct, s); vec2 off = nr * position.y * hw - dn * hw * (1. - s);
          c.xy += off / hr * c.w; gl_Position = c;
          vAl = s * (len + hw); vLen = len; vHw = hw; vAc = position.y; vC = mix(iC.rgb, iC2, s); }`,
      fragmentShader: `varying vec3 vC; varying float vAl, vLen, vHw, vAc;
        void main(){ float cap = smoothstep(0., vHw * 1.6, vAl), tail = pow(clamp(1. - (vAl - vHw) / max(vLen, 1.), 0., 1.), 1.4);
          float I = cap * tail * exp(-vAc * vAc * 2.6);
          gl_FragColor = vec4(vC * I, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`, transparent: true, depthWrite: false, blending: T.AdditiveBlending });
    const mesh = new T.Mesh(g, mat); mesh.frustumCulled = false;
    return { mesh, n,
      set(i, hx, hy, hz, tx, ty, tz, r, gg, b, px, r2, g2, b2) { const j = i * 3; H[j] = hx; H[j + 1] = hy; H[j + 2] = hz; Tl[j] = tx; Tl[j + 1] = ty; Tl[j + 2] = tz;
        C[i * 4] = r; C[i * 4 + 1] = gg; C[i * 4 + 2] = b; C[i * 4 + 3] = px; C2[j] = r2 == null ? r : r2; C2[j + 1] = g2 == null ? gg : g2; C2[j + 2] = b2 == null ? b : b2; },
      hide(i) { C[i * 4] = C[i * 4 + 1] = C[i * 4 + 2] = 0; },
      flush() { aH.needsUpdate = aT.needsUpdate = aC.needsUpdate = aC2.needsUpdate = true; } };
  };

  // ---------------- uniform lines (Hubble staging pass 2026-10-16) ----------------
  // One instanced draw of screen-space ribbons between two world points: constant width in pixels, constant brightness along the
  // line, soft edges. Instances with flag 1 fade out toward the faces of the box uBoxC +- uBoxH and carry a light pulse (a shell of
  // radius uPR around uPC, strength uPA). api: set(i, ax, ay, az, bx, by, bz, r, g, b, px, flag) ; hide(i) ; flush()
  M.cosmicLines = function (ctx, n) {
    const T = ctx.T, g = new T.InstancedBufferGeometry();
    g.setAttribute('position', new T.Float32BufferAttribute([0, -1, 0, 0, 1, 0, 1, -1, 0, 1, 1, 0], 3)); g.setIndex([0, 2, 1, 1, 2, 3]);
    const A = new Float32Array(n * 3), B = new Float32Array(n * 3), C = new Float32Array(n * 4), F = new Float32Array(n);
    const at = (a, k) => { const b = new T.InstancedBufferAttribute(a, k); b.setUsage(T.DynamicDrawUsage); return b; };
    const aA = at(A, 3), aB = at(B, 3), aC = at(C, 4), aF = at(F, 1);
    g.setAttribute('iA', aA); g.setAttribute('iB', aB); g.setAttribute('iC', aC); g.setAttribute('iF', aF); g.instanceCount = n;
    const U = { uRes: { value: new T.Vector2(ctx.W, ctx.H) }, uBoxC: { value: new T.Vector3() }, uBoxH: { value: new T.Vector3(1, 1, 1) },
      uPC: { value: new T.Vector3() }, uPR: { value: 0 }, uPA: { value: 0 } };
    const mat = new T.ShaderMaterial({ uniforms: U,
      vertexShader: `attribute vec3 iA, iB; attribute vec4 iC; attribute float iF; uniform vec2 uRes; varying vec3 vC, vW; varying float vAc, vF;
        void main(){ vec4 ca = projectionMatrix * modelViewMatrix * vec4(iA, 1.), cb = projectionMatrix * modelViewMatrix * vec4(iB, 1.);
          vC = iC.rgb; vF = iF; vAc = position.y; float s = position.x; vW = mix(iA, iB, s);
          if (ca.w < .05 || cb.w < .05 || dot(iC.rgb, vec3(1.)) < 1e-5) { gl_Position = vec4(2., 2., 2., 1.); return; }
          vec2 hr = uRes * .5, d = cb.xy / cb.w * hr - ca.xy / ca.w * hr; float len = length(d);
          vec2 dn = len > .01 ? d / len : vec2(1., 0.), nr = vec2(-dn.y, dn.x); float hw = max(.6, iC.w * .5);
          vec4 c = mix(ca, cb, s); c.xy += nr * position.y * hw / hr * c.w; gl_Position = c; }`,
      fragmentShader: `uniform vec3 uBoxC, uBoxH, uPC; uniform float uPR, uPA; varying vec3 vC, vW; varying float vAc, vF;
        void main(){ float I = exp(-vAc * vAc * 2.2);
          if (vF > .5) { vec3 q = abs(vW - uBoxC) / uBoxH; I *= (1. - smoothstep(.62, 1., q.x)) * (1. - smoothstep(.62, 1., q.y)) * (1. - smoothstep(.62, 1., q.z));
            float d = length(vW - uPC) - uPR; I *= 1. + uPA * exp(-d * d / 1.8); }
          gl_FragColor = vec4(vC * I, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`, transparent: true, depthWrite: false, blending: T.AdditiveBlending });
    const mesh = new T.Mesh(g, mat); mesh.frustumCulled = false;
    return { mesh, n, U,
      set(i, ax, ay, az, bx, by, bz, r, gg, b, px, fl) { const j = i * 3; A[j] = ax; A[j + 1] = ay; A[j + 2] = az; B[j] = bx; B[j + 1] = by; B[j + 2] = bz;
        C[i * 4] = r; C[i * 4 + 1] = gg; C[i * 4 + 2] = b; C[i * 4 + 3] = px; F[i] = fl || 0; },
      hide(i) { C[i * 4] = C[i * 4 + 1] = C[i * 4 + 2] = 0; },
      flush() { aA.needsUpdate = aB.needsUpdate = aC.needsUpdate = aF.needsUpdate = true; } };
  };

  // ---------------- the scene ----------------
  M.scenes.expanse = function (ctx, p) {
    const { T, sm, rng, cue, points, glow } = ctx;
    const S = new T.Scene(); S.background = new T.Color('#05071a');
    const cT = c => c == null ? 1e9 : cue(c);
    const cR = cT(p.redshift), cS = cT(p.stretch), cL = cT(p.law), cF = cT(p.fast), cM = cT(p.treadmill);
    const on = (c0, d) => sm(c0, c0 + d, ctx.t);
    // Hubble staging beats (all optional; 1e9 = off)
    const cFz = cT(p.freeze), cTv = cT(p.travel), cSh = cT(p.shatter), cSc = cT(p.scope), cSk = cT(p.shook), cB = cT(p.burst),
      cSp = cT(p.spectrum), cShf = cT(p.shift), cRo = cT(p.ribOff), cDp = cT(p.siren), cFa = cT(p.farther), cEv = cT(p.everywhere),
      cBa = cT(p.balloon), cHo = cT(p.horror), cBu = cT(p.bullets), cFb = cT(p.fabric), cLv = cT(p.living), cCu = cT(p.cubes);
    const X = [cFz, cTv, cSh, cSc, cSk, cB, cSp, cDp, cFa, cEv, cBa, cHo, cBu, cFb, cCu].some(c => c < 1e8);
    // extra expansion of the burst: a kick, then a steady recession; reset to 0 while the balloon hides the field
    const Eof = t => { if (!(t > cB)) return 0; const q = Math.min(60, t - cB);
      return (.25 * (1 - Math.exp(-q / 3)) + .02 * q) * sm(cB - .1, cB + .6, t) * (1 - sm(cBa + 1.2, cBa + 3.4, t)); };
    // fabric close-up: its own scale factor S(t) (log S grows slowly from the cue, faster once the new cubes appear)
    const Sof = t => Math.exp(.035 * M.ismooth(cFb + 1, cFb + 4, t) + .06 * M.ismooth(cCu + 1.5, cCu + 3.5, t));
    const tEnd = ctx.t1 == null ? 1e9 : ctx.t1, cOut = cFb < 1e8 ? tEnd - 4.7 : 1e9;
    // expansion: a(t) = exp(sum of long smooth ramps) — bounded (x3.9 in all) and independent of the shot span, so a second
    // instance of this stage (e.g. after the S13 data card) given the same cues continues exactly where the first one stopped
    const W = [[cS, 30, .45], [cL, 35, .3], [cF, 35, .35], [cM, 25, .25]];
    const aOf = t => Math.exp(W.reduce((s, [c, d, w]) => s + w * sm(c, c + d, t), 0));

    ctx.stars(S, 2400, 700, { size: 1.3, opacity: .55, seed: 17 });
    // far nebula haze (violet / blue), few large sprites
    const RN = rng(5); for (let k = 0; k < 4; k++) { const s = glow(S, k % 2 ? '#3b2f86' : '#22306e', 380 + RN() * 200, .16 + RN() * .08); const a = -1.2 + k * .9 + RN() * .4; s.position.set(Math.sin(a) * 600, 40 + RN() * 160, -Math.cos(a) * 600 - 100); }

    // grid: log-periodic comoving lattice, distance fade, light-speed ring, warm centre, brighter under the photon
    const gridM = new T.ShaderMaterial({ uniforms: { uA: { value: 1 }, uBase: { value: 4 }, uRing: { value: 30 }, uRingA: { value: 0 }, uCam: { value: new T.Vector3() }, uPh: { value: new T.Vector2() }, uPhA: { value: 0 },
        uDim: { value: 1 }, uPr: { value: Array.from({ length: 8 }, () => new T.Vector4()) }, uPrN: { value: 0 } }, defines: { BEATS: X ? 1 : 0 },
      vertexShader: 'varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position,1.); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }',
      fragmentShader: `uniform float uA, uBase, uRing, uRingA, uPhA, uDim; uniform vec3 uCam; uniform vec2 uPh; uniform vec4 uPr[8]; uniform int uPrN; varying vec3 vW;
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
          #if BEATS == 1
          for (int i = 0; i < 8; i++) { if (i >= uPrN) break; vec4 P = uPr[i]; float d = abs(length(vW.xz - P.xy) - P.z);
            col += vec3(.62, .8, 1.) * P.w * (exp(-pow(d / (.3 + .004 * P.z + fr), 2.)) + .22 * exp(-d / 2.5)) * (1. - smoothstep(140., 260., dc)); }
          col *= uDim;
          #endif
          gl_FragColor = vec4(col, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }`, transparent: true, depthWrite: false, blending: T.AdditiveBlending });
    const grid = new T.Mesh(new T.PlaneGeometry(900, 900).rotateX(-Math.PI / 2), gridM); grid.renderOrder = -1; S.add(grid);

    // camera basis at build (az0) to place the special galaxies on the screen side
    const az0 = .45, Rv = new T.Vector3(Math.cos(az0), 0, -Math.sin(az0)), Fv = new T.Vector3(-Math.sin(az0), 0, -Math.cos(az0));
    const N = 1000, NQ = 240, NX = X ? 92 : 0, XI = N + 1 + NQ, GF = M.cosmicGal(ctx, N + 1 + NQ + NX), R1 = rng(23), chi = [], base = [];
    const SRC = [[10, 2], [4, 17], [20, 30]];   // three ribbon sources: (right, forward) in camera basis
    for (let i = 0; i < N; i++) { let x, z;
      if (i < 3) { x = Rv.x * SRC[i][0] + Fv.x * SRC[i][1]; z = Rv.z * SRC[i][0] + Fv.z * SRC[i][1]; }
      else { const rr = 3.5 + 72 * Math.sqrt(R1()), a = R1() * 6.283; x = Math.cos(a) * rr; z = Math.sin(a) * rr; }
      const y = .6 + 4.2 * Math.pow(R1(), 1.5);
      const kind = GF.random(i, R1, .9, 2.6); if (i < 3) GF.shape(i, 1.7, R1() * 6.28, .5 + .2 * i, i === 2 ? 2 : 0, 1);
      const cu = R1(), br = .45 + .6 * R1(), col = kind === 1 ? [1, .8, .55] : cu < .5 ? [1, .86, .64] : cu < .82 ? [.8, .74, 1] : [.86, .9, 1];
      chi.push([x, y, z]); base.push([col[0] * br, col[1] * br, col[2] * br]); }
    GF.shape(N, 2.3, .6, .42, 0, 1.4); S.add(GF.mesh);   // the Milky Way at the centre
    // the speed stream (instances N+1..N+NQ) and its streaks
    const R5 = rng(59), QD = [];
    for (let k = 0; k < NQ; k++) { const a = R5() * 6.283, y = .6 + 4.2 * Math.pow(R5(), 1.5), rin = 6 + 4 * R5();
      const kind = GF.random(N + 1 + k, R5, .9, 2.4), cu = R5(), br = .45 + .6 * R5(), col = kind === 1 ? [1, .8, .55] : cu < .5 ? [1, .86, .64] : cu < .82 ? [.8, .74, 1] : [.86, .9, 1];
      QD.push([Math.cos(a), y, Math.sin(a), rin, .8 + .4 * R5(), R5(), col[0] * br, col[1] * br, col[2] * br, Math.log(160 / rin)]); }
    const SK = M.cosmicStreaks(ctx, NQ); S.add(SK.mesh);
    const rateF = x => sm(cF, cF + 4, x) * (.03 + .012 * (Math.exp(Math.min(x - cF, cM - cF, 45) / 14) - 1)) * (1 - .45 * sm(cM, cM + 6, x));
    const Fof = t => M.integ(rateF, cF, t, .1), fr = x => x - Math.floor(x);
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

    // ================= Hubble staging beats (built only when one of their cues is given) =================
    function buildBeats() {
      const sm2 = (a, b, c, d, x) => sm(a, b, x) * (1 - sm(c, d, x)), cl = x => Math.min(1, Math.max(0, x));
      const eOut = (x, k) => 1 - Math.pow(1 - cl(x), k || 3), fract = x => x - Math.floor(x);
      const up = new T.Vector3(0, 1, 0), V3 = (x, y, z) => new T.Vector3(x, y, z), RX = rng(71);
      for (let k = 0; k < NX; k++) GF.random(XI + k, RX, .7, 1.5);
      const gOff = j => GF.set(j, 0, 0, 0, 0, 0, 0, 0);
      const LAT = 779, LCU = LAT, LSC = LAT + 240, LSP = LSC + 8, LL = M.cosmicLines(ctx, LSP + 8); S.add(LL.mesh);
      const SK2 = M.cosmicStreaks(ctx, 32); S.add(SK2.mesh);
      const sideF = p.side == null ? .12 : p.side, asp = ctx.W / ctx.H;
      const cR0 = new T.Vector3(), cU0 = new T.Vector3(), cF0 = new T.Vector3(), tmp = new T.Vector3(), tmp2 = new T.Vector3();
      // a world point that appears at screen (sx, sy) (0..1, y down) at distance d in front of the scene camera
      const scr = (sx, sy, d, out) => { const h = d * Math.tan(cam.fov * Math.PI / 360);
        return (out || new T.Vector3()).copy(cam.position).addScaledVector(cF0, d).addScaledVector(cR0, (sx - .5 - sideF) * 2 * h * asp).addScaledVector(cU0, -(sy - .5) * 2 * h); };

      // ---- the pane of glass: frost while frozen, cracks, shards flying off (clip-space geometry, premultiplied alpha) ----
      let pane = null;
      if (cFz < 1e8 || cSh < 1e8) {
        const RAD = [0, .06, .15, .29, .5, .82, 1.3, 2.4], NG = RAD.length - 1, NRay = 16, R2 = rng(83), ang = [], Vt = [];
        for (let j = 0; j < NRay; j++) ang.push((j + .55 * (R2() - .5)) / NRay * 6.2832);
        for (let i = 0; i <= NG; i++) { Vt.push([]); for (let j = 0; j < NRay; j++) { const a = ang[j] + (i ? (R2() - .5) * .3 : 0), r = RAD[i] * (1 + (R2() - .5) * .34); Vt[i].push([Math.cos(a) * r, Math.sin(a) * r]); } }
        const pos = [], aC = [], aR = [], aE = [];
        const dist = (P, a, b) => { const ex = b[0] - a[0], ey = b[1] - a[1], L = Math.hypot(ex, ey); return L < 1e-6 ? 9 : Math.abs((P[0] - a[0]) * ey - (P[1] - a[1]) * ex) / L; };
        for (let i = 0; i < NG; i++) for (let j = 0; j < NRay; j++) {
          const q = [Vt[i][j], Vt[i][(j + 1) % NRay], Vt[i + 1][(j + 1) % NRay], Vt[i + 1][j]], cx = (q[0][0] + q[1][0] + q[2][0] + q[3][0]) / 4, cy = (q[0][1] + q[1][1] + q[2][1] + q[3][1]) / 4, rr = R2();
          [0, 1, 2, 0, 2, 3].forEach(k => { const P = q[k]; pos.push(P[0], P[1], 0); aC.push(cx, cy); aR.push(rr, i / (NG - 1)); aE.push(dist(P, q[0], q[1]), dist(P, q[1], q[2]), dist(P, q[2], q[3]), dist(P, q[3], q[0])); }); }
        const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('aC', new T.Float32BufferAttribute(aC, 2));
        g.setAttribute('aR', new T.Float32BufferAttribute(aR, 2)); g.setAttribute('aE', new T.Float32BufferAttribute(aE, 4));
        const U = { uSh: { value: -1 }, uAsp: { value: asp }, uImp: { value: new T.Vector2(.6, .45) }, uFrost: { value: 0 }, uCrack: { value: 0 }, uGlint: { value: 0 }, uSheen: { value: -1 }, uTint: { value: 0 } };
        const m = new T.ShaderMaterial({ uniforms: U,
          vertexShader: `attribute vec2 aC, aR; attribute vec4 aE; uniform float uSh, uAsp; uniform vec2 uImp; varying vec2 vP; varying vec4 vE; varying float vA; varying vec2 vR;
            void main(){ vec2 p = position.xy; vP = p; vE = aE; vR = aR;
              float tau = max(0., uSh - aR.y * .3 - aR.x * .22), an = tau * (aR.x - .5) * 2.4, cs = cos(an), sn = sin(an);
              vec2 q = p - aC; q = vec2(cs * q.x - sn * q.y, sn * q.x + cs * q.y) * (1. + .5 * tau);
              vec2 dir = aC / max(length(aC), 1e-3), c = aC + dir * (.35 * tau + .5 * tau * tau) * (.5 + aR.x) + vec2(0., -.6 * tau * tau);
              vec2 pp = c + q; vA = 1. - smoothstep(.1, 1.25, tau);
              gl_Position = vec4((pp.x / uAsp + uImp.x) * 2. - 1., (pp.y + uImp.y) * 2. - 1., 0., 1.); }`,
          fragmentShader: `uniform float uFrost, uCrack, uGlint, uSheen, uTint, uAsp; uniform vec2 uImp; varying vec2 vP; varying vec4 vE; varying float vA; varying vec2 vR;
            void main(){ vec2 uv = vec2(vP.x / uAsp + uImp.x, vP.y + uImp.y); float r = length(vP);
              float d = min(min(vE.x, vE.y), min(vE.z, vE.w)), on = 1. - smoothstep(uCrack - .04, uCrack, r);
              float edge = on * (exp(-d / .0009) * .75 + exp(-d / .0045) * .13) * (.55 + .7 * vR.x);
              float vig = smoothstep(.3, .8, length((uv - .5) * vec2(1.25, 1.)));
              float fro = uFrost * (.12 + .88 * vig);
              float sheen = exp(-pow((uv.x + uv.y * .55 - uSheen) / .05, 2.)) * .06 * uFrost;
              vec3 rgb = vec3(.6, .74, 1.) * fro * .12 + vec3(.85, .93, 1.) * (edge + sheen) + vec3(.04, .07, .14) * uTint
                + vec3(1., .97, .9) * uGlint * (exp(-r / .018) * .9 + exp(-r / .08) * .22);
              float a = clamp(uTint + fro * .12, 0., .6);
              if (a + rgb.r + rgb.g + rgb.b < .002) discard;
              gl_FragColor = vec4(rgb * vA, a * vA); }`,
          transparent: true, depthTest: false, depthWrite: false, side: T.DoubleSide, blending: T.CustomBlending, blendSrc: T.OneFactor, blendDst: T.OneMinusSrcAlphaFactor, blendEquation: T.AddEquation });
        const mesh = new T.Mesh(g, m); mesh.frustumCulled = false; mesh.renderOrder = 1000; S.add(mesh); pane = { mesh, U };
      }
      // ---- screen vignette (horror) ----
      let vig = null;
      if (cHo < 1e8) { const m = new T.ShaderMaterial({ uniforms: { uV: { value: 0 } },
          vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = vec4(position.xy * 2., 0., 1.); }',
          fragmentShader: 'uniform float uV; varying vec2 vUv; void main(){ float r = length((vUv - .5) * vec2(1.3, 1.)); gl_FragColor = vec4(0., 0., 0., uV * (.16 + .84 * smoothstep(.22, .85, r))); }',
          transparent: true, depthTest: false, depthWrite: false, blending: T.CustomBlending, blendSrc: T.OneFactor, blendDst: T.OneMinusSrcAlphaFactor, blendEquation: T.AddEquation });
        vig = new T.Mesh(new T.PlaneGeometry(1, 1), m); vig.frustumCulled = false; vig.renderOrder = 999; S.add(vig); }

      // ---- traveller to the edge ----
      const dirT = new T.Vector3().addScaledVector(Fv, .93).addScaledVector(Rv, .22).normalize();
      const tv1 = glow(S, '#fff3da', 2.6, 0), tv2 = glow(S, '#ffcf8a', 8, 0);

      // ---- the Hooker telescope ----
      let tel = null;
      if (cSc < 1e8) {
        const hz = new T.Vector3().addScaledVector(Rv, .9).addScaledVector(Fv, .42).normalize(), el0 = 26 * Math.PI / 180, pl = 34 * Math.PI / 180;
        const Dt = hz.clone().multiplyScalar(Math.cos(el0)).addScaledVector(up, Math.sin(el0)), P = hz.clone().multiplyScalar(Math.cos(pl)).addScaledVector(up, Math.sin(pl));
        const Ex = new T.Vector3().crossVectors(up, hz).normalize(), Uv = Ex.clone(), Vv = new T.Vector3().crossVectors(Dt, Ex).normalize();
        const C = V3(0, 4.2, 0).addScaledVector(Rv, -6), grp = new T.Group(); S.add(grp);
        const cutU = { value: -1 }, cutG = { value: 0 };
        const mat = (color, metal, rough) => { const m = new T.MeshPhongMaterial({ color, specular: new T.Color(metal * .55, metal * .58, metal * .62), shininess: 8 + (1 - rough) * 70 });
          m.onBeforeCompile = sh => { sh.uniforms.uCut = cutU; sh.uniforms.uCutG = cutG;
            sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying float vWy;').replace('#include <project_vertex>', '#include <project_vertex>\nvWy = (modelMatrix * vec4(transformed, 1.)).y;');
            sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float uCut, uCutG; varying float vWy;').replace('void main() {', 'void main() {\nif (vWy > uCut) discard;')
              .replace('#include <dithering_fragment>', '#include <dithering_fragment>\ngl_FragColor.rgb += vec3(.45, .75, 1.) * uCutG * exp(-(uCut - vWy) / .16);'); };
          return m; };
        const steel = mat('#3c4556', .8, .4), dark = mat('#1c212c', .6, .55), conc = mat('#3e404c', .1, .9), mirror = mat('#b8c8e0', 1.4, .05);
        const seg = (a, b, r, m, sides) => { const d = b.clone().sub(a), L = d.length(), o = new T.Mesh(new T.CylinderGeometry(r, r, L, sides || 10), m);
          o.position.copy(a).addScaledVector(d, .5); o.quaternion.setFromUnitVectors(up, d.normalize()); grp.add(o); return o; };
        const bar = (a, b, wd, m) => { const d = b.clone().sub(a), L = d.length(), o = new T.Mesh(new T.BoxGeometry(wd, L, wd), m);
          o.position.copy(a).addScaledVector(d, .5); o.quaternion.setFromUnitVectors(up, d.normalize()); grp.add(o); return o; };
        const ring = (c, R, r, m) => { const o = new T.Mesh(new T.TorusGeometry(R, r, 8, 48), m); o.position.copy(c); o.quaternion.setFromUnitVectors(V3(0, 0, 1), Dt); grp.add(o); return o; };
        const at = (s, a, b) => C.clone().addScaledVector(Dt, s).addScaledVector(Uv, a || 0).addScaledVector(Vv, b || 0);
        { const o = new T.Mesh(new T.CylinderGeometry(3.6, 3.8, .3, 40), conc); o.position.set(C.x, .15, C.z); grp.add(o); }
        const pS = C.clone().addScaledVector(P, -5), pN = C.clone().addScaledVector(P, 5);
        { const o = new T.Mesh(new T.BoxGeometry(1.5, pS.y, 1.9), conc); o.position.set(pS.x, pS.y / 2, pS.z); o.quaternion.setFromUnitVectors(V3(1, 0, 0), Ex); grp.add(o); }
        { const o = new T.Mesh(new T.BoxGeometry(1.5, pN.y, 1.9), conc); o.position.set(pN.x, pN.y / 2, pN.z); o.quaternion.setFromUnitVectors(V3(1, 0, 0), Ex); grp.add(o); }
        for (const s of [-1, 1]) { bar(pS.clone().addScaledVector(Ex, 1.6 * s), pN.clone().addScaledVector(Ex, 1.6 * s), .42, steel);
          seg(C.clone().addScaledVector(Ex, 1.2 * s), C.clone().addScaledVector(Ex, 1.62 * s), .24, dark); }
        bar(pS.clone().addScaledVector(Ex, -1.8), pS.clone().addScaledVector(Ex, 1.8), .5, steel); bar(pN.clone().addScaledVector(Ex, -1.8), pN.clone().addScaledVector(Ex, 1.8), .5, steel);
        seg(at(-.65), at(.65), 1.2, dark, 32); seg(at(-3.75), at(-2.9), 1.22, dark, 32); ring(at(3.6), 1.12, .085, steel); ring(at(2.1), 1.12, .05, steel); ring(at(-1.9), 1.15, .05, steel);
        const o8 = k => { const a = k / 8 * 6.2832; return [Math.cos(a) * 1.12, Math.sin(a) * 1.12]; };
        for (let k = 0; k < 8; k++) { const [a, b] = o8(k), [a2, b2] = o8(k + 1);
          seg(at(.65, a, b), at(3.6, a, b), .05, steel, 6); seg(at(-.65, a, b), at(-2.9, a, b), .055, steel, 6);
          seg(at(.65, a, b), at(2.1, a2, b2), .03, steel, 5); seg(at(2.1, a2, b2), at(3.6, a, b), .03, steel, 5); seg(at(-.65, a, b), at(-2.9, a2, b2), .035, steel, 5); }
        seg(at(3.05), at(3.95), .34, dark, 16);
        for (const [a, b] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) bar(at(3.6, a * .34, b * .34), at(3.6, a * 1.1, b * 1.1), .04, steel);
        { const o = new T.Mesh(new T.CircleGeometry(1.0, 48), mirror); o.position.copy(at(-2.88)); o.quaternion.setFromUnitVectors(V3(0, 0, 1), Dt); grp.add(o); }
        const key = new T.DirectionalLight('#d8e2ff', 2.4); key.position.copy(C).addScaledVector(Rv, -12).addScaledVector(Fv, -10).addScaledVector(up, 16); key.target.position.copy(C);
        const rim = new T.DirectionalLight('#ffd49a', 3.2); rim.position.copy(C).addScaledVector(Rv, 9).addScaledVector(Fv, 12).addScaledVector(up, 5); rim.target.position.copy(C);
        S.add(key, key.target, rim, rim.target, new T.HemisphereLight('#5868b0', '#0a0a12', .7));
        // light from four galaxies: source -> aperture point -> down the tube to the mirror -> back up to the focus
        const SRCo = [[7.4, -2.2, 1.5], [9, 1.9, 2.0], [7, 2.3, -1.5], [9.6, -1.2, -2.2]], paths = SRCo.map(([d, a, b]) => {
          const s0 = at(d, a, b), n = Math.hypot(a, b), ap = at(3.6, a / n * .62, b / n * .62), mi = ap.clone().addScaledVector(Dt, -6.48), fo = at(3.3);
          const L1 = s0.distanceTo(ap), L2 = ap.distanceTo(mi), L3 = mi.distanceTo(fo); return { pts: [s0, ap, mi, fo], L: [L1, L2, L3], Lt: L1 + L2 + L3 }; });
        const glint = glow(S, '#eaf3ff', 3.2, 0); glint.position.copy(at(-2.8));
        tel = { grp, cutU, cutG, paths, glint, C, Dt };
      }

      // ---- burst: flash + shock shell ----
      const shellMat = (col, lines) => new T.ShaderMaterial({ uniforms: { uOp: { value: 0 }, uCol: { value: new T.Color(col) }, uLines: { value: lines } },
        vertexShader: 'varying vec3 vN, vV; varying vec2 vUv; void main(){ vec4 w = modelMatrix * vec4(position, 1.); vN = normalize(mat3(modelMatrix) * normal); vV = cameraPosition - w.xyz; vUv = uv; gl_Position = projectionMatrix * viewMatrix * w; }',
        fragmentShader: `uniform float uOp, uLines; uniform vec3 uCol; varying vec3 vN, vV; varying vec2 vUv;
          void main(){ float fr = pow(1. - abs(dot(normalize(vN), normalize(vV))), 2.4 + 2.6 * (1. - uLines));
            vec2 q = vec2(vUv.x * 24., vUv.y * 12.), wq = fwidth(q), dq = abs(fract(q + .5) - .5), lq = 1. - smoothstep(wq * .4, wq * 1.4, dq);
            float gl = uLines * max(lq.x, lq.y) * (.25 + .75 * fr);
            gl_FragColor = vec4(uCol * (.035 * uLines + .9 * fr + .4 * gl) * uOp, 1.);
            #include <tonemapping_fragment>
            #include <colorspace_fragment>
          }`, transparent: true, depthWrite: false, blending: T.AdditiveBlending, side: T.DoubleSide });
      const shell = new T.Mesh(new T.SphereGeometry(1, 64, 32), shellMat('#ffe2b8', 0)); shell.position.set(0, 1.5, 0); shell.visible = false; S.add(shell);
      const flash = glow(S, '#fff1d8', 13, 0); flash.position.set(0, 1.5, 0);
      const balloon = new T.Mesh(new T.SphereGeometry(1, 64, 32), shellMat('#a9c8ff', 1)); balloon.position.set(0, 1.5, 0); balloon.visible = false; S.add(balloon);
      const NB = 80, bDir = [], bCol = [];
      for (let k = 0; k < NB; k++) { const yy = 1 - 2 * (k + .5) / NB, r = Math.sqrt(1 - yy * yy), a = k * 2.39996; bDir.push(V3(Math.cos(a) * r, yy, Math.sin(a) * r));
        const cu = RX(); bCol.push(cu < .5 ? [1, .86, .64] : cu < .8 ? [.8, .74, 1] : [.86, .9, 1]); GF.shape(XI + 12 + k, .55 + .35 * RX(), RX() * 6.28, .5 + .5 * RX(), Math.floor(RX() * 5), 1); }

      // ---- spectrum band, prism ----
      let spec = null;
      if (cSp < 1e8) {
        const m = new T.ShaderMaterial({ uniforms: { uZ: { value: 0 }, uRev: { value: 0 }, uOp: { value: 0 }, uArr: { value: 0 } },
          vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }',
          fragmentShader: `uniform float uZ, uRev, uOp, uArr; varying vec2 vUv;
            vec3 wl(float l){ vec3 c; if (l < 440.) c = vec3(-(l - 440.) / 60., 0., 1.); else if (l < 490.) c = vec3(0., (l - 440.) / 50., 1.); else if (l < 510.) c = vec3(0., 1., -(l - 510.) / 20.);
              else if (l < 580.) c = vec3((l - 510.) / 70., 1., 0.); else if (l < 645.) c = vec3(1., -(l - 645.) / 65., 0.); else c = vec3(1., 0., 0.);
              float f = l < 420. ? .3 + .7 * (l - 380.) / 40. : l > 690. ? .3 + .7 * (720. - l) / 30. : 1.; return pow(c, vec3(2.)) * f; }
            float ab(float l, float z){ float a = 0.;
              a = max(a, exp(-pow((l - 393.4 * (1. + z)) / 1.8, 2.))); a = max(a, exp(-pow((l - 396.8 * (1. + z)) / 1.8, 2.)));
              a = max(a, .7 * exp(-pow((l - 410.2 * (1. + z)) / 1.6, 2.))); a = max(a, .8 * exp(-pow((l - 434.0 * (1. + z)) / 1.7, 2.)));
              a = max(a, .9 * exp(-pow((l - 486.1 * (1. + z)) / 1.9, 2.))); a = max(a, .65 * exp(-pow((l - 517.3 * (1. + z)) / 1.7, 2.)));
              a = max(a, .85 * exp(-pow((l - 589.3 * (1. + z)) / 1.9, 2.))); a = max(a, exp(-pow((l - 656.3 * (1. + z)) / 2.2, 2.))); return a; }
            void main(){ float u = vUv.x, y = vUv.y, l = 380. + 340. * u; vec3 cont = wl(l) * 1.25 * (.6 + .4 * smoothstep(0., .08, u) * smoothstep(1., .92, u));
              float e1 = smoothstep(0., .04, y) * smoothstep(.44, .40, y), e2 = smoothstep(.68, .71, y) * smoothstep(.94, .91, y);
              vec3 col = cont * e1 * (1. - .93 * ab(l, uZ)) + cont * e2 * .62 * (1. - .93 * ab(l, 0.));
              float g = (y - .45) / .22;
              if (g > 0. && g < 1.) { float zz = uZ * (1. - g), a = 0.;
                for (int i = 0; i < 8; i++) { float l0 = i == 0 ? 393.4 : i == 1 ? 396.8 : i == 2 ? 410.2 : i == 3 ? 434.0 : i == 4 ? 486.1 : i == 5 ? 517.3 : i == 6 ? 589.3 : 656.3;
                  a = max(a, exp(-pow((l - l0 * (1. + zz)) / .55, 2.))); }
                col += vec3(.9, .92, 1.) * a * uArr * .45 * smoothstep(0., .1, g) * smoothstep(1., .9, g); }
              col += vec3(.5, .6, 1.) * .05 * (e1 + e2);
              gl_FragColor = vec4(col * uOp * smoothstep(uRev, uRev - .03, u), 1.);
              #include <tonemapping_fragment>
              #include <colorspace_fragment>
            }`, transparent: true, depthWrite: false, blending: T.AdditiveBlending, side: T.DoubleSide });
        const band = new T.Mesh(new T.PlaneGeometry(1, 1), m); band.frustumCulled = false; band.renderOrder = 5; S.add(band);
        const pg = new T.CylinderGeometry(1, 1, 1, 3), prism = new T.Mesh(pg, new T.MeshBasicMaterial({ color: '#9fbcff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false }));
        const pe = new T.LineSegments(new T.EdgesGeometry(pg), new T.LineBasicMaterial({ color: '#ffffff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false })); prism.add(pe);
        S.add(prism); const pgl = glow(S, '#ffffff', 2, 0);
        spec = { band, m, prism, pe, pgl, qT: new T.Quaternion().setFromAxisAngle(up, -.24), qP: new T.Quaternion().setFromEuler(new T.Euler(Math.PI / 2, .5, .3)) };
      }
      // ---- Doppler wave rings ----
      let dop = null;
      if (cDp < 1e8) {
        const P0 = V3(0, 0, 0).addScaledVector(Rv, 3.6).addScaledVector(Fv, 1.4), dir = new T.Vector3().addScaledVector(Rv, .86).addScaledVector(Fv, .5).normalize(), Pc = P0.clone().addScaledVector(dir, 15);
        const m = new T.ShaderMaterial({ uniforms: { uTau: { value: 0 }, uP0: { value: new T.Vector2(P0.x, P0.z) }, uDir: { value: new T.Vector2(dir.x, dir.z) }, uV: { value: 4.2 }, uCw: { value: 7 }, uDt: { value: .5 }, uOp: { value: 0 }, uC: { value: new T.Vector2(Pc.x, Pc.z) } },
          vertexShader: 'varying vec3 vW; void main(){ vec4 w = modelMatrix * vec4(position, 1.); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }',
          fragmentShader: `uniform float uTau, uV, uCw, uDt, uOp; uniform vec2 uP0, uDir, uC; varying vec3 vW;
            void main(){ float n = floor(uTau / uDt); vec3 acc = vec3(0.);
              for (int k = 0; k < 14; k++) { float te = (n - float(k)) * uDt; if (te < 0.) break;
                float age = uTau - te; vec2 d = vW.xz - (uP0 + uDir * uV * te); float r = length(d), R = uCw * age, dd = abs(r - R), wd = .14 + .006 * R;
                float ring = exp(-dd * dd / (wd * wd)) + .25 * exp(-dd / (wd * 4.));
                float fade = (1. - smoothstep(.5, 1., age / (14. * uDt))) * smoothstep(0., .2, age), cs = dot(d, uDir) / max(r, 1e-3);
                vec3 col = cs > 0. ? mix(vec3(1., .95, .9), vec3(.4, .62, 1.), cs) : mix(vec3(1., .95, .9), vec3(1., .3, .16), -cs);
                acc += col * ring * fade; }
              gl_FragColor = vec4(acc * uOp * .75 * (1. - smoothstep(34., 50., length(vW.xz - uC))), 1.);
              #include <tonemapping_fragment>
              #include <colorspace_fragment>
            }`, transparent: true, depthWrite: false, blending: T.AdditiveBlending });
        const pl = new T.Mesh(new T.PlaneGeometry(100, 100).rotateX(-Math.PI / 2), m); pl.position.set(Pc.x, .12, Pc.z); pl.visible = false; S.add(pl);
        dop = { m, pl, P0, dir };
      }
      // ---- everywhere: galaxies the pulse rings start from ----
      const evI = []; { const want = [0, 1.05, 2.1, 3.15, 4.2, 5.25]; want.forEach(a0 => { let best = -1, bd = 1e9;
        for (let i = 3; i < N; i++) { const c = chi[i], r = Math.hypot(c[0], c[2]); if (r < 9 || r > 24) continue; const da = Math.abs(((Math.atan2(c[2], c[0]) - a0 + 9.42) % 6.283) - 3.14); if (da < bd) { bd = da; best = i; } }
        evI.push(best); }); }
      // ---- fabric: lattice, patch galaxies, new cubes ----
      const O = V3(0, 1.3, 0), GC = [V3(0, 1.6, 0).addScaledVector(Rv, 4.2).addScaledVector(Fv, -1.5), V3(0, 2.4, 0).addScaledVector(Rv, -3.6).addScaledVector(Fv, 2.4), V3(0, .9, 0).addScaledVector(Rv, 1.0).addScaledVector(Fv, 4.6)];
      const GCc = [[1, .84, .6], [.82, .74, 1], [.8, .9, 1]];
      GC.forEach((g, j) => GF.shape(XI + 9 + j, 2.3, j * 2.1, .55 + .15 * j, [0, 3, 2][j], 1.3));
      for (let j = 0; j < 3; j++) GF.shape(XI + 6 + j, 2.1, j * 1.7 + .4, .6, [1, 4, 0][j], 1.3);
      GF.shape(XI + 4, 2.6, .8, .6, 0, 1.2); GF.shape(XI + 5, 1.9, .3, .55, 2, 1.2);
      const gq = t => 1.5 * Math.pow(2, fract(Math.log2(Sof(t))));
      const NCu = 20, cubes = [];
      if (cCu < 1e8) { const RC = rng(97);
        for (let k = 0; k < NCu; k++) { const tc = cCu + .3 + k * .45, j = k < 6 ? 0 : k % 3, uu = k < 6 ? .18 + k * .13 : .2 + .65 * RC(), sp = gq(tc) / Sof(tc);
          const pt = GC[j].clone().multiplyScalar(uu); pt.x += (RC() - .5) * sp; pt.z += (RC() - .5) * sp;
          const cc = V3((Math.floor(pt.x / sp) + .5) * sp, (Math.floor(pt.y / sp) + .5) * sp, (Math.floor(pt.z / sp) + .5) * sp);
          const fill = new T.Mesh(new T.BoxGeometry(1, 1, 1), new T.MeshBasicMaterial({ color: '#ffc46a', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false }));
          fill.visible = false; S.add(fill); cubes.push({ tc, sp, cc, fill }); } }
      const EDG = [[0, 0, 0, 1, 0, 0], [0, 1, 0, 1, 1, 0], [0, 0, 1, 1, 0, 1], [0, 1, 1, 1, 1, 1], [0, 0, 0, 0, 1, 0], [1, 0, 0, 1, 1, 0], [0, 0, 1, 0, 1, 1], [1, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1], [1, 0, 0, 1, 0, 1], [0, 1, 0, 0, 1, 1], [1, 1, 0, 1, 1, 1]];
      LL.U.uBoxC.value.set(0, 4, 0); LL.U.uBoxH.value.set(13, 3.8, 13);

      // ---- per-frame state shared by pre() and draw() ----
      let W = {};
      return {
        pre(t) {
          const w1 = .2 * sm(cFz, cFz + 16.5, t) * (1 - sm(cSh + .4, cSh + 3.4, t)), wS = sm2(cSc, cSc + 3.5, cSc + 10, cSc + 13.5, t);
          const wBal = sm2(cBa, cBa + 1, cBa + 3.7, cBa + 5.2, t), wH2 = sm(cHo, cHo + 8, t) * (1 - sm(cOut, cOut + 4.45, t)), wF2 = sm(cFb, cFb + 3, t);
          const wF = wF2 * (1 - sm(cOut, cOut + 4.4, t)), wSp = sm2(cSp, cSp + .6, Math.min(cDp + .4, cSp + 11), Math.min(cDp + 1.7, cSp + 12.3), t);
          const wD = sm2(cDp, cDp + .8, cDp + 7.7, cDp + 9.2, t), S0 = Sof(t), Dfab = 21 * Math.pow(S0, .65);
          const env = sm2(cSk, cSk + .2, cSk + .3, cSk + 2.2, t), shk = [Math.sin(t * 14.45) * .14 * env, Math.cos(t * 19.5) * .09 * env];
          W = { w1, wS, wBal, wH2, wF2, wF, wSp, wD, S0 };
          return { D: Dm => { Dm *= (1 - w1) * (1 - .5 * wS); return Dm * (1 - wH2) + wH2 * (Dm * .8 * (1 - wF2) + Dfab * wF2); },
            dEl: -.33 * wS - .13 * wH2, dY: 4.6 * wS + 1.4 * wH2 * wF2, sh: shk,
            trail: sm(cFa - .4, cFa + 1.6, t) * (1 - sm(cBa - .2, cBa + .8, t)), trailI: 1.3,
            field: (1 - .93 * wBal) * (1 - .35 * wS) * (1 - .3 * wSp) * (1 - .25 * wD) * (1 - .78 * wF),
            cold: .85 * sm(cFz, cFz + 2.5, t) * (1 - sm(cSh + .3, cSh + 2.5, t)), us: (1 - .85 * wS) * (1 - .9 * wBal),
            grid: (1 - .9 * wBal) * (1 - .5 * wF) * (1 - .2 * wS) };
        },
        draw(t, K, A) {
          cR0.setFromMatrixColumn(cam.matrixWorld, 0); cU0.setFromMatrixColumn(cam.matrixWorld, 1); cF0.setFromMatrixColumn(cam.matrixWorld, 2).negate();
          const PRv = gridM.uniforms.uPr.value, PRa = [], PR = Array.from({ length: 8 }, () => ({ set(x, z, r, a) { PRa.push([x, z, r, a]); } }));
          // pane
          if (pane) { const U = pane.U, fro = (sm(cFz, cFz + 2.5, t) * .55 + .45 * sm(cFz + 7, cFz + 8.4, t)) * (cSh < 1e8 ? 1 : 1 - sm(cFz + 17, cFz + 19, t));
            const crack = Math.max(.11 * sm(cSh - 1.2, cSh - 1.0, t), 2.5 * eOut((t - cSh) / .45, 2));
            U.uFrost.value = fro; U.uTint.value = .1 * fro; U.uSheen.value = -.6 + 2.6 * sm(cFz + 7.2, cFz + 8.9, t); U.uCrack.value = crack;
            U.uGlint.value = .45 * sm2(cSh - 1.2, cSh - 1.05, cSh - 1.05, cSh, t) + sm2(cSh, cSh + .15, cSh + .15, cSh + 1.3, t); U.uSh.value = t - (cSh + .35);
            pane.mesh.visible = t < cSh + 2.6 && (fro > .002 || crack > 0); }
          if (vig) { vig.material.uniforms.uV.value = .55 * sm(cHo + 2.7, cHo + 4.6, t) * (1 - .45 * sm(cFb, cFb + 3, t)) * (1 - sm(cOut, cOut + 3.5, t)); vig.visible = vig.material.uniforms.uV.value > .002; }
          // traveller
          { const q = cl((t - cTv) / 6.3), r = 2.5 + 65.5 * Math.pow(q, 2.3), o = sm2(cTv - .3, cTv + .5, cTv + 7, cTv + 8.6, t);
            tv1.position.copy(dirT).multiplyScalar(r).setY(1.6); tv2.position.copy(tv1.position); tv1.material.opacity = .95 * o; tv2.material.opacity = .35 * o;
            if (o > .002) SK2.set(28, tv1.position.x, 1.6, tv1.position.z, dirT.x * 2.5, 1.6, dirT.z * 2.5, .8 * o, .66 * o, .45 * o, 3.2); else SK2.hide(28);
            const ea = .9 * sm2(cTv + 6.1, cTv + 6.4, cTv + 6.6, cTv + 8.2, t); if (ea > 0) PR[1].set(0, 0, 68 * A, ea); }
          // shook / burst ring (slot 0)
          if (t < cB - .5) { const a = .7 * sm2(cSk, cSk + .15, cSk + .3, cSk + 2.2, t); if (a > 0) PR[0].set(0, 0, 2 + 40 * eOut((t - cSk) / 2.2), a); }
          else { const a = 1.1 * sm2(cB - .05, cB + .15, cB + .5, cB + 3.8, t); if (a > 0) PR[0].set(0, 0, 3 + 100 * eOut((t - cB) / 3.8), a); }
          flash.material.opacity = .6 * sm(cB - .05, cB + .15, t) * (1 - sm(cB + .2, cB + 1.5, t));
          { const so = .34 * sm2(cB - .05, cB + .2, cB + .5, cB + 2.8, t); shell.visible = so > .002; if (shell.visible) { shell.material.uniforms.uOp.value = so; shell.scale.setScalar(2 + 44 * eOut((t - cB) / 2.8, 2.2)); } }
          // telescope
          if (tel) { const wL = sm2(cSc + 3.5, cSc + 4.5, cSc + 9.6, cSc + 10.6, t);
            tel.cutU.value = -.3 + 12 * (sm(cSc + .5, cSc + 3.3, t) - sm(cSc + 10, cSc + 12.8, t));
            tel.cutG.value = 1.3 * (sm2(cSc + .4, cSc + .7, cSc + 3.0, cSc + 3.6, t) + sm2(cSc + 9.9, cSc + 10.2, cSc + 12.5, cSc + 13, t));
            tel.grp.visible = tel.cutU.value > -.25;
            tel.glint.material.opacity = wL * (.3 + .12 * Math.sin(t * 2.3)) + .7 * sm2(cSc + 4.6, cSc + 4.75, cSc + 4.75, cSc + 6, t) * wL;
            tel.paths.forEach((P, j) => { const g = XI + j, s0 = P.pts[0];
              if (wL > .002) GF.set(g, s0.x, s0.y, s0.z, .95 * wL, .85 * wL, .7 * wL, 1.2); else gOff(g);
              const ap = P.pts[1], mi = P.pts[2], fo = P.pts[3];
              if (wL > .002) { LL.set(LSC + j, s0.x, s0.y, s0.z, ap.x, ap.y, ap.z, .16 * wL, .14 * wL, .1 * wL, 1.4); LL.set(LSC + 4 + j, mi.x, mi.y, mi.z, fo.x, fo.y, fo.z, .1 * wL, .1 * wL, .09 * wL, 1.1); }
              else { LL.hide(LSC + j); LL.hide(LSC + 4 + j); }
              for (let k = 0; k < 6; k++) { const id = j * 6 + k; if (wL <= .002) { SK2.hide(id); continue; }
                const s = fract((t - cSc) * .2 + k / 6 + j * .09), dd = s * P.Lt, o = wL * sm(0, .05, s) * (1 - sm(.93, 1, s));
                let sg = 0, d0 = dd; while (sg < 2 && d0 > P.L[sg]) { d0 -= P.L[sg]; sg++; }
                const a = P.pts[sg], b = P.pts[sg + 1], L = P.L[sg], h = tmp.copy(a).lerp(b, d0 / L), tl = tmp2.copy(a).lerp(b, Math.max(0, d0 - 1.6) / L);
                SK2.set(id, h.x, h.y, h.z, tl.x, tl.y, tl.z, 1.1 * o, .95 * o, .7 * o, 2.6); } }); }
          // spectrum
          if (spec) { const o = W.wSp, rev = sm(cSp + .5, cSp + 2.3, t);
            spec.band.visible = o > .002; spec.prism.visible = o > .002;
            if (o > .002) { const d = 26, h = d * Math.tan(cam.fov * Math.PI / 360), wb = .56 * 2 * h * asp, hb = wb * .2;
              scr(.555, .645, d, spec.band.position); spec.band.quaternion.copy(cam.quaternion).multiply(spec.qT); spec.band.scale.set(wb, hb, 1);
              const mu = spec.m.uniforms; mu.uOp.value = o; mu.uRev.value = rev * 1.04; mu.uZ.value = .085 * sm(cShf, cShf + 1.7, t); mu.uArr.value = sm(cShf - .2, cShf + .5, t);
              const pp = scr(.665, .38, d, spec.prism.position); spec.prism.quaternion.copy(cam.quaternion).multiply(spec.qP); spec.prism.scale.set(.75, 1.9, .75);
              spec.prism.material.opacity = .14 * o; spec.pe.material.opacity = .55 * o; spec.pgl.position.copy(pp); spec.pgl.material.opacity = .5 * o * sm(cSp + .3, cSp + .9, t);
              const src = scr(.9, .17, 70, tmp2), bh = cl((t - cSp) / .8), hx = src.x + (pp.x - src.x) * bh, hy = src.y + (pp.y - src.y) * bh, hz = src.z + (pp.z - src.z) * bh;
              GF.set(XI + 4, src.x, src.y, src.z, 1.1 * o, 1 * o, .85 * o, 1.3);
              LL.set(LSP, src.x, src.y, src.z, hx, hy, hz, .55 * o, .55 * o, .5 * o, 2.6);
              const bU = tmp.setFromMatrixColumn(spec.band.matrixWorld, 1);
              spec.band.updateMatrixWorld(); const bR = new T.Vector3().setFromMatrixColumn(spec.band.matrixWorld, 0).normalize(), bUp = bU.setFromMatrixColumn(spec.band.matrixWorld, 1).normalize();
              const SPC = [[.55, .25, 1], [.2, .4, 1], [0, .8, .9], [.3, 1, .2], [1, .9, .1], [1, .5, .05], [1, .12, .05]];
              for (let k = 0; k < 7; k++) { const uu = .06 + k * .147, vis = o * sm(uu - .05, uu + .02, rev) * .42;
                const e = spec.band.position.clone().addScaledVector(bR, (uu - .5) * wb).addScaledVector(bUp, hb * .44);
                if (vis > .002) LL.set(LSP + 1 + k, pp.x, pp.y, pp.z, e.x, e.y, e.z, SPC[k][0] * vis, SPC[k][1] * vis, SPC[k][2] * vis, 1.8); else LL.hide(LSP + 1 + k); } }
            else { gOff(XI + 4); for (let k = 0; k < 8; k++) LL.hide(LSP + k); spec.pgl.material.opacity = 0; } }
          else gOff(XI + 4);
          // Doppler
          if (dop) { const o = W.wD, tau = Math.max(0, t - (cDp + .6)); dop.pl.visible = o > .002; dop.m.uniforms.uOp.value = o; dop.m.uniforms.uTau.value = tau;
            const sp = dop.P0.clone().addScaledVector(dop.dir, 4.2 * tau);
            if (o > .002) { GF.set(XI + 5, sp.x, .9, sp.z, 1.05 * o, .95 * o, .85 * o, 1.3);
              const tl = sp.clone().addScaledVector(dop.dir, -4.2 * Math.min(.7, tau)); SK2.set(24, sp.x, .9, sp.z, tl.x, .9, tl.z, .5 * o, .5 * o, .55 * o, 3, .3 * o, .1 * o, .05 * o); }
            else { gOff(XI + 5); SK2.hide(24); } }
          else gOff(XI + 5);
          // everywhere rings (slots 2-7)
          for (let m = 0; m < 6; m++) { const ts = cEv - 1.5 + m * .25, a = .85 * sm2(ts, ts + .15, ts + .6, ts + 2.8, t), i = evI[m];
            if (a > 0 && i >= 0) PR[2 + m].set(chi[i][0] * A, chi[i][2] * A, .5 + 16 * Math.pow(cl((t - ts) / 2.8), .8), a); }
          // balloon
          { const o = sm2(cBa - .2, cBa + .6, cBa + 4.0, cBa + 5.4, t), Rb = 2.4 + 15 * sm(cBa - .3, cBa + 5, t); balloon.visible = o > .002;
            if (balloon.visible) { balloon.scale.setScalar(Rb); balloon.material.uniforms.uOp.value = .8 * o; }
            for (let k = 0; k < NB; k++) { const j = XI + 12 + k; if (o <= .002) { gOff(j); continue; }
              const d = bDir[k], px = d.x * Rb * 1.01, py = 1.5 + d.y * Rb * 1.01, pz = d.z * Rb * 1.01;
              v.set(cam.position.x - px, cam.position.y - py, cam.position.z - pz).normalize(); const face = d.dot(v) > 0 ? 1 : .28, c = bCol[k], b = o * face * .9;
              GF.set(j, px, py, pz, c[0] * b, c[1] * b, c[2] * b, 1); } }
          // bullets
          for (let k = 0; k < 3; k++) { const tb = cBu + .2 + k * .55, o = sm2(tb, tb + .25, cBu + 3.9, cBu + 4.7, t), j = XI + 6 + k;
            if (o <= .002) { gOff(j); SK2.hide(25 + k); continue; }
            const ps = tmp.set(0, 3 + k * 1.6, 0).addScaledVector(Rv, -34 + 22 * (t - tb)).addScaledVector(Fv, [-6, 3, -13][k]);
            GF.set(j, ps.x, ps.y, ps.z, 1.3 * o, 1.3 * o, 1.4 * o, 1.4);
            SK2.set(25 + k, ps.x, ps.y, ps.z, ps.x - Rv.x * 15, ps.y, ps.z - Rv.z * 15, .9 * o, 1 * o, 1.3 * o, 5, .1 * o, .15 * o, .35 * o); }
          // fabric
          { const wF = W.wF, S0 = W.S0;
            if (wF > .002) { const lev = Math.log2(S0), f = fract(lev), g = 1.5 * Math.pow(2, f), wn = Math.min(1.15, f * (1 + 2.5 * (1 - f) * (1 - f)));
              const pf = fract((t - cLv) / 2.4), pa = 1.6 * sm(cLv, cLv + 1, t) * Math.sin(Math.PI * pf);
              LL.U.uPC.value.copy(O); LL.U.uPR.value = 2 + 17 * pf; LL.U.uPA.value = pa;
              let id = 0; const put = (ax, ay, az, bx, by, bz, ev) => { const I = wF * (ev ? .36 : .36 * wn); if (I < .003) LL.hide(id); else LL.set(id, ax, ay, az, bx, by, bz, .3 * I, .4 * I, 1 * I, ev ? 1.7 : 1.3, 1); id++; };
              for (let a = -5; a <= 5; a++) for (let b = -9; b <= 9; b++) { const y = O.y + a * g, z = b * g, ev = !(a & 1) && !(b & 1); put(-13, y, z, 13, y, z, ev); put(z, y, -13, z, y, 13, ev); }
              for (let a = -9; a <= 9; a++) for (let b = -9; b <= 9; b++) put(a * g, 0, b * g, a * g, 8, b * g, !(a & 1) && !(b & 1));
              GC.forEach((gc, j) => { const c = GCc[j]; GF.set(XI + 9 + j, O.x + gc.x * S0, O.y + gc.y * S0, O.z + gc.z * S0, c[0] * 1.7 * wF, c[1] * 1.7 * wF, c[2] * 1.7 * wF, 1.5); }); }
            else { for (let i = 0; i < LAT; i++) LL.hide(i); for (let j = 0; j < 3; j++) gOff(XI + 9 + j); }
            for (let k = 0; k < NCu; k++) { const cb = cubes[k], base = LCU + k * 12; if (!cb) { for (let e = 0; e < 12; e++) LL.hide(base + e); continue; }
              const on = t > cb.tc && wF > .002; cb.fill.visible = on; if (!on) { for (let e = 0; e < 12; e++) LL.hide(base + e); continue; }
              const x = cl((t - cb.tc) / .5), pop = 1 + 2.70158 * Math.pow(x - 1, 3) + 1.70158 * Math.pow(x - 1, 2), I = wF * (.45 + 1.1 * sm2(cb.tc, cb.tc + .15, cb.tc + .15, cb.tc + 1.3, t));
              const sz = cb.sp * S0 * pop * .9, cx = O.x + cb.cc.x * S0, cy = O.y + cb.cc.y * S0, cz = O.z + cb.cc.z * S0, hs = sz / 2;
              cb.fill.position.set(cx, cy, cz); cb.fill.scale.setScalar(Math.max(1e-3, sz)); cb.fill.material.opacity = .12 * I;
              EDG.forEach((e, n) => LL.set(base + n, cx + (e[0] * 2 - 1) * hs, cy + (e[1] * 2 - 1) * hs, cz + (e[2] * 2 - 1) * hs, cx + (e[3] * 2 - 1) * hs, cy + (e[4] * 2 - 1) * hs, cz + (e[5] * 2 - 1) * hs, 1 * I, .72 * I, .35 * I, 2)); } }
          PRa.forEach((q, k) => PRv[k].set(q[0], q[1], q[2], q[3])); gridM.uniforms.uPrN.value = PRa.length;
          [tv1, tv2, flash, tel && tel.glint, spec && spec.pgl].forEach(s => { if (s) s.visible = s.material.opacity > .002; });
          LL.flush(); SK2.flush();
        } };
    }

    const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .1, 3000); ctx.side(cam, p.side == null ? .12 : p.side);
    const RH = 30, KAP = .14, tgt = new T.Vector3(), v = new T.Vector3(), w = new T.Vector3(), e1 = new T.Vector3(), mb = new T.Matrix4();
    const BX = X ? buildBeats() : null;
    return { scene: S, camera: cam, draw(t, u) {
      ctx.t = t;
      const A0 = aOf(t), rs = on(cR, 2), st = on(cS, 3), lw = on(cL, 3), fs = on(cF, 3), tm = on(cM, 3);
      const E = X ? Eof(t) : 0, A = A0 * Math.exp(E), K = BX ? BX.pre(t) : null;
      // camera: slow orbit, pulls back as space grows (galaxies themselves keep their size); moves in on the photon at treadmill
      let D = 46 * Math.pow(A0, .7) * (1 - .32 * tm), el = .43 - .06 * tm;
      const az = az0 + u * .003 + .08 * Math.sin(u * .02);
      tm > 0 ? tgt.copy(phDir).multiplyScalar(11 * tm).setY(1.5) : tgt.set(0, 1.5, 0);
      if (K) { D = K.D(D * Math.exp(.55 * E)); el += K.dEl; tgt.y += K.dY; tgt.x += K.sh[0]; tgt.y += K.sh[1]; }
      cam.position.set(tgt.x + Math.sin(az) * Math.cos(el) * D, tgt.y + Math.sin(el) * D, tgt.z + Math.cos(az) * Math.cos(el) * D); cam.lookAt(tgt);
      cam.updateMatrixWorld();
      gridM.uniforms.uA.value = A; gridM.uniforms.uCam.value.copy(cam.position); gridM.uniforms.uRingA.value = fs * (1 - .4 * tm);
      // galaxies
      const Lc = KAP * RH; trM.uniforms.uLc.value = Lc + (1 - fs) * 400;
      const trailK = Math.max(lw * (1 - .7 * tm), K ? K.trail : 0), fk = K ? K.field : 1, cold = K ? K.cold : 0;
      for (let i = 0; i < N; i++) { const c = chi[i], x = c[0] * A, z = c[2] * A, y = c[1], rr = Math.hypot(x, z);
        const dc = Math.hypot(x - cam.position.x, y - cam.position.y, z - cam.position.z);
        let f = Math.exp(-Math.max(0, dc - D * 1.1) / (D * 1.3)) * sm(3, 9, dc) * (1 - .35 * tm);
        const red = fs * sm(RH * .96, RH * 1.12, rr), b = base[i];
        f *= 1 + .25 * red;
        if (K) { f *= fk; const r0 = b[0] * (1 - red) + red, g0 = b[1] * (1 - red) + red * .3, b0 = b[2] * (1 - red) + red * .2, l = (r0 + g0 + b0) / 3 * .85;
          GF.set(i, x, y, z, (r0 + (l * .7 - r0) * cold) * f, (g0 + (l * .86 - g0) * cold) * f, (b0 + (l * 1.3 - b0) * cold) * f, 1); }
        else GF.set(i, x, y, z, (b[0] * (1 - red) + red * 1.0) * f, (b[1] * (1 - red) + red * .3) * f, (b[2] * (1 - red) + red * .2) * f, 1);
        // trail
        const L = KAP * rr * trailK, o = i * 12, oa = i * 16;
        if (L < .02 || f < .01) { trA.fill(0, oa, oa + 16); continue; }
        const dx = x / rr, dz = z / rr; v.set(x - cam.position.x, y - cam.position.y, z - cam.position.z); e1.set(dx, 0, dz); w.crossVectors(e1, v).normalize();
        const hw = .22, tw = .11, tx = x - dx * L, tz = z - dz * L;
        trP.set([x + w.x * hw, y + w.y * hw, z + w.z * hw, x - w.x * hw, y - w.y * hw, z - w.z * hw, tx + w.x * tw, y + w.y * tw, tz + w.z * tw, tx - w.x * tw, y - w.y * tw, tz - w.z * tw], o);
        const I0 = Math.min(1, f * 1.3) * .34 * (K ? K.trailI : 1);
        trA.set([0, 1, L, I0, 0, -1, L, I0, L, 1, L, I0, L, -1, L, I0], oa); }
      if (K) { const k = K.us; GF.set(N, 0, 1.3, 0, 1.15 * k, .92 * k, .62 * k, 1.4); us1.material.opacity = .32 * k; us2.material.opacity = .85 * k; }
      else GF.set(N, 0, 1.3, 0, 1.15, .92, .62, 1.4);
      // speed stream: crawls inside the light-speed ring, races (red, streaked) beyond it, recycled near us
      const Tb = .4, Ft = Fof(t), Fb = Fof(t - Tb), rt0 = rateF(t), cp = cam.position;
      for (let k = 0; k < NQ; k++) { const d = QD[k], j = N + 1 + k, LAM = d[9];
        if (fs <= 0) { GF.set(j, 0, 0, 0, 0, 0, 0, 0); SK.hide(k); continue; }
        const s = fr(Ft * d[4] + d[5]), st = Math.max(0, s - (Ft - Fb) * d[4]), r = d[3] * Math.exp(LAM * s), rq = d[3] * Math.exp(LAM * st);
        const x = d[0] * r, z = d[2] * r, y = d[1], dc = Math.hypot(x - cp.x, y - cp.y, z - cp.z);
        const f = fs * sm(0, .08, s) * (1 - sm(.85, 1, s)) * Math.exp(-Math.max(0, dc - D * 1.1) / (D * 1.3)) * sm(3, 9, dc) * (1 - .45 * tm);
        const red = sm(RH * .96, RH * 1.12, r), redT = sm(RH * .96, RH * 1.12, rq), fr2 = f * (1 + .25 * red);
        const cr = (d[6] * (1 - red) + red) * fr2, cg = (d[7] * (1 - red) + red * .3) * fr2, cb = (d[8] * (1 - red) + red * .2) * fr2;
        GF.set(j, x, y, z, cr, cg, cb, 1);
        const sk = .55 * f * sm(2, 10, LAM * r * rt0 * d[4]) * (.45 + .55 * red);
        if (sk < .002) { SK.hide(k); continue; }
        SK.set(k, x, y, z, d[0] * rq, y, d[2] * rq, sk, sk * (.78 - .52 * red), sk * (.42 - .28 * red), 2.6,
          sk * .7, sk * .7 * (.78 - .52 * redT), sk * .7 * (.42 - .28 * redT)); }
      if (BX) { BX.draw(t, K, A); dust.material.opacity = .8 * fk; gridM.uniforms.uDim.value = K.grid; }
      GF.flush(); SK.flush();
      trG.attributes.position.needsUpdate = true; trG.attributes.aT.needsUpdate = true;
      for (let i = 0; i < ND; i++) { const c = dChi[i]; dA[i * 3] = c[0] * A; dA[i * 3 + 1] = c[1]; dA[i * 3 + 2] = c[2] * A; }
      dust.geometry.attributes.position.needsUpdate = true;
      // ribbons: reveal from the source toward us (staggered), then fade once the grid starts to stretch (or at ribOff)
      const ribOp = rs * (1 - sm(cS + 2, cS + 10, t)) * (1 - sm(cRo, cRo + 1.5, t));
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
