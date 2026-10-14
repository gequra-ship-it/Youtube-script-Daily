// blackhole — four looks (guideline art_spec 11-10, 2026-10-14): 'lensed' (default: thick glowing disk + far side bent over the
// shadow), 'ring' (face-on ring like the 2019 M87* / 2022 Sgr A* images, brighter on one side), 'whirlpool' (gas spiralling in),
// 'icon' (small dark disc + thin ring, far away). Also exported as MIYA.lib.blackhole(ctx, look) for other scenes (ocean).
// params: { look:'lensed', side:.1, dist:30, approach:1 (camera push-in over the shot), tilt:.10, spin:.35, bg:'#02030a', stars:2500 }
(function () {
  const M = (window.MIYA = window.MIYA || { scenes: {} }); M.lib = M.lib || {};
  let _disk = {};
  function diskTex(ctx, sd) {
    if (_disk[sd]) return _disk[sd];
    return (_disk[sd] = ctx.ctex(1024, (g, s) => { const r0 = s / 2, rr = ctx.rng(sd);
      const grd = g.createRadialGradient(r0, r0, r0 * .3, r0, r0, r0); grd.addColorStop(0, 'rgba(255,246,220,0)'); grd.addColorStop(.02, 'rgba(255,246,220,1)'); grd.addColorStop(.18, 'rgba(255,198,90,.95)'); grd.addColorStop(.5, 'rgba(255,122,90,.55)'); grd.addColorStop(1, 'rgba(255,122,90,0)');
      g.fillStyle = grd; g.beginPath(); g.arc(r0, r0, r0, 0, 6.283); g.arc(r0, r0, r0 * .3, 0, 6.283, true); g.fill(); g.globalCompositeOperation = 'lighter';
      for (let i = 0; i < 420; i++) { const r = r0 * (.32 + .66 * Math.pow(rr(), 1.3)), a = rr() * 6.283, L = .3 + rr() * 1.2; g.strokeStyle = `rgba(255,${200 + rr() * 55 | 0},${150 + rr() * 90 | 0},${.05 + rr() * .12})`; g.lineWidth = 1 + rr() * 3; g.beginPath(); g.arc(r0, r0, r, a, a + L); g.stroke(); } }));
  }
  // returns {group, update(t, cam)}; the hole has radius 3 in group units
  M.lib.blackhole = function (ctx, look) {
    const { T } = ctx, G = new T.Group(); look = look || 'lensed';
    const hole = new T.Mesh(new T.SphereGeometry(3, 64, 48), new T.MeshBasicMaterial({ color: '#000', fog: false })); G.add(hole);
    const add = (m) => (G.add(m), m);
    const mb = (map, op) => new T.MeshBasicMaterial({ map, transparent: true, opacity: op == null ? 1 : op, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide, fog: false });
    let disk = null, lens = null, ring = null, swirl = null;
    const halo = ctx.glow(G, '#ffb070', look === 'icon' ? 14 : look === 'lensed' ? 40 : 30, look === 'icon' ? .25 : look === 'lensed' ? .42 : .22);
    if (look === 'lensed') { disk = add(new T.Mesh(new T.RingGeometry(3.4, 13, 256, 1), mb(diskTex(ctx, 7)))); lens = add(new T.Mesh(new T.RingGeometry(3.25, 6.2, 256, 1), mb(diskTex(ctx, 11), .9))); }
    if (look === 'ring') { const tex = ctx.ctex(512, (g, s) => { const c = s / 2; const gr = g.createLinearGradient(0, 0, s * .35, s); gr.addColorStop(0, 'rgba(255,122,90,.45)'); gr.addColorStop(.55, 'rgba(255,198,90,1)'); gr.addColorStop(1, 'rgba(255,246,220,1)');
        g.strokeStyle = gr; for (let w = 90; w > 6; w -= 12) { g.globalAlpha = .12 + (90 - w) / 120; g.lineWidth = w; g.beginPath(); g.arc(c, c, s * .33, 0, 6.283); g.stroke(); } });
      ring = add(new T.Mesh(new T.PlaneGeometry(19, 19), mb(tex, .75))); }
    if (look === 'whirlpool') { const tex = ctx.ctex(1024, (g, s) => { const c = s / 2, rr = ctx.rng(21); g.globalCompositeOperation = 'lighter';
        for (let arm = 0; arm < 5; arm++) for (let k = 0; k < 160; k++) { const t = k / 159, r = s * (.48 - .33 * t), a = arm * 1.2566 + t * 3.2; const x = c + r * Math.cos(a), y = c + r * Math.sin(a);
          const col = t < .3 ? '255,122,90' : t < .75 ? '255,198,90' : '255,246,220'; g.fillStyle = `rgba(${col},${.05 + .12 * t})`; g.beginPath(); g.arc(x, y, 6 + 26 * t * (.6 + rr() * .4), 0, 6.283); g.fill(); } });
      swirl = add(new T.Mesh(new T.PlaneGeometry(24, 24), mb(tex, .6))); }
    const photon = add(new T.Mesh(new T.TorusGeometry(3.12, look === 'icon' ? .08 : .05, 12, 200), new T.MeshBasicMaterial({ color: '#fff2c8', fog: false })));
    return { group: G, update(t, cam, o) {
      o = o || {}; const tilt = o.tilt == null ? .10 : o.tilt, spin = o.spin == null ? .35 : o.spin;
      G.lookAt(cam.position);                                   // face the camera: lens/halo/photon ring stay round
      if (disk) disk.rotation.set(-Math.PI / 2 + tilt, 0, t * spin);
      if (lens) lens.rotation.set(0, 0, -t * spin * .6);
      if (ring) ring.rotation.set(0, 0, 0);
      if (swirl) swirl.rotation.set(0, 0, -t * spin * 1.6);
    } };
  };
  M.scenes.blackhole = function (ctx, p) {
    const { T } = ctx, S = new T.Scene(); S.background = new T.Color(p.bg || '#02030a');
    ctx.stars(S, p.stars || 2500, 300, { seed: 31 });
    const bh = M.lib.blackhole(ctx, p.look); S.add(bh.group);
    const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .1, 900); ctx.side(cam, p.side == null ? .1 : p.side);
    const D = p.dist || ({ ring: 44, whirlpool: 46, icon: 60 }[p.look] || 30), ap = p.approach == null ? 1 : p.approach, dur = Math.max(1, ctx.t1 - ctx.t0);
    return { scene: S, camera: cam, draw(t, u) {
      const d = D - ap * (D * .35) * (u / dur), e = .22 + .02 * Math.sin(u * .5);
      cam.position.set(Math.sin(u * .05) * d * .2, Math.sin(e) * d, Math.cos(e) * d); cam.lookAt(0, 0, 0);
      bh.update(t, cam, p);
    } };
  };
})();
