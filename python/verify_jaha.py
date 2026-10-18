# -*- coding: utf-8 -*-
"""verify_jaha.py — machine checks on manuscript_v51_JAHA.docx / supplement_v51_JAHA.docx."""
import re
import sys
from docx import Document

BASE = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\06_升级分析_v4"
fails = []


def check(cond, msg):
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        fails.append(msg)


texts = [p.text for p in Document(BASE + r"\manuscript_v52_JAHA.docx").paragraphs]
full = "\n".join(texts)
sections = {}
cur = "_front"
for t in texts:
    if t in ("Abstract", "Lay summary", "Nonstandard Abbreviations and Acronyms",
             "Clinical Perspective", "Introduction", "Methods", "Results",
             "Tables", "Discussion", "Declarations", "References"):
        cur = t
        sections.setdefault(cur, [])
        continue
    sections.setdefault(cur, []).append(t)

wc = lambda ls: sum(len(x.split()) for x in ls if x.strip())
abs_w = wc(sections.get("Abstract", []))
body = sum(wc(sections.get(s, [])) for s in ("Introduction", "Methods", "Results", "Discussion"))

check("With East Asian Contextual Analysis" in full, "full v5.1 title retained")
check(abs_w <= 250, f"abstract words = {abs_w} (<= 250)")
abs_text = " ".join(sections.get("Abstract", []))
for lab in ("Background:", "Methods and Results:", "Conclusions:"):
    check(lab in abs_text, f"abstract label '{lab}'")
check("Keywords:" in abs_text, "keywords line present")
check("Lay summary" not in sections, "no lay summary")
check(len(sections.get("Nonstandard Abbreviations and Acronyms", [])) >= 1, "NAA section present")
cp = sections.get("Clinical Perspective", [])
check(any("What Is New?" == t for t in cp) and any("What Are the Clinical Implications?" == t for t in cp),
      "Clinical Perspective with both AHA subheads")
check(body <= 6000, f"body words = {body} (<= ~6000) "
      f"(I {wc(sections.get('Introduction',[]))} / M {wc(sections.get('Methods',[]))} / "
      f"R {wc(sections.get('Results',[]))} / D {wc(sections.get('Discussion',[]))})")
check("Sources of Funding: None." in full, "Sources of Funding (JAHA label)")
check("Disclosures: The authors declare no conflicts of interest." in full, "Disclosures (JAHA label)")
check("ORCID: 0000-0002-8949-6078" in full, "ORCID on title page")

cites = sorted(set(int(x) for t in texts
                   for grp in re.findall(r"\[(\d{1,2}(?:,\d{1,2})*)\]", t)
                   for x in grp.split(",")))
check(cites == list(range(1, 47)), f"numbered citations cover 1..46 (got {cites})")

refs = [t for t in sections.get("References", []) if re.match(r"^\d{1,2}\.\s", t)]
check(len(refs) == 46, f"references: {len(refs)} numbered entries")

KEY = ["0.82", "1.34, 1.11–1.62", "P = 0.002", "0.894", "0.906", "0.313", "0.239",
       "0.923", "1.47", "2.0 × 10⁻²⁷", "−0.011", "−0.318", "P = 0.035", "1.15",
       "1.53", "9–47%", "0.77", "60,620", "67,783", "8,180", "111", "P < 5 × 10⁻⁶",
       "rg ≤ 0.075", "I² = 67%", "0.957", "0.931", "1,290,027", "64,949",
       "GCST90624413", "GCST010636", "Table S20", "2,781", "1.023", "3,818",
       "P = 0.0039", "0.689", "0.068", "0.257–0.958", "contamination-mixture",
       "p12", "Table S13", "Table S14", "Figure S2", "CAUSE", "1,081,418",
       "P = 0.53", "γ = 0.01", "Table S15", "Table S16", "Table S17", "Table S18",
       "Table S19", "Table S21", "0.343", "0.281", "120%", "−23% to 263%",
       "P = 2 × 10⁻³⁸", "MRlap", "two-step", "atrioventricular block",
       "I9_AVBLOCK", "difference P = 0.07", "atrial flutter", "Bonferroni",
       "field 1498", "field 21001", "OR 1.18", "0.93–1.50", "P = 0.166",
       "OR 1.23", "1.04–1.44", "P = 0.013", "33 of 34", "0.75 SD", "109%",
       "10.5281/zenodo.22099675", "healthy-user bias", "J-shaped", "green tea",
       "energy drinks", "caffeine avoidance", "0.993", "0.988", "0.896",
       "MR-RAPS", "0.41, P = 0.045", "P = 0.032", "P ≥ 0.51",
       "Sanderson–Windmeijer", "Table S24", "coffee 5.2", "BMI 7.5",
       "conditional F 1.3–7.5", "Instrument specificity and horizontal pleiotropy",
       "[8,29,40]", "[8,29,40,41]", "cardiovascular outcomes [41]",
       "East Asian contextual", "co-primary", "no evidence of a causal association",
       "moderate-to-large effects are excluded, but small effects",
       "Table S25", "GTF2I", "CYP2A6", "rs56113850", "GCST90200436",
       "0.99 (0.92–1.07; P = 0.85)", "0.98 (0.93–1.02; P = 0.31)",
       "0.84, 0.72–0.98; P = 0.029", "Wald-ratio estimation", "P ≥ 0.31",
       "minimum detectable odds ratios were 1.07–1.25",
       "SSB-attributable cardiovascular burden", "independent multi-locus instruments",
       "AF included [33]", "e035978", "39% fewer AF recurrences",
       "Evidence now converges across three independent designs",
       "as recently reviewed [46]", "Null genetic estimates converge"]
missing = [k for k in KEY if k not in full]
check(not missing, f"all {len(KEY)} key strings present (missing: {missing[:5]})")
check("0.47, P = 0.13" not in full, "v5.0 MR-RAPS R13 numbers fully replaced")

sfull = "\n".join(p.text for p in Document(BASE + r"\supplement_v52_JAHA.docx").paragraphs)
check("With East Asian Contextual Analysis" in sfull, "supplement keeps long title")
check("Table S24" in sfull and "Table S23. MR-RAPS" in sfull and "Table S22. Instrument-strength" in sfull and "Table S25" in sfull,
      "supplement contains S22/S23/S24/S25")

print()
if fails:
    print(f"VERIFICATION FAILED: {len(fails)} problem(s)")
    sys.exit(1)
print(f"ALL JAHA CHECKS PASSED. Abstract {abs_w} words; body {body} words.")
