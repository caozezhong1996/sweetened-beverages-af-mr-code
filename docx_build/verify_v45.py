# -*- coding: utf-8 -*-
"""verify_v45.py — machine checks on the built v4.5.6 docx files against EJPC rules.

v4.5.6 expectations:
  - 28 numbered references, cited strictly in order of first appearance
  - ref 6 = DECAF (Wong, JAMA 2026); ref 7 = AHA 2026 caffeine scientific
    statement (Marcus, Circulation); ref 18 = Burgess 2015 network MR;
    ref 21 = Burgess 2020 conmix; ref 22 = Morrison 2020 CAUSE;
    ref 23 = Mounier 2023 MRlap; ref 26 = Xie 2024
  - new content: two-step mediation MR (Table S16; proportion ~120%),
    MRlap correction (Table S17; difference P = 0.07),
    AV-block negative outcome control (Table S18), flutter-pooling limitation
  - supplement has 19 tables (S1..S19), version v4.5.5, ref notes renumbered
"""
import re
import sys
from docx import Document

BASE = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\06_升级分析_v4"
fails = []


def check(cond, msg):
    print(("PASS  " if cond else "FAIL  ") + msg)
    if not cond:
        fails.append(msg)


def paras(path):
    doc = Document(path)
    return [p.text for p in doc.paragraphs], doc


# ---------------- manuscript ----------------
texts, doc = paras(BASE + r"\manuscript_v45.docx")
full = "\n".join(texts)

sections = {}
current = "_front"
for t in texts:
    if t in ("Abstract", "Lay summary", "Introduction", "Methods", "Results",
             "Tables", "Discussion", "Declarations", "References"):
        current = t
        sections.setdefault(current, [])
        continue
    sections.setdefault(current, []).append(t)


def wc(lines):
    return sum(len(x.split()) for x in lines if x.strip())


abstract_words = wc(sections.get("Abstract", []))
lay_words = wc(sections.get("Lay summary", []))
body_words = sum(wc(sections.get(s, [])) for s in ("Introduction", "Methods", "Results", "Discussion"))
intro_w = wc(sections.get("Introduction", []))
meth_w = wc(sections.get("Methods", []))
res_w = wc(sections.get("Results", []))
disc_w = wc(sections.get("Discussion", []))

check(abstract_words <= 250, f"abstract words = {abstract_words} (EJPC <= 250)")
check(lay_words <= 250, f"lay summary words = {lay_words} (<= 250)")
check(body_words <= 5100, f"body words (Intro {intro_w} + Methods {meth_w} + Results {res_w} + Discussion {disc_w}) = {body_words} (target ~5000)")
check("Manuscript version: v4.5.6" in full, "manuscript version string v4.5.6")

abs_text = " ".join(sections.get("Abstract", []))
for lab in ("Aim:", "Methods:", "Results:", "Conclusions:"):
    check(lab in abs_text, f"abstract contains '{lab}'")
check("Keywords:" in abs_text, "keywords line present")
check(abs_text.count(";") >= 5, "6 keywords separated by semicolons")

cite_groups = [
    [int(x) for x in grp.split(",")]
    for t in texts
    for grp in re.findall(r"\[(\d{1,2}(?:,\d{1,2})*)\]", t)
]
cites = sorted(set(n for g in cite_groups for n in g))
check(cites == list(range(1, 29)), f"numbered citations cover 1..28 (got {cites})")
check("et al., 20" not in full, "no '(Author et al., year)' pattern in manuscript text")

firsts = {}
for i, g in enumerate(cite_groups):
    for n in g:
        firsts.setdefault(n, i)
seq = [n for n, _ in sorted(firsts.items(), key=lambda kv: kv[1])]
check(seq == list(range(1, 29)),
      f"citations appear in Vancouver order in the docx (first-appearance sequence = {seq})")

check("(Table 5)" not in full and "Table 5." not in full,
      "manuscript has no Table 5 caption or citation")
