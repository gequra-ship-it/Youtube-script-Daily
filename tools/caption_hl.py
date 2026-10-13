# Subtitle word highlight (guideline 5, 2026-10-13): the word being spoken turns yellow, the rest stays white.
# There are no word timestamps (transcription models cannot be downloaded here, guideline 15-2), so word times are
# estimated: the line's speaking window is split by word length (characters + 1), the same estimate the caption
# lines themselves use inside a sentence. Only the colour changes (no size/position change), so the line never jumps.
# Everything is tl.set, so the timeline stays seekable.
import html

HL = '#ffd54a'
CSS = '.cap i{font-style:normal}'


def words_html(k, text):
    """Caption k's text with every word in its own <i id="c<k>w<j>">."""
    return ' '.join(f'<i id="c{k}w{j}">{html.escape(w, quote=False)}</i>' for j, w in enumerate(text.split()))


def word_times(text, a, b):
    """Start time of each word when the line is spoken from a to b."""
    ws = text.split(); wt = [len(w) + 1 for w in ws]; tot = sum(wt) or 1; out = []; c = 0
    for w in wt:
        out.append(a + (b - a) * c / tot); c += w
    return out


def highlight_js(k, text, a, b):
    """GSAP lines: word j is yellow from its start until the next word starts (the last word until the line goes)."""
    ts = word_times(text, a, b); js = []
    for j, t in enumerate(ts):
        js.append(f'tl.set("#c{k}w{j}",{{color:"{HL}"}},{t:.3f});')
        if j + 1 < len(ts): js.append(f'tl.set("#c{k}w{j}",{{color:"#fff"}},{ts[j + 1]:.3f});')
    return ''.join(js)
