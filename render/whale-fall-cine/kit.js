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
  M.kit = { rng, noise, tex, normalMap, body, fin, shafts, snow, surfaceFromBelow };
})();
