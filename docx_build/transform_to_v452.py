# -*- coding: utf-8 -*-
"""
transform_to_v452.py — v4.5.1 -> v4.5.2 (auto-remap, same machinery as v451)

Adds the genome-wide CAUSE analysis:
  1. Methods: CAUSE mention with ⟦CAUSE⟧ placeholder citation (new ref: Morrison 2020).
  2. Results: CAUSE sentence after the conmix sentence (Table S15).
  3. Discussion (Xie paragraph): extend method list to include CAUSE.
  4. Vancouver renumbering by first appearance (24 -> 25 refs).
  5. Supplement: Table S15, contents note, version strings.
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

old_refs = dict((int(n), t) for n, t in re.findall(r"T`(\d+)\. ([^`]+)`", src))
if not check(sorted(old_refs) == list(range(1, 25)),
             f"parsed {len(old_refs)} refs (expected 1..24)"):
    sys.exit(1)
print(f"  ok: parsed {len(old_refs)} v4.5.1 references")

NEW_REFS = {
    "CAUSE": "Morrison J, Knoblauch N, Marcus JH, Stephens M, He X. Mendelian randomization accounting for correlated and uncorrelated pleiotropic effects using genome-wide summary statistics. Nat Genet. 2020;52(7):740-747.",
}

# ---- 1. content insertions ----
src = sub_once(
    src,
    "served as additional robust estimators, and leave-one-out analysis",
    "served as additional robust estimators; genome-wide CAUSE analysis ⟦CAUSE⟧ distinguished correlated pleiotropy from causation while modelling sample overlap between the beverage and AF GWAS; and leave-one-out analysis",
    "Methods: CAUSE mention",
)
src = sub_once(
    src,
    "but positive in FinnGen R13 (β = 0.689, 0.257–0.958; P = 0.001; Table S14).`,",
    "but positive in FinnGen R13 (β = 0.689, 0.257–0.958; P = 0.001; Table S14). Genome-wide CAUSE analysis (1,081,418 shared variants) corroborated the null interpretation: a correlated-pleiotropy model explained the coffee–AF genetic overlap as well as a causal model (P = 0.53 for the causal-model improvement), with the posterior causal effect centred on zero (γ = 0.01, 95% CI −0.01 to 0.04; Table S15).`,",
    "Results: CAUSE sentence",
)
src = sub_once(
    src,
    "our weighted-median, multivariable and colocalization analyses argue against",
    "our weighted-median, multivariable, colocalization and CAUSE analyses argue against",
    "Discussion: extend method list with CAUSE",
)
src = sub_once(
    src,
    "Manuscript version: v4.5.1 — EJPC format plus reviewer-driven additions: references renumbered by order of first appearance; Xie 2024 divergence addressed; colocalization prior-sensitivity scan (Table S13); contamination-mixture estimator (Table S14); LDSC rg forest plot (Figure S2) (24 August 2026)",
    "Manuscript version: v4.5.2 — EJPC format plus reviewer-driven additions: references renumbered by order of first appearance; Xie 2024 divergence addressed; colocalization prior-sensitivity scan (Table S13); contamination-mixture estimator (Table S14); LDSC rg forest plot (Figure S2); genome-wide CAUSE analysis (Table S15) (24 August 2026)",
    "version note v4.5.2",
)
src = sub_once(
    src,
    "Sweetened beverages and atrial fibrillation — MR manuscript (v4.5.1, EJPC format)",
    "Sweetened beverages and atrial fibrillation — MR manuscript (v4.5.2, EJPC format)",
    "page header v4.5.2",
)
if fails:
    print("\nMANUSCRIPT v4.5.2 ABORTED (insertions):", len(fails), "failure(s)")
    sys.exit(1)

# ---- 2. auto-remap citations by first appearance ----
tok_pat = re.compile(r"(?<![A-Za-z0-9_\)\]])\[(\d{1,2}(?:,\d{1,2})*)\]|⟦(CAUSE)⟧")
order = []
for m in tok_pat.finditer(src):
    toks = [m.group(2)] if m.group(2) else [int(x) for x in m.group(1).split(",")]
    for t in toks:
        if t not in order:
            order.append(t)
expected = set(range(1, 25)) | {"CAUSE"}
check(set(order) == expected, f"token set mismatch: {sorted(set(order), key=str)}")
check(len(order) == 25, f"{len(order)} distinct tokens (expected 25)")
if fails:
    print("\nMANUSCRIPT v4.5.2 ABORTED (scan):", len(fails), "failure(s)")
    sys.exit(1)

new_num = {t: i + 1 for i, t in enumerate(order)}
print("  old/token -> new:", {str(k): v for k, v in new_num.items()})


def remap(m):
    if m.group(2):
        return f"[{new_num[m.group(2)]}]"
    return "[" + ",".join(str(new_num[int(x)]) for x in m.group(1).split(",")) + "]"


src = tok_pat.sub(remap, src)
check("⟦" not in src and "⟧" not in src, "placeholder(s) left after remap")

groups = [[int(x) for x in m.group(1).split(",")]
          for m in re.finditer(r"(?<![A-Za-z0-9_\)\]])\[(\d{1,2}(?:,\d{1,2})*)\]", src)]
flat = [n for g in groups for n in g]
check(sorted(set(flat)) == list(range(1, 26)), f"post-remap citation set = {sorted(set(flat))}")
firsts = {}
for i, g in enumerate(groups):
    for n in g:
        firsts.setdefault(n, i)
seq = [n for n, _ in sorted(firsts.items(), key=lambda kv: kv[1])]
check(seq == list(range(1, 26)), f"first-appearance not monotonic after remap: {seq}")
print(f"  ok: renumbered {len(groups)} citation groups; first appearance monotonic 1..25")

# ---- 3. rebuild references array ----
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
print("  ok: references array rebuilt (25 entries)")

if fails:
    print("\nMANUSCRIPT v4.5.2 ABORTED:", len(fails), "failure(s)")
    sys.exit(1)
(BUILD / "build_manuscript_v45.js").write_text(src, encoding="utf-8")
print("written: build_manuscript_v45.js (v4.5.2)")

n_cause = new_num["CAUSE"]
n_xie = new_num[22]
print(f"  key numbers: CAUSE=[{n_cause}]  XIE=[{n_xie}]")

# ================= SUPPLEMENT =================
fails = []
shutil.copy(RESULTS / "cause_s15_v46.tsv", TBL / "S15_cause.tsv")
print("  ok: S15 TSV staged")

sup = (BUILD / "build_supplement_v45.js").read_text(encoding="utf-8")
sup = sub_once(
    sup,
    'const T14 = readTsv(path.join(DIR, "S14_conmix.tsv"));\n',
    'const T14 = readTsv(path.join(DIR, "S14_conmix.tsv"));\nconst T15 = readTsv(path.join(DIR, "S15_cause.tsv"));\n',
    "supplement: import S15 TSV",
)
n = sup.count("(v4.5.1)")
if check(n == 2, f"supplement '(v4.5.1)' x{n} (expected 2)"):
    sup = sup.replace("(v4.5.1)", "(v4.5.2)")
    print("  ok: supplement version strings -> v4.5.2")
sup = sub_once(
    sup,
    'and the main-text discussion now addresses the smaller SSB–AF MR study of Xie et al. 2024."',
    'and the main-text discussion now addresses the smaller SSB–AF MR study of Xie et al. 2024. v4.5.2 note: Table S15 reports the genome-wide CAUSE analysis (causal versus correlated-pleiotropy model) for coffee intake and AF."',
    "supplement: v4.5.2 contents note",
)
S15_BLOCK = f"""children.push(caption("Table S15. CAUSE analysis of coffee intake and atrial fibrillation (Nielsen 2018): causal versus correlated-pleiotropy (sharing) model"));
children.push(makeTable(
  [5200, 4200],
  T15.header, T15.rows, 18));
