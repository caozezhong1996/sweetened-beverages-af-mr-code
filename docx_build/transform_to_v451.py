# -*- coding: utf-8 -*-
"""
transform_to_v451.py — v4.5 -> v4.5.1  (v2, auto-remap)

Robust pipeline:
  1. Insert new manuscript content with ⟦CONMIX⟧ / ⟦XIE⟧ placeholder citations
     (anchors use ORIGINAL v4.5 citation numbers).
  2. Scan the whole JS source for citation tokens (old numbers + placeholders)
     and assign NEW Vancouver numbers strictly by order of first appearance.
  3. Renumber the references array programmatically in that order, adding the
     two new entries (Burgess 2020 conmix; Xie 2024).
  4. Supplement: Tables S13 (prior scan) & S14 (conmix), contents note, version bump.

Every replacement is asserted; the computed old->new mapping is printed so that
verify_v45.py and the revision note can be updated to match.
"""
import re
import shutil
import sys
from pathlib import Path

BUILD = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本")
RESULTS = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\06_升级分析_v4\results")
TBL = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\06_升级分析_v4\supplement_tables")

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


# ================= MANUSCRIPT =================
src = (BUILD / "build_manuscript_v45.js").read_text(encoding="utf-8")

# ---- parse old references (before any edit) ----
old_refs = dict(
    (int(n), t) for n, t in re.findall(r"T`(\d+)\. ([^`]+)`", src)
)
if not check(sorted(old_refs) == list(range(1, 23)),
             f"parsed {len(old_refs)} old refs (expected 1..22)"):
    sys.exit(1)
print(f"  ok: parsed {len(old_refs)} v4.5 references")

NEW_REFS = {
    "CONMIX": "Burgess S, Foley CN, Allara E, Staley JR, Howson JMM. A robust and efficient method for Mendelian randomization with hundreds of genetic variants. Nat Commun. 2020;11(1):376.",
    "XIE": "Xie H, Liu Y, Gu X, Liu S, Fang Y, Zhong W, et al. Association between sugar-sweetened beverages and pure fruit juice with risk of six cardiovascular diseases: a Mendelian randomization study. Eur J Clin Nutr. 2024;78(8):670-676.",
}

# ---- 1. content insertions (anchors carry ORIGINAL v4.5 numbers) ----
src = sub_once(
    src,
    "high consumers of SSBs or ASBs [1,2].",
    "high consumers of SSBs or ASBs [1,2]. A previous smaller MR study of SSB and pure-fruit-juice intake reported a positive causal association between SSBs and AF (OR 1.023, 1.007–1.038; P = 0.0039) ⟦XIE⟧. That analysis used an AF outcome GWAS with 3,818 cases—approximately one-sixteenth the size of our primary source—selected instruments at a relaxed threshold (P < 10⁻⁵) and did not model adiposity; the reported effect is far smaller than the observational hazard ratios and lies well within the confidence bounds of our estimates, and our weighted-median, multivariable and colocalization analyses argue against a causal interpretation of a signal of this size.",
    "Xie 2024 divergence discussion",
)
src = sub_once(
    src,
    "radial IVW regression (modified second-order weights) served as an additional heterogeneity-robust estimator,",
    "radial IVW regression (modified second-order weights) and the contamination-mixture estimator ⟦CONMIX⟧ (which remains consistent when only a subset of instruments is valid) served as additional robust estimators,",
    "Methods: conmix estimator mention",
)
src = sub_once(
    src,
    "with PP.H4 (shared causal variant) > 0.8 considered evidence of colocalization and PP.H1 indicating a coffee-specific signal with no AF counterpart.`,",
    "with PP.H4 (shared causal variant) > 0.8 considered evidence of colocalization and PP.H1 indicating a coffee-specific signal with no AF counterpart; prior sensitivity was assessed by varying the colocalization prior p12 from 10⁻⁶ to 5 × 10⁻⁵.`,",
    "Methods: coloc prior scan",
)
src = sub_once(
    src,
    "so a small genuine effect cannot be formally excluded.`,",
    "so a small genuine effect cannot be formally excluded. The contamination-mixture estimator gave the same source-dependent pattern—null in Nielsen 2018 (β = 0.068, −0.136 to 0.564; P = 0.45) but positive in FinnGen R13 (β = 0.689, 0.257–0.958; P = 0.001; Table S14).`,",
    "Results: conmix sentence",
)
src = sub_once(
    src,
    "genetic proxies of coffee intake acting through caffeine-handling pathways have no detectable effect on AF.`,",
    "genetic proxies of coffee intake acting through caffeine-handling pathways have no detectable effect on AF. The shared-variant conclusion at FTO was robust to the colocalization prior: PP.H4 exceeded 0.8 for p12 ≥ 5 × 10⁻⁶ in both outcome sources and weakened only under the most stringent prior tested (p12 = 10⁻⁶; PP.H4 = 0.46–0.49; Table S13).`,",
    "Results: coloc prior-scan sentence",
)
src = sub_once(
    src,
    "shared genetic architecture between beverage intake and AF (Table S10; Table S11).",
    "shared genetic architecture between beverage intake and AF (Table S10; Table S11; Figure S2).",
    "Results: Figure S2 reference",
)
src = sub_once(
    src,
    "(file: FigureS1_LOO_Funnel_v43_300dpi.png).`])",
    "(file: FigureS1_LOO_Funnel_v43_300dpi.png).`]),\n  mix([T`Figure S2. Forest plot of cross-trait LDSC genetic correlations (rg) between beverage intake and atrial fibrillation, with same-trait and overlap validation controls (file: FigureS2_LDSC_rg_v45_300dpi.png).`])",
    "Figure legends: add Figure S2",
)
src = sub_once(
    src,
    "Manuscript version: v4.5 — formatted for the European Journal of Preventive Cardiology (structured abstract, numbered references, six display items; Table 5 moved to Table S12); primary AF outcome Nielsen 2018; alcohol positive lifestyle control; cross-trait LDSC (24 August 2026)",
    "Manuscript version: v4.5.1 — EJPC format plus reviewer-driven additions: references renumbered by order of first appearance; Xie 2024 divergence addressed; colocalization prior-sensitivity scan (Table S13); contamination-mixture estimator (Table S14); LDSC rg forest plot (Figure S2) (24 August 2026)",
    "version note v4.5.1",
)
src = sub_once(
    src,
    "Sweetened beverages and atrial fibrillation — MR manuscript (v4.5, EJPC format)",
    "Sweetened beverages and atrial fibrillation — MR manuscript (v4.5.1, EJPC format)",
    "page header v4.5.1",
)
if fails:
    print("\nMANUSCRIPT v4.5.1 ABORTED (insertions):", len(fails), "failure(s)")
    sys.exit(1)

