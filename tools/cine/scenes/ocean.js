// ocean — a dark alien sea at night with a black hole in the sky and a wave wall sweeping toward the camera (prototype 2026-10-14).
// params: { look:'lensed' (black hole look), wall:34 (wave height), speed:11 (wall speed), start:-120 (wall start z), side:.1,
//   water:'#0a2630', bh:[-30,48,-230] (sky position), bhScale:4.2, rise:1.6 (black hole rise per s) }
(window.MIYA = window.MIYA || { scenes: {} }).scenes.ocean = function (ctx, p) {
  const { T } = ctx, M = window.MIYA, S = new T.Scene();
  S.background = new T.Color('#010208'); S.fog = new T.Fog('#030612', 60, 260);
  ctx.stars(S, 3500, 480, { seed: 9 });
  const g = new T.PlaneGeometry(420, 420, 220, 220); g.rotateX(-Math.PI / 2); const P = g.attributes.position;
  const ox = new Float32Array(P.count), oz = new Float32Array(P.count); for (let i = 0; i < P.count; i++) { ox[i] = P.getX(i); oz[i] = P.getZ(i); }
  S.add(new T.Mesh(g, new T.MeshStandardMaterial({ color: p.water || '#0a2630', roughness: .28, metalness: .2 })));
  const bh = M.lib.blackhole(ctx, p.look || 'lensed'); S.add(bh.group); const bp = p.bh || [-30, 48, -230]; bh.group.scale.setScalar(p.bhScale || 4.2);
  S.add(new T.AmbientLight('#123040', .5)); const k = new T.DirectionalLight('#ffd0a0', 1.1); k.position.set(bp[0], bp[1] + 14, bp[2]); S.add(k);
  const cam = new T.PerspectiveCamera(46, ctx.W / ctx.H, .1, 1200); ctx.side(cam, p.side == null ? .1 : p.side);
  const WALL = p.wall == null ? 34 : p.wall, SP = p.speed || 11, Z0 = p.start || -120;
  return { scene: S, camera: cam, draw(t, u) {
    const zc = Z0 + u * SP;
    for (let i = 0; i < P.count; i++) { const x = ox[i], z = oz[i], dz = z - zc; const wall = WALL * Math.exp(-dz * dz / (dz < 0 ? 260 : 1400)) * (.9 + .1 * Math.sin(x * .05));
      P.setY(i, wall + .6 * Math.sin(x * .18 + u * 1.6) * Math.cos(z * .15 - u * 1.1) + .35 * Math.sin(x * .41 - z * .33 + u * 2.3)); }
    P.needsUpdate = true; g.computeVertexNormals();
    bh.group.position.set(bp[0], bp[1] + u * (p.rise == null ? 1.6 : p.rise), bp[2]);
    cam.position.set(0, 4.5 + .4 * Math.sin(u * .9), 40 - u * 1.2); cam.lookAt(-6, 14 + u * .3, -150);
    bh.update(t, cam, { tilt: .12, spin: .3 });
  } };
};
