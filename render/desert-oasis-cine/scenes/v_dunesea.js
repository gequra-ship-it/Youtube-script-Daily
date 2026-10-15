// dunesea — an ocean of sand at dusk, then an oasis (desert-oasis-cine; look C rebuild 2026-10-15). Stage scene, one terrain.
// Look C (cine_spec 3A): real 3D dune field (sinuous transverse dunes with gentle windward slopes and sharp brinks over steep
// slip faces, a cross set of smaller dunes, broad swells) drawn with light: dark sand, glowing height contours, fine wind-ripple
// lines on the gentle slopes, a cool outline on the crests, faint warm sheen where the low sun grazes, sparse warm sand points.
// Sky: navy-violet dusk with a warm band and a low glowing sun disc ahead-right, a few stars. Distance fades into the horizon glow.
// Sand blowing off the surface as points, heat shimmer + mirage band on the horizon (post pass, kept subtle).
// The camera glides over the dunes, looks toward the sun, pans over the empty horizon, drops low over a crest, climbs a big dune
// and at the reveal crests it: below lies a basin with a pool (dark mirror: planar reflection of the palms' outlines and the sky,
// glints) ringed by date palms and grass. Palms are the subject: each palm is ONE mesh (curved trunk with leaf-scar rings + crown
// of arching pinnate fronds + hanging dry fronds), dark body, warm outline (fresnel + leaflet edges cut from the frond atlas),
// faint mesh lines and points; they sway by a vertex deform whose weight grows from 0 at the root. Hidden until the reveal cue.
// params (cues): { sun: cue (look toward the sun), shimmer: cue (heat shimmer grows), empty: cue (pan over the horizon),
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
  const SUN = new T.Vector3(Math.cos(.062) * Math.cos(.3), Math.sin(.062), Math.cos(.062) * Math.sin(.3)).normalize();   // low dusk sun (~4 deg), ahead-right
  // dusk sky: navy-violet zenith, violet horizon, warm band toward the sun; also the colour distance fades into
  const SKY = `vec3 sky(vec3 d){ float y=d.y; float s=max(dot(d,SUNDIR),0.); vec2 hz=normalize(d.xz+vec2(1e-5)); float sa=max(dot(hz,normalize(SUNDIR.xz)),0.);
      vec3 horV=vec3(.040,.028,.085), horS=vec3(.17,.06,.038), mid=vec3(.015,.012,.042), zen=vec3(.0025,.0035,.014);
      vec3 hor=mix(horV,horS,pow(sa,4.));
      vec3 c = y>0. ? mix(mix(hor,mid,smoothstep(0.,.13,y+.02*sa)),zen,smoothstep(.10,.6,y)) : hor*.85;
      c += vec3(1.,.40,.16)*pow(s,14.)*.16 + vec3(1.,.55,.25)*pow(s,120.)*.9;
      return c; }
`;
  const SUNDEF = 'uniform vec3 SUNDIR;\n', uSun = { value: SUN.clone() };   // the sun sets slowly through the shot (draw)
  const sky = new T.Mesh(new T.SphereGeometry(1800, 48, 24), new T.ShaderMaterial({ side: T.BackSide, depthWrite: false, fog: false, uniforms: { SUNDIR: uSun },
    vertexShader: 'varying vec3 vP; void main(){ vP=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: SUNDEF + SKY + `varying vec3 vP; void main(){ vec3 d=normalize(vP); vec3 c=sky(d); float s=dot(d,SUNDIR);
      c=mix(c,vec3(14.,6.5,2.4),smoothstep(.99962,.99976,s)*smoothstep(-.004,.002,d.y)) + vec3(.9,.42,.16)*pow(max(s,0.),1400.)*1.5;
      gl_FragColor=vec4(c,1.); }` }));
  sky.frustumCulled = false; S.add(sky);
  // stars: upper sky only, fading toward the horizon and away from the sun glow
  { const n = 900, st = ctx.points(n, { size: 1.6, opacity: .7, color: '#cdd6ff', atten: false }), a = st.geometry.attributes.position.array, c = st.geometry.attributes.color.array, r = ctx.rng(77);
    for (let i = 0; i < n; i++) { const y = .1 + .9 * Math.pow(r(), .8), th = r() * 6.283, q = Math.sqrt(1 - y * y), d = [q * Math.cos(th), y, q * Math.sin(th)];
      const near = Math.max(0, d[0] * SUN.x + d[1] * SUN.y + d[2] * SUN.z), v = sm(.1, .45, y) * (1 - sm(.6, .95, near)) * (.25 + .75 * r() * r());
      a.set([d[0] * 1500, d[1] * 1500, d[2] * 1500], i * 3); c.set([v, v, v], i * 3); }
    st.frustumCulled = false; sky.add(st); }
  // terrain mesh
  const X0 = -650, X1 = 760, Z0 = -720, Z1 = 720, NX = 250, NZ = 250;
  const tg = new T.PlaneGeometry(X1 - X0, Z1 - Z0, NX, NZ); tg.rotateX(-Math.PI / 2); tg.translate((X0 + X1) / 2, 0, (Z0 + Z1) / 2);
  const tp = tg.attributes.position;
  for (let i = 0; i < tp.count; i++) tp.setY(i, H(tp.getX(i), tp.getZ(i)));
  tg.computeVertexNormals();
  const hazeK = { value: .0026 }, uDim = { value: 1 }, uRev = { value: 1 };
  // terrain (look C): dark sand + height contours (every 1.6, brighter every 8) + wind ripples on gentle slopes + cool crest outline
  // + warm low-sun sheen + a glint line along the shore; fades into the sky colour with distance
  const VS = 'varying vec3 vW; varying vec3 vN; void main(){ vec4 w=modelMatrix*vec4(position,1.); vW=w.xyz; vN=normalize(mat3(modelMatrix)*normal); gl_Position=projectionMatrix*viewMatrix*w; }';
  const terrainM = new T.ShaderMaterial({ uniforms: { hazeK, uDim, SUNDIR: uSun }, vertexShader: VS,
    fragmentShader: SUNDEF + SKY + `uniform float hazeK, uDim; varying vec3 vW; varying vec3 vN;
      float ln(float h, float w){ float fw=fwidth(h); return clamp(1.-abs(fract(h+.5)-.5)/(w+fw),0.,1.)*smoothstep(.6,.15,fw); }
      void main(){ vec3 N=normalize(vN); vec3 dv=vW-cameraPosition; float dd=length(dv); vec3 V=-dv/dd;
        float sun=max(dot(N,SUNDIR),0.), grz=pow(1.-abs(dot(N,V)),5.);
        float c1=ln(vW.y/.9,.04), c2=ln(vW.y/4.5,.03);
        float rp=(vW.x+5.*sin(vW.z*.061)+2.5*sin(vW.z*.19+vW.x*.021))/2.1; float rip=ln(rp,.06)*smoothstep(.86,.97,N.y)*(1.-smoothstep(40.,150.,dd));
        float od=length(vW.xz-vec2(${OX.toFixed(1)},${OZ.toFixed(1)})); float shore=exp(-pow((vW.y-(${WL.toFixed(2)})-.06)/.05,2.))*(1.-smoothstep(50.,60.,od));
        vec3 base=vec3(.008,.006,.012)+vec3(.20,.085,.035)*pow(sun,2.)*.55;
        vec3 sand=vec3(.62,.36,.16);
        vec3 c=base + sand*(c1*.11+c2*.20+rip*.10)*uDim*(.55+.9*sun) + vec3(.30,.38,1.)*grz*.16 + vec3(1.,.55,.25)*pow(sun,6.)*.06 + vec3(.8,.85,1.)*shore*.28;
        float ff=1.-exp(-dd*dd*hazeK*hazeK); c=mix(c,sky(normalize(vec3(dv.x,max(dv.y*.3,0.),dv.z))),ff);
        gl_FragColor=vec4(c,1.); }` });
  const terrain = new T.Mesh(tg, terrainM); S.add(terrain);
  S.fog = new T.FogExp2('#0c0816', .0024);                 // for the point layers
  // sparse warm sand points on the dunes (brighter where the low sun grazes)
  { const n = 7000, sp = ctx.points(n, { size: .5, opacity: 1, color: '#ffcf96', fog: true }), a = sp.geometry.attributes.position.array, c = sp.geometry.attributes.color.array, r = ctx.rng(41);
    for (let i = 0; i < n; i++) { const x = -520 + r() * 680, z = -220 + r() * 440, h = H(x, z), hx = H(x + 1, z) - h, hz = H(x, z + 1) - h, l = Math.hypot(hx, 1, hz);
      const s = Math.max(0, (-hx * SUN.x + SUN.y - hz * SUN.z) / l), v = (.2 + .8 * Math.pow(s, 2)) * (.5 + .5 * r());
      if (Math.hypot(x - OX, z - OZ) < 55) { i--; continue; }
      a.set([x, h + .08, z], i * 3); c.set([v, v * .85, v * .66], i * 3); }
    sp.frustumCulled = false; S.add(sp); }
  // ---------- oasis: water (planar reflection: dark mirror of the outlines) ----------
  const rtRef = new T.WebGLRenderTarget(ctx.W >> 2, ctx.H >> 2, { type: T.HalfFloatType, colorSpace: T.LinearSRGBColorSpace });
  const wU = { tRef: { value: rtRef.texture }, res: { value: new T.Vector2(ctx.W, ctx.H) }, time: { value: 0 }, hazeK, uRev, SUNDIR: uSun };
  const water = new T.Mesh(new T.CircleGeometry(48, 96), new T.ShaderMaterial({ uniforms: wU, transparent: true,
    vertexShader: 'varying vec3 vWP; void main(){ vec4 w=modelMatrix*vec4(position,1.); vWP=w.xyz; gl_Position=projectionMatrix*viewMatrix*w; }',
    fragmentShader: SUNDEF + SKY + `uniform sampler2D tRef; uniform vec2 res; uniform float time, hazeK, uRev; varying vec3 vWP;
      float h21(vec2 p){ return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
      void main(){ vec2 q=vWP.xz; vec2 n=vec2(sin(q.x*.9+time*1.3)+sin(q.y*1.3-time*.9+q.x*.4)*.6, sin(q.y*.8+time*1.1)+sin(q.x*1.5+time*.7-q.y*.3)*.6)*.5;
        n+=vec2(sin(q.x*4.1+q.y*2.3+time*3.),sin(q.y*3.7-q.x*1.9+time*2.6))*.18;
        vec3 v=normalize(cameraPosition-vWP); float fr=.25+.75*pow(1.-max(v.y,0.),4.);
        vec2 uv=gl_FragCoord.xy/res; uv.y=1.-uv.y; uv+=n*.004;
        vec3 refl=texture2D(tRef,uv).rgb;
        vec3 N=normalize(vec3(-n.x*.08,1.,-n.y*.08)); float sp=pow(max(dot(reflect(-v,N),SUNDIR),0.),600.)*3.;
        vec2 g=floor(q*2.2+vec2(time*.4,0.)); float gl=step(.985,h21(g+floor(time*2.)))*pow(max(sin(time*7.+h21(g)*30.),0.),3.);
        vec3 c=vec3(.002,.004,.010)+refl*.85*fr+vec3(1.,.72,.42)*(sp+gl*.9);
        vec3 dv=vWP-cameraPosition; float dd=length(dv); float ff=1.-exp(-dd*dd*hazeK*hazeK); c=mix(c,sky(normalize(vec3(dv.x,0.,dv.z))),ff);
        gl_FragColor=vec4(c,uRev); }` }));
  water.rotation.x = -Math.PI / 2; water.position.set(OX, WL, OZ); S.add(water);
  // ---------- palms (ONE mesh each) + grass tufts ----------
  // atlas: only its shapes are used now (leaflet alpha -> cut-out + glowing leaflet edges; bark scars -> faint ring lines)
  const AT = 1024, ac = document.createElement('canvas'); ac.width = ac.height = AT; const g = ac.getContext('2d'), r = ctx.rng(21);
  g.clearRect(0, 0, AT, AT);
  g.fillStyle = '#5a4430'; g.fillRect(0, 0, 256, AT);
  for (let y = 0; y < AT; y += 16) for (let x = -16; x < 256; x += 32) { const ox = (y / 16 % 2) * 16; g.fillStyle = `rgba(${30 + r() * 20 | 0},${22 + r() * 14 | 0},${14 + r() * 10 | 0},.85)`; g.beginPath(); g.moveTo(x + ox, y + 14); g.lineTo(x + ox + 16, y + 2); g.lineTo(x + ox + 32, y + 14); g.closePath(); g.fill();
    g.fillStyle = `rgba(${120 + r() * 40 | 0},${92 + r() * 30 | 0},${62 + r() * 20 | 0},.5)`; g.fillRect(x + ox + 4, y + 13, 24, 2); }
  function frondTex(x0, w, dry) { for (let j = 0; j < 120; j++) { const y = 6 + j * 8.4; [-1, 1].forEach(sd => { const c = x0 + w / 2, L = w / 2 - 2, fy = 34 + r() * 12;
      const sh = r() * 18 - 9; g.fillStyle = dry ? '#8a6038' : '#4a7a2a';
      g.beginPath(); g.moveTo(c, y); g.quadraticCurveTo(c + sd * L * .5, y + fy * .2 + sh * .3, c + sd * L, y + fy + sh); g.quadraticCurveTo(c + sd * L * .5, y + fy * .2 + 5 + sh * .3, c, y + 5); g.closePath(); g.fill(); }); }
    g.fillStyle = dry ? '#7a5a34' : '#6a7a34'; g.fillRect(x0 + w / 2 - 4, 0, 8, AT); }
  frondTex(256, 384, false); frondTex(640, 384, true);
  const atlas = new T.CanvasTexture(ac); atlas.colorSpace = T.SRGBColorSpace; atlas.flipY = false; atlas.anisotropy = 4;
  const uTime = { value: 0 };
  const SWAY = `float ph = sw.z; float b = sw.x; float f = sw.y * sw.y;
      transformed.x += b * (.35 * sin(uTime * .7 + ph) + .12 * sin(uTime * 1.9 + ph * 2.)) + f * (.22 * sin(uTime * 2.1 + ph + position.y * .6) );
      transformed.z += b * .2 * sin(uTime * .55 + ph * 1.3) + f * .18 * sin(uTime * 1.7 + ph * 3. + position.x * .5);
      transformed.y += f * .25 * sin(uTime * 2.6 + ph * 1.7 + position.x * .7 + position.z * .4);`;
  // palm material (look C subject): dark body, warm fresnel outline + glowing leaflet edges, distance fade into the dusk
  function palmMat(o) { return new T.ShaderMaterial({ side: T.DoubleSide, defines: o.atlas ? { ATLAS: 1 } : {},
    uniforms: { atlas: { value: atlas }, uTime, hazeK, uRev, SUNDIR: uSun, rim: { value: new T.Color(o.rim) }, k: { value: o.k }, ke: { value: o.ke || 0 } },
    vertexShader: `attribute vec3 sw; uniform float uTime; varying vec2 vUv; varying vec3 vW; varying vec3 vN;
      void main(){ vUv=uv; vec3 transformed=position; ${SWAY} vec4 p=vec4(transformed,1.); vec3 n=normal;
        #ifdef USE_INSTANCING
          p=instanceMatrix*p; n=mat3(instanceMatrix)*n;
        #endif
        vec4 w=modelMatrix*p; vW=w.xyz; vN=normalize(mat3(modelMatrix)*n); gl_Position=projectionMatrix*viewMatrix*w; }`,
    fragmentShader: SUNDEF + SKY + `uniform sampler2D atlas; uniform vec3 rim; uniform float k, ke, hazeK, uRev; varying vec2 vUv; varying vec3 vW; varying vec3 vN;
      void main(){ float e=0.;
        #ifdef ATLAS
          vec4 tx=texture2D(atlas,vUv); if(tx.a<.45) discard;
          if(vUv.x>.25){ vec2 o=vec2(1.2/1024.,0.); float a1=texture2D(atlas,vUv+o).a, a2=texture2D(atlas,vUv-o).a, a3=texture2D(atlas,vUv+o.yx).a, a4=texture2D(atlas,vUv-o.yx).a;
            e=smoothstep(.15,.8,1.-min(min(a1,a2),min(a3,a4))); }
          else e=smoothstep(.22,.12,dot(tx.rgb,vec3(.33)))*.35;
        #endif
        vec3 dv=vW-cameraPosition; float dd=length(dv); vec3 V=-dv/dd; vec3 N=normalize(vN);
        float f=pow(1.-abs(dot(N,V)),4.5); float back=pow(max(dot(-V,SUNDIR),0.),4.);
        float fk=1.;
        #ifdef ATLAS
          fk=vUv.x>.25?.5:1.;
        #endif
        vec3 c=vec3(.006,.004,.006)+rim*(f*k*fk*(1.+back)+e*ke*(.25+.75*f))*uRev;
        float ff=1.-exp(-dd*dd*hazeK*hazeK*.7); c=mix(c,sky(normalize(vec3(dv.x,max(dv.y*.3,0.),dv.z))),ff);
        gl_FragColor=vec4(c,1.); }` }); }
  const plantM = palmMat({ atlas: true, rim: '#ffb850', k: .9, ke: .05 }), grassM = palmMat({ rim: '#e0a048', k: .9 });
  const swayPatch = m => { m.onBeforeCompile = sh => { sh.uniforms.uTime = uTime; sh.vertexShader = 'attribute vec3 sw; uniform float uTime;\n' + sh.vertexShader.replace('#include <begin_vertex>', '#include <begin_vertex>\n' + SWAY); }; return m; };
  function Geo() { this.p = []; this.u = []; this.w = []; this.i = []; }
  Geo.prototype.add = function (x, y, z, u, v, a, b2, ph) { this.p.push(x, y, z); this.u.push(u, v); this.w.push(a, b2, ph); return this.p.length / 3 - 1; };
  Geo.prototype.build = function () { const o = new T.BufferGeometry(); o.setAttribute('position', new T.Float32BufferAttribute(this.p, 3)); o.setAttribute('uv', new T.Float32BufferAttribute(this.u, 2));
    o.setAttribute('sw', new T.Float32BufferAttribute(this.w, 3)); o.setIndex(this.i); o.computeVertexNormals(); return o; };
  function palmGeo(seed, Ht, lean, az) {
    const G = new Geo(), q = ctx.rng(seed), ph = q() * 6.28, NS = 26, NR = 12;
    const spine = s => [Math.cos(az) * (lean * Ht * s * s * .9 + lean * Ht * s * .25), Ht * s, Math.sin(az) * (lean * Ht * s * s * .9 + lean * Ht * s * .25)];
    const bend = s => s * s;                                          // sway weight along the trunk
    for (let k = 0; k <= NS; k++) { const s = k / NS, c = spine(s), rr = (.36 - .12 * s + .22 * Math.exp(-s * 18)) * (1 + .05 * Math.sin(s * 90));
      for (let j = 0; j <= NR; j++) { const a = j / NR * 6.283; G.add(c[0] + Math.cos(a) * rr, c[1], c[2] + Math.sin(a) * rr, j / NR * .25, s * Ht / 3.5, bend(s), 0, ph); } }
    for (let k = 0; k < NS; k++) for (let j = 0; j < NR; j++) { const a = k * (NR + 1) + j, c = a + NR + 1; G.i.push(a, c, a + 1, a + 1, c, c + 1); }
    const top = spine(1), tb = bend(1);
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
  // faint mesh lines + vertex points on a palm, swaying with it (they share the palm geometry, the sway runs in the shader)
  const dressMats = [];
  function dressPalm(m, n, size) { const d = K.lookC.dress(m, { points: n, size, lines: .012, color: '#ffb850', pointColor: '#ffe0a0', opacity: .9 });
    swayPatch(d.lines.material); d.lines.material.fog = true; swayPatch(d.points.material); d.points.material.fog = true; d.points.geometry.setAttribute('sw', m.geometry.attributes.sw); dressMats.push([d.lines.material, d.lines.material.opacity], [d.points.material, d.points.material.opacity]); }
  const palms = [], pr = ctx.rng(5), oasis = palms;
  for (let i = 0; i < 26; i++) { const th = i / 26 * 6.283 + (pr() - .5) * .25, rp = Rp(th), rr = rp + 3 + pr() * (i % 3 == 0 ? 16 : 8), x = OX + Math.cos(th) * rr, z = OZ + Math.sin(th) * rr;
    const Ht = 8 + pr() * 7, m = new T.Mesh(palmGeo(100 + i, Ht, .05 + pr() * .1, th + (pr() - .5) * .6), plantM); m.position.set(x, H(x, z) - .2, z); m.frustumCulled = false; dressPalm(m, 170, .09); S.add(m); palms.push(m); }
  for (let i = 0; i < 9; i++) { const th = pr() * 6.283, rr = Rp(th) + 6 + pr() * 18, x = OX + Math.cos(th) * rr, z = OZ + Math.sin(th) * rr;   // young palms
    const m = new T.Mesh(palmGeo(300 + i, 1.2 + pr() * 1.5, .02, th), plantM); m.position.set(x, H(x, z) - .1, z); m.scale.setScalar(.8); dressPalm(m, 60, .06); S.add(m); oasis.push(m); }
  // grass tufts: one mesh per tuft (blades from a common base), instanced; a warm point at each tuft
  const tuft = (() => { const G = new Geo(), q = ctx.rng(8); for (let b = 0; b < 14; b++) { const a = q() * 6.283, l = .6 + q() * .7, lean = .3 + q() * .5, w = .05, base = G.p.length / 3;
      for (let k = 0; k < 5; k++) { const s = k / 4, x = Math.cos(a) * lean * l * s * s, z = Math.sin(a) * lean * l * s * s, y = l * s, ww = w * (1 - s);
        G.add(x - Math.sin(a) * ww, y, z + Math.cos(a) * ww, .3, .5, 0, s * .6, a); G.add(x + Math.sin(a) * ww, y, z - Math.cos(a) * ww, .32, .5, 0, s * .6, a); }
      for (let k = 0; k < 4; k++) { const a0 = base + k * 2; G.i.push(a0, a0 + 2, a0 + 1, a0 + 1, a0 + 2, a0 + 3); } } return G.build(); })();
  const NG = 260, gim = new T.InstancedMesh(tuft, grassM, NG), M4 = new T.Matrix4(), Q = new T.Quaternion(), V = new T.Vector3(), Sc = new T.Vector3();
  const gpts = ctx.points(NG, { size: .14, opacity: .9, color: '#ffd890', fog: true }), gpa = gpts.geometry.attributes.position.array;
  for (let i = 0; i < NG; i++) { const th = pr() * 6.283, rr = Rp(th) + .5 + Math.pow(pr(), 2) * 12, x = OX + Math.cos(th) * rr, z = OZ + Math.sin(th) * rr, s = .7 + pr() * 1.1;
    V.set(x, H(x, z) - .05, z); Q.setFromAxisAngle(new T.Vector3(0, 1, 0), pr() * 6.28); Sc.set(s, s, s); M4.compose(V, Q, Sc); gim.setMatrixAt(i, M4); gpa.set([x, V.y + .9 * s, z], i * 3); }
  gim.frustumCulled = false; S.add(gim); oasis.push(gim); gpts.frustumCulled = false; S.add(gpts); oasis.push(gpts); dressMats.push([gpts.material, gpts.material.opacity]);
  // ---------- blowing sand: grains skimming the surface downwind ----------
  const NP = 2400, sand = ctx.points(NP, { size: .13, opacity: .6, color: '#ffd9a8' }), sbuf = []; const r7 = ctx.rng(31); S.add(sand); sand.frustumCulled = false;
  for (let i = 0; i < NP; i++) sbuf.push([r7(), r7(), r7(), r7()]);
  // ---------- camera path (seek-safe: splines of t) ----------
  const key = [[0, -400, -28], [4.2, -335, -22], [7.7, -280, -14], [13.5, -190, -2], [17.1, -132, 6], [20.7, -84, 8], [23.5, -60, 2], [27.5, -38, -8]];
  function path(t) { let i = 0; while (i < key.length - 2 && t > key[i + 1][0]) i++; const a = key[Math.max(0, i - 1)], b = key[i], c = key[i + 1], d = key[Math.min(key.length - 1, i + 2)];
    const s = Math.min(1, Math.max(0, (t - b[0]) / (c[0] - b[0]))); const cr = (p0, p1, p2, p3) => .5 * (2 * p1 + (-p0 + p2) * s + (2 * p0 - 5 * p1 + 4 * p2 - p3) * s * s + (-p0 + 3 * p1 - 3 * p2 + p3) * s * s * s);
    return [cr(a[1], b[1], c[1], d[1]), cr(a[2], b[2], c[2], d[2])]; }
  function ground(t) { let acc = 0; for (let k = -5; k <= 4; k++) { const q = path(t + k * .3), h = H(q[0], q[1]); acc += Math.exp(h * .35) * Math.exp(-k * k / 30); } return Math.log(acc / 5.2) / .35; }
  // ---------- post: heat shimmer + mirage band (subtle), lens falloff, tone mapping ----------
  const quad = new T.Scene(), qcam = new T.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const rtS = new T.WebGLRenderTarget(ctx.W, ctx.H, { type: T.HalfFloatType, samples: 0, colorSpace: T.LinearSRGBColorSpace });
  const qU = { tS: { value: rtS.texture }, time: { value: 0 }, hy: { value: .5 }, amt: { value: 0 }, asp: { value: ctx.W / ctx.H } };
  const qm = new T.Mesh(new T.PlaneGeometry(2, 2), new T.ShaderMaterial({ uniforms: qU, depthTest: false, depthWrite: false,
    vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=vec4(position.xy,0.,1.); }',
    fragmentShader: `uniform sampler2D tS; uniform float time,hy,amt,asp; varying vec2 vUv;
      void main(){ vec2 uv=vUv; float band=exp(-pow((uv.y-hy)/.04,2.)), below=smoothstep(hy+.01,hy-.25,uv.y)*.3;
        float a=amt*(band+below);
        vec2 o=vec2(sin(uv.y*520.+time*11.+sin(uv.x*36.+time*2.3)*2.4)+.6*sin(uv.y*210.-time*7.+uv.x*14.), .5*sin(uv.x*120.+time*6.+uv.y*260.))*a*.0012;
        vec3 c=texture2D(tS,uv+o).rgb;
        float mb=smoothstep(hy-.025,hy-.007,uv.y)*(1.-smoothstep(hy-.004,hy+.001,uv.y));
        vec3 m=texture2D(tS,vec2(uv.x,2.*hy-uv.y+.006)+o*2.5).rgb; c=mix(c,m,mb*.45*amt);
        vec2 q=(uv-.5)*vec2(asp,1.); c*=1.-.3*smoothstep(.35,1.05,length(q));
        gl_FragColor=vec4(c,1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` })); qm.frustumCulled = false; quad.add(qm);

  const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .3, 4000); ctx.side(cam, p.side == null ? .1 : p.side);
  const camR = new T.PerspectiveCamera(); const clip = new T.Plane(new T.Vector3(0, 1, 0), -WL + .05), V2 = new T.Vector3(), V3 = new T.Vector3();
  return { scene: quad, camera: qcam, draw(t, u) {
    uTime.value = t; wU.time.value = t;
    { const el = .062 - .105 * sm(cLow, cRev, t); uSun.value.set(Math.cos(el) * Math.cos(.3), Math.sin(el), Math.cos(el) * Math.sin(.3)); }
    // --- camera ---
    const pp = path(t), pa = path(t + 1.2), heading = Math.atan2(pa[1] - pp[1], pa[0] - pp[0]);
    const gH = ground(t), low = sm(cLow - .5, cLow + 1.5, t) * (1 - sm(cTurn - .5, cTurn + 2, t));
    const clr = 16 - low * 9 - sm(cTurn, cRev - 1.5, t) * 13 + sm(cRev - .3, cRev + 2.5, t) * 15;
    const camY = gH + clr; cam.position.set(pp[0], camY, pp[1]);
    // yaw: ahead; turn toward the low sun at "sun", sweep the horizon at "empty", back ahead; at the reveal turn right/down to the oasis
    const yawSweep = sm(cEmpty, cEmpty + 2.6, t) * .55 - sm(cEmpty + 2.2, cLow, t) * 1.1 + sm(cLow - .5, cLow + 2, t) * .55;
    let yaw = heading + .12 * sm(cSun - .5, cSun + 1.5, t) * (1 - sm(cEmpty, cEmpty + 1.5, t)) + yawSweep;
    let pitch = -.1 + .1 * sm(cSun - .3, cSun + 1.6, t) * (1 - sm(cShim + .5, cEmpty + .5, t)) + .04 * low + .02 * sm(cTurn, cTurn + 2, t);
    const rv = sm(cRev - .6, cRev + 2.2, t), oy = Math.atan2(OZ - pp[1], OX - pp[0]) - .25, od = Math.hypot(OX - pp[0], OZ - pp[1]), op = Math.atan2(WL + 3 - camY, od);
    let dy = oy - yaw; dy = Math.atan2(Math.sin(dy), Math.cos(dy)); yaw += dy * rv; pitch += (op - pitch) * rv;
    V2.set(pp[0] + Math.cos(yaw) * Math.cos(pitch) * 100, camY + Math.sin(pitch) * 100, pp[1] + Math.sin(yaw) * Math.cos(pitch) * 100);
    cam.up.set(Math.sin(t * .3) * .008, 1, 0); cam.lookAt(V2);
    uDim.value = 1 - .35 * rv;                               // the dunes step back a little when the palms arrive
    // --- sand grains: skim downwind (+x) close to the surface around the camera ---
    const sa = sand.geometry.attributes.position.array, sc2 = sand.geometry.attributes.color.array, BX = 160, BZ = 120;
    for (let i = 0; i < NP; i++) { const [a, b, c, d] = sbuf[i]; const ph = t * (.5 + d * .4) + a * 7, cyc = Math.floor(ph), f = ph - cyc;
      const x0 = cam.position.x - 20 + ((b * BX + cyc * 37.1 * (d + .3)) % BX) + f * (18 + d * 14), z0 = cam.position.z + ((c * BZ + cyc * 23.7) % BZ) - BZ / 2;
      const y = H(x0, z0) + .2 + d * 1.6 * Math.sin(f * Math.PI) + (d > .9 ? f * 4 : 0); sa.set([x0, y, z0], i * 3); const v = Math.sin(f * Math.PI) * (.25 + .6 * d); sc2.set([v, v * .8, v * .58], i * 3); }
    sand.geometry.attributes.position.needsUpdate = sand.geometry.attributes.color.needsUpdate = true;
    // --- reflection pass for the pool (only once the oasis can be seen) ---
    const showW = t > cRev - .15, lit = sm(cRev - .15, cRev + 1, t); uRev.value = lit;
    dressMats.forEach(([m, o]) => m.opacity = o * lit);
    water.visible = false; oasis.forEach(m => m.visible = showW);
    if (showW) { cam.updateMatrixWorld(); camR.copy(cam); camR.position.set(cam.position.x, 2 * WL - cam.position.y, cam.position.z); V3.set(V2.x, 2 * WL - V2.y, V2.z); camR.up.set(0, 1, 0); camR.lookAt(V3);
      camR.projectionMatrix.copy(cam.projectionMatrix); camR.projectionMatrixInverse.copy(cam.projectionMatrixInverse);
      sky.position.copy(camR.position); R.clippingPlanes = [clip]; R.setRenderTarget(rtRef); R.render(S, camR); R.clippingPlanes = []; }
    water.visible = showW;
    // --- main pass into the target, then shimmer ---
    sky.position.copy(cam.position); R.setRenderTarget(rtS); R.render(S, cam); R.setRenderTarget(null);
    V3.set(cam.position.x + Math.cos(yaw) * 3000, cam.position.y, cam.position.z + Math.sin(yaw) * 3000).project(cam); qU.hy.value = V3.y * .5 + .5;
    qU.time.value = t; qU.amt.value = .25 + .5 * sm(cShim - .5, cShim + 1.5, t) - .5 * rv;
  } };
};
