// TEST (2026-10-15): the same pond scene in two other looks, by swapping materials after the scene is built.
// requires: pond
//  look 'glow': solid forms kept, surfaces dark; light only from a fresnel rim (cool for the world, warm for the frogs) + fog fade
//  look 'wire': the meshes drawn as their own lines (wireframe) and vertex points, additive, on black
(function () {
  const M = window.MIYA;
  function rimMat(T, base, rim, k, far) {
    return new T.ShaderMaterial({ side: T.DoubleSide, uniforms: { base: { value: new T.Color(base) }, rim: { value: new T.Color(rim) }, k: { value: k }, far: { value: far } },
      vertexShader: 'varying vec3 vN; varying vec3 vV; varying float vD; void main(){ vec4 p=vec4(position,1.); vec3 n=normal;\n#ifdef USE_INSTANCING\n p=instanceMatrix*p; n=mat3(instanceMatrix)*n;\n#endif\n vec4 mv=modelViewMatrix*p; vN=normalize(normalMatrix*n); vV=normalize(-mv.xyz); vD=length(mv.xyz); gl_Position=projectionMatrix*mv; }',
      fragmentShader: 'uniform vec3 base; uniform vec3 rim; uniform float k; uniform float far; varying vec3 vN; varying vec3 vV; varying float vD; void main(){ float f=pow(1.-abs(dot(normalize(vN),normalize(vV))),6.); float a=clamp(1.-vD/far,0.,1.); gl_FragColor=vec4(base+rim*f*k*a,1.); }' });
  }
  function isFrogish(o) { let x = o; while (x) { if (x.userData && x.userData.frog) return true; x = x.parent; } return false; }
  function apply(ctx, S, look) {
    const T = ctx.T, list = [];
    S.traverse(o => { if ((o.isMesh || o.isInstancedMesh) && !o.isPoints) list.push(o); });
    S.fog = new T.FogExp2(look === 'wire' ? '#010208' : '#03040c', look === 'wire' ? .02 : .03);
    list.forEach(o => {
      const m = Array.isArray(o.material) ? o.material[0] : o.material;
      if (m && m.isShaderMaterial && m.uniforms.deep && look === 'wire') { m.uniforms.deep.value.set('#010309'); m.uniforms.fogD.value.set('#010208'); return; }   // dark water
      if (!m || m.isShaderMaterial && !m.uniforms.base) {   // dome / water shaders
        if (m && m.side === T.BackSide) { o.visible = false; S.background = new T.Color(look === 'wire' ? '#010208' : '#04051a'); }   // sky dome off
        return; }
      if (m.isMeshBasicMaterial && m.map && o.geometry.type === 'SphereGeometry' && o.geometry.parameters.radius > 5) return;   // moon
      const warm = o.geometry.attributes.position.count > 20000 || isFrogish(o);   // the frog meshes are the dense ones
      if (look === 'glow') {
        if (m.emissiveMap || (m.emissive && m.emissive.getHex() && m.emissiveIntensity > .5)) return;   // eyes / glowing insect stay
        o.material = rimMat(T, warm ? '#040306' : '#010207', warm ? '#ffbf66' : '#6f84ff', warm ? 2.6 : .8, warm ? 60 : 40);
      } else {
        const nv = o.geometry.attributes.position.count, dens = Math.min(1, 1500 / nv);   // dense meshes get fainter lines
        o.material = new T.MeshBasicMaterial({ color: warm ? '#ffc870' : '#5d78ff', wireframe: true, transparent: true, opacity: (warm ? .3 : (o.isInstancedMesh ? .05 : .1)) * Math.max(.1, Math.sqrt(dens)), blending: T.AdditiveBlending, depthWrite: false, fog: true });
        if (!o.isInstancedMesh) {   // points on every n-th vertex, sharing the live position attribute (follows the deform)
          const step = Math.max(1, Math.round(nv / (warm ? 2500 : 1200))), ix = []; for (let i = 0; i < nv; i += step) ix.push(i);
          const pg = new T.BufferGeometry(); pg.setAttribute('position', o.geometry.attributes.position); pg.setIndex(ix);
          const pts = new T.Points(pg, new T.PointsMaterial({ color: warm ? '#ffd890' : '#9fb4ff', size: warm ? .028 : .05, transparent: true, opacity: warm ? .8 : .3, blending: T.AdditiveBlending, depthWrite: false }));
          pts.frustumCulled = false; o.add(pts);
        }
      }
    });
  }
  M.scenes.pondlook = function (ctx, p) { const s = M.scenes.pond(ctx, p); apply(ctx, s.scene, p.look || 'glow'); return s; };
})();
