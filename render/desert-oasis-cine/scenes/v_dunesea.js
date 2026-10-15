// dunesea — an ocean of sand at golden hour, then an oasis (desert-oasis-cine, 2026-10-14). Stage scene, one terrain.
// Real 3D dune field (sinuous transverse dunes with gentle windward slopes and sharp brinks over steep slip faces, a cross set of
// smaller dunes, broad swells), wind ripples + grain as a tiled normal map, warm glowing haze that hides the distance, the sun
// low ahead (contre-jour: lit crests, dark slip faces), sand blowing off the surface, heat shimmer and a mirage band on the horizon
// (post pass: the scene is rendered into a target and shown through a distortion shader).
// Look rules (2026-10-15): the camera keeps the sun side in frame (backlit crests), thicker glowing haze, the oasis seen from
// low over the crest (palms against the haze and the water). The camera glides over the dunes, looks up at the sun, pans over the empty horizon, drops low over a crest, climbs a big dune and
// at the reveal crests it: below lies a basin with a clear pool (planar reflection pass: palms and sky in the water, ripples,
// shallow edges showing the sand bottom) ringed by date palms and grass. Each palm is ONE mesh (curved trunk with leaf-scar rings +
// crown of arching pinnate fronds + hanging dry fronds) swaying by a vertex deform whose weight grows from 0 at the root.
// params (cues): { sun: cue (look up at the sun), shimmer: cue (heat shimmer grows), empty: cue (pan over the horizon),
//   low: cue (drop low over a crest), turn: cue (climb the big dune), reveal: cue (crest: the oasis below), side: .1 }
(window.MIYA = window.MIYA || { scenes: {} }).scenes.dunesea = function (ctx, p) {
  const { T, sm, cue } = ctx, K = window.MIYA.kit, R = ctx.R;
  const cSun = cue(p.sun, 4.2), cShim = cue(p.shimmer, 6), cEmpty = cue(p.empty, 8), cLow = cue(p.low, 13.5), cTurn = cue(p.turn, 17.1), cRev = cue(p.reveal, 20.7);
  // ---------- terrain function ----------
  const hsh = (x, y) => { const s = Math.sin(x * 127.1 + y * 311.7) * 43758.5453; return s - Math.floor(s); };
  const vn = (x, y) => { const i = Math.floor(x), j = Math.floor(y), fx = x - i, fy = y - j, ux = fx * fx * (3 - 2 * fx), uy = fy * fy * (3 - 2 * fy);
    const a = hsh(i, j), b = hsh(i + 1, j), c = hsh(i, j + 1), d = hsh(i + 1, j + 1); return a + (b - a) * ux + (c - a) * uy + (a - b - c + d) * ux * uy; };
  const fbm = (x, y, o) => { let v = 0, a = .5; for (let k = 0; k < (o || 4); k++) { v += a * vn(x, y); x *= 2.03; y *= 2.03; a *= .5; } return v / (1 - Math.pow(.5, o || 4)); };
  const OX = 45, OZ = 62, WL = -5.6;                    // oasis centre and water level
  const prof = f => { const c = .74; if (f < c) { const r = f / c; return .65 * r + .35 * r * r * (3 - 2 * r); } const s = (f - c) / (1 - c); return 1 - Math.sin(s * Math.PI / 2); };
  const LAM = 130, PH0 = .37;
  function dunes(x, z) {
    const w = 34 * fbm(z * .0035 + 3, x * .002, 3) + 16 * Math.sin(z * .012 + x * .002);
    const ph = (x + w) / LAM + PH0, f = ph - Math.floor(ph);
    const A = 22 * (.5 + .7 * fbm(x * .0025 + 5, z * .0025, 3));
    const u2 = (x * .5 - z * .866) / 52 + .3 * fbm(x * .006, z * .006, 2), f2 = u2 - Math.floor(u2);
    return A * prof(f) + 5 * fbm(x * .004 + 9, z * .004, 3) * prof(f2) + 10 * fbm(x * .0012, z * .0012, 3) - 8;
  }
  const Rp = th => 30 + 5 * Math.sin(3 * th + .5) + 3 * Math.sin(5 * th + 1.7);
  function H(x, z) {
    const dx = x - OX, dz = z - OZ, r = Math.hypot(dx, dz), th = Math.atan2(dz, dx), rp = Rp(th);
    const uu = x + .25 * (z - 8) + 86, rid = 38 * (uu < 0 ? Math.pow(Math.max(0, 1 + uu / 150), 1.5) : Math.exp(-uu * uu / 380)) * Math.exp(-Math.pow((z - 20) / 260, 2));
    const m = 1 - sm(50, 105, r), d = dunes(x, z) * (1 - .85 * rid / 38) + rid; if (m <= 0) return d;
    const floorH = -5 + 1.2 * fbm(x * .03, z * .03, 2), shore = r < rp ? WL - 3.2 * (1 - (r / rp) ** 2) - .3 : WL + .25 + (floorH - WL - .25) * sm(rp, rp + 16, r);
    return d + (shore - d) * m;
  }
  // ---------- scene ----------
  const S = new T.Scene();
  const SUN = new T.Vector3(Math.cos(.3) * Math.cos(.3), Math.sin(.3), Math.cos(.3) * Math.sin(.3)).normalize();   // elevation ~25 deg, ahead-right
  const HAZE = `vec3 haze(vec3 d){ float y=d.y; float s=max(dot(d,SUNDIR),0.);
      vec3 hor=vec3(.66,.31,.13), zen=vec3(.025,.035,.08), mid=vec3(.22,.14,.15);
      vec3 c = y>0. ? mix(mix(hor,mid,smoothstep(0.,.18,y)),zen,smoothstep(.12,.75,y)) : hor*.9;
      c += vec3(1.,.55,.25)*pow(s,6.)*.8 + vec3(1.,.72,.4)*pow(s,40.)*2.4;
      return c; }
`;
  const SUNDEF = `const vec3 SUNDIR=vec3(${SUN.x.toFixed(4)},${SUN.y.toFixed(4)},${SUN.z.toFixed(4)});\n`;
  const sky = new T.Mesh(new T.SphereGeometry(1800, 48, 24), new T.ShaderMaterial({ side: T.BackSide, depthWrite: false, fog: false,
    vertexShader: 'varying vec3 vP; void main(){ vP=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: SUNDEF + HAZE + `varying vec3 vP; void main(){ vec3 d=normalize(vP); vec3 c=haze(d); float s=dot(d,SUNDIR); c=mix(c,vec3(16.,9.,3.6),smoothstep(.99935,.9996,s))+vec3(.5,.3,.12)*pow(max(s,0.),900.); gl_FragColor=vec4(c,1.); }` }));
  sky.frustumCulled = false; S.add(sky);
  // terrain mesh
  const X0 = -650, X1 = 760, Z0 = -720, Z1 = 720, NX = 250, NZ = 250;
  const tg = new T.PlaneGeometry(X1 - X0, Z1 - Z0, NX, NZ); tg.rotateX(-Math.PI / 2); tg.translate((X0 + X1) / 2, 0, (Z0 + Z1) / 2);
  const tp = tg.attributes.position, tc = new Float32Array(tp.count * 3), cc = new T.Color(), sandA = new T.Color('#c98a52'), sandB = new T.Color('#a8643a'), sandC = new T.Color('#e0aa6e'), wet = new T.Color('#6a4a30'), deep = new T.Color('#0a3438'), shal = new T.Color('#2f7a72'), grass = new T.Color('#5a6a2a');
  for (let i = 0; i < tp.count; i++) { const x = tp.getX(i), z = tp.getZ(i), h = H(x, z); tp.setY(i, h);
    const r = Math.hypot(x - OX, z - OZ), rp = Rp(Math.atan2(z - OZ, x - OX));
    cc.copy(sandB).lerp(sandA, sm(-12, 6, h)).lerp(sandC, sm(8, 26, h) * .6).lerp(sandB, (fbm(x * .02, z * .02, 3) - .5) * .5);
    if (r < rp + 30) { cc.lerp(wet, sm(rp + 12, rp + 1, r) * .8); cc.lerp(grass, sm(rp + 22, rp + 6, r) * sm(rp - 1, rp + 3, r) * (.5 + .5 * fbm(x * .2, z * .2, 2)) * .85); }
    if (h < WL) cc.copy(shal).lerp(deep, sm(0, 2.6, WL - h));
    tc.set([cc.r, cc.g, cc.b], i * 3); }
  tg.setAttribute('color', new T.BufferAttribute(tc, 3)); tg.computeVertexNormals();
  // ripples + grain: height canvas -> normal map; colour grain
  const RC = 512, rcv = document.createElement('canvas'); rcv.width = rcv.height = RC; const rg = rcv.getContext('2d'), rim = rg.createImageData(RC, RC), nz = K.noise(RC, { seed: 3, octaves: 4 }).getContext('2d').getImageData(0, 0, RC, RC).data, gr = ctx.rng(9);
  // smooth wind ripples (2026-10-15, "make the ripples softer"): rounded asymmetric profile (gentle windward rise, softer lee
  // side), gently wandering crest lines, no per-pixel noise (that read as grit and sparkled in motion)
  for (let y = 0; y < RC; y++) for (let x = 0; x < RC; x++) { const i = (y * RC + x) * 4, wv = nz[i] / 255; const ph = (x + 22 * Math.sin(y / RC * 6.283 * 2) + 9 * Math.sin(y / RC * 6.283 * 5 + 1.3) + 18 * wv) / RC * 14, f = ph - Math.floor(ph);
    const r = f < .62 ? f / .62 : 1 - (f - .62) / .38, v = r * r * (3 - 2 * r) * .9 + wv * .1; const q = v * 255 | 0; rim.data[i] = rim.data[i + 1] = rim.data[i + 2] = q; rim.data[i + 3] = 255; }
  rg.putImageData(rim, 0, 0);
  rg.filter = 'blur(1.2px)'; rg.drawImage(rcv, 0, 0); rg.filter = 'none';
  const ripN = K.normalMap(rcv, 1.5); ripN.repeat.set((X1 - X0) / 22, (Z1 - Z0) / 22);
  const grain = K.tex(K.noise(256, { seed: 15, octaves: 6 }), true); grain.repeat.set((X1 - X0) / 9, (Z1 - Z0) / 9);
  const sandM = new T.MeshStandardMaterial({ vertexColors: true, map: grain, normalMap: ripN, normalScale: new T.Vector2(.42, .42), roughness: .92, metalness: 0 });
  const hazeK = { value: .0032 };
  function hazeFog(m) { m.onBeforeCompile = sh => { sh.uniforms.hazeK = hazeK;
    sh.vertexShader = 'varying vec3 vWP;\n' + sh.vertexShader.replace('#include <worldpos_vertex>', '#include <worldpos_vertex>\n vWP = (modelMatrix * vec4(transformed, 1.0)).xyz;');
    sh.fragmentShader = 'varying vec3 vWP; uniform float hazeK;\n' + SUNDEF + HAZE + sh.fragmentShader.replace('#include <fog_fragment>', `{ vec3 dv=vWP-cameraPosition; float dd=length(dv); float ff=1.-exp(-dd*dd*hazeK*hazeK); vec3 hc=haze(normalize(vec3(dv.x,max(dv.y*.3,0.),dv.z))); gl_FragColor.rgb=mix(gl_FragColor.rgb,hc,ff); }`).replace('#include <map_fragment>', '#include <map_fragment>\n diffuseColor.rgb *= 1.0;'); }; m.needsUpdate = true; return m; }
  // grain map is a mid-grey noise: lift it so it modulates instead of darkening
  sandM.onBeforeCompile = null; hazeFog(sandM); const _obc = sandM.onBeforeCompile;
  sandM.onBeforeCompile = sh => { _obc(sh); sh.fragmentShader = sh.fragmentShader.replace('diffuseColor.rgb *= 1.0;', 'diffuseColor.rgb = diffuseColor.rgb / max(texture2D(map, vMapUv).rgb, vec3(.001)) * (.82 + .36 * texture2D(map, vMapUv).r);'); };
  { const _o2 = sandM.onBeforeCompile;   // ripples fade with distance: far ripples are finer than a pixel and turned into crawling moire bands in motion (2026-10-15)
    sandM.onBeforeCompile = sh => { _o2(sh); sh.fragmentShader = sh.fragmentShader.replace('#include <normal_fragment_maps>', T.ShaderChunk.normal_fragment_maps.replace('mapN.xy *= normalScale;', 'mapN.xy *= normalScale * (1. - .9 * smoothstep(14., 60., length(vViewPosition)));')); }; }
  ripN.anisotropy = grain.anisotropy = R ? R.capabilities.getMaxAnisotropy() : 4;
  const terrain = new T.Mesh(tg, sandM); terrain.receiveShadow = true; terrain.castShadow = true; S.add(terrain);
  // ---------- light ----------
  const sun = new T.DirectionalLight('#ffc890', 3.2); sun.position.copy(SUN).multiplyScalar(400); S.add(sun, sun.target);
  sun.castShadow = true; sun.shadow.mapSize.set(2048, 2048); const sc = sun.shadow.camera; sc.left = -150; sc.right = 150; sc.top = 150; sc.bottom = -150; sc.near = 10; sc.far = 1200; sun.shadow.bias = -.0006; sun.shadow.normalBias = .6;
  R.shadowMap.enabled = true; R.shadowMap.type = T.PCFSoftShadowMap;
  const hemi = new T.HemisphereLight('#7088b0', '#8a5028', 1.45); S.add(hemi);   // strong sand bounce: shaded slip faces stay warm, not muddy
  // ---------- oasis: water (planar reflection) ----------
  const rtRef = new T.WebGLRenderTarget(ctx.W >> 1, ctx.H >> 1, { type: T.HalfFloatType, colorSpace: T.LinearSRGBColorSpace });
  const wU = { tRef: { value: rtRef.texture }, res: { value: new T.Vector2(ctx.W, ctx.H) }, time: { value: 0 }, hazeK };
  const water = new T.Mesh(new T.CircleGeometry(48, 96), new T.ShaderMaterial({ uniforms: wU, transparent: true, depthWrite: false,
    vertexShader: 'varying vec3 vWP; void main(){ vec4 w=modelMatrix*vec4(position,1.); vWP=w.xyz; gl_Position=projectionMatrix*viewMatrix*w; }',
    fragmentShader: SUNDEF + HAZE + `uniform sampler2D tRef; uniform vec2 res; uniform float time, hazeK; varying vec3 vWP;
      void main(){ vec2 q=vWP.xz; vec2 n=vec2(sin(q.x*.9+time*1.3)+sin(q.y*1.3-time*.9+q.x*.4)*.6, sin(q.y*.8+time*1.1)+sin(q.x*1.5+time*.7-q.y*.3)*.6)*.5;
        n+=vec2(sin(q.x*4.1+q.y*2.3+time*3.),sin(q.y*3.7-q.x*1.9+time*2.6))*.18;
        vec3 v=normalize(cameraPosition-vWP); float fr=.04+.96*pow(1.-max(v.y,0.),5.);
        vec2 uv=gl_FragCoord.xy/res; uv.y=1.-uv.y; uv+=n*.006;
        vec3 refl=min(texture2D(tRef,uv).rgb,vec3(.75));
        vec3 N=normalize(vec3(-n.x*.08,1.,-n.y*.08)); float sp=pow(max(dot(reflect(-v,N),SUNDIR),0.),220.)*.7;
        vec3 body=vec3(.03,.21,.19);
        vec3 c=mix(body,refl*vec3(.55,.8,.8),clamp(.12+fr*.45,0.,1.))+vec3(1.,.8,.55)*sp;
        float a=clamp(.42+fr*.4,0.,1.);
        vec3 dv=vWP-cameraPosition; float dd=length(dv); float ff=1.-exp(-dd*dd*hazeK*hazeK); c=mix(c,haze(normalize(vec3(dv.x,0.,dv.z))),ff);
        gl_FragColor=vec4(c,a);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  water.rotation.x = -Math.PI / 2; water.position.set(OX, WL, OZ); S.add(water);
  // ---------- palms (ONE mesh each) + grass tufts ----------
  const AT = 1024, ac = document.createElement('canvas'); ac.width = ac.height = AT; const g = ac.getContext('2d'), r = ctx.rng(21);
  g.clearRect(0, 0, AT, AT);
  // bark: leaf-base scars in rings, crossed
  g.fillStyle = '#5a4430'; g.fillRect(0, 0, 256, AT);
  for (let y = 0; y < AT; y += 16) for (let x = -16; x < 256; x += 32) { const ox = (y / 16 % 2) * 16; g.fillStyle = `rgba(${30 + r() * 20 | 0},${22 + r() * 14 | 0},${14 + r() * 10 | 0},.85)`; g.beginPath(); g.moveTo(x + ox, y + 14); g.lineTo(x + ox + 16, y + 2); g.lineTo(x + ox + 32, y + 14); g.closePath(); g.fill();
    g.fillStyle = `rgba(${120 + r() * 40 | 0},${92 + r() * 30 | 0},${62 + r() * 20 | 0},.5)`; g.fillRect(x + ox + 4, y + 13, 24, 2); }
  // fronds: pinnate leaflets from the rachis (u .5) toward both edges, angled forward; green and dry brown versions
  function frondTex(x0, w, col, dry) { for (let j = 0; j < 120; j++) { const y = 6 + j * 8.4; [-1, 1].forEach(sd => { const c = x0 + w / 2, L = w / 2 - 2, fy = 34 + r() * 12;
      const sh = r() * 18 - 9; g.fillStyle = dry ? `rgb(${120 + r() * 40 | 0},${84 + r() * 26 | 0},${44 + r() * 16 | 0})` : `rgb(${col[0] + r() * 22 | 0},${col[1] + r() * 30 | 0},${col[2] + r() * 14 | 0})`;
      g.beginPath(); g.moveTo(c, y); g.quadraticCurveTo(c + sd * L * .5, y + fy * .2 + sh * .3, c + sd * L, y + fy + sh); g.quadraticCurveTo(c + sd * L * .5, y + fy * .2 + 5 + sh * .3, c, y + 5); g.closePath(); g.fill(); }); }
    g.fillStyle = dry ? '#7a5a34' : '#6a7a34'; g.fillRect(x0 + w / 2 - 4, 0, 8, AT); }
  frondTex(256, 384, [52, 88, 30], false); frondTex(640, 384, 0, true);
  const atlas = new T.CanvasTexture(ac); atlas.colorSpace = T.SRGBColorSpace; atlas.flipY = false; atlas.anisotropy = 4;
  const uTime = { value: 0 };
  const plantM = new T.MeshStandardMaterial({ map: atlas, alphaTest: .45, side: T.DoubleSide, roughness: .6, metalness: 0, emissive: '#202408', emissiveIntensity: 1 });
  plantM.onBeforeCompile = sh => { sh.uniforms.uTime = uTime;
    sh.vertexShader = 'attribute vec3 sw; uniform float uTime;\n' + sh.vertexShader.replace('#include <begin_vertex>', `#include <begin_vertex>
      float ph = sw.z; float b = sw.x; float f = sw.y * sw.y;
      transformed.x += b * (.35 * sin(uTime * .7 + ph) + .12 * sin(uTime * 1.9 + ph * 2.)) + f * (.22 * sin(uTime * 2.1 + ph + position.y * .6) );
      transformed.z += b * .2 * sin(uTime * .55 + ph * 1.3) + f * .18 * sin(uTime * 1.7 + ph * 3. + position.x * .5);
      transformed.y += f * .25 * sin(uTime * 2.6 + ph * 1.7 + position.x * .7 + position.z * .4);`); };
  function Geo() { this.p = []; this.u = []; this.w = []; this.i = []; }
  Geo.prototype.add = function (x, y, z, u, v, a, b2, ph) { this.p.push(x, y, z); this.u.push(u, v); this.w.push(a, b2, ph); return this.p.length / 3 - 1; };
  Geo.prototype.build = function () { const o = new T.BufferGeometry(); o.setAttribute('position', new T.Float32BufferAttribute(this.p, 3)); o.setAttribute('uv', new T.Float32BufferAttribute(this.u, 2));
    o.setAttribute('sw', new T.Float32BufferAttribute(this.w, 3)); o.setIndex(this.i); o.computeVertexNormals(); return o; };
  function palmGeo(seed, Ht, lean, az) {
    const G = new Geo(), q = ctx.rng(seed), ph = q() * 6.28, NS = 26, NR = 12;
    // trunk spine: leans and curves back up a little
    const spine = s => [Math.cos(az) * (lean * Ht * s * s * .9 + lean * Ht * s * .25), Ht * s, Math.sin(az) * (lean * Ht * s * s * .9 + lean * Ht * s * .25)];
    const bend = s => s * s;                                          // sway weight along the trunk
    for (let k = 0; k <= NS; k++) { const s = k / NS, c = spine(s), rr = (.36 - .12 * s + .22 * Math.exp(-s * 18)) * (1 + .05 * Math.sin(s * 90));
      for (let j = 0; j <= NR; j++) { const a = j / NR * 6.283; G.add(c[0] + Math.cos(a) * rr, c[1], c[2] + Math.sin(a) * rr, j / NR * .25, s * Ht / 3.5, bend(s), 0, ph); } }
    for (let k = 0; k < NS; k++) for (let j = 0; j < NR; j++) { const a = k * (NR + 1) + j, c = a + NR + 1; G.i.push(a, c, a + 1, a + 1, c, c + 1); }
    // crown knob (leaf bases)
    const top = spine(1), tb = bend(1);
    // fronds
    const nF = 20 + (q() * 6 | 0);
    for (let f = 0; f < nF; f++) {
      const dry = f >= nF - 4, az2 = f * 2.39996 + q() * .3, el = dry ? -1.2 - q() * .2 : (f < 6 ? 1.0 + q() * .3 : .55 - (f - 6) / nF * .9 + q() * .2), droop = dry ? .2 : 1.6 + q() * .7, L = dry ? 2.6 + q() * .6 : 3.8 + q() * 1.4;
      const NSg = 16; let x = top[0], y = top[1] - .1, z = top[2]; const sv = [-Math.sin(az2), 0, Math.cos(az2)], base = G.p.length / 3;
      for (let k = 0; k < NSg; k++) { const s = k / (NSg - 1), e = el - droop * s * s, dir = [Math.cos(e) * Math.cos(az2), Math.sin(e), Math.cos(e) * Math.sin(az2)];
        const up = [dir[1] * sv[2] - dir[2] * sv[1], dir[2] * sv[0] - dir[0] * sv[2], dir[0] * sv[1] - dir[1] * sv[0]];
        const w = (dry ? .35 : .95) * Math.pow(Math.sin(Math.PI * Math.min(1, .08 + s * .97)), .7), fold = (dry ? .1 : .38) * w;
        const u0 = dry ? .625 : .25, u1 = dry ? 1 : .625;
        [[-1, 1], [0, 0], [1, 1]].forEach(([e2, m]) => G.add(x + sv[0] * e2 * w + up[0] * m * fold, y + sv[1] * e2 * w + up[1] * m * fold, z + sv[2] * e2 * w + up[2] * m * fold, u0 + (u1 - u0) * (e2 + 1) / 2, s, tb, s, ph));
        const dl = L / (NSg - 1); x += dir[0] * dl; y += dir[1] * dl; z += dir[2] * dl; }
      for (let k = 0; k < NSg - 1; k++) for (let e2 = 0; e2 < 2; e2++) { const a = base + k * 3 + e2, c = a + 3; G.i.push(a, c, a + 1, a + 1, c, c + 1); } }
    return G.build(); }
  const palms = [], pr = ctx.rng(5), palmPos = [], oasis = palms;
  for (let i = 0; i < 26; i++) { const th = i / 26 * 6.283 + (pr() - .5) * .25, rp = Rp(th), rr = rp + 3 + pr() * (i % 3 == 0 ? 16 : 8), x = OX + Math.cos(th) * rr, z = OZ + Math.sin(th) * rr;
    const Ht = 8 + pr() * 7, m = new T.Mesh(palmGeo(100 + i, Ht, .05 + pr() * .1, th + (pr() - .5) * .6), plantM); m.position.set(x, H(x, z) - .2, z); m.castShadow = true; S.add(m); palms.push(m); palmPos.push([x, z]); }
  for (let i = 0; i < 9; i++) { const th = pr() * 6.283, rr = Rp(th) + 6 + pr() * 18, x = OX + Math.cos(th) * rr, z = OZ + Math.sin(th) * rr;   // young palms
    const m = new T.Mesh(palmGeo(300 + i, 1.2 + pr() * 1.5, .02, th), plantM); m.position.set(x, H(x, z) - .1, z); m.scale.setScalar(.8); S.add(m); oasis.push(m); }
  // grass tufts: one mesh per tuft (blades from a common base), instanced
  const tuft = (() => { const G = new Geo(), q = ctx.rng(8); for (let b = 0; b < 14; b++) { const a = q() * 6.283, l = .6 + q() * .7, lean = .3 + q() * .5, w = .05, base = G.p.length / 3;
      for (let k = 0; k < 5; k++) { const s = k / 4, x = Math.cos(a) * lean * l * s * s, z = Math.sin(a) * lean * l * s * s, y = l * s, ww = w * (1 - s);
        G.add(x - Math.sin(a) * ww, y, z + Math.cos(a) * ww, .3, .5, 0, s * .6, a); G.add(x + Math.sin(a) * ww, y, z - Math.cos(a) * ww, .32, .5, 0, s * .6, a); }
      for (let k = 0; k < 4; k++) { const a0 = base + k * 2; G.i.push(a0, a0 + 2, a0 + 1, a0 + 1, a0 + 2, a0 + 3); } } return G.build(); })();
  const grassM = new T.MeshStandardMaterial({ color: '#8a9a3c', emissive: '#1c2408', roughness: .8, side: T.DoubleSide }); grassM.onBeforeCompile = plantM.onBeforeCompile;
  [plantM, grassM].forEach(m => { const a = m.onBeforeCompile; hazeFog(m); const b = m.onBeforeCompile; m.onBeforeCompile = sh => { a(sh); b(sh); }; });
  const NG = 260, gim = new T.InstancedMesh(tuft, grassM, NG), M4 = new T.Matrix4(), Q = new T.Quaternion(), V = new T.Vector3(), Sc = new T.Vector3();
  for (let i = 0; i < NG; i++) { const th = pr() * 6.283, rr = Rp(th) + .5 + Math.pow(pr(), 2) * 12, x = OX + Math.cos(th) * rr, z = OZ + Math.sin(th) * rr, s = .7 + pr() * 1.1;
    V.set(x, H(x, z) - .05, z); Q.setFromAxisAngle(new T.Vector3(0, 1, 0), pr() * 6.28); Sc.set(s, s, s); M4.compose(V, Q, Sc); gim.setMatrixAt(i, M4); }
  S.add(gim); oasis.push(gim);
  // ---------- blowing sand: grains skimming the surface downwind, + a thin veil off the crests ----------
  const NP = 3000, sand = ctx.points(NP, { size: .16, opacity: .55, color: '#ffd9a8' }), sbuf = []; const r7 = ctx.rng(31); S.add(sand); sand.frustumCulled = false;
  for (let i = 0; i < NP; i++) sbuf.push([r7(), r7(), r7(), r7()]);
  // ---------- camera path (seek-safe: splines of t) ----------
  const key = [[0, -400, -28], [4.2, -335, -22], [7.7, -280, -14], [13.5, -190, -2], [17.1, -132, 6], [20.7, -84, 8], [23.5, -60, 2], [27.5, -38, -8]];
  function path(t) { let i = 0; while (i < key.length - 2 && t > key[i + 1][0]) i++; const a = key[Math.max(0, i - 1)], b = key[i], c = key[i + 1], d = key[Math.min(key.length - 1, i + 2)];
    const s = Math.min(1, Math.max(0, (t - b[0]) / (c[0] - b[0]))); const cr = (p0, p1, p2, p3) => .5 * (2 * p1 + (-p0 + p2) * s + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s * s + (-p0 + 3 * p1 - 3 * p2 + p3) * s * s * s);
    return [cr(a[1], b[1], c[1], d[1]), cr(a[2], b[2], c[2], d[2])]; }
  // the terrain under the camera, smoothed along the path (soft maximum of samples ahead and behind) so the glide never jerks
  function ground(t) { let acc = 0; for (let k = -5; k <= 4; k++) { const q = path(t + k * .3), h = H(q[0], q[1]); acc += Math.exp(h * .35) * Math.exp(-k * k / 30); } return Math.log(acc / 5.2) / .35; }
  const quad = new T.Scene(), qcam = new T.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const rtS = new T.WebGLRenderTarget(ctx.W, ctx.H, { type: T.HalfFloatType, samples: 4, colorSpace: T.LinearSRGBColorSpace });
  const qU = { tS: { value: rtS.texture }, time: { value: 0 }, hy: { value: .5 }, amt: { value: 0 }, asp: { value: ctx.W / ctx.H } };
  const qm = new T.Mesh(new T.PlaneGeometry(2, 2), new T.ShaderMaterial({ uniforms: qU, depthTest: false, depthWrite: false,
    vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=vec4(position.xy,0.,1.); }',
    fragmentShader: `uniform sampler2D tS; uniform float time,hy,amt,asp; varying vec2 vUv;
      void main(){ vec2 uv=vUv; float band=exp(-pow((uv.y-hy)/.05,2.)), below=smoothstep(hy+.01,hy-.3,uv.y)*.45;
        float a=amt*(band+below);
        vec2 o=vec2(sin(uv.y*90.+time*2.2+sin(uv.x*9.+time*.7)*1.6)+.5*sin(uv.y*41.-time*1.6+uv.x*5.), .4*sin(uv.x*30.+time*1.4+uv.y*60.))*a*.0022;
        vec3 c=texture2D(tS,uv+o).rgb;
        float mb=smoothstep(hy-.03,hy-.008,uv.y)*(1.-smoothstep(hy-.004,hy+.001,uv.y));
        vec3 m=texture2D(tS,vec2(uv.x,2.*hy-uv.y+.006)+o*2.5).rgb; c=mix(c,m*vec3(.95,.97,1.05),mb*.6*amt);
        vec2 q=(uv-.5)*vec2(asp,1.); c*=1.-.28*smoothstep(.35,1.05,length(q));             // lens falloff
        gl_FragColor=vec4(c,1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` })); qm.frustumCulled = false; quad.add(qm);

  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .3, 4000); ctx.side(cam, p.side == null ? .1 : p.side);
  const camR = new T.PerspectiveCamera(); const clip = new T.Plane(new T.Vector3(0, 1, 0), -WL + .05), V2 = new T.Vector3(), V3 = new T.Vector3();
  return { scene: quad, camera: qcam, draw(t, u) {
    uTime.value = t; wU.time.value = t;
    // --- camera ---
    const pp = path(t), pa = path(t + 1.2), heading = Math.atan2(pa[1] - pp[1], pa[0] - pp[0]);
    const gH = ground(t), low = sm(cLow - .5, cLow + 1.5, t) * (1 - sm(cTurn - .5, cTurn + 2, t));
    const clr = 16 - low * 9 - sm(cTurn, cRev - 1.5, t) * 13 + sm(cRev - .3, cRev + 2.5, t) * 10;
    const camY = gH + clr; cam.position.set(pp[0], camY, pp[1]);
    // yaw: ahead; look right toward the sun at "sun", sweep the horizon at "empty", back ahead; at the reveal turn right/down to the oasis
    const yawSweep = sm(cEmpty, cEmpty + 2.6, t) * .38 - sm(cEmpty + 2.2, cLow, t) * .62 + sm(cLow - .5, cLow + 2, t) * .24;   // the pan stays on the sun side (2026-10-15: backlit crests, no muddy slip faces filling the frame)
    let yaw = heading + .08 * sm(cSun - .5, cSun + 1.5, t) * (1 - sm(cEmpty, cEmpty + 1.5, t)) + yawSweep;
    let pitch = -.1 + .3 * sm(cSun - .3, cSun + 1.6, t) * (1 - sm(cShim - .2, cShim + 1.2, t)) + .08 * low + .04 * sm(cEmpty, cEmpty + 2, t) * (1 - sm(cTurn, cTurn + 2, t)) + .02 * sm(cTurn, cTurn + 2, t);
    // reveal: look at the oasis
    const rv = sm(cRev - .6, cRev + 2.2, t), oy = Math.atan2(OZ - pp[1], OX - pp[0]) - .18, od = Math.hypot(OX - pp[0], OZ - pp[1]), op = Math.atan2(WL + 3 - camY, od);
    let dy = oy - yaw; dy = Math.atan2(Math.sin(dy), Math.cos(dy)); yaw += dy * rv; pitch += (op - pitch) * rv;
    V2.set(pp[0] + Math.cos(yaw) * Math.cos(pitch) * 100, camY + Math.sin(pitch) * 100, pp[1] + Math.sin(yaw) * Math.cos(pitch) * 100);
    cam.up.set(Math.sin(t * .3) * .008, 1, 0); cam.lookAt(V2);
    // --- light follows the camera for the shadow map ---
    // snapped to whole shadow texels in light space (2026-10-15: a sliding shadow camera made the palm shadows crawl)
    sun.target.position.set(pp[0] + Math.cos(yaw) * 110, 0, pp[1] + Math.sin(yaw) * 110);
    { const tx = 300 / 2048, lx = V3.set(0, 1, 0).cross(SUN).normalize(), ly = new T.Vector3().crossVectors(SUN, lx).normalize(), q = sun.target.position;
      const a = Math.round(q.dot(lx) / tx) * tx - q.dot(lx), b = Math.round(q.dot(ly) / tx) * tx - q.dot(ly); q.addScaledVector(lx, a).addScaledVector(ly, b); }
    sun.position.copy(sun.target.position).addScaledVector(SUN, 500);
    // --- sand grains: skim downwind (+x) close to the surface around the camera ---
    const sa = sand.geometry.attributes.position.array, sc2 = sand.geometry.attributes.color.array, BX = 160, BZ = 120;
    for (let i = 0; i < NP; i++) { const [a, b, c, d] = sbuf[i]; const ph = t * (.5 + d * .4) + a * 7, cyc = Math.floor(ph), f = ph - cyc;
      const x0 = cam.position.x - 20 + ((b * BX + cyc * 37.1 * (d + .3)) % BX) + f * (18 + d * 14), z0 = cam.position.z + ((c * BZ + cyc * 23.7) % BZ) - BZ / 2;
      const y = H(x0, z0) + .2 + d * 1.6 * Math.sin(f * Math.PI) + (d > .9 ? f * 4 : 0); sa.set([x0, y, z0], i * 3); const v = Math.sin(f * Math.PI) * (.35 + .65 * d); sc2.set([v, v * .86, v * .7], i * 3); }
    sand.geometry.attributes.position.needsUpdate = sand.geometry.attributes.color.needsUpdate = true;
    // --- reflection pass for the pool (only when it can be seen) ---
    const showW = t > cRev - 3;
    water.visible = false; oasis.forEach(m => m.visible = showW);
    if (showW) { cam.updateMatrixWorld(); camR.copy(cam); camR.position.set(cam.position.x, 2 * WL - cam.position.y, cam.position.z); V3.set(V2.x, 2 * WL - V2.y, V2.z); camR.up.set(0, 1, 0); camR.lookAt(V3);
      camR.projectionMatrix.copy(cam.projectionMatrix); camR.projectionMatrixInverse.copy(cam.projectionMatrixInverse);
      sky.position.copy(camR.position); R.clippingPlanes = [clip]; const sh = R.shadowMap.autoUpdate; R.setRenderTarget(rtRef); R.render(S, camR); R.clippingPlanes = []; }
    water.visible = showW;
    // --- main pass into the target, then shimmer ---
    sky.position.copy(cam.position); R.setRenderTarget(rtS); R.render(S, cam); R.setRenderTarget(null);
    V3.set(cam.position.x + Math.cos(yaw) * 3000, cam.position.y, cam.position.z + Math.sin(yaw) * 3000).project(cam); qU.hy.value = V3.y * .5 + .5;
    qU.time.value = t; qU.amt.value = Math.max(0, sm(cShim - .5, cShim + 2, t) - .6 * rv);
  } };
};