check("(Table S12)" in full, "manuscript cites Table S12")

check(len(doc.tables) == 4, f"manuscript has {len(doc.tables)} tables (expected 4; +2 figures = 6 display items)")

refs = [t for t in sections.get("References", []) if re.match(r"^\d{1,2}\.\s", t)]
check(len(refs) == 28, f"references: {len(refs)} numbered entries (expected 28)")
check(len(refs) >= 6 and refs[5].startswith("6.") and "Wong CX" in refs[5]
      and "DECAF" in refs[5] and "JAMA. 2026;335(4):317-325" in refs[5],
      "ref 6 = DECAF published version (Wong, JAMA 2026)")
check(len(refs) >= 7 and refs[6].startswith("7.") and "Marcus GM" in refs[6]
      and "Caffeine and cardiovascular disease" in refs[6]
      and "Circulation. 2026" in refs[6] and "10.1161/CIR.0000000000001454" in refs[6],
      "ref 7 = AHA 2026 caffeine scientific statement (Marcus, Circulation)")
check(any(r.startswith("18.") and "Network Mendelian randomization" in r
          and "Int J Epidemiol. 2015;44(2):484-495" in r for r in refs),
      "ref 18 = Burgess 2015 network (two-step) mediation MR")
check(any(r.startswith("21.") and "Burgess S, Foley CN" in r and "Nat Commun. 2020;11(1):376" in r for r in refs),
      "ref 21 = Burgess 2020 contamination-mixture methods paper")
check(any(r.startswith("22.") and "Morrison J, Knoblauch N" in r and "Nat Genet. 2020;52(7):740-747" in r for r in refs),
      "ref 22 = Morrison 2020 CAUSE methods paper")
check(any(r.startswith("23.") and "Mounier N, Kutalik Z" in r and "Genet Epidemiol. 2023;47(4):314-331" in r for r in refs),
      "ref 23 = Mounier 2023 MRlap methods paper")
check(any(r.startswith("26.") and "Xie H" in r and "Eur J Clin Nutr. 2024;78(8):670-676" in r for r in refs),
      "ref 26 = Xie 2024 SSB-AF MR study")
check(all(("et al." in r) for r in refs if r.split(".")[0] not in ("4", "5", "17", "18", "20", "21", "22", "23")),
      "refs with >6 authors use et al. (refs 4/5/17/18/20/21/22/23 have <=6 authors, all listed)")
check("as reported" not in full and "placeholder" not in full.lower(),
      "no DECAF placeholder text remains")

KEY = ["0.82", "1.34, 1.11–1.62", "P = 0.002", "0.894", "0.906", "0.313", "0.239",
       "0.923", "1.47", "2.0 × 10⁻²⁷", "−0.011", "−0.318", "P = 0.035", "1.15",
       "1.53", "9–47%", "0.77", "60,620", "67,783", "8,180", "111", "P < 5 × 10⁻⁶",
       "rg ≤ 0.075", "I² = 67%", "0.957", "0.931",
       "1,290,027", "64,949", "GCST90624413",
       "1.023", "3,818", "P = 0.0039", "0.689", "0.068", "0.257–0.958",
       "contamination-mixture", "p12", "0.46–0.49",
       "Table S13", "Table S14", "Figure S2",
       "CAUSE", "1,081,418", "P = 0.53", "γ = 0.01", "Table S15",
       "Table S16", "Table S17", "Table S18", "Table S19",
       "0.343", "0.281", "120%", "−23% to 263%", "P = 2 × 10⁻³⁸",
       "MRlap", "two-step", "atrioventricular block", "I9_AVBLOCK",
       "difference P = 0.07", "atrial flutter", "Bonferroni",
       "field 1498", "field 21001", "OR 1.18", "0.93–1.50", "P = 0.166",
       "OR 1.23", "1.04–1.44", "P = 0.013", "33 of 34", "0.75 SD", "109%"]
