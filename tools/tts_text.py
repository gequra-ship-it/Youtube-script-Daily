"""TTS input pre-processing: spell out four-digit years so Kokoro does not say "nineteen hundred ninety" for 1990.
1100-1999 and 2010-2099: two pairs ("nineteen ninety", "twenty twenty-six"); xx00: "nineteen hundred"; xx01-xx09: "nineteen oh five";
2000: "two thousand"; 2001-2009: "two thousand five"; decades: 1990s -> "nineteen nineties".
Four-digit numbers with a comma/decimal/$ or followed by a unit (km, people, ...) are left alone."""
import re, sys
ONES = 'zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen'.split()
TENS = 'x x twenty thirty forty fifty sixty seventy eighty ninety'.split()
def two(n):
    if n < 20: return ONES[n]
    return TENS[n // 10] + ('' if n % 10 == 0 else '-' + ONES[n % 10])
def year(y):
    a, b = divmod(y, 100)
    if y == 2000: return 'two thousand'
    if 2001 <= y <= 2009: return 'two thousand ' + ONES[b]
    if b == 0: return two(a) + ' hundred'
    return two(a) + (' oh ' + ONES[b] if b < 10 else ' ' + two(b))
def decade(y):
    a, b = divmod(y, 100)
    if y == 2000: return 'two thousands'
    if b == 0: return two(a) + ' hundreds'
    if b < 10: return two(a) + ' oh ' + ONES[b] + 's'
    w = two(b); return two(a) + ' ' + (w[:-1] + 'ies' if w.endswith('y') else w + 's')
UNIT = r'(?:km|m|cm|mm|kg|g|mg|mi|miles?|feet|ft|meters?|metres?|kilometers?|people|years?|days?|hours?|degrees?|calories|words|units|hz|mph|percent|%)\b'
PAT = re.compile(r'(?<![\d$.,/-])(1[1-9]\d\d|20\d\d)(s?)(?![\d])(?![.,]\d)(?!\s*' + UNIT + ')', re.I)
def years(text):
    return PAT.sub(lambda m: decade(int(m[1])) if m[2] else year(int(m[1])), text)
if __name__ == '__main__':
    for t in sys.argv[1:]: print(years(t))
