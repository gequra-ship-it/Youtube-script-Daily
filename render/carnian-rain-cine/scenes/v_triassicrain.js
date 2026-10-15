// triassicrain — a rain-soaked Triassic valley at night (carnian-rain-cine; look C rebuild 2026-10-15): a river valley under a low
// storm ceiling, slopes covered in ferns and tall whorled conifers fading into mist, heavy rain, splashes on the river, lightning.
// Look C (cine_spec 3A): real 3D forms drawn with light. Terrain: dark ground with glowing height contours + cool outline.
// Near ferns (subject): dark fronds cut from the pinnae atlas, warm fresnel outline + glowing pinna edges, faint mesh lines and
// sparse warm points. Conifers (surroundings): dark with a cool outline and a few cool points. River: dark mirror (planar
// reflection pass) reflecting the outlines, rippled by the rain. Rain: thin light streaks; splashes: short-lived points.
// Lightning stays the bright accent: bolts + sky flash, and every outline flares with the flash.
// Every plant is ONE mesh: a fern = 8 arching fronds merged into one geometry; a conifer = trunk + whorls of drooping branch sprays
// merged into one geometry (one atlas: bark / fern pinnae / conifer sprays, alpha-cut). They sway and shake under the rain by a
// vertex deform (weight grows from 0 at the root, so attached parts move with the stem); lines and points follow the same deform.
// The camera starts low among the ferns and rises over the valley.
// params (cues): { rise: cue (camera starts rising), bolt: cue (the big lightning strike), side: .1 }
(window.MIYA = window.MIYA || { scenes: {} }).scenes.triassicrain = function (ctx, p) {
  const { T, sm, cue } = ctx, K = window.MIYA.kit, LC = K.lookC;
  const FOG = new T.Color('#05070f'); const S = new T.Scene(); S.fog = new T.FogExp2(FOG.clone(), .0085); S.background = FOG.clone();
  const tBolt = cue(p.bolt, ctx.t0 + 4.2), tRise = cue(p.rise, ctx.t0), WL = -3.6;
  // shader materials here render straight to the canvas: give them the renderer's tone mapping + output colour space, so they look
  // the same in plain frames and inside transitions (which composite linear targets)
  const TM = m => { m.fragmentShader = m.fragmentShader.replace(/}\s*$/, '\n#include <tonemapping_fragment>\n#include <colorspace_fragment>\n}'); return m; };
  const uFlash = { value: 0 }, uTime = { value: 0 };
  // ---------- valley ----------
  const xr = z => 28 * Math.sin(z * .011 + .6) + 10 * Math.sin(z * .031);
  const hsh = (x, y) => { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); };
  const vn = (x, y) => { const i = Math.floor(x), j = Math.floor(y), fx = x - i, fy = y - j, ux = fx * fx * (3 - 2 * fx), uy = fy * fy * (3 - 2 * fy);
    const a = hsh(i, j), b = hsh(i + 1, j), c = hsh(i, j + 1), d = hsh(i + 1, j + 1); return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy; };
  const fbm = (x, y) => { let v = 0, a = .5; for (let k = 0; k < 5; k++) { v += a * vn(x, y); x *= 2.03; y *= 2.03; a *= .5; } return v; };
  const H = (x, z) => { const d = Math.abs(x - xr(z)); return -3 + sm(9, 150, d) * 34 + fbm(x * .02, z * .02) * 9 * sm(6, 40, d) + (fbm(x * .1, z * .1) - .5) * 1.2 - 1.6 * (1 - sm(4, 11, d)); };
  const TW = 520, TD = 760, tg = new T.PlaneGeometry(TW, TD, 120, 180); tg.rotateX(-Math.PI / 2); tg.translate(0, 0, -TD / 2 + 60);
  const tp = tg.attributes.position;
  for (let i = 0; i < tp.count; i++) tp.setY(i, H(tp.getX(i), tp.getZ(i)));
  tg.computeVertexNormals();
  const terM = TM(LC.contour({ base: '#020308', line: '#3a4890', rim: '#0c1030', spacing: 1.4, width: .04, far: 200, k: .5 }));
  // flat ground (the floodplain) would turn the height lines into wide bands: cap their width at ~2.5 px in screen space
  terM.fragmentShader = terM.fragmentShader.replace('abs(fract(h+.5)-.5)/(wd+fw)', 'abs(fract(h+.5)-.5)/(min(wd,fw*1.5)+fw)');
  const terK = .5;
  if (!p.noTer) S.add(new T.Mesh(tg, terM));
  // ---------- sky (night storm ceiling with lightning) ----------
  const skyU = { flash: uFlash, fpos: { value: new T.Vector2(0, -1) }, time: uTime };
  const skyM = TM(new T.ShaderMaterial({ side: T.BackSide, depthWrite: false, fog: false, uniforms: skyU,
    vertexShader: 'varying vec3 vP; void main(){ vP=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: `uniform float flash,time; uniform vec2 fpos; varying vec3 vP;
      float h(vec2 p){ return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
      float n(vec2 p){ vec2 i=floor(p),f=fract(p); f=f*f*(3.-2.*f); return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y); }
      float fbm(vec2 p){ float v=0.,a=.5; for(int i=0;i<4;i++){ v+=a*n(p); p*=2.02; a*=.5; } return v; }
      void main(){ float y=max(vP.y,0.); vec2 q=vP.xz/(y+.1)*1.2; float c=fbm(q+vec2(time*.06,time*.03)), c2=fbm(q*2.5+vec2(-time*.1,time*.05));
        vec3 col=mix(vec3(.0035,.004,.012),vec3(.016,.017,.045),c)*(.7+.5*c2);
        col=mix(vec3(.010,.011,.028),col,smoothstep(0.,.25,y));
        float fd=length(vP.xz/(y+.25)-fpos); col+=vec3(.55,.62,1.)*flash*(.025+.7*exp(-fd*.9))*(.3+c*c*1.6);
        gl_FragColor=vec4(col,1.); }` }));
  const dome = new T.Mesh(new T.SphereGeometry(600, 48, 24), skyM); if (!p.noSky) S.add(dome);
  // ---------- river: dark mirror (planar reflection of the outlines), rain-rippled ----------
  const rtRef = new T.WebGLRenderTarget(ctx.W >> 2, ctx.H >> 2, { type: T.HalfFloatType, colorSpace: T.LinearSRGBColorSpace });
  const wNz = K.tex(K.noise(256, { seed: 33, octaves: 4, sx: 2, sy: 2 }), false);
  const wU = { tRef: { value: rtRef.texture }, tN: { value: wNz }, res: { value: new T.Vector2(ctx.W, ctx.H) }, time: uTime, flash: uFlash, fogC: { value: FOG }, dens: { value: .0085 } };
  const water = new T.Mesh(new T.PlaneGeometry(TW, TD), TM(new T.ShaderMaterial({ uniforms: wU,
    vertexShader: 'varying vec3 vW; void main(){ vec4 w=modelMatrix*vec4(position,1.); vW=w.xyz; gl_Position=projectionMatrix*viewMatrix*w; }',
    fragmentShader: `uniform sampler2D tRef, tN; uniform vec2 res; uniform float time, flash, dens; uniform vec3 fogC; varying vec3 vW;
      void main(){ vec2 q=vW.xz; float a=texture2D(tN,q*.06+vec2(time*.05,-time*.08)).r, b=texture2D(tN,q*.11-vec2(time*.07,time*.04)).r, c=texture2D(tN,q*.31+vec2(0.,time*.3)).r;
        vec2 n=vec2(a-b, b+c-1.)*.6;
        vec3 dv=vW-cameraPosition; float dd=length(dv); vec3 v=-dv/dd; float fr=.22+.78*pow(1.-max(v.y,0.),3.);
        vec2 uv=gl_FragCoord.xy/res; uv.y=1.-uv.y; uv+=n*.012;
        vec3 refl=texture2D(tRef,uv).rgb;
        vec3 col=vec3(.002,.003,.007)+refl*fr*.8+vec3(.35,.4,.7)*flash*.03*fr;
        float ff=1.-exp(-dens*dens*dd*dd); col=mix(col,fogC,ff);
        gl_FragColor=vec4(col,1.); }` })));
  water.rotation.x = -Math.PI / 2; water.position.set(0, WL, -TD / 2 + 60); if (!p.noWat) S.add(water);

  // ---------- plant atlas: [0,.25] bark, [.25,.625] fern pinnae, [.625,1] conifer sprays (only the shapes are used now) ----------
  const AT = 1024, ac = document.createElement('canvas'); ac.width = ac.height = AT; const g = ac.getContext('2d'), r = ctx.rng(5);
  g.clearRect(0, 0, AT, AT);
  g.fillStyle = '#3a2c20'; g.fillRect(0, 0, 256, AT); for (let i = 0; i < 260; i++) { g.fillStyle = `rgba(${r() < .5 ? '20,14,10' : '90,70,52'},${.25 + r() * .4})`; g.fillRect(r() * 256, r() * AT, 2 + r() * 6, 30 + r() * 140); }
  const F0 = 256, FW = 384;
  for (let j = 0; j < 64; j++) { const y = 4 + j * 16; [-1, 1].forEach(sd => { const x0 = F0 + FW / 2, L = FW / 2 - 4, fy = 26 + r() * 8, wd = 7.5;
      g.fillStyle = '#3e6a22'; g.beginPath(); g.moveTo(x0, y - wd * .6);
      for (let k = 0; k <= 10; k++) { const q = k / 10, px = x0 + sd * q * L, py = y + q * fy - wd * (1 - q * .85) - (k % 2 ? 2.2 : 0) * (1 - q); g.lineTo(px, py); }
      for (let k = 10; k >= 0; k--) { const q = k / 10, px = x0 + sd * q * L, py = y + q * fy + wd * (1 - q * .85) + (k % 2 ? 2.2 : 0) * (1 - q); g.lineTo(px, py); }
      g.closePath(); g.fill(); }); }
  g.fillStyle = '#4a5a26'; g.fillRect(F0 + FW / 2 - 3, 0, 6, AT);
  const C0 = 640, CW = 384;
  for (let j = 0; j < 46; j++) { const y = 10 + j * 22; [-1, 1].forEach(sd => { const x0 = C0 + CW / 2;
      for (let k = 0; k < 16; k++) { const q = k / 16, px = x0 + sd * (6 + q * (CW / 2 - 10)), py = y + q * 26;
        g.fillStyle = '#2a4a2a'; g.beginPath(); g.ellipse(px, py, 7, 4.5, sd * -.6, 0, 6.283); g.fill(); } }); }
  g.fillStyle = '#2a2418'; g.fillRect(C0 + CW / 2 - 4, 0, 8, AT);
  const atlas = new T.CanvasTexture(ac); atlas.colorSpace = T.SRGBColorSpace; atlas.flipY = false; atlas.anisotropy = 4;
  // geometry builder: strips with uv into an atlas region, plus a sway weight per vertex
  function Geo() { this.p = []; this.u = []; this.w = []; this.i = []; }
  Geo.prototype.strip = function (pts, side, up, wid, u0, u1, w0, w1, fold) {
    const b = this.p.length / 3, n = pts.length;
    for (let k = 0; k < n; k++) { const s = k / (n - 1), c = pts[k], sv = side[k], uv = up[k], w = wid(s), f = fold * w;
      [[-1, 0], [0, 1], [1, 0]].forEach(([e, m]) => { this.p.push(c.x + sv.x * e * w + uv.x * (m * f - f * .5), c.y + sv.y * e * w + uv.y * (m * f - f * .5), c.z + sv.z * e * w + uv.z * (m * f - f * .5));
        this.u.push(u0 + (u1 - u0) * (e + 1) / 2, s); this.w.push(w0 + (w1 - w0) * s); }); }
    for (let k = 0; k < n - 1; k++) for (let e = 0; e < 2; e++) { const a = b + k * 3 + e, c = a + 3; this.i.push(a, c, a + 1, a + 1, c, c + 1); } };
  Geo.prototype.tube = function (h, r0, r1, seg, ring, u0, u1, wf) {
    const b = this.p.length / 3; for (let k = 0; k <= seg; k++) { const s = k / seg, rr = r0 + (r1 - r0) * s; for (let j = 0; j <= ring; j++) { const a = j / ring * 6.283;
      this.p.push(Math.cos(a) * rr, s * h, Math.sin(a) * rr); this.u.push(u0 + (u1 - u0) * j / ring, s); this.w.push(wf(s)); } }
    for (let k = 0; k < seg; k++) for (let j = 0; j < ring; j++) { const a = b + k * (ring + 1) + j, c = a + ring + 1; this.i.push(a, c, a + 1, a + 1, c, c + 1); } };
  Geo.prototype.build = function () { const o = new T.BufferGeometry(); o.setAttribute('position', new T.Float32BufferAttribute(this.p, 3)); o.setAttribute('uv', new T.Float32BufferAttribute(this.u, 2));
    o.setAttribute('sw', new T.Float32BufferAttribute(this.w, 1)); o.setIndex(this.i); o.computeVertexNormals(); return o; };
  function arch(o, az, el, droop, len, n) { const pts = [], side = [], up = []; let x = o.x, y = o.y, z = o.z;
    for (let k = 0; k < n; k++) { const s = k / (n - 1), e = el - droop * s * s, dl = len / (n - 1);
      pts.push(new T.Vector3(x, y, z)); const dir = new T.Vector3(Math.cos(e) * Math.cos(az), Math.sin(e), Math.cos(e) * Math.sin(az));
      const sv = new T.Vector3(-Math.sin(az), 0, Math.cos(az)); side.push(sv); up.push(new T.Vector3().crossVectors(dir, sv).normalize());
      x += dir.x * dl; y += dir.y * dl; z += dir.z * dl; }
    return { pts, side, up }; }
  function fernGeo(seed) { const G = new Geo(), q = ctx.rng(seed), n = 8;
    for (let f = 0; f < n; f++) { const az = f / n * 6.283 + q() * .5, len = 1.5 + q() * .9, a = arch(new T.Vector3(0, .05, 0), az, 1.05 + q() * .35, 1.9 + q() * .8, len, 10);
      G.strip(a.pts, a.side, a.up, s => .3 * len / 2 * Math.pow(Math.sin(Math.PI * Math.min(1, .12 + s * .95)), .8), .25, .625, 0, 1, .18); }
    return G.build(); }
  function coniferGeo(seed) { const G = new Geo(), q = ctx.rng(seed);   // unit height, scaled per instance
    const sw = s => s * s * .6;
    G.tube(1, .016, .004, 10, 6, 0, .25, sw);
    for (let y = .32; y < .97; y += .075 + q() * .025) { const nb = 4, L = (1 - y) * .26 + .04, rr = .016 * (1 - y) + .004;
      for (let b = 0; b < nb; b++) { const az = b / nb * 6.283 + y * 7 + q() * .4, a = arch(new T.Vector3(Math.cos(az) * rr, y, Math.sin(az) * rr), az, .15 - y * .1, .9 + q() * .5, L * 1.25, 5);
        const wd = s => Math.sin(Math.PI * Math.min(1, .2 + s * .85));
        G.strip(a.pts, a.side, a.up, s => (.09 + .03 * (1 - y)) * wd(s), .625, 1, sw(y), sw(y) + .06, .05);
        G.strip(a.pts, a.up, a.side, s => .06 * wd(s), .625, 1, sw(y), sw(y) + .06, 0); } }
    return G.build(); }
  // sway/shake deform (GLSL, on `transformed`, before the instance matrix); `ph` from the instance position
  const SWAY = (amp, shake) => `float w2 = sw * sw;
        transformed.x += w2 * ${amp.toFixed(3)} * (sin(uTime * 1.3 + ph) * .6 + sin(uTime * 3.3 + ph * 2. + position.y * 3.) * .3);
        transformed.z += w2 * ${amp.toFixed(3)} * .5 * sin(uTime * 1.1 + ph * 1.7);
        transformed.y -= w2 * ${shake.toFixed(3)} * (.5 + .5 * sin(uTime * 9. + ph * 5. + position.x * 4. + position.z * 3.));`;
  // look C plant material: dark body cut from the atlas, fresnel outline + glowing leaf edges, flares with the lightning, fog
  function plantMat(o) { return TM(new T.ShaderMaterial({ side: T.DoubleSide,
    uniforms: { atlas: { value: atlas }, uTime, flash: uFlash, base: { value: new T.Color(o.base) }, rim: { value: new T.Color(o.rim) }, k: { value: o.k }, ke: { value: o.ke }, fogC: { value: FOG }, dens: { value: .0085 } },
    vertexShader: `attribute float sw; uniform float uTime; varying vec2 vUv; varying vec3 vN; varying vec3 vV; varying float vD;
      void main(){ vUv=uv; vec3 transformed=position; float ph=0.;
        #ifdef USE_INSTANCING
          ph = instanceMatrix[3].x * .37 + instanceMatrix[3].z * .21;
        #endif
        ${SWAY(o.amp, o.shake)}
        vec4 pp=vec4(transformed,1.); vec3 n=normal;
        #ifdef USE_INSTANCING
          pp=instanceMatrix*pp; n=mat3(instanceMatrix)*n;
        #endif
        vec4 mv=viewMatrix*modelMatrix*pp; vN=normalize(normalMatrix*n); vV=normalize(-mv.xyz); vD=length(mv.xyz); gl_Position=projectionMatrix*mv; }`,
    fragmentShader: `uniform sampler2D atlas; uniform vec3 base, rim, fogC; uniform float k, ke, flash, dens; varying vec2 vUv; varying vec3 vN; varying vec3 vV; varying float vD;
      void main(){ vec4 tx=texture2D(atlas,vUv); if(tx.a<.45) discard;
        float e=0.; if(vUv.x>.25){ vec2 o=vec2(1.2/1024.,0.); e=smoothstep(.15,.8,1.-min(min(texture2D(atlas,vUv+o).a,texture2D(atlas,vUv-o).a),min(texture2D(atlas,vUv+o.yx).a,texture2D(atlas,vUv-o.yx).a))); }
        float f=pow(1.-abs(dot(normalize(vN),normalize(vV))),5.);
        vec3 c=base+rim*(f*k+e*ke)*(1.+flash*1.6);
        float ff=1.-exp(-dens*dens*vD*vD); c=mix(c,fogC,ff);
        gl_FragColor=vec4(c,1.); }` })); }
  // swaying wireframe/points over the same instanced geometry
  const swayPatch = (m, amp, shake, inst) => { m.onBeforeCompile = sh => { sh.uniforms.uTime = uTime;
    sh.vertexShader = (inst ? 'attribute float sw; uniform float uTime;\n' : 'attribute float sw; attribute float ph; uniform float uTime;\n') + sh.vertexShader.replace('#include <begin_vertex>', `#include <begin_vertex>
      ${inst ? 'float ph = 0.;\n#ifdef USE_INSTANCING\n ph = instanceMatrix[3].x * .37 + instanceMatrix[3].z * .21;\n#endif' : ''}
      ${SWAY(amp, shake)}`); }; return m; };
  const FERN = { amp: .12, shake: .09 }, CON = { amp: .03, shake: .004 };
  const fernM = plantMat({ ...FERN, base: '#040205', rim: '#ffb850', k: .55, ke: .05 });
  const conM = plantMat({ ...CON, base: '#020308', rim: '#5f78ff', k: .5, ke: .0 });
  const M4 = new T.Matrix4(), Q = new T.Quaternion(), V = new T.Vector3(), Sc = new T.Vector3(), E = new T.Euler(), pr = ctx.rng(71);
  // points that follow the sway: a subset of each instance's vertices, placed in world space (sway runs in the shader)
  function instPoints(geo, mats, every, o) { const pa = geo.attributes.position.array, swa = geo.attributes.sw.array, P = [], W = [], PH = [], v = new T.Vector3();
    mats.forEach((m, k) => { const ph = m.elements[12] * .37 + m.elements[14] * .21; for (let i = (k * 7) % every; i < swa.length; i += every) { v.set(pa[i * 3], pa[i * 3 + 1], pa[i * 3 + 2]).applyMatrix4(m); P.push(v.x, v.y, v.z); W.push(swa[i]); PH.push(ph); } });
    const pg = new T.BufferGeometry(); pg.setAttribute('position', new T.Float32BufferAttribute(P, 3)); pg.setAttribute('sw', new T.Float32BufferAttribute(W, 1)); pg.setAttribute('ph', new T.Float32BufferAttribute(PH, 1));
    const pts = new T.Points(pg, swayPatch(new T.PointsMaterial({ color: o.color, size: o.size, transparent: true, opacity: o.opacity, blending: T.AdditiveBlending, depthWrite: false, fog: true }), o.amp * .5, o.shake * .5, false));
    pts.frustumCulled = false; return pts; }
  const flareMats = [];                                  // line/point layers that brighten with the lightning: [material, base opacity]
  // ferns (subject, warm): along the slopes near the camera path
  const fernGs = [fernGeo(3), fernGeo(9), fernGeo(17)], NF = 120;
  fernGs.forEach(fg => { const im = new T.InstancedMesh(fg, fernM, NF), mats = []; let k = 0;
    while (k < NF) { const z = 40 - pr() * 190, sd = pr() < .5 ? -1 : 1, d = 6 + pr() * 55, x = xr(z) + sd * d;
      if (z > -10 && Math.abs(x - xr(z) - 16) < 6) continue; const s = .9 + pr() * 1.1; V.set(x, H(x, z) - .05, z); E.set((pr() - .5) * .25, pr() * 6.28, (pr() - .5) * .25); Q.setFromEuler(E); Sc.set(s, s * (.85 + pr() * .3), s); M4.compose(V, Q, Sc); im.setMatrixAt(k++, M4); mats.push(M4.clone()); }
    if (p.noFern) return; S.add(im);
    const wm = swayPatch(new T.MeshBasicMaterial({ color: '#ffb850', wireframe: true, transparent: true, opacity: .03, blending: T.AdditiveBlending, depthWrite: false, fog: true }), FERN.amp, FERN.shake, true);
    const wl = new T.InstancedMesh(fg, wm, NF); for (let i = 0; i < NF; i++) wl.setMatrixAt(i, mats[i]); wl.frustumCulled = false; S.add(wl); flareMats.push([wm, wm.opacity]);
    const pts = instPoints(fg, mats, 30, { color: '#ffe0a0', size: .035, opacity: .9, ...FERN }); S.add(pts); flareMats.push([pts.material, .9]); });
  // conifers (surroundings, cool): on the slopes, thinning out into the mist
  const conGs = [coniferGeo(4), coniferGeo(8)], NC = 50;
  conGs.forEach(cg => { const im = new T.InstancedMesh(cg, conM, NC), mats = []; let k = 0;
    while (k < NC) { const z = 30 - pr() * 420, sd = pr() < .5 ? -1 : 1, d = 16 + Math.pow(pr(), 1.2) * 150, x = xr(z) + sd * d;
      const h = 16 + pr() * 18; V.set(x, H(x, z) - .3, z); Q.setFromEuler(E.set(0, pr() * 6.28, 0)); Sc.set(h, h, h); M4.compose(V, Q, Sc); im.setMatrixAt(k++, M4); mats.push(M4.clone()); }
    if (p.noCon) return; S.add(im); const pts = instPoints(cg, mats, 41, { color: '#8fa6ff', size: .2, opacity: .35, ...CON }); S.add(pts); flareMats.push([pts.material, .35]); });
  { const im = new T.InstancedMesh(conGs[0], conM, 14), mats = []; for (let k = 0; k < 14; k++) { const z = 8 - k * 9 - pr() * 5, sd = k % 3 == 0 ? -1 : 1, x = xr(z) + sd * (24 + pr() * 14), h = 20 + pr() * 12;
      V.set(x, H(x, z) - .3, z); Q.setFromEuler(E.set(0, pr() * 6.28, 0)); Sc.set(h, h, h); M4.compose(V, Q, Sc); im.setMatrixAt(k, M4); mats.push(M4.clone()); }
    if (!p.noCon) { S.add(im); const pts = instPoints(conGs[0], mats, 23, { color: '#8fa6ff', size: .16, opacity: .5, ...CON }); S.add(pts); flareMats.push([pts.material, .5]); } }
  // lightning: bolts in the clouds ahead (ribbons) + flash in the sky shader
  const strikes = [[ctx.t0 + 1.2, -90, -380, .6], [tBolt, 40, -330, 1.3], [ctx.t0 + 6.6, 160, -420, .7]];
  const bolts = strikes.map(([, x, z], i) => { const r4 = ctx.rng(90 + i), pos = []; const trunk = []; let px = x, py = 140; while (py > 0) { trunk.push([px, py]); px += (r4() - .5) * 20; py -= 7 + r4() * 9; } trunk.push([px, -2]);
    const seg = (pts, w0) => { for (let k = 0; k < pts.length - 1; k++) { const [x0, y0] = pts[k], [x1, y1] = pts[k + 1], w = w0 * (1 - .5 * k / pts.length); pos.push(x0 - w, y0, 0, x0 + w, y0, 0, x1 + w, y1, 0, x0 - w, y0, 0, x1 + w, y1, 0, x1 - w, y1, 0); } };
    seg(trunk, 1.6); for (let b = 0; b < 4; b++) { const st = trunk[2 + (r4() * (trunk.length - 5) | 0)], br = [st]; let bx = st[0], by = st[1]; for (let k = 0; k < 5; k++) { bx += (r4() - .3) * 16 * (b % 2 ? 1 : -1); by -= 6 + r4() * 6; br.push([bx, by]); } seg(br, .7); }
    const g2 = new T.BufferGeometry(); g2.setAttribute('position', new T.BufferAttribute(new Float32Array(pos), 3));
    const m = new T.Mesh(g2, new T.MeshBasicMaterial({ color: new T.Color('#e4eaff').multiplyScalar(8), transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, fog: false, side: T.DoubleSide }));
    m.position.set(0, 0, z); S.add(m); const gl = ctx.glow(S, '#b8c6ff', 220, 0); gl.position.set(x, 90, z); return { m, gl }; });
  const flashAt = (t, ts) => { const dt = t - ts; if (dt < 0 || dt > 1.5) return 0; return Math.exp(-dt * 4) * (.55 + .45 * Math.cos(dt * 41)) * (dt < .04 ? dt / .04 : 1); };
  // ---------- mist banks (soft billboards, faint navy) ----------
  const mistT = (() => { const c = K.noise(256, { seed: 44, octaves: 5 }), c2 = document.createElement('canvas'); c2.width = c2.height = 256; const x = c2.getContext('2d');
    x.drawImage(c, 0, 0); const id = x.getImageData(0, 0, 256, 256); for (let i = 0; i < 256 * 256; i++) { const px = i % 256, py = i / 256 | 0, rx = (px - 128) / 128, ry = (py - 128) / 128, f = Math.max(0, 1 - rx * rx - ry * ry * 1.4);
      const v = id.data[i * 4] / 255; id.data[i * 4] = id.data[i * 4 + 1] = id.data[i * 4 + 2] = 255; id.data[i * 4 + 3] = Math.max(0, Math.min(255, (v - .25) * 1.6 * f * 255)); } x.putImageData(id, 0, 0);
    const t = new T.CanvasTexture(c2); t.colorSpace = T.SRGBColorSpace; return t; })();
  const mists = []; const mr = ctx.rng(66);
  for (let i = 0; i < 7; i++) { const z = 10 - mr() * 380, x = xr(z) + (mr() - .5) * 160, s = 60 + mr() * 90;
    const sp = new T.Sprite(new T.SpriteMaterial({ map: mistT, color: '#3a4a86', transparent: true, opacity: .06 + mr() * .08, depthWrite: false, fog: true })); sp.scale.set(s, s * .35, 1);
    sp.position.set(x, H(x, z) + 4 + mr() * 14, z); if (!p.noMist) S.add(sp); mists.push([sp, x, mr(), sp.material.opacity]); }
  // ---------- rain (thin light streaks around the camera) + splashes on the river ----------
  const NR = 2400, rg = new T.BufferGeometry(), rpos = new Float32Array(NR * 6), rb = []; const r5 = ctx.rng(88);
  for (let i = 0; i < NR; i++) rb.push([(r5() - .5) * 60, r5() * 40, -Math.pow(r5(), .9) * 70 + 4, r5()]);
  rg.setAttribute('position', new T.BufferAttribute(rpos, 3));
  const rainM = new T.LineBasicMaterial({ color: '#a8bcff', transparent: true, opacity: .32, blending: T.AdditiveBlending, depthWrite: false, fog: true });
  const rainL = new T.LineSegments(rg, rainM); rainL.frustumCulled = false; if (!p.noRain) S.add(rainL);
  const NS = 1600, spl = ctx.points(NS, { size: .22, opacity: .75, color: '#c8d6ff', fog: true }), sb = []; const r6 = ctx.rng(99); if (!p.noSpl) S.add(spl); spl.frustumCulled = false;
  for (let i = 0; i < NS; i++) { const z = 30 - r6() * 140; sb.push([xr(z) + (r6() - .5) * 16, z, r6()]); }

  const cam = new T.PerspectiveCamera(42, ctx.W / ctx.H, .3, 1500); ctx.side(cam, p.side == null ? .1 : p.side);
  const camR = new T.PerspectiveCamera(), R = ctx.R;
  return { scene: S, camera: cam, draw(t, u) {
    uTime.value = t;
    let fl = 0, fb = 0, fi = 0; strikes.forEach((s, i) => { const f = flashAt(t, s[0]) * s[3]; fl += f; bolts[i].m.material.opacity = f > .06 && Math.cos((t - s[0]) * 41) > -.3 ? Math.min(1, f * 1.5) : 0; bolts[i].gl.material.opacity = .35 * f; if (f > fb) { fb = f; fi = i; } });
    uFlash.value = fl; skyU.fpos.value.set(strikes[fi][1] / 160, strikes[fi][2] / 160);
    terM.uniforms.k.value = terK * (1 + fl * 2.2);
    flareMats.forEach(([m, o]) => m.opacity = Math.min(1, o * (1 + fl * 1.5)));
    S.fog.color.copy(FOG).lerp(new T.Color('#141a34'), Math.min(1, fl * .25)); S.background.copy(S.fog.color);
    // camera: low among the ferns, moving up the valley, rising to look out over the river and the forest in the rain
    const k = sm(tRise, ctx.t1 + .5, t), z = 26 - u * 3.2, side = 13 + k * 6, x = xr(z) + side, gy = H(x, z);
    cam.position.set(x, Math.max(gy, -3) + 1.4 + k * 6, z);
    const zt = z - 60, xt = xr(zt) + 2 - k * 4, yt = H(xr(zt), zt) + 5 + 2 * (1 - k); cam.lookAt(xt, yt, zt);
    mists.forEach(([sp, x0, o, op]) => { sp.position.x = x0 + Math.sin(t * .05 + o * 6) * 8 + t * .6; sp.material.opacity = op * (1 + fl * 2); });
    // rain streaks in a box that follows the camera
    const cx = cam.position.x, cy = cam.position.y, cz = cam.position.z;
    for (let i = 0; i < NR; i++) { const [rx, ry, rz, o] = rb[i]; const yy = ((ry - t * (22 + o * 8)) % 40 + 40) % 40 - 18, xx = cx + rx + yy * .12, zz = cz + rz, ln = .9 + o * .8;
      rpos.set([xx, cy + yy, zz, xx + ln * .12, cy + yy + ln, zz], i * 6); }
    rg.attributes.position.needsUpdate = true;
    rainM.opacity = .32 + fl * .3;
    // splashes: each one a short-lived bright point on the water, re-placed every cycle (seek-safe by the cycle index)
    const sa = spl.geometry.attributes.position.array, sc = spl.geometry.attributes.color.array;
    for (let i = 0; i < NS; i++) { const [x0, z0, o] = sb[i], per = .5 + o * .4, ph = t / per + o * 13, cyc = Math.floor(ph), f = ph - cyc, j = hsh(i, cyc);
      sa.set([x0 + (j - .5) * 6, -3.5 + f * .25, z0 + (hsh(cyc, i) - .5) * 6], i * 3); const v = Math.max(0, 1 - f * 3) * .8; sc.set([v, v, v], i * 3); }
    spl.geometry.attributes.position.needsUpdate = spl.geometry.attributes.color.needsUpdate = true;
    // river mirror: render the scene from below the water plane into the reflection target
    if (!p.noWat) { cam.updateMatrixWorld(); camR.copy(cam); camR.position.set(cam.position.x, 2 * WL - cam.position.y, cam.position.z); camR.up.set(0, 1, 0); camR.lookAt(xt, 2 * WL - yt, zt);
      camR.projectionMatrix.copy(cam.projectionMatrix); camR.projectionMatrixInverse.copy(cam.projectionMatrixInverse);
      water.visible = rainL.visible = spl.visible = false; R.setRenderTarget(rtRef); R.render(S, camR); R.setRenderTarget(null); water.visible = rainL.visible = spl.visible = true; }
  } };
};
