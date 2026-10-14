// whale — a realistic swimming great whale in the open ocean (stage), built with MIYA.kit (2026-10-14, whale-fall test).
// Body swept along a spine with blue-whale proportions, mottled skin + throat pleats (procedural colour/normal maps), wet clearcoat,
// flukes/pectorals/dorsal fin that follow the swimming wave, god rays, marine snow, the surface seen from below.
// params (cues): { court: cue (a ghost basketball court appears under the body for scale, ~28 m vs a 30 m whale), courtOff: cue,
//   calf: cue (a calf swims in beside it), exhale: cue (last breath: a bubble cloud from the blowholes), sink: cue (the body stops,
//   rolls and sinks, the light fades), deep: cue (darkness, a few bioluminescent specks below), side:.12, length:30 }
(window.MIYA = window.MIYA || { scenes: {} }).scenes.whale = function (ctx, p) {
  const { T, sm, cue } = ctx, K = window.MIYA.kit, L = p.length || 30;
  const S = new T.Scene(); const FOG = new T.Color('#06324d'), DEEP = new T.Color('#00060c');
  S.fog = new T.FogExp2(FOG.clone(), .012);
  // sky dome: bright from above, dark below
  const dome = new T.Mesh(new T.SphereGeometry(500, 32, 16), new T.ShaderMaterial({ side: T.BackSide, depthWrite: false, fog: false, uniforms: { k: { value: 1 } },
    vertexShader: 'varying vec3 vP; void main(){ vP=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: 'uniform float k; varying vec3 vP; void main(){ float y=vP.y; vec3 top=vec3(.10,.42,.62), mid=vec3(.02,.17,.29), bot=vec3(.0,.02,.04); vec3 c = y>0. ? mix(mid,top,pow(y,.7)) : mix(mid,bot,pow(-y,.6)); gl_FragColor=vec4(c*k,1.); }' }));
  S.add(dome);
  const hemi = new T.HemisphereLight('#7cc4f0', '#000a14', .65); S.add(hemi);
  const sun = new T.DirectionalLight('#d8f0ff', 1.9); sun.position.set(-6, 70, 12); S.add(sun);
  const rim = new T.DirectionalLight('#7cc8ff', 1.6); rim.position.set(25, 18, -45); S.add(rim);
  S.environment = ctx.env();
  // ---------- skin textures (u = along the body tail->head, v = around: .25 top, .75 belly) ----------
  const W2 = 2048, H2 = 512, base = document.createElement('canvas'); base.width = W2; base.height = H2; const g = base.getContext('2d');
  const grd = g.createLinearGradient(0, 0, 0, H2); [[0, '#3f566e'], [.12, '#2e4258'], [.25, '#1b2838'], [.4, '#2f455c'], [.55, '#4f677f'], [.75, '#6c8296'], [.92, '#4f677f'], [1, '#3f566e']].forEach(([o, c]) => grd.addColorStop(o, c));
  g.fillStyle = grd; g.fillRect(0, 0, W2, H2);
  const mott = K.noise(512, { seed: 21, octaves: 5, sx: 3, sy: 1 }); g.globalAlpha = .35; g.globalCompositeOperation = 'overlay'; g.drawImage(mott, 0, 0, W2, H2);
  g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1; const r1 = K.rng(4);
  for (let i = 0; i < 2600; i++) { const x = r1() * W2, y = r1() * H2 * .9; g.fillStyle = `rgba(${r1() < .6 ? '150,175,200' : '15,25,40'},${.10 + r1() * .16})`; g.beginPath(); g.ellipse(x, y, 3 + r1() * 12, 2 + r1() * 6, 0, 0, 6.283); g.fill(); }
  // throat pleats on the lower front (s .66-.97, v .58-.92) and the mouth line
  g.strokeStyle = 'rgba(30,40,55,.55)'; g.lineWidth = 3; for (let k = 0; k < 34; k++) { const y = H2 * (.58 + k * .01); g.beginPath(); g.moveTo(W2 * .66, y); g.bezierCurveTo(W2 * .8, y + 4, W2 * .9, y - 2, W2 * .97, y); g.stroke(); }
  g.strokeStyle = 'rgba(15,20,30,.85)'; g.lineWidth = 6; [H2 * .5, H2 * 1.0 - 2].forEach(() => {}); g.beginPath(); g.moveTo(W2 * .8, H2 * .045); g.quadraticCurveTo(W2 * .9, H2 * .07, W2 * .995, H2 * .02); g.stroke();
  g.beginPath(); g.moveTo(W2 * .8, H2 * .955); g.quadraticCurveTo(W2 * .9, H2 * .93, W2 * .995, H2 * .98); g.stroke();
  const hc = document.createElement('canvas'); hc.width = 1024; hc.height = 256; const hg = hc.getContext('2d'); hg.drawImage(K.noise(256, { seed: 7, octaves: 4, sx: 4, sy: 1 }), 0, 0, 1024, 256);
  hg.strokeStyle = 'rgba(0,0,0,.6)'; hg.lineWidth = 2; for (let k = 0; k < 34; k++) { const y = 256 * (.58 + k * .01); hg.beginPath(); hg.moveTo(1024 * .66, y); hg.lineTo(1024 * .97, y); hg.stroke(); }
  const skinMap = K.tex(base, true), skinN = K.normalMap(hc, 3); skinMap.flipY = skinN.flipY = false;   // canvas row = v (top .25, belly .75)
  const skin = new T.MeshPhysicalMaterial({ map: skinMap, normalMap: skinN, normalScale: new T.Vector2(.6, .6), roughness: .5, metalness: 0, clearcoat: .5, clearcoatRoughness: .3, envMapIntensity: .3 });
  // ---------- body ----------
  const prof = (s) => Math.pow(Math.sin(Math.PI * Math.min(.9995, Math.pow(s, 1.35))), .8);
  // ONE mesh (user rule 2026-10-14): body + flukes + dorsal fin + flippers. Body space runs FL longer at the tail for the flukes;
  // sb = position along the old body (0 tail stock end, 1 snout), negative inside the flukes.
  const FL = 4.4, LB = L + FL, SB = s => (s * LB - FL) / L, ROOT = .015, SP = 3.4, SW = 2.1;
  const oldW = sb => (.16 + 2.25 * prof(sb)) * (.55 + .45 * sm(.03, .3, sb)) * (sb > .86 ? .92 + .2 * sm(.86, .97, sb) * (1 - sm(.97, 1, sb)) : 1);
  const oldH = sb => (.3 + 1.85 * prof(sb)) * (sb > .85 ? .82 : 1);
  const Q = sb => Math.min(1, Math.max(0, (ROOT - sb) / (ROOT + FL / L)));   // 0 at the fluke root, 1 at the trailing end
  const W0 = oldW(ROOT), H0 = oldH(ROOT);
  const flW = q => q < .7 ? W0 + (SP - W0) * Math.pow(Math.sin(Math.PI / 2 * q / .7), .9) : SP * (1 - .97 * Math.pow((q - .7) / .3, 1.5));
  const flH = q => H0 + (.15 - H0) * sm(0, .45, q);
  const dorsal = sb => sb > .262 && sb < .292 ? (.292 - sb) / .03 : sb > .248 && sb <= .262 ? (sb - .248) / .014 : 0;
  function makeWhale(scale) {
    const grp = new T.Group();
    // flippers: placed in body space (x shifted by FL/2), merged into the same mesh
    const pecG = K.fin([[0, 0], [.6, .35], [2.2, .38], [4.2, .12], [4.6, -.05], [2.4, -.32], [.6, -.35]].map(([x, y]) => [-x, y]), .16); pecG.translate(-2.1, 0, 0);
    const hp = oldH(.68), wp = oldW(.68), Mx = new T.Matrix4();
    const pecs = [1, -1].map(sd => { const g2 = pecG.clone(); Mx.compose(new T.Vector3(L * .18 + FL / 2, -hp * .5, sd * wp * .78), new T.Quaternion().setFromEuler(new T.Euler(sd * .35, sd * .3, .55)), new T.Vector3(1, 1, 1)); g2.applyMatrix4(Mx); g2.userData.v = .8; return g2; });
    const b = K.body({ length: LB, seg: 220, ring: 56, belly: .22, ridge: .08, extra: pecs, u: s => Math.min(1, Math.max(0, SB(s))),
      width: s => { const sb = SB(s); return sb >= ROOT ? oldW(sb) : flW(Q(sb)); },
      height: s => { const sb = SB(s); return sb >= ROOT ? oldH(sb) : flH(Q(sb)); } });
    const mesh = new T.Mesh(b.geo, skin); mesh.position.x = -FL / 2; grp.add(mesh);
    const eye = new T.Mesh(new T.SphereGeometry(.13, 16, 12), new T.MeshStandardMaterial({ color: '#05070a', roughness: .2 })); grp.add(eye); const eye2 = eye.clone(); grp.add(eye2);
    grp.scale.setScalar(scale);
    // swimming wave: vertical, growing toward the tail (the flukes take it too, so they pitch with the stroke)
    const wave = (sb, t, A) => A * Math.pow(1 - Math.max(sb, -.16), 2.2) * Math.sin(t * 1.25 - (1 - sb) * 5.5);
    return { grp, update(t, A) {
      b.deform((s, th, base, k) => { const sb = SB(s); let dx = 0, dy = wave(sb, t, A);
        if (th >= 0) { const q = Q(sb); if (q > 0) dx = -SW * Math.pow(Math.abs(base[k * 3 + 2]) / SP, 1.6) * sm(0, .25, q);   // swept-back flukes
          const d = dorsal(sb); if (d) dy += .75 * d * Math.pow(Math.max(0, Math.sin(th)), 14); }
        return [dx, dy, 0]; });
      const ye = wave(.88, t, A), we = oldW(.88); eye.position.set(L * .38, ye - .25, we * .97); eye2.position.set(L * .38, ye - .25, -we * .97);
    } };
  }
  const W = makeWhale(1); S.add(W.grp); W.grp.rotation.order = 'ZYX';   // pitch (z) in world space after the roll (x)
  const calf = makeWhale(.36); S.add(calf.grp); calf.grp.visible = false;
  // ghost basketball court (28 x 15 m) for scale
  const cp = [], rect = (x0, z0, x1, z1) => cp.push(x0, 0, z0, x1, 0, z0, x1, 0, z0, x1, 0, z1, x1, 0, z1, x0, 0, z1, x0, 0, z1, x0, 0, z0);
  rect(-14, -7.5, 14, 7.5); cp.push(0, 0, -7.5, 0, 0, 7.5); for (let k = 0; k < 48; k++) { const a = k / 48 * 6.283, b2 = (k + 1) / 48 * 6.283; cp.push(1.8 * Math.cos(a), 0, 1.8 * Math.sin(a), 1.8 * Math.cos(b2), 0, 1.8 * Math.sin(b2)); }
  [-1, 1].forEach(sd => { for (let k = 0; k < 24; k++) { const a = -Math.PI / 2 + k / 24 * Math.PI, b2 = -Math.PI / 2 + (k + 1) / 24 * Math.PI; cp.push(sd * (14 - 6.75 * Math.cos(a)), 0, 6.75 * Math.sin(a), sd * (14 - 6.75 * Math.cos(b2)), 0, 6.75 * Math.sin(b2)); } });
  const cg = new T.BufferGeometry(); cg.setAttribute('position', new T.BufferAttribute(new Float32Array(cp), 3));
  const court = new T.LineSegments(cg, new T.LineBasicMaterial({ color: ctx.ACC, transparent: true, opacity: 0, fog: false })); S.add(court);
  // bubbles (last breath)
  const NB = 700, bub = ctx.points(NB, { size: .55, opacity: .9, color: '#e6f6ff' }); S.add(bub); const br = K.rng(31), bb = []; for (let i = 0; i < NB; i++) bb.push([br() - .5, br() - .5, br() - .5, br()]);
  // light and particles
  const shafts = K.shafts(S, { n: 11, top: 70, height: 150, spread: 160, depth: 100, opacity: .1, color: '#a8dcff' });
  const snow = K.snow(S, { n: 4500, box: [120, 90, 80], size: .26, opacity: .6, fall: .35 });
  const NG = 260, gas = ctx.points(NG, { size: .35, opacity: .8, color: '#dff4ff' }); S.add(gas); const gr2 = K.rng(55), gb = []; for (let i = 0; i < NG; i++) gb.push([gr2() - .5, gr2(), gr2() - .5, gr2()]);
  const surf = K.surfaceFromBelow(S, { y: 62, opacity: .35 });
  const glowN = 160, bio = ctx.points(glowN, { size: .6, color: '#5ff0ff' }); S.add(bio); const bo = K.rng(77), bp = []; for (let i = 0; i < glowN; i++) bp.push([(bo() - .5) * 90, -40 - bo() * 30, (bo() - .5) * 60, bo()]);
  const cam = new T.PerspectiveCamera(36, ctx.W / ctx.H, .1, 1200); ctx.side(cam, p.side == null ? .12 : p.side);
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + d, ctx.t);
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    // the fall: after the last breath the body stops, rolls belly-up, tips head-down and sinks for the rest of the shot
    // (accelerating, then steady). The camera stays high and follows late, so the body drops away below it into the dark.
    const ts = p.sink != null ? cue(p.sink) : 1e9, f = Math.max(0, t - ts), sink = sm(0, 3, f), deep = at(p.deep, 5), stop = at(p.exhale, 4);
    const fall = d => d <= 0 ? 0 : d < 3 ? 1.6 * d * d : 14.4 + 9.6 * (d - 3);
    const A = 1.25 * (1 - stop * .95);
    const uS = Math.min(u, ts - ctx.t0), X = d => uS * 1.6 + Math.min(Math.max(d, 0), 4) * .4, xw = X(f), yw = 6 - fall(f);
    W.grp.position.set(xw, yw, 0);
    W.grp.rotation.set(Math.PI * .8 * sm(.3, 6, f), 0, -.5 * sm(0, 4, f) + .04 * Math.sin(u * .4) * (1 - sink));
    W.update(t, A);
    // the calf turns away when the mother stops
    const cv = at(p.calf, 4), cgo = stop; calf.grp.visible = cv > .01 && cgo < .99;
    if (calf.grp.visible) { calf.grp.position.set(xw - 4 + (1 - cv) * -30 - cgo * 22, yw + f * 0 - 5.5 + Math.sin(u * .5) * .4, 6.5 + cgo * 14); calf.grp.rotation.y = cgo * .7; calf.update(t + .9, 1.1); }
    court.material.opacity = .7 * at(p.court, 1.2) * (1 - at(p.courtOff, 1)); court.position.set(xw, yw - 4.2, 0);
    // last breath: a loose column of bubbles from the blowholes, rising and spreading
    const te = p.exhale ? t - cue(p.exhale) : -1, ba = bub.geometry.attributes.position.array, bc = bub.geometry.attributes.color.array;
    for (let i = 0; i < NB; i++) { const [a, b2, c, o] = bb[i]; const k = Math.max(0, te - o * 1.6), r = (.8 + k * 1.6) * (.3 + Math.abs(a));
      ba.set([xw + L * .33 + a * r + Math.sin(k * 2 + i) * .2, yw + 2 + k * (2.2 + o * 2.5) + b2 * .6, c * r * 1.4], i * 3);
      const v = te > o * 1.6 && te < 8 ? .45 * (1 - k / 6.5) : 0; bc[i * 3] = bc[i * 3 + 1] = bc[i * 3 + 2] = Math.max(0, v); }
    bub.geometry.attributes.position.needsUpdate = true; bub.geometry.attributes.color.needsUpdate = true;
    // camera height: stays near the swimming depth, then follows at half speed
    const camY = 13 + at(p.court, 2) * 6 * (1 - at(p.courtOff, 2)) - .55 * fall(f - .8);
    const depthK = Math.min(1, (13 - camY) / 45), light = 1 - depthK * .85 - deep * .06; dome.material.uniforms.k.value = Math.max(.08, light);
    const lit = Math.max(.1, 1 - Math.min(1, fall(f) / 70) * .8); hemi.intensity = .65 * lit; sun.intensity = 1.9 * lit;
    S.fog.color.copy(FOG).lerp(DEEP, Math.min(1, depthK * 1.2)); S.fog.density = .012 + Math.min(1, fall(f) / 90) * .01;
    shafts.update(t, Math.max(0, 1 - depthK * 1.4)); surf.update(t, Math.max(0, 1 - depthK * .9));
    // gas from the carcass: each bubble leaves the body where it was and rises, so a trail stretches up behind the fall
    const ga = gas.geometry.attributes.position.array, gc = gas.geometry.attributes.color.array, P = 5;
    for (let i = 0; i < NG; i++) { const [a, o, c, w] = gb[i]; const loc = f - .6 - o * P; let v = 0, x = 0, y = -999, z = 0;
      if (loc > 0) { const tr = f - (loc % P), age = f - tr; x = X(tr) + a * 7 + Math.sin(age * 1.5 + i) * .4; y = 6 - fall(tr) + 1.8 + age * (2.2 + w * 1.6); z = c * 3; v = sink * (1 - age / P) * .85; }
      ga.set([x, y, z], i * 3); gc[i * 3] = gc[i * 3 + 1] = gc[i * 3 + 2] = v; }
    gas.geometry.attributes.position.needsUpdate = true; gas.geometry.attributes.color.needsUpdate = true;
    const ba2 = bio.geometry.attributes.color.array, bpos = bio.geometry.attributes.position.array; for (let i = 0; i < glowN; i++) { const [x, y, z, o] = bp[i]; bpos.set([xw + x, yw + y + 30 + Math.sin(t * .7 + o * 9) * .5, z], i * 3); const v = deep * (.4 + .6 * Math.max(0, Math.sin(t * 1.3 + o * 20))); ba2[i * 3] = v * .4; ba2[i * 3 + 1] = v; ba2[i * 3 + 2] = v; }
    bio.geometry.attributes.position.needsUpdate = true; bio.geometry.attributes.color.needsUpdate = true;
    // camera: alongside, slow orbit; in the fall it stops orbiting, backs off a little and tilts down after the body
    const ca = -.25 + Math.min(u, ts - ctx.t0 + 2) * .02, cd = 46 - 6 * at(p.court, 2) * (1 - at(p.courtOff, 2)) + sink * 4;
    const xc = X(Math.min(f, 1));
    cam.position.set(xc + Math.sin(ca) * cd, camY, Math.cos(ca) * cd);
    const ty = yw + Math.min(12, .4 * (camY - yw)) * sink;   // the body sinks toward the lower part of the frame
    cam.lookAt(xc + 1.5 * (1 - sink), ty, 0);
    snow.update(t, [cam.position.x, cam.position.y - 10, 0]);
  } };
};