for k in KEY:
    check(k in full, f"key string '{k}' present in manuscript")

# ---------------- supplement ----------------
stexts, sdoc = paras(BASE + r"\supplement_v45.docx")
sfull = "\n".join(stexts)
check("Table S12. Statistical power" in sfull, "supplement contains Table S12 caption")
check("(v4.5.5)" in sfull, "supplement version string v4.5.5")
check("moved from the main text" in sfull, "supplement notes Table S12 provenance")
check(len(sdoc.tables) == 19, f"supplement has {len(sdoc.tables)} tables (expected S1..S19 = 19)")
check("Table S13. Colocalization prior-sensitivity scan" in sfull, "supplement contains Table S13 caption")
check("Table S14. Contamination-mixture" in sfull, "supplement contains Table S14 caption")
check("Table S15. CAUSE analysis" in sfull, "supplement contains Table S15 caption")
check("Table S16. Two-step (network) mediation MR" in sfull, "supplement contains Table S16 caption")
check("Table S17. MRlap correction" in sfull, "supplement contains Table S17 caption")
check("Table S18. Negative outcome control" in sfull, "supplement contains Table S18 caption")
check("1,740 harmonized SNPs" in sfull, "Table S13 note discloses Nielsen region rebuild")
check("manuscript ref 21" in sfull, "Table S14 note ref renumbered to 21")
check("manuscript ref 22" in sfull, "Table S15 note ref renumbered to 22")
check("manuscript ref 18" in sfull, "Table S16 note cites network-MR ref 18")
check("manuscript ref 23" in sfull, "Table S17 note cites MRlap ref 23")
tab_text = "\n".join(c.text for t in sdoc.tables for row in t.rows for c in row.cells)
check("0.894" in tab_text and "0.906" in tab_text and "0.457" in tab_text and "10⁻⁵" in tab_text,
      "Table S13 PP.H4 values rendered with formatting")
check("0.068 (-0.136 to 0.564)" in tab_text and "0.449" in tab_text,
      "Table S14 conmix Nielsen row rendered")
check("0.689 (0.257 to 0.958)" in tab_text and "9.6 × 10⁻⁴" in tab_text,
      "Table S14 conmix R13 row rendered")
check("0.8202" in tab_text and "0.3428" in tab_text and "1.198" in tab_text and "2.2e-38" in tab_text,
      "Table S16 mediation rows rendered")
check("0.0279" in tab_text and "0.0371" in tab_text and "-0.0104" in tab_text,
      "Table S17 MRlap rows rendered")
check("+0.4800" in tab_text and "-0.6759" in tab_text and "0.0012" in tab_text,
      "Table S18 AV-block rows rendered")
check("3.5873" in tab_text and "0.7473" in tab_text and "1.091" in tab_text,
      "Table S16 Neale 21001 sensitivity rows rendered")
check("0.1682" in tab_text and "0.2042" in tab_text and "1.23 (1.04-1.44)" in tab_text
      and "0.013" in tab_text,
      "Table S19 replication and meta-analysis rows rendered")
check("Table S19. Independent coffee-exposure GWAS replication" in sfull,
      "supplement contains Table S19 caption")

# ---------------- cover letter ----------------
ctexts, _ = paras(BASE + r"\cover_letter_v45.docx")
cfull = "\n".join(ctexts)
check("European Journal of Preventive Cardiology" in cfull, "cover letter addresses EJPC")
check("artificial-intelligence tool" in cfull, "cover letter discloses AI use")

print()
if fails:
    print(f"VERIFICATION FAILED: {len(fails)} problem(s)")
    sys.exit(1)
print(f"ALL CHECKS PASSED. Abstract {abstract_words} words; body {body_words} words "
      f"(Intro {intro_w} / Methods {meth_w} / Results {res_w} / Discussion {disc_w}); "
      f"lay summary {lay_words} words.")
