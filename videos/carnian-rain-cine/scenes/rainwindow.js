// rainwindow — a window at night seen from inside a dark room, rain running down the glass (carnian-rain-cine, 2026-10-14).
// Real 3D: wall with a deep window reveal, beveled outer frame, two sashes with glazing bars, interior sill, a candle in a glass jar
// and a glazed mug on the sill, a heavy curtain. The glass is a refraction shader: the outside world (wet street, houses with lit
// windows, sodium street lamps, hills, cloud ceiling, rain streaks, distant lightning) is rendered first into a mip-mapped target,
// and the glass shows it blurred by condensation, sharp and inverted inside the drops and the trails the running drops wipe clear.
// Time passes: from `cycle` the light runs through days and nights faster and faster (the candle burns down), the rain never stops.
// params (cues): { stop: cue (the rain thickens), cycle: cue (days start to pass), fast: cue (the cycle accelerates),
//   push: cue (shot end: the camera pushes into the glass before it), side: .1 }
(window.MIYA = window.MIYA || { scenes: {} }).scenes.rainwindow = function (ctx, p) {
  const { T, sm, cue } = ctx, K = window.MIYA.kit, R = ctx.R;
  const tStop = cue(p.stop, 1e9), tCyc = cue(p.cycle, 1e9), tPush = cue(p.push, ctx.t1);

  // ---------- time of day (seek-safe: closed form of the accelerating clock) ----------
  const r0 = .11, kk = .4;
  const days = t => .08 + (t < tCyc ? 0 : r0 / kk * (Math.exp(kk * (Math.min(t, tPush) - tCyc)) - 1));
  const rate = t => t < tCyc ? 0 : r0 * Math.exp(kk * (Math.min(t, tPush) - tCyc));
  // daylight 0..1 for a day fraction (0 = midnight); at high speed the swing averages out (like a long exposure)
  function light(t) { const d = days(t), f = d - Math.floor(d), rt = rate(t);
    const raw = sm(.2, .34, f) * (1 - sm(.66, .8, f)), warm = Math.exp(-Math.pow((f - .27) / .04, 2)) + Math.exp(-Math.pow((f - .73) / .04, 2));
    const a = 1 / (1 + Math.pow(rt / 1.1, 2)), mean = .42;
    return { day: mean + (raw - mean) * a, warm: warm * a, d }; }

  // ---------- outside world (rendered into a target, shown through the glass) ----------
  const O = new T.Scene(); O.fog = new T.FogExp2('#0a1220', .012);
  const skyU = { night: { value: new T.Color('#0a1424') }, dayc: { value: new T.Color('#4a5868') }, warm: { value: 0 }, day: { value: 0 }, flash: { value: 0 }, fpos: { value: new T.Vector2(.3, .2) }, time: { value: 0 } };
  const dome = new T.Mesh(new T.SphereGeometry(400, 48, 24), new T.ShaderMaterial({ side: T.BackSide, depthWrite: false, fog: false, uniforms: skyU,
    vertexShader: 'varying vec3 vP; void main(){ vP=normalize(position); gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: `uniform vec3 night,dayc; uniform float warm,day,flash,time; uniform vec2 fpos; varying vec3 vP;
      float h(vec2 p){ return fract(sin(dot(p,vec2(127.1,311.7)))*43758.5453); }
      float n(vec2 p){ vec2 i=floor(p),f=fract(p); f=f*f*(3.-2.*f); return mix(mix(h(i),h(i+vec2(1,0)),f.x),mix(h(i+vec2(0,1)),h(i+vec2(1,1)),f.x),f.y); }
      float fbm(vec2 p){ float v=0.,a=.5; for(int i=0;i<5;i++){ v+=a*n(p); p*=2.03; a*=.5; } return v; }
      void main(){ float y=max(vP.y,0.); vec2 q=vP.xz/(y+.12)*1.4; float c=fbm(q+vec2(time*.05,time*.02)); float c2=fbm(q*2.3-vec2(time*.08,0.));
        vec3 base=mix(night,dayc,day); vec3 col=base*(.55+.7*c+.25*c2);
        col+=vec3(1.,.55,.35)*warm*.35*exp(-y*6.);                       // dawn / dusk band low in the sky
        col+=vec3(.9,.45,.25)*.06*(1.-day)*exp(-y*9.);                    // town glow under the clouds at night
        float fd=length(vP.xz/(y+.3)-fpos*3.); col+=vec3(.75,.8,1.)*flash*(.35+1.4*exp(-fd*.6))*(.4+c);
        col*=mix(1.,.6,smoothstep(.0,.6,y));
        gl_FragColor=vec4(col,1.); }` }));
  O.add(dome);
  const oHemi = new T.HemisphereLight('#7088a8', '#0a0a10', .2); O.add(oHemi);
  const oSun = new T.DirectionalLight('#aab8cc', .3); oSun.position.set(10, 30, -20); O.add(oSun);
  // ground: wet street + lawns, a row of houses, lamps along the street, hills behind
  const ANI = R ? R.capabilities.getMaxAnisotropy() : 4;   // stable in motion: max anisotropy on tiled maps
  const gTexC = K.noise(256, { seed: 4, octaves: 5 }), gNorm = K.normalMap(gTexC, 2); gNorm.repeat.set(20, 20); gNorm.anisotropy = ANI;
  const ground = new T.Mesh(new T.PlaneGeometry(600, 400), new T.MeshStandardMaterial({ color: '#141a1c', roughness: .35, metalness: .1, normalMap: gNorm, normalScale: new T.Vector2(.3, .3) }));
  ground.rotation.x = -Math.PI / 2; ground.position.set(0, -3.5, -200); O.add(ground);
  const road = new T.Mesh(new T.PlaneGeometry(400, 9), new T.MeshStandardMaterial({ color: '#07090c', roughness: .08, metalness: .3 })); road.rotation.x = -Math.PI / 2; road.position.set(0, -3.45, -22); O.add(road);
  const rr = ctx.rng(11), houses = [], winMats = [];
  const wallM = new T.MeshStandardMaterial({ color: '#2a2a2e', roughness: .9 }), roofM = new T.MeshStandardMaterial({ color: '#15171c', roughness: .6, metalness: .2 });
  for (let i = 0; i < 16; i++) {
    const g = new T.Group(), w = 7 + rr() * 5, d = 6 + rr() * 3, h = 4 + rr() * 3.5, x = -95 + i * 12.5 + (rr() - .5) * 4, z = -38 - rr() * 30 - (i % 3) * 12;
    const b = new T.Mesh(new T.BoxGeometry(w, h, d), wallM); b.position.y = h / 2; g.add(b);
    const roof = new T.Mesh(new T.CylinderGeometry(.01, d * .62, w + .6, 3, 1), roofM); roof.rotation.set(0, 0, Math.PI / 2); roof.scale.set(1, 1, .55); roof.position.y = h + d * .16; g.add(roof);
    const wm = new T.MeshBasicMaterial({ color: new T.Color('#ffb060') }); winMats.push(wm);
    const nw = 2 + (rr() * 3 | 0); for (let k = 0; k < nw; k++) { const wn = new T.Mesh(new T.PlaneGeometry(1.1, 1.3), wm); wn.position.set(-w / 2 + (k + .7) * w / (nw + .4), h * (k % 2 ? .62 : .32), d / 2 + .02); g.add(wn); }
    g.position.set(x, -3.5, z); g.rotation.y = (rr() - .5) * .3; O.add(g); houses.push({ g, wm, seed: rr() * 100, warm: rr() });
  }
  const lamps = [], lampHead = new T.MeshBasicMaterial({ color: new T.Color('#ffb466').multiplyScalar(14) }), poleM = new T.MeshStandardMaterial({ color: '#111', roughness: .6 });
  for (let i = 0; i < 7; i++) { const x = -48 + i * 17, z = -19 - (i % 2) * 6;
    const pole = new T.Mesh(new T.CylinderGeometry(.09, .12, 6, 8), poleM); pole.position.set(x, -.5, z); O.add(pole);
    const head = new T.Mesh(new T.SphereGeometry(.28, 12, 8), lampHead); head.position.set(x, 2.6, z); O.add(head);
    const gl = ctx.glow(O, '#ffa860', 9, .5); gl.position.copy(head.position); const pl = new T.PointLight('#ffa050', 0, 26, 1.6); pl.position.set(x, 2.3, z); O.add(pl); lamps.push({ head, gl, pl }); }
  // hills: dark ridges with a noisy top edge
  [[-120, 22, '#0c1218', 3], [-190, 40, '#0f1620', 7], [-280, 70, '#131b26', 9]].forEach(([z, hgt, col, sd]) => {
    const g = new T.PlaneGeometry(900, hgt, 160, 1), P = g.attributes.position, r2 = ctx.rng(sd);
    const ph = [r2() * 6, r2() * 6, r2() * 6]; for (let i = 0; i < P.count; i++) if (P.getY(i) > 0) { const x = P.getX(i); P.setY(i, hgt / 2 * (.3 + .35 * Math.sin(x * .011 + ph[0]) + .25 * Math.sin(x * .031 + ph[1]) + .1 * Math.sin(x * .09 + ph[2]))); }
    const m = new T.Mesh(g, new T.MeshStandardMaterial({ color: col, roughness: 1 })); m.position.set(0, -3.5 + hgt * .2, z); O.add(m); });
  // trees in the yards (one merged mesh each: trunk + crown blobs), dark silhouettes against the cloud glow
  const treeG = (() => { const parts = [new T.CylinderGeometry(.18, .3, 5, 8).translate(0, 2.5, 0)]; const r3 = ctx.rng(31);
    for (let k = 0; k < 9; k++) { const s = new T.IcosahedronGeometry(1.6 + r3() * 1.2, 2); s.translate((r3() - .5) * 3, 5.2 + r3() * 3, (r3() - .5) * 3); parts.push(s); }
    return merge(parts); })();
  const treeM = new T.MeshStandardMaterial({ color: '#0b120e', roughness: 1 });
  for (let i = 0; i < 9; i++) { const tr = new T.Mesh(treeG, treeM); tr.position.set(-70 + i * 18 + rr() * 6, -3.5, -30 - rr() * 14); tr.scale.setScalar(.8 + rr() * .6); O.add(tr); }
  // lightning bolts: jagged ribbons, one per strike
  const strikes = [[2.3, -60, -260], [5.3, 90, -300], [8.6, -20, -240], [10.4, 120, -320], [11.9, 40, -260], [12.9, -90, -300], [13.7, 10, -230]];
  const bolts = strikes.map(([, x, z], i) => { const r4 = ctx.rng(50 + i), pts = []; let px = x, py = 120; while (py > -3) { pts.push([px, py]); px += (r4() - .5) * 14; py -= 6 + r4() * 9; } pts.push([px, -3.5]);
    const pos = []; for (let k = 0; k < pts.length - 1; k++) { const [x0, y0] = pts[k], [x1, y1] = pts[k + 1], w = 1.2 * (1 - k / pts.length) + .4; pos.push(x0 - w, y0, 0, x0 + w, y0, 0, x1 + w, y1, 0, x0 - w, y0, 0, x1 + w, y1, 0, x1 - w, y1, 0); }
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(new Float32Array(pos), 3));
    const m = new T.Mesh(g, new T.MeshBasicMaterial({ color: new T.Color('#dfe6ff').multiplyScalar(6), transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, fog: false, side: T.DoubleSide }));
    m.position.z = z; O.add(m); return m; });
  const flashAt = (t, ts) => { const dt = t - ts; if (dt < 0 || dt > 1.4) return 0; return Math.exp(-dt * 4.5) * (.55 + .45 * Math.cos(dt * 38)) * (dt < .05 ? dt / .05 : 1); };
  // rain streaks outside (a box in front of the window)
  const NR = 3500, rainG = new T.BufferGeometry(), rp = new Float32Array(NR * 6), rb = []; const r5 = ctx.rng(77);
  for (let i = 0; i < NR; i++) rb.push([(r5() - .5) * 40, r5() * 24, -1.5 - Math.pow(r5(), .8) * 34, r5()]);
  rainG.setAttribute('position', new T.BufferAttribute(rp, 3));
  const rainM = new T.LineBasicMaterial({ color: '#9fb4d0', transparent: true, opacity: .35, blending: T.AdditiveBlending, depthWrite: false, fog: false });
  O.add(new T.LineSegments(rainG, rainM));

  const rtOut = new T.WebGLRenderTarget(ctx.W >> 1, ctx.H >> 1, { type: T.HalfFloatType, samples: 4, generateMipmaps: true, minFilter: T.LinearMipmapLinearFilter, magFilter: T.LinearFilter, colorSpace: T.LinearSRGBColorSpace });

  // ---------- room ----------
  const S = new T.Scene(); S.background = new T.Color('#020306');
  const OW = 1.9, OH = 2.0, OY = 1.95;           // window opening (width, height, centre height), glass at z = 0
  const plC = K.noise(256, { seed: 8, octaves: 6 }), plN = K.normalMap(plC, 1.2); plN.repeat.set(3, 3); plN.anisotropy = ANI;
  const wallM2 = new T.MeshStandardMaterial({ color: '#4a4440', roughness: .92, normalMap: plN, normalScale: new T.Vector2(.25, .25) });
  const wsh = new T.Shape(); wsh.moveTo(-6, -.5); wsh.lineTo(6, -.5); wsh.lineTo(6, 3.6); wsh.lineTo(-6, 3.6); wsh.lineTo(-6, -.5);
  const hole = new T.Path(); hole.moveTo(-OW / 2, OY - OH / 2); hole.lineTo(-OW / 2, OY + OH / 2); hole.lineTo(OW / 2, OY + OH / 2); hole.lineTo(OW / 2, OY - OH / 2); hole.lineTo(-OW / 2, OY - OH / 2); wsh.holes.push(hole);
  const wallG = new T.ExtrudeGeometry(wsh, { depth: .4, bevelEnabled: false }); wallG.translate(0, 0, -.18); S.add(new T.Mesh(wallG, wallM2));
  const ceil = new T.Mesh(new T.PlaneGeometry(12, 8), new T.MeshStandardMaterial({ color: '#2a2622', roughness: 1 })); ceil.rotation.x = Math.PI / 2; ceil.position.set(0, 3.6, 4); S.add(ceil);
  const floor = new T.Mesh(new T.PlaneGeometry(12, 8), new T.MeshStandardMaterial({ color: '#1b1410', roughness: .5 })); floor.rotation.x = -Math.PI / 2; floor.position.set(0, -.5, 4); S.add(floor);
  // frames: beveled rectangular rings (outer frame, two sashes) + glazing bars
  const paint = new T.MeshStandardMaterial({ color: '#b9b1a2', roughness: .5, metalness: 0 });
  function ring(w, h, b, d) { const s = new T.Shape(); s.moveTo(-w / 2, -h / 2); s.lineTo(w / 2, -h / 2); s.lineTo(w / 2, h / 2); s.lineTo(-w / 2, h / 2); s.lineTo(-w / 2, -h / 2);
    const iw = w / 2 - b, ih = h / 2 - b, hp = new T.Path(); hp.moveTo(-iw, -ih); hp.lineTo(-iw, ih); hp.lineTo(iw, ih); hp.lineTo(iw, -ih); hp.lineTo(-iw, -ih); s.holes.push(hp);
    const g = new T.ExtrudeGeometry(s, { depth: d, bevelEnabled: true, bevelThickness: .012, bevelSize: .012, bevelSegments: 3 }); g.translate(0, 0, -d / 2); return g; }
  function bar(len, w, d) { const s = new T.Shape(); s.moveTo(-len / 2, -w / 2); s.lineTo(len / 2, -w / 2); s.lineTo(len / 2, w / 2); s.lineTo(-len / 2, w / 2); s.lineTo(-len / 2, -w / 2);
    const g = new T.ExtrudeGeometry(s, { depth: d, bevelEnabled: true, bevelThickness: .008, bevelSize: .008, bevelSegments: 2 }); g.translate(0, 0, -d / 2); return g; }
  const fr = new T.Mesh(ring(OW, OH, .085, .12), paint); fr.position.set(0, OY, .01); S.add(fr);
  const SW = (OW - .17) / 2, SH = OH - .17;
  [-1, 1].forEach(sd => { const s = new T.Mesh(ring(SW, SH, .065, .07), paint); s.position.set(sd * SW / 2, OY, .03); S.add(s);
    const b = new T.Mesh(bar(SW - .1, .035, .045), paint); b.position.set(sd * SW / 2, OY + SH * .17, .03); S.add(b); });
  const sill = new T.Mesh(new T.BoxGeometry(OW + .5, .05, .38), paint); sill.position.set(0, OY - OH / 2 - .02, .2); S.add(sill);
  const apron = new T.Mesh(new T.BoxGeometry(OW + .3, .14, .03), paint); apron.position.set(0, OY - OH / 2 - .12, .235); S.add(apron);
  // candle in a glass jar + a glazed mug on the sill (left part of the sill, so the pane stays clear)
  const sy = OY - OH / 2 + .005, cx = -.55, cz = .24;
  const jarG = new T.LatheGeometry([[0, 0], [.055, 0], [.062, .01], [.064, .13], [.06, .14], [.056, .135], [.058, .015], [0, .012]].map(([a, b]) => new T.Vector2(a, b)), 40);
  const jar = new T.Mesh(jarG, new T.MeshPhysicalMaterial({ color: '#e8d8c0', roughness: .05, transmission: 0, transparent: true, opacity: .22, envMap: ctx.env(), envMapIntensity: 1.5, depthWrite: false })); jar.position.set(cx, sy, cz); S.add(jar);
  const waxM = new T.MeshStandardMaterial({ color: '#d8c7a8', roughness: .7, emissive: '#ff9a40', emissiveIntensity: .25 });
  const wax = new T.Mesh(new T.CylinderGeometry(.05, .05, 1, 32), waxM); S.add(wax);
  const wick = new T.Mesh(new T.CylinderGeometry(.002, .002, .015, 6), new T.MeshBasicMaterial({ color: '#111' })); S.add(wick);
  const flameT = ctx.ctex(64, (g, s) => { const r = g.createRadialGradient(s / 2, s * .62, 0, s / 2, s * .55, s * .5); r.addColorStop(0, 'rgba(255,250,230,1)'); r.addColorStop(.3, 'rgba(255,190,90,.9)'); r.addColorStop(1, 'rgba(255,120,30,0)'); g.fillStyle = r; g.fillRect(0, 0, s, s); });
  const flame = new T.Sprite(new T.SpriteMaterial({ map: flameT, color: new T.Color(2.2, 1.8, 1.4), transparent: true, blending: T.AdditiveBlending, depthWrite: false })); flame.scale.set(.03, .06, 1); S.add(flame);
  const halo = ctx.glow(S, '#ffb060', .5, .35), halo2 = ctx.glow(S, '#ff9a40', 1.6, .08);
  const candleL = new T.PointLight('#ffa860', 1.2, 0, 2); S.add(candleL);
  const mugG = new T.LatheGeometry([[0, 0], [.04, 0], [.045, .005], [.046, .095], [.042, .1], [.038, .095], [.037, .012], [0, .01]].map(([a, b]) => new T.Vector2(a, b)), 40);
  const mugM = new T.MeshPhysicalMaterial({ color: '#1f4a4a', roughness: .3, clearcoat: .8, clearcoatRoughness: .15, envMap: ctx.env(), envMapIntensity: .5 });
  const mug = new T.Group(); mug.add(new T.Mesh(mugG, mugM)); const hnd = new T.Mesh(new T.TorusGeometry(.028, .008, 10, 24, Math.PI), mugM); hnd.rotation.z = -Math.PI / 2; hnd.position.set(.046, .05, 0); mug.add(hnd);
  mug.position.set(-.78, sy, .3); mug.rotation.y = .9; S.add(mug);
  // curtain: a heavy drape with folds on the left of the window, swaying a little in the draught
  const cg = new T.PlaneGeometry(1.15, 3.9, 90, 30), cP = cg.attributes.position, cb = cP.array.slice();
  const curtain = new T.Mesh(cg, new T.MeshPhysicalMaterial({ color: '#2e2a33', roughness: .85, sheen: 1, sheenColor: new T.Color('#8a7a9a'), sheenRoughness: .5, side: T.DoubleSide }));
  curtain.position.set(-OW / 2 - .52, 1.55, .38); S.add(curtain);
  S.add(new T.HemisphereLight('#3a4660', '#0a0806', .3));
  const winL = new T.DirectionalLight('#8aa0c0', .4); winL.position.set(.6, 2.2, -3); winL.target.position.set(0, 1, 2); S.add(winL, winL.target);
  const flashL = new T.PointLight('#c8d4ff', 0, 0, 1.2); flashL.position.set(.8, 3, -2.5); S.add(flashL);
  const fillL = new T.PointLight('#5a6c90', 0, 0, 1.6); fillL.position.set(0, OY, -.6); S.add(fillL);
  // reflection of the flame on the glass (the mirror image sits behind the pane)
  const refl = ctx.glow(S, '#ffb070', .16, .25); refl.material.depthTest = false; refl.renderOrder = 5;

  // ---------- glass: drops, trails, condensation blur, refraction of the outside target ----------
  const glassU = { tOut: { value: rtOut.texture }, res: { value: new T.Vector2(ctx.W, ctx.H) }, time: { value: 0 }, wet: { value: 1 }, warmPos: { value: new T.Vector2(.2, .1) }, fog: { value: new T.Color('#1a2230') } };
  const glass = new T.Mesh(new T.PlaneGeometry(OW, OH), new T.ShaderMaterial({ uniforms: glassU,
    vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.); }',
    fragmentShader: `uniform sampler2D tOut; uniform vec2 res,warmPos; uniform float time,wet; uniform vec3 fog; varying vec2 vUv;
      vec3 h3(float p){ vec3 q=fract(vec3(p)*vec3(.1031,.1030,.0973)); q+=dot(q,q.yzx+33.33); return fract((q.xxy+q.yzz)*q.zyx); }
      float sw(float b,float x){ return smoothstep(0.,b,x)*smoothstep(1.,b,x); }
      // running drops: columns of cells scrolling down; inside each cell a drop creeps and jerks, leaving beads and a wiped streak
      vec2 run(vec2 p,float t,float sc){ p*=sc; vec2 g=vec2(4.,.9); float cx=floor(p.x*g.x); vec3 cn=h3(cx*13.7+sc*3.1);
        float y=p.y+t*(.35+.25*cn.x); float cy=floor(y*g.y); vec3 n=h3(cx*71.3+cy*17.9+sc);
        vec2 st=vec2(fract(p.x*g.x)-.5,fract(y*g.y));
        float x=(n.x-.5)*.55; float wig=sin(p.y*7.+sin(p.y*3.1+n.y*6.))*.12*(n.z-.3); x+=wig;
        float ti=fract(t*(.25+.2*n.y)+n.z); float yd=(sw(.82,ti)-.5)*.8+.5;
        vec2 dv=vec2((st.x-x)/g.x*3.2,(st.y-yd)/g.y*1.4); float d=length(dv);
        float drop=smoothstep(.075,.0,d)*step(.25,n.y);
        float up=st.y-yd; float tr=smoothstep(0.,.02,up)*smoothstep(1.,0.,up/(1.-yd+.001)); float dx=abs(st.x-x);
        float clear=smoothstep(.09,.04,dx)*tr*step(.25,n.y);
        float by=fract(p.y*5.5)-.5; float bead=smoothstep(.07,.0,length(vec2((st.x-x)/g.x*3.2,by/5.5*1.6)))*tr*smoothstep(.0,.3,1.-up)*step(.45,n.y);
        return vec2(max(drop,bead*.7),clear); }
      float stat(vec2 p,float t){ p*=7.; vec2 id=floor(p); vec2 f=fract(p)-.5; vec3 n=h3(id.x*107.45+id.y*35.43); vec2 c=(n.xy-.5)*.7;
        float r=.12+.18*n.z; float d=length(f-c)/r; float life=sw(.04,fract(t*.18+n.z*7.)); return max(0.,1.-d*d)*step(.35,fract(n.z*13.))*life; }
      vec2 drops(vec2 p,float t){ vec2 a=run(p,t,1.),b=run(p+vec2(.37,.11),t*1.1,1.7); float s=stat(p,t); return vec2(max(max(a.x,b.x),s*.8),max(a.y,b.y*.8)); }
      void main(){ vec2 p=vUv*vec2(${OW.toFixed(2)},${OH.toFixed(2)})*2.2; float t=time;
        vec2 c=drops(p,t); float e=.004; float cx=drops(p+vec2(e,0.),t).x, cy=drops(p+vec2(0.,e),t).x; vec2 gr=vec2(cx-c.x,cy-c.x)/e;
        vec2 uv=gl_FragCoord.xy/res; vec2 off=-gr*.0035*wet;
        float focus=clamp(c.x*3.+c.y,0.,1.)*wet; float lod=mix(4.6,.6,focus);
        float px=exp2(lod)/res.x*2.;
        vec3 col=vec3(0.); col+=textureLod(tOut,uv+off,lod).rgb*.4;
        col+=textureLod(tOut,uv+off+vec2(px,px*.6),lod).rgb*.15; col+=textureLod(tOut,uv+off+vec2(-px,px*.6),lod).rgb*.15;
        col+=textureLod(tOut,uv+off+vec2(px*.6,-px),lod).rgb*.15; col+=textureLod(tOut,uv+off+vec2(-px*.6,-px),lod).rgb*.15;
        col=mix(col,col*.82+fog*.10,(1.-focus)*wet);                                         // condensation haze
        vec2 ln=normalize(gr+1e-5); float rim=c.x*smoothstep(.2,1.,dot(ln,normalize(warmPos-vUv)))*smoothstep(1.,.3,c.x);
        col+=vec3(1.,.62,.3)*rim*.35*smoothstep(1.4,.0,length(vUv-warmPos));             // drops catch the candle
        col+=vec3(.6,.7,.9)*pow(max(0.,ln.y),3.)*c.x*.05;                                    // sky glint on the drop tops
        gl_FragColor=vec4(col,1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` }));
  glass.position.set(0, OY, 0); S.add(glass);

  const cam = new T.PerspectiveCamera(38, ctx.W / ctx.H, .05, 900); ctx.side(cam, p.side == null ? .1 : p.side);
  const V = new T.Vector3();
  return { scene: S, camera: cam, draw(t, u) {
    const L = light(t), dl = L.day, fl = strikes.reduce((a, s) => a + flashAt(t, s[0]), 0);
    // sky + outside light
    skyU.day.value = dl; skyU.warm.value = L.warm; skyU.time.value = t; skyU.flash.value = fl;
    let fi = 0, fb = 0; strikes.forEach((s, i) => { const f = flashAt(t, s[0]); bolts[i].material.opacity = f > .05 ? Math.min(1, f * 1.6) * (Math.cos((t - s[0]) * 38) > -.2 ? 1 : 0) : 0; if (f > fb) { fb = f; fi = i; } });
    skyU.fpos.value.set(strikes[fi][1] / 300, -strikes[fi][2] / 300);
    O.fog.color.setRGB(.04 + dl * .2, .06 + dl * .22, .1 + dl * .25); O.fog.density = .012 + .004 * sm(tStop - 1, tStop + 1, t);
    oHemi.intensity = .12 + dl * 1.1 + fl * .8; oSun.intensity = dl * .6 + fl * 1.5;
    const night = 1 - sm(.3, .55, dl);
    lamps.forEach(l => { l.pl.intensity = 60 * night; l.gl.material.opacity = .9 * night; l.head.material.color.setRGB(16 * night + .15, 9 * night + .12, 3.5 * night + .1); });
    const di = Math.floor(L.d);
    houses.forEach((h, i) => { const on = (Math.sin(h.seed + di * 3.7) > -.3 ? 1 : 0) * night * (Math.sin(h.seed * 3 + di) > -.6 ? 1 : .25); h.wm.color.setRGB(7 * on + .03, (3.6 + 1.4 * h.warm) * on + .03, 1.2 * on + .03); });
    // rain streaks: fall fast, slight wind slant; heavier after "does not stop"
    const heavy = .7 + .3 * sm(tStop - .5, tStop + 1.5, t); rainM.opacity = (.22 + dl * .25) * heavy;
    for (let i = 0; i < NR; i++) { const [x, y, z, o] = rb[i]; const yy = ((y - t * (16 + o * 6)) % 24 + 24) % 24 - 3.5, xx = x + yy * .08;
      const len = .5 + o * .5; rp.set([xx, yy, z, xx + len * .08, yy + len, z], i * 6); }
    rainG.attributes.position.needsUpdate = true;
    // camera: slow drift toward the window; at the end it pushes into the glass
    const pk = sm(tPush - 1.25, tPush + .3, t), q = sm(ctx.t0, tPush, t);
    const cpos = [-1.55 + q * .4, 1.84 + .03 * Math.sin(u * .4), 4.9 - q * .55]; const tgt = [.28, 1.9, 0];
    V.set(cpos[0] + (.12 - cpos[0]) * pk, cpos[1] + (1.95 - cpos[1]) * pk, cpos[2] + (.32 - cpos[2]) * pk); cam.position.copy(V);
    cam.lookAt(tgt[0] + (.12 - tgt[0]) * pk, tgt[1] + (1.95 - tgt[1]) * pk, 0);
    // render the outside first
    const prev = R.getRenderTarget(); R.setRenderTarget(rtOut); R.render(O, cam); R.setRenderTarget(prev);
    glassU.time.value = t; glassU.wet.value = .85 + .15 * heavy;
    // candle: burns down as the days pass, flickers
    const hC = .115 * (1 - Math.min(.75, (L.d - .08) / 7)) + .01, fk = .85 + .08 * Math.sin(t * 13.1) + .05 * Math.sin(t * 31.7 + 1) + .03 * Math.sin(t * 57.3);
    wax.scale.set(1, hC, 1); wax.position.set(cx, sy + .012 + hC / 2, cz); const top = sy + .012 + hC;
    wick.position.set(cx, top + .007, cz); flame.position.set(cx + .002 * Math.sin(t * 9), top + .03, cz); flame.scale.set(.026 * fk, .06 * fk, 1);
    halo.position.copy(flame.position); halo2.position.copy(flame.position); halo.material.opacity = .3 * fk; halo2.material.opacity = .07 * fk;
    candleL.position.set(cx, top + .05, cz); candleL.intensity = .6 * fk;
    refl.position.set(cx, top + .03, -cz); refl.material.opacity = .22 * fk;
    // glass highlight position of the flame (in pane uv)
    glassU.warmPos.value.set((cx + OW / 2) / OW, (top - (OY - OH / 2)) / OH);
    winL.intensity = .15 + dl * 1.4; winL.color.setRGB(.5 + dl * .2 + L.warm * .4, .6 + dl * .2, .8 + dl * .1);
    flashL.intensity = fl * 6; fillL.intensity = .25 + dl * 2.5;
    S.background.setRGB(.004, .005, .008);
    // curtain sway (a slow draught)
    for (let i = 0; i < cP.count; i++) { const x = cb[i * 3], y = cb[i * 3 + 1], dn = (1.95 - y) / 3.9;
      cP.array[i * 3 + 2] = .07 * Math.sin(x * 17 + 1.3) + .03 * Math.sin(x * 41) + dn * .03 * Math.sin(t * .8 + x * 3); cP.array[i * 3] = x + dn * .015 * Math.sin(t * .6); }
    cP.needsUpdate = true; cg.computeVertexNormals();
  } };

  function merge(list) {
    const gs = list.map(g => g.index ? g.toNonIndexed() : g); const n = gs.reduce((a, g) => a + g.attributes.position.count, 0);
    const pos = new Float32Array(n * 3), nor = new Float32Array(n * 3); let k = 0;
    gs.forEach(g => { if (!g.attributes.normal) g.computeVertexNormals(); pos.set(g.attributes.position.array, k * 3); nor.set(g.attributes.normal.array, k * 3); k += g.attributes.position.count; });
    const o = new T.BufferGeometry(); o.setAttribute('position', new T.BufferAttribute(pos, 3)); o.setAttribute('normal', new T.BufferAttribute(nor, 3)); return o; }
};
