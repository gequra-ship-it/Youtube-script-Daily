// void (cosmic-prison-cine override of tools/cine/scenes/basic.js "void", 2026-10-16 third staging pass): the background behind the
// data cards, alive but calm. A deep star sphere turning slowly, a faint coloured nebula (fBm texture, two tints) breathing and
// drifting, ~70 small galaxies (face-on spirals, tilted spirals, edge-on discs, ellipticals) on three depth layers that slowly
// recede from the camera (a gentle continuous zoom-out with parallax: near layer faster, far layer slower), a fine dust layer
// drifting past. Every galaxy is a recycling particle: s = fract(u * rate + phase) -> distance, fade in near s = 0, fade out near
// s = 1, so nothing ever pops and any frame can be drawn alone (seek-safe). The middle of the frame (where the card text sits) is
// kept darker. The page also lays a 55% black dim over it while a card shows.
// params (same as the shared void): { bg:'#020309', tint:'#3b3a8c', stars:3000 }; optional: tint2 (second nebula colour,
//   default '#6a2a5e'), calm (0..1 scale of the motion, default 1)
(function () {
  const M = (window.MIYA = window.MIYA || { scenes: {} });
  M.scenes.void = function (ctx, p) {
    const { T, sm, rng } = ctx, S = new T.Scene(); S.background = new T.Color(p.bg || '#020309');
    const K = window.MIYA.kit, CALM = p.calm == null ? 1 : p.calm, VERT = ctx.VERT;
    const st = ctx.stars(S, p.stars || 3000, 200, { seed: 41, size: 1.1 });
    const st2 = ctx.stars(S, 900, 190, { seed: 43, size: 1.7, opacity: .55, color: '#fff2dc' });
    // nebula: one fBm canvas, coloured with the two tints, on two large far planes that drift and scale against each other
    const tA = new T.Color(p.tint || '#3b3a8c'), tB = new T.Color(p.tint2 || '#6a2a5e');
    const nebT = (() => { const n1 = K.noise(256, { seed: 12, octaves: 5 }), n2 = K.noise(256, { seed: 29, octaves: 4 }), c = document.createElement('canvas'); c.width = c.height = 256;
      const g = c.getContext('2d'), a = n1.getContext('2d').getImageData(0, 0, 256, 256).data, b = n2.getContext('2d').getImageData(0, 0, 256, 256).data, im = g.createImageData(256, 256);
      for (let y = 0; y < 256; y++) for (let x = 0; x < 256; x++) { const i = (y * 256 + x) * 4, dx = (x - 128) / 128, dy = (y - 128) / 128, rr = Math.min(1, Math.hypot(dx, dy));
        const e = Math.pow(Math.max(0, 1 - rr), 1.4), v = Math.pow(Math.max(0, a[i] / 255 - .35) / .65, 1.6) * e, w = Math.pow(Math.max(0, b[i] / 255 - .4) / .6, 1.3) * e;
        im.data[i] = Math.min(255, 255 * (v * tA.r * 2.2 + w * tB.r * 2.2)); im.data[i + 1] = Math.min(255, 255 * (v * tA.g * 2.2 + w * tB.g * 2.2)); im.data[i + 2] = Math.min(255, 255 * (v * tA.b * 2.2 + w * tB.b * 2.2)); im.data[i + 3] = 255; }
      g.putImageData(im, 0, 0); const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; return t; })();
    const nebM = o => new T.MeshBasicMaterial({ map: nebT, transparent: true, opacity: o, blending: T.AdditiveBlending, depthWrite: false, fog: false });
    const neb1 = new T.Mesh(new T.PlaneGeometry(330, 330), nebM(.55)), neb2 = new T.Mesh(new T.PlaneGeometry(260, 260), nebM(.35)); neb1.position.set(35, 8, -150); neb2.position.set(-60, -18, -165); neb2.rotation.z = 2.1; S.add(neb1, neb2);
    const glo = ctx.glow(S, p.tint || '#3b3a8c', 260, .3); glo.position.set(40, 10, -120);
    // galaxy sprites: four procedural types
    function galTex(kind, seed) { return ctx.ctex(128, (g, s) => { const r = rng(seed); g.translate(s / 2, s / 2);
      const halo = g.createRadialGradient(0, 0, 0, 0, 0, s / 2); halo.addColorStop(0, 'rgba(255,240,215,1)'); halo.addColorStop(kind === 2 ? .35 : .1, kind === 2 ? 'rgba(255,225,190,.45)' : 'rgba(255,232,205,.55)'); halo.addColorStop(kind === 2 ? .8 : .45, 'rgba(190,185,255,.08)'); halo.addColorStop(1, 'rgba(0,0,0,0)');
      g.fillStyle = halo; g.fillRect(-s / 2, -s / 2, s, s); if (kind === 2) return;
      if (kind === 3) { g.scale(1, .16); const d = g.createRadialGradient(0, 0, 0, 0, 0, s * .48); d.addColorStop(0, 'rgba(255,240,220,.9)'); d.addColorStop(.6, 'rgba(200,200,255,.25)'); d.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = d; g.fillRect(-s / 2, -s / 2, s, s); return; }
      for (let a = 0; a < 2; a++) for (let k = 0; k < 140; k++) { const f = k / 140, th = f * (kind === 1 ? 3.4 : 4.4) + a * Math.PI, rr = 5 + f * s * .4, w = (r() - .5) * 6 * (.4 + f);
        g.fillStyle = `rgba(${r() < .35 ? '255,215,190' : '185,200,255'},${.2 * (1 - f) + .06})`; g.beginPath(); g.arc(Math.cos(th) * rr + w, Math.sin(th) * rr + w, 1.2 + 2.4 * r() * (1 - f * .5), 0, 6.283); g.fill(); } }); }
    const texs = [galTex(0, 3), galTex(0, 7), galTex(1, 5), galTex(2, 9), galTex(3, 11)];
    // three depth layers: [count, distance near, distance far, rate (cycles per second), size]
    const LAY = [[14, 18, 70, .012, 3.4], [24, 30, 120, .008, 3.0], [34, 50, 170, .005, 2.6]], G = [], R = rng(57);
    LAY.forEach(([n, d0, d1, rate, sz], li) => { for (let k = 0; k < n; k++) {
      const ty = Math.floor(R() * texs.length), sp = new T.Sprite(new T.SpriteMaterial({ map: texs[ty], color: R() < .6 ? '#ffe6c8' : '#cdd4ff', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, fog: false, rotation: R() * 6.283 }));
      const s = sz * (.6 + .8 * R()); S.add(sp);
      G.push({ sp, li, d0, d1, rate: rate * (.85 + .3 * R()), ph: R(), x: R() * 2 - 1, y: R() * 2 - 1, s, sq: ty === 2 || ty === 4 ? 1 : .45 + .5 * R(), rot: (R() - .5) * .02, br: .35 + .5 * R() }); } });
    G.forEach(o => o.sp.scale.set(o.s, o.s * o.sq, 1));
    // dust: fine points drifting slowly past, recycled in depth like the galaxies
    const ND = 260, du = ctx.points(ND, { size: .9, opacity: 1, atten: false, color: '#ffffff' }), duA = du.geometry.attributes.position.array, duC = du.geometry.attributes.color.array, duB = [];
    { const r = rng(61); for (let i = 0; i < ND; i++) duB.push([r() * 2 - 1, r() * 2 - 1, r(), .02 + .02 * r()]); } du.frustumCulled = false; S.add(du);
    const cam = new T.PerspectiveCamera(50, ctx.W / ctx.H, .1, 600), th = Math.tan(25 * Math.PI / 180), asp = ctx.W / ctx.H, v = new T.Vector3();
    const look = new T.Vector3(), DRIFT = [.0065, .004, .0022];
    return { scene: S, camera: cam, draw(t, u) {
      const uu = u * CALM;
      // gentle camera: fixed position, a very slow pan; the look-at point keeps a constant distance (10)
      cam.position.set(0, 0, 0); look.set(Math.sin(uu * .01) * 10, Math.sin(uu * .006) * .8, -10 * Math.cos(uu * .01)); cam.lookAt(look);
      cam.updateMatrixWorld();
      st.rotation.y = uu * .004; st2.rotation.y = uu * .006; st2.rotation.x = uu * .002;
      // nebula: slow drift + scale (zoom-out: shrinking toward the far field), opacity breathes gently
      const zo = 1 / (1 + uu * .006);
      neb1.scale.setScalar(1.15 * zo); neb1.rotation.z = uu * .004; neb1.material.opacity = .95 * (.85 + .15 * Math.sin(t * .21));
      neb2.scale.setScalar(1.1 * (1 / (1 + uu * .004))); neb2.rotation.z = 2.1 - uu * .003; neb2.material.opacity = .62 * (.85 + .15 * Math.sin(t * .17 + 1.3));
      neb1.position.x = 35 - uu * .15; neb2.position.x = -60 + uu * .1;
      // galaxies: recede (distance from near to far), placed in the view cone of the camera's forward axis
      const fw = look.clone().normalize(), rt = new T.Vector3().crossVectors(fw, new T.Vector3(0, 1, 0)).normalize(), up = new T.Vector3().crossVectors(rt, fw);
      G.forEach(o => { const s = ((uu * o.rate + o.ph) % 1 + 1) % 1, d = o.d0 + (o.d1 - o.d0) * s;
        // parallax: each layer drifts sideways at its own speed (near fast, far slow), wrapped with a soft fade at the frame edges
        const ox = ((o.x + uu * DRIFT[o.li] + 1.25) % 2.5 + 2.5) % 2.5 - 1.25, edge = 1 - sm(1, 1.2, Math.abs(ox));
        const X = ox * 1.1 * th * asp * d, Y = o.y * 1.05 * th * d;
        v.copy(cam.position).addScaledVector(fw, d).addScaledVector(rt, X).addScaledVector(up, Y); o.sp.position.copy(v);
        // keep the card's middle darker: screen position of the galaxy (fixed per galaxy since it recedes along its own ray)
        const cx = Math.abs(ox * 1.1), cy = Math.abs(o.y * 1.05), mid = VERT ? 1 - .55 * (1 - sm(.55, .95, cx)) * (1 - sm(.6, .9, cy)) : 1 - .6 * (1 - sm(.45, .85, cx)) * (1 - sm(.55, .9, cy));
        o.sp.material.opacity = edge * o.br * sm(0, .18, s) * (1 - sm(.8, 1, s)) * mid * (o.li === 0 ? 2.1 : o.li === 1 ? 1.7 : 1.35);
        o.sp.material.rotation = o.ph * 6.283 + uu * o.rot; });
      // dust: also receding
      for (let i = 0; i < ND; i++) { const b = duB[i], s = ((uu * b[3] + b[2]) % 1 + 1) % 1, d = 4 + 40 * s;
        v.copy(cam.position).addScaledVector(fw, d).addScaledVector(rt, b[0] * th * asp * d).addScaledVector(up, b[1] * th * d);
        duA[i * 3] = v.x; duA[i * 3 + 1] = v.y; duA[i * 3 + 2] = v.z;
        const a = .9 * sm(0, .15, s) * (1 - sm(.7, 1, s)); duC[i * 3] = a * .8; duC[i * 3 + 1] = a * .85; duC[i * 3 + 2] = a; }
      du.geometry.attributes.position.needsUpdate = true; du.geometry.attributes.color.needsUpdate = true;
    } };
  };
})();
