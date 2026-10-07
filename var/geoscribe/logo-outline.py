"""Turn the wordmark "GeoScribe Social" into outlines (Inter) and write the
final logo files for the At Pin mark.

Usage (from the repo root):
  python outline.py <pylibs dir> <font cache dir> <output dir>
"""
import glob
import os
import sys

sys.path.insert(0, sys.argv[1])

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

FONT_DIR, OUT = sys.argv[2], sys.argv[3]

RED = '#D00314'
MARK = (
    '<g fill="none" stroke="{c}" stroke-width="7.5" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M56 28V42A9.35 9.35 0 0 0 74.7 42A27 27 0 1 0 25.09 52.29L48 89L60.83 68.44"/>'
    '<circle cx="46.5" cy="38" r="9.5"/></g>'
)


def find_inter():
    """The dev server caches Inter as several subset files; pick the upright Latin one."""
    for path in sorted(glob.glob(os.path.join(FONT_DIR, '*.woff2'))):
        font = TTFont(path)
        names = {record.toUnicode() for record in font['name'].names if record.nameID in (1, 4, 16)}
        if not any('Inter' in name for name in names):
            continue
        cmap = font.getBestCmap()
        upright = font['post'].italicAngle == 0
        if upright and all(ord(ch) in cmap for ch in 'GeoScribeSocial') and 'fvar' in font:
            return path
    raise SystemExit('no upright Latin Inter file found in ' + FONT_DIR)


def outline(source, weight, text, size, x, baseline, tracking):
    font = TTFont(source)
    axes = {axis.axisTag: axis.defaultValue for axis in font['fvar'].axes}
    axes['wght'] = weight
    font = instancer.instantiateVariableFont(font, axes)
    glyphs = font.getGlyphSet()
    cmap = font.getBestCmap()
    scale = size / font['head'].unitsPerEm
    paths = []
    for ch in text:
        name = cmap[ord(ch)]
        pen = SVGPathPen(glyphs, ntos=lambda v: ('%.2f' % v).rstrip('0').rstrip('.'))
        glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, baseline)))
        paths.append(pen.getCommands())
        x += glyphs[name].width * scale + tracking * size
    return ''.join(paths), x - tracking * size


def lockup(source, word, accent):
    size, baseline, tracking = 52.6, 67.1, -0.035
    start = 96.0
    geo, end = outline(source, 700, 'GeoScribe', size, start, baseline, tracking)
    social, end = outline(source, 500, 'Social', size, end + 12.6, baseline, tracking)
    width = round(end + 3 - 14, 1)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="14 2 {width} 92" fill="none">\n'
        f'  <title>GeoScribe Social</title>\n'
        f'  {MARK.format(c=RED)}\n'
        f'  <path fill="{word}" d="{geo}"/>\n'
        f'  <path fill="{accent}" d="{social}"/>\n'
        f'</svg>\n'
    )


source = find_inter()
print('font:', os.path.basename(source))
os.makedirs(OUT, exist_ok=True)

files = {
    'geoscribe-social-mark.svg': (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" fill="none">\n'
        '  <title>GeoScribe Social</title>\n'
        f'  {MARK.format(c=RED)}\n'
        '</svg>\n'
    ),
    'geoscribe-social-mark-white.svg': (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" fill="none">\n'
        '  <title>GeoScribe Social</title>\n'
        f'  {MARK.format(c="#FFFFFF")}\n'
        '</svg>\n'
    ),
    # App icon: white mark, drawn a little heavier so it holds up at tab size.
    'geoscribe-social-icon.svg': (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" fill="none">\n'
        '  <title>GeoScribe Social</title>\n'
        f'  <rect width="96" height="96" rx="22" fill="{RED}"/>\n'
        '  <g transform="translate(9.6 10.6) scale(0.8)" fill="none" stroke="#FFFFFF" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M56 28V42A9.35 9.35 0 0 0 74.7 42A27 27 0 1 0 25.09 52.29L48 89L60.83 68.44"/>'
        '<circle cx="46.5" cy="38" r="9.5"/></g>\n'
        '</svg>\n'
    ),
    'geoscribe-social-logo.svg': lockup(source, '#1A1915', '#C0291F'),
    'geoscribe-social-logo-dark.svg': lockup(source, '#F0EDE6', '#FF7065'),
}
for name, content in files.items():
    with open(os.path.join(OUT, name), 'w', encoding='utf-8', newline='\n') as handle:
        handle.write(content)
    print('wrote', name, len(content), 'bytes')
