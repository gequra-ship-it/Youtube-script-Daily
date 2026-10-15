// bodymuseum — an x-ray-glow anatomy stage that turns into an ancient ocean (stage).
// A realistic human heart (ONE mesh: deformed sphere + great vessels merged, beating "lub-dub" by vertex deform, glowing coronary
// vessels, warm light that lights the bones around it); ribs and backbone (solid bones with depth: flat ribs swept along curves,
// instanced vertebrae with body, arch and processes) revealed by a glowing scan line; two lungs (ONE mesh each, translucent, breathing
// by deform); above them a calm frosted-glass head (no face features) seen from the side, with the jaw bones softly lit inside
// (the mandible is a separate bone on a hinge, it opens and closes as if speaking; the glass chin follows a little). At "strange" the camera pulls far back into a dark ancient ocean (fog, god rays, marine snow)
// where early armoured fish (ONE mesh each, kit.body + fins merged, swimming by deform) glide past; the heart's glow stays as a
// distant light.
// params (cues): { ribs, spine, lungs, jaw (skull + jaws appear, camera tilts up), open (jaw opens and "speaks"), ocean (pull back
//   into the ancient sea), fish (fish arrive), side:.13 }
(window.MIYA = window.MIYA || { scenes: {} }).scenes.bodymuseum = function (ctx, p) {
  const { T, sm, cue } = ctx, K = window.MIYA.kit;
  const S = new T.Scene(); const BG0 = new T.Color('#05061a'), BG1 = new T.Color('#021a28'); S.background = BG0.clone();
  S.fog = new T.FogExp2(BG0.clone(), .03);   // depth haze in the anatomy stage (far ribs and spine sink into navy)
  const at = (c, d) => c == null ? 0 : sm(cue(c), cue(c) + d, ctx.t);
  S.environment = ctx.env();
  // ---------- helpers ----------
  function curve(keys, col) { return s => { s = Math.min(1, Math.max(0, s)); let i = 0; while (i < keys.length - 2 && s > keys[i + 1][0]) i++;
    const k0 = keys[Math.max(0, i - 1)], k1 = keys[i], k2 = keys[i + 1], k3 = keys[Math.min(keys.length - 1, i + 2)], h = k2[0] - k1[0], x = (s - k1[0]) / h;
    const m1 = (k2[col] - k0[col]) / Math.max(1e-6, k2[0] - k0[0]) * h, m2 = (k3[col] - k1[col]) / Math.max(1e-6, k3[0] - k1[0]) * h, x2 = x * x, x3 = x2 * x;
    return (2 * x3 - 3 * x2 + 1) * k1[col] + (x3 - 2 * x2 + x) * m1 + (-2 * x3 + 3 * x2) * k2[col] + (x3 - x2) * m2; }; }
  const V3 = (a) => a.map(q => new T.Vector3(q[0], q[1], q[2]));
  // sweep an elliptical section along a curve: rf(s) -> [a (along binormal), b (along normal)]; ends capped
  function sweep(cv, n, m, rf, uvf) { const fr = cv.computeFrenetFrames(n, false), pos = [], uv = [], idx = [], P = new T.Vector3();
    for (let i = 0; i <= n; i++) { const s = i / n; cv.getPointAt(s, P); const N = fr.normals[i], B = fr.binormals[i], [a, b] = rf(s);
      for (let j = 0; j < m; j++) { const an = j / m * Math.PI * 2, c = Math.cos(an), sn = Math.sin(an); pos.push(P.x + N.x * c * b + B.x * sn * a, P.y + N.y * c * b + B.y * sn * a, P.z + N.z * c * b + B.z * sn * a); uv.push(...(uvf ? uvf(s, j / m) : [s, j / m])); } }
    for (let i = 0; i < n; i++) for (let j = 0; j < m; j++) { const a = i * m + j, b = i * m + (j + 1) % m, c = (i + 1) * m + j, d = (i + 1) * m + (j + 1) % m; idx.push(a, c, b, b, c, d); }
    [0, n].forEach(i => { const c0 = pos.length / 3; cv.getPointAt(i / n, P); pos.push(P.x, P.y, P.z); uv.push(...(uvf ? uvf(i / n, .5) : [i / n, .5])); for (let j = 0; j < m; j++) i ? idx.push(c0, i * m + j, i * m + (j + 1) % m) : idx.push(c0, (j + 1) % m, j); });
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.Float32BufferAttribute(pos, 3)); g.setAttribute('uv', new T.Float32BufferAttribute(uv, 2)); g.setIndex(idx); g.computeVertexNormals(); return g; }
  function merge(list) { let nv = 0, ni = 0; list = list.map(g => { if (!g.index) { const a = []; for (let i = 0; i < g.attributes.position.count; i++) a.push(i); g.setIndex(a); } if (!g.attributes.normal) g.computeVertexNormals(); if (!g.attributes.uv) g.setAttribute('uv', new T.Float32BufferAttribute(new Float32Array(g.attributes.position.count * 2), 2)); nv += g.attributes.position.count; ni += g.index.count; return g; });
    const P = new Float32Array(nv * 3), N = new Float32Array(nv * 3), U = new Float32Array(nv * 2), I = new Uint32Array(ni); let o = 0, oi = 0;
    list.forEach(g => { P.set(g.attributes.position.array, o * 3); N.set(g.attributes.normal.array, o * 3); U.set(g.attributes.uv.array, o * 2); const ix = g.index.array; for (let i = 0; i < ix.length; i++) I[oi + i] = ix[i] + o; o += g.attributes.position.count; oi += ix.length; });
    const g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(P, 3)); g.setAttribute('normal', new T.BufferAttribute(N, 3)); g.setAttribute('uv', new T.BufferAttribute(U, 2)); g.setIndex(new T.BufferAttribute(I, 1)); return g; }
  const ACC = new T.Color(ctx.ACC);
  // stable in motion (cine_spec 3A): max anisotropy, fine normal detail fades with distance; rim only on edges facing the back light
  const ANI = ctx.R ? ctx.R.capabilities.getMaxAnisotropy() : 8, aniso = (...ts) => ts.forEach(x => { x.anisotropy = ANI; });
  const RIM = { rimL: { value: new T.Vector3(0, .5, -1) } };   // direction toward the back light, in view space (set in draw)
  const fadeN = (sh, n0, n1) => { sh.fragmentShader = sh.fragmentShader.replace('#include <normal_fragment_maps>',
    T.ShaderChunk.normal_fragment_maps.replace('mapN.xy *= normalScale;', `mapN.xy *= normalScale * (1. - smoothstep(${n0.toFixed(1)}, ${n1.toFixed(1)}, length(vViewPosition)));`)); };
  const RIMW = 'smoothstep(-.05,.6,dot(normal,rimL))';   // weight: only the side of the silhouette that faces the light
  // ---------- the heart: ONE mesh ----------
  const HW = 1024, HH = 512, hc = document.createElement('canvas'); hc.width = HW; hc.height = HH; const g = hc.getContext('2d');
  const ec = document.createElement('canvas'); ec.width = HW; ec.height = HH; const eg = ec.getContext('2d'); eg.fillStyle = '#000'; eg.fillRect(0, 0, HW, HH);
  const bc = document.createElement('canvas'); bc.width = HW; bc.height = HH; const bgx = bc.getContext('2d');
  { const gr = g.createLinearGradient(0, 0, 0, HH); gr.addColorStop(0, '#5c1016'); gr.addColorStop(.5, '#6e141b'); gr.addColorStop(1, '#4c0b12'); g.fillStyle = gr; g.fillRect(0, 0, HW, HH);
    g.globalCompositeOperation = 'multiply'; g.globalAlpha = .5; g.drawImage(K.noise(512, { seed: 3, octaves: 3, sx: 2 }), 0, 0, HW, HH); g.globalCompositeOperation = 'source-over'; g.globalAlpha = 1;
    bgx.fillStyle = '#808080'; bgx.fillRect(0, 0, HW, HH); bgx.globalAlpha = .4; bgx.drawImage(K.noise(512, { seed: 5, octaves: 3 }), 0, 0, HW, HH); bgx.globalAlpha = 1;
    const r = K.rng(12);
    for (let i = 0; i < 2600; i++) { const x = r() * HW, y = r() * HH, l = 20 + r() * 50; g.strokeStyle = `rgba(${r() < .5 ? '140,40,45' : '40,5,10'},.12)`; g.lineWidth = 1 + r(); g.beginPath(); g.moveTo(x, y); g.lineTo(x + l * .7, y + l * .5); g.stroke();
      bgx.strokeStyle = `rgba(${r() < .5 ? '255,255,255' : '0,0,0'},.15)`; bgx.lineWidth = 1.5; bgx.beginPath(); bgx.moveTo(x, y); bgx.lineTo(x + l * .7, y + l * .5); bgx.stroke(); }   // muscle fibres
    // fat along the coronary groove (v ~ .27) and the interventricular grooves (u ~ .27 front, .77 back)
    const fat = (x0, y0, x1, y1, w) => { g.strokeStyle = 'rgba(190,150,80,.55)'; g.lineWidth = w; g.lineCap = 'round'; g.beginPath(); g.moveTo(x0, y0); g.bezierCurveTo(x0 + (x1 - x0) * .3 + 15, y0 + (y1 - y0) * .3, x0 + (x1 - x0) * .7 - 15, y0 + (y1 - y0) * .7, x1, y1); g.stroke(); };
    for (let k = 0; k < 3; k++) { g.filter = 'blur(6px)'; fat(0, HH * .27, HW, HH * .27, 26); fat(HW * .27, HH * .27, HW * .33, HH * .9, 16); fat(HW * .77, HH * .27, HW * .72, HH * .88, 14); } g.filter = 'none';
    // coronary arteries: branching vessels from the coronary groove, raised and glowing
    const vessel = (x, y, a, len, w, d) => { for (let k = 0; k < len; k++) { const nx = x + Math.cos(a) * 6, ny = y + Math.sin(a) * 6;
        g.strokeStyle = 'rgba(120,20,25,.95)'; g.lineWidth = w + 2; g.beginPath(); g.moveTo(x, y); g.lineTo(nx, ny); g.stroke(); g.strokeStyle = 'rgba(200,70,60,.8)'; g.lineWidth = w * .5; g.beginPath(); g.moveTo(x, y); g.lineTo(nx, ny); g.stroke();
        eg.strokeStyle = `rgba(255,255,255,${.5 + w * .1})`; eg.lineWidth = w; eg.beginPath(); eg.moveTo(x, y); eg.lineTo(nx, ny); eg.stroke();
        bgx.strokeStyle = 'rgba(255,255,255,.9)'; bgx.lineWidth = w + 2; bgx.beginPath(); bgx.moveTo(x, y); bgx.lineTo(nx, ny); bgx.stroke();
        x = nx; y = ny; a += (r() - .5) * .35; if (d < 3 && r() < .09) vessel(x, y, a + (r() < .5 ? -.7 : .7), len * .5 | 0, w * .65, d + 1); } };
    vessel(HW * .27, HH * .26, Math.PI * .45, 55, 5, 0); vessel(HW * .77, HH * .26, Math.PI * .55, 50, 4.5, 0);
    for (let k = 0; k < 7; k++) vessel(HW * (.05 + k * .14), HH * .28, Math.PI * (.4 + r() * .2), 25 + r() * 25 | 0, 3, 1);
    for (let k = 0; k < 2; k++) { vessel(k * HW * .5, HH * .27, 0, 85, 4.5, 2); }
    // top band: vessel colours (aorta / pulmonary / veins)
    [['#7a4a42', 0, .34], ['#6a2a34', .34, .67], ['#3a2440', .67, 1]].forEach(([c, a, b]) => { g.fillStyle = c; g.fillRect(a * HW, 0, (b - a) * HW, HH * .035); }); }
  const hMap = K.tex(hc, true), hEm = K.tex(ec, true), hN = K.normalMap(bc, 3);
  const VU = (k) => (s, q) => [k / 3 + .02 + s * .29, 1 - .015];   // uv in the top band for vessel k
  const heartG = (() => {
    const sg = new T.SphereGeometry(1, 160, 120), P = sg.attributes.position, UV = sg.attributes.uv;
    const rrT = t => t < .22 ? .92 * Math.sin(Math.min(1, t / .22) * Math.PI / 2) : t < .45 ? .92 + .1 * sm(.22, .45, t) : 1.02 * Math.pow(Math.max(0, 1 - Math.pow((t - .45) / .55, 1.9)), .85);
    for (let i = 0; i < P.count; i++) { const u = UV.getX(i), t = 1 - UV.getY(i), ph = u * Math.PI * 2;
      let rr = rrT(t); const y = 1.05 - 2.35 * Math.pow(t, 1.05);
      const dphi = (a, b) => Math.atan2(Math.sin(a - b), Math.cos(a - b));
      rr *= 1 - .06 * Math.exp(-Math.pow(dphi(ph, Math.PI * 2 * .27) / .09, 2)) * sm(.25, .45, t) * (1 - sm(.85, .98, t));   // front groove
      rr *= 1 - .05 * Math.exp(-Math.pow(dphi(ph, Math.PI * 2 * .77) / .09, 2)) * sm(.25, .45, t) * (1 - sm(.85, .98, t));
      rr *= 1 - .05 * Math.exp(-Math.pow((t - .27) / .03, 2));   // coronary groove
      const atr = Math.exp(-Math.pow((t - .14) / .1, 2)); rr += .2 * atr * Math.exp(-Math.pow(dphi(ph, Math.PI * 1.05) / .7, 2)) + .14 * atr * Math.exp(-Math.pow(dphi(ph, 0) / .6, 2));   // atria
      const x = -Math.cos(ph) * rr * 1.0, z = Math.sin(ph) * rr * .86; P.setXYZ(i, x, y, z); }
    sg.computeVertexNormals();
    const tube = (pts, r0, r1, k) => sweep(new T.CatmullRomCurve3(V3(pts)), 48, 18, s => { const r = r0 + (r1 - r0) * s; return [r, r]; }, VU(k));
    const parts = [sg,
      tube([[0, .7, .05], [.02, 1.55, .12], [.2, 2.15, .05], [.6, 2.3, -.25], [.85, 1.9, -.55], [.88, 1.0, -.8], [.82, -.3, -.95]], .25, .21, 0),   // aorta
      tube([[.05, 2.0, .08], [0, 2.9, .12]], .1, .085, 0), tube([[.32, 2.2, -.05], [.38, 3.0, -.05]], .09, .075, 0), tube([[.58, 2.15, -.22], [.7, 2.9, -.28]], .09, .075, 0),
      tube([[.3, .6, .48], [.33, 1.35, .42], [.5, 1.6, .25], [1.05, 1.6, -.05]], .22, .15, 1), tube([[.38, 1.45, .35], [0, 1.62, .0], [-.5, 1.62, -.25], [-1.0, 1.5, -.35]], .14, .13, 1),   // pulmonary trunk + branches
      tube([[-.6, .7, -.05], [-.62, 1.6, -.08], [-.64, 2.7, -.1]], .18, .17, 2), tube([[-.5, -.5, -.25], [-.55, -1.15, -.32], [-.6, -1.8, -.35]], .18, .17, 2)];   // venae cavae
    return merge(parts); })();
  const HU = { beat: { value: 0 }, atr: { value: 0 }, emk: { value: 1 }, rimK: { value: .35 } };
  const heartMat = new T.MeshPhysicalMaterial({ map: hMap, normalMap: hN, normalScale: new T.Vector2(.7, .7), roughness: .38, metalness: 0, clearcoat: .6, clearcoatRoughness: .3, emissive: '#ff7a3a', emissiveMap: hEm, emissiveIntensity: 1, envMapIntensity: .5, side: T.DoubleSide });
  heartMat.onBeforeCompile = sh => { Object.assign(sh.uniforms, HU, RIM); fadeN(sh, 12, 45);
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nuniform float beat, atr;').replace('#include <begin_vertex>', `#include <begin_vertex>
      { float ven = smoothstep(.75,-.2,position.y)*(1.-smoothstep(1.4,2.,position.y)); float at2 = smoothstep(.2,.9,position.y)*(1.-smoothstep(1.3,1.9,position.y));
        float k = .085*beat*ven + .05*atr*at2; transformed.xz *= 1.-k; transformed.y += .09*beat*ven*(.4-position.y)*.5; transformed.xz *= 1. + .02*beat*smoothstep(1.6,2.4,position.y); }`);
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float emk, rimK; uniform vec3 rimL;').replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
      totalEmissiveRadiance *= emk; { float fr=pow(1.-max(dot(normal,normalize(vViewPosition)),0.),2.5); totalEmissiveRadiance += vec3(1.,.32,.16)*fr*rimK*(.25+.75*${RIMW}); }`); };
  const heart = new T.Mesh(heartG, heartMat); const HG = new T.Group(); HG.add(heart); HG.position.set(.35, .1, .5); HG.rotation.set(-.25, .2, .4); HG.scale.setScalar(1.1); S.add(HG);
  const hGlow = ctx.glow(S, '#ff5a32', 9, .35); hGlow.position.copy(HG.position); const hGlow2 = ctx.glow(S, '#ffb070', 3.5, .3); hGlow2.position.copy(HG.position);
  const hLight = new T.PointLight('#ff7448', 30, 16, 1.6); hLight.position.copy(HG.position).add(new T.Vector3(0, 0, .4)); S.add(hLight);
  // ---------- bones (reveal by a glowing scan line; warm rim) ----------
  const boneN = K.normalMap(K.noise(512, { seed: 44, octaves: 3 }), 2.5); boneN.repeat.set(3, 3);
  const boneC = document.createElement('canvas'); boneC.width = boneC.height = 256; { const bg2 = boneC.getContext('2d'); bg2.fillStyle = '#d9ccb0'; bg2.fillRect(0, 0, 256, 256); bg2.globalCompositeOperation = 'multiply'; bg2.globalAlpha = .45; bg2.drawImage(K.noise(256, { seed: 46, octaves: 2 }), 0, 0); }
  const boneT = K.tex(boneC, true, [2, 2]); aniso(boneN, boneT);
  function boneMat(o) { const U = { rev: { value: -99 }, revC: { value: ACC.clone() }, rimK: { value: .8 }, rimC: { value: new T.Color('#ffc080') } };
    const m = new T.MeshStandardMaterial(Object.assign({ map: boneT, normalMap: boneN, normalScale: new T.Vector2(.6, .6), roughness: .55, metalness: 0, envMapIntensity: .35, color: '#e8dcc4' }, o || {}));
    m.onBeforeCompile = sh => { Object.assign(sh.uniforms, U, RIM); fadeN(sh, 5, 22);
      sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nvarying vec3 vWP;').replace('#include <project_vertex>', `#include <project_vertex>
        { vec4 wp = vec4(transformed,1.);
        #ifdef USE_INSTANCING
          wp = instanceMatrix*wp;
        #endif
        vWP = (modelMatrix*wp).xyz; }`);
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nvarying vec3 vWP; uniform float rev, rimK; uniform vec3 revC, rimC, rimL;').replace('#include <clipping_planes_fragment>', '#include <clipping_planes_fragment>\nif(vWP.y>rev) discard;')
        .replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
          { float fr=pow(1.-max(dot(normal,normalize(vViewPosition)),0.),2.2); totalEmissiveRadiance += rimC*fr*rimK*${RIMW} + revC*exp(-pow((rev-vWP.y)/.14,2.))*2.5; }`); };
    m.userData.U = U; return m; }
  const ribMat = boneMat(), spineMat = boneMat(), jawMat = boneMat({ color: '#bfb39b', normalScale: new T.Vector2(.25, .25), roughness: .7 }), toothMat = boneMat({ color: '#8f877a', roughness: .5, normalScale: new T.Vector2(.15, .15) });
  toothMat.userData.U.rimK.value = .25;   // small teeth stay in shadow
  // spine: S-curved column, vertebrae instanced along it (body + arch + spinous + transverse processes)
  const spineCv = new T.CatmullRomCurve3(V3([[0, -5.2, -2.0], [0, -2.6, -2.35], [0, 0, -2.55], [0, 2.6, -2.45], [0, 4.6, -2.0], [0, 6.2, -1.7]]));
  const vertG = (() => { const lp = [[0, -.22], [.34, -.22], [.4, -.18], [.36, 0], [.4, .18], [.34, .22], [0, .22]].map(([r, y]) => new T.Vector2(r, y));
    const body = new T.LatheGeometry(lp, 28);
    const arch = new T.TorusGeometry(.27, .08, 10, 20, Math.PI); arch.rotateX(Math.PI / 2); arch.rotateY(Math.PI); arch.translate(0, 0, -.42);
    const spn = sweep(new T.CatmullRomCurve3(V3([[0, 0, -.65], [0, -.15, -.95], [0, -.42, -1.25]])), 10, 10, s => [.13 - .06 * s, .07 - .02 * s]);
    const tr = [1, -1].map(sd => sweep(new T.CatmullRomCurve3(V3([[sd * .2, .03, -.55], [sd * .5, .05, -.62], [sd * .8, .02, -.72]])), 10, 10, s => [.09 - .03 * s, .08 - .02 * s]));
    return merge([body, arch, spn, ...tr]); })();
  const NVt = 26, vI = new T.InstancedMesh(vertG, spineMat, NVt); { const M4 = new T.Matrix4(), Q = new T.Quaternion(), P0 = new T.Vector3(), Tg = new T.Vector3(), up = new T.Vector3(0, 1, 0);
    for (let i = 0; i < NVt; i++) { const s = (i + .5) / NVt; spineCv.getPointAt(s, P0); spineCv.getTangentAt(s, Tg); Q.setFromUnitVectors(up, Tg); const sc = 1.25 - .6 * s; M4.compose(P0, Q, new T.Vector3(sc, sc * .95, sc)); vI.setMatrixAt(i, M4); } }
  S.add(vI);
  // discs between the vertebrae (pale blue-grey cartilage)
  const discG = new T.CylinderGeometry(.36, .36, .14, 24); const dI = new T.InstancedMesh(discG, spineMat, NVt - 1); { const M4 = new T.Matrix4(), Q = new T.Quaternion(), P0 = new T.Vector3(), Tg = new T.Vector3(), up = new T.Vector3(0, 1, 0);
    for (let i = 0; i < NVt - 1; i++) { const s = (i + 1) / NVt; spineCv.getPointAt(s, P0); spineCv.getTangentAt(s, Tg); Q.setFromUnitVectors(up, Tg); const sc = 1.25 - .6 * s; M4.compose(P0, Q, new T.Vector3(sc * .95, sc, sc * .95)); dI.setMatrixAt(i, M4); } }
  S.add(dI);
  // ribs: 12 pairs, flat bones curving from the spine round the sides toward the front (cut away at the front so the heart is seen)
  const ribGs = [];
  for (let i = 0; i < 12; i++) { const y0 = 3.15 - i * .6, Rx = 1.25 + 1.55 * Math.sin(Math.min(1, (i + 1) / 6.5) * Math.PI / 2) - .25 * sm(8, 11, i), Rz = 1.0 + 1.25 * Math.sin(Math.min(1, (i + 1) / 6) * Math.PI / 2), zc = -2.55 + Rz * .95;
    const fe = i >= 10 ? .42 : i >= 7 ? .62 - (i - 7) * .04 : .72, drop = 1.15 + i * .03;
    [1, -1].forEach(sd => { const pts = [[sd * .35, y0 + .1, -2.5]]; for (let k = 0; k <= 10; k++) { const ph = .12 + k / 10 * (fe * Math.PI - .12); pts.push([sd * Rx * Math.sin(ph), y0 - drop * Math.pow(ph / Math.PI, 1.3), zc - Rz * Math.cos(ph)]); }
      ribGs.push(sweep(new T.CatmullRomCurve3(V3(pts)), 60, 12, s => { const w = .17 * (1 - .35 * s) * Math.min(1, s * 12 + .5) * (i < 2 ? .8 : 1); return [w, .065 * (1 - .3 * s)]; })); }); }
  const ribs = new T.Mesh(merge(ribGs), ribMat); S.add(ribs);
  // ---------- lungs: ONE translucent mesh each, breathing by deform ----------
  const LU = { br: { value: 0 }, op: { value: 0 } };
  const lungC = document.createElement('canvas'); lungC.width = lungC.height = 512; { const lg = lungC.getContext('2d'); lg.fillStyle = '#000'; lg.fillRect(0, 0, 512, 512); const r = K.rng(61);
    const br = (x, y, a, len, w, d) => { for (let k = 0; k < len; k++) { const nx = x + Math.cos(a) * 5, ny = y + Math.sin(a) * 5; lg.strokeStyle = `rgba(255,255,255,${.25 + w * .12})`; lg.lineWidth = w; lg.beginPath(); lg.moveTo(x, y); lg.lineTo(nx, ny); lg.stroke(); x = nx; y = ny; a += (r() - .5) * .4; if (d < 5 && r() < .12) br(x, y, a + (r() < .5 ? -.6 : .6), len * .6 | 0, w * .7, d + 1); } };
    for (let k = 0; k < 8; k++) br(k * 64 + 32, 40, Math.PI / 2 + (r() - .5) * .4, 70, 3.5, 0); }
  const lungEm = K.tex(lungC, true);
  function lungGeo(sd) { const g2 = new T.SphereGeometry(1, 72, 54), P = g2.attributes.position;
    for (let i = 0; i < P.count; i++) { let x = P.getX(i), y = P.getY(i), z = P.getZ(i);
      const top = sm(-.2, 1, y); x *= 1 - .5 * top; z *= 1 - .35 * top;   // narrow rounded apex
      if (y < -.55) y = -.55 - (y + .55) * .35;   // broad base resting on the diaphragm, dome-shaped
      y -= .25 * (1 - x * x) * sm(-.3, -.9, y);   // concave base
      if (x * -sd > 0) x *= .55 + .45 * (1 - Math.exp(-Math.pow((y + .1) / .6, 2)) * (sd > 0 ? 1 : .6));   // medial side hollowed where the heart sits (more on the left)
      P.setXYZ(i, x * 1.25, y * 2.7, z * 1.6); }
    g2.computeVertexNormals(); return g2; }
  const lungMat = () => { const m = new T.MeshStandardMaterial({ color: '#d98a86', roughness: .55, metalness: 0, transparent: true, opacity: .5, depthWrite: false, emissive: '#ffb08a', emissiveMap: lungEm, emissiveIntensity: .5, envMapIntensity: .4 });
    m.onBeforeCompile = sh => { Object.assign(sh.uniforms, LU, RIM);
      sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nuniform float br;').replace('#include <begin_vertex>', '#include <begin_vertex>\n{ float k=br*.07; transformed.x*=1.+k; transformed.z*=1.+k*.7; transformed.y+= -br*.22*smoothstep(.5,-2.4,position.y); }');
      sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float op; uniform vec3 rimL;').replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
        { float fr=pow(1.-max(dot(normal,normalize(vViewPosition)),0.),2.); totalEmissiveRadiance += vec3(.55,.75,1.)*fr*.9*(.3+.7*${RIMW}); }`).replace('#include <opaque_fragment>', '{ float fr=pow(1.-abs(dot(normal,normalize(vViewPosition))),2.); diffuseColor.a = op*(.28+.6*fr); }\n#include <opaque_fragment>'); };   // r169 chunk name (was opacity_fragment, which does not exist: the fade and edge alpha never ran)
    return m; };
  const lungs = [1, -1].map(sd => { const m = new T.Mesh(lungGeo(sd), lungMat()); m.position.set(sd * 1.75, .2, -.6); m.renderOrder = 2; S.add(m); return m; });
  // ---------- head: a calm frosted-glass bust (no face features) seen from the side; inside it the jaw bones, softly lit ----------
  // local frame: face toward +z, condyle hinge at PIV; the group turns so the camera sees the head in profile / slight 3/4 rear
  const PIV = new T.Vector3(0, -.38, -.15), HR = -1.0, SK = new T.Group(); SK.rotation.y = HR;
  SK.position.set(0, 7.9, -1.7).sub(new T.Vector3(0, 0, -.75).applyAxisAngle(new T.Vector3(0, 1, 0), HR)); S.add(SK);   // glass neck sits on the spine top
  const headG = (() => { const g2 = new T.SphereGeometry(1, 96, 72), P = g2.attributes.position, jw = new Float32Array(P.count), d = new T.Vector3();
    for (let i = 0; i < P.count; i++) { d.set(P.getX(i), P.getY(i), P.getZ(i)).normalize();
      const f = sm(-.2, .7, d.z) * sm(.3, -.6, d.y);   // lower front: the face plane drops forward-down to a smooth chin
      let x = d.x * 1.5 * (1 - .3 * f), y = d.y * 1.65 + .55 - 1.15 * f, z = d.z * 1.95 - .35 + .4 * f;
      const n = sm(-.55, -.85, d.y), hl = Math.max(1e-4, Math.hypot(d.x, d.z));   // bottom: blends into a neck column
      const ny = -1.3 - Math.max(0, -d.y - .55) / .45 * 2.8, nx = d.x / hl * .85, nz = -.75 + d.z / hl * .8;
      x += (nx - x) * n; y += (ny - y) * n; z += (nz - z) * n;
      jw[i] = f * (1 - n) * sm(-.6, -1.1, y);   // the chin follows the jaw a little
      P.setXYZ(i, x, y, z); }
    g2.setAttribute('jw', new T.BufferAttribute(jw, 1)); g2.computeVertexNormals(); return g2; })();
  const GU = { op: { value: 0 }, jo: { value: 0 }, piv: { value: PIV.clone() } };
  const glassMat = new T.MeshStandardMaterial({ color: '#9fb0c6', roughness: .22, metalness: 0, transparent: true, depthWrite: false, envMapIntensity: .7 });
  glassMat.onBeforeCompile = sh => { Object.assign(sh.uniforms, GU, RIM);
    sh.vertexShader = sh.vertexShader.replace('#include <common>', '#include <common>\nattribute float jw; uniform float jo; uniform vec3 piv; varying float vY;')
      .replace('#include <beginnormal_vertex>', '#include <beginnormal_vertex>\nfloat ja = jo*jw*.8, jc = cos(ja), js = sin(ja); mat3 JR = mat3(1.,0.,0., 0.,jc,js, 0.,-js,jc); objectNormal = JR*objectNormal;')
      .replace('#include <begin_vertex>', '#include <begin_vertex>\nvY = position.y; transformed = piv + JR*(transformed - piv);');
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform float op; uniform vec3 rimL; varying float vY;')
      .replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
        { float fr=pow(1.-max(dot(normal,normalize(vViewPosition)),0.),2.6); totalEmissiveRadiance += vec3(1.,.8,.58)*fr*.55*${RIMW} + vec3(.45,.6,.85)*fr*.08; }`)
      .replace('#include <opaque_fragment>', '{ float fr=pow(1.-abs(dot(normal,normalize(vViewPosition))),2.2); diffuseColor.a = op*(.04+.4*fr)*smoothstep(-3.6,-2.,vY); }\n#include <opaque_fragment>'); };
  const glass = new T.Mesh(headG, glassMat); glass.renderOrder = 3; SK.add(glass);
  // jaw bones (anatomical side profile): each half of the mandible is an extruded outline — body, angle, ramus, coronoid, condyle
  const halfJaw = (() => { const sh = new T.Shape(); sh.moveTo(.05, .08);
    sh.splineThru([[-.1, .0], [-.07, -.14], [-.02, -.45], [.04, -.74], [.1, -.85], [.22, -.92], [.5, -.95], [.9, -1.0], [1.3, -1.06], [1.6, -1.08], [1.77, -.98], [1.79, -.78], [1.7, -.62],
      [1.2, -.57], [.82, -.55], [.62, -.42], [.56, -.18], [.55, .0], [.47, -.04], [.32, -.17], [.16, -.1], [.08, -.02], [.05, .08]].map(([u, v]) => new T.Vector2(u, v)));
    const g2 = new T.ExtrudeGeometry(sh, { depth: .04, bevelEnabled: true, bevelThickness: .03, bevelSize: .03, bevelSegments: 4, curveSegments: 60 }); g2.translate(0, 0, -.02);
    { const P = g2.attributes.position; for (let i = 0; i < P.count; i++) { const u = P.getX(i), v = P.getY(i);   // the body thickens toward its lower border, the ramus stays a thin plate
        P.setZ(i, P.getZ(i) * (1 + 1.6 * sm(-.5, -1.0, v) * sm(.2, .8, u)) + .06 * sm(-.4, -.95, v) * sm(.2, .8, u)); } g2.computeVertexNormals(); }
    g2.rotateY(-Math.PI / 2); return g2; })();
  const AL = .58, side2 = (sd, u, v) => [sd * (1.0 - u * Math.sin(AL)), v, u * Math.cos(AL)];   // a point on half-jaw sd (u forward, v up; hinge at 0)
  const manParts = [1, -1].map(sd => { const g2 = halfJaw.clone(); g2.rotateY(-sd * AL); g2.translate(sd * 1.0, 0, 0); return g2; });
  const toothG = (r, h, up) => { const tg = new T.LatheGeometry([[0, 0], [r, 0], [r * 1.05, h * .45], [r * .8, h * .85], [0, h]].map(([a, b]) => new T.Vector2(a, b)), 8); if (!up) tg.rotateX(Math.PI); return tg; };
  function toothRow(v, up) { const out = []; [1, -1].forEach(sd => { for (let k = 0; k < 7; k++) { const u = .86 + k * .135, mol = k < 3, q = side2(sd, u, v);
      const tg = toothG(mol ? .065 : .045, mol ? .075 : .1, up); tg.scale(1, 1, mol ? 1.2 : .7); tg.rotateY(-sd * AL); tg.translate(q[0], q[1], q[2]); out.push(tg); } });
    [-.05, .05].forEach(x => { const tg = toothG(.035, .09, up); tg.scale(1, 1, .6); tg.translate(x, v, 1.47); out.push(tg); }); return merge(out); }
  const mand = new T.Mesh(merge(manParts), jawMat); const MJ = new T.Group(); MJ.position.copy(PIV); MJ.add(mand); SK.add(MJ);
  MJ.add(new T.Mesh(toothRow(-.57, true), toothMat));
  // upper jaw: a slim alveolar arch with small teeth
  const up0 = (sd, u, v) => { const q = side2(sd, u, v); return [q[0], q[1] + PIV.y, q[2] + PIV.z]; };
  const maxG = sweep(new T.CatmullRomCurve3(V3([up0(1, .7, -.32), up0(1, 1.3, -.34), [0, PIV.y - .35, PIV.z + 1.52], up0(-1, 1.3, -.34), up0(-1, .7, -.32)])), 60, 12, s => [.12, .065]); maxG.translate(0, .06, 0);
  SK.add(new T.Mesh(maxG, jawMat));
  const upT = new T.Mesh(toothRow(-.39, false), toothMat); upT.position.copy(PIV); SK.add(upT);
  // a soft warm light inside the head so the jaw reads without hard edges
  const jLight = new T.PointLight('#ffc89a', 0, 4.5, 1.8); jLight.position.set(.2, -.2, .6); SK.add(jLight);
  // ---------- ancient ocean ----------
  const shafts = K.shafts(S, { n: 10, top: 60, height: 140, spread: 120, depth: 60, opacity: .1, color: '#7cc6ff' }); shafts.group.position.set(0, 0, 30);
  const snow = K.snow(S, { n: 3500, box: [80, 50, 60], size: .14, opacity: .5, fall: .3, color: '#bfe2ff' });
  const dust = K.snow(S, { n: 1400, box: [24, 22, 18], size: .09, opacity: .7, fall: .04, color: '#ffcf9a', seed: 9 });
  // early armoured fish: broad head shield, tapering body, vertical tail fin (ONE mesh each)
  const fC = document.createElement('canvas'); fC.width = 512; fC.height = 256; { const fg = fC.getContext('2d'), gr = fg.createLinearGradient(0, 0, 0, 256);
    [[0, '#3e3a30'], [.18, '#1c1d1b'], [.3, '#1a1b1a'], [.5, '#4a463a'], [.68, '#857e68'], [.75, '#9a927a'], [.82, '#857e68'], [1, '#3e3a30']].forEach(([o, c]) => gr.addColorStop(o, c)); fg.fillStyle = gr; fg.fillRect(0, 0, 512, 256);
    fg.globalCompositeOperation = 'overlay'; fg.globalAlpha = .5; fg.drawImage(K.noise(256, { seed: 73, octaves: 5, sx: 3 }), 0, 0, 512, 256); fg.globalCompositeOperation = 'source-over'; fg.globalAlpha = 1;
    fg.strokeStyle = 'rgba(200,190,160,.35)'; fg.lineWidth = 2; const r = K.rng(8); for (let k = 0; k < 40; k++) { const x = 512 * (.68 + r() * .3), y = r() * 256; fg.strokeRect(x, y, 10 + r() * 22, 8 + r() * 18); }
    for (let x = 30; x < 350; x += 9) { fg.strokeStyle = 'rgba(0,0,0,.25)'; fg.lineWidth = 1.5; fg.beginPath(); fg.moveTo(x, 0); fg.lineTo(x + 6, 256); fg.stroke(); } }
  const fMap = K.tex(fC, true); fMap.flipY = false;
  const fishMat = new T.MeshStandardMaterial({ map: fMap, color: '#ffffff', roughness: .45, metalness: .1, normalMap: K.normalMap(K.noise(512, { seed: 71, octaves: 3, sx: 2 }), 4), normalScale: new T.Vector2(.8, .8), envMapIntensity: .6 });
  fishMat.onBeforeCompile = sh => { Object.assign(sh.uniforms, RIM); fadeN(sh, 16, 55);
    sh.fragmentShader = sh.fragmentShader.replace('#include <common>', '#include <common>\nuniform vec3 rimL;').replace('#include <emissivemap_fragment>', `#include <emissivemap_fragment>
    { float fr=pow(1.-max(dot(normal,normalize(vViewPosition)),0.),2.5); totalEmissiveRadiance += vec3(.45,.75,1.)*fr*.7*${RIMW}; }`); };
  function makeFish(type) { const L = type ? 4.2 : 3.2;
    const KW = type ? [[0, .02], [.06, .03], [.25, .12], [.5, .3], [.7, .42], [.86, .44], [.96, .3], [1, .04]] : [[0, .015], [.08, .04], [.3, .15], [.55, .3], [.7, .55], [.85, .6], [.95, .48], [1, .05]];
    const KH = type ? [[0, .5], [.05, .45], [.11, .09], [.3, .2], [.55, .36], [.75, .38], [.92, .28], [1, .05]] : [[0, .42], [.045, .38], [.1, .08], [.3, .15], [.55, .22], [.75, .26], [.9, .2], [1, .04]];
    const wF = curve(KW, 1), hF = curve(KH, 1), extra = [];
    if (type) [1, -1].forEach(sd => { const f = K.fin([[0, 0], [.5, .12], [1.1, .05], [1.0, -.1], [.3, -.12]], .05); f.rotateX(Math.PI / 2); f.rotateY(sd * .5); f.rotateZ(-.25); f.translate(L * .2, -.15, sd * .45); f.userData.v = .8; extra.push(f); });
    const b = K.body({ length: L, seg: 90, ring: 28, belly: .35, ridge: type ? .25 : .05, width: wF, height: hF, extra });
    const m = new T.Mesh(b.geo, fishMat); const grp = new T.Group(); grp.add(m);
    const eye = new T.Mesh(new T.SphereGeometry(.05, 10, 8), new T.MeshBasicMaterial({ color: '#cfe8ff' })); [1, -1].forEach(sd => { const e = eye.clone(); e.position.set(L * .44, .1, sd * wF(.94) * .8); grp.add(e); });
    return { grp, update(t, ph) { b.deform((s, th, base, k) => [0, type && s < .1 && base[k * 3 + 1] > 0 ? .1 * (1 - s / .1) : 0, .32 * Math.pow(1 - Math.min(1, s), 2.2) * Math.sin(t * 3.2 + ph - s * 6.5)]); } }; }
  const FISH = [[0, 0, 2.0, 7.5, 16, 1, -1], [1, 1.1, .2, -1, 14, 1, 1.0], [0, 2.3, 4.0, 11, 24, .85, -1.1], [0, .5, 6.0, 1, 30, .8, 1.0], [1, 3.4, 1.4, 14, 34, 1, -1.2]].map(([ty, ph, y, x0, z, sc, v]) => { const f = makeFish(ty); f.grp.scale.setScalar(sc); S.add(f.grp); f.grp.visible = false; return { f, ph, y, x0, z, v }; });
  // ---------- light ----------
  // cool neutral fill (form and colour stay readable), a warm back light from upper left (its halo stays in frame), a soft side key
  const hemi = new T.HemisphereLight('#8a98b8', '#0a0a14', .4); S.add(hemi);
  const rim = new T.DirectionalLight('#ffd2a0', 2.2); rim.position.set(-9, 11, -12); S.add(rim);
  const rim2 = new T.DirectionalLight('#9fc0ff', .8); rim2.position.set(10, 4, -12); S.add(rim2);
  const key = new T.DirectionalLight('#dfe6f2', .35); key.position.set(14, 5, 6); S.add(key);
  const backG = ctx.glow(S, '#ffc890', 24, .2), backG2 = ctx.glow(S, '#ff9a5a', 9, .14); backG.renderOrder = backG2.renderOrder = -1;
  const RD = new T.Vector3(-9, 11, -12).normalize(), OD = new T.Vector3(0, 1, -.35).normalize(), LW = new T.Vector3(), HO = new T.Vector3(-7, 3.2, -10);
  const top = new T.DirectionalLight('#9fd8ff', 0); top.position.set(0, 50, 20); S.add(top);
  const cam = new T.PerspectiveCamera(35, ctx.W / ctx.H, .1, 900); ctx.side(cam, p.side == null ? .13 : p.side);
  const tgt = new T.Vector3();
  function camAt(t, pos, tg) { const t0 = ctx.t; ctx.t = t; const u = t - ctx.t0, oc = at(p.ocean, 4), kR = at(p.ribs, 2.5), kJ = at(p.jaw, 1.6);
    const a0 = .35 + Math.min(u, (p.ocean ? cue(p.ocean) + 4.5 : 1e9) - ctx.t0) * .025 - .2 * oc;
    let d = 11.5 - .8 * sm(0, 3.5, u) + 6.5 * kR - 2.8 * kJ; tg.set(.3 - .2 * kR, .7 - .3 * kR + 6.9 * kJ, 0);
    const back = oc * oc * (3 - 2 * oc); d += 44 * back; tg.y += (3.6 - tg.y) * back;
    pos.set(Math.sin(a0) * d, tg.y + 1.2 + 1.5 * kJ - 1.5 * kJ * (1 - back) + 3 * back, Math.cos(a0) * d); ctx.t = t0; }
  // the far camera's frame (after the pull back): the fish swim across it
  const FP = new T.Vector3(), FT = new T.Vector3(); camAt(p.ocean ? cue(p.ocean) + 4.5 : ctx.t1, FP, FT);
  const FF = FT.clone().sub(FP).normalize(), FR = new T.Vector3().crossVectors(FF, new T.Vector3(0, 1, 0)).normalize(), FU = new T.Vector3().crossVectors(FR, FF), FY = Math.atan2(-FR.z, FR.x);
  const revOf = (c, y0, y1, d) => c == null ? -99 : y0 + (y1 - y0) * sm(cue(c), cue(c) + d, ctx.t) + (ctx.t < cue(c) ? -99 : 0);
  return { scene: S, camera: cam, draw(t, u) {
    ctx.t = t;
    // heartbeat: ~72 per minute, lub-dub; the atria squeeze just before the ventricles
    const ph = (t * 1.2) % 1, lub = Math.exp(-Math.pow((ph - .12) / .05, 2)), dub = .55 * Math.exp(-Math.pow((ph - .3) / .05, 2)), beat = lub + dub;
    HU.beat.value = beat; HU.atr.value = Math.exp(-Math.pow((ph - .02) / .05, 2)); HU.emk.value = .7 + 1.3 * beat;
    hGlow.material.opacity = .22 + .25 * beat; hGlow2.material.opacity = .18 + .3 * beat; hGlow.scale.setScalar(8 + 2.5 * beat);
    const oc = at(p.ocean, 4), fishK = at(p.fish, 3);
    hLight.intensity = (16 + 26 * beat) * (1 - .7 * oc);
    // reveals
    ribMat.userData.U.rev.value = revOf(p.ribs, -5, 4.5, 1.3); spineMat.userData.U.rev.value = revOf(p.spine, -6, 7, 1.4);
    jawMat.userData.U.rev.value = revOf(p.jaw, 4.5, 10, 1.2); toothMat.userData.U.rev.value = jawMat.userData.U.rev.value;
    LU.op.value = at(p.lungs, 1.5) * (1 - .8 * oc); LU.br.value = .5 - .5 * Math.cos((t - (p.lungs ? cue(p.lungs) : 0)) * 2 * Math.PI / 3.6);
    lungs.forEach(l => l.visible = LU.op.value > .01);
    GU.op.value = at(p.jaw, 1.5) * (1 - oc);
    // the jaw "speaks": opens on "open", then a few short syllables
    const jc = p.open ? cue(p.open) : 1e9, jt = t - jc; let jo = 0;
    if (jt > -.3) { jo = .3 * sm(-.3, .25, jt) * (1 - sm(.6, 1.0, jt)) + (jt > .9 && jt < 3.6 ? .14 * Math.pow(Math.max(0, Math.sin((jt - .9) * Math.PI * 2.6)), 1.4) * (1 - sm(3.0, 3.6, jt)) : 0); }
    MJ.rotation.x = jo; GU.jo.value = jo; jLight.intensity = 6 * GU.op.value;
    // ocean
    S.background.copy(BG0).lerp(BG1, oc); S.fog.color.copy(BG0).lerp(BG1, oc); S.fog.density = .004 + .028 * oc;
    S.fog.density = .03 * (1 - oc) + (.004 + .028 * oc) * oc;
    shafts.update(t, oc); top.intensity = 1.2 * oc; hemi.intensity = .4 + .2 * oc; hemi.color.set('#8a98b8').lerp(new T.Color('#3a8ac8'), oc);
    rim.intensity = 2.2 * (1 - .6 * oc); rim2.intensity = .8 * (1 - oc); backG.material.opacity = .2 * (1 - oc); backG2.material.opacity = .14 * (1 - oc);
    snow.points.material.opacity = .5 * oc; snow.points.visible = oc > .01; dust.points.material.opacity = .65 * (1 - oc);
    // camera: close on the heart -> wider for ribs/spine/lungs -> up to the jaws -> far back into the ancient sea
    camAt(t, cam.position, tgt); cam.lookAt(tgt); cam.updateMatrixWorld();
    // the back light's halo sits behind the subject toward the light (upper left), so the light side stays in frame
    backG.position.copy(tgt).add(HO); backG2.position.copy(tgt).addScaledVector(HO, .8);
    LW.copy(RD).lerp(OD, oc).normalize(); RIM.rimL.value.copy(LW).transformDirection(cam.matrixWorldInverse);
    snow.update(t, [cam.position.x, cam.position.y, cam.position.z - 20]); dust.update(t, [0, 2, 0]);
    // fish glide across in front of the far camera
    FISH.forEach(({ f, ph: fp, y, x0, z, v }) => { f.grp.visible = fishK > .01; if (!f.grp.visible) return; const tt = t - (p.fish ? cue(p.fish) : 0);
      f.grp.position.copy(FP).addScaledVector(FF, z).addScaledVector(FR, x0 + v * .8 * tt).addScaledVector(FU, y + .4 * Math.sin(tt * .6 + fp)); f.grp.rotation.y = FY + (v > 0 ? 0 : Math.PI); f.grp.rotation.z = .05 * Math.sin(tt * .5 + fp); f.update(t, fp); });
  } };
};
