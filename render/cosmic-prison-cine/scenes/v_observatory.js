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
(window.MIYA = window.MIYA || { scenes: {} }).scenes.observatory = function (ctx, p) {
  const { T, sm, rng, cue, points, glow } = ctx, K = window.MIYA.kit, E = ctx.env();
  const S = new T.Scene(); S.background = new T.Color('#0f1128');
  const FOGC = new T.Color('#0d0d26'); S.fog = new T.FogExp2(FOGC, .0019);
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), ctx.t);
  const v3 = (x, y, z) => new T.Vector3(x, y, z);

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
  const gal = [], RG = rng(41); for (let i = 0; i < 40; i++) { const d = v3(RG() - .5, .35 + RG() * .9, -.6 - RG() * .8).normalize();
    const sp = new T.Sprite(new T.SpriteMaterial({ map: ctx.dotTex(), color: RG() < .5 ? '#ffd9a8' : '#bcc8ff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, fog: false, rotation: RG() * 3.14 }));
    const s0 = 8 + RG() * 18; sp.scale.set(s0, s0 * (.3 + RG() * .5), 1); sp.position.copy(d.multiplyScalar(1350)); sp.renderOrder = -1; S.add(sp); gal.push([sp, RG()]); }

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
  const path = tau => { tau = Math.max(0, tau); const y = 3.2 * tau * tau + 1.2 * tau * tau * tau; return v3(PAD.x - y * .06, PAD.y + 3 + y, PAD.z - y * 1.1 * Math.min(1, y / 160)); };
  // exhaust trail (particles left along the path; each drifts and fades with age) and the smoke cloud at the pad
  const NT = 4200, tr = points(NT, { size: 1.6, opacity: 1, color: '#ffffff', fog: false }), trA = tr.geometry.attributes.position.array, trC = tr.geometry.attributes.color.array, trB = [];
  { const r = rng(71); for (let i = 0; i < NT; i++) trB.push([r(), r() - .5, r() - .5, r() - .5, r()]); } S.add(tr); tr.frustumCulled = false; tr.renderOrder = 2;
  const NSm = 1400, smk = points(NSm, { size: 16, opacity: .35, color: '#ffffff', fog: true }), smA = smk.geometry.attributes.position.array, smC = smk.geometry.attributes.color.array, smB = [];
  { const r = rng(73); for (let i = 0; i < NSm; i++) smB.push([r() * 6.283, r(), r(), r()]); } smk.material.blending = T.NormalBlending; S.add(smk); smk.frustumCulled = false; smk.renderOrder = 1;

  // ---------------- meteor, dust, lights ----------------
  const met = new T.Mesh(new T.PlaneGeometry(1, 1), new T.MeshBasicMaterial({ map: ctx.ctex(256, (g, s) => { const gr = g.createLinearGradient(0, 0, s, 0); gr.addColorStop(0, 'rgba(255,255,255,0)'); gr.addColorStop(.9, 'rgba(220,230,255,.9)'); gr.addColorStop(1, 'rgba(255,255,255,1)'); g.fillStyle = gr; g.fillRect(0, s * .47, s, s * .06); }),
    transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, fog: false, side: T.DoubleSide })); S.add(met);
  const dust = K.snow(S, { n: 1600, box: [60, 30, 60], size: .1, opacity: .5, color: '#ffd9a0', fall: .05, seed: 9 });
  S.add(new T.HemisphereLight('#4a4f9a', '#06050e', .55));
  const moon = new T.DirectionalLight('#9aa8ff', .55); moon.position.set(-30, 40, -60); S.add(moon);
  const fill = new T.DirectionalLight('#ffd2a0', .12); fill.position.set(40, 20, 40); S.add(fill);
  const key = new T.DirectionalLight('#aab4ff', .9); key.position.set(-25, 30, 45); S.add(key);

  const cam = new T.PerspectiveCamera(42, ctx.W / ctx.H, .1, 4000); ctx.side(cam, p.side == null ? .12 : p.side);
  const PSC = Math.atan2(8, 24), tgt = new T.Vector3(), cp = new T.Vector3(), up = new T.Vector3();
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    const g1 = at(p.glow, 2.5), wd = at(p.widen, 4), sc1 = at(p.scope, 2.2), fo = at(p.follow, 3.2), ed = at(p.edge, 3.5);
    const intro = sm(0, 6.5, u), cl = at(p.close, 6), nt = at(p.night, 16);
    // long shots with the new cues: the slow dolly eases out instead of running into the dome (old cues: unchanged)
    const ue = (p.close != null || p.night != null) ? 30 * (1 - Math.exp(-u / 30)) : u;
    cp.set(8.5 - ue * .1 - 2 * wd, 1.0 + .8 * intro + 2.2 * wd + .1 * Math.sin(u * .3), 25 - ue * .2 + 5 * wd);
    if (nt > 0) { cp.y += 16 * nt; cp.z += 8 * nt; cp.x -= 3 * nt; }
    cam.position.copy(cp);
    // dome: slit first faces left-back, on "telescopes" it turns toward the camera side; shutter opens fully
    DOME.rotation.y = PSC + 1.75 - 1.6 * sc1 + .04 * Math.sin(u * .2);
    SHUT.rotation.x = -(0.55 + .45 * g1 + (GM - 1.0) * sc1);
    if (LEAF) { const c1 = sm(0, .7, cl), c2 = sm(.3, 1, cl); SHUT.rotation.x *= 1 - c1; LEAF.rotation.x = -(2.36 - (2.36 - (SHD - .04)) * c2); }
    const el = .7 + .2 * g1 - .15 * sc1 + (cl > 0 ? (1.45 - (.7 + .2 * g1 - .15 * sc1)) * cl : 0); TUBE.quaternion.setFromUnitVectors(v3(0, 1, 0), v3(0, Math.sin(el), Math.cos(el)));
    const lit = (.25 + .75 * g1) * (1 - .85 * cl); innerM.emissiveIntensity = .035 * lit; inGlow.material.opacity = .3 * lit + .15 * sc1; edgeM.opacity = .25 + .55 * lit;
    mirror.material.color.setRGB(1 * lit + .2, .89 * lit + .15, .69 * lit + .1);
    rimGlow.material.opacity = .45 + .25 * g1;
    // starlight stream: points flow from the sky down into the slit and the telescope mouth
    const dir = v3(0, Math.sin(el), Math.cos(el)), mouth = dir.clone().multiplyScalar(2.6).add(v3(0, .35, 0)), sk = (.9 * g1 + .4 * sc1) * (1 - cl);
    for (let i = 0; i < NS; i++) { const [o, a, b, w] = slB[i], f = (o + t * .22 * (1 + w)) % 1, d = (1 - f) * 34; const spread = .2 + (1 - f) * 2.6;
      slA[i * 3] = mouth.x + dir.x * d + a * spread; slA[i * 3 + 1] = mouth.y + dir.y * d + b * spread * .4; slA[i * 3 + 2] = mouth.z + dir.z * d + b * spread;
      const v = sk * Math.sin(Math.PI * f) * (.4 + .6 * w); slC[i * 3] = v; slC[i * 3 + 1] = v * .92; slC[i * 3 + 2] = v * .75; }
    sl.geometry.attributes.position.needsUpdate = true; sl.geometry.attributes.color.needsUpdate = true;
    // stars twinkle
    starSets.forEach(({ P, c, base, n }) => { for (let i = 0; i < n; i++) { const k = i * 4, tw = .82 + .18 * Math.sin(t * (1.3 + (base[k + 3] % 1) * 2) + base[k + 3] * 7); c[i * 3] = base[k] * tw; c[i * 3 + 1] = base[k + 1] * tw; c[i * 3 + 2] = base[k + 2] * tw; } P.geometry.attributes.color.needsUpdate = true; });
    gal.forEach(([sp, o]) => sp.material.opacity = Math.max(ed, .8 * nt) * (.25 + .35 * o));
    skyK.setScalar(1 + .25 * Math.max(ed, .6 * nt));
    // meteor (one, early)
    const mt = (t - 4.6) / .8; met.visible = mt > 0 && mt < 1;
    if (met.visible) { const a = v3(-380, 820, -1000), b = v3(-640, 620, -980), m = a.clone().lerp(b, mt); met.position.copy(m); met.scale.set(160 * Math.min(1, mt * 3), 6, 1); met.lookAt(0, 0, 0); met.rotateZ(Math.atan2(b.y - a.y, b.x - a.x) + Math.PI); met.material.opacity = Math.sin(Math.PI * mt) * .9; }
    // rocket
    const tau = t - tR, on = true;
    ROCK.visible = on && !((p.night != null || p.close != null) && p.rocket == null); tr.visible = smk.visible = tau > -1.2;
    if (on) { const ign = sm(-1.2, 0, tau), q = path(tau), q2 = path(tau + .05); ROCK.position.copy(q);
      const dv = q2.clone().sub(q); if (dv.lengthSq() > 1e-6) ROCK.quaternion.setFromUnitVectors(v3(0, 1, 0), dv.normalize()); else ROCK.quaternion.identity();
      const fk = .85 + .15 * Math.sin(t * 37) * Math.sin(t * 23);
      fl1.material.opacity = .95 * ign * fk; fl2.material.opacity = .45 * ign * fk; fl1.scale.set(1, .6 + .4 * ign + .25 * sm(0, 4, tau), 1); fl2.scale.set(1 + sm(0, 6, tau) * .6, .6 + .8 * sm(0, 4, tau), 1 + sm(0, 6, tau) * .6);
      fg1.material.opacity = .9 * ign * fk; fg2.material.opacity = .32 * ign;
      const dist = cam.position.distanceTo(q), grow = Math.max(1, dist / 900); fg1.scale.setScalar(9 * grow); fg2.scale.setScalar(40 * grow);
      padG.material.opacity = .5 * ign * (1 - sm(2, 8, tau));
      // trail: particle i was emitted at te = i/NT * span after lift-off
      const span = Math.max(0, Math.min(tau, 12));
      for (let i = 0; i < NT; i++) { const [o, a, b, c, w] = trB[i], te = o * 12; let v = 0;
        if (te < span) { const age = tau - te, e = path(te), sp2 = .6 + age * (1.2 + w * 1.5);
          trA[i * 3] = e.x + a * sp2 + age * 1.5; trA[i * 3 + 1] = e.y + b * sp2 - age * 2; trA[i * 3 + 2] = e.z + c * sp2;
          v = 1.5 * Math.exp(-age * .3) * (age < .25 ? 1.6 : 1) * (.5 + .5 * w); }
        else { trA[i * 3 + 1] = -9999; }
        trC[i * 3] = v; trC[i * 3 + 1] = v * (.72 + .2 * Math.exp(-tau + te)); trC[i * 3 + 2] = v * (.45 + .3 * Math.exp(-tau + te)); }
      tr.geometry.attributes.position.needsUpdate = true; tr.geometry.attributes.color.needsUpdate = true;
      tr.material.size = 3.2 * Math.max(1, cam.position.distanceTo(q) / 500);
      // smoke cloud at the pad: billows outward, lit warm by the flame from below early on
      const sk2 = sm(-1, 1.5, tau), wl = Math.max(0, 1 - sm(1, 6, tau));
      for (let i = 0; i < NSm; i++) { const [a, r0, h0, w] = smB[i], g = Math.max(0, tau + 1 - w * .8), R = (3 + 26 * Math.sqrt(g) * (.3 + r0 * .7));
        smA[i * 3] = PAD.x + Math.cos(a) * R; smA[i * 3 + 1] = PAD.y + 1 + h0 * h0 * (4 + g * 7) * (.3 + .7 * w); smA[i * 3 + 2] = PAD.z + Math.sin(a) * R * .7;
        const v = sk2 * (.22 + .3 * wl) * (1 - sm(6, 14, g)); smC[i * 3] = v * (1.0 + 1.6 * wl); smC[i * 3 + 1] = v * (.9 + 1.0 * wl); smC[i * 3 + 2] = v * (.95 + .4 * wl); }
      smk.geometry.attributes.position.needsUpdate = true; smk.geometry.attributes.color.needsUpdate = true; }
    // camera: begins looking up at the sky, tilts down onto the observatory, rises a little on "widen", then on "follow" tilts
    // up after the rocket and on "edge" pushes in toward the deep field
    tgt.set(-.5 + 1.5 * wd, 4.4 + 16 * (1 - intro) + 1.5 * wd, 0);
    const ft = tgt.clone();
    if (tau > 0 && fo > 0) { const rq = path(tau + .3), dq = rq.distanceTo(cp);
      const lk = rq.clone().add(v3(0, dq * .08 * (1 - ed), 0)).lerp(cp.clone().addScaledVector(A0.clone().add(v3(.05, .16, 0)).normalize(), dq), .55 * ed);
      const yp = q => { const d = q.clone().sub(cp).normalize(); return [Math.atan2(d.x, -d.z), Math.asin(d.y)]; };
      const [y0, p0] = yp(tgt), [y1, p1] = yp(lk), yw = y0 + (y1 - y0) * fo * (.35 + .65 * ed), pt = p0 + (p1 - p0) * fo;
      ft.copy(cp).add(v3(Math.sin(yw) * Math.cos(pt), Math.sin(pt), -Math.cos(yw) * Math.cos(pt)).multiplyScalar(tgt.distanceTo(cp))); }   // same distance as the plain target: the camera director pivots on the look-at point, a sudden 25 -> 100 jump made the camera jump (2026-10-16)
    if (nt > 0) { const d0 = ft.clone().sub(cp).normalize(), d1 = A0.clone().add(v3(.3, .3, 0)).normalize(); ft.copy(cp).addScaledVector(d0.lerp(d1, sm(.1, 1, nt)).normalize(), tgt.distanceTo(cp)); }
    cam.lookAt(ft);
    cam.fov = 42 - 4 * wd + 4 * fo - 10 * ed + 10 * nt;
    if (ctx.VERT) { const h = 2 * Math.atan(Math.tan(cam.fov * Math.PI / 360) * 16 / 9 * .62); cam.fov = 2 * Math.atan(Math.tan(h / 2) * ctx.H / ctx.W) * 180 / Math.PI; }   // Shorts: same vertical fit as ctx.side()
    cam.updateProjectionMatrix();
    dust.update(t, [cp.x - 10, cp.y + 4, cp.z - 20]);
  } };
};
