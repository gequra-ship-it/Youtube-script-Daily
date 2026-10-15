# Miya's Lab model prep (2026-10-15): a downloaded 3D model (glTF/GLB/FBX/OBJ, e.g. CC0 from Poly Haven, Smithsonian 3D,
# Sketchfab) -> a page-ready model file that tools/cine scenes load synchronously with MIYA.kit.model(name).
#   python3 tools/model_prep.py <model file> <name> [--faces 80000] [--tex 512] [--out tools/cine/models]
# 1) Blender (python module bpy; BLENDER_PY=<python with bpy>, default: the venv in $MIYA_WORK/bvenv) imports the model,
#    decimates every mesh so the total stays under --faces, scales textures down to --tex px, exports one GLB.
# 2) Headless Chromium loads the GLB with three.js GLTFLoader and writes <out>/<name>.js: geometry as base64 typed arrays,
#    PBR materials, textures as raw RGBA (so nothing loads asynchronously: chunked renders stay seek-safe), skeletons and
#    animation clips. A scene lists the models it uses in a line "// models: frog, fern_02" and build_cine copies the files.
# Keep the licence: write the source, author and licence into <out>/<name>.txt (the script asks for --credit).
import os, sys, json, base64, argparse, subprocess, tempfile, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import REPO, WORK

ap = argparse.ArgumentParser()
ap.add_argument('src'); ap.add_argument('name')
ap.add_argument('--faces', type=int, default=80000); ap.add_argument('--tex', type=int, default=512)
ap.add_argument('--out', default=f'{REPO}/tools/cine/models'); ap.add_argument('--credit', required=True, help='source URL, author, licence')
ap.add_argument('--keep', default='', help='comma list of mesh name parts to keep (others are dropped), e.g. a set of rocks')
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
BPY = os.environ.get('BLENDER_PY') or f'{WORK}/bvenv/bin/python'
tmp = tempfile.mkdtemp(); glb = f'{tmp}/{a.name}.glb'

blender = r'''
import bpy, sys, os, math
src, out, faces, tex, keep = sys.argv[-5], sys.argv[-4], int(sys.argv[-3]), int(sys.argv[-2]), sys.argv[-1]
bpy.ops.wm.read_factory_settings(use_empty=True)
ext = os.path.splitext(src)[1].lower()
if ext in ('.gltf', '.glb'): bpy.ops.import_scene.gltf(filepath=src)
elif ext == '.fbx': bpy.ops.import_scene.fbx(filepath=src)
elif ext == '.obj': bpy.ops.wm.obj_import(filepath=src)
elif ext == '.blend': bpy.ops.wm.open_mainfile(filepath=src)
else: raise SystemExit('unsupported ' + ext)
if keep:
    ks = [k.strip() for k in keep.split(',') if k.strip()]
    for o in list(bpy.data.objects):
        if o.type == 'MESH' and not any(k in o.name for k in ks): bpy.data.objects.remove(o, do_unlink=True)
meshes = [o for o in bpy.data.objects if o.type == 'MESH']
tot = sum(len(o.data.polygons) for o in meshes)
print('faces before', tot)
if tot > faces:
    r = faces / tot
    for o in meshes:
        m = o.modifiers.new('dec', 'DECIMATE'); m.ratio = max(.01, r)
        bpy.context.view_layer.objects.active = o
        if not o.data.shape_keys: bpy.ops.object.modifier_apply(modifier=m.name)
for im in bpy.data.images:
    if im.size[0] > tex or im.size[1] > tex:
        s = tex / max(im.size[0], im.size[1]); im.scale(max(1, int(im.size[0] * s)), max(1, int(im.size[1] * s)))
print('faces after', sum(len(o.data.polygons) for o in bpy.data.objects if o.type == 'MESH'))
bpy.ops.export_scene.gltf(filepath=out, export_format='GLB', export_apply=True, export_animations=True, export_image_format='JPEG')
'''
bs = f'{tmp}/b.py'; open(bs, 'w').write(blender)
r = subprocess.run([BPY, bs, '--', os.path.abspath(a.src), glb, str(a.faces), str(a.tex), a.keep], capture_output=True, text=True)
print('\n'.join(l for l in r.stdout.splitlines() if l.startswith('faces')))
if not os.path.exists(glb): raise SystemExit('blender failed:\n' + r.stdout[-2000:] + r.stderr[-2000:])

