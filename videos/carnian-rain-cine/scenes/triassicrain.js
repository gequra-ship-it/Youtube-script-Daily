// triassicrain — a rain-soaked Triassic valley (carnian-rain-cine, 2026-10-14): a river valley under a low storm ceiling, slopes
// covered in ferns and tall whorled conifers fading into mist, heavy rain, splashes on the river, lightning in the clouds.
// Every plant is ONE mesh: a fern = 9 arching fronds merged into one geometry; a conifer = trunk + whorls of drooping branch sprays
// merged into one geometry (trunk and foliage share one texture atlas: bark / fern pinnae / conifer sprays, alpha-tested).
// They sway and shake under the rain by a vertex deform (weight grows from 0 at the root, so attached parts move with the stem).
// The camera starts low among the ferns and rises over the valley.
// params (cues): { rise: cue (camera starts rising), bolt: cue (the big lightning strike), side: .1 }
(window.MIYA = window.MIYA || { scenes: {} }).scenes.triassicrain = function (ctx, p) {
  const { T, sm, cue } = ctx, K = window.MIYA.kit;
  const S = new T.Scene(); const FOG = new T.Color('#24302e'); S.fog = new T.FogExp2(FOG.clone(), .0095); S.background = FOG.clone();   // lighter rain haze: far slopes fade into luminous mist
  // stable in motion: tiled maps get max anisotropy, fine normal detail fades with distance
  const ANI = ctx.R ? ctx.R.capabilities.getMaxAnisotropy() : 4;
  const fadeN = (m, n, f, lo, key) => { const prev = m.onBeforeCompile; m.onBeforeCompile = sh => { if (prev) prev(sh);
    sh.fragmentShader = sh.fragmentShader.replace('#include <normal_fragment_maps>', T.ShaderChunk.normal_fragment_maps.replace('mapN.xy *= normalScale;', `mapN.xy *= normalScale * mix(1., ${lo.toFixed(2)}, smoothstep(${n.toFixed(1)}, ${f.toFixed(1)}, length(vViewPosition)));`)); };
    m.customProgramCacheKey = () => key; return m; };
  const KEYDIR = new T.Vector3(-.3, .5, -1).normalize();   // the brighter part of the storm sky: ahead, down the valley (backlight)
  const tBolt = cue(p.bolt, ctx.t0 + 4.2), tRise = cue(p.rise, ctx.t0);
  // ---------- valley ----------
  const xr = z => 28 * Math.sin(z * .011 + .6) + 10 * Math.sin(z * .031);
  const hsh = (x, y) => { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); };
  const vn = (x, y) => { const i = Math.floor(x), j = Math.floor(y), fx = x - i, fy = y - j, ux = fx * fx * (3 - 2 * fx), uy = fy * fy * (3 - 2 * fy);
    const a = hsh(i, j), b = hsh(i + 1, j), c = hsh(i, j + 1), d = hsh(i + 1, j + 1); return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy; };
  const fbm = (x, y) => { let v = 0, a = .5; for (let k = 0; k < 5; k++) { v += a * vn(x, y); x *= 2.03; y *= 2.03; a *= .5; } return v; };
  const H = (x, z) => { const d = Math.abs(x - xr(z)); return -3 + sm(9, 150, d) * 34 + fbm(x * .02, z * .02) * 9 * sm(6, 40, d) + (fbm(x * .1, z * .1) - .5) * 1.2 - 1.6 * (1 - sm(4, 11, d)); };
  const TW = 520, TD = 760, tg = new T.PlaneGeometry(TW, TD, 200, 300); tg.rotateX(-Math.PI / 2); tg.translate(0, 0, -TD / 2 + 60);
  const tp = tg.attributes.position, tcol = new Float32Array(tp.count * 3), cA = new T.Color('#56663e'), cB = new T.Color('#647a3e'), cM = new T.Color('#4a4232'), cc = new T.Color();
  for (let i = 0; i < tp.count; i++) { const x = tp.getX(i), z = tp.getZ(i), h = H(x, z); tp.setY(i, h); const d = Math.abs(x - xr(z));
    cc.copy(cM).lerp(cA, sm(8, 20, d)).lerp(cB, fbm(x * .05 + 9, z * .05) * sm(10, 30, d)); tcol.set([cc.r, cc.g, cc.b], i * 3); }
  tg.setAttribute('color', new T.BufferAttribute(tcol, 3)); tg.computeVertexNormals();
  const gN = K.normalMap(K.noise(256, { seed: 12, octaves: 6 }), 3); gN.repeat.set(60, 90); gN.anisotropy = ANI;
  // ground colour: moss clumps over dark mud (broad patches, so the bank reads as soil and not as more water)
  const gC = (() => { const c = document.createElement('canvas'); c.width = c.height = 256; const x = c.getContext('2d'); x.fillStyle = '#ffffff'; x.fillRect(0, 0, 256, 256);
    x.globalCompositeOperation = 'multiply'; x.globalAlpha = .45; x.drawImage(K.noise(256, { seed: 21, octaves: 4 }), 0, 0); x.globalAlpha = 1; x.globalCompositeOperation = 'source-over'; const rq = ctx.rng(23);
    for (let i = 0; i < 260; i++) { const px = rq() * 256, py = rq() * 256, rd = 4 + rq() * 12, gr = x.createRadialGradient(px, py, 0, px, py, rd); gr.addColorStop(0, `rgba(${170 + rq() * 40 | 0},${215 + rq() * 40 | 0},${110 + rq() * 30 | 0},.5)`); gr.addColorStop(1, 'rgba(170,215,110,0)'); x.fillStyle = gr; x.fillRect(px - rd, py - rd, rd * 2, rd * 2); }
    return K.tex(c, true, [40, 60]); })(); gC.anisotropy = ANI;
  if (!p.noTer) S.add(new T.Mesh(tg, fadeN(new T.MeshPhongMaterial({ vertexColors: true, map: gC, shininess: 16, specular: '#121616', normalMap: gN, normalScale: new T.Vector2(.3, .3) }), 8, 45, .12, 'tr-ground')));
  // ---------- sky (storm ceiling with lightning) + environment for the wet reflections ----------
  const skyU = { flash: { value: 0 }, fpos: { value: new T.Vector2(0, -1) }, time: { value: 0 } };
  const skyM = new T.ShaderMaterial({ side: T.BackSide, depthWrite: false, fog: false, uniforms: skyU,
    vertexShader: 'varying vec3 vP; void main(){ vP=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: `uniform float flash,time; uniform vec2 fpos; varying vec3 vP;
      float h(vec2 p){ return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
      float n(vec2 p){ vec2 i=floor(p),f=fract(p); f=f*f*(3.-2.*f); return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y); }
      float fbm(vec2 p){ float v=0.,a=.5; for(int i=0;i<4;i++){ v+=a*n(p); p*=2.02; a*=.5; } return v; }
      void main(){ float y=max(vP.y,0.); vec2 q=vP.xz/(y+.1)*1.2; float c=fbm(q+vec2(time*.06,time*.03)), c2=fbm(q*2.5+vec2(-time*.1,time*.05));
        vec3 col=mix(vec3(.05,.07,.07),vec3(.13,.16,.16),c)*(.7+.5*c2);
        col=mix(vec3(.15,.19,.18),col,smoothstep(0.,.3,y));
        float ah=max(0.,dot(normalize(vP.xz+1e-5),normalize(vec2(-.2,-1.))));                // thinner cloud ahead, down the valley
        col+=vec3(.20,.25,.24)*pow(ah,4.)*exp(-y*4.)*(.75+.5*c);
        float fd=length(vP.xz/(y+.25)-fpos); col+=vec3(.7,.75,1.)*flash*(.15+1.6*exp(-fd*.9))*(.3+c*c*1.6);
        gl_FragColor=vec4(col,1.); }` });
  const dome = new T.Mesh(new T.SphereGeometry(600, 48, 24), skyM); if (!p.noSky) S.add(dome);
  // sky reflection for the river: a plain cube map rendered once (Phong env lookup is cheap; no PMREM on every material)
  const envS = new T.Scene(); envS.add(new T.Mesh(new T.SphereGeometry(100, 32, 16), skyM)); const cubeRT = new T.WebGLCubeRenderTarget(256, { type: T.HalfFloatType }); new T.CubeCamera(1, 1000, cubeRT).update(ctx.R, envS);
  // river: dark mirror with rain ripples
  const wN = K.normalMap(K.noise(256, { seed: 33, octaves: 4, sx: 2, sy: 2 }), 4); wN.repeat.set(40, 60); wN.anisotropy = ANI;
  const water = new T.Mesh(new T.PlaneGeometry(TW, TD), fadeN(new T.MeshPhongMaterial({ color: '#020404', specular: '#404848', shininess: 120, envMap: cubeRT.texture, reflectivity: .3, combine: T.MixOperation, normalMap: wN, normalScale: new T.Vector2(.1, .1) }), 10, 70, .2, 'tr-water'));
  water.rotation.x = -Math.PI / 2; water.position.set(0, -3.6, -TD / 2 + 60); if (!p.noWat) S.add(water);

  // ---------- plant atlas: [0,.25] bark, [.25,.625] fern pinnae, [.625,1] conifer sprays ----------
  const AT = 1024, ac = document.createElement('canvas'); ac.width = ac.height = AT; const g = ac.getContext('2d'), r = ctx.rng(5);
  g.clearRect(0, 0, AT, AT);
  g.fillStyle = '#3a2c20'; g.fillRect(0, 0, 256, AT); for (let i = 0; i < 260; i++) { g.fillStyle = `rgba(${r() < .5 ? '20,14,10' : '90,70,52'},${.25 + r() * .4})`; g.fillRect(r() * 256, r() * AT, 2 + r() * 6, 30 + r() * 140); }
  // fern frond: rachis along v at u=.5, pinnae to both edges, each pinna lobed
  const F0 = 256, FW = 384;
  for (let j = 0; j < 64; j++) { const y = 4 + j * 16; [-1, 1].forEach(sd => { const x0 = F0 + FW / 2, L = FW / 2 - 4, fy = 26 + r() * 8, wd = 7.5;
      const gr = g.createLinearGradient(x0, 0, x0 + sd * L, 0); gr.addColorStop(0, '#2c4a1a'); gr.addColorStop(.5, `rgb(${58 + r() * 20 | 0},${100 + r() * 26 | 0},${38 + r() * 12 | 0})`); gr.addColorStop(1, '#4e7a2a');
      g.fillStyle = gr; g.beginPath(); g.moveTo(x0, y - wd * .6);
      for (let k = 0; k <= 10; k++) { const q = k / 10, px = x0 + sd * q * L, py = y + q * fy - wd * (1 - q * .85) - (k % 2 ? 2.2 : 0) * (1 - q); g.lineTo(px, py); }
      for (let k = 10; k >= 0; k--) { const q = k / 10, px = x0 + sd * q * L, py = y + q * fy + wd * (1 - q * .85) + (k % 2 ? 2.2 : 0) * (1 - q); g.lineTo(px, py); }
      g.closePath(); g.fill(); g.strokeStyle = 'rgba(150,180,90,.5)'; g.lineWidth = 1.2; g.beginPath(); g.moveTo(x0, y); g.lineTo(x0 + sd * L * .95, y + fy * .95); g.stroke(); }); }
  g.fillStyle = '#4a5a26'; g.fillRect(F0 + FW / 2 - 3, 0, 6, AT);
  // conifer spray: a flattened branch with dense scale-leaf branchlets
  const C0 = 640, CW = 384;
  for (let j = 0; j < 46; j++) { const y = 10 + j * 22; [-1, 1].forEach(sd => { const x0 = C0 + CW / 2;
      for (let k = 0; k < 16; k++) { const q = k / 16, px = x0 + sd * (6 + q * (CW / 2 - 10)), py = y + q * 26;
        g.fillStyle = `rgb(${24 + r() * 14 | 0},${50 + r() * 22 | 0},${30 + r() * 12 | 0})`; g.beginPath(); g.ellipse(px, py, 7, 4.5, sd * -.6, 0, 6.283); g.fill(); } }); }
  g.fillStyle = '#2a2418'; g.fillRect(C0 + CW / 2 - 4, 0, 8, AT);
  const atlas = new T.CanvasTexture(ac); atlas.colorSpace = T.SRGBColorSpace; atlas.flipY = false; atlas.anisotropy = ANI;
  // geometry builder: strips with uv into an atlas region, plus a sway weight per vertex
  function Geo() { this.p = []; this.u = []; this.w = []; this.i = []; }
  Geo.prototype.strip = function (pts, side, up, wid, u0, u1, w0, w1, fold) {   // pts along the strip; side/up: per point vectors
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
  // an arching frond / branch: start point, azimuth, start elevation, droop over its length
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
        G.strip(a.pts, a.up, a.side, s => .06 * wd(s), .625, 1, sw(y), sw(y) + .06, 0); } }   // second spray turned 90 degrees: volume from every side
    return G.build(); }
  const uTime = { value: 0 }, uKey = { value: new T.Vector3() }, uBack = { value: 0 };
  function plantMat(amp, shake) { const m = new T.MeshLambertMaterial({ map: atlas, alphaTest: .45, alphaToCoverage: true, side: T.DoubleSide });
    m.onBeforeCompile = sh => { sh.uniforms.uTime = uTime; sh.uniforms.uKey = uKey; sh.uniforms.uBack = uBack;
      // backlight: fronds between the camera and the bright sky ahead let light through (soft, view-dependent, no outline)
      sh.fragmentShader = 'uniform vec3 uKey; uniform float uBack;\n' + sh.fragmentShader.replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
        totalEmissiveRadiance += diffuseColor.rgb * vec3(.85, 1., .8) * uBack * pow(max(0., dot(normalize(-vViewPosition), uKey)), 3.);`);
      sh.vertexShader = 'attribute float sw; uniform float uTime;\n' + sh.vertexShader.replace('#include <begin_vertex>', `#include <begin_vertex>
        float ph = 0.;
        #ifdef USE_INSTANCING
          ph = instanceMatrix[3].x * .37 + instanceMatrix[3].z * .21;
        #endif
        float w2 = sw * sw;
        transformed.x += w2 * ${amp.toFixed(3)} * (sin(uTime * 1.3 + ph) * .6 + sin(uTime * 3.3 + ph * 2. + position.y * 3.) * .3);
        transformed.z += w2 * ${amp.toFixed(3)} * .5 * sin(uTime * 1.1 + ph * 1.7);
        transformed.y -= w2 * ${shake.toFixed(3)} * (.5 + .5 * sin(uTime * 9. + ph * 5. + position.x * 4. + position.z * 3.));`); };
    return m; }
  const fernM = plantMat(.12, .09), conM = plantMat(.03, .004);
  const M4 = new T.Matrix4(), Q = new T.Quaternion(), V = new T.Vector3(), Sc = new T.Vector3(), E = new T.Euler(), pr = ctx.rng(71);
  // ferns: along the slopes near the camera path
  const fernGs = [fernGeo(3), fernGeo(9), fernGeo(17)], NF = 170;
  fernGs.forEach(fg => { const im = new T.InstancedMesh(fg, fernM, NF); let k = 0;
    while (k < NF) { const z = 40 - pr() * 190, sd = pr() < .5 ? -1 : 1, d = 6 + pr() * 55, x = xr(z) + sd * d;
      if (z > -10 && Math.abs(x - xr(z) - 16) < 6) continue; const s = .9 + pr() * 1.1; V.set(x, H(x, z) - .05, z); E.set((pr() - .5) * .25, pr() * 6.28, (pr() - .5) * .25); Q.setFromEuler(E); Sc.set(s, s * (.85 + pr() * .3), s); M4.compose(V, Q, Sc); im.setMatrixAt(k++, M4); }
    if (!p.noFern) S.add(im); });
  // conifers: on the slopes, thinning out into the mist
  const conGs = [coniferGeo(4), coniferGeo(8)], NC = 50;
  conGs.forEach(cg => { const im = new T.InstancedMesh(cg, conM, NC); let k = 0;
    while (k < NC) { const z = 30 - pr() * 420, sd = pr() < .5 ? -1 : 1, d = 16 + Math.pow(pr(), 1.2) * 150, x = xr(z) + sd * d;
      const h = 16 + pr() * 18; V.set(x, H(x, z) - .3, z); Q.setFromEuler(E.set(0, pr() * 6.28, 0)); Sc.set(h, h, h); M4.compose(V, Q, Sc); im.setMatrixAt(k++, M4); }
    if (!p.noCon) S.add(im); });
  { const im = new T.InstancedMesh(conGs[0], conM, 14); for (let k = 0; k < 14; k++) { const z = 8 - k * 9 - pr() * 5, sd = k % 3 == 0 ? -1 : 1, x = xr(z) + sd * (24 + pr() * 14), h = 20 + pr() * 12;
      V.set(x, H(x, z) - .3, z); Q.setFromEuler(E.set(0, pr() * 6.28, 0)); Sc.set(h, h, h); M4.compose(V, Q, Sc); im.setMatrixAt(k, M4); } if (!p.noCon) S.add(im); }
  // ---------- light ----------
  const hemi = new T.HemisphereLight('#9aaeb0', '#2a3222', 1.0); S.add(hemi);   // cool neutral sky fill, mossy ground bounce
  const key = new T.DirectionalLight('#c4d0cc', 1.1); key.position.copy(KEYDIR).multiplyScalar(100); S.add(key);
  const flashL = new T.DirectionalLight('#d8e0ff', 0); S.add(flashL);
  // lightning: bolts in the clouds ahead (ribbons) + flash in the sky shader
  const strikes = [[ctx.t0 + 1.2, -90, -380, .6], [tBolt, 40, -330, 1.3], [ctx.t0 + 6.6, 160, -420, .7]];
  const bolts = strikes.map(([, x, z], i) => { const r4 = ctx.rng(90 + i), pos = []; const trunk = []; let px = x, py = 140; while (py > 0) { trunk.push([px, py]); px += (r4() - .5) * 20; py -= 7 + r4() * 9; } trunk.push([px, -2]);
    const seg = (pts, w0) => { for (let k = 0; k < pts.length - 1; k++) { const [x0, y0] = pts[k], [x1, y1] = pts[k + 1], w = w0 * (1 - .5 * k / pts.length); pos.push(x0 - w, y0, 0, x0 + w, y0, 0, x1 + w, y1, 0, x0 - w, y0, 0, x1 + w, y1, 0, x1 - w, y1, 0); } };
    seg(trunk, 1.6); for (let b = 0; b < 4; b++) { const st = trunk[2 + (r4() * (trunk.length - 5) | 0)], br = [st]; let bx = st[0], by = st[1]; for (let k = 0; k < 5; k++) { bx += (r4() - .3) * 16 * (b % 2 ? 1 : -1); by -= 6 + r4() * 6; br.push([bx, by]); } seg(br, .7); }
    const g2 = new T.BufferGeometry(); g2.setAttribute('position', new T.BufferAttribute(new Float32Array(pos), 3));
    const m = new T.Mesh(g2, new T.MeshBasicMaterial({ color: new T.Color('#e4eaff').multiplyScalar(8), transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, fog: false, side: T.DoubleSide }));
    m.position.set(0, 0, z); S.add(m); const gl = ctx.glow(S, '#c8d4ff', 220, 0); gl.position.set(x, 90, z); return { m, gl }; });
  const flashAt = (t, ts) => { const dt = t - ts; if (dt < 0 || dt > 1.5) return 0; return Math.exp(-dt * 4) * (.55 + .45 * Math.cos(dt * 41)) * (dt < .04 ? dt / .04 : 1); };
  // ---------- mist banks (soft billboards) ----------
  const mistT = (() => { const c = K.noise(256, { seed: 44, octaves: 5 }), c2 = document.createElement('canvas'); c2.width = c2.height = 256; const x = c2.getContext('2d');
    x.drawImage(c, 0, 0); const id = x.getImageData(0, 0, 256, 256); for (let i = 0; i < 256 * 256; i++) { const px = i % 256, py = i / 256 | 0, rx = (px - 128) / 128, ry = (py - 128) / 128, f = Math.max(0, 1 - rx * rx - ry * ry * 1.4);
      const v = id.data[i * 4] / 255; id.data[i * 4] = id.data[i * 4 + 1] = id.data[i * 4 + 2] = 255; id.data[i * 4 + 3] = Math.max(0, Math.min(255, (v - .25) * 1.6 * f * 255)); } x.putImageData(id, 0, 0);
    const t = new T.CanvasTexture(c2); t.colorSpace = T.SRGBColorSpace; return t; })();
  const mists = []; const mr = ctx.rng(66);
  for (let i = 0; i < 7; i++) { const z = 10 - mr() * 380, x = xr(z) + (mr() - .5) * 160, s = 60 + mr() * 90;
    const sp = new T.Sprite(new T.SpriteMaterial({ map: mistT, color: '#9aaaa6', transparent: true, opacity: .1 + mr() * .14, depthWrite: false, fog: true })); sp.scale.set(s, s * .35, 1);
    sp.position.set(x, H(x, z) + 4 + mr() * 14, z); if (!p.noMist) S.add(sp); mists.push([sp, x, mr()]); }
  // ---------- rain (streaks around the camera) + splashes on the river ----------
  const NR = 2200, rg = new T.BufferGeometry(), rpos = new Float32Array(NR * 6), rb = []; const r5 = ctx.rng(88);
  for (let i = 0; i < NR; i++) rb.push([(r5() - .5) * 60, r5() * 40, -Math.pow(r5(), .9) * 70 + 4, r5()]);
  rg.setAttribute('position', new T.BufferAttribute(rpos, 3));
  const rainM = new T.LineBasicMaterial({ color: '#b8c8d0', transparent: true, opacity: .3, blending: T.AdditiveBlending, depthWrite: false, fog: true });
  const rainL = new T.LineSegments(rg, rainM); rainL.frustumCulled = false; if (!p.noRain) S.add(rainL);
  const NS = 1600, spl = ctx.points(NS, { size: .25, opacity: .7, color: '#cfe0e8', fog: true }), sb = []; const r6 = ctx.rng(99); if (!p.noSpl) S.add(spl); spl.frustumCulled = false;
  for (let i = 0; i < NS; i++) { const z = 30 - r6() * 140; sb.push([xr(z) + (r6() - .5) * 16, z, r6()]); }

  const cam = new T.PerspectiveCamera(42, ctx.W / ctx.H, .1, 1500); ctx.side(cam, p.side == null ? .1 : p.side);
  return { scene: S, camera: cam, draw(t, u) {
    uTime.value = t; skyU.time.value = t;
    let fl = 0, fb = 0, fi = 0; strikes.forEach((s, i) => { const f = flashAt(t, s[0]) * s[3]; fl += f; bolts[i].m.material.opacity = f > .06 && Math.cos((t - s[0]) * 41) > -.3 ? Math.min(1, f * 1.5) : 0; bolts[i].gl.material.opacity = .35 * f; if (f > fb) { fb = f; fi = i; } });
    skyU.flash.value = fl; skyU.fpos.value.set(strikes[fi][1] / 160, strikes[fi][2] / 160);
    hemi.intensity = .9 + fl * .9; flashL.intensity = fl * 2.5; flashL.position.set(strikes[fi][1], 120, strikes[fi][2]);
    S.fog.color.copy(FOG).lerp(new T.Color('#3c4650'), Math.min(1, fl * .5)); S.background.copy(S.fog.color);
    wN.offset.set(t * .02, -t * .035);
    // camera: low among the ferns, moving up the valley, rising to look out over the river and the forest in the rain
    const k = sm(tRise, ctx.t1 + .5, t), z = 26 - u * 3.2, side = 13 + k * 6, x = xr(z) + side, gy = H(x, z);
    cam.position.set(x, Math.max(gy, -3) + 1.4 + k * 6, z);
    const zt = z - 60, xt = xr(zt) + 2 - k * 4; cam.lookAt(xt, H(xr(zt), zt) + 5 + 2 * (1 - k), zt); cam.updateMatrixWorld();
    uKey.value.copy(KEYDIR).transformDirection(cam.matrixWorldInverse); uBack.value = .9 + fl * 1.2;
    // mist drifts slowly down the valley
    mists.forEach(([sp, x0, o]) => { sp.position.x = x0 + Math.sin(t * .05 + o * 6) * 8 + t * .6; });
    // rain streaks in a box that follows the camera
    const cx = cam.position.x, cy = cam.position.y, cz = cam.position.z;
    for (let i = 0; i < NR; i++) { const [rx, ry, rz, o] = rb[i]; const yy = ((ry - t * (22 + o * 8)) % 40 + 40) % 40 - 18, xx = cx + rx + yy * .12, zz = cz + rz, ln = .9 + o * .8;
      rpos.set([xx, cy + yy, zz, xx + ln * .12, cy + yy + ln, zz], i * 6); }
    rg.attributes.position.needsUpdate = true;
    // splashes: each one a short-lived bright point on the water, re-placed every cycle (seek-safe by the cycle index)
    const sa = spl.geometry.attributes.position.array, sc = spl.geometry.attributes.color.array;
    for (let i = 0; i < NS; i++) { const [x0, z0, o] = sb[i], per = .5 + o * .4, ph = t / per + o * 13, cyc = Math.floor(ph), f = ph - cyc, j = hsh(i, cyc);
      sa.set([x0 + (j - .5) * 6, -3.5 + f * .25, z0 + (hsh(cyc, i) - .5) * 6], i * 3); const v = Math.max(0, 1 - f * 3) * .8; sc.set([v, v, v], i * 3); }
    spl.geometry.attributes.position.needsUpdate = spl.geometry.attributes.color.needsUpdate = true;
  } };
};
