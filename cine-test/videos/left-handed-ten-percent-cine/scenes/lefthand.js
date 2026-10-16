// lefthand — three shots for "nine out of ten people are right-handed" (left-handed-ten-percent-cine, 2026-10-14).
// Every person is ONE THREE.SkinnedMesh (torso, head, arms, hands, legs merged into one geometry that shares one skeleton of 14
// bones: root, spine, chest, head, shoulder/elbow/wrist x2, hip/knee x2). Skin weights blend across every joint, so arms bend
// smoothly and nothing can come apart. People are anonymous silhouettes seen from behind (featureless heads, no faces).
// Bone angles come from t only (seek-safe).
//  lhtrain  — a dim night train carriage: benches, chrome poles and rails with hanging straps, warm ceiling strips, city lights
//             streaming past the windows; passengers sway with the train, most hold the rail with the right hand.
//             params { side:.1 }
//  lhcrowd  — a dark field of 100 people (10 rows of 10) seen from behind. `right` cue: 90 raise the RIGHT hand in a ripple (cool
//             light at each hand); `left` cue: the one left-hander in every row raises the LEFT hand and glows in the warm accent
//             (halo, light pool on the floor); `share` cue: the right-handers dim, the ten warm figures brighten.
//             params { side:.12, right:cue, left:cue, share:cue }
//  lhglobe  — a dark Earth of light points (land from rough continent outlines); warm points scattered over every inhabited
//             continent light up from `turn` to `every`; the camera pulls back.   params { side:.12, turn:cue, every:cue }
(function () {
  const M = (window.MIYA = window.MIYA || { scenes: {} });

  // ---------------- shared: one skinned person ----------------
  // bone indices
  const ROOT = 0, SPINE = 1, CHEST = 2, HEAD = 3, SHR = 4, ELR = 5, WRR = 6, SHL = 7, ELL = 8, WRL = 9, HIPR = 10, KNR = 11, HIPL = 12, KNL = 13;
  const BPOS = [[0, .95, 0], [0, 1.12, 0], [0, 1.32, 0], [0, 1.52, 0], [.2, 1.43, 0], [.205, 1.14, 0], [.21, .885, 0], [-.2, 1.43, 0], [-.205, 1.14, 0], [-.21, .885, 0],
    [.09, .93, 0], [.09, .5, 0], [-.09, .93, 0], [-.09, .5, 0]];
  const PARENT = [-1, ROOT, SPINE, CHEST, CHEST, SHR, ELR, CHEST, SHL, ELL, ROOT, HIPR, ROOT, HIPL];
  let _geo = null;
  function personGeo(T) {
    if (_geo) return _geo;
    const P = [], SI = [], SW = [], IDX = [], CO = [];
    const lerpW = (a, b, k) => k <= 0 ? [[a, 1]] : k >= 1 ? [[b, 1]] : [[a, 1 - k], [b, k]];
    const ss = (a, b, x) => { x = Math.min(1, Math.max(0, (x - a) / (b - a))); return x * x * (3 - 2 * x); };
    // vertical tube: rings from y0 (bottom) to y1 (top); f(s) -> [cx, cz, rx, rz]; wf(y) -> [[bone, w], ...]; ends closed
    function tube(y0, y1, n, m, f, wf, mat) {
      const start = P.length / 3;
      for (let i = 0; i <= n; i++) { const s = i / n, y = y0 + (y1 - y0) * s, [cx, cz, rx, rz] = f(s), w = wf(y);
        for (let j = 0; j < m; j++) { const a = j / m * Math.PI * 2; P.push(cx + Math.sin(a) * rx, y, cz + Math.cos(a) * rz); const cv = mat ? .42 : 1; CO.push(cv, cv * .96, cv * .92);
          const si = [0, 0, 0, 0], sw = [0, 0, 0, 0]; w.forEach(([b, v], k) => { si[k] = b; sw[k] = v; }); SI.push(...si); SW.push(...sw); } }
      for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) { const a = start + i * m + j, b = start + i * m + (j + 1) % m, c = a + m, d = b + m; IDX.push(a, b, c, b, d, c); }
    }
    const cap = (s, e) => Math.sqrt(Math.max(0, 1 - Math.pow(1 - Math.min(1, s / e), 2)));   // rounded end over the first e of s
    const ends = (s, a, b) => cap(s, a) * cap(1 - s, b);
    // torso: hips .84 -> neck 1.56 (half width x, half depth z), with a sloping shoulder line
    const tw = [[0, .15], [.06, .17], [.25, .155], [.45, .165], [.62, .19], [.76, .205], [.84, .19], [.9, .13], [.96, .075], [1, .06]];
    const td = [[0, .1], [.06, .11], [.25, .1], [.45, .11], [.62, .12], [.76, .105], [.84, .09], [.9, .07], [.96, .055], [1, .05]];
    const pl = (tab, s) => { for (let k = 1; k < tab.length; k++) if (s <= tab[k][0]) { const [a, va] = tab[k - 1], [b, vb] = tab[k], q = (s - a) / (b - a), e = q * q * (3 - 2 * q); return va + (vb - va) * e; } return tab[tab.length - 1][1]; };
    tube(.84, 1.56, 22, 22, s => [0, .008 * Math.sin(s * 3), pl(tw, s) * (s < .03 ? .6 + s / .03 * .4 : 1), pl(td, s) * (s < .03 ? .6 + s / .03 * .4 : 1)],
      y => y < 1.0 ? lerpW(ROOT, SPINE, ss(.95, 1.05, y)) : y < 1.25 ? lerpW(ROOT, SPINE, ss(.95, 1.12, y)) : y < 1.5 ? lerpW(SPINE, CHEST, ss(1.2, 1.34, y)) : lerpW(CHEST, HEAD, ss(1.5, 1.58, y)), 0);
    // neck + head (back of the head, hair): one closed tube
    tube(1.5, 1.79, 16, 18, s => { const y = 1.5 + .29 * s; const hs = Math.max(0, 1 - Math.pow((y - 1.675) / .115, 2)); const neck = .05;
      const rx = Math.max(neck * (1 - ss(1.6, 1.65, y) * .2), .088 * Math.sqrt(hs)); const rz = Math.max(neck, .102 * Math.sqrt(hs));
      return [0, .012 + .01 * ss(1.6, 1.7, y), rx * cap(1 - s, .12), rz * cap(1 - s, .12)]; },
      y => lerpW(CHEST, HEAD, ss(1.5, 1.58, y)), 1);
    // arms (shoulder top 1.48 -> wrist .88) and hands (.9 -> .7), both sides
    [[1, SHR, ELR, WRR], [-1, SHL, ELL, WRL]].forEach(([sd, sh, el, wr]) => {
      const ar = [[0, .028], [.1, .036], [.4, .04], [.5, .043], [.78, .046], [.9, .052], [1, .05]];
      tube(.875, 1.49, 18, 10, s => [sd * (.21 - .01 * s), 0, pl(ar, s) * cap(1 - s, .09), pl(ar, s) * cap(1 - s, .09) * 1.05],
        y => y > 1.44 ? lerpW(sh, CHEST, ss(1.45, 1.5, y) * .5) : y > 1.0 ? lerpW(el, sh, ss(1.09, 1.19, y)) : lerpW(wr, el, ss(.87, .93, y)), 0);
      tube(.69, .905, 6, 8, s => [sd * (.212 + .006 * Math.sin(s * 3)), -.008, .02 * ends(s, .25, .2) + .004, .045 * ends(s, .3, .25) * (s > .7 ? 1 - (s - .7) * .9 : 1)],
        y => lerpW(wr, el, ss(.87, .93, y)), 1);
    });
    // legs + feet
    [[1, HIPR, KNR], [-1, HIPL, KNL]].forEach(([sd, hp, kn]) => {
      const lr = [[0, .042], [.1, .045], [.3, .055], [.42, .058], [.55, .056], [.75, .075], [.9, .085], [1, .085]];
      tube(.04, .95, 12, 8, s => [sd * (.095 - .01 * s), 0, pl(lr, s) * cap(1 - s, .05), pl(lr, s) * 1.05 * cap(1 - s, .05)],
        y => y > .9 ? lerpW(hp, ROOT, ss(.92, .98, y) * .6) : lerpW(kn, hp, ss(.44, .56, y)), 0);
      tube(0, .1, 4, 8, s => [sd * .095, -.055, .045 * cap(1 - s, .5), .125 * cap(1 - s, .7)], () => [[kn, 1]], 0);
    });
    const g = new T.BufferGeometry();
    g.setAttribute('position', new T.Float32BufferAttribute(P, 3)); g.setAttribute('skinIndex', new T.Uint16BufferAttribute(SI, 4)); g.setAttribute('skinWeight', new T.Float32BufferAttribute(SW, 4));
    g.setAttribute('color', new T.Float32BufferAttribute(CO, 3)); g.setIndex(IDX); g.computeVertexNormals(); g.computeBoundingSphere();
    _geo = g; return g;
  }
  // ---- dressed person (lhtrain, 2026-10-15 "the subway people look like mannequins"): the SAME 14-bone skeleton, but clothes,
  // hair and bags are silhouettes inside the ONE skinned geometry: coat/jacket hem that flares below the hips (open hem with an
  // inner lip), collar or a hood lying on the upper back, sleeves wider than the wrist with a cuff, trousers or a skirt, shoes,
  // hair volume (short, long, bun, ponytail, cap, beanie), backpack or sling bag. Colours live in vertex colours (one material per
  // person, colour white), roughness per vertex in `aRo` (wool vs nylon vs hair sheen vs leather), uv for a fabric normal map.
  // o: { seed, top:'coat'|'jacket'|'hoodie'|'parka', hem, bulk, collar, hood, hair, bag:null|'pack'|'sling', skirt, sit, glove,
  //      cols:{ top, low, hair, skin, shoe, bag, hat, tights } }
  function dressedGeo(T, o) {
    const P = [], SI = [], SW = [], IDX = [], CO = [], UV = [], RO = [], SEAM = [];
    const C = h => { const c = new T.Color(h); return [c.r, c.g, c.b]; }, cl = o.cols;
    const cTop = C(cl.top), cLow = C(cl.low), cHair = C(cl.hair), cSkin = C(cl.skin), cShoe = C(cl.shoe), cBag = C(cl.bag || '#1d1f24'), cHat = C(cl.hat || cl.hair), cTig = C(cl.tights || '#141418');
    const lerpW = (a, b, k) => k <= 0 ? [[a, 1]] : k >= 1 ? [[b, 1]] : [[a, 1 - k], [b, k]];
    const ss = (a, b, x) => { x = Math.min(1, Math.max(0, (x - a) / (b - a))); return x * x * (3 - 2 * x); };
    const cap = (s, e) => Math.sqrt(Math.max(0, 1 - Math.pow(1 - Math.min(1, s / e), 2)));
    const ends = (s, a, b) => cap(s, a) * cap(1 - s, b);
    const pl = (tab, s) => { for (let k = 1; k < tab.length; k++) if (s <= tab[k][0]) { const [a, va] = tab[k - 1], [b, vb] = tab[k], q = (s - a) / (b - a), e = q * q * (3 - 2 * q); return va + (vb - va) * e; } return tab[tab.length - 1][1]; };
    const ph = [0, 1, 2, 3, 4, 5].map(k => { const s = Math.sin((k + 1) * 12.9898 + o.seed * 78.233) * 43758.5453; return (s - Math.floor(s)) * 6.283; });
    const mot = (y, a, k) => 1 + k * (.6 * Math.sin(y * 6.5 + ph[0] + Math.sin(a * 2 + ph[1])) + .4 * Math.sin(a * 3 + y * 2.3 + ph[2]));   // low-frequency dye/wear
    const mul = (c, k) => [c[0] * k, c[1] * k, c[2] * k];
    const span = (a, b, n) => Array.from({ length: n + 1 }, (_, i) => a + (b - a) * i / n);
    // ring tube: ys = ring heights; f(y, i) -> [cx, cz, rx, rz]; wf(y, x) -> [[bone, w], ...]; dr(y, a, x) -> outward offset (m);
    // col(y, a, x, i) -> [rgb, roughness]; e < 1 squares the section; U = texture repeats around. Seam normals are averaged below.
    function tube(ys, m, f, wf, col, dr, e, U) {
      const start = P.length / 3; e = e || 1; U = U || 1;
      ys.forEach((y, i) => { const [cx, cz, rx, rz] = f(y, i);
        for (let j = 0; j <= m; j++) { const a = Math.PI + j / m * Math.PI * 2, sa = Math.sin(a), ca = Math.cos(a);
          const ex = Math.sign(sa) * Math.pow(Math.abs(sa), e), ez = Math.sign(ca) * Math.pow(Math.abs(ca), e), x0 = cx + ex * rx;
          const d = dr ? dr(y, a, x0) * Math.min(1, Math.min(rx, rz) / .03) : 0;
          P.push(x0 + ex * d, y, cz + ez * (rz + d));
          const [c, r] = col(y, a, x0, i); CO.push(c[0], c[1], c[2]); RO.push(r); UV.push(j / m * U, y * 4);
          const si = [0, 0, 0, 0], sw = [0, 0, 0, 0]; wf(y, x0).forEach(([b, v], k) => { si[k] = b; sw[k] = v; }); SI.push(...si); SW.push(...sw); }
        SEAM.push([start + i * (m + 1), start + i * (m + 1) + m]); });
      for (let i = 0; i < ys.length - 1; i++) for (let j = 0; j < m; j++) { const a = start + i * (m + 1) + j, b = a + 1, c = a + m + 1, d = b + m + 1; IDX.push(a, b, c, b, d, c); }
    }
    const bk = o.bulk || 1, hem = o.hem, coat = hem < .8, hood = !!o.hood, bag = o.bag;
    const rTop = o.top === 'parka' ? .5 : o.top === 'hoodie' ? .9 : .82;   // nylon parka has a soft sheen; wool and cotton are matte
    // ---- torso / coat: hem (open, inner lip) -> collar (inner lip at the neck)
    const tw = [[0, .15], [.06, .17], [.25, .155], [.45, .165], [.62, .19], [.76, .205], [.84, .19], [.9, .13], [.96, .075], [1, .06]];
    const td = [[0, .1], [.06, .11], [.25, .1], [.45, .11], [.62, .12], [.76, .105], [.84, .09], [.9, .07], [.96, .055], [1, .05]];
    const flare = coat ? .13 : .06;
    const W = y => { const s = Math.min(1, (y - .84) / .72), nat = pl(tw, Math.max(0, s)) * (s < .85 ? bk : 1 + (bk - 1) * .4), cov = .19 * (1 + (bk - 1) * .5);
      if (y < .84) return cov + (.84 - y) * flare; return y < 1.06 ? cov + (nat - cov) * ss(.95, 1.06, y) : nat; };
    const D = y => { const s = Math.min(1, (y - .84) / .72), nat = pl(td, Math.max(0, s)) * (s < .85 ? bk : 1 + (bk - 1) * .4), cov = .128 * (1 + (bk - 1) * .5);
      if (y < .84) return cov + (.84 - y) * flare * .6; return y < 1.06 ? cov + (nat - cov) * ss(.95, 1.06, y) : nat; };
    const topY = o.collar ? 1.61 : hood ? 1.575 : 1.565;
    const tys = [hem + .03, hem, ...span(hem + .015, 1.53, Math.round((1.53 - hem) / .034)), ...span(1.545, topY, 3), topY - .006];
    const NT = tys.length;
    tube(tys, 30, (y, i) => { const cz = .008 * Math.sin(Math.max(0, (y - .84) / .72) * 3) + (y < .9 ? .006 : 0);
        if (i === 0) return [0, cz, W(hem) * .9, D(hem) * .88];
        if (i === NT - 1) return [0, .012, .054, .054];
        if (y > 1.535) { const cr = o.collar ? .074 + .012 * ss(1.575, 1.55, y) : .066; return [0, .01, cr, cr * .95]; }
        return [0, cz, W(y), D(y)]; },
      (y, x) => y < .93 ? (o.sit ? lerpW(ROOT, x > 0 ? HIPR : HIPL, ss(.93, .8, y) * .5) : [[ROOT, 1]]) : y < 1.25 ? lerpW(ROOT, SPINE, ss(.95, 1.12, y)) : y < 1.5 ? lerpW(SPINE, CHEST, ss(1.2, 1.34, y)) : lerpW(CHEST, HEAD, ss(1.53, 1.62, y) * .3),
      (y, a, x, i) => { let c = mul(cTop, mot(y, a, .07) * (.86 + .14 * ss(hem, 1.4, y))), r = rTop;
        if (i === 0 || i === NT - 1) c = mul(c, .45);
        if (hood) c = mul(c, 1 - .3 * Math.exp(-Math.pow((y - 1.37) / .02, 2)) * Math.max(0, Math.cos(a)));   // shadow under the hood
        if (bag === 'pack' && y > 1.25 && Math.abs(Math.abs(x) - .1) < .024) { c = mul(cBag, .8); r = .6; }
        if (bag === 'sling' && y > .95 && y < 1.5 && Math.abs(x - (-.15 + (1.5 - y) * .5)) < .022) { c = mul(cBag, .8); r = .6; }
        return [c, r]; },
      (y, a, x) => { let d = 0;
        if (y < .98) d += (coat ? .011 : .005) * Math.sin(a * 7 + ph[3] + y * 4) * ss(.98, .62, y);   // hanging folds below the waist
        d += .003 * Math.sin(a * 5 + ph[4] + y * 9) * ss(1.0, 1.3, y) * ss(1.5, 1.3, y);              // soft pull wrinkles on the back
        if (hood) d += .042 * Math.exp(-Math.pow((y - 1.43) / .05, 2)) * Math.pow(Math.max(0, Math.cos(a)), 1.6);   // hood lying flat on the upper back
        if (bag === 'pack' && y > 1.25 && Math.abs(Math.abs(x) - .1) < .024) d += .006;
        if (bag === 'sling' && y > .95 && y < 1.5 && Math.abs(x - (-.15 + (1.5 - y) * .5)) < .022) d += .005;
        return d; }, .82, 4);
    // ---- skirt (under a short jacket)
    if (o.skirt) { const sh = o.skirtHem || .52;
      tube([sh + .025, sh, ...span(sh + .012, .97, 9)], 24, (y, i) => { const k = (.97 - y) / (.97 - sh), w = .172 + .065 * k, dd = .118 + .04 * k; return i === 0 ? [0, .004, w * .9, dd * .9] : [0, .004, w, dd]; },
        () => [[ROOT, 1]], (y, a, x, i) => [mul(cLow, mot(y, a, .06) * (i === 0 ? .45 : 1)), .8],
        (y, a) => .009 * Math.sin(a * 8 + ph[5]) * ss(.95, .6, y), 1, 3);
    }
    // ---- sleeves (cuff with inner lip) and hands
    const arC = [[0, .049], [.15, .046], [.45, .045], [.55, .047], [.8, .052], [.9, .056], [1, .052]], ba = o.top === 'parka' ? 1.15 : bk;
    [[1, SHR, ELR, WRR], [-1, SHL, ELL, WRL]].forEach(([sd, sh, el, wr]) => {
      const AW = (y, x) => y > 1.44 ? lerpW(sh, CHEST, ss(1.45, 1.5, y) * .5) : y > 1.0 ? lerpW(el, sh, ss(1.09, 1.19, y)) : lerpW(wr, el, ss(.87, .93, y));
      tube([.922, .9, ...span(.912, 1.47, 20)], 14, (y, i) => { const s = Math.max(0, (y - .875) / .595), cx = sd * (.244 - .03 * s);
          if (i === 0) return [cx, 0, .029, .031]; const rr = pl(arC, s) * ba * cap(1 - s, .09); return [cx, 0, rr, rr * 1.04]; },
        AW, (y, a, x, i) => [mul(cTop, mot(y, a + sd, .07) * (i === 0 ? .4 : .9 + .1 * ss(.9, 1.4, y))), rTop],
        (y, a) => .005 * Math.sin(y * 70 + ph[5] + a * .6) * Math.exp(-Math.pow((y - 1.13) / .07, 2)), 1, 1);
      tube(span(.735, .912, 6), 8, y => { const s = (y - .735) / .177; return [sd * (.246 + .006 * Math.sin(s * 3)), -.006, .022 * ends(s, .3, .2) + .005, .04 * ends(s, .35, .25) * (s > .7 ? 1 - (s - .7) * .9 : 1)]; },
        AW, () => [o.glove ? mul(cHat, .8) : cSkin, o.glove ? .7 : .6], null, 1, 1);
    });
    // ---- trouser legs (or tights) and shoes
    const lr = [[0, .045], [.1, .046], [.3, .055], [.42, .058], [.55, .056], [.75, .075], [.9, .085], [1, .085]], lk = o.skirt ? .82 : 1.1;
    [[1, HIPR, KNR], [-1, HIPL, KNL]].forEach(([sd, hp, kn]) => {
      tube(span(.05, .95, 16), 12, y => { const s = (y - .04) / .91, rr = pl(lr, s) * lk * cap(1 - s, .05); return [sd * (.095 - .01 * s), 0, rr, rr * 1.05]; },
        y => y > .9 ? lerpW(hp, ROOT, ss(.92, .98, y) * .6) : lerpW(kn, hp, ss(.44, .56, y)),
        (y, a) => [o.skirt ? cTig : mul(cLow, mot(y, a, .06) * (.8 + .2 * ss(.1, .6, y))), o.skirt ? .45 : .85],
        (y, a) => o.skirt ? 0 : .006 * Math.sin(a * 3 + y * 22 + ph[4]) * ss(.45, .12, y) + .004 * Math.sin(a * 2 + y * 40) * Math.exp(-Math.pow((y - .5) / .06, 2)), 1, 2);
      tube(span(0, .1, 4), 10, y => { const s = y / .1; return [sd * .095, -.055, .047 * cap(1 - s, .5), .128 * cap(1 - s, .7)]; }, () => [[kn, 1]], () => [cShoe, .45], null, 1, 1);
    });
    // ---- neck + head with hair volume (long hair: a curtain down the upper back); hat or hair shapes
    const hair = o.hair, top = hair === 'beanie' ? .016 : hair === 'cap' ? .012 : .008, y0 = 1.5, yb = hair === 'long' ? 1.42 : 1.6, hatL = hair === 'beanie' ? 1.665 : 1.688;
    const hatOn = hair === 'cap' || hair === 'beanie';
    const hairK = (y, a) => ss(-.05, .05, y - (1.725 + (yb - 1.725) * ss(-.3, .6, Math.cos(a))));
    tube(span(y0, 1.79 + top, 18), 20, y => { const s = (y - y0) / (1.79 + top - y0), q = (y - 1.675) / (y > 1.675 ? .115 + top : .115), hs = Math.max(0, 1 - q * q), neck = .05;
        const rx = Math.max(neck * (1 - ss(1.6, 1.65, y) * .2), .088 * Math.sqrt(hs)), rz = Math.max(neck, .102 * Math.sqrt(hs));
        return [0, .012 + .01 * ss(1.6, 1.7, y), rx * cap(1 - s, .12), rz * cap(1 - s, .12)]; },
      y => y < 1.5 ? [[CHEST, 1]] : lerpW(CHEST, HEAD, ss(1.5, 1.58, y)),
      (y, a) => { if (hatOn && y > hatL) return [mul(cHat, mot(y, a, .05) * (hair === 'beanie' && y < hatL + .035 ? .8 : 1)), hair === 'cap' ? .7 : .9];
        const k = hairK(y, a), hc = mul(cHair, mot(y * 3, a, .12)); return [[cSkin[0] * .8 + (hc[0] - cSkin[0] * .8) * k, cSkin[1] * .8 + (hc[1] - cSkin[1] * .8) * k, cSkin[2] * .8 + (hc[2] - cSkin[2] * .8) * k], .6 + (.55 - .6) * k]; },
      (y, a) => { const hk = hairK(y, a); let d = hk * ((hair === 'long' ? .016 : .011) + .005 * Math.sin(a * 5 + ph[2] + y * 26) + .003 * Math.sin(a * 11 + ph[3]));   // uneven hair, not a smooth shell
        if (hatOn && y > hatL) d += .003 + (hair === 'beanie' && y < hatL + .03 ? .004 : 0);
        return d; }, 1, 2);
    // long hair: a flat curtain hanging from the back of the head onto the upper back (wide, thin, strand-like normals)
    if (hair === 'long') { const hb = 1.36 + (o.seed % 5) * .012;
      tube(span(hb, 1.7, 10), 16, y => { const s = (y - hb) / (1.7 - hb), k = cap(s, .12) * cap(1 - s, .25), u = ss(1.62, hb, y);
          return [0, .068 + .022 * u, (.085 + .03 * u) * k, .03 * (.75 + .25 * k)]; },
        y => y < 1.5 ? [[CHEST, 1]] : lerpW(CHEST, HEAD, ss(1.5, 1.6, y)), (y, a) => [mul(cHair, mot(y * 3, a * 3, .12) * (.8 + .2 * ss(hb, 1.6, y))), .5],
        (y, a) => .004 * Math.sin(a * 9 + ph[1] + y * 6), .9, 4); }
    if (hair === 'bun') tube(span(1.695, 1.785, 6), 12, y => { const s = (y - 1.695) / .09, r = .042 * ends(s, .5, .5); return [0, .118, r, r]; }, () => [[HEAD, 1]], (y, a) => [mul(cHair, mot(y * 3, a, .1)), .5], null, 1, 1);
    if (hair === 'pony') tube(span(1.45, 1.73, 8), 10, y => { const s = (y - 1.45) / .28, r = .026 * (.55 + .45 * s) * cap(s, .15) * cap(1 - s, .2); return [0, .118 + .012 * s, r, r * 1.1]; }, () => [[HEAD, 1]], (y, a) => [mul(cHair, mot(y * 3, a, .1)), .5], null, 1, 1);
    if (hair === 'cap') tube([1.69, 1.7, 1.712], 16, (y, i) => i === 1 ? [0, -.13, .085, .07] : [0, -.12, .002, .002], () => [[HEAD, 1]], () => [cHat, .7], null, 1, 1);
    // ---- bags
    // bags: boxy sections (e < 1) with flat, slightly rounded top and bottom (end rings close in)
    const box = (y0, y1, n) => [y0, y0 + .006, y0 + .02, ...span(y0 + .04, y1 - .04, n), y1 - .02, y1 - .006, y1];
    const boxK = i => [0, .7, .94][i] != null ? [0, .7, .94][i] : 1, boxR = (i, n) => i >= n - 3 ? [0, .7, .94][n - 1 - i] : boxK(i);
    if (bag === 'pack') { const ys = box(.97, 1.37, 6), n = ys.length;
      tube(ys, 16, (y, i) => { const k = boxR(i, n) * (1 - .12 * ss(1.24, 1.37, y)); return [0, .2 * (1 + (bk - 1) * .6), .135 * k, .068 * k]; },
        y => lerpW(SPINE, CHEST, ss(1.15, 1.3, y)), (y, a) => [mul(cBag, mot(y, a, .08)), .55],
        (y, a) => .018 * Math.max(0, Math.cos(a)) * ss(1.01, 1.05, y) * ss(1.2, 1.16, y) * ss(.85, .45, Math.abs(Math.sin(a))), .5, 1); }
    if (bag === 'sling') { const ys = box(.8, 1.0, 3), n = ys.length;
      tube(ys, 14, (y, i) => { const k = boxR(i, n); return [.07, .19, .11 * k, .042 * k]; }, () => [[ROOT, 1]], (y, a) => [mul(cBag, mot(y, a, .08)), .6], null, .45, 1); }
    const g = new T.BufferGeometry();
    g.setAttribute('position', new T.Float32BufferAttribute(P, 3)); g.setAttribute('skinIndex', new T.Uint16BufferAttribute(SI, 4)); g.setAttribute('skinWeight', new T.Float32BufferAttribute(SW, 4));
    g.setAttribute('color', new T.Float32BufferAttribute(CO, 3)); g.setAttribute('uv', new T.Float32BufferAttribute(UV, 2)); g.setAttribute('aRo', new T.Float32BufferAttribute(RO, 1));
    g.setIndex(IDX); g.computeVertexNormals();
    const N = g.attributes.normal, nv = new T.Vector3(), nw = new T.Vector3();
    SEAM.forEach(([a, b]) => { nv.fromBufferAttribute(N, a).add(nw.fromBufferAttribute(N, b)).normalize(); N.setXYZ(a, nv.x, nv.y, nv.z); N.setXYZ(b, nv.x, nv.y, nv.z); });
    g.computeBoundingSphere(); return g;
  }
  // material with a DIRECTIONAL fresnel rim: only the edges that face the light behind the figure catch it (fresnel weighted by
  // the light direction in view space, spec 3A "backlit but readable"; never an all-round outline). `lit` is a shared uniform
  // object { L: view-space direction (P = 0) or view-space light position (P = 1) } that the scene updates every frame.
  function rimLight(T) { return { L: { value: new T.Vector3(0, .5, -.85) }, P: { value: 0 } }; }
  // cloth (optional): a fabric normal-map texture; the material then also reads per-vertex roughness `aRo` (dressedGeo) and fades
  // the fabric normals with distance (spec 3A "stable in motion")
  function personMat(T, color, rim, k, rough, lit, cloth) {
    const m = new T.MeshStandardMaterial({ color, roughness: rough == null ? .74 : rough, metalness: 0, vertexColors: true });
    if (cloth) { m.normalMap = cloth; m.normalScale.set(.4, .4); }
    m.userData.rimC = { value: new T.Color(rim) }; m.userData.rimK = { value: k }; lit = lit || rimLight(T);
    m.onBeforeCompile = sh => { sh.uniforms.rimC = m.userData.rimC; sh.uniforms.rimK = m.userData.rimK; sh.uniforms.rimL = lit.L; sh.uniforms.rimP = lit.P;
      sh.fragmentShader = 'uniform vec3 rimC; uniform float rimK; uniform vec3 rimL; uniform float rimP;\n' + sh.fragmentShader.replace('#include <emissivemap_fragment>',
        '#include <emissivemap_fragment>\n vec3 rLv = normalize(rimP > .5 ? rimL + vViewPosition : rimL);\n' +
        ' float fr = pow(1.0 - clamp(abs(dot(normal, normalize(vViewPosition))), 0.0, 1.0), 2.6);\n' +
        ' vec2 rN = normal.xy / max(1e-4, length(normal.xy)), rS = rLv.xy / max(1e-4, length(rLv.xy));\n' +
        ' float rw = smoothstep(-.25, .75, dot(rN, rS)) * (.35 + .65 * smoothstep(-.4, .5, dot(normal, rLv)));\n totalEmissiveRadiance += rimC * fr * rw * rimK;');
      if (cloth) {
        sh.vertexShader = 'attribute float aRo;\nvarying float vRo;\n' + sh.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>\n vRo = aRo;');
        sh.fragmentShader = 'varying float vRo;\n' + sh.fragmentShader.replace('#include <roughnessmap_fragment>', '#include <roughnessmap_fragment>\n roughnessFactor = vRo;')
          .replace('#include <normal_fragment_maps>', T.ShaderChunk.normal_fragment_maps.replace('mapN.xy *= normalScale;', 'mapN.xy *= normalScale * (1.0 - smoothstep(4.5, 12.0, length(vViewPosition)));'));
      } };
    m.customProgramCacheKey = () => cloth ? 'lhrimcloth' : 'lhrimdir';
    return m;
  }
  // world light (direction when P = 0, position when P = 1) -> view space, after the camera has moved
  function aimRim(lit, cam, w) { cam.updateMatrixWorld(); if (lit.P.value > .5) lit.L.value.copy(w).applyMatrix4(cam.matrixWorldInverse); else lit.L.value.copy(w).transformDirection(cam.matrixWorldInverse); }
  // one person: { root (Object3D to place), mesh, bones, pose(o) }
  function person(T, mats, geo) {
    const g = geo || personGeo(T), bones = BPOS.map(() => new T.Bone());
    bones.forEach((b, i) => { const p = BPOS[i], q = PARENT[i] < 0 ? [0, 0, 0] : BPOS[PARENT[i]]; b.position.set(p[0] - q[0], p[1] - q[1], p[2] - q[2]); if (PARENT[i] >= 0) bones[PARENT[i]].add(b); });
    const mesh = new T.SkinnedMesh(g, mats); mesh.add(bones[0]); mesh.bind(new T.Skeleton(bones)); mesh.boundingSphere = new T.Sphere(new T.Vector3(0, 1.15, 0), 1.35);
    const root = new T.Group(); root.add(mesh);
    // o: { r:[shX, shZ, elX, wrX], l:[...], breath, sway, lean, sit, look (+ tips the head BACK, - looks down), turn,
    //      hip (weight shift: pelvis tilt, upper body counter-tilts), knee (+ relaxed right knee, - left), slump (rounded upper
    //      back), tilt (head roll), shrug (chest roll: one shoulder higher) }  — the optional ones default to 0 (lhcrowd unchanged)
    function pose(o) {
      bones.forEach(b => b.rotation.set(0, 0, 0)); const hip = o.hip || 0; bones[ROOT].position.set(-hip * .45, .95, 0);
      const br = o.breath || 0; bones[SPINE].rotation.x = -.02 + .015 * br + (o.lean || 0); bones[CHEST].rotation.x = .02 * br + (o.slump || 0); bones[CHEST].rotation.z = (o.sway || 0) * .5 + (o.shrug || 0);
      bones[ROOT].rotation.z = (o.sway || 0) + hip; bones[SPINE].rotation.z = -hip * 1.4; bones[HEAD].rotation.x = (o.look || 0); bones[HEAD].rotation.y = (o.turn || 0); bones[HEAD].rotation.z = (o.tilt || 0);
      if (o.knee) { const kk = Math.abs(o.knee); bones[o.knee > 0 ? KNR : KNL].rotation.x = -kk; bones[o.knee > 0 ? HIPR : HIPL].rotation.x = kk * .45; }
      const r = o.r || [0, 0, 0, 0], l = o.l || [0, 0, 0, 0];
      bones[SHR].rotation.set(r[0], 0, .05 + r[1]); bones[ELR].rotation.x = r[2]; bones[WRR].rotation.x = r[3] || 0;
      bones[SHL].rotation.set(l[0], 0, -.05 - l[1]); bones[ELL].rotation.x = l[2]; bones[WRL].rotation.x = l[3] || 0;
      if (o.sit) { bones[ROOT].position.y = .95 - .47 * o.sit; bones[HIPR].rotation.x = bones[HIPL].rotation.x = 1.57 * o.sit; bones[KNR].rotation.x = bones[KNL].rotation.x = -1.57 * o.sit; }
    }
    return { root, mesh, bones, pose };
  }
  M.lhPerson = { person, personMat, personGeo, dressedGeo, rimLight, aimRim, WRR, WRL, CHEST, HEAD };

  // navy-violet sky dome with a soft glow band
  function dome(T, top, mid, bot) {
    return new T.Mesh(new T.SphereGeometry(400, 32, 16), new T.ShaderMaterial({ side: T.BackSide, depthWrite: false, fog: false,
      uniforms: { a: { value: new T.Color(top) }, b: { value: new T.Color(mid) }, c: { value: new T.Color(bot) }, k: { value: 1 } },
      vertexShader: 'varying vec3 vP; void main(){ vP=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
      fragmentShader: 'uniform vec3 a,b,c; uniform float k; varying vec3 vP; void main(){ float y=vP.y; vec3 col = y>0. ? mix(b,a,pow(min(1.,y*1.6),.7)) : mix(b,c,pow(min(1.,-y*3.),.6)); gl_FragColor=vec4(col*k,1.); }' }));
  }

  // ---------------- lhtrain ----------------
  M.scenes.lhtrain = function (ctx, p) {
    const { T, sm, rng } = ctx, K = M.kit, S = new T.Scene(), E = ctx.env();
    S.background = new T.Color('#05050e'); S.fog = new T.FogExp2('#0b0a18', .07);
    const HW = 1.42, Z0 = 4, Z1 = -20, LEN = Z0 - Z1, ZC = (Z0 + Z1) / 2;
    // floor: speckled rubber
    const fl = K.noise(256, { seed: 3, octaves: 5, sx: 6, sy: 6 }), flT = K.tex(fl, true, [3, 22]); flT.anisotropy = ctx.R.capabilities.getMaxAnisotropy();
    const floor = new T.Mesh(new T.PlaneGeometry(HW * 2, LEN), new T.MeshStandardMaterial({ color: '#2b2a34', map: flT, roughness: .55, metalness: .1, envMap: E, envMapIntensity: .25 }));
    floor.rotation.x = -Math.PI / 2; floor.position.z = ZC; S.add(floor);
    const wallM = new T.MeshLambertMaterial({ color: '#3a3b48' });   // matte (Lambert: half the cost of PBR here)
    const trimM = new T.MeshStandardMaterial({ color: '#9aa0b4', roughness: .25, metalness: 1, envMap: E, envMapIntensity: .8 });
    const seatM = new T.MeshLambertMaterial({ color: '#4a2228' });
    // city lights outside (seek-safe scrolling texture)
    const city = ctx.ctex(1024, (g, z) => { g.fillStyle = '#04060f'; g.fillRect(0, 0, z, z); const r = rng(12);
      for (let i = 0; i < 520; i++) { const x = r() * z, y = z * (.15 + r() * .8), s = 2 + r() * 14, warm = r() < .65;
        const gr = g.createRadialGradient(x, y, 0, x, y, s); gr.addColorStop(0, warm ? 'rgba(255,190,110,.9)' : 'rgba(150,180,255,.8)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(x - s, y - s, s * 2, s * 2); }
      for (let i = 0; i < 40; i++) { const y = z * (.3 + r() * .6); g.fillStyle = `rgba(255,${180 + r() * 60 | 0},120,${.05 + r() * .12})`; g.fillRect(0, y, z, 1 + r() * 3); } });
    city.wrapS = city.wrapT = T.RepeatWrapping; city.repeat.set(3, 1);
    const glassM = new T.MeshBasicMaterial({ map: city, color: '#7d86a8', fog: false });
    [-1, 1].forEach(sd => {
      const win = new T.Mesh(new T.PlaneGeometry(LEN, 1.0), glassM); win.position.set(sd * (HW + .12), 1.42, ZC); win.rotation.y = -sd * Math.PI / 2; S.add(win);
      // wall: lower panel, upper band, pillars between windows (all with depth)
      const lo = new T.Mesh(new T.BoxGeometry(.1, .92, LEN), wallM); lo.position.set(sd * (HW + .05), .46, ZC); S.add(lo);
      const up = new T.Mesh(new T.BoxGeometry(.1, .3, LEN), wallM); up.position.set(sd * (HW + .05), 2.07, ZC); S.add(up);
      for (let z = Z0 - .6; z > Z1; z -= 1.7) { const pi = new T.Mesh(new T.BoxGeometry(.14, 1.04, .22), wallM); pi.position.set(sd * (HW + .03), 1.42, z); S.add(pi); }
      const sill = new T.Mesh(new T.BoxGeometry(.08, .04, LEN), trimM); sill.position.set(sd * (HW - .01), .92, ZC); S.add(sill);
      // longitudinal bench: rounded seat/back profile extruded along the carriage
      const sh = new T.Shape(); sh.moveTo(0, 0); sh.lineTo(.47, 0); sh.lineTo(.47, .4); sh.quadraticCurveTo(.47, .47, .4, .47); sh.lineTo(.12, .47); sh.lineTo(.06, .95); sh.quadraticCurveTo(.03, 1, 0, .98); sh.lineTo(0, 0);
      for (let z = Z0 - 1; z > Z1 + 1; z -= 5.2) {
        const bg = new T.ExtrudeGeometry(sh, { depth: 3.6, bevelEnabled: true, bevelThickness: .03, bevelSize: .03, bevelSegments: 3, curveSegments: 8 });
        const b = new T.Mesh(bg, seatM); b.rotation.y = sd > 0 ? Math.PI : 0; b.position.set(sd * (HW - .02), 0, sd > 0 ? z : z - 3.6); S.add(b);
        const pole = new T.Mesh(new T.CylinderGeometry(.02, .02, 1.95, 16), trimM); pole.position.set(sd * (HW - .5), .98, z + .15); S.add(pole);
      }
      // overhead rail + straps
      const rail = new T.Mesh(new T.CylinderGeometry(.018, .018, LEN, 12), trimM); rail.rotation.x = Math.PI / 2; rail.position.set(sd * .72, 1.97, ZC); S.add(rail);
    });
    const NS = 60, strapM = new T.MeshStandardMaterial({ color: '#d8d2c4', roughness: .45, metalness: .1 }), strapG = new T.BoxGeometry(.03, .2, .008); strapG.translate(0, -.1, 0);
    const ringG = new T.TorusGeometry(.05, .009, 8, 24); ringG.translate(0, -.27, 0);
    const straps = new T.InstancedMesh(strapG, strapM, NS), rings = new T.InstancedMesh(ringG, strapM, NS); S.add(straps, rings);
    const SPOS = []; for (let i = 0; i < NS; i++) SPOS.push([(i % 2 ? 1 : -1) * .72, 1.96, Z0 - .3 - Math.floor(i / 2) * .78]);
    // ceiling: curved panel, warm light strips, practical lights
    const ceil = new T.Mesh(new T.CylinderGeometry(HW + .1, HW + .1, LEN, 40, 1, true, -Math.PI / 2, Math.PI), new T.MeshLambertMaterial({ color: '#2d2c38', side: T.BackSide }));
    ceil.rotation.x = Math.PI / 2; ceil.scale.set(1, 1, .28); ceil.position.set(0, 2.2, ZC); S.add(ceil);
    const roof = new T.Mesh(new T.BoxGeometry(HW * 2 + .3, .06, LEN), new T.MeshLambertMaterial({ color: '#24232c' })); roof.position.set(0, 2.52, ZC); S.add(roof);
    const stripM = new T.MeshBasicMaterial({ color: new T.Color('#ffd49a').multiplyScalar(.5) });
    [-1, 1].forEach(sd => { const s = new T.Mesh(new T.BoxGeometry(.07, .02, LEN), stripM); s.position.set(sd * .5, 2.44, ZC); S.add(s);
      const hs = new T.Mesh(new T.BoxGeometry(.2, .05, LEN), new T.MeshStandardMaterial({ color: '#1c1a22', metalness: .5, roughness: .55 })); hs.position.set(sd * .5, 2.47, ZC); S.add(hs); });
    S.add(new T.HemisphereLight('#6a7390', '#0d0d14', .9));   // cool neutral fill (not violet): backs stay readable
    // ceiling lights sit just AHEAD of the nearest passengers: their backs get the cool fill, shoulders and heads the warm edge
    [-1.3, -7, -13].forEach((z, i) => { const L = new T.PointLight('#ffc98a', 7, 10, 1.5); L.position.set(0, 2.25, z); S.add(L); });
    const winL = new T.DirectionalLight('#7f8cff', .35); winL.position.set(4, 1.5, -2); S.add(winL);
    // far end: connecting door with warm light beyond
    const endW = new T.Mesh(new T.BoxGeometry(HW * 2, 2.5, .1), wallM); endW.position.set(0, 1.25, Z1); S.add(endW);
    const door = new T.Mesh(new T.PlaneGeometry(.7, 1.25), new T.MeshBasicMaterial({ color: new T.Color('#ffcf94').multiplyScalar(1.3), fog: false })); door.position.set(0, 1.45, Z1 + .06); S.add(door);
    const dg = ctx.glow(S, '#ffb870', 4, .35); dg.position.set(0, 1.45, Z1 + .3);
    // dust in the light
    const dust = K.snow(S, { n: 900, box: [2.6, 2.2, 16], size: .02, opacity: .5, color: '#ffe0b8', fall: .03, center: [0, 1.2, -6] });
    // passengers
    // rim from the warm light ahead (ceiling strips + the lit door at the far end): world direction forward and up
    const lit = rimLight(T), LW = new T.Vector3(0, .55, -1).normalize();
    const r = rng(41), pick = (q, a) => a[(q() * a.length) | 0];
    const TOPS = ['#2b2c30', '#232a3a', '#5e4b38', '#3a3d31', '#43272b', '#47484d', '#18181b', '#6e604d', '#22302a', '#34303a', '#2e3644'];
    const HOOD = ['#3d3f45', '#1d2230', '#4a3d36', '#2c3a33', '#55545a'];
    const LOWS = ['#232b40', '#19191c', '#38383d', '#4b4537', '#2a2d33', '#1f2533'];
    const HAIRC = ['#100c0a', '#1f150f', '#34251a', '#0b0b0d', '#5d5853', '#2a1a12', '#151110'];
    const SKIN = ['#8a6a56', '#6e5243', '#a08068', '#4e3a30', '#7d5e4c'];
    const BAGS = ['#1b1d22', '#3a2f28', '#283241', '#4a4038'], HATS = ['#26262b', '#4a2628', '#2f3a48', '#5b5248'];
    // seeded outfit per passenger (seated: short jackets/hoodies only, so nothing pokes through the bench)
    function outfit(i, sit) { const q = rng(1 + Math.floor((Math.sin(i * 91.37 + 4.1) * .5 + .5) * 2e9)); q();
      const top = sit ? pick(q, ['jacket', 'hoodie', 'jacket', 'parka']) : pick(q, ['coat', 'coat', 'jacket', 'jacket', 'hoodie', 'parka', 'coat']);
      const hair = pick(q, ['short', 'short', 'short', 'long', 'bun', 'pony', 'cap', 'beanie', 'long', 'short']);
      const hood = top === 'hoodie' || top === 'parka', skirt = !sit && top === 'jacket' && (hair === 'long' || hair === 'bun' || hair === 'pony') && q() < .6;
      const bag = null;   // no backpacks/slings (user 2026-10-15: "something strange on their backs")
      const hem = top === 'coat' ? .5 + q() * .12 : top === 'parka' ? (sit ? .8 : .68 + q() * .06) : top === 'jacket' ? .8 + q() * .04 : .82;
      const bulk = top === 'parka' ? 1.12 : top === 'coat' ? 1.03 + q() * .05 : .96 + q() * .08;
      return { seed: i * 7 + 3, top, hair, hood, skirt, skirtHem: .5 + q() * .1, bag, hem, bulk, sit, collar: !hood, glove: q() < .15,
        cols: { top: top === 'hoodie' ? pick(q, HOOD) : pick(q, TOPS), low: pick(q, LOWS), hair: pick(q, HAIRC), skin: pick(q, SKIN), shoe: pick(q, ['#141416', '#2a1f19', '#1c1c20']), bag: pick(q, BAGS), hat: pick(q, HATS) } }; }
    const PEOPLE = [
      // x, z, rotY, scale, kind  (rail: right hand on the rail, railL: left hand, phone, pole, sit)
      [.3, -.4, .05, 1.02, 'rail'], [-.35, -1.6, -.1, .97, 'phone'], [.45, -2.9, .1, 1.05, 'rail'], [-.15, -3.9, 0, .94, 'railL'], [.2, -5.3, -.05, 1.0, 'rail'],
      [-.45, -6.1, .1, 1.04, 'rail'], [.35, -7.4, 0, .96, 'phone'], [-.1, -8.6, .05, 1.0, 'rail'], [.45, -9.8, 0, 1.03, 'rail'], [-.35, -11.0, 0, .98, 'rail'],
      [.15, -12.4, 0, 1.0, 'phone'], [-.3, -13.7, 0, 1.02, 'rail'], [.4, -14.8, 0, .97, 'rail'],
      [-1.12, -2.4, Math.PI / 2, .98, 'sit'], [1.12, -4.6, -Math.PI / 2, 1.0, 'sit'], [-1.12, -7.9, Math.PI / 2, 1.02, 'sit'], [1.12, -10.4, -Math.PI / 2, .96, 'sit'], [-1.12, -12.8, Math.PI / 2, 1.0, 'sit']];
    // look of the never-eat-human-meat people (user 2026-10-15): one matte slate-navy material for everyone (no per-garment colours,
    // no fabric texture), the clothes only as silhouette, a warm rim on the light-facing edges, a soft cool fill from the camera side
    const pplM = personMat(T, '#3c4058', '#ffc98a', 1.1, .75, lit); pplM.vertexColors = false;
    const pplFill = new T.DirectionalLight('#b4bed2', .45); pplFill.position.set(1.5, 3, 9); S.add(pplFill);
    const ppl = PEOPLE.map(([x, z, ry, sc, kind], i) => { const of = outfit(i, kind === 'sit'), mat = pplM;
      const pr = person(T, mat, dressedGeo(T, of)); pr.root.position.set(x, 0, z); pr.root.rotation.y = ry; pr.root.scale.set(sc * (.95 + r() * .1), sc, sc); S.add(pr.root);
      // natural idle: weight on one leg (hip tilt + relaxed knee), head down/turned, one shoulder higher, own sway amplitude/phase
      const q = rng(7 + Math.floor((Math.sin(i * 47.91 + 1.3) * .5 + .5) * 2e9)); q(); const side = q() < .5 ? 1 : -1;
      return { pr, x, kind, ph: r() * 6.28, rate: .7 + r() * .4, sc, hip: side * (.03 + q() * .035), knee: -side * (.12 + q() * .14), look: -(.1 + q() * .22), turn: (q() - .5) * .5,
        tilt: (q() - .5) * .12, shrug: (q() - .5) * .07, slump: -(.03 + q() * .09), amp: .6 + q() * .8, ph2: q() * 6.28 }; });
    const cam = new T.PerspectiveCamera(42, ctx.W / ctx.H, .05, 120); ctx.side(cam, p.side == null ? .1 : p.side);
    const M4 = new T.Matrix4(), Q = new T.Quaternion(), V = new T.Vector3(), One = new T.Vector3(1, 1, 1), Eu = new T.Euler();
    return { scene: S, camera: cam, draw(t, u) {
      // train motion: gentle lateral rock and small bumps (functions of t only)
      const rock = .035 * Math.sin(t * 1.3) + .015 * Math.sin(t * 3.1 + 1), bump = .006 * Math.sin(t * 7.3) * Math.sin(t * 1.7);
      city.offset.x = t * .55;   // outside streams past
      for (let i = 0; i < NS; i++) { const [x, y, z] = SPOS[i], sw = rock * 2.4 + .05 * Math.sin(t * 1.9 + i * .7); Eu.set(.04 * Math.sin(t * 1.4 + i), 0, sw); Q.setFromEuler(Eu); V.set(x, y, z); M4.compose(V, Q, One); straps.setMatrixAt(i, M4); rings.setMatrixAt(i, M4); }
      straps.instanceMatrix.needsUpdate = rings.instanceMatrix.needsUpdate = true;
      ppl.forEach(({ pr, x, kind, ph, rate, hip, knee, look, turn, tilt, shrug, slump, amp, ph2 }) => { const br = Math.sin(t * 1.6 * rate + ph), sway = (-rock * .9 + .01 * Math.sin(t * .9 + ph)) * amp;
        const o = { breath: br, sway, hip: hip * (1 + .15 * Math.sin(t * .25 + ph2)), knee, look: look + .04 * Math.sin(t * .3 + ph), turn: turn + .05 * Math.sin(t * .21 + ph2), tilt, shrug, slump };
        if (kind === 'rail') { const out = (x > 0 ? .72 - x : -.72 - x); o.r = [2.65 + .05 * Math.sin(t * 1.3 + ph), Math.max(-.3, Math.min(.5, out * 1.1)), .45 + .05 * br, .2]; o.l = [.08 + .04 * amp, .02, .15 + .1 * amp, 0]; o.shrug = shrug + .04; }
        else if (kind === 'railL') { const out = (x > 0 ? x - .72 : -.72 - x); o.l = [2.65 + .05 * Math.sin(t * 1.3 + ph), Math.max(-.3, Math.min(.5, -out * 1.1 + .1)), .45, .2]; o.r = [.06, .02, .12, 0]; o.shrug = shrug - .04; }
        else if (kind === 'phone') { o.r = [.55, -.12, 1.55 + .04 * Math.sin(t * .8 + ph), .1]; o.l = [.35, -.1, 1.3, 0]; o.look = -.5 + .03 * Math.sin(t * .4 + ph); o.turn = turn * .3; o.slump = slump - .05; }
        else if (kind === 'sit') { o.sit = 1; o.hip = 0; o.knee = 0; o.sway = -rock * .3 * amp; o.lean = .1; o.slump = slump - .1; o.r = [.9, -.15, .9, 0]; o.l = [.9, -.15, .9, 0]; o.look = -.3 + look * .5; }
        pr.pose(o); });
      dust.update(t, [0, 1.2, -6]);
      const cz = 3.3 - u * .32;
      cam.position.set(.12 + rock * .4, 1.52 + bump, cz); cam.lookAt(.05 + rock * .2, 1.38, cz - 12); cam.rotation.z += rock * .12;
      aimRim(lit, cam, LW);
    } };
  };

  // ---------------- lhcrowd ----------------
  M.scenes.lhcrowd = function (ctx, p) {
    const { T, sm, rng, cue } = ctx, K = M.kit, S = new T.Scene();
    S.add(dome(T, '#0a0b22', '#1c1846', '#04040c')); S.fog = new T.FogExp2('#0d0c26', .028);
    const ACC = new T.Color(ctx.ACC), COOL = new T.Color('#8fb4ff');
    // floor: dark polished stone with faint tiles
    const ft = ctx.ctex(512, (g, z) => { g.fillStyle = '#0c0d1c'; g.fillRect(0, 0, z, z); g.drawImage(K.noise(256, { seed: 8, octaves: 4 }), 0, 0, z, z); g.fillStyle = 'rgba(8,9,22,.82)'; g.fillRect(0, 0, z, z);
      g.strokeStyle = 'rgba(150,160,255,.10)'; g.lineWidth = 2; g.strokeRect(1, 1, z - 2, z - 2); });
    ft.wrapS = ft.wrapT = T.RepeatWrapping; ft.repeat.set(60, 60); ft.anisotropy = ctx.R.capabilities.getMaxAnisotropy();
    // unlit floor (lighting baked into vertex colours: a cool sheen toward the backlit horizon, darker at the camera) — a lit
    // full-screen floor cost more than all 100 people in the software renderer
    const fg = new T.PlaneGeometry(130, 130, 64, 64); fg.rotateX(-Math.PI / 2); const fcol = [], fp = fg.attributes.position;
    for (let i = 0; i < fp.count; i++) { const x = fp.getX(i), z = fp.getZ(i) - 10, d = Math.hypot((x - 1) * .8, (z + 16) * .55);
      const k = .22 + .9 * Math.exp(-d * d / 160) + .2 * Math.exp(-(x * x + (z + 5.5) ** 2) / 60); fcol.push(.7 * k, .75 * k, 1.2 * k); }
    fg.setAttribute('color', new T.Float32BufferAttribute(fcol, 3));
    const floor = new T.Mesh(fg, new T.MeshBasicMaterial({ map: ft, vertexColors: true })); floor.position.z = -10; S.add(floor);
    S.add(new T.HemisphereLight('#6c7896', '#0a0a12', 3.0));   // cool neutral fill (not violet)
    const back = new T.DirectionalLight('#9aa8ff', 1.25); back.position.set(-3, 9, -22); S.add(back);
    // cool neutral fill from the camera side: form stays readable
    const fill = new T.DirectionalLight('#b4bed2', 1.4); fill.position.set(6, 5, 14); S.add(fill);
    const horizon = ctx.glow(S, '#5a4fc0', 60, .22); horizon.position.set(4, 2, -55);
    const horizon2 = ctx.glow(S, '#2a3a9a', 120, .25); horizon2.position.set(-20, -4, -70);
    ctx.stars(S, 1200, 300, { size: .8, seed: 19, opacity: .5 });
    // 10 rows x 10; one left-hander per row
    const r = rng(77), NR = 10, NC = 10, DX = 1.05, DZ = 1.3, cols = ['#4c5368', '#555068', '#475668', '#5a5668', '#50505c', '#574d56'];   // mid-dark cloth so the cool fill shows form
    // rims only on the edges facing the backlight over the horizon (direction of `back`)
    const lit = rimLight(T), LW = back.position.clone().normalize();
    const coolM = cols.map(c => personMat(T, c, '#7fa6ff', .55, null, lit));
    const hairM = personMat(T, '#121218', '#8fb0ff', .6, .6, lit);
    const leftM = personMat(T, '#3a3442', '#7fa6ff', .55, null, lit), leftHair = personMat(T, '#16131a', '#8fb0ff', .6, .6, lit);
    const LEFTCOL = []; for (let k = 0; k < NR; k++) LEFTCOL.push(1 + ((r() * 8) | 0));
    const crowd = [];
    for (let row = 0; row < NR; row++) for (let c = 0; c < NC; c++) {
      const left = LEFTCOL[row] === c, pr = person(T, left ? leftM : coolM[(r() * coolM.length) | 0]);
      const x = (c - (NC - 1) / 2) * DX + (r() - .5) * .22, z = -row * DZ + (r() - .5) * .25, sc = .93 + r() * .14;
      pr.root.position.set(x, 0, z); pr.root.rotation.y = (r() - .5) * .25; pr.root.scale.set(sc * (.94 + r() * .12), sc, sc); S.add(pr.root);
      crowd.push({ pr, left, row, c, x, z, sc, ph: r() * 6.28, d: r(), hi: r() });
    }
    // light pools on the floor (cool for everyone, warm under the left-handers) and halos
    const poolT = ctx.ctex(128, (g, z) => { const gr = g.createRadialGradient(z / 2, z / 2, 0, z / 2, z / 2, z / 2); gr.addColorStop(0, 'rgba(255,255,255,.9)'); gr.addColorStop(.35, 'rgba(255,255,255,.35)'); gr.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = gr; g.fillRect(0, 0, z, z); });
    const pools = crowd.map(cr => { if (!cr.left) return null; const m = new T.Mesh(new T.PlaneGeometry(1, 1), new T.MeshBasicMaterial({ map: poolT, color: cr.left ? ACC : COOL, transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false }));
      m.rotation.x = -Math.PI / 2; m.position.set(cr.x, .01, cr.z); m.scale.setScalar(cr.left ? 2.4 : 1.1); S.add(m); return m; });
    const halos = crowd.filter(cr => cr.left).map(cr => { const h = ctx.glow(S, ctx.ACC, 3.2, 0); h.position.set(cr.x, 1.2 * cr.sc, cr.z - .05); return h; });
    // hand lights: one point per person at the raised wrist
    const hp = ctx.points(NR * NC, { size: .32, color: '#ffffff' }), ha = hp.geometry.attributes.position.array, hc = hp.geometry.attributes.color.array; S.add(hp);
    const hg = ctx.points(NR * NC, { size: .85, opacity: .6, color: '#ffffff' }), hga = hg.geometry.attributes.position.array, hgc = hg.geometry.attributes.color.array; S.add(hg);
    const dust = K.snow(S, { n: 1800, box: [26, 8, 26], size: .05, opacity: .45, color: '#b9c4ff', fall: .05, center: [0, 3, -6] });
    const warmDust = ctx.points(400, { size: .07, opacity: .9, color: ctx.ACC }), wda = warmDust.geometry.attributes.position.array, wdc = warmDust.geometry.attributes.color.array; S.add(warmDust);
    const wr = rng(5), WD = []; for (let i = 0; i < 400; i++) WD.push([(wr() * NR) | 0, wr() * 6.28, .2 + wr() * .6, wr()]);
    const cam = new T.PerspectiveCamera(36, ctx.W / ctx.H, .1, 600); ctx.side(cam, p.side == null ? .12 : p.side);
    const tR = cue(p.right, ctx.t0 + .6), tL = cue(p.left, ctx.t0 + 6), tS = cue(p.share, tL + 2), V = new T.Vector3(), dur = Math.max(1, ctx.t1 - ctx.t0);
    const leftCrowd = crowd.filter(c => c.left);
    return { scene: S, camera: cam, draw(t, u) {
      const lift = sm(tL, tL + 1.0, t), share = sm(tS, tS + 1.5, t), rightOn = sm(tR, tR + 3, t);
      crowd.forEach((cr, i) => { const br = Math.sin(t * 1.5 + cr.ph);
        const o = { breath: br, sway: .01 * Math.sin(t * .6 + cr.ph), look: .03 * Math.sin(t * .4 + cr.ph * 2) };
        if (!cr.left) { const t0 = tR + .1 + (NR - 1 - cr.row) * .17 + cr.d * .5, a = sm(t0, t0 + .9, t) * (1 - share * .12);
          o.r = [a * (2.45 + cr.hi * .45), a * (.12 + cr.hi * .15), a * (.25 + (1 - cr.hi) * .5), a * .3]; o.l = [0, .02, .08, 0]; }
        else { const t0 = tL + cr.d * .35, a = sm(t0, t0 + .8, t); o.l = [a * 2.75, a * .18, a * .28, a * .3]; o.r = [0, .02, .08, 0]; o.look = .03 + .06 * a; }
        cr.pr.pose(o); });
      S.updateMatrixWorld(true);
      crowd.forEach((cr, i) => { cr.pr.bones[cr.left ? 9 : 6].getWorldPosition(V); V.y -= .1 * cr.sc;
        ha.set([V.x, V.y, V.z], i * 3); hga.set([V.x, V.y, V.z], i * 3);
        let k, col;
        if (!cr.left) { const t0 = tR + .1 + (NR - 1 - cr.row) * .17 + cr.d * .5; k = sm(t0 + .3, t0 + 1.1, t) * (1 - share * .45); col = COOL; }
        else { k = sm(tL + .2, tL + 1.2, t) * (1.3 + .4 * share); col = ACC; }
        hc.set([col.r * k, col.g * k, col.b * k], i * 3); hgc.set([col.r * k * .6, col.g * k * .6, col.b * k * .6], i * 3);
        if (pools[i]) pools[i].material.opacity = lift * (.5 + .25 * share); });
      hp.geometry.attributes.position.needsUpdate = hp.geometry.attributes.color.needsUpdate = hg.geometry.attributes.position.needsUpdate = hg.geometry.attributes.color.needsUpdate = true;
      // materials: cool rim grows with the raised right hands, then dims; the left-handers take the warm accent
      coolM.forEach(m => { m.userData.rimK.value = .95 + .6 * rightOn - .55 * share; });
      hairM.userData.rimK.value = 1 + .5 * rightOn - .5 * share;
      leftM.userData.rimC.value.copy(new T.Color('#7fa6ff')).lerp(ACC, lift); leftM.userData.rimK.value = .95 + lift * (1.8 + .8 * share);
      leftM.emissive.copy(ACC).multiplyScalar(lift * (.22 + .12 * share));
      leftHair.userData.rimC.value.copy(new T.Color('#8fb0ff')).lerp(ACC, lift); leftHair.userData.rimK.value = .6 + lift * 1.8;
      halos.forEach((h, k) => { h.material.opacity = lift * (.28 + .14 * share) * (.9 + .1 * Math.sin(t * 2 + k)); });
      for (let i = 0; i < 400; i++) { const [row, a0, rr, o] = WD[i], cr = leftCrowd[row], a = a0 + t * (.3 + o * .4), y = ((o * 2.6 + t * .25 * (.5 + o)) % 2.6);
        wda.set([cr.x + Math.cos(a) * rr, y, cr.z + Math.sin(a) * rr], i * 3); const k = lift * (1 - y / 2.6) * .9; wdc.set([k, k, k], i * 3); }
      warmDust.geometry.attributes.position.needsUpdate = warmDust.geometry.attributes.color.needsUpdate = true;
      dust.update(t, [0, 3, -6]);
      // camera: behind and above the crowd, slow drift; leans in a little toward the field when the left-handers appear
      const k = sm(0, dur, u), ca = .2 - .1 * k, cd = 15.5 - 1.5 * k - 1.0 * lift, ch = 5.4 + .6 * k;
      cam.position.set(Math.sin(ca) * cd, ch, -5.8 + Math.cos(ca) * cd); cam.lookAt(0, 1.1, -5.6);
      aimRim(lit, cam, LW);
    } };
  };

  // ---------------- lhglobe ----------------
  // rough continent outlines [lon, lat] (symbolic shapes, enough to read the continents from far away)
  const LAND = {
    namerica: [[-168, 66], [-162, 70], [-140, 70], [-125, 70], [-95, 72], [-80, 73], [-65, 62], [-60, 55], [-53, 47], [-66, 44], [-70, 41], [-76, 35], [-81, 31], [-80, 25], [-82, 28], [-84, 30], [-90, 29], [-97, 27], [-97, 22], [-92, 19], [-87, 21], [-88, 16], [-83, 10], [-79, 9], [-78, 7], [-80, 8], [-85, 11], [-92, 14], [-100, 17], [-106, 23], [-112, 29], [-110, 23], [-115, 30], [-118, 34], [-124, 40], [-124, 48], [-130, 55], [-140, 60], [-150, 60], [-158, 57], [-165, 60]],
    greenland: [[-50, 60], [-42, 60], [-20, 70], [-18, 80], [-35, 83], [-60, 82], [-70, 77], [-55, 70]],
    samerica: [[-78, 8], [-72, 12], [-62, 11], [-52, 5], [-35, -5], [-38, -13], [-40, -22], [-48, -26], [-53, -34], [-58, -38], [-65, -42], [-68, -50], [-70, -55], [-74, -52], [-74, -42], [-72, -30], [-70, -18], [-76, -14], [-81, -5], [-80, 0], [-77, 4]],
    europe: [[-9, 37], [-9, 43], [-2, 43], [-4, 48], [2, 51], [8, 54], [8, 57], [5, 59], [5, 62], [14, 67], [20, 70], [30, 70], [40, 67], [45, 68], [60, 68], [60, 55], [50, 47], [40, 47], [36, 45], [30, 46], [28, 41], [23, 40], [22, 37], [19, 40], [16, 38], [18, 40], [13, 44], [12, 45], [8, 44], [3, 43], [0, 39], [-5, 36]],
    uk: [[-5, 50], [1, 51], [2, 53], [-1, 55], [-2, 58], [-5, 58], [-6, 55], [-3, 54], [-5, 52]], ireland: [[-10, 52], [-6, 52], [-6, 55], [-9, 55]], iceland: [[-24, 64], [-14, 64], [-14, 66], [-22, 66]],
    africa: [[-17, 15], [-17, 21], [-13, 28], [-6, 36], [10, 37], [11, 33], [20, 31], [32, 31], [35, 28], [43, 12], [51, 12], [44, 0], [40, -10], [40, -16], [35, -24], [32, -29], [27, -34], [20, -35], [18, -32], [12, -18], [13, -8], [9, -1], [9, 4], [4, 6], [-4, 5], [-8, 4], [-13, 8], [-16, 12]],
    madagascar: [[44, -25], [47, -25], [50, -15], [49, -12], [44, -17]],
    asia: [[26, 40], [36, 36], [35, 32], [34, 28], [39, 22], [43, 13], [52, 16], [57, 22], [57, 25], [50, 30], [56, 27], [62, 25], [67, 24], [73, 21], [77, 8], [80, 13], [80, 16], [87, 22], [92, 22], [94, 17], [98, 16], [98, 8], [101, 3], [104, 1], [103, 8], [105, 9], [109, 12], [108, 21], [118, 24], [122, 30], [121, 37], [118, 38], [122, 40], [126, 38], [129, 35], [129, 42], [135, 44], [141, 52], [141, 59], [150, 59], [160, 61], [164, 60], [163, 56], [156, 51], [160, 60], [178, 64], [180, 66], [180, 69], [160, 70], [140, 72], [113, 74], [100, 78], [80, 73], [70, 73], [66, 70], [60, 68], [60, 55], [50, 47], [45, 42], [42, 41]],
    japan: [[130, 31], [132, 34], [135, 34], [140, 35], [142, 40], [141, 45], [145, 44], [141, 42], [140, 38], [137, 37], [133, 36], [130, 34]],
    sumatra: [[95, 5], [98, 4], [106, -6], [104, -6], [96, 2]], borneo: [[109, 1], [110, -3], [116, -4], [119, 1], [117, 7], [113, 3]], java: [[106, -6], [115, -8], [114, -8.8], [105, -7]],
    guinea: [[131, -1], [138, -2], [147, -6], [150, -10], [142, -9], [138, -8], [132, -4]], philippines: [[120, 18], [122, 18], [124, 12], [126, 7], [122, 7], [120, 14]],
    australia: [[114, -22], [114, -34], [118, -35], [124, -34], [130, -31], [135, -35], [138, -35], [141, -38], [147, -38], [150, -37], [153, -28], [153, -25], [146, -19], [142, -11], [141, -15], [136, -12], [132, -11], [129, -15], [123, -17], [119, -20]],
    tasmania: [[145, -41], [148, -41], [147, -43.5], [145, -43]], nzn: [[172, -34], [175, -37], [178, -38], [175, -41], [173, -40]], nzs: [[174, -41], [171, -44], [167, -46], [169, -46.5], [173, -43]],
  };
  const INHABITED = { namerica: 1, samerica: 1, europe: 1, uk: 1, ireland: 1, africa: 1, madagascar: 1, asia: 1, japan: 1, sumatra: 1, borneo: 1, java: 1, guinea: 1, philippines: 1, australia: 1, tasmania: 1, nzn: 1, nzs: 1 };
  function inPoly(lo, la, P) { let c = false; for (let i = 0, j = P.length - 1; i < P.length; j = i++) { const [xi, yi] = P[i], [xj, yj] = P[j]; if ((yi > la) !== (yj > la) && lo < (xj - xi) * (la - yi) / (yj - yi) + xi) c = !c; } return c; }
  function landOf(lo, la) { if (la < -70) return 'antarctica'; for (const k in LAND) if (inPoly(lo, la, LAND[k])) return k; return null; }

  M.scenes.lhglobe = function (ctx, p) {
    const { T, sm, rng, cue } = ctx, S = new T.Scene(), RAD = 6;
    S.add(dome(T, '#0b0a26', '#14123a', '#050512'));
    ctx.stars(S, 2600, 300, { size: .7, seed: 23 });
    const G = new T.Group(); S.add(G);
    // ocean body: dark solid sphere (hides the far side) + atmosphere rim
    const ocean = new T.Mesh(new T.SphereGeometry(RAD, 96, 64), new T.MeshStandardMaterial({ color: '#070a1e', roughness: .55, metalness: .3, envMap: ctx.env(), envMapIntensity: .25 })); G.add(ocean);
    const atmo = new T.Mesh(new T.SphereGeometry(RAD * 1.035, 64, 48), new T.ShaderMaterial({ transparent: true, blending: T.AdditiveBlending, depthWrite: false, side: T.BackSide,
      uniforms: { c: { value: new T.Color('#4c5ad0') } },
      vertexShader: 'varying vec3 vN; varying vec3 vV; void main(){ vN=normalize(normalMatrix*normal); vec4 mv=modelViewMatrix*vec4(position,1.); vV=normalize(-mv.xyz); gl_Position=projectionMatrix*mv; }',
      fragmentShader: 'uniform vec3 c; varying vec3 vN; varying vec3 vV; void main(){ float f=pow(clamp(1.0-abs(dot(vN,vV))*1.0,0.,1.),1.5); float r=smoothstep(0.,.35,abs(dot(vN,vV))); gl_FragColor=vec4(c*f*r*.75,1.); }' }));
    S.add(atmo);
    const inner = new T.Mesh(new T.SphereGeometry(RAD * 1.002, 96, 64), new T.ShaderMaterial({ transparent: true, blending: T.AdditiveBlending, depthWrite: false,
      vertexShader: 'varying vec3 vN; varying vec3 vV; void main(){ vN=normalize(normalMatrix*normal); vec4 mv=modelViewMatrix*vec4(position,1.); vV=normalize(-mv.xyz); gl_Position=projectionMatrix*mv; }',
      fragmentShader: 'varying vec3 vN; varying vec3 vV; void main(){ float f=pow(1.0-clamp(dot(vN,vV),0.,1.),3.); gl_FragColor=vec4(vec3(.25,.3,.9)*f*.9,1.); }' }));
    G.add(inner);
    const sun = new T.DirectionalLight('#aab4ff', .9); sun.position.set(-20, 10, 12); S.add(sun); S.add(new T.AmbientLight('#1a1c44', .4));
    // land points: Fibonacci sphere, kept where the rough outlines say land
    const NF = 42000, land = [], warm = [], r = rng(31), gold = Math.PI * (3 - Math.sqrt(5));
    for (let i = 0; i < NF; i++) { const y = 1 - (i + .5) / NF * 2, q = Math.sqrt(1 - y * y), a = i * gold; const x = Math.cos(a) * q, z = Math.sin(a) * q;
      const la = Math.asin(y) * 180 / Math.PI, lo = Math.atan2(-z, x) * 180 / Math.PI, k = landOf(lo, la);
      if (k) { land.push([x, y, z, k]); if (INHABITED[k] && r() < .085) warm.push([x, y, z, lo, r()]); } }
    const lp = ctx.points(land.length, { size: .085, opacity: .9, color: '#b8c4ff' }), la = lp.geometry.attributes.position.array, lc = lp.geometry.attributes.color.array;
    land.forEach(([x, y, z, k], i) => { la.set([x * RAD * 1.004, y * RAD * 1.004, z * RAD * 1.004], i * 3); const v = k === 'antarctica' || k === 'greenland' ? .3 : .5; lc.set([v, v, v], i * 3); });
    G.add(lp);
    const NW = warm.length, wp = ctx.points(NW, { size: .26, color: ctx.ACC }), wa = wp.geometry.attributes.position.array, wc = wp.geometry.attributes.color.array;
    const wh = ctx.points(NW, { size: 1.0, opacity: .45, color: ctx.ACC }), wha = wh.geometry.attributes.position.array, whc = wh.geometry.attributes.color.array;
    warm.forEach(([x, y, z], i) => { wa.set([x * RAD * 1.01, y * RAD * 1.01, z * RAD * 1.01], i * 3); wha.set([x * RAD * 1.012, y * RAD * 1.012, z * RAD * 1.012], i * 3); });
    G.add(wp, wh);
    // faint lat-long grid of dots on the ocean
    const gpts = []; for (let m = 0; m < 36; m++) for (let k = 1; k < 90; k++) { const a = m / 36 * 6.283, b = k / 90 * Math.PI; gpts.push([Math.sin(b) * Math.cos(a), Math.cos(b), Math.sin(b) * Math.sin(a)]); }
    const gp = ctx.points(gpts.length, { size: .04, opacity: .35, color: '#6f7cff' }); gpts.forEach((v, i) => gp.geometry.attributes.position.array.set([v[0] * RAD * 1.001, v[1] * RAD * 1.001, v[2] * RAD * 1.001], i * 3)); G.add(gp);
    const halo = ctx.glow(S, '#4b55d8', RAD * 4.2, .18);
    const cam = new T.PerspectiveCamera(36, ctx.W / ctx.H, .1, 900); ctx.side(cam, p.side == null ? .12 : p.side);
    const tT = cue(p.turn, ctx.t0 + 1), tE = cue(p.every, ctx.t0 + 3), dur = Math.max(1, ctx.t1 - ctx.t0);
    return { scene: S, camera: cam, draw(t, u) {
      // the Earth turns west -> east so the Americas, then Europe/Africa, then Asia/Australia pass the camera
      const rot = 1.6 - u * .5; G.rotation.set(.32, rot, 0);
      // warm points light up from `turn` to `every`, staggered by longitude so they bloom continent by continent
      for (let i = 0; i < NW; i++) { const [, , , lo, o] = warm[i]; const st = tT + ((lo + 170) / 350) * Math.max(.8, tE - tT + 1.2) + o * .5, k = sm(st, st + .6, t) * (.85 + .15 * Math.sin(t * 3 + o * 30));
        wc.set([k, k, k], i * 3); const h = k * (1 + .6 * Math.exp(-Math.max(0, t - st) * 2)); whc.set([h * .8, h * .8, h * .8], i * 3); }
      wp.geometry.attributes.color.needsUpdate = wh.geometry.attributes.color.needsUpdate = true;
      halo.material.opacity = .14 + .08 * sm(tE, tE + 2, t);
      const k = sm(0, dur, u), d = 28 + 6 * k;
      cam.position.set(Math.sin(.15) * d, 2.5 + 2 * k, Math.cos(.15) * d); cam.lookAt(0, -.9, 0);
    } };
  };
})();
