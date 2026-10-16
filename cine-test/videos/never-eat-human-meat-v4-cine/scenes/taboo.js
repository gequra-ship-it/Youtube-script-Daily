// taboo scenes for never-eat-human-meat-v4-cine (2026-10-14). Abstract and calm: no bodies other than distant silhouettes seen
// from behind, no flesh, no gore.
//  societyring — a wide ring of standing human silhouettes (each ONE merged mesh, faceless, seen from behind on the near side) on a
//    dark plain around a solid balance of light (lathe pillar, extruded beam, hanging pans with glowing rims). On "every society"
//    small lights wake at the figures' feet one by one round the ring; on "one rule" spokes of light run from every figure to the
//    balance; on "moral line" the beam settles level and a ring of light rises on the ground between the people and the balance.
//    params (cues): { ring, rule, line, side:.12 }
//  proteinlab — a folded protein (one continuous swept chain: round loops, wide helix ribbons, sheet strands with arrowheads; glossy
//    with glowing edges) floating over a projector ring in a dark lab; on "biology" a DNA double helix of light builds itself from
//    the floor up behind it (two backbones + base-pair rungs), on "write" a pulse runs up it, on "law" the camera pulls back.
//    params (cues): { turn, dna, write, law, side:.12 }
(function () {
  const M = (window.MIYA = window.MIYA || { scenes: {} });

  // fresnel rim + optional self glow from vertex colour, added to a standard/physical material (the series' "glowing edges")
  function rimify(T, mat, col, k, self) {
    mat.onBeforeCompile = sh => { sh.uniforms.rimC = { value: new T.Color(col) }; sh.uniforms.rimK = { value: k }; mat.userData.sh = sh;
      sh.fragmentShader = 'uniform vec3 rimC; uniform float rimK;\n' + sh.fragmentShader.replace('#include <emissivemap_fragment>',
        '#include <emissivemap_fragment>\n float fr = pow(1.0 - abs(dot(normalize(normal), normalize(vViewPosition))), 2.6);\n totalEmissiveRadiance += rimC * fr * rimK;' +
        (self ? '\n#ifdef USE_COLOR\n totalEmissiveRadiance += vColor.rgb * ' + self.toFixed(3) + ';\n#endif' : '')); };
    mat.customProgramCacheKey = () => 'rim' + (self || 0); return mat;
  }
  // people only: a rim on the edges that FACE the light (fresnel weighted by the direction to a point light in view space, spec 3A
  // "backlit but readable"), not an all-round outline. `lp` = { value: view-space light position }, updated every frame.
  function rimToward(T, mat, col, k, lp) {
    mat.onBeforeCompile = sh => { sh.uniforms.rimC = { value: new T.Color(col) }; sh.uniforms.rimK = { value: k }; sh.uniforms.rimL = lp; mat.userData.sh = sh;
      sh.fragmentShader = 'uniform vec3 rimC; uniform float rimK; uniform vec3 rimL;\n' + sh.fragmentShader.replace('#include <emissivemap_fragment>',
        '#include <emissivemap_fragment>\n vec3 rLv = normalize(rimL + vViewPosition);\n' +
        ' float fr = pow(1.0 - abs(dot(normalize(normal), normalize(vViewPosition))), 2.6);\n' +
        ' vec2 rN = normal.xy / max(1e-4, length(normal.xy)), rS = rLv.xy / max(1e-4, length(rLv.xy));\n' +
        ' float rw = smoothstep(-.25, .75, dot(rN, rS)) * (.35 + .65 * smoothstep(-.4, .5, dot(normal, rLv)));\n totalEmissiveRadiance += rimC * fr * rw * rimK;'); };
    mat.customProgramCacheKey = () => 'rimToward'; return mat;
  }
  function merge(T, list) {   // [geometry, matrix] -> one non-indexed geometry (position + normal)
    let n = 0; const gs = list.map(([g, m]) => { const q = (g.index ? g.toNonIndexed() : g.clone()); q.applyMatrix4(m); n += q.attributes.position.count; return q; });
    const pos = new Float32Array(n * 3), nor = new Float32Array(n * 3); let o = 0;
    gs.forEach(g => { pos.set(g.attributes.position.array, o * 3); nor.set(g.attributes.normal.array, o * 3); o += g.attributes.position.count; });
    const out = new T.BufferGeometry(); out.setAttribute('position', new T.BufferAttribute(pos, 3)); out.setAttribute('normal', new T.BufferAttribute(nor, 3)); return out;
  }

  // one standing figure (faceless, arms down), height ~1.75, faces -z. ONE geometry: torso lathe + head + limbs merged.
  function figureGeo(T, o) {
    const V = (x, y, z) => new T.Vector3(x, y, z), L = [], sw = o.sh || 1, hip = o.hip || 1, coat = o.coat;
    const limb = (a, b, r0, r1) => { const d = b.clone().sub(a), len = d.length(), g = new T.CylinderGeometry(r1, r0, len, 14, 1, true);
      const m = new T.Matrix4().compose(a.clone().add(b).multiplyScalar(.5), new T.Quaternion().setFromUnitVectors(V(0, 1, 0), d.normalize()), V(1, 1, 1)); L.push([g, m]);
      [[a, r0], [b, r1]].forEach(([p, r]) => L.push([new T.SphereGeometry(r, 14, 10), new T.Matrix4().makeTranslation(p.x, p.y, p.z)])); };
    // torso: hip -> waist -> chest -> shoulders -> neck, elliptical cross-section (z scaled)
    const tp = [[0, .86], [.165 * hip, .9], [.17 * hip, .98], [.145, 1.08], [.16 * sw, 1.22], [.19 * sw, 1.36], [.17 * sw, 1.44], [.08, 1.5], [.055, 1.53], [.055, 1.58], [0, 1.6]].map(([r, h]) => new T.Vector2(r, h));
    L.push([new T.LatheGeometry(tp, 20), new T.Matrix4().makeScale(1, 1, .62)]);
    L.push([new T.SphereGeometry(.105, 18, 14), new T.Matrix4().compose(V(0, 1.665, .005), new T.Quaternion(), V(.88, 1.08, .95))]);
    if (o.hair) L.push([new T.SphereGeometry(.115, 16, 12, 0, 6.283, 0, 2.0), new T.Matrix4().compose(V(0, 1.665, .02), new T.Quaternion(), V(.95, 1.25, 1.0))]);
    const sx = .2 * sw;
    limb(V(sx - .02, 1.4, 0), V(sx + .03, 1.13, .02), .055, .045); limb(V(sx + .03, 1.13, .02), V(sx + .02, .87, -.03), .043, .034);
    limb(V(-sx + .02, 1.4, 0), V(-sx - .03, 1.13, .02), .055, .045); limb(V(-sx - .03, 1.13, .02), V(-sx - .02, .87, -.03), .043, .034);
    L.push([new T.SphereGeometry(.045, 10, 8), new T.Matrix4().compose(V(sx + .02, .82, -.03), new T.Quaternion(), V(.8, 1.3, .7))]);
    L.push([new T.SphereGeometry(.045, 10, 8), new T.Matrix4().compose(V(-sx - .02, .82, -.03), new T.Quaternion(), V(.8, 1.3, .7))]);
    if (coat) { const cp = [[.0, .3], [.26, .3], [.22, .6], [.18, .9], [.0, .92]].map(([r, h]) => new T.Vector2(r, h)); L.push([new T.LatheGeometry(cp, 20), new T.Matrix4().makeScale(1, 1, .75)]); }
    limb(V(.09, .9, 0), V(.1, .48, .01), .075, .055); limb(V(.1, .48, .01), V(.1, .07, .03), .052, .04);
    limb(V(-.09, .9, 0), V(-.1, .48, .01), .075, .055); limb(V(-.1, .48, .01), V(-.1, .07, .03), .052, .04);
    [.1, -.1].forEach(x => L.push([new T.SphereGeometry(.06, 10, 8), new T.Matrix4().compose(V(x, .045, -.05), new T.Quaternion(), V(.75, .6, 1.7))]));
    return merge(T, L);
  }

  M.scenes.societyring = function (ctx, p) {
    const { T, sm, cue, rng, glow, points } = ctx, K = M.kit, E = ctx.env();
    const S = new T.Scene(), BG = new T.Color('#0b0a21'); S.background = BG; S.fog = new T.FogExp2('#0e0b26', .022);
    ctx.stars(S, 1800, 300, { seed: 19, size: 1.3, opacity: .6 });
    const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), ctx.t);
    const GOLD = new T.Color(ctx.ACC), VIO = new T.Color('#8a6cff'), MAG = new T.Color('#d64b9a');
    // ground: dark plain with a soft warm pool of light at the centre
    const gT = ctx.ctex(512, (g, s) => { g.fillStyle = '#000'; g.fillRect(0, 0, s, s); const r = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2); r.addColorStop(0, 'rgba(255,200,120,.55)'); r.addColorStop(.12, 'rgba(200,120,140,.22)'); r.addColorStop(.4, 'rgba(90,70,170,.08)'); r.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = r; g.fillRect(0, 0, s, s); });
    const nz = K.noise(256, { seed: 4, octaves: 5 }), gTile = K.tex(nz, true, [30, 30]); gTile.anisotropy = ctx.R.capabilities.getMaxAnisotropy();
    const ground = new T.Mesh(new T.CircleGeometry(120, 96).rotateX(-Math.PI / 2), new T.MeshLambertMaterial({ color: '#16132e', map: gTile })); S.add(ground);
    const pool = new T.Mesh(new T.PlaneGeometry(70, 70).rotateX(-Math.PI / 2), new T.MeshBasicMaterial({ map: gT, transparent: true, blending: T.AdditiveBlending, depthWrite: false })); pool.position.y = .02; S.add(pool);
    // ---- the balance (machine: separate solid parts are right) ----
    const BAL = new T.Group(); S.add(BAL);
    const brass = new T.MeshStandardMaterial({ color: '#b08a4a', metalness: 1, roughness: .28, envMap: E, envMapIntensity: .6, emissive: '#2a1806' });
    const dark = new T.MeshStandardMaterial({ color: '#2a2440', metalness: .8, roughness: .35, envMap: E, envMapIntensity: .5 });
    const pil = [[0, 0], [.75, 0], [.75, .12], [.6, .16], [.55, .3], [.36, .34], [.2, .45], [.14, .6], [.12, 2.2], [.16, 2.28], [.16, 2.36], [.1, 2.42], [0, 2.44]].map(([r, h]) => new T.Vector2(r, h));
    BAL.add(new T.Mesh(new T.LatheGeometry(pil, 48), dark));
    const BEAM = new T.Group(); BEAM.position.y = 2.42; BAL.add(BEAM);
    const bs = new T.Shape(); bs.moveTo(-1.7, -.03); bs.lineTo(-.15, -.07); bs.quadraticCurveTo(0, -.16, .15, -.07); bs.lineTo(1.7, -.03); bs.lineTo(1.7, .03); bs.lineTo(.15, .07); bs.quadraticCurveTo(0, .14, -.15, .07); bs.lineTo(-1.7, .03); bs.closePath();
    const beamG = new T.ExtrudeGeometry(bs, { depth: .08, bevelEnabled: true, bevelThickness: .02, bevelSize: .02, bevelSegments: 2, curveSegments: 12 }); beamG.translate(0, 0, -.04);
    BEAM.add(new T.Mesh(beamG, brass));
    BEAM.add(new T.Mesh(new T.SphereGeometry(.09, 20, 14), brass));
    const lineM = new T.MeshBasicMaterial({ color: GOLD.clone().multiplyScalar(1.6), transparent: true, opacity: .7, blending: T.AdditiveBlending, depthWrite: false });
    const bl = new T.Mesh(new T.BoxGeometry(3.4, .012, .012), lineM); bl.position.z = .065; BEAM.add(bl);
    const pans = [-1.62, 1.62].map(x => { const g = new T.Group(); g.position.x = x; BEAM.add(g);
      const P2 = new T.Group(); g.add(P2);
      for (let k = 0; k < 3; k++) { const a = k / 3 * 6.283; const top = new T.Vector3(0, 0, 0), bot = new T.Vector3(Math.cos(a) * .42, -1.0, Math.sin(a) * .42); const d = bot.clone().sub(top);
        const c = new T.Mesh(new T.CylinderGeometry(.008, .008, d.length(), 6), lineM); c.position.copy(top.clone().add(bot).multiplyScalar(.5)); c.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), d.normalize()); P2.add(c); }
      const pp = [[0, -1.12], [.25, -1.11], [.42, -1.04], [.5, -.98], [.48, -.97], [.4, -1.02], [.24, -1.08], [0, -1.09]].map(([r, h]) => new T.Vector2(r, h));
      P2.add(new T.Mesh(new T.LatheGeometry(pp, 40), brass));
      const rim = new T.Mesh(new T.TorusGeometry(.5, .012, 8, 64).rotateX(Math.PI / 2).translate(0, -.98, 0), lineM); P2.add(rim);
      const gl = glow(P2, '#ffd08a', 1.6, .25); gl.position.y = -.98; return { g, P2, gl }; });
    const top = glow(BAL, '#ffe2b0', 3.5, .35); top.position.y = 2.5; const halo = glow(BAL, '#d6a0ff', 16, .12); halo.position.y = 2.0;
    const cL = new T.PointLight('#ffcf90', 26, 30, 1.5); cL.position.set(0, 3.2, 0); S.add(cL);
    // light column rising from the balance (two crossed additive gradient planes)
    const colT = ctx.ctex(128, (g, s) => { const gr = g.createLinearGradient(0, s, 0, 0); gr.addColorStop(0, 'rgba(255,220,160,.7)'); gr.addColorStop(1, 'rgba(255,220,160,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); const gx = g.createLinearGradient(0, 0, s, 0); gx.addColorStop(0, 'rgba(0,0,0,1)'); gx.addColorStop(.5, 'rgba(0,0,0,0)'); gx.addColorStop(1, 'rgba(0,0,0,1)'); g.globalCompositeOperation = 'destination-out'; g.fillStyle = gx; g.fillRect(0, 0, s, s); });
    const colM = new T.MeshBasicMaterial({ map: colT, transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide, fog: false });
    [0, Math.PI / 2].forEach(r => { const m = new T.Mesh(new T.PlaneGeometry(3.2, 14), colM); m.position.y = 9.4; m.rotation.y = r; BAL.add(m); });
    // ---- the ring of people ----
    const R = rng(23), NF = 30, RAD = 9.5, variants = [{ sh: 1.05 }, { sh: .92, hip: 1.1, hair: 1 }, { sh: 1, coat: 1 }, { sh: .95, hair: 1, coat: 1 }, { sh: 1.12 }].map(o => figureGeo(T, o));
    const rimLP = { value: new T.Vector3() }, BALW = new T.Vector3(0, 2.5, 0);   // the balance's light, in world space
    const skin = rimToward(T, new T.MeshStandardMaterial({ color: '#424760', roughness: .75, metalness: .05 }), '#ffc98a', .9, rimLP);
    const figs = [], FEET = [], footG = new T.PlaneGeometry(1.6, 1.6).rotateX(-Math.PI / 2);
    for (let i = 0; i < NF; i++) { const a = i / NF * 6.283 + (R() - .5) * .08, r = RAD + (R() - .5) * 1.2, v = (R() * variants.length) | 0, sc = (.93 + R() * .14) * (R() < .12 ? .72 : 1);
      const m = new T.Mesh(variants[v], skin); m.position.set(Math.sin(a) * r, 0, Math.cos(a) * r); m.scale.setScalar(sc); m.lookAt(0, 0, 0); m.rotateY(Math.PI);   // face the centre (-z forward)
      m.rotation.order = 'YXZ'; S.add(m); figs.push([m, a, R() * 6.283, m.rotation.y]);
      const f = new T.Mesh(footG, new T.MeshBasicMaterial({ map: ctx.dotTex(), color: '#ffcf8a', transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false })); f.position.set(Math.sin(a) * r, .04, Math.cos(a) * r); S.add(f); FEET.push([f, a]); }
    figs.forEach(([m]) => { m.rotation.x = 0; });
    // spokes of light on the ground from each figure to the balance
    const spokeM = new T.MeshBasicMaterial({ map: ctx.ctex(64, (g, s) => { const gr = g.createLinearGradient(0, 0, s, 0); gr.addColorStop(0, 'rgba(0,0,0,0)'); gr.addColorStop(.5, 'rgba(255,255,255,1)'); gr.addColorStop(1, 'rgba(0,0,0,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); }),
      color: GOLD.clone().multiplyScalar(.9), transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false });
    const spokes = figs.map(([m, a]) => { const g = new T.PlaneGeometry(.08, 1).rotateX(-Math.PI / 2).translate(0, 0, -.5); const s = new T.Mesh(g, spokeM); s.position.set(Math.sin(a) * (RAD - .4), .03, Math.cos(a) * (RAD - .4)); s.rotation.y = a; S.add(s); return s; });
    // the moral line: a ring of light on the ground (thin torus) that rises a little and brightens
    const ringM = new T.MeshBasicMaterial({ color: GOLD.clone().multiplyScalar(1.5), transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false });
    const ring = new T.Mesh(new T.TorusGeometry(5.2, .025, 8, 240).rotateX(Math.PI / 2), ringM); S.add(ring);
    const ringPts = points(600, { size: .09, color: '#ffe0a8' }); { const a = ringPts.geometry.attributes.position.array, r2 = rng(5); for (let i = 0; i < 600; i++) { const q = r2() * 6.283, rr = 5.2 + (r2() - .5) * .2; a.set([Math.sin(q) * rr, .05 + r2() * .1, Math.cos(q) * rr], i * 3); } } ringPts.material.opacity = 0; S.add(ringPts);
    const dust = K.snow(S, { n: 1500, box: [40, 12, 40], size: .07, opacity: .5, color: '#ffd9a0', fall: -.08, seed: 12 });
    S.add(new T.HemisphereLight('#6c7896', '#0a0a1c', 2.0));   // cool neutral fill (not violet): backs stay readable
    const fillL = new T.DirectionalLight('#b4bed2', 1.3); fillL.position.set(8, 7, 22); S.add(fillL);   // soft cool fill from the camera side
    const back = new T.DirectionalLight('#9a86ff', .5); back.position.set(-10, 8, -20); S.add(back);
    const cam = new T.PerspectiveCamera(36, ctx.W / ctx.H, .1, 600); ctx.side(cam, p.side == null ? .12 : p.side);
    const dur = Math.max(1, ctx.t1 - ctx.t0), cR = p.ring != null ? cue(p.ring) : ctx.t0 + 1;
    return { scene: S, camera: cam, draw(t, u) {
      ctx.t = t; const rl = at(p.rule, 1.6), ln = at(p.line, 1.4);
      // the people breathe and sway a little (whole figure; no limbs move)
      figs.forEach(([m, a, ph, ry]) => { m.rotation.z = .012 * Math.sin(t * .6 + ph); m.position.y = .004 * Math.sin(t * 1.3 + ph); });
      // feet lights wake round the ring (starting nearest the camera, both ways)
      FEET.forEach(([f, a]) => { const k = Math.abs(((a + Math.PI) % 6.283) - Math.PI) / Math.PI; f.material.opacity = .55 * sm(cR + k * 1.6, cR + k * 1.6 + .5, t) * (.85 + .15 * Math.sin(t * 2 + a * 5)); });
      spokeM.opacity = .55 * rl; spokes.forEach((s, i) => { s.scale.z = (RAD - .9) * sm(cue(p.rule, 1e9) + (i % 5) * .08, cue(p.rule, 1e9) + 1.2 + (i % 5) * .08, t) + .001; });
      colM.opacity = .1 * rl + .06 * ln; top.material.opacity = .35 + .35 * rl; halo.material.opacity = .12 + .1 * rl;
      cL.intensity = 18 + 14 * rl;
      // the beam: rocks, then settles level on "moral line"
      const st = p.settle ? at(p.settle, 1.4) : ln, amp = .16 * (1 - st) + .01; BEAM.rotation.z = amp * Math.sin(t * .9) * Math.exp(-0 * u); pans.forEach(o => { o.P2.rotation.z = -BEAM.rotation.z; o.gl.material.opacity = .2 + .4 * st; });
      lineM.opacity = .55 + .4 * ln;
      ringM.opacity = .9 * ln; ring.position.y = .03 + .05 * ln; ringPts.material.opacity = .8 * ln;
      dust.update(t, [0, 3, 0]);
      const k = sm(0, dur, u), ca = .18 - .1 * k;
      cam.position.set(Math.sin(ca) * (22 - 5 * k), 2.4 + .4 * k, Math.cos(ca) * (22 - 5 * k)); cam.lookAt(0, 1.7 - .2 * k, 0);
      cam.updateMatrixWorld(); rimLP.value.copy(BALW).applyMatrix4(cam.matrixWorldInverse);
    } };
  };

  M.scenes.proteinlab = function (ctx, p) {
    const { T, sm, cue, rng, glow, points } = ctx, K = M.kit, E = ctx.env();
    const S = new T.Scene(); S.background = new T.Color('#0a0920'); S.fog = new T.FogExp2('#0c0a24', .03);
    const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + (d || 1.2), ctx.t);
    const V = (x, y, z) => new T.Vector3(x, y, z);
    // ---------- protein backbone: samples with a type and a ribbon normal ----------
    const smp = [];   // [pos, normal, type] type 0 loop, 1 helix, 2 strand
    const helix = (a, b, turns, r) => { const ax = b.clone().sub(a), L = ax.length(), d = ax.clone().normalize(), u0 = Math.abs(d.y) < .9 ? V(0, 1, 0).cross(d).normalize() : V(1, 0, 0).cross(d).normalize(), v0 = d.clone().cross(u0);
      const n = Math.round(turns * 36); for (let i = 0; i <= n; i++) { const f = i / n, th = f * turns * 6.283, rad = u0.clone().multiplyScalar(Math.cos(th)).addScaledVector(v0, Math.sin(th));
        smp.push([a.clone().addScaledVector(d, f * L).addScaledVector(rad, r), rad, 1]); } };
    const strand = (a, b, nrm) => { const n = 36; for (let i = 0; i <= n; i++) { const f = i / n; smp.push([a.clone().lerp(b, f).addScaledVector(nrm, .1 * Math.sin(f * 6.283 * 3)), nrm.clone(), 2, f]); } };
    const loop = (pts) => { const prev = smp[smp.length - 1][0], c = new T.CatmullRomCurve3([prev, ...pts]); const L = c.getLength(), n = Math.max(6, Math.round(L * 7));
      for (let i = 1; i < n; i++) smp.push([c.getPoint(i / n), null, 0]); };
    const Z = V(0, 0, 1);
    smp.push([V(-4.2, -3.6, .6), null, 0]); loop([V(-3.6, -3.2, 1.6), V(-3.0, -2.8, 1.5)]);
    helix(V(-3.0, -2.4, 1.0), V(-2.8, 2.6, 1.2), 3.5, 1.0);
    loop([V(-2.2, 3.8, 0), V(-1.0, 3.6, -1.2)]);
    strand(V(-.7, 3.0, -1.5), V(-.7, -2.2, -1.5), Z); loop([V(-.3, -3.0, -1.6)]);
    strand(V(.25, -2.4, -1.5), V(.25, 2.9, -1.5), Z); loop([V(.7, 3.7, -1.6)]);
    strand(V(1.2, 3.0, -1.5), V(1.2, -2.2, -1.5), Z); loop([V(2.2, -3.4, -.8), V(3.2, -2.9, .2)]);
    helix(V(3.2, -2.2, .7), V(3.0, 2.8, 1.2), 3, .95);
    loop([V(2.6, 4.0, 2.2), V(1.6, 3.4, 3.0)]);
    helix(V(1.2, 2.6, 3.0), V(-1.8, 1.0, 3.2), 2, .85);
    loop([V(-2.8, .2, 3.4), V(-2.2, -1.4, 3.6), V(-.6, -2.4, 3.2), V(.8, -1.8, 2.6)]);
    const N = smp.length, pos = smp.map(s => s[0]), tan = pos.map((q, i) => pos[Math.min(N - 1, i + 1)].clone().sub(pos[Math.max(0, i - 1)]).normalize());
    // normals: helix radial, strand sheet normal, loops parallel-transported; then smoothed and kept continuous
    let nPrev = V(0, 1, 0).cross(tan[0]).normalize(); const nr = [];
    for (let i = 0; i < N; i++) { let n = smp[i][1] ? smp[i][1].clone() : nPrev.clone(); n.addScaledVector(tan[i], -n.dot(tan[i])).normalize(); if (n.dot(nPrev) < 0) n.negate(); nr.push(n); nPrev = n; }
    const nsm = nr.map((n, i) => { const a = V(0, 0, 0); for (let k = -4; k <= 4; k++) a.add(nr[Math.min(N - 1, Math.max(0, i + k))]); return a.addScaledVector(tan[i], -a.dot(tan[i])).normalize(); });
    // cross-section half sizes per type (smoothed), strand arrowheads
    const wA = smp.map(s => s[2] === 1 ? .5 : s[2] === 2 ? (s[3] > .82 ? .55 + .45 * Math.min(1, (s[3] - .82) / .02) * (1 - (s[3] - .84) / .16) : .48) : .15);
    const wB = smp.map(s => s[2] === 0 ? .15 : .1);
    const sA = wA.map((v, i) => { let a = 0; for (let k = -3; k <= 3; k++) a += wA[Math.min(N - 1, Math.max(0, i + k))]; return smp[i][2] === 2 ? v : a / 7; }), sB = wB.map((v, i) => { let a = 0; for (let k = -3; k <= 3; k++) a += wB[Math.min(N - 1, Math.max(0, i + k))]; return a / 7; });
    const RS = 14, vp = new Float32Array(N * RS * 3), vn = new Float32Array(N * RS * 3), vc = new Float32Array(N * RS * 3), idx = [];
    const c0 = new T.Color('#7a5cff'), c1 = new T.Color('#e0559f'), c2 = new T.Color('#f2c14e'), cc = new T.Color();
    for (let i = 0; i < N; i++) { const t = tan[i], n = nsm[i], b = t.clone().cross(n).normalize(), f = i / (N - 1);
      if (f < .5) cc.copy(c0).lerp(c1, f * 2); else cc.copy(c1).lerp(c2, (f - .5) * 2);
      for (let j = 0; j < RS; j++) { const th = j / RS * 6.283, ca = Math.cos(th), sa = Math.sin(th);
        // superellipse-ish section: flat faces for ribbons, round for loops
        const e = sA[i] > .25 ? .55 : 1, cx = Math.sign(ca) * Math.pow(Math.abs(ca), e), sy = Math.sign(sa) * Math.pow(Math.abs(sa), e);
        const q = pos[i].clone().addScaledVector(b, cx * sA[i]).addScaledVector(n, sy * sB[i]);
        const nn = b.clone().multiplyScalar(cx / sA[i]).addScaledVector(n, sy / sB[i]).normalize();
        const k = (i * RS + j) * 3; vp.set([q.x, q.y, q.z], k); vn.set([nn.x, nn.y, nn.z], k); vc.set([cc.r, cc.g, cc.b], k); } }
    for (let i = 0; i < N - 1; i++) for (let j = 0; j < RS; j++) { const a = i * RS + j, b2 = i * RS + (j + 1) % RS, c = a + RS, d = b2 + RS; idx.push(a, c, b2, b2, c, d); }
    const pg = new T.BufferGeometry(); pg.setAttribute('position', new T.BufferAttribute(vp, 3)); pg.setAttribute('normal', new T.BufferAttribute(vn, 3)); pg.setAttribute('color', new T.BufferAttribute(vc, 3)); pg.setIndex(idx);
    pg.computeVertexNormals();
    const pmat = rimify(T, new T.MeshPhysicalMaterial({ vertexColors: true, roughness: .28, metalness: .1, clearcoat: 1, clearcoatRoughness: .15, envMap: E, envMapIntensity: .45 }), '#ffd9a0', .7, .18);
    const PRO = new T.Group(); PRO.position.set(0, 4.2, 0); S.add(PRO); const prot = new T.Mesh(pg, pmat); PRO.add(prot); PRO.scale.setScalar(.55);
    // C-alpha light points along the chain + a soft halo
    const NA = Math.floor(N / 6), ap = points(NA, { size: .16, color: '#fff0d0' }); { const a = ap.geometry.attributes.position.array; for (let i = 0; i < NA; i++) { const q = pos[i * 6]; a.set([q.x, q.y, q.z], i * 3); } } PRO.add(ap);
    const ph = glow(PRO, '#a77cff', 16, .18), ph2 = glow(PRO, '#ffcf8a', 7, .12);
    // ---------- lab: reflective floor with tile seams, projector ring, far vertical light panels ----------
    const tile = ctx.ctex(512, (g, s) => { g.fillStyle = '#0d0c1e'; g.fillRect(0, 0, s, s); g.strokeStyle = 'rgba(140,130,255,.22)'; g.lineWidth = 2; for (let k = 0; k <= 4; k++) { g.beginPath(); g.moveTo(k * s / 4, 0); g.lineTo(k * s / 4, s); g.stroke(); g.beginPath(); g.moveTo(0, k * s / 4); g.lineTo(s, k * s / 4); g.stroke(); } });
    tile.wrapS = tile.wrapT = T.RepeatWrapping; tile.repeat.set(84, 84); tile.anisotropy = ctx.R.capabilities.getMaxAnisotropy();
    const floor = new T.Mesh(new T.PlaneGeometry(500, 500).rotateX(-Math.PI / 2), new T.MeshStandardMaterial({ map: tile, roughness: .85, metalness: .1 })); S.add(floor);
    const ped = [[0, 0], [1.9, 0], [1.9, .18], [1.7, .26], [1.3, .3], [0, .3]].map(([r, h]) => new T.Vector2(r, h));
    S.add(new T.Mesh(new T.LatheGeometry(ped, 64), new T.MeshStandardMaterial({ color: '#232040', metalness: .9, roughness: .3, envMap: E, envMapIntensity: .5 })));
    const prM = new T.MeshBasicMaterial({ color: new T.Color(ctx.ACC).multiplyScalar(1.5), transparent: true, opacity: .8, blending: T.AdditiveBlending, depthWrite: false });
    S.add(new T.Mesh(new T.TorusGeometry(1.5, .025, 8, 120).rotateX(Math.PI / 2).translate(0, .31, 0), prM));
    const beamT = ctx.ctex(128, (g, s) => { const gr = g.createLinearGradient(0, s, 0, 0); gr.addColorStop(0, 'rgba(255,220,170,.5)'); gr.addColorStop(1, 'rgba(255,220,170,0)'); g.fillStyle = gr; g.fillRect(0, 0, s, s); });
    const cone = new T.Mesh(new T.CylinderGeometry(2.6, 1.5, 3.4, 48, 1, true).translate(0, 2.0, 0), new T.MeshBasicMaterial({ map: beamT, color: '#ffb070', transparent: true, opacity: .1, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide, fog: false })); S.add(cone);
    const panM = new T.MeshBasicMaterial({ color: '#4a3fa0' });
    for (let k = 0; k < 9; k++) { const a = -1.1 + k * .28, m = new T.Mesh(new T.BoxGeometry(.5, 9, .2), panM); m.position.set(Math.sin(a) * 26, 4.5, -Math.cos(a) * 26); m.lookAt(0, 4.5, 0); S.add(m); }
    // ---------- DNA double helix (builds from the floor up) ----------
    const DNA = new T.Group(); DNA.position.set(-5.0, 0, -6.2); S.add(DNA);
    const DH = 7.8, TURNS = 2.4, DR = 1.15, bb = [0, Math.PI * .8].map(off => { const pts = []; for (let i = 0; i <= 240; i++) { const f = i / 240, th = f * TURNS * 6.283 + off; pts.push(V(Math.cos(th) * DR, .2 + f * DH, Math.sin(th) * DR)); } return new T.CatmullRomCurve3(pts); });
    const bbM = [rimify(T, new T.MeshPhysicalMaterial({ color: '#8f6cff', roughness: .25, clearcoat: 1, envMap: E, envMapIntensity: .5, emissive: '#2a1a70' }), '#d6c4ff', .8), rimify(T, new T.MeshPhysicalMaterial({ color: '#e6699f', roughness: .25, clearcoat: 1, envMap: E, envMapIntensity: .5, emissive: '#5a1838' }), '#ffd0e0', .8)];
    const bbMesh = bb.map((c, k) => { const m = new T.Mesh(new T.TubeGeometry(c, 480, .13, 12, false), bbM[k]); DNA.add(m); return m; });
    const NR = Math.round(TURNS * 10), rungG = new T.CylinderGeometry(.055, .055, 1, 10); rungG.rotateZ(Math.PI / 2);
    const rgM = [new T.MeshStandardMaterial({ color: '#f2c14e', emissive: '#a8741a', emissiveIntensity: .9, roughness: .35, metalness: .3 }), new T.MeshStandardMaterial({ color: '#7fd0ff', emissive: '#2a6aa0', emissiveIntensity: .8, roughness: .35, metalness: .3 })];
    const rungs = [];
    for (let i = 0; i < NR; i++) { const f = (i + .5) / NR, a = bb[0].getPoint(f), b = bb[1].getPoint(f), m = a.clone().lerp(b, .5);
      const g = new T.Group(); DNA.add(g);
      [[a, 0], [b, 1]].forEach(([e, k]) => { const h = new T.Mesh(rungG, rgM[(i + k) % 2]); const d = m.clone().sub(e); h.position.copy(e.clone().lerp(m, .5)); h.scale.set(d.length() * 1.0, 1, 1); h.quaternion.setFromUnitVectors(V(1, 0, 0), d.normalize()); g.add(h); });
      rungs.push([g, f, m]); }
    const tip = glow(DNA, '#fff0c8', 3.0, 0), tip2 = glow(DNA, '#b48cff', 9, 0), pulse = glow(DNA, '#ffe2a8', 4, 0);
    const dHalo = glow(DNA, '#7a5cff', 22, 0); dHalo.position.y = DH / 2;
    const dust = K.snow(S, { n: 1400, box: [30, 14, 30], size: .06, opacity: .45, color: '#ffd9a0', fall: -.05, seed: 21 });
    S.add(new T.HemisphereLight('#4a40a0', '#06051a', .5));
    const key = new T.DirectionalLight('#ffe0b8', 1.1); key.position.set(-6, 10, 8); S.add(key);
    const rimL = new T.DirectionalLight('#a080ff', 1.6); rimL.position.set(4, 3, -10); S.add(rimL);
    const pl = new T.PointLight('#ffcf90', 10, 12, 1.5); pl.position.set(0, 1.2, 0); S.add(pl);
    const cam = new T.PerspectiveCamera(36, ctx.W / ctx.H, .1, 300); ctx.side(cam, p.side == null ? .12 : p.side);
    const tD = p.dna != null ? cue(p.dna) : 1e9, dur = Math.max(1, ctx.t1 - ctx.t0);
    return { scene: S, camera: cam, draw(t, u) {
      ctx.t = t; const tn = at(p.turn, 2), wr = p.write ? t - cue(p.write) : -1, lw = at(p.law, 3);
      PRO.rotation.set(.25 + .1 * Math.sin(u * .3), u * .32 + tn * .6, .05); PRO.position.y = 4.2 + .12 * Math.sin(u * .8);
      // DNA grows: backbone draw range + rungs appear just behind the growing tip
      const gr = Math.min(1, Math.max(0, (t - tD) / 3.6)), ge = gr * gr * (3 - 2 * gr);
      bbMesh.forEach(m => { const n = m.geometry.index.count; m.geometry.setDrawRange(0, Math.floor(n * ge / 6) * 6); m.visible = ge > .003; });
      rungs.forEach(([g, f]) => { const v = sm(f, f + .06, ge); g.visible = v > .01; g.scale.set(Math.max(.01, v), 1, Math.max(.01, v)); });
      const tp = bb[0].getPoint(Math.max(.001, ge)).lerp(bb[1].getPoint(Math.max(.001, ge)), .5); tip.position.copy(tp); tip2.position.copy(tp);
      const tipOn = ge > 0 && ge < 1 ? 1 : ge >= 1 ? Math.max(0, 1 - (t - tD - 3.6)) : 0; tip.material.opacity = .9 * tipOn; tip2.material.opacity = .3 * tipOn;
      dHalo.material.opacity = .12 * ge;
      const pf = wr > 0 ? (wr / 2.2) % 1.2 : -1; pulse.visible = pf >= 0 && pf <= 1; if (pulse.visible) { pulse.position.set(0, .2 + pf * DH, 0); pulse.material.opacity = .7 * Math.sin(Math.PI * pf); }
      DNA.rotation.y = u * .25;
      dust.update(t, [0, 4, 0]);
      const k = sm(0, dur, u), ca = -.15 + .2 * k - .1 * lw, cd = 17 - 2 * k + 5 * lw;
      cam.position.set(Math.sin(ca) * cd + .2, 4.0 + 1.0 * lw, Math.cos(ca) * cd); cam.lookAt(-.2, 3.7 + .5 * lw, -1.5);
    } };
  };
})();