# ---- 2. auto-remap citations by first appearance ----
tok_pat = re.compile(
    r"(?<![A-Za-z0-9_\)\]])\[(\d{1,2}(?:,\d{1,2})*)\]|⟦(CONMIX|XIE)⟧"
)
order = []
tokens_raw = []
for m in tok_pat.finditer(src):
    if m.group(2):
        tokens_raw.append((m, [m.group(2)]))
    else:
        tokens_raw.append((m, [int(x) for x in m.group(1).split(",")]))
    for t in tokens_raw[-1][1]:
        if t not in order:
            order.append(t)

expected = set(range(1, 23)) | {"CONMIX", "XIE"}
check(set(order) == expected,
      f"token set mismatch: {sorted(set(order), key=str)} vs 1..22+CONMIX+XIE")
check(len(order) == 24, f"{len(order)} distinct tokens (expected 24)")
if fails:
    print("\nMANUSCRIPT v4.5.1 ABORTED (scan):", len(fails), "failure(s)")
    sys.exit(1)

new_num = {t: i + 1 for i, t in enumerate(order)}
print("  old/token -> new:", {str(k): v for k, v in new_num.items()})


def remap(m):
    if m.group(2):
        return f"[{new_num[m.group(2)]}]"
    return "[" + ",".join(str(new_num[int(x)]) for x in m.group(1).split(",")) + "]"


src = tok_pat.sub(remap, src)
check("⟦" not in src and "⟧" not in src, "placeholder(s) left after remap")

# verify monotonic first appearance of new numbers
groups = [
    [int(x) for x in m.group(1).split(",")]
    for m in re.finditer(r"(?<![A-Za-z0-9_\)\]])\[(\d{1,2}(?:,\d{1,2})*)\]", src)
]
flat = [n for g in groups for n in g]
check(sorted(set(flat)) == list(range(1, 25)),
      f"post-remap citation set = {sorted(set(flat))}")
firsts = {}
for i, g in enumerate(groups):
    for n in g:
        firsts.setdefault(n, i)
seq = [n for n, _ in sorted(firsts.items(), key=lambda kv: kv[1])]
check(seq == list(range(1, 25)),
      f"first-appearance order not monotonic after remap: {seq}")
print(f"  ok: renumbered {len(groups)} citation groups; first appearance monotonic 1..24")

# ---- 3. rebuild references array in new order ----
lines = []
for tok in order:
    n = new_num[tok]
    body = NEW_REFS[tok] if isinstance(tok, str) else old_refs[tok]
    lines.append(f"    T`{n}. {body}`,")
REFS_BLOCK = "  ...[\n" + "\n".join(lines) + "\n  ].map"
pat_refs = re.compile(r"  \.\.\.\[\n[\s\S]*?\n  \]\.map")
m = pat_refs.findall(src)
check(len(m) == 1, f"refs array matched {len(m)}")
src = pat_refs.sub(lambda _: REFS_BLOCK, src, count=1)
print("  ok: references array rebuilt (24 entries, Vancouver by appearance)")

if fails:
    print("\nMANUSCRIPT v4.5.1 ABORTED:", len(fails), "failure(s)")
    sys.exit(1)
