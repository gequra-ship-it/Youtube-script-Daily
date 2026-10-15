# Miya's Lab image generation (2026-10-15): photoreal stills with the Gemini API for photo-based 2.5D scenes.
#   GEMINI_API_KEY=... python3 tools/gen_image.py <out dir> <jobs.json> [--model <id>]
# jobs.json: [{"name": "pond_wide", "prompt": "...", "aspect": "16:9"}, ...] -> <out dir>/<name>.png (+ <name>.txt with the prompt
# and the model). Without --model the script lists the models the key can use and tries the image-capable ones in order.
# Run it in GitHub Actions (workflow gen-image.yml): the key is a repository secret and is never printed.
import os, sys, json, argparse
from google import genai
from google.genai import types

ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('jobs'); ap.add_argument('--model', default='')
a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
client = genai.Client(api_key=os.environ['GEMINI_API_KEY'])
names = [m.name.split('/')[-1] for m in client.models.list()]
img = [n for n in names if 'image' in n or n.startswith('imagen')]
print('image-capable models:', img)
order = [a.model] if a.model else sorted(img, key=lambda n: (not n.startswith('imagen'), 'preview' in n, n), reverse=False)

def gen(model, prompt, aspect):
    if model.startswith('imagen'):
        r = client.models.generate_images(model=model, prompt=prompt, config=types.GenerateImagesConfig(number_of_images=1, aspect_ratio=aspect))
        return r.generated_images[0].image.image_bytes
    r = client.models.generate_content(model=model, contents=prompt + f' Aspect ratio {aspect}.',
        config=types.GenerateContentConfig(response_modalities=['IMAGE'], image_config=types.ImageConfig(aspect_ratio=aspect)))
    for p in r.candidates[0].content.parts:
        if getattr(p, 'inline_data', None) and p.inline_data.data: return p.inline_data.data
    raise RuntimeError('no image in response')

for j in json.load(open(a.jobs)):
    for m in order:
        try:
            b = gen(m, j['prompt'], j.get('aspect', '16:9'))
            open(f"{a.out}/{j['name']}.png", 'wb').write(b)
            open(f"{a.out}/{j['name']}.txt", 'w').write(f"model: {m}\nprompt: {j['prompt']}\n")
            print(j['name'], 'ok with', m, len(b), 'bytes'); break
        except Exception as e:
            print(j['name'], 'failed with', m, type(e).__name__, str(e)[:200])
    else:
        sys.exit(f"{j['name']}: no model produced an image")
