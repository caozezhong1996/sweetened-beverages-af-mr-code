# -*- coding: utf-8 -*-
"""patch_v523_spelling.py — v5.2.3 US spelling unification (JAHA = AHA journal).

1:1 word swaps only; word counts unchanged; no KEY string is affected.
Each (file, old, new, expected_count) is asserted exactly.
"""
import io
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
MS = os.path.join(BASE, "build_manuscript_v51_JAHA.js")
CL = os.path.join(BASE, "build_cover_letter_v51_JAHA.js")
SU = os.path.join(BASE, "build_supplement_v51_JAHA.js")

RULES = [
    # manuscript
    (MS, "behaviour", "behavior", 11),      # incl. behavioural -> behavioral
    (MS, "analysed", "analyzed", 7),
    (MS, "modelled", "modeled", 4),
    (MS, "towards", "toward", 4),
    (MS, "centred", "centered", 2),
    (MS, "harbour", "harbor", 2),           # harbouring -> harboring
    (MS, "aetiolog", "etiolog", 2),         # aetiology -> etiology
    (MS, "ischaemic", "ischemic", 1),
    (MS, "ageing", "aging", 1),
    (MS, "millilitre", "milliliter", 1),
    (MS, "colour", "color", 1),
    # cover letter
    (CL, "behaviour", "behavior", 2),
    (CL, "analysed", "analyzed", 1),
    # supplement
    (SU, "behaviour", "behavior", 3),
    (SU, "harbour", "harbor", 1),
    (SU, "modelled", "modeled", 1),
    (SU, "centred", "centered", 1),
    (SU, "towards", "toward", 1),
]

for path, old, new, want in RULES:
    with io.open(path, encoding="utf-8") as f:
        content = f.read()
    n = content.count(old)
    if n != want:
        print("FAIL  %s: %r found %d times (expected %d)" % (os.path.basename(path), old, n, want))
        sys.exit(1)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content.replace(old, new))
    print("OK    %-36s %-12s -> %-12s x%d" % (os.path.basename(path), old, new, n))

print("All spelling rules applied.")