children.push(note("CAUSE (Morrison et al., 2020; manuscript ref {n_cause}) compares a causal model with a correlated-pleiotropy (sharing) model using genome-wide summary statistics and explicitly models sample overlap (estimated rho ≈ 0.001). Both traits entered as Z-scores with unit standard errors (the same munged files used for the LDSC analysis, Tables S10–S11); gamma and eta are therefore in Z units and only their sign and precision are interpreted. The causal model did not fit significantly better than the sharing model (P = 0.534) and the posterior causal effect gamma was centred on zero, consistent with the weighted-median, contamination-mixture and colocalization analyses: the coffee–AF genetic overlap is adequately explained by correlated pleiotropy, including the adiposity-mediated component colocalizing at FTO (Tables S8 and S13)."));

const doc = new Document({{"""
sup = sub_once(sup, "const doc = new Document({", S15_BLOCK, "supplement: add Table S15")

if fails:
    print("\nSUPPLEMENT v4.5.2 ABORTED:", len(fails), "failure(s)")
    sys.exit(1)
(BUILD / "build_supplement_v45.js").write_text(sup, encoding="utf-8")
print("written: build_supplement_v45.js (v4.5.2)")
print("\nALL v4.5.2 TRANSFORMS COMPLETED")
print("OLD->NEW:", {str(k): v for k, v in sorted(new_num.items(), key=lambda kv: kv[1])})
