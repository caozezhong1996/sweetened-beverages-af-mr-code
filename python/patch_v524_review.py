# -*- coding: utf-8 -*-
"""patch_v524_review.py — v5.2.4 changes from external 3-reviewer report (2026-10-18).

Adopted:
 R1-M1  abstract: weak-conditional-instrument qualifier on the BMI attenuation item
 R3-1   abstract: parallel structure in the "not robust" list (funded by abstract trims)
 R1-M2  Table S16 note: mediated proportion flagged "not estimable"
 R2-m1  intro: HR 3.51 flagged as interaction estimate (funded by body trims)
 R3-2   Discussion principal findings: fix "no exception" referent
 R3-4   "entails possible" -> "involves possible"
 R3-3   estimand sentence recast in active voice (partial adoption; full gloss declined, word ceiling)
 R3-5   "its weight remains an unsettled methodological debate" clarified
 R3-6   objective (iv) recast as methodological aim (net-zero)
 R3-7   Table 2 footnote heterogeneity phrasing (Tables section, outside body count)
Declined (documented in report): R2-m2 (ref 45 framing already in Discussion; word ceiling),
 R1-M3/M4 (already disclosed), R3-8 ("likewise" not present in highlights_v51.docx), full estimand gloss.
"""
import io
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
MS = os.path.join(BASE, "build_manuscript_v51_JAHA.js")
SU = os.path.join(BASE, "build_supplement_v51_JAHA.js")

PATCHES = [
    # A1+R3-1 abstract
    (MS,
     "was not robust: null weighted-median estimates, source-dependent outlier robustness, attenuation after body-mass-index adjustment (OR 0.82; P = 0.099) and colocalization only at the adiposity locus FTO.",
     "was not robust: weighted-median estimates were null, outlier robustness was source-dependent, the estimate attenuated in multivariable models with weak conditional instruments (OR 0.82; P = 0.099), and colocalization was confined to the adiposity locus FTO."),
    # abstract trims funding A1
    (MS,
     "Null genetic estimates converge with randomized acute and recurrence evidence.",
     "Null genetic estimates converge with randomized trial evidence."),
    (MS,
     "multivariable MR, locus-level colocalization and cross-trait LD-score regression.",
     "multivariable MR, colocalization and LD-score regression."),
    (MS,
     "AFGen 2018 (sensitivity) and BioBank Japan (East Asian context).",
     "AFGen 2018 and BioBank Japan (East Asian context)."),
    (MS,
     "Plasma caffeine and paraxanthine instruments were likewise unassociated with AF (P ≥ 0.31).",
     "Plasma caffeine and paraxanthine instruments were unassociated with AF (P ≥ 0.31)."),
    # R2-m1 intro interaction flag
    (MS,
     "with the highest risk (HR 3.51) among participants with high genetic susceptibility and high ASB intake [2].",
     "with the highest risk (HR 3.51, an interaction estimate) among participants with high genetic susceptibility and high ASB intake [2]."),
    # body trims funding R2-m1
    (MS,
     "These studies are observational, however;",
     "These studies are observational;"),
    (MS,
     "warrant cautious interpretation.",
     "warrant caution."),
    (MS,
     "The present data themselves illustrate",
     "The present data illustrate"),
    # R3-2 referent fix
    (MS,
     "and the positive association for coffee intake, although nominally significant after Benjamini–Hochberg correction (meta-analytic OR 1.34; P = 0.002), was no exception.",
     "and the positive association for coffee intake also failed scrutiny despite nominal significance after Benjamini–Hochberg correction (meta-analytic OR 1.34; P = 0.002)."),
    # R3-4
    (MS,
     "which additionally entails possible sugar–caffeine interaction",
     "which additionally involves possible sugar–caffeine interaction"),
    # R3-3 partial (active voice)
    (MS,
     "and an acute per-serving character that lies outside a per-category lifelong estimand.",
     "and an acute per-serving character that a per-category lifelong estimand does not capture."),
    # R3-5
    (MS,
     "its weight remains an unsettled methodological debate [43]",
     "how much this matters remains methodologically debated [43]"),
    # R3-6
    (MS,
     "and (iv) to benchmark sensitivity with alcohol as a positive control.",
     "and (iv) to verify pipeline sensitivity against the alcohol positive control."),
    # R3-7 table footnote
    (MS,
     "was negligible for all exposures except sugar added to tea (I² = 0–3% versus I² = 67%);",
     "was negligible for all exposures (I² = 0–3%) except sugar added to tea (I² = 67%);"),
    # R1-M2 supplement S16 note
    (SU,
     "indicates that the nominal total association is statistically explained by the adiposity pathway.",
     "indicates that the nominal total association is statistically explained by the adiposity pathway. The mediated proportion itself is not estimable with precision and is reported for completeness."),
]

for path, old, new in PATCHES:
    with io.open(path, encoding="utf-8") as f:
        content = f.read()
    n = content.count(old)
    if n != 1:
        print("FAIL  %s: pattern found %d times (expected 1)\n      %r" % (os.path.basename(path), n, old[:90]))
        sys.exit(1)
    with io.open(path, "w", encoding="utf-8", newline="") as f:
        f.write(content.replace(old, new))
    print("OK    %s: %r..." % (os.path.basename(path), old[:55]))

print("All patches applied.")