# ---- 2) serialize in a headless browser (GLTFLoader decodes textures there) ----
CINE = f'{REPO}/tools/cine/assets'
page = f'''<html><body><script src="file://{CINE}/three.js"></script><script src="file://{CINE}/gltf-loader.js"></script><script>
const T = THREE;
function b64(buf) {{ let s = '', u = new Uint8Array(buf.buffer || buf, buf.byteOffset || 0, buf.byteLength); for (let i = 0; i < u.length; i += 32768) s += String.fromCharCode.apply(null, u.subarray(i, i + 32768)); return btoa(s); }}
window.run = (glb64) => new Promise(res => {{
  const bin = Uint8Array.from(atob(glb64), c => c.charCodeAt(0)).buffer;
  new T.GLTFLoader().parse(bin, '', g => {{
    const nodes = [], geoms = [], mats = [], texs = [], gmap = new Map(), mmap = new Map(), tmap = new Map(), nmap = new Map();
    const TY = {{ Float32Array: 'f32', Uint16Array: 'u16', Uint32Array: 'u32', Uint8Array: 'u8', Int16Array: 'i16', Int8Array: 'i8' }};
    function tex(t) {{ if (!t) return null; if (tmap.has(t)) return tmap.get(t); const im = t.image; const c = document.createElement('canvas'); c.width = im.width; c.height = im.height;
      const x = c.getContext('2d'); x.drawImage(im, 0, 0); const d = x.getImageData(0, 0, c.width, c.height).data;
      texs.push({{ w: c.width, h: c.height, rgba: b64(d), srgb: t.colorSpace === T.SRGBColorSpace, wrapS: t.wrapS, wrapT: t.wrapT }}); tmap.set(t, texs.length - 1); return texs.length - 1; }}
    function mat(m) {{ if (mmap.has(m)) return mmap.get(m);
      const o = {{ name: m.name, color: m.color ? m.color.getHex() : 0xffffff, roughness: m.roughness ?? 1, metalness: m.metalness ?? 0, emissive: m.emissive ? m.emissive.getHex() : 0,
        transparent: m.transparent, opacity: m.opacity, alphaTest: m.alphaTest, side: m.side, map: tex(m.map), normalMap: tex(m.normalMap), roughnessMap: tex(m.roughnessMap),
        metalnessMap: tex(m.metalnessMap), aoMap: tex(m.aoMap), emissiveMap: tex(m.emissiveMap), alphaMap: tex(m.alphaMap), vertexColors: m.vertexColors }};
      mats.push(o); mmap.set(m, mats.length - 1); return mats.length - 1; }}
    function geom(gm) {{ if (gmap.has(gm)) return gmap.get(gm); const at = {{}};
      for (const k in gm.attributes) {{ const A = gm.attributes[k]; const arr = A.isInterleavedBufferAttribute ? Float32Array.from({{ length: A.count * A.itemSize }}, (_, i) => A.getComponent(Math.floor(i / A.itemSize), i % A.itemSize)) : A.array;
        at[k] = {{ t: TY[arr.constructor.name], n: A.itemSize, norm: A.normalized, d: b64(arr) }}; }}
      const ix = gm.index ? {{ t: TY[gm.index.array.constructor.name], d: b64(gm.index.array) }} : null;
      geoms.push({{ at, ix, groups: gm.groups }}); gmap.set(gm, geoms.length - 1); return geoms.length - 1; }}
    g.scene.traverse(o => {{ nmap.set(o, nodes.length); nodes.push(null); }});
    g.scene.traverse(o => {{ const n = {{ name: o.name, type: o.isSkinnedMesh ? 'skinned' : o.isMesh ? 'mesh' : o.isBone ? 'bone' : 'obj', parent: o.parent && nmap.has(o.parent) ? nmap.get(o.parent) : -1,
        p: o.position.toArray(), q: o.quaternion.toArray(), s: o.scale.toArray() }};
      if (o.isMesh) {{ n.g = geom(o.geometry); n.m = Array.isArray(o.material) ? o.material.map(mat) : mat(o.material); }}
      if (o.isSkinnedMesh) {{ n.bones = o.skeleton.bones.map(b => nmap.get(b)); n.inv = b64(new Float32Array(o.skeleton.boneInverses.flatMap(m => m.elements))); n.bindMatrix = o.bindMatrix.elements; }}
      nodes[nmap.get(o)] = n; }});
    res(JSON.stringify({{ nodes, geoms, mats, texs, anims: g.animations.map(c => T.AnimationClip.toJSON(c)) }}));
  }}, e => res('ERR ' + e));
}});
</script></body></html>'''
pf = f'{tmp}/s.html'; open(pf, 'w').write(page)
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(executable_path=os.environ.get('HYPERFRAMES_BROWSER_PATH', '/opt/pw-browsers/chromium'), args=['--allow-file-access-from-files'])
    pg = b.new_page(); errs = []; pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file://' + pf); data = pg.evaluate('g => window.run(g)', base64.b64encode(open(glb, 'rb').read()).decode()); b.close()
if data.startswith('ERR') or errs: raise SystemExit(f'serialize failed: {data[:300]} {errs}')
d = json.loads(data)
open(f'{a.out}/{a.name}.js', 'w').write(f'(window.MIYA = window.MIYA || {{}}).models = window.MIYA.models || {{}};\nwindow.MIYA.models[{json.dumps(a.name)}] = {data};\n')
open(f'{a.out}/{a.name}.txt', 'w').write(a.credit.strip() + '\n')
mb = os.path.getsize(f'{a.out}/{a.name}.js') / 1e6
print(f'{a.out}/{a.name}.js  {mb:.1f} MB  nodes {len(d["nodes"])}  meshes {sum(1 for n in d["nodes"] if n["type"] in ("mesh","skinned"))}  textures {len(d["texs"])}  clips {len(d["anims"])}')
shutil.rmtree(tmp)
