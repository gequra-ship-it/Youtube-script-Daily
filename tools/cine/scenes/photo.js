// photo — a real photograph as a 2.5D shot (2026-10-15, "use free real photos first, 3D only where no photo exists").
// The photo is a dense plane pushed toward the camera by its depth map (tools/depth_prep.py), so a slow camera move gives
// real parallax. A grade matches photos taken in different light to the scene (night, deep sea, space). Only light is added
// in 3D (fireflies, marine snow, stars). Use it in "cuts" chapters, one shot per photo; seq switches to further photos on
// words inside the same unit (a shot can only start on a unit).
// Files: videos/<slug>/plates/photo/<img>.jpg and <img>_depth.png (build_cine inlines them as <img id="ph_/dp_<img>">).
// params: img (name), D (depth push, .3-.6; 0 for flat pictures such as deep-sky images), move [[x,y,z],[x,y,z]] (camera
//   from/to over the photo's time, keep within +-.3), grade 'none'|'night'|'deep'|'space', gk (grade strength 0-1),
//   flash (cue: a short light flash), fx 'fireflies'|'snow'|'stars'|'none', side (text panel offset),
//   seq [{at: cue, img, D, move, grade, gk}, ...] (next photos, cross-faded in 0.3 s at each cue)
(window.MIYA = window.MIYA || { scenes: {} }).scenes.photo = function (ctx, p) {
  const { T, cue } = ctx, S = new T.Scene(); S.background = new T.Color('#020308');
  const cam = new T.PerspectiveCamera(30, ctx.W / ctx.H, .05, 100); ctx.side(cam, p.side == null ? .08 : p.side);
  const Z = 3.2, fa = ctx.W / ctx.H;
  const tex = (el, srgb) => { const t = new T.Texture(el); t.colorSpace = srgb ? T.SRGBColorSpace : T.NoColorSpace; t.minFilter = T.LinearFilter; t.generateMipmaps = false; return t; };
  function layer(c, start, order) {
    const im = document.getElementById('ph_' + c.img), dm = document.getElementById('dp_' + c.img);
    if (!im || !dm) throw new Error('photo ' + c.img + ': no inlined image (videos/<slug>/plates/photo/' + c.img + '.jpg and _depth.png)');
    const ph = tex(im, true), dp = tex(dm, false), asp = (im.naturalWidth || 3) / (im.naturalHeight || 2);
    let h = 2 * Math.tan(15 * Math.PI / 180) * Z * 1.08, w = h * fa; if (w / h < asp) w = h * asp; else h = w / asp;   // cover the frame (+8%)
    const G = { none: 0, night: 1, deep: 2, space: 3 }[c.grade || 'none'];
    const mat = new T.ShaderMaterial({ transparent: true, uniforms: { ph: { value: ph }, dp: { value: dp }, D: { value: c.D == null ? .4 : c.D }, G: { value: G }, gk: { value: c.gk == null ? .6 : c.gk }, fl: { value: 0 }, op: { value: 1 } },
      vertexShader: `uniform sampler2D dp; uniform float D; varying vec2 vU; void main(){ vU = uv; vec3 q = position; q.z += D * texture2D(dp, uv).r * ${(Z * .25).toFixed(3)}; gl_Position = projectionMatrix * modelViewMatrix * vec4(q, 1.); }`,
      fragmentShader: `uniform sampler2D ph; uniform float G, gk, fl, op; varying vec2 vU;
        void main(){ vec3 c = texture2D(ph, vU).rgb, g = c; float l = dot(c, vec3(.299, .587, .114));
          if (G > .5 && G < 1.5) g = pow(mix(vec3(l), c, .45) * vec3(.55, .68, 1.05) * .55, vec3(1.12)) + vec3(.004, .006, .014);   // moonlight
          else if (G > 1.5 && G < 2.5) g = mix(vec3(l), c, .6) * vec3(.35, .72, .95) * .8;                                        // deep water: red goes first
          else if (G > 2.5) g = pow(c, vec3(1.15)) * vec3(.92, .95, 1.08);                                                        // space: deeper blacks, cooler
          c = mix(c, g, gk);
          vec2 q = vU - .5; c *= 1. - .5 * dot(q, q) * 2.;
          gl_FragColor = vec4(c + fl * vec3(1., .95, .75), op); }` });
    const plane = new T.Mesh(new T.PlaneGeometry(w, h, 240, Math.round(240 / Math.max(asp, .3))), mat); plane.position.z = -Z - order * .01; plane.frustumCulled = false; plane.renderOrder = order; S.add(plane);
    return { plane, mat, texs: [ph, dp], start, mv: c.move || [[0, 0, .15], [0, 0, -.05]] };
  }
  const L = [layer(p, ctx.t0, 0)].concat((p.seq || []).map((c, i) => layer(c, cue(c.at), i + 1)));
  // light-only effects in front of the photos
  const NF = p.fx === 'stars' ? 260 : p.fx === 'snow' ? 500 : p.fx === 'fireflies' ? 60 : 0, rr = ctx.rng(11), FD = [];
  const fx = NF ? ctx.points(NF, { size: p.fx === 'snow' ? .012 : p.fx === 'stars' ? .006 : .03, color: p.fx === 'fireflies' ? '#f4f090' : '#dfe8ff' }) : null;
  if (fx) { S.add(fx); for (let i = 0; i < NF; i++) FD.push([(rr() - .5) * 3, (rr() - .5) * 1.8, -.8 - rr() * 2, rr() * 6.28, .5 + rr()]); }
  const fc = p.flash ? cue(p.flash) : null;
  return { scene: S, camera: cam, draw(t) {
    let a = 0; L.forEach((l, i) => { l.texs.forEach(x => { if (!x.userData.ok && x.image.complete && x.image.naturalWidth) { x.needsUpdate = true; x.userData.ok = 1; } }); if (t >= l.start) a = i; });
    L.forEach((l, i) => { const o = i === 0 ? 1 : Math.min(1, Math.max(0, (t - l.start) / .3)); l.mat.uniforms.op.value = o; l.plane.visible = i <= a; });
    const l = L[a], end = a + 1 < L.length ? L[a + 1].start : ctx.t1, k = Math.min(1, Math.max(0, (t - l.start) / Math.max(.5, end - l.start))), e = k * k * (3 - 2 * k), mv = l.mv;
    cam.position.set(mv[0][0] + (mv[1][0] - mv[0][0]) * e, mv[0][1] + (mv[1][1] - mv[0][1]) * e, mv[0][2] + (mv[1][2] - mv[0][2]) * e);
    if (fc != null && t > fc) cam.position.z -= .06 * Math.exp(-(t - fc) * 4);
    cam.lookAt(cam.position.x * .3, cam.position.y * .3, -Z);
    L.forEach(x => { x.mat.uniforms.fl.value = fc != null ? .45 * Math.exp(-Math.pow((t - fc) / .06, 2)) : 0; });
    if (fx) { const ar = fx.geometry.attributes.position.array, c = fx.geometry.attributes.color.array;
      for (let i = 0; i < NF; i++) { const [x, y, z, ph2, sp] = FD[i]; let b;
        if (p.fx === 'snow') { ar.set([x + .05 * Math.sin(t * .3 + ph2), ((y - t * .02 * sp) % .9 + .9) % 1.8 - .9, z], i * 3); b = .35 + .25 * sp; }
        else if (p.fx === 'stars') { ar.set([x, y, z - 1], i * 3); b = (.25 + .5 * sp * sp) * (.75 + .25 * Math.sin(t * 2 * sp + ph2)); }
        else { ar.set([x + .25 * Math.sin(t * .2 * sp + ph2), y * .6 + .1 * Math.sin(t * .3 * sp + ph2 * 2), z], i * 3); b = Math.pow(Math.max(0, Math.sin(t * (.8 + sp * .6) + ph2 * 3)), 6); }
        c.set(p.fx === 'fireflies' ? [b, b, b * .6] : [b, b, b], i * 3); }
      fx.geometry.attributes.position.needsUpdate = fx.geometry.attributes.color.needsUpdate = true; }
  } };
};
