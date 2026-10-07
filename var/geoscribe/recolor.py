"""Swap Postiz's hard-coded brand purples for the GeoScribe palette.

Run from the repo root. Safe to run again after an upstream merge: colours
already converted are left alone, new purple ones are converted.
"""
import collections
import os
import re

MAP = {
    # primary
    '612bd3': 'd00314', '612ad5': 'd00314', '662fda': 'd00314', '622aff': 'd00314',
    '6112ff': 'd00314', '622ff6': 'd00314',
    # darker (hover / pressed)
    '5520cb': 'a80210', '5720cb': 'a80210', '5023b8': 'a80210', '5826c2': 'a80210',
    '4500e7': 'a80210', '2a008d': '5c0109',
    # brighter
    '7236f1': 'ff2a3a', '7950f2': 'ff2a3a', '7b3ff2': 'ff2a3a', '7c3aff': 'ff2a3a',
    '7640e0': 'ff2a3a', '8155dd': 'e23a2f', '832ad5': 'e23a2f', '8b5cf6': 'e23a2f',
    # light tints
    '8c66ff': 'ff7065', '9162ff': 'ff7065', '9d6eff': 'ff7065', 'a78bfa': 'ff7065',
    'b69dec': 'ff7065', 'c4b5fd': 'ffb3ad', 'dacbfb': 'ffd2ce', 'e7ddfe': 'fde8e6',
    # secondary accent (pink -> cyan), also mentions and hashtags in previews
    'fc69ff': '22b8e0', 'ae8afc': '22b8e0',
    # notification dot, AI accent
    'ff3ea2': 'd00314', 'd82d7e': 'a855f7',
    # plain dark greys hard-coded on the sign-up and approval screens -> warm greys
    '0e0e0e': '0d0c0a', '0b0a0a': '0a0908', '121212': '141310', '1a1919': '161512',
    '1e1d1d': '1d1b17', '1e1e1e': '1d1b17', '1f1f1f': '1d1b17', '232222': '24221d',
    '2a2929': '2a2823', '2b2a2a': '2a2823', '2b2b2b': '2a2823', '2c2b2b': '2a2823',
    '3a3939': '3a3730',
}
HEX = re.compile(rb'#(' + b'|'.join(k.encode() for k in MAP) + rb')\b', re.I)
RGB = re.compile(rb'97,\s?43,\s?211')
# stock Tailwind purple classes (glows on the onboarding buttons, the admin banner)
PALETTE = [
    (b'shadow-purple-500', b'shadow-[#D00314]'),
    (b'bg-purple-700', b'bg-[#A80210]'),
    # the fade over the review carousel
    (b'rgba(14, 14, 14, 0)', b'rgba(13, 12, 10, 0)'),
    # the big number on the sign-up page: brand red, not the secondary cyan
    (b'text-[42px] text-[#22B8E0]', b'text-[42px] text-[#FF2A3A]'),
    (b'text-[42px] text-[#FC69FF]', b'text-[42px] text-[#FF2A3A]'),
]

ROOTS = ['apps/frontend/src', 'libraries/react-shared-libraries/src']
SKIP = {'colors.scss'}


def swap(match):
    old = match.group(1).decode()
    new = MAP[old.lower()]
    return b'#' + (new if old == old.lower() else new.upper()).encode()


changed = collections.Counter()
for root in ROOTS:
    for folder, _, names in os.walk(root):
        for name in names:
            if not name.endswith(('.tsx', '.ts', '.scss', '.css')) or name in SKIP:
                continue
            path = os.path.join(folder, name)
            with open(path, 'rb') as handle:
                before = handle.read()
            after, hex_hits = HEX.subn(swap, before)
            after, rgb_hits = RGB.subn(b'208, 3, 20', after)
            for old, new in PALETTE:
                rgb_hits += after.count(old)
                after = after.replace(old, new)
            if hex_hits or rgb_hits:
                with open(path, 'wb') as handle:
                    handle.write(after)
                changed[path] = hex_hits + rgb_hits

print(len(changed), 'files,', sum(changed.values()), 'replacements')
