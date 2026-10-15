# Miya's Lab depth prep (2026-10-15): a photo -> a depth map for photo-based 2.5D scenes (the camera moves a little and near
# things shift more than far things). Depth Anything V2 small (ONNX, Apache-2.0) on the CPU, a few seconds per image.
#   python3 tools/depth_prep.py <image> [<image> ...]   -> <image stem>_depth.png next to each image (8-bit, white = near)
# Model: DEPTH_MODEL=<model.onnx> (default $MIYA_WORK/depth/model.onnx), from
# huggingface.co/onnx-community/depth-anything-v2-small (onnx/model.onnx). Needs onnxruntime, numpy, pillow.
import os, sys
import numpy as np, onnxruntime as ort
from PIL import Image, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paths import WORK

sess = ort.InferenceSession(os.environ.get('DEPTH_MODEL') or f'{WORK}/depth/model.onnx', providers=['CPUExecutionProvider'])
inp = sess.get_inputs()[0].name
for f in sys.argv[1:]:
    im = Image.open(f).convert('RGB'); W, H = im.size
    h = 518; w = int(round(W / H * h / 14)) * 14   # the model works on multiples of 14 px
    x = np.asarray(im.resize((w, h), Image.BICUBIC), np.float32) / 255
    x = ((x - [.485, .456, .406]) / [.229, .224, .225]).transpose(2, 0, 1)[None].astype(np.float32)
    d = sess.run(None, {inp: x})[0].squeeze()   # relative inverse depth: larger = nearer
    d = (d - d.min()) / max(1e-6, d.max() - d.min())
    out = Image.fromarray((d * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(1.5))
    o = os.path.splitext(f)[0] + '_depth.png'; out.save(o); print(o, W, H)
