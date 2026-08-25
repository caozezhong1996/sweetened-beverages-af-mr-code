# -*- coding: utf-8 -*-
"""trim_v453_words2.py — second round of word-budget trims (5146 -> ~5090)."""
import sys
from pathlib import Path

BUILD = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本")
fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)
        print("FAIL:", msg)
    return cond


def sub_once(text, old, new, label):
    n = text.count(old)
    if not check(n == 1, f"{label}: anchor x{n}"):
        return text
    print("  ok:", label)
    return text.replace(old, new, 1)


src = (BUILD / "build_manuscript_v45.js").read_text(encoding="utf-8")

src = sub_once(src,
    "Against atrioventricular block (FinnGen R13 I9_AVBLOCK; Table S18), six of nine exposure tests were null (P ≥ 0.53); nominal associations for alcohol intake frequency (P = 0.043) and coffee intake (P = 0.042) did not survive Bonferroni correction, whereas the inverse association for sugar added to tea (P = 0.001) did. Both beverage estimates mirrored their AF associations in direction and magnitude, as expected if they track the shared adiposity-mediated pathway (Limitations).",
    "Against atrioventricular block (Table S18), six of nine exposure tests were null (P ≥ 0.53); nominal associations for alcohol intake frequency (P = 0.043) and coffee intake (P = 0.042) did not survive Bonferroni correction, whereas the inverse association for sugar added to tea (P = 0.001) did. Both beverage estimates mirrored their AF associations, as expected under the shared adiposity-mediated pathway (Limitations).",
    "Results negative control: shorten further")

src = sub_once(src,
    "Three deviations are reported transparently: the revision-stage mediation probe just described; locus-level colocalization was performed at the three loci harbouring the strongest coffee instruments as a mechanistic probe of the sole nominal signal;",
    "Three deviations are reported transparently: the revision-stage mediation probe; locus-level colocalization at the three loci harbouring the strongest coffee instruments;",
    "Methods deviations: shorten")

src = sub_once(src,
    "Two-step mediation MR quantified this pathway: the BMI-mediated indirect effect statistically accounted for the entire nominal coffee association (Table S16).",
    "Two-step mediation MR quantified this pathway: the BMI-mediated indirect effect accounted for the entire nominal coffee association (Table S16).",
    "Discussion mechanisms: tighten")

src = sub_once(src,
    "coffee intake increased BMI (β = 0.82 kg/m² per intake category; P = 0.007), BMI increased AF (β = 0.343 log OR per kg/m²; P = 2 × 10⁻³⁸), and the BMI-mediated indirect effect (0.281, SE 0.106) statistically accounted for the entire total association",
    "coffee intake increased BMI (β = 0.82 kg/m²; P = 0.007), BMI increased AF (β = 0.343 per kg/m²; P = 2 × 10⁻³⁸), and the BMI-mediated indirect effect (0.281, SE 0.106) accounted for the entire total association",
    "Results mediation: tighten")

src = sub_once(src,
    "Because the instruments derive from European-ancestry GWAS, these estimates are interpreted as supportive context rather than independent evidence.",
    "Given European-ancestry instruments, these estimates are supportive context rather than independent evidence.",
    "East Asian: tighten")

src = sub_once(src,
    "Genome-wide genetic correlation told a consistent story (coffee–AF rg ≤ 0.075, not surviving correction).",
    "Genome-wide genetic correlation was consistent (coffee–AF rg ≤ 0.075, not surviving correction).",
    "Discussion coffee: tighten")

src = sub_once(src,
    "European meta-analyses are fixed-effect combinations of Nielsen 2018 and FinnGen release R13; AFGen 2018 shares cohorts with Nielsen 2018 and is shown as a sensitivity source; the earlier FinnGen R5 freeze is subsumed by R13 and is not reported.",
    "European meta-analyses are fixed-effect combinations of Nielsen 2018 and FinnGen release R13; AFGen 2018 shares cohorts with Nielsen 2018 and is shown as a sensitivity source; FinnGen R5 is subsumed by R13.",
    "Table 2 footnote: tighten")

src = sub_once(src,
    "Identical instrument lists were used across outcome sources, so estimates differ only in the outcome data queried.",
    "Identical instrument lists were used across outcome sources.",
    "Methods instruments: tighten")

if fails:
    print("\nTRIM2 ABORTED:", len(fails), "failure(s)")
    sys.exit(1)
(BUILD / "build_manuscript_v45.js").write_text(src, encoding="utf-8")
print("written: build_manuscript_v45.js (round-2 trims applied)")
