// MIYA.kit — realism helpers for scene modules (2026-10-14, after "the clock scene looks like a 2D picture; upgrade how objects,
// things, animals and plants are made"). Load after three.js and before the scene files.
//  noise(size, opt)            fBm value-noise canvas (grey), seedable
//  normalMap(canvas, strength) tangent-space normal map texture from a height canvas (Sobel)
//  tex(canvas, srgb)           CanvasTexture with wrapping
//  body(opt)                   organic body swept along a spine (fish, whale, worm, stem, trunk...): width/height profiles, flat belly,
//                              UV u = along the body, v = around; returns {geo, deform(fn)} where fn(s, theta, base) -> [dx,dy,dz]
//  fin(outline, thick)         a fin/leaf/flipper/petal: extruded outline with rounded edge
//  shafts(scene, opt)          underwater / forest god rays (additive gradient planes), returns update(t)
//  snow(scene, opt)            drifting particles (marine snow, dust, pollen), returns update(t)
//  surfaceFromBelow(scene,opt) bright rippling water surface seen from below, returns update(t)
//  grass(scene, opt)           soft, lush grass (never hard spiky blades; user 2026-10-15). Returns {group, clumps, band, lawn,
//                              update(t, camera)} — call update every frame (wind from t only: seek-safe; sun glow needs the camera).
//                              Three layers, use any mix:
//                              * tufts (opt.n > 0): instanced crossed alpha cards, each textured with hundreds of fine curved strands
//                                (strandTex), alphaTest + alphaToCoverage, mip-aware alpha so far tufts stay full, darker roots
//                                n, area:[x0,z0,x1,z1], ground(x,z)->y, mask(x,z)->0..1 (keep probability), scale(x,z)->size factor,
//                                size:[width,height] m, cards (2), base (.35, root width) / splay (.3, top 1+splay wide),
//                                sink (.04), seed, tint, dryTint,
//                                dryFrac, strands:{n,width,hMin,hMax,root,tip,dry,dryFrac,spread} (texture), tex (share one),
//                                thin:[near,far,keepFar] distance thinning from the camera (default [14,45,.3]), receiveShadow
//                                Cost (software GL): fragment overdraw. At a grazing view a pixel ray crosses many tufts, so
//                                density x card area x cards is what you pay; ~1500 three-card tufts on an island cost ~1.4 s.
//                              * band (opt.band): far background line of grass — low soft ribbons with a tileable strand texture along
//                                a path instead of single blades: {path:[[x,z],...], closed, height, rows (2), rowGap, tile (m per
//                                texture repeat), wind, color, strands}
//                              * lawn (opt.lawn): fur / shell texturing for short lawn near the camera: {geo (ground patch with uv),
//                                layers (8), height (.07 m), repeat, dots, color, map, far (fades out by this view distance)}.
//                                Cost: each layer redraws the patch (measured: 8 layers over a 9 m island seen from 15-25 m
//                                ~ +0.4 s/frame, 4 layers ~ +0.2 s); the ground geometry must face up (CCW seen from above).
//                              common: wind (.12 = sway per metre of height), windDir [x,z], windFreq, sun [x,y,z] world direction to
//                              the sun (light glows through blades when looking toward it), trans (colour), transK, color,
//                              alphaTest (.3), clip (clipping planes, for mirrored copies), parent (add to this group instead).
//  strandTex(opt)              the strand texture alone (DataTexture): w, h, n, width, hMin, hMax, root, tip, dry, dryFrac, tile, seed
(function () {
  const T = THREE, M = (window.MIYA = window.MIYA || { scenes: {} });
  function rng(seed) { let s = (seed | 0) % 2147483647; if (s <= 0) s += 2147483646; return () => (s = (s * 16807) % 2147483647) / 2147483647; }
  function noise(size, o) {
    o = o || {}; const oct = o.octaves || 5, seed = o.seed || 1, sx = o.sx || 1, sy = o.sy || 1, r = rng(seed);
    const G = 64, grid = new Float32Array(G * G).map(() => r());
    const val = (x, y) => { x = ((x % G) + G) % G; y = ((y % G) + G) % G; const x0 = Math.floor(x), y0 = Math.floor(y), fx = x - x0, fy = y - y0, x1 = (x0 + 1) % G, y1 = (y0 + 1) % G;
      const ux = fx * fx * (3 - 2 * fx), uy = fy * fy * (3 - 2 * fy); const a = grid[y0 * G + x0], b = grid[y0 * G + x1], c = grid[y1 * G + x0], d = grid[y1 * G + x1];
      return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy; };
    const c = document.createElement('canvas'); c.width = c.height = size; const g = c.getContext('2d'), im = g.createImageData(size, size);
    for (let y = 0; y < size; y++) for (let x = 0; x < size; x++) { let v = 0, a = .5, f = 4 / size; for (let k = 0; k < oct; k++) { v += a * val(x * f * G / 4 * sx, y * f * G / 4 * sy); a *= .5; f *= 2; }
      const q = Math.max(0, Math.min(255, v * 255)) | 0, i = (y * size + x) * 4; im.data[i] = im.data[i + 1] = im.data[i + 2] = q; im.data[i + 3] = 255; }
    g.putImageData(im, 0, 0); return c;
  }
  function tex(c, srgb, rep) { const t = new T.CanvasTexture(c); t.wrapS = t.wrapT = T.RepeatWrapping; if (rep) t.repeat.set(rep[0], rep[1]); t.colorSpace = srgb ? T.SRGBColorSpace : T.NoColorSpace; t.anisotropy = 4; return t; }
  function normalMap(c, strength) {
    const w = c.width, h = c.height, src = c.getContext('2d').getImageData(0, 0, w, h).data, o = document.createElement('canvas'); o.width = w; o.height = h;
    const g = o.getContext('2d'), im = g.createImageData(w, h), s = strength || 2, H = (x, y) => src[(((y + h) % h) * w + ((x + w) % w)) * 4] / 255;
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) { const dx = (H(x + 1, y) - H(x - 1, y)) * s, dy = (H(x, y + 1) - H(x, y - 1)) * s, l = Math.hypot(dx, dy, 1), i = (y * w + x) * 4;
      im.data[i] = (-dx / l * .5 + .5) * 255; im.data[i + 1] = (dy / l * .5 + .5) * 255; im.data[i + 2] = (1 / l * .5 + .5) * 255; im.data[i + 3] = 255; }
    g.putImageData(im, 0, 0); return tex(o, false);
  }
  // body: spine along +x from tail (s=0, x=-L/2) to head (s=1, x=+L/2). ONE mesh for the whole animal (user rule 2026-10-14):
  //   flukes/tail fins come from the width/height profiles plus a sweep in deform(); small fins/flippers that are not tubes can be
  //   passed as `extra` geometries (already placed in body space) — they are merged into the same mesh and take the same deform at
  //   their s, so nothing can come apart. u(s) maps s to the texture u (default s). Limbs with joints: see cine_spec 3A (skinning).
  function body(o) {
    const L = o.length || 10, N = o.seg || 120, Mr = o.ring || 48, wf = o.width, hf = o.height, belly = o.belly == null ? .25 : o.belly, ridge = o.ridge || 0, uf = o.u || (s => s);
    const ex = (o.extra || []).map(g => g.index ? g.toNonIndexed() : g), nE = ex.reduce((a, g) => a + g.attributes.position.count, 0), nB = (N + 1) * Mr, nV = nB + nE;
    const pos = new Float32Array(nV * 3), uv = new Float32Array(nV * 2), S = new Float32Array(nV), TH = new Float32Array(nV), idx = [];
    for (let i = 0; i <= N; i++) { const s = i / N, x = (s - .5) * L, w = wf(s), hh = hf(s);
      for (let j = 0; j < Mr; j++) { const th = j / Mr * Math.PI * 2, c = Math.cos(th), sn = Math.sin(th);
        let y = sn * hh; if (sn < 0) y *= 1 - belly; y += ridge * Math.max(0, sn) ** 8 * hh;
        const k = i * Mr + j; pos.set([x, y, c * w], k * 3); uv.set([uf(s), j / Mr], k * 2); S[k] = s; TH[k] = th; } }
    for (let i = 0; i < N; i++) for (let j = 0; j < Mr; j++) { const a = i * Mr + j, b = i * Mr + (j + 1) % Mr, c = (i + 1) * Mr + j, d = (i + 1) * Mr + (j + 1) % Mr; idx.push(a, c, b, b, c, d); }
    let k = nB; ex.forEach(g => { const pa = g.attributes.position.array, v = g.userData.v == null ? .75 : g.userData.v;
      for (let q = 0; q < pa.length / 3; q++, k++) { const x = pa[q * 3], s = x / L + .5; pos.set([x, pa[q * 3 + 1], pa[q * 3 + 2]], k * 3); uv.set([uf(Math.min(1, Math.max(0, s))), v], k * 2); S[k] = s; TH[k] = -1; idx.push(k); } });
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(pos, 3)); g.setAttribute('uv', new T.BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals();
    const base = pos.slice();
    return { geo: g, S, TH, base, deform(fn) { const p = g.attributes.position.array; for (let k = 0; k < S.length; k++) { const d = fn(S[k], TH[k], base, k); p[k * 3] = base[k * 3] + d[0]; p[k * 3 + 1] = base[k * 3 + 1] + d[1]; p[k * 3 + 2] = base[k * 3 + 2] + d[2]; }
      g.attributes.position.needsUpdate = true; g.computeVertexNormals(); } };
  }
  function fin(outline, thick) {
    const sh = new T.Shape(); outline.forEach((p, i) => i ? sh.lineTo(p[0], p[1]) : sh.moveTo(p[0], p[1]));
    const g = new T.ExtrudeGeometry(sh, { depth: thick * .2, bevelEnabled: true, bevelThickness: thick * .4, bevelSize: thick * .5, bevelSegments: 4, curveSegments: 24 }); g.center(); g.computeVertexNormals(); return g;
  }
  let _shaft = null;
  function shafts(scene, o) {
    o = o || {}; const n = o.n || 9, r = rng(o.seed || 3), col = new T.Color(o.color || '#9fd4ff'), grp = new T.Group(); scene.add(grp);
    _shaft = _shaft || (() => { const c = document.createElement('canvas'); c.width = 64; c.height = 512; const g = c.getContext('2d'); const gr = g.createLinearGradient(0, 0, 0, 512); gr.addColorStop(0, 'rgba(255,255,255,.9)'); gr.addColorStop(.6, 'rgba(255,255,255,.18)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, 64, 512);
      const gx = g.createLinearGradient(0, 0, 64, 0); gx.addColorStop(0, 'rgba(0,0,0,1)'); gx.addColorStop(.5, 'rgba(0,0,0,0)'); gx.addColorStop(1, 'rgba(0,0,0,1)'); g.globalCompositeOperation = 'destination-out'; g.fillStyle = gx; g.fillRect(0, 0, 64, 512); return tex(c, true); })();
    const items = []; for (let i = 0; i < n; i++) { const w = (o.width || 6) * (.5 + r()), h = o.height || 120;
      const m = new T.Mesh(new T.PlaneGeometry(w, h), new T.MeshBasicMaterial({ map: _shaft, color: col, transparent: true, opacity: (o.opacity || .12) * (.5 + r()), blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide, fog: false }));
      m.position.set((r() - .5) * (o.spread || 120), (o.top || 50) - h / 2, (r() - .5) * (o.depth || 80)); m.rotation.set(0, r() * Math.PI, (r() - .5) * .25 + (o.tilt || .18)); m.userData = { ph: r() * 6.28, op: m.material.opacity }; grp.add(m); items.push(m); }
    return { group: grp, update(t, fade) { const f = fade == null ? 1 : fade; items.forEach(m => { m.material.opacity = m.userData.op * f * (.75 + .25 * Math.sin(t * .4 + m.userData.ph)); m.rotation.y += 0; m.position.x += 0; }); } };
  }
  function snow(scene, o) {
    o = o || {}; const n = o.n || 4000, r = rng(o.seed || 5), bx = o.box || [120, 80, 80], g = new T.BufferGeometry(), p = new Float32Array(n * 3), b = new Float32Array(n * 4);
    for (let i = 0; i < n; i++) b.set([(r() - .5) * bx[0], (r() - .5) * bx[1], (r() - .5) * bx[2], r()], i * 4);
    g.setAttribute('position', new T.BufferAttribute(p, 3));
    const dot = (() => { const c = document.createElement('canvas'); c.width = c.height = 32; const x = c.getContext('2d'), gr = x.createRadialGradient(16, 16, 0, 16, 16, 16); gr.addColorStop(0, 'rgba(255,255,255,1)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); x.fillStyle = gr; x.fillRect(0, 0, 32, 32); return tex(c, true); })();
    const pts = new T.Points(g, new T.PointsMaterial({ size: o.size || .25, map: dot, color: o.color || '#cfe8ff', transparent: true, opacity: o.opacity || .55, depthWrite: false, blending: T.AdditiveBlending })); scene.add(pts);
    const c = o.center || [0, 0, 0];
    // world-fixed particles wrapped inside a box that follows `center` (the camera or subject), so they never run out
    const wrap = (v, sz) => ((v % sz) + sz * 1.5) % sz - sz / 2;
    return { points: pts, update(t, center) { const cc = center || c, fall = o.fall == null ? .6 : o.fall;
      for (let i = 0; i < n; i++) { const k = i * 4;
        p[i * 3] = cc[0] + wrap(b[k] + Math.sin(t * .3 + i) * .6 - cc[0], bx[0]);
        p[i * 3 + 1] = cc[1] + wrap(b[k + 1] - t * fall * (.5 + b[k + 3]) - cc[1], bx[1]);
        p[i * 3 + 2] = cc[2] + wrap(b[k + 2] - cc[2], bx[2]); }
      g.attributes.position.needsUpdate = true; } };
  }
  function surfaceFromBelow(scene, o) {
    o = o || {}; const nz = noise(512, { seed: o.seed || 9, octaves: 4, sx: 2, sy: 2 }); const t1 = tex(nz, true, [6, 6]);
    const m = new T.Mesh(new T.PlaneGeometry(o.size || 600, o.size || 600), new T.MeshBasicMaterial({ map: t1, color: o.color || '#bfe6ff', transparent: true, opacity: o.opacity || .5, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide, fog: false }));
    m.rotation.x = Math.PI / 2; m.position.y = o.y || 60; scene.add(m);
    return { mesh: m, update(t, fade) { t1.offset.set(t * .006, t * .004); m.material.opacity = (o.opacity || .5) * (fade == null ? 1 : fade); } };
  }
  // ---------- soft grass (2026-10-15, user: "the grass is too spiky; use fur or a background line, so it looks natural and lush") ----------
  // strandTex: hundreds of fine curved strands with tapering soft tips and a root-to-tip colour gradient. RGB comes from an opaque
  // colour canvas (so mip levels keep the grass colour and never fringe dark), alpha from a second canvas. Row 0 = roots (v = 0).
  function strandTex(o) {
    const W = o.w || 512, H = o.h || 512, r = rng(o.seed || 1), tile = !!o.tile, cc = document.createElement('canvas'), ac = document.createElement('canvas');
    cc.width = ac.width = W; cc.height = ac.height = H; const cg = cc.getContext('2d'), ag = ac.getContext('2d');
    const root = new T.Color(o.root || '#1f2a12'), tip = new T.Color(o.tip || '#9aa860'), dry = new T.Color(o.dry || '#b8a868'), tmp = new T.Color(), tmp2 = new T.Color();
    const bg = cg.createLinearGradient(0, H, 0, 0); bg.addColorStop(0, root.getStyle()); bg.addColorStop(1, tmp.copy(root).lerp(tip, .7).getStyle()); cg.fillStyle = bg; cg.fillRect(0, 0, W, H);
    const n = o.n || 420, hMin = o.hMin == null ? .35 : o.hMin, hMax = o.hMax || .98, wid = o.width || 3.2;
    for (let i = 0; i < n; i++) {
      const g = tile ? r() - .5 : ((r() + r() + r()) / 3 - .5) * (o.spread || 1.5), x0 = W / 2 + g * W, f = i / n;   // tufts: roots bunched in the middle
      let len = H * (hMin + (hMax - hMin) * Math.pow(r(), .8)); if (!tile) len *= 1 - .45 * Math.min(1, Math.abs(g) * 2);
      const lean = (tile ? 0 : g * 2 * len * .42) + (r() - .5) * len * .45, bend = (r() - .5) * len * .25, w0 = wid * (.55 + .9 * r()), a0 = .78 + .22 * r();
      const shade = .55 + .6 * f + (r() - .5) * .25;   // strands drawn later sit in front: lighter
      const cr = tmp.copy(root).multiplyScalar(.8 + .4 * r()), ct = tmp2.copy(tip).lerp(dry, r() < (o.dryFrac || .18) ? .4 + .6 * r() : 0).multiplyScalar(shade);
      const strand = (dx) => { const P = [], Q = [], K = 14;
        for (let k = 0; k <= K; k++) { const t = k / K, a = (1 - t) * (1 - t), b = 2 * (1 - t) * t, c = t * t;
          const x = a * x0 + b * (x0 + lean * .15 + bend) + c * (x0 + lean) + dx, y = a * H + b * (H - len * .55) + c * (H - len);
          const tx = 2 * (1 - t) * (lean * .15 + bend) + 2 * t * (lean * .85 - bend), ty = -2 * (1 - t) * len * .55 - 2 * t * len * .45, tl = Math.hypot(tx, ty) || 1;
          const hw = Math.max(.35, w0 * .5 * Math.pow(1 - t, .65)); P.push([x - ty / tl * hw, y + tx / tl * hw]); Q.unshift([x + ty / tl * hw, y - tx / tl * hw]); }
        const pts = P.concat(Q), path = gx => { gx.beginPath(); pts.forEach((p, j) => j ? gx.lineTo(p[0], p[1]) : gx.moveTo(p[0], p[1])); gx.closePath(); gx.fill(); };
        const gc = cg.createLinearGradient(0, H, 0, H - len); gc.addColorStop(0, cr.getStyle()); gc.addColorStop(1, ct.getStyle()); cg.fillStyle = gc; path(cg);
        const ga = ag.createLinearGradient(0, H, 0, H - len); ga.addColorStop(0, `rgba(255,255,255,${a0})`); ga.addColorStop(.62, `rgba(255,255,255,${a0})`); ga.addColorStop(1, 'rgba(255,255,255,0)'); ag.fillStyle = ga; path(ag); };
      strand(0); if (tile) { strand(-W); strand(W); }
    }
    const cd = cg.getImageData(0, 0, W, H).data, ad = ag.getImageData(0, 0, W, H).data, out = new Uint8Array(W * H * 4);
    for (let y = 0; y < H; y++) { const sy = H - 1 - y; for (let x = 0; x < W; x++) { const s = (sy * W + x) * 4, d = (y * W + x) * 4; out[d] = cd[s]; out[d + 1] = cd[s + 1]; out[d + 2] = cd[s + 2]; out[d + 3] = ad[s + 3]; } }
    const t = new T.DataTexture(out, W, H); t.colorSpace = T.SRGBColorSpace; t.generateMipmaps = true; t.minFilter = T.LinearMipmapLinearFilter; t.magFilter = T.LinearFilter;
    t.wrapS = tile ? T.RepeatWrapping : T.ClampToEdgeWrapping; t.wrapT = T.ClampToEdgeWrapping; t.anisotropy = o.aniso || 16; t.needsUpdate = true; return t;
  }
  // shared material: Lambert + alphaTest + alpha-to-coverage, wind sway from t (seek-safe), distance thinning (instanced clumps),
  // up-facing normals on both sides (soft even shading, no dark card backs), light shining through when looking toward the sun
  function grassMaterial(tx, U, kind, o) {
    const m = new T.MeshLambertMaterial({ map: tx, color: o.color || '#ffffff', alphaTest: o.alphaTest || .3, alphaToCoverage: true, side: T.DoubleSide });
    if (o.clip) m.clippingPlanes = o.clip;
    m.onBeforeCompile = sh => { Object.assign(sh.uniforms, U);
      sh.vertexShader = sh.vertexShader.replace('#include <common>', `#include <common>
        uniform float gT; uniform vec4 gWind; uniform vec3 gThin; attribute float gh; varying float vGH;${kind === 0 ? ' attribute float aRnd;' : ' attribute float gm;'}`)
        .replace('#include <begin_vertex>', `#include <begin_vertex>
        vGH = gh;
        {
          #ifdef USE_INSTANCING
          mat4 IM = instanceMatrix;
          #else
          mat4 IM = mat4(1.);
          #endif
          vec3 wp = (IM * vec4(transformed, 1.)).xyz, ip = ${kind === 0 ? 'IM[3].xyz' : 'vec3(wp.x, wp.y - gm, wp.z)'};
          float hy = ${kind === 0 ? 'gh * length(IM[1].xyz)' : 'gm'}, k = 1.;
          vec3 wo = (modelMatrix * vec4(ip, 1.)).xyz;
          ${kind === 0 ? 'float dc = distance(wo.xz, cameraPosition.xz); float keep = mix(1., gThin.z, smoothstep(gThin.x, gThin.y, dc)); k = clamp((keep - aRnd) / .08, 0., 1.);' : ''}
          float ph = dot(wo.xz, gWind.zw) * gWind.y;
          float s = sin(gT * 1.6 - ph) * .5 + sin(gT * 2.9 - ph * 1.9 + wo.x * .37 + wo.z * .23) * .22 + .4;
          vec2 dsp = gWind.zw * (s * gWind.x * hy * gh);
          wp.xz += dsp; wp.y -= dot(dsp, dsp) * .5 / max(hy, .05);
          wp = ip + (wp - ip) * k;
          transformed = (inverse(IM) * vec4(wp, 1.)).xyz;
        }`);
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', `#include <common>
        uniform vec3 gSunV, gTrans; uniform vec2 gTexSz; varying float vGH;`)
        .replace('#include <map_fragment>', `#include <map_fragment>
        { vec2 tc = vMapUv * gTexSz; float lod = max(0., .5 * log2(max(dot(dFdx(tc), dFdx(tc)), dot(dFdy(tc), dFdy(tc)))));
          diffuseColor.a = min(1., diffuseColor.a * (1. + .32 * lod)); }
        diffuseColor.rgb *= mix(.42, 1., smoothstep(0., .6, vGH));`)
        .replace('#include <normal_fragment_begin>', `#include <normal_fragment_begin>
        #ifdef DOUBLE_SIDED
        normal *= faceDirection;
        #endif`)
        .replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
        { float bl = pow(max(dot(normalize(-vViewPosition), gSunV), 0.), 5.);
          totalEmissiveRadiance += gTrans * diffuseColor.rgb * bl * (.2 + .8 * vGH); }`);
    };
    m.customProgramCacheKey = () => 'kit-grass-' + kind + (o.clip ? '-c' : '');
    return m;
  }
  function grassUniforms(o, tx) {
    const wd = o.windDir || [1, .35], wl = Math.hypot(wd[0], wd[1]) || 1;
    return { gT: { value: 0 }, gWind: { value: new T.Vector4(o.wind == null ? .12 : o.wind, o.windFreq || .35, wd[0] / wl, wd[1] / wl) },
      gThin: { value: new T.Vector3(...(o.thin || [14, 45, .3])) }, gSunV: { value: new T.Vector3(0, 0, -1) },
      gTrans: { value: new T.Color(o.trans || '#ffb070').multiplyScalar(o.transK == null ? 1.2 : o.transK) }, gTexSz: { value: new T.Vector2(tx.image.width, tx.image.height) } };
  }
  // a tuft: `cards` unit-high cards (root at y = 0) crossing at the centre, narrow at the root (`base` wide) and fanning out to
  // 1 + splay at the top (V shape: fewer empty texels to shade); normals mostly up + outward
  function tuftGeo(cards, splay, base) {
    const P = [], N = [], UV = [], G = [], I = [], V = 4;
    for (let c = 0; c < cards; c++) { const a = c / cards * Math.PI + .4, ca = Math.cos(a), sa = Math.sin(a), b = P.length / 3;
      for (let j = 0; j <= V; j++) for (let i = 0; i <= 1; i++) { const y = j / V, x = (i - .5) * (base + (1 + splay - base) * Math.pow(y, .7));
        P.push(x * ca, y, x * sa); const nx = -sa * .3 + x * ca * .5, nz = ca * .3 + x * sa * .5, l = Math.hypot(nx, 1, nz); N.push(nx / l, 1 / l, nz / l); UV.push(i, y); G.push(y); }
      for (let j = 0; j < V; j++) { const q = b + j * 2; I.push(q, q + 1, q + 2, q + 1, q + 3, q + 2); } }
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(P, 3)); g.setAttribute('normal', new T.Float32BufferAttribute(N, 3));
    g.setAttribute('uv', new T.Float32BufferAttribute(UV, 2)); g.setAttribute('gh', new T.Float32BufferAttribute(G, 1)); g.setIndex(I); return g;
  }
  // grass(scene, opt) -> { group, clumps, band, lawn, update(t, camera) }   soft, lush grass (see the header list for the options)
  function grass(scene, o) {
    o = o || {}; const grp = new T.Group(); (o.parent || scene).add(grp); const r = rng(o.seed || 7), out = { group: grp, mats: [] };
    const sun = o.sun ? new T.Vector3(...(o.sun.isVector3 ? o.sun.toArray() : o.sun)).normalize() : null, ground = o.ground || (() => 0);
    const tint = new T.Color(o.tint || '#ffffff'), dryC = new T.Color(o.dryTint || '#d8c890'), tc = new T.Color();
    if (o.n) {   // instanced crossed-card tufts
      const tx = o.tex || strandTex(Object.assign({ seed: (o.seed || 7) + 1 }, o.strands || {})), U = grassUniforms(o, tx), mat = grassMaterial(tx, U, 0, o);
      const geo = tuftGeo(o.cards || 2, o.splay == null ? .3 : o.splay, o.base == null ? .35 : o.base), mesh = new T.InstancedMesh(geo, mat, o.n), M4 = new T.Matrix4(), Q = new T.Quaternion(), E = new T.Euler();
      const rnd = new Float32Array(o.n), A = o.area || [-10, -10, 10, 10], sz = o.size || [.6, .45], mask = o.mask || (() => 1), scl = o.scale || (() => 1);
      let k = 0;
      for (let tries = 0; k < o.n && tries < o.n * 40; tries++) { const x = A[0] + r() * (A[2] - A[0]), z = A[1] + r() * (A[3] - A[1]); if (r() > mask(x, z)) continue;
        const s = scl(x, z), h = sz[1] * s * (.65 + .7 * r()), w = sz[0] * Math.sqrt(s) * (.7 + .6 * r());
        M4.compose(new T.Vector3(x, ground(x, z) - (o.sink == null ? .04 : o.sink), z), Q.setFromEuler(E.set((r() - .5) * .25, r() * 6.283, (r() - .5) * .25)), new T.Vector3(w, h, w)); mesh.setMatrixAt(k, M4);
        tc.copy(tint).multiplyScalar(.82 + .3 * r()); if (r() < (o.dryFrac || .15)) tc.lerp(dryC, .3 + .5 * r()); mesh.setColorAt(k, tc); rnd[k] = r(); k++; }
      mesh.count = k; geo.setAttribute('aRnd', new T.InstancedBufferAttribute(rnd, 1)); mesh.receiveShadow = o.receiveShadow !== false; mesh.castShadow = false;
      mesh.frustumCulled = false; grp.add(mesh); out.clumps = mesh; out.mats.push(U);
    }
    if (o.band) {   // far background band: a low soft strip of grass along a path (ribbons of a tileable strand texture), no single blades
      const b = o.band, tx = b.tex || strandTex(Object.assign({ w: 1024, h: 256, tile: true, n: 1100, width: 4, hMin: .3, hMax: 1, seed: (o.seed || 7) + 2 }, b.strands || {}));
      const U = grassUniforms(Object.assign({}, o, { wind: b.wind == null ? .05 : b.wind }), tx), mat = grassMaterial(tx, U, 1, o);
      const path = b.path, rows = b.rows || 2, P = [], N = [], UV = [], G = [], GM = [], I = [], hgt = b.height || 1.4, tm = b.tile || 3;
      for (let rw = 0; rw < rows; rw++) { let len = 0; const base = P.length / 3, cnt = path.length + (b.closed ? 1 : 0);
        for (let i = 0; i < cnt; i++) { const p = path[i % path.length], q = path[(i + 1) % path.length], pp = path[(i - 1 + path.length) % path.length];
          if (i) len += Math.hypot(p[0] - pp[0], p[1] - pp[1]);
          const dx = q[0] - pp[0], dz = q[1] - pp[1], dl = Math.hypot(dx, dz) || 1, off = rw * (b.rowGap || 1.2), x = p[0] + dz / dl * off, z = p[1] - dx / dl * off;
          const hh = hgt * (1 + rw * .25) * (.75 + .5 * (Math.sin(len * .23 + rw * 2) * .5 + .5) * (Math.sin(len * .061 + 1) * .5 + .5) + .1 * Math.sin(len * 1.3)), y0 = ground(x, z) - .08;
          for (let j = 0; j <= 2; j++) { const f = j / 2; P.push(x, y0 + hh * f, z); N.push(0, 1, 0); UV.push(len / tm + rw * .37, f); G.push(f); GM.push(hh * f); } }
        for (let i = 0; i < cnt - 1; i++) for (let j = 0; j < 2; j++) { const a = base + i * 3 + j, c = a + 3; I.push(a, c, a + 1, a + 1, c, c + 1); } }
      const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(P, 3)); g.setAttribute('normal', new T.Float32BufferAttribute(N, 3)); g.setAttribute('uv', new T.Float32BufferAttribute(UV, 2));
      g.setAttribute('gh', new T.Float32BufferAttribute(G, 1)); g.setAttribute('gm', new T.Float32BufferAttribute(GM, 1)); g.setIndex(I);
      mat.color.set(b.color || o.color || '#ffffff'); const mesh = new T.Mesh(g, mat); mesh.receiveShadow = false; grp.add(mesh); out.band = mesh; out.mats.push(U);
    }
    if (o.lawn) {   // fur / shell lawn: N offset copies of a ground patch, each keeps the blade dots taller than its layer (short lawn near the camera)
      const L = o.lawn, nL = L.layers || 8, dc = document.createElement('canvas'); dc.width = dc.height = 256; const dg = dc.getContext('2d'), rl = rng((o.seed || 7) + 3);
      dg.fillStyle = '#000'; dg.fillRect(0, 0, 256, 256);
      for (let i = 0; i < (L.dots || 2600); i++) { const x = rl() * 256, y = rl() * 256, rad = 1.6 + rl() * 2.6, v = .45 + .55 * rl();
        for (const ox of [-256, 0, 256]) for (const oy of [-256, 0, 256]) { const gr = dg.createRadialGradient(x + ox, y + oy, 0, x + ox, y + oy, rad); gr.addColorStop(0, `rgba(255,255,255,${v})`); gr.addColorStop(1, 'rgba(255,255,255,0)'); dg.fillStyle = gr; dg.fillRect(x + ox - rad, y + oy - rad, rad * 2, rad * 2); } }
      const at = tex(dc, false, [L.repeat || 8, L.repeat || 8]); at.anisotropy = 16;
      const lm = new T.MeshLambertMaterial({ color: L.color || '#5b6a34', alphaMap: at, alphaTest: .5, alphaToCoverage: true, map: L.map || null }); if (o.clip) lm.clippingPlanes = o.clip;
      const LU = { gT: { value: 0 }, gH: { value: L.height || .07 }, gFar: { value: L.far || 22 }, gWind: { value: new T.Vector2(.02, .008) } };
      lm.onBeforeCompile = sh => { Object.assign(sh.uniforms, LU);
        sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nuniform float gT,gH; uniform vec2 gWind; attribute float aL; varying float vL;')
          .replace('#include <begin_vertex>', `#include <begin_vertex>
          vL = aL; transformed += normal * aL * gH; transformed.xz += gWind * aL * aL * sin(gT * 1.6 - dot(position.xz, vec2(.35, .12)));`);
        sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float gFar; varying float vL;')
          .replace('#include <alphamap_fragment>', `{ float hv = texture2D(alphaMap, vAlphaMapUv).g; diffuseColor.a = clamp((hv - vL) * 7. + .5, 0., 1.) * (1. - smoothstep(gFar * .7, gFar, length(vViewPosition))); }
          diffuseColor.rgb *= mix(.55, 1.15, vL);`);
      };
      lm.customProgramCacheKey = () => 'kit-lawn' + (o.clip ? '-c' : '');
      const lmesh = new T.InstancedMesh(L.geo, lm, nL), la = new Float32Array(nL), I4 = new T.Matrix4();
      for (let i = 0; i < nL; i++) { lmesh.setMatrixAt(i, I4); la[i] = (i + 1) / (nL + 1) * .95; }
      L.geo.setAttribute('aL', new T.InstancedBufferAttribute(la, 1)); lmesh.receiveShadow = true; lmesh.frustumCulled = false; grp.add(lmesh); out.lawn = lmesh; out.lawnU = LU;
    }
    const sv = new T.Vector3();
    out.update = (t, cam) => { if (sun && cam) sv.copy(sun).transformDirection(cam.matrixWorldInverse);
      out.mats.forEach(U => { U.gT.value = t; if (sun && cam) U.gSunV.value.copy(sv); }); if (out.lawnU) out.lawnU.gT.value = t; };
    return out;
  }
  M.kit = { rng, noise, tex, normalMap, body, fin, shafts, snow, surfaceFromBelow, grass, strandTex };

})();