(BUILD / "build_manuscript_v45.js").write_text(src, encoding="utf-8")
print("written: build_manuscript_v45.js (v4.5.1)")

n_conmix = new_num["CONMIX"]
n_xie = new_num["XIE"]
n_decaf = new_num[5]
print(f"  key numbers: CONMIX=[{n_conmix}]  XIE=[{n_xie}]  DECAF(old5)=[{n_decaf}]")

# ================= SUPPLEMENT =================
fails = []
shutil.copy(RESULTS / "coloc_priorscan_v45.tsv", TBL / "S13_coloc_priorscan.tsv")
shutil.copy(RESULTS / "conmix_coffee_v45.tsv", TBL / "S14_conmix.tsv")
print("  ok: TSVs staged into supplement_tables")

sup = (BUILD / "build_supplement_v45.js").read_text(encoding="utf-8")
sup = sub_once(
    sup,
    'const T5 = readTsv(path.join(DIR, "T5_power.tsv"));\n',
    'const T5 = readTsv(path.join(DIR, "T5_power.tsv"));\nconst T13 = readTsv(path.join(DIR, "S13_coloc_priorscan.tsv"));\nconst T14 = readTsv(path.join(DIR, "S14_conmix.tsv"));\n',
    "supplement: import S13/S14 TSVs",
)
n = sup.count("(v4.5)")
if check(n == 2, f"supplement '(v4.5)' x{n} (expected 2)"):
    sup = sup.replace("(v4.5)", "(v4.5.1)")
    print("  ok: supplement version strings -> v4.5.1")
sup = sub_once(
    sup,
    'main-text citations of the power analysis now refer to Table S12."',
    'main-text citations of the power analysis now refer to Table S12. v4.5.1 note (reviewer-driven additions): Table S13 reports a colocalization prior-sensitivity (p12) scan at the FTO locus; Table S14 reports contamination-mixture estimates for the nominal coffee signal; Figure S2 (separate PNG) plots the LDSC genetic correlations; and the main-text discussion now addresses the smaller SSB–AF MR study of Xie et al. 2024."',
    "supplement: v4.5.1 contents note",
)
S_BLOCKS = f"""children.push(caption("Table S13. Colocalization prior-sensitivity scan at the FTO locus (coffee intake vs atrial fibrillation): posterior probabilities as the coloc.abf prior p12 is varied"));
children.push(makeTable([1400, 1700, 1100, 1000, 1400, 1400, 1400], T13.header, T13.rows, 18));
children.push(note("The coloc.abf default prior is p12 = 10⁻⁵. The shared-causal-variant conclusion at FTO held for p12 ≥ 5 × 10⁻⁶ in both outcome sources (PP.H4 ≥ 0.81) and weakened only under the most stringent prior (p12 = 10⁻⁶; PP.H4 = 0.46–0.49), which a priori disfavours colocalization; higher priors increased PP.H4 to ≥ 0.95. The Nielsen 2018 region dataset was rebuilt from the local full summary statistics for this scan (1,740 harmonized SNPs; PP.H4 = 0.894 at the default prior, exactly reproducing the primary analysis). Prior scans at CYP1A1–CYP1A2 and AHR were not repeated: those loci supported a coffee-specific signal (PP.H1 ≥ 0.93), a conclusion driven by the absence of an AF association and insensitive to p12, and their caffeine-pathway instruments were additionally null in subgroup MR (Table S4)."));

children.push(caption("Table S14. Contamination-mixture (conmix) estimates for the nominal coffee–atrial fibrillation signal"));
children.push(makeTable(
  [3400, 1100, 2700, 1300],
  ["Analysis", "No. SNPs", "conmix estimate, beta (95% CI)", "P value"],
  T14.rows.map((r) => [r[0], r[1], `${{r[2]}} (${{r[3]}} to ${{r[4]}})`, r[5]]), 18));
children.push(note("The contamination-mixture estimator (Burgess et al., 2020; manuscript ref {n_conmix}) remains consistent when only a subset of instruments is valid. Estimates mirror the source-dependent robustness pattern seen in the weighted-median and MR-PRESSO analyses: null in Nielsen 2018 but positive in FinnGen R13, so the nominal coffee signal cannot be credibly interpreted as causal, although a small genuine effect cannot be excluded."));

const doc = new Document({{"""
sup = sub_once(sup, "const doc = new Document({", S_BLOCKS, "supplement: add Tables S13/S14")

if fails:
    print("\nSUPPLEMENT v4.5.1 ABORTED:", len(fails), "failure(s)")
    sys.exit(1)
(BUILD / "build_supplement_v45.js").write_text(sup, encoding="utf-8")
print("written: build_supplement_v45.js (v4.5.1)")
print("\nALL v4.5.1 TRANSFORMS COMPLETED")
print("OLD->NEW:", {str(k): v for k, v in sorted(new_num.items(), key=lambda kv: kv[1])})
