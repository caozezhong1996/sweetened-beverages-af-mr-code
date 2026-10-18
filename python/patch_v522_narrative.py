# -*- coding: utf-8 -*-
"""patch_v522_narrative.py — v5.2.2 narrative patch.

1) Correct DECAF description (39% fewer AF recurrences; JAMA 2026).
2) Discussion coffee paragraph: three-design convergence narrative + new ref [46].
3) Abstract: one convergence sentence.
4) Reference list: add [46] Dewland TA, van Dam RM, Marcus GM. Eur Heart J 2025.
5) Cover letter: explicit quantified workload sentence.
6) verify_jaha.py: citation range 1..46, refs == 46, new KEY strings.

Each (file, old, new) must match exactly once.
"""
import io
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
VERIFY = os.path.join(ROOT, "06_升级分析_v4", "scripts", "verify_jaha.py")

PATCHES = [
    # --- manuscript: abstract ---
    (os.path.join(BASE, "build_manuscript_v51_JAHA.js"),
     "Plasma caffeine and paraxanthine instruments were likewise unassociated with AF (P ≥ 0.31).`",
     "Plasma caffeine and paraxanthine instruments were likewise unassociated with AF (P ≥ 0.31). Null genetic estimates converge with randomized acute and recurrence evidence.`"),

    # --- manuscript: introduction, DECAF correction ---
    (os.path.join(BASE, "build_manuscript_v51_JAHA.js"),
     "and the randomized DECAF trial [9] found that daily caffeinated coffee did not increase AF recurrence.",
     "and the randomized DECAF trial found 39% fewer AF recurrences with daily caffeinated coffee than with abstinence [9]."),

    # --- manuscript: discussion coffee paragraph, convergence sentence + rebalance ---
    (os.path.join(BASE, "build_manuscript_v51_JAHA.js"),
     "observational, acute-exposure randomized and recent genetic evidence points to no harm [4,9,30,31], although healthy-user bias may colour inverse estimates [10].",
     "observational and genetic evidence points to no harm [4,31], although healthy-user bias may colour inverse estimates [10]. Evidence now converges across three independent designs: susceptibility (genetic nulls here and previously [8,33,44]), acute triggering (day-long randomized exposure showed no atrial arrhythmia excess [30]) and recurrence (39% lower hazard with randomized caffeinated coffee [9]), as recently reviewed [46]."),

    (os.path.join(BASE, "build_manuscript_v51_JAHA.js"),
     "and was source-dependent—null after outlier correction in Nielsen 2018 but retained in FinnGen R13—a divergence consistent with residual heterogeneity rather than a stable causal signal.",
     "and source-dependent after outlier correction."),

    (os.path.join(BASE, "build_manuscript_v51_JAHA.js"),
     "reinforcing that the adiposity pathway captured here reflects",
     "reinforcing that the adiposity pathway here reflects"),

    (os.path.join(BASE, "build_manuscript_v51_JAHA.js"),
     "This reading aligns with the 2026 American Heart Association statement [10], which left caffeine-metabolism effect modification unresolved;",
     "The 2026 American Heart Association statement left caffeine-metabolism effect modification unresolved [10];"),

    # --- manuscript: discussion penultimate paragraph trims ---
    (os.path.join(BASE, "build_manuscript_v51_JAHA.js"),
     "At the trigger level, randomized acute coffee exposure found no excess of atrial arrhythmias [30], although case reports link high-dose energy drinks to acute AF in young, low-risk individuals [35].",
     "Case reports link high-dose energy drinks to acute AF in young, low-risk individuals [35]."),

    (os.path.join(BASE, "build_manuscript_v51_JAHA.js"),
     "This conclusion is not a verdict of safety:",
     "This is no verdict of safety:"),

    # --- manuscript: reference 46 ---
    (os.path.join(BASE, "build_manuscript_v51_JAHA.js"),
     "e035978.`,\n  ].map((text)",
     "e035978.`,\n    T`46. Dewland TA, van Dam RM, Marcus GM. Coffee and cardiovascular disease. Eur Heart J. 2025;46(36):3546-3554.`,\n  ].map((text)"),

    # --- cover letter: quantified workload ---
    (os.path.join(BASE, "build_cover_letter_v51_JAHA.js"),
     "field directly. The work was strengthened",
     "field directly. In total, the analysis spans ten exposures (seven behavioural beverage phenotypes and three plasma metabolites) plus cis estimation, four outcome sources including an overlap-free co-primary and an East Asian contextual arm, twenty-five supplementary tables, and fully archived code and harmonized datasets—a workload that distinguishes this study from its single-exposure predecessors. The work was strengthened"),

    # --- verify script ---
    (VERIFY,
     'range(1, 46)), f"numbered citations cover 1..45',
     'range(1, 47)), f"numbered citations cover 1..46'),
    (VERIFY,
     'check(len(refs) == 45, f"references: {len(refs)} numbered entries")',
     'check(len(refs) == 46, f"references: {len(refs)} numbered entries")'),
    (VERIFY,
     '"AF included [33]", "e035978"]',
     '"AF included [33]", "e035978", "39% fewer AF recurrences",\n       "Evidence now converges across three independent designs",\n       "as recently reviewed [46]", "Null genetic estimates converge"]'),
]

for path, old, new in PATCHES:
    with io.open(path, encoding="utf-8") as f:
        content = f.read()
    n = content.count(old)
    if n != 1:
        print("FAIL  %s: pattern found %d times (expected 1)\n      %r" % (os.path.basename(path), n, old[:80]))
        sys.exit(1)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content.replace(old, new))
    print("OK    %s: %r..." % (os.path.basename(path), old[:60]))

print("All patches applied.")
