// paleblue — the Pale Blue Dot short (cosmic-prison-cine-short3, written 2026-10-16). One file, five scene types that share a
// small toolkit (probe model copied from voyager.js, globe shaders copied from earth.js; neither file is changed). No text.
// requires: earth
//
// pbdot      the famous image as a real 3D place: broad soft bands of scattered sunlight (axial billboards, so they read from any
//            angle) fanning down from a Sun far above the frame, warm dust motes drifting in the beam, and a tiny pale-blue speck
//            (Earth) inside the warm band. The speck breathes gently (period ~2.6 s).
//   view     'photo' (default) camera looks along the bands' plane, like the photograph; 'beam' the camera sees the beam from the
//            side, Earth one mote among the dust
//   d0, d1   camera distance at shot start / end (photo; eased in log space; default 40 / 24)
//   dive     cue: the camera rushes in from far outside the bands (700 units) to d0 within 3.4 s (motes stream past as streaks)
//   life     cue: warm city-light glints flicker inside the dot's halo for `lifeDur` s (default 3.2; each rises .2 s, fades 1.1 s)
//   pixel    cue: a faint pixel grid fades in around the dot; the dot's own cell is outlined in warm light (0.12 of a pixel)
//   ping     cue (or list of cues): a soft ring breathes out from the dot
//   pull     cue (beam): from close on the small globe the camera pulls back until Earth is a mote in the sunbeam (4.8 s)
//   bd0, bd1 beam view distances (default .32 = close on the globe, 38 = a mote); without `pull` eased over the whole shot
//   dim      cue: the whole picture fades down softly (2.5 s) for the ending
//   orbit    degrees of slow sideways drift over the shot (default 6)
// pbprobe    the Voyager probe (real parts, rim light) and its scan platform. `view` picks the staging:
//   'hero'   slow close orbit, the Sun small and bright behind
//   'turn'   cue `turn`: the scan platform swings its cameras round toward the Sun while the camera circles to look over its shoulder
//   'glare'  over the platform toward the Sun; cue `glare`: the Sun's glare swells, warm ghosts slide across, the frame burns warm
//   'off'    close on the platform, its status lights lit; cue `off`: lights die, the platform parks, the view fades to near dark
//   'away'   the probe recedes into the dark, dish toward us (cue `away`, default the shot start)
//   'data'   from behind the probe toward the faint Sun; faint pulses leave the dish and trickle inward (recycling, seek-safe)
//   'deep'   interstellar: the faint violet heliosphere bubble behind the probe, the Sun only a bright star inside it
//   'shell'  wide: the Sun/Earth point at the centre of a faint golden sphere one light-day across; the probe's glint travels out
//            along a dotted trail and touches the sphere on cue `reach` (ripple + glint)
//   all views: `side` (landscape offset), `lift` (vertical frames: subject raised by this fraction of the height)
// pbportrait the Family Portrait: 60 frames on a gently curved wall (6 x 10, thin glass panels with bevelled glowing edges); each
//            frame snaps in turn (soft warm shutter flash: rise .15 s, fade 1 s) and shows its picture (grain, scattered-light band,
//            Sun glare, a planet speck; one frame holds the band with the pale blue speck)
//   snap     cue of the first snap (default shot start + .4 s); dur: seconds for all 60 (default 5.6)
//   dive     cue: the camera rushes into the Earth frame until it fills the screen (2 s; hand over with a `zoom` transition)
// pbearth    Earth (procedural globe of earth.js: day, night lights, clouds, atmosphere rim), Sun to the left
//   view     'pulse' radio pulse shells leave Earth on cue `pulse`, camera backs away to watch them go
//            'clock' Earth turns once between cue `day` and the shot end while a thin ring's marker sweeps once round it (a day
//                    clock without numbers); a slow pulse shell travels outward from cue `pulse`
//            'home'  close slow orbit over clouds and the night-side lights
//            'fragile' pull back from close until Earth is small and alone (cue `pull`, default shot start + .5)
// pbsystem   the inner Solar System seen from above at a tilt: Sun, faint orbits, Earth moving a quarter turn along its orbit over
//            the shot (months pass) with a fading trail, faint data pulses streaming in from deep space to Earth
(function () {
  const M = (window.MIYA = window.MIYA || { scenes: {} });
  const envl = (x, r, f) => x <= 0 ? 0 : x < r ? (x / r) * (x / r) * (3 - 2 * x / r) : Math.exp(-(x - r) / f);
  const ease5 = x => { x = Math.min(1, Math.max(0, x)); return x * x * x * (x * (x * 6 - 15) + 10); };
  const cues = (ctx, c) => c == null ? [] : (Array.isArray(c) ? c : [c]).map(x => ctx.cue(x));
  // landscape fov -> the vertical frame's fov (same rule as ctx.side / voyager.js), then subject offset: side (landscape) or lift (vertical)
  const vf = (ctx, f) => { if (!ctx.VERT) return f; const h = 2 * Math.atan(Math.tan(f * Math.PI / 360) * 16 / 9 * .62); return 2 * Math.atan(Math.tan(h / 2) * ctx.H / ctx.W) * 180 / Math.PI; };
  function lift(ctx, cam, side, f, fov) { if (fov != null) cam.fov = vf(ctx, fov);
    if (ctx.VERT) { if (f) cam.setViewOffset(ctx.W, ctx.H, 0, ctx.H * f, ctx.W, ctx.H); else cam.clearViewOffset(); }
    else cam.setViewOffset(ctx.W, ctx.H, -ctx.W * (side || 0), 0, ctx.W, ctx.H);
    cam.updateProjectionMatrix(); }

  // camera-facing streak quads (from voyager.js): set(i, head, tail, width, rgb) each frame from t only
  function streaks(ctx, par, n, o) { const T = ctx.T; o = o || {}; const g = new T.BufferGeometry(), H = new Float32Array(n * 12), Tl = new Float32Array(n * 12), C = new Float32Array(n * 12), Wd = new Float32Array(n * 4), cr = new Float32Array(n * 8), ix = [];
    for (let i = 0; i < n; i++) { cr.set([0, 0, 0, 1, 1, 0, 1, 1], i * 8); const b = i * 4; ix.push(b, b + 2, b + 1, b + 1, b + 2, b + 3); }
    const ad = (a, k, nm) => { const q = new T.BufferAttribute(a, k); q.setUsage(T.DynamicDrawUsage); g.setAttribute(nm, q); };
    ad(H, 3, 'aH'); ad(Tl, 3, 'aT'); ad(C, 3, 'aC'); ad(Wd, 1, 'aW'); g.setAttribute('corner', new T.BufferAttribute(cr, 2)); g.setAttribute('position', new T.BufferAttribute(new Float32Array(n * 12), 3)); g.setIndex(ix);
    const m = new T.ShaderMaterial({ uniforms: { uH: { value: ctx.H }, uMin: { value: o.minPx || 1.6 }, uNear: { value: new T.Vector2(...(o.near || [.5, 4])) } }, transparent: true, depthWrite: false, blending: T.AdditiveBlending, side: T.DoubleSide,
      vertexShader: `attribute vec3 aH, aT, aC; attribute float aW; attribute vec2 corner; uniform float uH, uMin; uniform vec2 uNear; varying vec2 vUv; varying vec3 vC; varying float vCap;
        void main(){ vec3 wH = (modelMatrix * vec4(aH, 1.)).xyz, wT = (modelMatrix * vec4(aT, 1.)).xyz, d = wH - wT; float L = length(d); vec3 dir = L > 1e-5 ? d / L : vec3(1., 0., 0.);
          vec3 P0 = mix(wT, wH, corner.x), V = cameraPosition - P0; float dc = max(length(V), 1e-4);
          float w = max(aW, dc * 2. / (projectionMatrix[1][1] * uH) * uMin); vec3 sd = cross(dir, V); float sl = length(sd); sd = sl > 1e-6 ? sd / sl : vec3(0., 1., 0.);
          vec3 P = P0 + sd * (corner.y - .5) * w + dir * (corner.x - .5) * w;
          vUv = corner; vCap = clamp(w / (L + w), .02, 1.); vC = aC * (aW / w) * smoothstep(uNear.x, uNear.y, dc);
          gl_Position = projectionMatrix * viewMatrix * vec4(P, 1.); }`,
      fragmentShader: `varying vec2 vUv; varying vec3 vC; varying float vCap;
        void main(){ float x = vUv.x, y = abs(vUv.y * 2. - 1.); float a = pow(x, 1.6) * smoothstep(1., 1. - vCap, x) * pow(max(0., 1. - y * y), 2.);
          gl_FragColor = vec4(vC * a, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` });
    const Ms = new T.Mesh(g, m); Ms.frustumCulled = false; Ms.renderOrder = o.order || 0; par.add(Ms);
    return { mesh: Ms, set(i, hx, hy, hz, tx, ty, tz, w, r, gg, b) { for (let k = 0; k < 4; k++) { const j = (i * 4 + k) * 3; H[j] = hx; H[j + 1] = hy; H[j + 2] = hz; Tl[j] = tx; Tl[j + 1] = ty; Tl[j + 2] = tz; C[j] = r; C[j + 1] = gg; C[j + 2] = b; Wd[i * 4 + k] = w; } },
      hide(i) { for (let k = 0; k < 4; k++) { const j = (i * 4 + k) * 3; C[j] = C[j + 1] = C[j + 2] = 0; } },
      commit() { ['aH', 'aT', 'aC', 'aW'].forEach(k => g.attributes[k].needsUpdate = true); } }; }

  // soft points whose pixel size is clamped to [2, max] (smaller ones dim instead: nothing shimmers); per-point colour
  function cpoints(ctx, par, pos, col, o) { const T = ctx.T, g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(pos, 3)); g.setAttribute('color', new T.BufferAttribute(col, 3));
    if (o.phase) g.setAttribute('phase', new T.BufferAttribute(o.phase, 1));
    const U = { uS: { value: o.size }, uMax: { value: o.max || 4 }, uH: { value: ctx.H }, uO: { value: 1 }, uT: { value: 0 }, uNear: { value: o.near || 0 }, uMap: { value: ctx.dotTex() } };
    const P = new T.Points(g, new T.ShaderMaterial({ uniforms: U, transparent: true, depthWrite: false, blending: T.AdditiveBlending,
      vertexShader: `attribute vec3 color; ${o.phase ? 'attribute float phase;' : 'float phase = 0.;'} uniform float uS, uMax, uH, uO, uT, uNear; varying vec3 vC;
        void main(){ vec4 mv = modelViewMatrix * vec4(position, 1.); float z = max(-mv.z, 1e-4), px = uS * uH * .5 * projectionMatrix[1][1] / z;
          float tw = ${o.phase ? '.65 + .35 * sin(uT * (.6 + .5 * fract(phase * 7.)) + phase * 6.283)' : '1.'};
          vC = color * uO * tw * min(1., px / 2.) * smoothstep(uNear * .4, uNear, z) * step(0., -mv.z); gl_PointSize = clamp(px, 2., uMax); gl_Position = projectionMatrix * mv; }`,
      fragmentShader: `uniform sampler2D uMap; varying vec3 vC;
        void main(){ float a = texture2D(uMap, gl_PointCoord).r; gl_FragColor = vec4(vC * a, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` }));
    P.frustumCulled = false; par.add(P); return { P, U }; }

  // sky: navy gradient sphere at infinity + star layers riding with the camera (no parallax), soft >= 2 px points
  function sky(ctx, S, o) { const T = ctx.T; o = o || {};
    const U = { uK: { value: 1 }, uS: { value: (o.sun || new T.Vector3(0, 1, 0)).clone().normalize() }, uH: { value: o.halo == null ? 1 : o.halo } };
    const m = new T.Mesh(new T.SphereGeometry(1, 32, 16), new T.ShaderMaterial({ uniforms: U, side: T.BackSide, depthWrite: false, depthTest: false,
      vertexShader: `varying vec3 vD; void main(){ vD = position; vec4 q = projectionMatrix * vec4(mat3(viewMatrix) * position, 1.0); gl_Position = vec4(q.xy, q.w * .99999, q.w); }`,
      fragmentShader: `varying vec3 vD; uniform vec3 uS; uniform float uK, uH;
        void main(){ vec3 d = normalize(vD); vec3 c = mix(vec3(.004,.005,.014), vec3(.01,.011,.03), .5 + .5 * d.y);
          float th = acos(clamp(dot(d, uS), -1., 1.)); c += vec3(1., .72, .4) * (.03 * exp(-th * th / .05) + .01 * exp(-th * th / .7)) * uH;
          gl_FragColor = vec4(c * uK, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` }));
    m.frustumCulled = false; m.renderOrder = -10; S.add(m);
    const G = new T.Group(); S.add(G); const r = ctx.rng(o.seed || 3), layers = [];
    [[o.n || 2200, 2.1], [Math.round((o.n || 2200) / 9), 3.4]].forEach(([n, size]) => { const g = new T.BufferGeometry(), a = new Float32Array(n * 3), c = new Float32Array(n * 3);
      for (let i = 0; i < n; i++) { const u = r() * 2 - 1, th = r() * 6.283, q = Math.sqrt(1 - u * u); a.set([q * Math.cos(th), u, q * Math.sin(th)], i * 3);
        const tp = r(), br = (.3 + .9 * Math.pow(r(), 2.2)) * (o.bright || 1), col = tp < .25 ? [.75, .82, 1] : tp < .8 ? [1, .96, .9] : [1, .82, .6]; c.set(col.map(x => x * br), i * 3); }
      g.setAttribute('position', new T.BufferAttribute(a, 3)); g.setAttribute('color', new T.BufferAttribute(c, 3));
      const P = new T.Points(g, new T.PointsMaterial({ size, map: ctx.dotTex(), vertexColors: true, transparent: true, blending: T.AdditiveBlending, depthWrite: false, depthTest: false, sizeAttenuation: false }));
      P.frustumCulled = false; P.renderOrder = -9; G.add(P); layers.push(P); });
    return { U, G, layers, update(cam, k) { G.position.copy(cam.position); G.scale.setScalar(cam.near * 40); if (k != null) { U.uK.value = k; layers.forEach(l => l.material.opacity = k); } } }; }

  // a full-screen fade plane in front of the camera (black, or additive warm for glare)
  function veil(ctx, S, cam, col, additive) { const T = ctx.T; if (!cam.parent) S.add(cam);
    const m = new T.Mesh(new T.PlaneGeometry(1, 1), new T.MeshBasicMaterial({ color: col, transparent: true, opacity: 0, depthTest: false, depthWrite: false, blending: additive ? T.AdditiveBlending : T.NormalBlending, toneMapped: !additive }));
    m.renderOrder = 100; m.frustumCulled = false; cam.add(m);
    return { m, set(op) { m.visible = op > .002; m.material.opacity = op; const z = cam.near * 1.5, h = 2 * z * Math.tan(cam.fov * Math.PI / 360) * 1.6; m.position.set(0, 0, -z); m.scale.set(h * 2, h * 2, 1); } }; }

  // ring texture for pings / ripples
  function ringTex(ctx) { return M._pbRing || (M._pbRing = ctx.ctex(128, (g, s) => { const r = g.createRadialGradient(s / 2, s / 2, s * .3, s / 2, s / 2, s / 2);
    r.addColorStop(0, 'rgba(255,255,255,0)'); r.addColorStop(.72, 'rgba(255,255,255,.0)'); r.addColorStop(.86, 'rgba(255,255,255,1)'); r.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = r; g.fillRect(0, 0, s, s); })); }

  // ---------------- globe (earth.js shaders on the earth.js textures; the textures are made once per page) ----------------
  function earthTex(ctx) { if (!M._earthTex && M.scenes.earth) M.scenes.earth(Object.assign({}, ctx), {}); return M._earthTex; }
  function globe(ctx, S, SUN) { const T = ctx.T, TX = earthTex(ctx);
    const EG = new T.Group(); EG.rotation.z = .41; S.add(EG);
    const sphere = new T.SphereGeometry(1, 128, 64);
    const eU = { day: { value: TX.day }, night: { value: TX.night }, cloud: { value: TX.cloud }, ocean: { value: TX.ocean }, sunPos: { value: SUN }, cOff: { value: 0 }, city: { value: 1 }, uT: { value: 0 } };
    const vs = `varying vec2 vUv; varying vec3 vN; varying vec3 vP;
      void main() { vUv = uv; vN = normalize(mat3(modelMatrix) * normal); vec4 w = modelMatrix * vec4(position, 1.); vP = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`;
    const earthM = new T.ShaderMaterial({ uniforms: eU, vertexShader: vs,
      fragmentShader: `uniform sampler2D day, night, cloud, ocean; uniform vec3 sunPos; uniform float cOff, city, uT; varying vec2 vUv; varying vec3 vN; varying vec3 vP;
        void main() { vec3 N = normalize(vN), L = normalize(sunPos - vP), V = normalize(cameraPosition - vP); float nl = dot(N, L);
          vec3 d = texture2D(day, vUv).rgb; float cs = texture2D(cloud, vUv + vec2(cOff + .002, -.002)).r, oc = texture2D(ocean, vUv).r;
          float dif = smoothstep(-.03, .12, nl) * (.1 + .9 * max(nl, 0.));
          vec3 sunC = mix(vec3(1., .55, .32), vec3(1., .96, .9), smoothstep(.0, .18, nl));
          vec3 col = d * sunC * dif * 1.8 * (1. - .5 * cs);
          vec3 H = normalize(L + V); float nh = max(dot(N, H), 0.), gl = oc * (1. - cs) * smoothstep(0., .15, nl);
          col += sunC * gl * (pow(nh, 90.) * 2.2 + pow(nh, 12.) * .06);
          float nf = smoothstep(.05, -.14, nl); float shim = .75 + .5 * (texture2D(cloud, vUv * 7. + vec2(uT * .004, uT * .0025)).g - .55) / .45;
          col += texture2D(night, vUv).rgb * nf * (1. - .8 * cs) * 1.1 * city * shim;
          float fr = pow(1. - max(dot(N, V), 0.), 2.6), sf = smoothstep(-.3, .5, nl);
          col += vec3(.25, .5, 1.) * fr * (sf * .9 + .02);
          col = mix(col, vec3(.2, .38, .8) * dif, .08 * sf);
          gl_FragColor = vec4(col, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` });
    const earth = new T.Mesh(sphere, earthM); EG.add(earth);
    const cU = { cloud: { value: TX.cloud }, sunPos: { value: SUN }, cOff: { value: 0 } };
    const clouds = new T.Mesh(sphere, new T.ShaderMaterial({ uniforms: cU, transparent: true, depthWrite: false, vertexShader: vs,
      fragmentShader: `uniform sampler2D cloud; uniform vec3 sunPos; uniform float cOff; varying vec2 vUv; varying vec3 vN; varying vec3 vP;
        void main() { vec3 N = normalize(vN), L = normalize(sunPos - vP), V = normalize(cameraPosition - vP); float nl = dot(N, L);
          vec4 c = texture2D(cloud, vUv + vec2(cOff, 0.)); float a = c.r;
          float dif = smoothstep(-.06, .18, nl) * (.15 + .85 * max(nl, 0.));
          vec3 sunC = mix(vec3(1., .72, .55), vec3(1.), smoothstep(.0, .2, nl));
          vec3 col = vec3(.92, .94, 1.) * sunC * dif * (.45 + .55 * c.g) * .95 + vec3(.004, .006, .012);
          float fr = 1. - max(dot(N, V), 0.); a *= 1. - .5 * pow(fr, 4.);
          gl_FragColor = vec4(col, a * .95);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` })); clouds.scale.setScalar(1.008); EG.add(clouds);
    const aU = { sunPos: { value: SUN }, uB: { value: 1 } };
    const atmo = new T.Mesh(new T.SphereGeometry(1.1, 96, 48), new T.ShaderMaterial({ uniforms: aU, side: T.BackSide, transparent: true, depthWrite: false, blending: T.AdditiveBlending,
      vertexShader: `varying vec3 vN; varying vec3 vP; varying vec3 vNv;
        void main() { vN = normalize(mat3(modelMatrix) * normal); vNv = normalize(normalMatrix * normal); vec4 w = modelMatrix * vec4(position, 1.); vP = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
      fragmentShader: `uniform vec3 sunPos; uniform float uB; varying vec3 vN; varying vec3 vP; varying vec3 vNv;
        void main() { vec3 L = normalize(sunPos - vP), Vd = normalize(vP - cameraPosition); float k = clamp(-vNv.z / .42, 0., 1.);
          float a = pow(k, 3.2), sw = smoothstep(-.45, .6, dot(normalize(vN), L)), fwd = pow(max(dot(Vd, L), 0.), 5.);
          vec3 col = (vec3(.28, .55, 1.) * a * (sw * 1.1 + .04) + vec3(.75, .8, 1.) * a * fwd * 4.5) * uB;
          gl_FragColor = vec4(col, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` }));
    EG.add(atmo); atmo.rotation.z = 0;
    return { EG, earth, clouds, atmo, eU, aU, set(t, rot) { earth.rotation.y = rot; clouds.rotation.y = rot + .0006 * t; const o = -t * .0018; eU.cOff.value = o; cU.cOff.value = o; eU.uT.value = t; } }; }

  // ---------------- the Voyager probe (model from voyager.js) ----------------
  function probe(ctx, S, SD, roll) { const T = ctx.T, K = M.kit, E = ctx.env(), v3 = (x, y, z) => new T.Vector3(x, y, z);
    const PROBE = new T.Group(); S.add(PROBE);
    const RIMU = { value: new T.Vector3() }, RIMK = { value: 1 };
    function rim(m, k, col) { m.onBeforeCompile = sh => { sh.uniforms.uL = RIMU; sh.uniforms.uRK = RIMK; sh.uniforms.uRim = { value: new T.Color(col || '#ffd08a').multiplyScalar(k) };
      sh.fragmentShader = 'uniform vec3 uL; uniform vec3 uRim; uniform float uRK;\n' + sh.fragmentShader.replace('#include <emissivemap_fragment>',
        '#include <emissivemap_fragment>\n{ float fr = 1.0 - abs(dot(normal, normalize(vViewPosition))); totalEmissiveRadiance += uRim * uRK * pow(fr, 1.3) * smoothstep(-0.35, 0.6, dot(normal, uL)); }'); };
      m.customProgramCacheKey = () => 'pbrim'; return m; }
    const dishM = rim(new T.MeshStandardMaterial({ color: '#d6d8df', roughness: .58, metalness: .08, envMap: E, envMapIntensity: .18, side: T.DoubleSide }), 3.2);
    const metM = rim(new T.MeshStandardMaterial({ color: '#a9afbd', roughness: .34, metalness: .85, envMap: E, envMapIntensity: .35 }), 2.6);
    const darkM = rim(new T.MeshStandardMaterial({ color: '#4a4e5c', roughness: .5, metalness: .6, envMap: E, envMapIntensity: .3 }), 1.0);
    const foilN = K.normalMap(K.noise(256, { seed: 21, octaves: 3 }), 6); foilN.repeat.set(3, 1);
    const foilM = rim(new T.MeshStandardMaterial({ color: '#c99a48', roughness: .28, metalness: 1, envMap: E, envMapIntensity: .55, normalMap: foilN }), 1.2);
    const louT = ctx.ctex(256, (g, s) => { g.fillStyle = '#4a4e5c'; g.fillRect(0, 0, s, s); g.fillStyle = '#2a2d36'; g.fillRect(14, 22, s - 28, s - 44);
      for (let k = 0; k < 8; k++) { const y = 30 + k * 25; g.fillStyle = '#9aa0b0'; g.fillRect(20, y, s - 40, 12); g.fillStyle = '#5c6070'; g.fillRect(20, y + 12, s - 40, 4); }
      g.fillStyle = '#6a6e7c'; g.fillRect(0, 0, s, 6); g.fillRect(0, s - 6, s, 6); });
    louT.anisotropy = 8; louT.repeat.set(10, 1); louT.wrapS = T.RepeatWrapping;
    const busM = rim(new T.MeshStandardMaterial({ map: louT, roughness: .42, metalness: .7, envMap: E, envMapIntensity: .35, flatShading: true }), 1.1);
    const add = (g, m, par) => { const o = new T.Mesh(g, m); (par || PROBE).add(o); return o; };
    function rod(a, b, r, m, par) { const d = b.clone().sub(a), o = add(new T.CylinderGeometry(r, r, d.length(), 8), m, par);
      o.position.copy(a).addScaledVector(d, .5); o.quaternion.setFromUnitVectors(v3(0, 1, 0), d.normalize()); return o; }
    const FL = 1.55, DR = 1.83, yP = r => r * r / (4 * FL);
    { const pr = []; for (let i = 0; i <= 20; i++) { const r = DR * i / 20; pr.push(new T.Vector2(r, yP(r) - .08 - .02 * (1 - i / 20))); }
      pr.push(new T.Vector2(DR + .04, yP(DR) - .04), new T.Vector2(DR + .04, yP(DR) + .02));
      for (let i = 20; i >= 0; i--) { const r = DR * i / 20; pr.push(new T.Vector2(Math.max(r, .0001), yP(r))); }
      add(new T.LatheGeometry(pr, 96), dishM); }
    for (let k = 0; k < 16; k++) { const a = k / 16 * 6.283, pts = [];
      for (let j = 0; j <= 10; j++) { const r = .3 + 1.45 * j / 10; pts.push(v3(r * Math.cos(a), yP(r) - .12, r * Math.sin(a))); }
      add(new T.TubeGeometry(new T.CatmullRomCurve3(pts), 10, .028, 6, false), metM); }
    add(new T.TorusGeometry(1.15, .03, 8, 64).rotateX(Math.PI / 2).translate(0, yP(1.15) - .12, 0), metM);
    add(new T.TorusGeometry(.42, .04, 8, 40).rotateX(Math.PI / 2).translate(0, yP(.42) - .12, 0), metM);
    for (let k = 0; k < 4; k++) { const a = k / 4 * 6.283 + .4; rod(v3(.95 * Math.cos(a), yP(.95), .95 * Math.sin(a)), v3(.13 * Math.cos(a), 1.02, .13 * Math.sin(a)), .022, metM); }
    { const sp = [[0, 1.08], [.14, 1.07], [.24, 1.03], [.25, 1.0], [.12, .98], [0, .97]].map(([r, h]) => new T.Vector2(r, h)); add(new T.LatheGeometry(sp, 32), metM); }
    add(new T.CylinderGeometry(.07, .14, .4, 20).translate(0, .2, 0), darkM);
    add(new T.CylinderGeometry(.38, .42, .3, 24).translate(0, -.22, 0), foilM);
    add(new T.CylinderGeometry(.92, .92, .47, 10).translate(0, -.6, 0), busM);
    add(new T.CylinderGeometry(.95, .95, .04, 10).translate(0, -.36, 0), darkM);
    add(new T.CylinderGeometry(.95, .95, .04, 10).translate(0, -.84, 0), darkM);
    add(new T.SphereGeometry(.4, 24, 12, 0, 6.283, Math.PI / 2, Math.PI / 2).translate(0, -.84, 0), foilM);
    for (let k = 0; k < 4; k++) { const a = k / 4 * 6.283 + .8; add(new T.CylinderGeometry(.03, .07, .16, 10).translate(.62 * Math.cos(a), -.94, .62 * Math.sin(a)), darkM); }
    const ra = v3(.88, -.6, 0), rb = v3(3.5, -1.05, .35), rdir = rb.clone().sub(ra).normalize();
    rod(ra.clone().add(v3(0, .08, 0)), rb.clone().add(v3(0, .08, 0)), .025, metM); rod(ra.clone().add(v3(0, -.08, 0)), rb.clone().add(v3(0, -.08, 0)), .025, metM);
    for (let k = 0; k < 6; k++) { const s0 = k / 6, s1 = (k + 1) / 6; rod(ra.clone().lerp(rb, s0).add(v3(0, .08, 0)), ra.clone().lerp(rb, s1).add(v3(0, -.08, 0)), .012, metM); }
    const rtgM = rim(new T.MeshStandardMaterial({ color: '#3a3c46', roughness: .5, metalness: .6, envMap: E, envMapIntensity: .3, emissive: '#ff7a3a', emissiveIntensity: .05 }), 1.0);
    const rtgs = [];
    for (let k = 0; k < 3; k++) { const G = new T.Group(); PROBE.add(G); G.position.copy(ra.clone().lerp(rb, .45 + k * .22)); G.quaternion.setFromUnitVectors(v3(0, 1, 0), rdir);
      add(new T.CylinderGeometry(.17, .17, .48, 20), rtgM, G); add(new T.CylinderGeometry(.19, .19, .04, 20).translate(0, .25, 0), metM, G); add(new T.CylinderGeometry(.19, .19, .04, 20).translate(0, -.25, 0), metM, G);
      for (let f = 0; f < 6; f++) { const a = f / 6 * 6.283; const fin = add(new T.BoxGeometry(.13, .44, .018), rtgM, G); fin.position.set(.23 * Math.cos(a), 0, .23 * Math.sin(a)); fin.rotation.y = -a; }
      rtgs.push(G); }
    const sa = v3(-.88, -.5, 0), sb = v3(-2.5, -.55, .3);
    rod(sa.clone().add(v3(0, .07, .05)), sb.clone().add(v3(0, .07, .05)), .03, metM); rod(sa.clone().add(v3(0, -.07, -.05)), sb.clone().add(v3(0, -.07, -.05)), .03, metM);
    const PLAT = new T.Group(); PROBE.add(PLAT); PLAT.position.copy(sb);
    const q0 = new T.Quaternion().setFromEuler(new T.Euler(.2, -.5, .1));
    add(new T.BoxGeometry(.5, .32, .42), darkM, PLAT).position.set(-.15, 0, 0);
    add(new T.BoxGeometry(.3, .22, .3), foilM, PLAT).position.set(-.15, .27, 0);
    const camA = add(new T.CylinderGeometry(.08, .09, .62, 18).rotateZ(Math.PI / 2), metM, PLAT); camA.position.set(.33, .06, .08);
    const camB = add(new T.CylinderGeometry(.07, .075, .34, 16).rotateZ(Math.PI / 2), metM, PLAT); camB.position.set(.2, -.1, -.12);
    add(new T.BoxGeometry(.22, .2, .24), metM, PLAT).position.set(-.15, -.06, .3);
    // lens faces (dark glass discs at the camera fronts) and small status lamps on the platform
    const glassM = new T.MeshStandardMaterial({ color: '#0a0c14', roughness: .08, metalness: .2, envMap: E, envMapIntensity: 1.2 });
    add(new T.CircleGeometry(.07, 24).rotateY(Math.PI / 2), glassM, PLAT).position.set(.645, .06, .08);
    add(new T.CircleGeometry(.06, 24).rotateY(Math.PI / 2), glassM, PLAT).position.set(.375, -.1, -.12);
    const lamps = [[-.15, .17, .215, '#7dffb0'], [-.02, .06, .215, '#ffc65a'], [-.28, .06, .215, '#7dffb0'], [-.15, .04, .425, '#ffc65a']].map(([x, y, z, c]) => {
      const m = new T.Mesh(new T.SphereGeometry(.018, 10, 8), new T.MeshBasicMaterial({ color: new T.Color(c).multiplyScalar(2.2), transparent: true })); m.position.set(x, y, z); PLAT.add(m);
      const g = ctx.glow(PLAT, c, .16, .5); g.position.set(x, y, z + .01); return { m, g }; });
    const ma = v3(-.6, -.75, -.55), md = v3(-.45, -.18, -.87).normalize(), mb = ma.clone().addScaledVector(md, 12.5);
    rod(ma, mb, .035, metM); add(new T.CylinderGeometry(.16, .16, .4, 16), darkM).position.copy(ma);
    for (let k = 1; k < 13; k++) { const ring = add(new T.TorusGeometry(.05, .015, 6, 12), metM); ring.position.copy(ma).addScaledVector(md, k); ring.quaternion.setFromUnitVectors(v3(0, 0, 1), md); }
    { const c = add(new T.CylinderGeometry(.09, .09, .3, 14), darkM); c.position.copy(mb); c.quaternion.setFromUnitVectors(v3(0, 1, 0), md); }
    PROBE.quaternion.setFromUnitVectors(v3(0, 1, 0), SD);
    PROBE.quaternion.premultiply(new T.Quaternion().setFromAxisAngle(SD, roll == null ? 2.3 : roll));
    PROBE.updateMatrixWorld(true);
    const rtgGlow = rtgs.map(G => { const s = ctx.glow(PROBE, '#ff9a55', .9, .12); s.position.copy(G.position); return s; });
    // the turned pose: the cameras' axis (platform +X) points at the Sun
    const sdL = SD.clone().applyQuaternion(PROBE.quaternion.clone().invert()).normalize();
    const qT = new T.Quaternion().setFromUnitVectors(v3(1, 0, 0), sdL);
    const qPark = new T.Quaternion().setFromEuler(new T.Euler(-.35, .2, -.45));
    const qq = new T.Quaternion();
    return { PROBE, PLAT, RIMU, RIMK, lamps, rtgGlow, camA, DR, yP,
      // w: 0 = stowed pose, 1 = cameras on the Sun; park: 0..1 toward the powered-down pose
      pose(w, park) { qq.copy(q0).slerp(qT, w); if (park) qq.slerp(qPark, park); PLAT.quaternion.copy(qq); },
      lensPos(out) { return out.set(.66, .06, .08).applyMatrix4(PLAT.matrixWorld); },
      platPos(out) { return out.set(0, 0, 0).applyMatrix4(PLAT.matrixWorld); } }; }

  // ======================================================================================================================
  // pbdot
  // ======================================================================================================================
  M.scenes.pbdot = function (ctx, p) {
    const { T, sm, rng, cue } = ctx, v3 = (x, y, z) => new T.Vector3(x, y, z);
    const S = new T.Scene(); S.background = new T.Color('#020309');
    const has = k => p[k] != null, cu = k => cue(p[k]);
    const VIEW = p.view || 'photo';
    const SRC = v3(-34, 260, -30);                         // where the scattered-light bands fan out from (the Sun, far above)
    const SDIR = SRC.clone().normalize();
    const SK = sky(ctx, S, { n: 1400, bright: .5, sun: SDIR, halo: .6 });
    // ---- bands: axial billboards from SRC through points near the y = 0 plane (Earth's band passes through the origin) ----
    const BANDS = [ // [x, z, width at y=0, colour, strength]
      [0, 0, 3.4, '#d38a4e', 1.0], [-5.5, -6, 2.6, '#c26a86', .55], [5.2, -3, 2.2, '#7d8fe0', .6], [-12, -22, 6, '#b07ad4', .45],
      [11, -18, 5, '#d9a35e', .5], [-2.4, -40, 9, '#c47a5a', .35], [20, -45, 8, '#6a7fd0', .35], [-24, -50, 9, '#d08a62', .3], [2.4, 4, 1.2, '#e0a070', .35]];
    const NB = BANDS.length, bg = new T.BufferGeometry(), SEG = 24;
    const bA = [], bB = [], bW = [], bC = [], bS = [], bCor = [], bix = [];
    BANDS.forEach((b, i) => { const Q = v3(b[0], 0, b[1]), d = Q.clone().sub(SRC).normalize(), A = Q.clone().addScaledVector(d, -150), B = Q.clone().addScaledVector(d, 70), c = new T.Color(b[3]);
      for (let s = 0; s <= SEG; s++) for (let k = 0; k < 2; k++) { bA.push(A.x, A.y, A.z); bB.push(B.x, B.y, B.z); bW.push(b[2], b[4], i); bC.push(c.r, c.g, c.b); bCor.push(s / SEG, k); }
      const o = i * (SEG + 1) * 2; for (let s = 0; s < SEG; s++) { const a = o + s * 2; bix.push(a, a + 1, a + 2, a + 1, a + 3, a + 2); } });
    const fa = (a, k, n) => bg.setAttribute(n, new T.Float32BufferAttribute(a, k));
    fa(bA, 3, 'aA'); fa(bB, 3, 'aB'); fa(bW, 3, 'aW'); fa(bC, 3, 'aC'); fa(bCor, 2, 'corner'); fa(new Array(bA.length).fill(0), 3, 'position'); bg.setIndex(bix);
    const bU = { uSrc: { value: SRC }, uK: { value: 1 }, uT: { value: 0 } };
    const bands = new T.Mesh(bg, new T.ShaderMaterial({ uniforms: bU, transparent: true, depthWrite: false, depthTest: false, blending: T.AdditiveBlending, side: T.DoubleSide,
      vertexShader: `attribute vec3 aA, aB, aW, aC; attribute vec2 corner; uniform vec3 uSrc; varying vec2 vUv; varying vec3 vC; varying float vS, vI, vD;
        void main(){ vec3 P = mix(aA, aB, corner.x), ax = normalize(aB - aA), V = cameraPosition - P; vec3 sd = cross(ax, V); float sl = length(sd); sd = sl > 1e-5 ? sd / sl : vec3(1., 0., 0.);
          float w = aW.x * length(P - uSrc) / length(mix(aA, aB, 150. / 220.) - uSrc);
          vec3 Q = P + sd * (corner.y - .5) * w * 2.4; vUv = corner; vC = aC; vS = aW.y; vI = aW.z; vD = length(cameraPosition - Q);
          gl_Position = projectionMatrix * viewMatrix * vec4(Q, 1.); }`,
      fragmentShader: `uniform float uK, uT; varying vec2 vUv; varying vec3 vC; varying float vS, vI, vD;
        float h1(float x){ return fract(sin(x * 91.7) * 43758.5); }
        float n1(float x){ float i = floor(x), f = fract(x); f = f * f * (3. - 2. * f); return mix(h1(i), h1(i + 1.), f); }
        void main(){ float u = (vUv.y - .5) * 2.4, prof = exp(-u * u * 3.2);
          float fine = .78 + .22 * n1(vUv.y * 46. + vI * 13.) + .12 * n1(vUv.y * 140. + vI * 5.);
          float along = smoothstep(0., .35, vUv.x) * (1. - smoothstep(.82, 1., vUv.x)) * (.85 + .15 * n1(vUv.x * 9. + vI * 3.));
          float nearF = smoothstep(1.2, 9., vD);
          vec3 c = vC * prof * fine * along * vS * uK * .15 * nearF;
          gl_FragColor = vec4(c, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` }));
    bands.frustumCulled = false; bands.renderOrder = -5; S.add(bands);
    // ---- dust motes in the beam: brighter inside a band, drifting slowly down the beam (wrapped with fades: seek-safe) ----
    const ND = 1400, dpos = new Float32Array(ND * 3), dcol = new Float32Array(ND * 3), dph = new Float32Array(ND), dB = [], r = rng(11);
    for (let i = 0; i < ND; i++) { const x = (r() - .5) * 70, y = (r() - .5) * 110, z = -55 + 70 * r(); let inb = 0;
      BANDS.forEach(b => { const Q = v3(b[0], 0, b[1]), d = Q.clone().sub(SRC).normalize(), P = v3(x, y, z).sub(Q); const perp = P.addScaledVector(d, -P.dot(d)).length(); inb = Math.max(inb, Math.exp(-perp * perp / (b[2] * b[2] * .6)) * b[4]); });
      const br = (.12 + .9 * inb) * (.4 + .6 * r()), warm = r() < .75; dB.push([x, y, z, .3 + .7 * r()]); dph[i] = r();
      dcol.set(warm ? [br, br * .8, br * .58] : [br * .7, br * .8, br], i * 3); }
    const dust = cpoints(ctx, S, dpos, dcol, { size: .07, max: 3.4, near: .8, phase: dph });
    // ---- Earth: small globe (seen only when close) + the pale-blue speck sprites ----
    const RE = .05, SUNW = SRC.clone().multiplyScalar(10);
    let G = null;
    if (VIEW === 'beam' || has('pull')) { G = globe(ctx, S, SUNW); G.EG.scale.setScalar(RE); }
    const spr = (col, op, tex) => { const s = new T.Sprite(new T.SpriteMaterial({ map: tex || ctx.dotTex(), color: col, transparent: true, opacity: op, blending: T.AdditiveBlending, depthWrite: false, depthTest: false })); s.renderOrder = 5; S.add(s); return s; };
    const core = spr(new T.Color(1.3, 1.75, 2.6), 1), halo = spr(new T.Color('#6f9cff'), .5), halo2 = spr(new T.Color('#9fc2ff'), .18);
    // city-light glints ("every king, every war, every love story"): inside the halo, each rises .2 s and fades 1.1 s
    const NGL = 46, gl = [], LIFE = has('life') ? cu('life') : null, LD = p.lifeDur || 3.2;
    { const rr = rng(29); for (let i = 0; i < NGL; i++) { const a = rr() * 6.283, rad = .05 + .32 * Math.sqrt(rr()), tp = rr(), s = spr(new T.Color(...(tp < .6 ? [1.7, .95, .35] : tp < .82 ? [1.7, .55, .35] : [1.5, .7, 1.0])), 0);
      s.visible = false; gl.push({ s, x: Math.cos(a) * rad, y: Math.sin(a) * rad, t: LIFE == null ? 1e9 : LIFE + .1 + (LD - .4) * Math.pow(rr(), .9), sz: .035 + .05 * rr() }); } }
    // pings
    const PINGS = cues(ctx, p.ping), pingS = PINGS.map(() => { const s = spr(new T.Color('#9fc2ff'), 0, ringTex(ctx)); s.visible = false; return s; });
    // pixel grid (plane facing the photo camera, through Earth)
    const PX = has('pixel') ? cu('pixel') : null, CELL = .7;
    let grid = null;
    if (PX != null) { grid = new T.Mesh(new T.PlaneGeometry(CELL * 13, CELL * 13), new T.ShaderMaterial({ uniforms: { uO: { value: 0 }, uC: { value: CELL }, uH: { value: 0 } }, transparent: true, depthWrite: false, depthTest: false, blending: T.AdditiveBlending,
      vertexShader: `varying vec2 vP; void main(){ vP = position.xy; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }`,
      fragmentShader: `uniform float uO, uC, uH; varying vec2 vP;
        void main(){ vec2 q = vP / uC + .5, f = fract(q), w = fwidth(q); vec2 l = smoothstep(w * 1.5, vec2(0.), f) + smoothstep(1. - w * 1.5, vec2(1.), f);
          float line = max(l.x, l.y), rad = length(vP) / (uC * 6.), fade = 1. - smoothstep(.25, 1., rad);
          bool own = abs(vP.x) < uC * .5 && abs(vP.y) < uC * .5;
          vec3 c = vec3(.55, .65, .95) * line * .22 * fade;
          if (own) c = c * .2 + vec3(1., .78, .42) * line * 1.1 * uH + vec3(.3, .45, .9) * .03 * uH;
          gl_FragColor = vec4(c * uO, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` })); grid.renderOrder = 4; grid.position.set(0, 0, 0); S.add(grid); }
    // streaks for the dive (motes rushing past)
    const DV = has('dive') ? cu('dive') : null, NST = 260, st = DV != null ? streaks(ctx, S, NST, { minPx: 1.4, near: [.6, 3] }) : null, stB = [];
    if (st) { const rs = rng(41); for (let i = 0; i < NST; i++) stB.push([(rs() - .5) * 2, (rs() - .5) * 2, rs(), .4 + .6 * rs()]); }
    const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .01, 4000); lift(ctx, cam, p.side == null ? .1 : p.side, p.lift == null ? .07 : p.lift, 40);
    if (!cam.parent) S.add(cam);
    const dimVeil = veil(ctx, S, cam, '#000000');
    const D0 = p.d0 || 40, D1 = p.d1 || 24, ORB = (p.orbit == null ? 6 : p.orbit) * Math.PI / 180, PULL = has('pull') ? cu('pull') : null;
    const BEAMDIR = v3(.92, .12, .38).normalize(), BD0 = p.bd0 || .32, BD1 = p.bd1 || 38;
    // camera as a pure function of t: returns [position, target]
    const tgt = v3(0, 0, 0), pos = v3(0, 0, 0);
    function camAt(t, P, Tg) { const u = (t - ctx.t0) / Math.max(1, ctx.t1 - ctx.t0);
      if (VIEW === 'beam') { const k = PULL == null ? sm(0, 1, u) : ease5((t - PULL) / 4.8), d = Math.exp(Math.log(BD0) + (Math.log(BD1) - Math.log(BD0)) * k) * (1 + .04 * u);
        const dir = BEAMDIR.clone().applyAxisAngle(v3(0, 1, 0), -ORB * (u - .5) - .5 * k).normalize();
        Tg.set(0, 0, 0).lerp(v3(-1.2, 1.8, -2), sm(.3, 1, k)); P.copy(Tg).addScaledVector(dir, d); return d; }
      let d = Math.exp(Math.log(D0) + (Math.log(D1) - Math.log(D0)) * sm(0, 1, u));
      if (DV != null) { const k = 1 - Math.pow(1 - Math.min(1, Math.max(0, (t - DV) / 3.4)), 2.6); d = Math.exp(Math.log(700) + (Math.log(d) - Math.log(700)) * k); }
      const a = ORB * (u - .5), dir = v3(Math.sin(a), .05 + .03 * Math.sin(u * 2), Math.cos(a)).normalize();
      Tg.set(0, 0, 0); P.copy(dir).multiplyScalar(d); return d; }
    const pB = v3(0, 0, 0), tB = v3(0, 0, 0), tmp = v3(0, 0, 0);
    return { scene: S, camera: cam, draw(t, u) {
      const d = camAt(t, pos, tgt); cam.position.copy(pos); cam.up.set(0, 1, 0); cam.lookAt(tgt);
      cam.near = Math.max(.004, Math.min(d * .02, .5)); cam.far = 4000; cam.updateProjectionMatrix(); cam.updateMatrixWorld();
      SK.update(cam);
      bU.uT.value = t;
      // the speck: constant small angular core + world-sized halo (grows as the camera nears); gentle breathing
      const dE = cam.position.length(), pxW = ctx.H / (2 * dE * Math.tan(cam.fov * Math.PI / 360));   // pixels per world unit at Earth
      const br = .86 + .14 * Math.sin(t * 2.4), gOn = G ? sm(9, 3, RE * 2 * pxW) : 1;      // globe takes over once it is ~6+ px wide
      core.scale.setScalar(Math.max(5.5 / pxW, RE * 2.4)); core.material.opacity = gOn;
      halo.scale.setScalar(Math.max(34 / pxW, .9) * (.94 + .1 * br)); halo.material.opacity = .42 * br * (.35 + .65 * gOn);
      halo2.scale.setScalar(Math.max(110 / pxW, 2.6)); halo2.material.opacity = .11 * br * (.4 + .6 * gOn);
      if (G) { G.EG.visible = gOn < .999; G.set(t, t * .05); }
      // glints
      gl.forEach(g => { const e = envl(t - g.t, .2, 1.1); g.s.visible = e > .004; if (!g.s.visible) return;
        tmp.set(g.x, g.y, 0).applyQuaternion(cam.quaternion); g.s.position.copy(tmp); g.s.scale.setScalar(Math.max(g.sz, 3 / pxW)); g.s.material.opacity = .9 * e; });
      PINGS.forEach((tp, i) => { const q = (t - tp) / 2.6, s = pingS[i]; s.visible = q > 0 && q < 1; if (!s.visible) return; s.scale.setScalar((.2 + 2.2 * Math.pow(q, .7)) * Math.max(1, 30 / pxW / .9)); s.material.opacity = sm(0, .12, q) * (1 - q) * (1 - q) * .8; });
      if (grid) { const o = sm(PX, PX + .8, t); grid.visible = o > 0; grid.material.uniforms.uO.value = o; grid.material.uniforms.uH.value = sm(PX + .5, PX + 1.4, t) * (.85 + .15 * Math.sin(t * 2.4)); grid.quaternion.copy(cam.quaternion); }
      // dust drift down the beam (wrap with fades)
      const a = dust.P.geometry.attributes.position.array, c = dust.P.geometry.attributes.color;
      for (let i = 0; i < ND; i++) { const b = dB[i], s0 = (b[3] * .05 * t + dph[i]) % 1, s = s0 < 0 ? s0 + 1 : s0, off = (s - .5) * 14;
        a[i * 3] = b[0] - SDIR.x * off; a[i * 3 + 1] = b[1] - SDIR.y * off; a[i * 3 + 2] = b[2] - SDIR.z * off; }
      dust.P.geometry.attributes.position.needsUpdate = true; dust.U.uT.value = t;
      // dive streaks: points on a tube around the camera path, tails = camera motion over the last .06 s
      if (st) { const e = sm(DV - .1, DV + .3, t) * (1 - sm(DV + 2.2, DV + 3.4, t)); st.mesh.visible = e > 0;
        if (e > 0) { camAt(t - .06, pB, tB); const dv = pos.clone().sub(pB), L = dv.length(), fw = tgt.clone().sub(pos).normalize(), rt = v3(0, 0, 0).crossVectors(fw, v3(0, 1, 0)).normalize(), up = v3(0, 0, 0).crossVectors(rt, fw);
          for (let i = 0; i < NST; i++) { const b = stB[i], ahead = d * (.15 + 1.6 * ((b[2] + t * .9) % 1)), rad = d * .35 * (.4 + Math.hypot(b[0], b[1]));
            const ang = Math.atan2(b[1], b[0]), P = pos.clone().addScaledVector(fw, ahead).addScaledVector(rt, Math.cos(ang) * rad).addScaledVector(up, Math.sin(ang) * rad);
            const k = e * b[3] * .6; st.set(i, P.x, P.y, P.z, P.x + dv.x * 1.4, P.y + dv.y * 1.4, P.z + dv.z * 1.4, d * .002, k, k * .82, k * .62); }
          st.commit(); } }
      const dm = has('dim') ? sm(cu('dim'), cu('dim') + 2.5, t) * .85 : 0; dimVeil.set(dm);
    } };
  };

  // ======================================================================================================================
  // pbprobe
  // ======================================================================================================================
  M.scenes.pbprobe = function (ctx, p) {
    const { T, sm, rng, cue } = ctx, v3 = (x, y, z) => new T.Vector3(x, y, z);
    const S = new T.Scene(); S.background = new T.Color('#02030a');
    const has = k => p[k] != null, cu = k => cue(p[k]), VIEW = p.view || 'hero';
    const SD = v3(-.62, .5, -.6).normalize(), SUN = SD.clone().multiplyScalar(1600);
    const SK = sky(ctx, S, { n: 2400, sun: SD, halo: VIEW === 'deep' || VIEW === 'shell' ? .15 : 1 });
    const PR = probe(ctx, S, SD, p.roll);
    const sunL = new T.DirectionalLight('#fff0d8', 3.2); sunL.position.copy(SD).multiplyScalar(50); S.add(sunL);
    const fillL = new T.DirectionalLight('#9aa6c0', .7); S.add(fillL);
    S.add(new T.HemisphereLight('#3a4270', '#07080f', .45));
    const spr = (col, op, tex, order) => { const s = new T.Sprite(new T.SpriteMaterial({ map: tex || ctx.dotTex(), color: col, transparent: true, opacity: op, blending: T.AdditiveBlending, depthWrite: false, fog: false })); s.renderOrder = order || 0; S.add(s); return s; };
    const sunCore = spr(new T.Color(4, 3.7, 3.2), 1), sunHalo = spr(new T.Color('#ffc874'), .5), sunWide = spr(new T.Color('#ff9c50'), .18);
    [sunCore, sunHalo, sunWide].forEach(s => s.position.copy(SUN));
    const dust = M.kit.snow(S, { n: 500, box: [40, 26, 40], size: .07, opacity: .4, color: '#ffdcae', fall: .02, seed: 9 });
    // lens ghosts on the line from the Sun through the frame centre (placed by project / unproject each frame)
    const GH = [[.3, .05, '#6f8cff'], [.55, .11, '#c79aff'], [.75, .03, '#ffb070'], [1.05, .16, '#7fd0c0'], [1.3, .07, '#ff9a60']].map(([k, sz, c]) => [spr(new T.Color(c), 0, null, 60), k, sz]);
    GH.forEach(([g]) => { g.material.depthTest = false; });
    const lensG = spr(new T.Color(2.4, 2.1, 1.7), 0, null, 6);
    const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .05, 1e5);
    lift(ctx, cam, p.side == null ? .12 : p.side, p.lift == null ? .06 : p.lift, 40); S.add(cam);
    const dark = veil(ctx, S, cam, '#000000'), warm = veil(ctx, S, cam, '#ff9a4a', true);
    // ---- data pulses (view data): faint packets leaving the dish toward the Sun, recycling ----
    const NDP = 34, dps = VIEW === 'data' ? streaks(ctx, S, NDP, { minPx: 1.6, near: [1, 4] }) : null, dpB = [];
    if (dps) { const r = rng(7); for (let i = 0; i < NDP; i++) dpB.push([r(), (r() - .5) * .5, (r() - .5) * .5, .6 + .4 * r()]); }
    // ---- heliosphere bubble (deep) / light-day shell (shell) ----
    let bubble = null, shellM = null, trail = null, rip = null, pglint = null;
    const fres = (col, k) => new T.ShaderMaterial({ uniforms: { uC: { value: new T.Color(col) }, uK: { value: k }, uO: { value: 1 } }, transparent: true, depthWrite: false, blending: T.AdditiveBlending, side: T.DoubleSide,
      vertexShader: `varying vec3 vN, vW; void main(){ vN = normalize(mat3(modelMatrix) * normal); vec4 w = modelMatrix * vec4(position, 1.); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
      fragmentShader: `uniform vec3 uC; uniform float uK, uO; varying vec3 vN, vW;
        float h3(vec3 p){ p = fract(p * .3183099 + .1); p *= 17.; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
        float n3(vec3 x){ vec3 i = floor(x), f = fract(x); f = f * f * (3. - 2. * f);
          return mix(mix(mix(h3(i), h3(i + vec3(1,0,0)), f.x), mix(h3(i + vec3(0,1,0)), h3(i + vec3(1,1,0)), f.x), f.y), mix(mix(h3(i + vec3(0,0,1)), h3(i + vec3(1,0,1)), f.x), mix(h3(i + vec3(0,1,1)), h3(i + vec3(1,1,1)), f.x), f.y), f.z); }
        void main(){ vec3 V = normalize(cameraPosition - vW); float fr = 1. - abs(dot(normalize(vN), V)), n = .6 + .4 * n3(normalize(vW) * 5.) * n3(normalize(vW) * 11. + 3.);
          gl_FragColor = vec4(uC * (pow(fr, 5.) * 1.1 + .012) * n * uK * uO, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` });
    const RB = 1580;   // heliosphere radius around the Sun: the probe (origin) sits just outside it
    if (VIEW === 'deep') { bubble = new T.Mesh(new T.SphereGeometry(RB, 96, 48), fres('#6c5ae0', .3)); bubble.position.copy(SUN); S.add(bubble); }
    const RS = 100, SC = v3(0, 0, 0), PD = v3(.78, .3, -.55).normalize(), REACH = has('reach') ? cu('reach') : ctx.t1;
    if (VIEW === 'shell') { shellM = new T.Mesh(new T.SphereGeometry(RS, 128, 64), fres('#ffc65a', .5)); S.add(shellM);
      trail = streaks(ctx, S, 60, { minPx: 1.8, near: [1, 5] });
      rip = [0, 1, 2].map(() => { const m = new T.Mesh(new T.RingGeometry(.86, 1, 96), new T.MeshBasicMaterial({ color: new T.Color(1.6, 1.2, .6), transparent: true, opacity: 0, blending: T.AdditiveBlending, depthWrite: false, side: T.DoubleSide }));
        m.position.copy(PD).multiplyScalar(RS); m.lookAt(PD.clone().multiplyScalar(RS * 2)); S.add(m); return m; });
      pglint = spr(new T.Color(2.4, 2.1, 1.6), 1, null, 8); }
    const earthDot = VIEW === 'shell' ? spr(new T.Color(1, 1.5, 2.6), 1, null, 7) : null;
    // ---- camera stories (pure functions of t) ----
    const TURN = has('turn') ? cu('turn') : null, GLARE = has('glare') ? cu('glare') : null, OFF = has('off') ? cu('off') : null;
    const lp = v3(0, 0, 0), pp = v3(0, 0, 0), tmp = v3(0, 0, 0), tq = v3(0, 0, 0);
    const AW = has('away') ? cu('away') : ctx.t0;
    const ORB = v3(0, 1, 0);
    function story(t) { const u = (t - ctx.t0), U = u / Math.max(1, ctx.t1 - ctx.t0); let pos, tg, fov = 40;
      const turnW = TURN == null ? (VIEW === 'glare' || VIEW === 'off' ? 1 : 0) : sm(TURN, TURN + 3.6, t);
      const park = OFF == null ? 0 : sm(OFF + .3, OFF + 3.5, t);
      PR.pose(turnW, park); PR.PROBE.updateMatrixWorld(true); PR.platPos(pp);
      const base = v3(6.4, -1.6, 8.6).normalize();
      if (VIEW === 'hero') { const dir = base.clone().applyAxisAngle(ORB, -.25 + .5 * U); tg = v3(0, -.7, 0); pos = tg.clone().addScaledVector(dir, 14 - 2.5 * sm(0, 1, U)); }
      else if (VIEW === 'turn') { const k = sm(0, 1, U); const dir = base.clone().applyAxisAngle(ORB, -1.2 + 1.1 * k).lerp(SD.clone().negate(), .25 * k).normalize();
        tg = v3(-1.2, -.6, 0).lerp(pp, .35 + .3 * k); pos = tg.clone().addScaledVector(dir, 9 - 3 * k); }
      else if (VIEW === 'glare') { const k = sm(0, 1, U); tg = pp.clone().addScaledVector(SD, 30); const sdv = v3(0, 0, 0).crossVectors(SD, v3(0, 1, 0)).normalize();
        pos = pp.clone().addScaledVector(SD, -7.5 + 1.6 * k).addScaledVector(sdv, 2.2 - .6 * k).add(v3(0, -1.1, 0)); fov = 44 - 6 * k; }
      else if (VIEW === 'off') { const k = sm(0, 1, U), dir = base.clone().applyAxisAngle(ORB, -1.9 + .3 * k).addScaledVector(v3(0, 1, 0), .2).normalize();
        tg = pp.clone().lerp(v3(0, -.6, 0), .3); pos = tg.clone().addScaledVector(dir, 6.5 - 1.2 * k); }
      else if (VIEW === 'away') { const k = Math.max(0, t - AW) / Math.max(1, ctx.t1 - AW), dir = SD.clone().lerp(base, .55).normalize(); const PO = SD.clone().multiplyScalar(-1).multiplyScalar(Math.exp(Math.log(1) + Math.log(60) * ease5(k * .95)) - 1);
        PR.PROBE.position.copy(PO); PR.PROBE.updateMatrixWorld(true); tg = PO.clone().add(v3(0, -.7, 0)); pos = dir.clone().multiplyScalar(13); }
      else if (VIEW === 'data') { const dir = SD.clone().negate().lerp(base, .35).normalize().applyAxisAngle(ORB, .12 * U - .06); tg = SD.clone().multiplyScalar(5); pos = dir.clone().multiplyScalar(17 - 2.5 * U).add(v3(0, 2.2, 0)); }
      else if (VIEW === 'deep') { const dir = SD.clone().negate().lerp(base, .6).normalize().applyAxisAngle(ORB, -.3 + .35 * U); tg = v3(0, -.5, 0); pos = dir.clone().multiplyScalar(15 - 3 * U); fov = 44; }
      else { // shell: wide over the light-day sphere, drifting toward the contact point
        const k = sm(0, 1, U), dir = PD.clone().multiplyScalar(-.2).add(v3(.2, .35, 1)).normalize().applyAxisAngle(ORB, .35 - .3 * k);
        tg = SC.clone().lerp(PD.clone().multiplyScalar(RS), .4 + .35 * k); pos = tg.clone().addScaledVector(dir, 420 - 110 * k); fov = 40; }
      return { pos, tg, fov, turnW, park }; }
    return { scene: S, camera: cam, draw(t, u) {
      const s = story(t); cam.position.copy(s.pos); cam.up.set(0, 1, 0); cam.lookAt(s.tg);
      const D = cam.position.distanceTo(s.tg); lift(ctx, cam, p.side == null ? .12 : p.side, p.lift == null ? .06 : p.lift, s.fov);
      cam.near = Math.max(.03, D * .004); cam.far = 2e5; cam.updateProjectionMatrix(); cam.updateMatrixWorld();
      SK.update(cam);
      PR.RIMU.value.copy(SD).transformDirection(cam.matrixWorldInverse);
      fillL.position.copy(cam.position).add(v3(0, 6, 0)).normalize().multiplyScalar(30);
      PR.rtgGlow.forEach((g, i) => g.material.opacity = .12 + .03 * Math.sin(t * .7 + i));
      // lamps: on until `off`, then they fade (rise/fall soft, no blink)
      const lampK = OFF == null ? 1 : 1 - sm(OFF, OFF + 1.4, t);
      PR.lamps.forEach((l, i) => { const k = lampK * (.8 + .2 * Math.sin(t * 1.3 + i * 1.7)); l.m.material.opacity = k; l.g.material.opacity = .55 * k; l.m.visible = l.g.visible = k > .01; });
      // Sun: small and very bright; in glare view it swells on cue
      const gk = GLARE == null ? 0 : sm(GLARE - .2, GLARE + 2.6, t), sd = cam.position.distanceTo(SUN), far = VIEW === 'deep' || VIEW === 'shell' ? 1 : 0;
      sunCore.scale.setScalar(sd * .012 * (1 + 3.2 * gk) * (1 - .6 * far)); sunHalo.scale.setScalar(sd * .1 * (1 + 3.6 * gk) * (1 - .75 * far)); sunWide.scale.setScalar(sd * .34 * (1 + 2 * gk) * (1 - .8 * far));
      sunHalo.material.opacity = .5 + .3 * gk; sunWide.material.opacity = (.16 + .2 * gk) * (1 - .7 * far);
      sunL.intensity = 3.2 * (1 + .6 * gk) * (1 - .55 * (OFF == null ? 0 : sm(OFF + .6, OFF + 3, t)));
      // lens glint on the camera front once it faces the Sun
      PR.lensPos(lp); lensG.position.copy(lp); const lg = s.turnW * (1 - s.park) * (VIEW === 'turn' || VIEW === 'glare' ? 1 : 0); lensG.material.opacity = .9 * lg * (1 + .6 * gk); lensG.scale.setScalar(.25 + .5 * gk);
      lensG.visible = lg > .01;
      // lens ghosts
      tq.copy(SUN).project(cam); const onS = tq.z < 1 && Math.abs(tq.x) < 1.3 && Math.abs(tq.y) < 1.3 ? 1 : 0, fl = onS * ((VIEW === 'glare' ? .35 : VIEW === 'turn' ? .2 * s.turnW : VIEW === 'hero' ? .15 : 0) + .9 * gk);
      GH.forEach(([g, k, sz]) => { g.visible = fl > .01; if (!g.visible) return; g.position.set(tq.x * (1 - 2 * k), tq.y * (1 - 2 * k), .5).unproject(cam); const dd = g.position.distanceTo(cam.position); g.scale.setScalar(sz * dd * (1 + .5 * gk)); g.material.opacity = fl * .28; });
      warm.set(VIEW === 'glare' ? .2 * gk : 0);
      // darkness after the cameras switch off / for the journey away
      const dk = VIEW === 'off' && OFF != null ? .7 * sm(OFF + .4, OFF + 2.2, t) : VIEW === 'away' ? .3 : 0; dark.set(dk);
      dust.points.visible = D < 60; if (dust.points.visible) dust.update(t, [0, 0, 0]);
      // data pulses
      if (dps) { PR.PROBE.updateMatrixWorld(true); const o = v3(0, 1.1, 0).applyMatrix4(PR.PROBE.matrixWorld);
        for (let i = 0; i < NDP; i++) { const b = dpB[i], q0 = (t * .07 * b[3] + b[0]) % 1, q = q0 < 0 ? q0 + 1 : q0, x = Math.pow(q, 1.7) * 160;
          const hx = o.x + SD.x * x + b[1] * (5 + x * .05), hy = o.y + SD.y * x + b[2] * (5 + x * .05), hz = o.z + SD.z * x, L = 1.6 + x * .03, k = .55 * sm(0, .06, q) * (1 - sm(.55, 1, q)) * b[3];
          dps.set(i, hx + SD.x * L, hy + SD.y * L, hz + SD.z * L, hx, hy, hz, .16, k * 1.1, k * 1.25, k * 1.5); }
        dps.commit(); }
      if (bubble) bubble.material.uniforms.uO.value = .9;
      if (shellM) { const k = sm(REACH - 8, REACH, t), fP = .62 + .38 * Math.pow(k, .9), P = PD.clone().multiplyScalar(RS * fP);
        PR.PROBE.visible = false; pglint.position.copy(P); const dd = cam.position.distanceTo(P), hit = envl(t - REACH, .3, 1.6); pglint.scale.setScalar(dd * (.016 + .03 * hit)); pglint.material.opacity = 1;
        earthDot.position.copy(SC); earthDot.scale.setScalar(cam.position.distanceTo(SC) * .02);
        sunCore.visible = sunHalo.visible = sunWide.visible = false;
        shellM.material.uniforms.uO.value = .7 + .8 * hit;
        for (let i = 0; i < 60; i++) { const f0 = i / 60 * fP, f1 = (i + .45) / 60 * fP, kk = .25 * (.4 + .6 * i / 60);
          trail.set(i, PD.x * RS * f1, PD.y * RS * f1, PD.z * RS * f1, PD.x * RS * f0, PD.y * RS * f0, PD.z * RS * f0, .35, kk, kk * .78, kk * .45); }
        trail.commit();
        rip.forEach((m, i) => { const q = (t - REACH - i * .5) / 3; m.visible = q > 0 && q < 1; if (!m.visible) return; m.scale.setScalar(2 + 34 * Math.pow(q, .6)); m.material.opacity = sm(0, .08, q) * (1 - q) * (1 - q) * .9; }); }
    } };
  };

  // ======================================================================================================================
  // pbportrait
  // ======================================================================================================================
  M.scenes.pbportrait = function (ctx, p) {
    const { T, sm, rng, cue } = ctx, v3 = (x, y, z) => new T.Vector3(x, y, z);
    const S = new T.Scene(); S.background = new T.Color('#02030a');
    const has = k => p[k] != null, cu = k => cue(p[k]);
    const SK = sky(ctx, S, { n: 1800, bright: .6, halo: 0 });
    const NC = 6, NR = 10, SZ = 1, GAP = .16, PIT = SZ + GAP, RC = 16;            // panels on a cylinder of radius RC (concave toward the camera)
    const SNAP = has('snap') ? cu('snap') : ctx.t0 + .4, DUR = p.dur || 5.6;
    const EI = 6 * NC + 1;                                                         // the Earth frame: row 6, column 1
    const order = []; for (let r = 0; r < NR; r++) for (let c = 0; c < NC; c++) order.push(r * NC + c);
    const g = new T.BoxGeometry(SZ, SZ, .05);
    const kind = new Float32Array(NC * NR), snap = new Float32Array(NC * NR), seed = new Float32Array(NC * NR), r = rng(5);
    const centre = []; for (let i = 0; i < NC * NR; i++) { const row = Math.floor(i / NC), col = i % NC;
      kind[i] = i === EI ? 4 : (row === 4 || row === 5) && (col === 2 || col === 3) ? 2 : [9, 15, 26, 46, 52].includes(i) ? 3 : r() < .45 ? 1 : 0;
      snap[i] = SNAP + DUR * order.indexOf(i) / (NC * NR) + .03 * (r() - .5); seed[i] = r() * 100;
      const x = (col - (NC - 1) / 2) * PIT, y = ((NR - 1) / 2 - row) * PIT, a = x / RC; centre.push([Math.sin(a) * RC, y, RC - Math.cos(a) * RC, a]); }
    g.setAttribute('aKind', new T.InstancedBufferAttribute(kind, 1)); g.setAttribute('aSnap', new T.InstancedBufferAttribute(snap, 1)); g.setAttribute('aSeed', new T.InstancedBufferAttribute(seed, 1));
    const U = { uT: { value: 0 } };
    const mat = new T.ShaderMaterial({ uniforms: U,
      vertexShader: `attribute float aKind, aSnap, aSeed; uniform float uT; varying vec2 vUv; varying float vK, vF, vOn, vSeed, vFace; varying vec3 vN, vW;
        void main(){ vUv = uv; vK = aKind; vSeed = aSeed; float dt = uT - aSnap; vOn = smoothstep(0., .12, dt);
          vF = dt <= 0. ? 0. : (dt < .15 ? smoothstep(0., .15, dt) : exp(-(dt - .15) / 1.)); vFace = step(.5, normal.z);
          vec4 w = modelMatrix * instanceMatrix * vec4(position, 1.); vW = w.xyz; vN = normalize(mat3(modelMatrix * instanceMatrix) * normal); gl_Position = projectionMatrix * viewMatrix * w; }`,
      fragmentShader: `varying vec2 vUv; varying float vK, vF, vOn, vSeed, vFace; varying vec3 vN, vW;
        float h2(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
        float n2(vec2 p){ vec2 i = floor(p), f = fract(p); f = f * f * (3. - 2. * f); return mix(mix(h2(i), h2(i + vec2(1, 0)), f.x), mix(h2(i + vec2(0, 1)), h2(i + vec2(1, 1)), f.x), f.y); }
        void main(){ vec2 q = vUv - .5; float e = max(abs(q.x), abs(q.y));
          vec3 edge = vec3(.35, .42, .7) * smoothstep(.44, .5, e) * (.25 + .5 * vOn) + vec3(1., .82, .5) * smoothstep(.43, .5, e) * vF * 1.6;
          if (vFace < .5) { gl_FragColor = vec4(vec3(.02, .025, .05) + edge * .3, 1.);
            #include <tonemapping_fragment>
            #include <colorspace_fragment>
            return; }
          float grain = n2(vUv * 70. + vSeed) * .5 + n2(vUv * 150. + vSeed * 2.) * .5;
          vec3 c = vec3(.012, .014, .03) + vec3(.03, .03, .05) * grain * .5;
          if (vK > .5 && vK < 1.5 || vK > 3.5) { float x = q.x - q.y * .18 + (fract(vSeed) - .5) * .5 * step(vK, 3.5); float b = exp(-x * x / .02) * (.8 + .2 * n2(vec2(x * 30., vSeed)));
            c += mix(vec3(.55, .32, .18), vec3(.45, .3, .55), fract(vSeed * 3.) * step(vK, 3.5)) * b * .32; }
          if (vK > 1.5 && vK < 2.5) { float r = length(q - vec2((fract(vSeed) - .5) * .6, 0.)); c += vec3(1., .78, .5) * (exp(-r * r / .02) * 1.4 + exp(-r * r / .2) * .25); }
          if (vK > 2.5 && vK < 3.5) { vec2 o = vec2(fract(vSeed * 1.7) - .5, fract(vSeed * 2.3) - .5) * .6; float r = length(q - o); c += vec3(1., .9, .75) * exp(-r * r / .0004) * 1.2 + vec3(.6, .5, .4) * exp(-r * r / .004) * .2; }
          if (vK > 3.5) { float r = length(q - vec2(.0, .03)); c += vec3(.5, .75, 1.3) * exp(-r * r / .00012) * 1.5 + vec3(.3, .5, 1.) * exp(-r * r / .002) * .25; }
          vec3 col = c * vOn + vec3(1., .9, .75) * vF * .55 * (1. - e) + edge;
          vec3 V = normalize(cameraPosition - vW); float fr = pow(1. - abs(dot(normalize(vN), V)), 4.);
          col += vec3(.2, .25, .45) * fr * .3;
          gl_FragColor = vec4(col, 1.);
          #include <tonemapping_fragment>
          #include <colorspace_fragment>
        }` });
    const IM = new T.InstancedMesh(g, mat, NC * NR); const o3 = new T.Object3D();
    centre.forEach(([x, y, z, a], i) => { o3.position.set(x, y, z); o3.rotation.set(0, -a, 0); o3.updateMatrix(); IM.setMatrixAt(i, o3.matrix); });
    IM.frustumCulled = false; S.add(IM);
    const glowB = ctx.glow(S, '#3a4a9a', 26, .08); glowB.position.set(0, 0, -6);
    const dust = M.kit.snow(S, { n: 400, box: [16, 20, 16], size: .03, opacity: .35, color: '#ffdcae', fall: .01, seed: 4 });
    const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .01, 3000); lift(ctx, cam, 0, p.lift == null ? .04 : p.lift, 40);
    const DIVE = has('dive') ? cu('dive') : null, EP = v3(centre[EI][0], centre[EI][1], centre[EI][2]), EN = v3(-Math.sin(centre[EI][3]), 0, Math.cos(centre[EI][3]));
    const firstP = v3(centre[0][0] + .6 * PIT, centre[0][1] - .4 * PIT, centre[0][2]);
    // the whole wall fits the frame (vertical: the 6 x 10 grid fills the 9:16 frame) at distance DW
    const DW = ctx.VERT ? 16.5 : 13;
    const tgt = v3(0, 0, 0), pos = v3(0, 0, 0);
    function camAt(t) { const k = sm(ctx.t0, SNAP + DUR * .75, t), ld = Math.log(4) + (Math.log(DW) - Math.log(4)) * k;
      tgt.copy(firstP).lerp(v3(0, 0, 0), sm(0, 1, k)); const dir = v3(-.25 * (1 - k) + .08 * Math.sin(t * .2), .12 * (1 - k), 1).normalize(); let d = Math.exp(ld);
      if (DIVE != null) { const w = ease5((t - DIVE) / 2.0); tgt.lerp(EP, w); dir.lerp(EN, w).normalize(); d = Math.exp(Math.log(d) + (Math.log(.62) - Math.log(d)) * w); }
      pos.copy(tgt).addScaledVector(dir, d); return d; }
    return { scene: S, camera: cam, draw(t, u) {
      const d = camAt(t); cam.position.copy(pos); cam.up.set(0, 1, 0); cam.lookAt(tgt); cam.near = Math.max(.01, d * .02); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
      SK.update(cam); U.uT.value = t; dust.update(t, [0, 0, 0]);
    } };
  };

  // ======================================================================================================================
  // pbearth
  // ======================================================================================================================
  M.scenes.pbearth = function (ctx, p) {
    const { T, sm, rng, cue } = ctx, v3 = (x, y, z) => new T.Vector3(x, y, z);
    const S = new T.Scene(); S.background = new T.Color('#03040d');
    const has = k => p[k] != null, cu = k => cue(p[k]), VIEW = p.view || 'home';
    const SUND = v3(-.88, .14, -.45).normalize(), SUN = SUND.clone().multiplyScalar(400);
    const SK = sky(ctx, S, { n: 2400, sun: SUND, halo: .8 });
    const G = globe(ctx, S, SUN);
    const spr = (col, op, tex, order) => { const s = new T.Sprite(new T.SpriteMaterial({ map: tex || ctx.dotTex(), color: col, transparent: true, opacity: op, blending: T.AdditiveBlending, depthWrite: false })); s.renderOrder = order || 0; S.add(s); return s; };
    const sun1 = spr(new T.Color(4, 3.7, 3.2), 1), sun2 = spr(new T.Color('#ffc874'), .45), sun3 = spr(new T.Color('#ff9c50'), .12);
    [sun1, sun2, sun3].forEach((s, i) => { s.position.copy(SUN); s.scale.setScalar([6, 40, 160][i]); });
    // pulse shells (radio): fresnel spheres scaling out from Earth
    const PU = cues(ctx, p.pulse), shells = [];
    const shellMat = () => new T.ShaderMaterial({ uniforms: { uO: { value: 0 }, uC: { value: new T.Color('#ffc65a') } }, transparent: true, depthWrite: false, blending: T.AdditiveBlending, side: T.FrontSide,
      vertexShader: `varying vec3 vN, vW; void main(){ vN = normalize(mat3(modelMatrix) * normal); vec4 w = modelMatrix * vec4(position, 1.); vW = w.xyz; gl_Position = projectionMatrix * viewMatrix * w; }`,
      fragmentShader: `uniform float uO; uniform vec3 uC; varying vec3 vN, vW; void main(){ vec3 V = normalize(cameraPosition - vW); float fr = 1. - abs(dot(normalize(vN), V));
        gl_FragColor = vec4(uC * (pow(fr, 6.) * 1.4 + .006) * uO, 1.);
        #include <tonemapping_fragment>
        #include <colorspace_fragment>
      }` });
    const SLOW = VIEW === 'clock';
    PU.forEach(tp => [0, 1, 2].forEach(k => { const m = new T.Mesh(new T.SphereGeometry(1, 64, 32), shellMat()); m.visible = false; S.add(m); shells.push({ m, t: tp + k * (SLOW ? .9 : .45) }); }));
    // day clock: a thin ring in the equatorial plane, a bright marker sweeping once
    let ring = null, mark = null;
    const DAY = has('day') ? cu('day') : ctx.t0 + .3, DAYE = ctx.t1 - .2;
    if (VIEW === 'clock') { const rg = new T.Mesh(new T.TorusGeometry(1.55, .005, 6, 256), new T.MeshBasicMaterial({ color: new T.Color(.5, .45, .35), transparent: true, opacity: .55, blending: T.AdditiveBlending, depthWrite: false }));
      rg.rotation.x = Math.PI / 2; G.EG.add(rg); ring = rg;
      mark = ctx.glow(G.EG, '#ffd58a', .16, 1); }
    const dust = M.kit.snow(S, { n: 300, box: [14, 10, 14], size: .025, opacity: .3, color: '#cfe0ff', fall: .01, seed: 13 });
    const cam = new T.PerspectiveCamera(35, ctx.W / ctx.H, .02, 1e5); lift(ctx, cam, p.side == null ? .1 : p.side, p.lift == null ? .07 : p.lift, 35);
    const PULL = has('pull') ? cu('pull') : ctx.t0 + .5;
    const tgt = v3(0, 0, 0), pos = v3(0, 0, 0);
    function camAt(t) { const U = (t - ctx.t0) / Math.max(1, ctx.t1 - ctx.t0); let dir, d;
      if (VIEW === 'pulse') { dir = v3(-.25, .22, 1).normalize().applyAxisAngle(v3(0, 1, 0), .25 * U); d = 3.3 + (PU.length ? 5.5 * ease5((t - PU[0] + .3) / 3.2) : 2 * U); }
      else if (VIEW === 'clock') { dir = v3(-.2, .32, 1).normalize().applyAxisAngle(v3(0, 1, 0), -.12 * U); d = 5.4 - .5 * U; }
      else if (VIEW === 'fragile') { dir = v3(-.55, .1, 1).normalize().applyAxisAngle(v3(0, 1, 0), .2 * U); d = Math.exp(Math.log(2.5) + (Math.log(14) - Math.log(2.5)) * ease5((t - PULL) / 4.2)); }
      else { dir = v3(-.5, .18, 1).normalize().applyAxisAngle(v3(0, 1, 0), .35 * U - .1); d = 2.75 - .3 * U; }
      tgt.set(0, 0, 0); pos.copy(dir).multiplyScalar(d); return d; }
    const v = v3(0, 0, 0);
    return { scene: S, camera: cam, draw(t, u) {
      const d = camAt(t); cam.position.copy(pos); cam.up.set(0, 1, 0); cam.lookAt(tgt); cam.near = Math.max(.02, (d - 1.2) * .3); cam.far = 1e5; cam.updateProjectionMatrix(); cam.updateMatrixWorld();
      SK.update(cam);
      const rot = VIEW === 'clock' ? 1.2 + 6.2832 * sm(DAY, DAYE, t) : .6 + t * .02;
      G.set(t, rot);
      if (ring) { const a = rot - 1.2; mark.position.set(Math.cos(a + 1.9) * 1.55, 0, -Math.sin(a + 1.9) * 1.55); mark.material.opacity = .9; }
      G.eU.city.value = VIEW === 'home' ? 1.35 : 1.15;
      shells.forEach(s => { const q = (t - s.t) / (SLOW ? 4.5 : 3.2); s.m.visible = q > 0 && q < 1; if (!s.m.visible) return; s.m.scale.setScalar(1.05 + (SLOW ? 2.6 : 5) * Math.pow(q, .8)); s.m.material.uniforms.uO.value = sm(0, .08, q) * (1 - q) * .6; });
      dust.update(t, [0, 0, 0]);
    } };
  };

  // ======================================================================================================================
  // pbsystem
  // ======================================================================================================================
  M.scenes.pbsystem = function (ctx, p) {
    const { T, sm, rng, cue } = ctx, v3 = (x, y, z) => new T.Vector3(x, y, z);
    const S = new T.Scene(); S.background = new T.Color('#02030a');
    const SK = sky(ctx, S, { n: 2000, halo: 0 });
    const spr = (col, op, sz) => { const s = new T.Sprite(new T.SpriteMaterial({ map: ctx.dotTex(), color: col, transparent: true, opacity: op, blending: T.AdditiveBlending, depthWrite: false })); s.scale.setScalar(sz); S.add(s); return s; };
    spr(new T.Color(4, 3.6, 3), 1, 2.6); spr(new T.Color('#ffc874'), .5, 12); spr(new T.Color('#ff9c50'), .14, 40);
    const RO = [12, 20, 30, 44], orbit = R => { const pts = []; for (let i = 0; i <= 256; i++) { const a = i / 256 * 6.2832; pts.push(new T.Vector3(Math.cos(a) * R, 0, Math.sin(a) * R)); }
      const l = new T.Line(new T.BufferGeometry().setFromPoints(pts), new T.LineBasicMaterial({ color: new T.Color(.35, .3, .22), transparent: true, opacity: R === 30 ? .55 : .25, blending: T.AdditiveBlending, depthWrite: false })); S.add(l); return l; };
    RO.forEach(orbit);
    const pl = [[12, 1.1, '#c9b8a0', .7], [20, 3.2, '#ffe2b0', 1.0], [44, 5.3, '#ff9a70', .6]].map(([R, a, c, s]) => { const g = spr(new T.Color(c), .9, s); g.position.set(Math.cos(a) * R, 0, Math.sin(a) * R); return g; });
    const earthC = spr(new T.Color(1, 1.5, 2.6), 1, 1.1), earthH = spr(new T.Color('#6f9cff'), .45, 4.5);
    const A0 = 2.6, A1 = A0 + Math.PI / 2, ea = t => A0 + (A1 - A0) * sm(ctx.t0, ctx.t1, t), eP = (t, o) => o.set(Math.cos(ea(t)) * 30, 0, -Math.sin(ea(t)) * 30);
    const NT = 80, tr = streaks(ctx, S, NT, { minPx: 2, near: [1, 5] });
    const IN = v3(.6, .75, .3).normalize(), NP = 40, pk = streaks(ctx, S, NP, { minPx: 1.6, near: [1, 5] }), pkB = [], r = rng(3);
    for (let i = 0; i < NP; i++) pkB.push([r(), (r() - .5) * 2, (r() - .5) * 2, .5 + .5 * r()]);
    const cam = new T.PerspectiveCamera(40, ctx.W / ctx.H, .5, 1e5); lift(ctx, cam, 0, p.lift == null ? .05 : p.lift, 40);
    const e = v3(0, 0, 0), e2 = v3(0, 0, 0), tg = v3(0, 0, 0);
    return { scene: S, camera: cam, draw(t, u) {
      const U = (t - ctx.t0) / Math.max(1, ctx.t1 - ctx.t0);
      eP(t, e); tg.set(0, 0, 0).lerp(e, .35);
      const dir = v3(.3, .95, .85).normalize().applyAxisAngle(v3(0, 1, 0), .2 - .35 * U);
      cam.position.copy(tg).addScaledVector(dir, 96 - 14 * U); cam.up.set(0, 1, 0); cam.lookAt(tg); cam.updateProjectionMatrix(); cam.updateMatrixWorld();
      SK.update(cam);
      earthC.position.copy(e); earthH.position.copy(e); earthH.material.opacity = .4 + .08 * Math.sin(t * 2.4);
      // trail: the arc Earth has covered since the shot start (time passing)
      for (let i = 0; i < NT; i++) { const a0 = A0 + (ea(t) - A0) * i / NT, a1 = A0 + (ea(t) - A0) * (i + 1) / NT, k = .5 * (i / NT);
        tr.set(i, Math.cos(a1) * 30, 0, -Math.sin(a1) * 30, Math.cos(a0) * 30, 0, -Math.sin(a0) * 30, .25, k * .5, k * .75, k); }
      tr.commit();
      // data pulses: from deep space (along IN) to where Earth is now, faint, recycling
      for (let i = 0; i < NP; i++) { const b = pkB[i], q0 = (t * .16 * b[3] + b[0]) % 1, q = q0 < 0 ? q0 + 1 : q0, R0 = 150, s0 = v3(IN.x * R0 + b[1] * 8, IN.y * R0 + b[2] * 6, IN.z * R0);
        const P = s0.clone().lerp(e, q), dl = s0.clone().sub(e).normalize().multiplyScalar(2.6), k = .7 * sm(0, .15, q) * sm(1, .9, q) * b[3];
        pk.set(i, P.x, P.y, P.z, P.x + dl.x, P.y + dl.y, P.z + dl.z, .3, k * .8, k * .9, k); }
      pk.commit();
    } };
  };
})();
