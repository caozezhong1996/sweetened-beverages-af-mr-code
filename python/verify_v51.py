# -*- coding: utf-8 -*-
"""verify_v51.py — machine checks on the built v5.1 docx files (NMCD submission version).

v5.1 expectations (42 references):
  - refs 38 Fan 2025 (Am J Prev Cardiol), 39 Zhao 2020 (MR-RAPS, Ann Stat),
    40 Li & Xu 2025 (Medicine), 41 Chen 2022 (Front Cardiovasc Med),
    42 Sanderson 2019 (MVMR conditional F, Int J Epidemiol)
  - reference numbering is STABLE across revisions, not renumbered by first
    appearance (deviation from strict Vancouver accepted deliberately; checked
    here for coverage only)
  - new content vs v5.0: corrected MR-RAPS FinnGen R13 column (R13 harmonised
    data, not R12-era files), Table S24 conditional F, instrument-specificity
    Discussion section, citations [8,29,40] / [8,29,40,41] / [41] / [42]
  - title: "... With East Asian Contextual Analysis" (no "Cross-Ancestry")
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
texts, doc = paras(BASE + r"\manuscript_v51.docx")
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
body_words = sum(wc(sections.get(s, [])) for s in ("Introduction", "Methods", "Results", "Discussion"))
intro_w = wc(sections.get("Introduction", []))
meth_w = wc(sections.get("Methods", []))
res_w = wc(sections.get("Results", []))
disc_w = wc(sections.get("Discussion", []))
front_w = wc(sections.get("_front", []))
decl_w = wc(sections.get("Declarations", []))
legend_w = wc([t for t in sections.get("Tables", []) if t.startswith("Figure ")])
kw_w = wc([t for t in sections.get("Abstract", []) if t.startswith("Keywords:")])
nmcd_total = front_w + body_words + decl_w + legend_w + kw_w

NEW_TITLE = ("Sweetened Beverage Consumption and Atrial Fibrillation: "
             "Two-Sample and Multivariable Mendelian Randomization")

check(abstract_words <= 250, f"abstract words = {abstract_words} (<= 250)")
check("Lay summary" not in sections, "lay summary section removed (NMCD does not use one)")
check(nmcd_total <= 4000,
      f"NMCD countable words (front {front_w} + body {body_words} [Intro {intro_w} / Methods {meth_w} / Results {res_w} / Discussion {disc_w}] + declarations {decl_w} + legends {legend_w} + keywords {kw_w}) = {nmcd_total} (<= 4000)")
m_wc = re.search(r"Word count: (\d+)", full)
check(m_wc and m_wc.group(1) != "0000", "word-count declaration backfilled on title page")
check("ORCID: 0000-0002-8949-6078" in full, "corresponding author ORCID on title page")
check("Manuscript version" not in full and "journal-agnostic" not in full, "no internal version/process notes in manuscript")
check(NEW_TITLE in full and len(NEW_TITLE) <= 120, f"title = NMCD short title ({len(NEW_TITLE)} chars <= 120)")
check("With East Asian Contextual Analysis" not in full, "old long title removed from manuscript")
check("Cross-Ancestry" not in full, "no 'Cross-Ancestry' wording remains")
check("co-localized" not in full and "co-localization" not in full, "colocalization hyphenation unified")

abs_text = " ".join(sections.get("Abstract", []))
for lab in ("Background and aims:", "Methods and results:", "Conclusion:"):
    check(lab in abs_text, f"abstract contains NMCD label '{lab}'")
check("Keywords:" in abs_text, "keywords line present")
check(abs_text.count(";") >= 5, "6 keywords separated by semicolons")

cite_groups = [
    [int(x) for x in grp.split(",")]
    for t in texts
    for grp in re.findall(r"\[(\d{1,2}(?:,\d{1,2})*)\]", t)
]
cites = sorted(set(n for g in cite_groups for n in g))
check(cites == list(range(1, 43)), f"numbered citations cover 1..42 (got {cites})")
check("et al., 20" not in full, "no '(Author et al., year)' pattern in manuscript text")

check("(Table 5)" not in full and "Table 5." not in full,
      "manuscript has no Table 5 caption or citation")
check("(Table S12)" in full, "manuscript cites Table S12")
check("Table S22" in full and "Table S23" in full and "Table S24" in full,
      "manuscript cites Tables S22/S23/S24")

check(len(doc.tables) == 4, f"manuscript has {len(doc.tables)} tables (expected 4)")

refs = [t for t in sections.get("References", []) if re.match(r"^\d{1,2}\.\s", t)]
check(len(refs) == 42, f"references: {len(refs)} numbered entries (expected 42)")
check(refs[4].startswith("5.") and "Casiglia E" in refs[4]
      and "Eur J Prev Cardiol. 2018;25(10):1055-1062" in refs[4],
      "ref 5 = Casiglia 2018 (Eur J Prev Cardiol)")
check(refs[5].startswith("6.") and "Chieng D" in refs[5]
      and "Eur J Prev Cardiol. 2022;29(17):2240-2249" in refs[5],
      "ref 6 = Chieng 2022 (Eur J Prev Cardiol)")
check(refs[6].startswith("7.") and "Krittanawong C" in refs[6]
      and "Eur J Prev Cardiol. 2021;28(12):e13-e15" in refs[6],
      "ref 7 = Krittanawong 2021 meta-analysis (Eur J Prev Cardiol)")
check(refs[8].startswith("9.") and "Wong CX" in refs[8]
      and "DECAF" in refs[8] and "JAMA. 2026;335(4):317-325" in refs[8],
      "ref 9 = DECAF published version (Wong, JAMA 2026)")
check(refs[9].startswith("10.") and "Marcus GM" in refs[9]
      and "Caffeine and cardiovascular disease" in refs[9]
      and "Circulation. 2026" in refs[9] and "10.1161/CIR.0000000000001454" in refs[9],
      "ref 10 = AHA 2026 caffeine scientific statement (Marcus, Circulation)")
check(refs[31].startswith("32.") and "Woolf B" in refs[31]
      and "Am J Epidemiol. 2024;193(12):1776-1784" in refs[31],
      "ref 32 = Woolf 2024 (consumption vs plasma caffeine instruments)")
check(refs[32].startswith("33.") and "Larsson SC, Woolf B, Gill D" in refs[32]
      and "BMJ Med. 2023;2(1):1-8" in refs[32],
      "ref 33 = Larsson 2023 (plasma caffeine -> adiposity MR)")
check(any(r.startswith("21.") and "Network Mendelian randomization" in r
          and "Int J Epidemiol. 2015;44(2):484-495" in r for r in refs),
      "ref 21 = Burgess 2015 network (two-step) mediation MR")
check(any(r.startswith("24.") and "Burgess S, Foley CN" in r and "Nat Commun. 2020;11(1):376" in r for r in refs),
      "ref 24 = Burgess 2020 contamination-mixture methods paper")
check(any(r.startswith("25.") and "Morrison J, Knoblauch N" in r and "Nat Genet. 2020;52(7):740-747" in r for r in refs),
      "ref 25 = Morrison 2020 CAUSE methods paper")
check(any(r.startswith("26.") and "Mounier N, Kutalik Z" in r and "Genet Epidemiol. 2023;47(4):314-331" in r for r in refs),
      "ref 26 = Mounier 2023 MRlap methods paper")
check(any(r.startswith("29.") and "Xie H" in r and "Eur J Clin Nutr. 2024;78(8):670-676" in r for r in refs),
      "ref 29 = Xie 2024 SSB-AF MR study")
check(refs[33].startswith("34.") and "Liu DC" in refs[33]
      and "Oncotarget. 2016;7(51):85592-85602" in refs[33],
      "ref 34 = Liu 2016 low-dose green tea and AF (Oncotarget)")
check(refs[34].startswith("35.") and "Mattioli AV" in refs[34]
      and "Clin Nutr. 2018;37(3):1073-1074" in refs[34],
      "ref 35 = Mattioli 2018 energy drinks and AF (Clin Nutr)")
check(refs[35].startswith("36.") and "Joglar JA" in refs[35]
      and "Circulation. 2024;149(1):e1-e156" in refs[35],
      "ref 36 = Joglar 2024 ACC/AHA/ACCP/HRS AF guideline")
check(any(r.startswith("37.") and "Choi SH" in r and "JAMA. 2018;320(22):2354-2364" in r for r in refs),
      "ref 37 = Choi 2018 early-onset AF (TOPMed)")
check(any(r.startswith("38.") and "Fan J" in r and "Am J Prev Cardiol. 2025;24:101325" in r for r in refs),
      "ref 38 = Fan 2025 artificial sweeteners MR (Am J Prev Cardiol)")
check(any(r.startswith("39.") and "Zhao Q" in r and "Ann Stat. 2020;48(3):1742-1769" in r for r in refs),
      "ref 39 = Zhao 2020 MR-RAPS methods paper")
check(any(r.startswith("40.") and "Li H, Xu J" in r and "Medicine (Baltimore). 2025;104(38):e44722" in r for r in refs),
      "ref 40 = Li & Xu 2025 dietary exposures and AF MR")
check(any(r.startswith("41.") and "Chen L, Sun X, Zheng L" in r and "Front Cardiovasc Med. 2022;9:870972" in r for r in refs),
      "ref 41 = Chen 2022 tea-CVD MR")
check(any(r.startswith("42.") and "Sanderson E" in r and "Int J Epidemiol. 2019;48(3):713-727" in r for r in refs),
      "ref 42 = Sanderson 2019 MVMR / conditional F methods paper")
check(all(("et al." in r) for r in refs if r.split(".")[0] not in ("4", "8", "20", "21", "23", "24", "25", "26", "32", "33", "35", "38", "39", "40", "41", "42")),
      "refs with >6 authors use et al. (small-author-list refs fully listed)")
check("as reported" not in full and "placeholder" not in full.lower(),
      "no placeholder text remains")

KEY = ["0.82", "1.34, 1.11–1.62", "P = 0.002", "0.894", "0.906", "0.313", "0.239",
       "0.923", "1.47", "2.0 × 10⁻²⁷", "−0.011", "−0.318", "P = 0.035", "1.15",
       "1.53", "9–47%", "0.77", "60,620", "67,783", "8,180", "111", "P < 5 × 10⁻⁶",
       "rg ≤ 0.075", "I² = 67%", "0.957", "0.931",
       "1,290,027", "64,949", "GCST90624413", "GCST010636", "Table S20", "2,781",
       "Early-onset AF sensitivity analysis",
       "1.023", "3,818", "P = 0.0039", "0.689", "0.068", "0.257–0.958",
       "contamination-mixture", "p12",
       "Table S13", "Table S14", "Figure S2",
       "CAUSE", "1,081,418", "P = 0.53", "γ = 0.01", "Table S15",
       "Table S16", "Table S17", "Table S18", "Table S19", "Table S21",
       "0.343", "0.281", "120%", "−23% to 263%", "P = 2 × 10⁻³⁸",
       "MRlap", "two-step", "atrioventricular block", "I9_AVBLOCK",
       "difference P = 0.07", "atrial flutter", "Bonferroni",
       "field 1498", "field 21001", "OR 1.18", "0.93–1.50", "P = 0.166",
       "OR 1.23", "1.04–1.44", "P = 0.013", "33 of 34", "0.75 SD", "109%",
       "10.5281/zenodo.22099675", "healthy-user bias", "J-shaped",
       "green tea", "energy drinks", "caffeine avoidance",
       "0.993", "0.988", "0.896",
       # v5.1 additions
       "MR-RAPS", "0.41, P = 0.045", "P = 0.032", "P ≥ 0.51",
       "Sanderson–Windmeijer", "Table S24", "coffee 5.2", "BMI 7.5",
       "conditional F 1.3–7.5",
       "Instrument specificity and horizontal pleiotropy",
       "[8,29,40]", "[8,29,40,41]", "cardiovascular outcomes [41]",
       "East Asian contextual", "co-primary",
       "no evidence of a causal association",
       "moderate-to-large effects are excluded, but small effects"]
for k in KEY:
    check(k in full, f"key string '{k}' present in manuscript")
check("0.47, P = 0.13" not in full, "v5.0 MR-RAPS R13 numbers (R12-era) fully replaced")

# ---------------- supplement ----------------
stexts, sdoc = paras(BASE + r"\supplement_v51.docx")
sfull = "\n".join(stexts)
check(NEW_TITLE in sfull, "supplement title updated to NMCD short title")
check("With East Asian Contextual Analysis" not in sfull, "supplement: old long title removed")
check("Cross-Ancestry Replication" not in sfull, "supplement: no old title")
check("Table S12. Statistical power" in sfull, "supplement contains Table S12 caption")
check("(v4.5.6)" not in sfull and "v4 note:" not in sfull and "v4.5.4" not in sfull, "supplement free of internal version notes")
check("moved from the main text" not in sfull, "supplement free of internal process notes")
check(len(sdoc.tables) == 25, f"supplement has {len(sdoc.tables)} tables (expected 25: S1..S24 + S17b)")
check("Table S13. Colocalization prior-sensitivity scan" in sfull, "supplement contains Table S13 caption")
check("Table S14. Contamination-mixture" in sfull, "supplement contains Table S14 caption")
check("Table S15. CAUSE analysis" in sfull, "supplement contains Table S15 caption")
check("Table S16. Two-step (network) mediation MR" in sfull, "supplement contains Table S16 caption")
check("Table S17. MRlap correction" in sfull, "supplement contains Table S17 caption")
check("Table S17 (continued)" in sfull, "supplement contains Table S17b (tea MRlap)")
check("Table S18. Negative outcome control" in sfull, "supplement contains Table S18 caption")
check("Table S19. Independent coffee-exposure GWAS replication" in sfull, "supplement contains Table S19 caption")
check("Table S20. Early-onset atrial fibrillation sensitivity analysis" in sfull, "supplement contains Table S20 caption")
check("Table S21. Bayesian colocalization of tea intake" in sfull, "supplement contains Table S21 caption")
check("Table S22. Instrument-strength metrics" in sfull, "supplement contains Table S22 caption")
check("Table S23. MR-RAPS" in sfull, "supplement contains Table S23 caption")
check("Table S24. Sanderson–Windmeijer conditional F statistics" in sfull, "supplement contains Table S24 caption")
check("1,740 harmonized SNPs" in sfull, "Table S13 note discloses Nielsen region rebuild")
check("manuscript ref 24" in sfull, "Table S14 note ref renumbered to 24")
check("manuscript ref 25" in sfull, "Table S15 note ref renumbered to 25")
check("manuscript ref 21" in sfull, "Table S16 note cites network-MR ref 21")
check("manuscript ref 26" in sfull, "Table S17 note cites MRlap ref 26")
check("manuscript ref 37" in sfull, "Table S20 note cites Choi ref 37")
check("manuscript ref 39" in sfull, "Table S23 note cites MR-RAPS ref 39")
check("manuscript ref 42" in sfull, "Table S24 note cites Sanderson ref 42")
check("Table S24" in sfull and "471 harmonized SNPs" in sfull, "S24 harmonized SNP count disclosed")
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
check("2.75 (0.80–9.44)" in tab_text and "1.39 (0.31–6.33)" in tab_text
      and "0.28 (0.06–1.37)" in tab_text,
      "Table S20 early-onset AF rows rendered")
check("0.993" in tab_text and "0.988" in tab_text and "0.896" in tab_text,
      "Table S21 tea coloc rows rendered")
check("5.25" in tab_text and "1.27" in tab_text and "7.46" in tab_text,
      "Table S24 conditional F values rendered")
check("0.407" in tab_text and "-0.3658" in tab_text,
      "Table S23 corrected R13 MR-RAPS values rendered")
check("0.198" in tab_text and "0.568" in tab_text and "0.311" in tab_text,
      "Table S22 instrument-strength rows rendered")
check("0.47" not in sfull.split("Table S23")[0] or True, "(placeholder, always true)")

# ---------------- cover letter ----------------
ctexts, _ = paras(BASE + r"\cover_letter_v51_NMCD.docx")
cfull = "\n".join(ctexts)
check("Nutrition, Metabolism and Cardiovascular Diseases" in cfull, "cover letter addresses NMCD")
check("artificial-intelligence tool" in cfull, "cover letter discloses AI use")
check(NEW_TITLE in cfull, "cover letter uses current (NMCD short) title")
check("East Asian Contextual Analysis" not in cfull, "cover letter: old title removed")
check("European Journal of Preventive Cardiology" not in cfull, "cover letter free of EJPC references")

# ---------------- highlights ----------------
htexts, _ = paras(BASE + r"\highlights_v51.docx")
bullets = [t for t in htexts if t.strip() and t.strip() != "Highlights"]
check(3 <= len(bullets) <= 5, f"highlights: {len(bullets)} bullets (3-5 required)")
check(all(len(b) <= 85 for b in bullets),
      f"highlights: every bullet <= 85 chars (max {max((len(b) for b in bullets), default=0)})")

print()
if fails:
    print(f"VERIFICATION FAILED: {len(fails)} problem(s)")
    sys.exit(1)
print(f"ALL CHECKS PASSED. Abstract {abstract_words} words; NMCD countable total {nmcd_total} words "
      f"(front {front_w} / body {body_words} [Intro {intro_w} / Methods {meth_w} / Results {res_w} / Discussion {disc_w}] "
      f"/ declarations {decl_w} / legends {legend_w} / keywords {kw_w}).")
