// Miya's Lab cine runtime (2026-10-14). Reads window.CINE (written by tools/build_cine.py) and builds:
//  - one WebGL renderer; every shot is a scene module (tools/cine/scenes/*.js or videos/<slug>/scenes/*.js) registered with
//    MIYA.def(type, factory). A shot is drawn as a pure function of the timeline time, so any frame can be rendered alone
//    (seek-safe) and the video can be rendered in parallel chunks (render-chunked.yml).
//  - a compositor pass (two render targets + a shader) for transitions between shots and for tone mapping.
//  - the HUD and text layers (chapter label, clock, progress bar, rolling keyword, subtitle, log, plot, badge, text cards,
//    data cards, captions with the spoken word highlighted), all on one paused GSAP timeline (window.__timelines.main).
(function () {
'use strict';
const C = window.CINE, T = THREE, W = C.w, H = C.h, VERT = H > W, ACC = C.accent || '#ffc65a';
const root = document.getElementById('root');
if (VERT) root.classList.add('vert');
document.documentElement.style.setProperty('--w', W + 'px'); document.documentElement.style.setProperty('--h', H + 'px');
document.documentElement.style.setProperty('--acc', ACC);

// ---------------- helpers shared with scene modules ----------------
const sm = (a, b, x) => { x = Math.min(1, Math.max(0, (x - a) / (b - a))); return x * x * (3 - 2 * x); };
const clamp = (x, a, b) => Math.min(b, Math.max(a, x));
function rng(seed) { let s = (seed | 0) % 2147483647; if (s <= 0) s += 2147483646; return () => (s = (s * 16807) % 2147483647) / 2147483647; }
function ctex(sz, fn) { const c = document.createElement('canvas'); c.width = c.height = sz; fn(c.getContext('2d'), sz); const t = new T.CanvasTexture(c); t.colorSpace = T.SRGBColorSpace; return t; }
let _dot = null;
function dotTex() { return _dot || (_dot = ctex(64, (g, s) => { const r = g.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2); r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(.3, 'rgba(255,255,255,.6)'); r.addColorStop(1, 'rgba(255,255,255,0)'); g.fillStyle = r; g.fillRect(0, 0, s, s); })); }
function points(n, o) { o = o || {}; const g = new T.BufferGeometry(); g.setAttribute('position', new T.BufferAttribute(new Float32Array(n * 3), 3)); g.setAttribute('color', new T.BufferAttribute(new Float32Array(n * 3).fill(1), 3));
  return new T.Points(g, new T.PointsMaterial({ size: o.size || .2, map: dotTex(), vertexColors: true, transparent: true, opacity: o.opacity == null ? 1 : o.opacity, blending: T.AdditiveBlending, depthWrite: false, sizeAttenuation: o.atten !== false, color: o.color || '#ffffff', fog: !!o.fog })); }
function stars(scene, n, r, o) { o = o || {}; const p = points(n, { size: o.size || 1.2, opacity: o.opacity || .75, color: o.color || '#cfd8ff', atten: false }); const a = p.geometry.attributes.position.array, rr = rng(o.seed || 5);
  for (let i = 0; i < n; i++) { const u = rr() * 2 - 1, th = rr() * 6.283, q = Math.sqrt(1 - u * u); a.set([q * Math.cos(th) * r, u * r, q * Math.sin(th) * r], i * 3); } scene.add(p); return p; }
function glow(parent, color, scale, op) { const s = new T.Sprite(new T.SpriteMaterial({ map: dotTex(), color, transparent: true, opacity: op == null ? .5 : op, blending: T.AdditiveBlending, depthWrite: false, fog: false })); s.scale.set(scale, scale, 1); parent.add(s); return s; }
let _env = null;
function env() { return _env || (_env = new T.PMREMGenerator(R).fromScene(new RoomEnvironment(), .04).texture); }
function cue(name, fallback) { if (name == null) return fallback; if (typeof name === 'number') return name; const v = C.cues[name]; if (v == null) { if (fallback == null) console.warn('cue missing', name); return fallback == null ? 1e9 : fallback; } return v; }
function unit(uid) { return C.units.find(u => u.uid === uid); }
// put the subject left or right of centre without moving the camera (frac of width, + = subject to the right)
function side(cam, frac) {
  if (VERT) {   // Shorts: keep the landscape horizontal field of view, so the subject fits the narrow frame
    if (!cam.userData.vfit) { cam.userData.vfit = 1; const h = 2 * Math.atan(Math.tan(cam.fov * Math.PI / 360) * 16 / 9 * .62); cam.fov = 2 * Math.atan(Math.tan(h / 2) * H / W) * 180 / Math.PI; cam.updateProjectionMatrix(); }
    cam.clearViewOffset(); return; }
  cam.setViewOffset(W, H, -W * frac, 0, W, H); }

// scene files load BEFORE this file and register themselves: (window.MIYA = window.MIYA || {scenes: {}}).scenes.<type> = (ctx, params) => ...
window.MIYA = window.MIYA || {};
const MIYA = window.MIYA; MIYA.scenes = MIYA.scenes || {};
MIYA.def = (type, factory) => { MIYA.scenes[type] = factory; };

// ---------------- renderer + compositor ----------------
let R = null;
try { R = new T.WebGLRenderer({ canvas: document.getElementById('gl'), antialias: false, preserveDrawingBuffer: true }); }
catch (e) { document.getElementById('err').style.display = 'block'; }
const ctxBase = { T, W, H, VERT, ACC, sm, clamp, rng, ctex, dotTex, points, stars, glow, env, cue, unit, side, get R() { return R; }, pal: C.pal || {} };
let RTa, RTb, quad, qcam, qmat;
if (R) {
  R.setPixelRatio(1); R.setSize(W, H, false); R.autoClear = true;
  const mk = () => new T.WebGLRenderTarget(W, H, { type: T.HalfFloatType, samples: 4, colorSpace: T.LinearSRGBColorSpace });
  RTa = mk(); RTb = mk();
  qcam = new T.OrthographicCamera(-1, 1, 1, -1, 0, 1);
  const tones = (C.tones || ['#1d2150', '#252a63', '#2e3476', '#373f89', '#40499b', '#4a54ad']).map(c => new T.Color(c));
  qmat = new T.ShaderMaterial({
    uniforms: { tA: { value: null }, tB: { value: null }, p: { value: 0 }, kind: { value: 0 }, o: { value: new T.Vector2(.5, .5) }, aspect: { value: W / H },
      acc: { value: new T.Color(ACC) }, tones: { value: tones }, expo: { value: C.exposure || 1.0 } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv=uv; gl_Position=vec4(position.xy,0.,1.); }',
    fragmentShader: `
      uniform sampler2D tA,tB; uniform float p,aspect,expo; uniform int kind; uniform vec2 o; uniform vec3 acc; uniform vec3 tones[6]; varying vec2 vUv;
      vec3 RRT(vec3 v){ vec3 a=v*(v+0.0245786)-0.000090537; vec3 b=v*(0.983729*v+0.4329510)+0.238081; return a/b; }
      vec3 aces(vec3 c){ const mat3 I=mat3(vec3(0.59719,0.07600,0.02840),vec3(0.35458,0.90834,0.13383),vec3(0.04823,0.01566,0.83777));
        const mat3 O=mat3(vec3(1.60475,-0.10208,-0.00327),vec3(-0.53108,1.10813,-0.07276),vec3(-0.07367,-0.00605,1.07602));
        c*=expo/0.6; c=I*c; c=RRT(c); c=O*c; return clamp(c,0.,1.); }
      vec3 srgb(vec3 c){ return mix(c*12.92, 1.055*pow(c,vec3(1./2.4))-0.055, step(vec3(0.0031308),c)); }
      vec3 A(vec2 u){ return texture2D(tA,u).rgb; } vec3 B(vec2 u){ return texture2D(tB,u).rgb; }
      float e3(float x){ return x<.5?4.*x*x*x:1.-pow(-2.*x+2.,3.)/2.; }
      void main(){ vec2 u=vUv; vec3 c;
        if(kind==0){ c=A(u); }
        else if(kind==1){ c = p<.5 ? A(u)*(1.-2.*p) : B(u)*(2.*p-1.); }                                   // dip to black
        else if(kind==2){ c = mix(A(u),B(u),smoothstep(0.,1.,p)); }                                         // cross dissolve
        else if(kind==3){ float m=1.-abs(2.*p-1.); c=(p<.5?A(u):B(u)) + vec3(1.,.93,.82)*pow(m,1.5)*1.4; }   // light flash
        else if(kind==4){ float d=(u.x*aspect+(1.-u.y))/(aspect+1.), e=e3(p)*1.08-.04; c = d<e ? B(u) : A(u);  // diagonal wipe + light edge
          c += acc*smoothstep(.012,0.,abs(d-e))*2.2*(1.-abs(2.*p-1.)*.3); }
        else if(kind==5){ vec2 q=(u-o)*vec2(aspect,1.); float r=length(q), R=e3(p)*1.25*max(aspect,1.)*1.2; c = mix(A(u),B(u),smoothstep(R,R-.02,r)); }  // iris
        else if(kind==6){ float h=e3(p)*.52; c = mix(A(u),B(u),smoothstep(h,h-.01,abs(u.y-.5))); }        // eye opening
        else if(kind==7){ float q=e3(p); c = u.y<q ? B(u+vec2(0.,1.-q)) : A(u-vec2(0.,q)); }               // push up
        else if(kind==8){ float q=e3(p), v=sin(3.14159*p)*.05; vec3 sa=vec3(0.), sb=vec3(0.);              // whip pan with motion blur
          for(int i=0;i<9;i++){ float k=(float(i)-4.)/4.*v; sa+=A(u+vec2(q+k,0.)); sb+=B(u+vec2(q-1.+k,0.)); }
          c = (u.x+q<1.) ? sa/9. : sb/9.; }
        else if(kind==9){ float q=e3(p); vec2 ua=o+(u-o)/(1.+q*2.5); vec2 ub=o+(u-o)/(.75+.25*q); c=mix(A(ua),B(ub),smoothstep(.35,.65,p)); }  // zoom through
        else if(kind==10){ float bar=floor(u.x*6.), dl=bar*.06; bool cov;                                  // tone bars
          if(p<.5){ float q=clamp(p*2.7-dl,0.,1.); cov=(1.-u.y)<q; } else { float q=clamp((p-.5)*2.7-dl,0.,1.); cov=u.y>q; }
          if(cov){ gl_FragColor=vec4(srgb(tones[int(bar)]),1.); return; } c = p<.5 ? A(u) : B(u); }
        else { c=B(u); }
        gl_FragColor = vec4(srgb(aces(c)), 1.); }`,
    depthTest: false, depthWrite: false });
  quad = new T.Mesh(new T.PlaneGeometry(2, 2), qmat); quad.frustumCulled = false;
}
const KIND = { cut: 0, none: 0, dip: 1, xfade: 2, flash: 3, wipe: 4, iris: 5, eye: 6, push: 7, whip: 8, zoom: 9, blinds: 10 };
const TDUR = { cut: 0, none: 0, dip: .9, xfade: .8, flash: .7, wipe: .8, iris: .9, eye: .8, push: .7, whip: .45, zoom: .9, blinds: 1.1 };

// ---------------- shots ----------------
const SHOTS = []; C.chapters.forEach(ch => ch.shots.forEach(s => SHOTS.push(Object.assign({ ch }, s))));
SHOTS.sort((a, b) => a.t0 - b.t0);
const inst = new Map();
function shotObj(i) {
  if (inst.has(i)) return inst.get(i);
  const s = SHOTS[i], f = MIYA.scenes[s.type];
  if (!f) throw new Error('unknown scene type ' + s.type);
  const ctx = Object.assign({}, ctxBase, { t0: s.t0, t1: s.t1, shot: s, chapter: s.ch });
  const o = f(ctx, s.params || {}); inst.set(i, o); return o;
}
function renderShot(i, t, rt) { const o = shotObj(i); o.draw(t, t - SHOTS[i].t0); R.setRenderTarget(rt); R.render(o.scene, o.camera); }
function frame(t) {
  if (!R) return;
  let i = 0; for (let k = 0; k < SHOTS.length; k++) if (t >= SHOTS[k].t0) i = k;
  // transition window around the start of shot k: [t0 - d/2, t0 + d/2]
  let tr = null;
  for (const k of [i, i + 1]) { const s = SHOTS[k]; if (!s || k === 0) continue; const d = s.trd != null ? s.trd : (TDUR[s.tr] || 0);
    if (d > 0 && t >= s.t0 - d / 2 && t < s.t0 + d / 2) tr = { a: k - 1, b: k, p: (t - (s.t0 - d / 2)) / d, kind: KIND[s.tr] || 0, o: s.tro || [.5, .5] }; }
  if (tr) { renderShot(tr.a, t, RTa); renderShot(tr.b, t, RTb); qmat.uniforms.kind.value = tr.kind; qmat.uniforms.p.value = tr.p; qmat.uniforms.o.value.set(tr.o[0], 1 - tr.o[1]); }
  else { renderShot(i, t, RTa); qmat.uniforms.kind.value = 0; }
  qmat.uniforms.tA.value = RTa.texture; qmat.uniforms.tB.value = RTb.texture;
  R.setRenderTarget(null); R.render(quad, qcam);
}

// ---------------- DOM ----------------
const el = (tag, cls, id, html, parent) => { const d = document.createElement(tag); if (cls) d.className = cls; if (id) d.id = id; if (html != null) d.innerHTML = html; (parent || root).appendChild(d); return d; };
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const emph = s => esc(s).replace(/\*([^*]+)\*/g, '<em>$1</em>');
const NS = 'http://www.w3.org/2000/svg';
const hudL = document.getElementById('hudL'), clk = document.getElementById('clk'), prog = document.getElementById('prog'), dot = document.getElementById('dot');
C.chapters.forEach(ch => { if (ch.t0 > .5) { const i = document.createElement('i'); i.style.left = (ch.t0 / C.total * 100) + '%'; document.getElementById('bar').appendChild(i); } });
C.units.forEach((u, k) => {
  if (u.kw) { const d = el('div', 'kw' + (u.acc ? ' acc' : '') + (u.kw.length > 11 ? ' s' : ''), 'kw' + k, esc(u.kw)); }
  if (u.sub) el('div', 'sb', 'sb' + k, emph(u.sub));
  if (u.log) el('div', 'li', 'li' + k, esc(u.log));
  if (u.badge) el('div', 'bv', 'bv' + k, esc(u.badge));
  if (u.card) el('div', 'card', 'cd' + k, emph(u.card));
});
el('div', null, 'plotlab'); el('div', null, 'badgelab');
const svg = document.createElementNS(NS, 'svg'); svg.id = 'plot'; svg.setAttribute('width', 640); svg.setAttribute('height', 190); svg.setAttribute('viewBox', '0 0 640 190'); root.appendChild(svg);
svg.innerHTML = '<path d="M0 170 H640" stroke="rgba(230,236,255,.2)" stroke-width="1" fill="none"/><g id="ptk"></g><path id="pc" d="" stroke="rgba(255,236,200,.85)" stroke-width="2.2" fill="none" stroke-linecap="round"/><circle id="phg" r="16" fill="rgba(255,198,90,.25)"/><circle id="ph" r="5" fill="#fff4dc"/>';
C.caps.forEach((c, k) => el('div', 'cap', 'c' + k, c.words.map((w, j) => `<i id="c${k}w${j}">${esc(w)}</i>`).join(' ')));
(C.datacards || []).forEach((d, k) => {
  const rows = d.rows.map((r, j) => `<div class="rw" id="dc${k}r${j}"><div class="rl">${esc(r[0])}</div><div class="rv ${r[3] || ''}">${esc(r[1])}</div><div class="rn">${esc(r[2] || '')}</div></div>`).join('');
  el('div', 'dc', 'dc' + k, `<div class="dt">${esc(d.title)}</div><div class="ds">${esc(d.sub || '')}</div>${rows}<div class="dk" id="dc${k}k">${emph(d.concl || '')}</div><div class="dsrc">${esc(d.source || '')}</div>`);
});

// plot per chapter (values given on units; smooth steps between unit starts)
const plots = C.chapters.filter(ch => ch.plot).map(ch => {
  const us = C.units.filter(u => u.t0 >= ch.t0 - 1e-6 && u.t0 < ch.t1 && u.plot != null);
  const val = t => { let v = us.length ? us[0].plot : 0; for (let j = 1; j < us.length; j++) v += (us[j].plot - us[j - 1].plot) * sm(us[j].t0, us[j].t0 + Math.min(3, (us[j].t1 - us[j].t0)), t); return v; };
  const lo = ch.plot.min != null ? ch.plot.min : Math.min(...us.map(u => u.plot)), hi = ch.plot.max != null ? ch.plot.max : Math.max(...us.map(u => u.plot));
  const px = t => (t - ch.t0) / (ch.t1 - ch.t0) * 640, py = v => 158 - (hi > lo ? (v - lo) / (hi - lo) : .5) * 120;
  let d = ''; for (let k = 0; k <= 240; k++) { const t = ch.t0 + k / 240 * (ch.t1 - ch.t0); d += (k ? 'L' : 'M') + px(t).toFixed(1) + ' ' + py(val(t)).toFixed(1); }
  return { ch, d, ticks: us.map(u => px(u.t0)) };
});
const pc = document.getElementById('pc'), ph = document.getElementById('ph'), phg = document.getElementById('phg'), ptk = document.getElementById('ptk');
let curPlot = null, PL = 1;
function setPlot(pl) { if (curPlot === pl) return; curPlot = pl; ptk.innerHTML = ''; if (!pl) { pc.setAttribute('d', ''); return; }
  pc.setAttribute('d', pl.d); PL = pc.getTotalLength(); pc.style.strokeDasharray = PL;
  pl.ticks.forEach(x => { const l = document.createElementNS(NS, 'line'); l.setAttribute('x1', x); l.setAttribute('x2', x); l.setAttribute('y1', 166); l.setAttribute('y2', 174); l.setAttribute('stroke', 'rgba(230,236,255,.35)'); ptk.appendChild(l); }); }
let curCh = null;
function hud(t) {
  clk.textContent = new Date(Math.max(0, t - (C.lead || 0)) * 1000).toISOString().substr(11, 12);
  prog.style.width = (t / C.total * 100) + '%'; dot.style.left = (t / C.total * 100) + '%';
  const ch = C.chapters.find(c => t >= c.t0 && t < c.t1) || C.chapters[C.chapters.length - 1];
  if (ch !== curCh) { curCh = ch; hudL.innerHTML = (ch.label ? `<em>${esc(ch.label)}</em> &nbsp;·&nbsp; ` : '') + esc(ch.title || C.title || ''); }
  const pl = plots.find(p => p.ch === ch) || null; setPlot(pl);
  if (pl) { const q = clamp((t - ch.t0) / (ch.t1 - ch.t0), 0, 1); pc.style.strokeDashoffset = PL * (1 - q); const p = pc.getPointAtLength(PL * q); ph.setAttribute('cx', p.x); ph.setAttribute('cy', p.y); phg.setAttribute('cx', p.x); phg.setAttribute('cy', p.y); }
}

// ---------------- timeline ----------------
let cur = -1;
const drv = { t(v) { if (v === undefined) return cur; cur = v; frame(v); hud(v); } };
const tl = gsap.timeline({ paused: true });
tl.fromTo(drv, { t: 0 }, { t: C.total, duration: C.total, ease: 'none', immediateRender: true }, 0);
tl.fromTo('#fade', { opacity: 1 }, { opacity: 0, duration: 1.4, ease: 'power1.out', immediateRender: false }, .05);
tl.to('#fade', { opacity: 1, duration: 1.0, ease: 'power1.in' }, C.total - 1.0);
// per chapter: plot/badge labels in and out
C.chapters.forEach(ch => {
  const pl = plots.find(p => p.ch === ch);
  if (pl) { tl.set('#plotlab', { textContent: ch.plot.label || '' }, ch.t0); tl.fromTo('#plot,#plotlab', { opacity: 0 }, { opacity: 1, duration: .8, immediateRender: false }, ch.t0 + .4); tl.to('#plot,#plotlab', { opacity: 0, duration: .5 }, ch.t1 - .6); }
  if (ch.badge_label) { tl.set('#badgelab', { textContent: ch.badge_label }, ch.t0); tl.fromTo('#badgelab', { opacity: 0 }, { opacity: 1, duration: .8, immediateRender: false }, ch.t0 + .4); tl.to('#badgelab', { opacity: 0, duration: .5 }, ch.t1 - .6); }
});
const chOf = t => C.chapters.find(c => t >= c.t0 - 1e-6 && t < c.t1) || C.chapters[C.chapters.length - 1];
// a keyword/subtitle/badge stays until the next one, a text card (which clears the left column) or the chapter end
const nextWith = (k, key) => { const ch = chOf(C.units[k].t0); for (let j = k + 1; j < C.units.length; j++) { if (C.units[j].t0 >= ch.t1) break; if (C.units[j][key] != null || C.units[j].card) return C.units[j].t0; } return ch.t1; };
C.units.forEach((u, k) => {
  const a = Math.max(.3, u.t0 + .15);
  if (u.kw) { const b = nextWith(k, 'kw');
    tl.fromTo('#kw' + k, { opacity: 0, y: 46, filter: 'blur(10px)' }, { opacity: 1, y: 0, filter: 'blur(0px)', duration: .6, ease: 'power3.out', immediateRender: false }, a);
    tl.to('#kw' + k, { opacity: 0, y: -46, filter: 'blur(10px)', duration: .4, ease: 'power2.in' }, b - .15); }
  if (u.sub) { const b = nextWith(k, 'sub');
    tl.fromTo('#sb' + k, { opacity: 0, filter: 'blur(6px)' }, { opacity: 1, filter: 'blur(0px)', duration: .7, ease: 'power2.out', immediateRender: false }, a + .25);
    tl.to('#sb' + k, { opacity: 0, duration: .3 }, b - .2); }
  if (u.badge) { const b = nextWith(k, 'badge');
    tl.fromTo('#bv' + k, { opacity: 0, y: 18 }, { opacity: 1, y: 0, duration: .5, ease: 'power2.out', immediateRender: false }, a + .25);
    tl.to('#bv' + k, { opacity: 0, y: -18, duration: .3 }, b - .1); }
  if (u.card) { tl.fromTo('#cd' + k, { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .9, ease: 'power2.out', immediateRender: false }, u.t0 + .2);
    tl.to('#cd' + k, { opacity: 0, duration: .45 }, u.t1 - .5);
    tl.to('#dim', { opacity: .82, duration: .6 }, u.t0); tl.to('#dim', { opacity: 0, duration: .6 }, u.t1 - .45); }
});
// log: lines accumulate per chapter; newest at the bottom, older lines move up and dim
C.chapters.forEach(ch => {
  const ls = C.units.map((u, k) => [u, k]).filter(([u]) => u.log && u.t0 >= ch.t0 - 1e-6 && u.t0 < ch.t1);
  ls.forEach(([u, k], n) => {
    tl.fromTo('#li' + k, { opacity: 0, top: 720 }, { opacity: 1, top: 700, duration: .5, ease: 'power2.out', immediateRender: false }, Math.max(.3, u.t0 + .65));
    ls.slice(n + 1).forEach(([w], m) => { const d = m + 1; tl.to('#li' + k, { top: 700 - d * 34, opacity: Math.max(.12, 1 - d * .2), duration: .45, ease: 'power2.out' }, w.t0 + .65); });
    tl.to('#li' + k, { opacity: 0, duration: .4 }, ch.t1 - .6);
  });
});
// data cards (the chalkboard's place): title fades up, rows pop at their spoken times, conclusion last
(C.datacards || []).forEach((d, k) => {
  tl.fromTo('#dc' + k, { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .8, ease: 'power2.out', immediateRender: false }, d.t0 + .1);
  tl.to('#dim', { opacity: .55, duration: .6 }, d.t0);
  d.rows.forEach((r, j) => tl.fromTo(`#dc${k}r${j}`, { opacity: 0, x: -20 }, { opacity: 1, x: 0, duration: .5, ease: 'power2.out', immediateRender: false }, d.pop[j + 1] != null ? d.pop[j + 1] : d.t0 + .6 + j * .8));
  tl.fromTo(`#dc${k}k`, { opacity: 0 }, { opacity: 1, duration: .6, immediateRender: false }, d.pop[d.rows.length + 1] != null ? d.pop[d.rows.length + 1] : d.t1 - 3);
  tl.to('#dc' + k, { opacity: 0, duration: .5 }, d.t1 - .55); tl.to('#dim', { opacity: 0, duration: .5 }, d.t1 - .5);
});
// captions: on/off at their times, the spoken word turns to the accent colour
C.caps.forEach((c, k) => {
  tl.fromTo('#c' + k, { opacity: 0 }, { opacity: 1, duration: .2, immediateRender: false }, c.t0); tl.to('#c' + k, { opacity: 0, duration: .15 }, c.t1 - .15);
  c.wt.forEach((w, j) => { tl.set(`#c${k}w${j}`, { color: '#ffd58a' }, w); if (j + 1 < c.wt.length) tl.set(`#c${k}w${j}`, { color: 'rgba(255,255,255,.92)' }, c.wt[j + 1]); });
});
window.__timelines = window.__timelines || {}; window.__timelines.main = tl; tl.seek(0);
window.MIYA_CINE_READY = true;
})();
