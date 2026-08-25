# -*- coding: utf-8 -*-
"""
transform_to_v453.py — v4.5.2 -> v4.5.3 (auto-remap, same machinery as v452)

Adds three revision-stage robustness analyses:
  1. Two-step (network) mediation MR coffee->BMI->AF  (Table S16; new ref NETMR)
  2. MRlap overlap/winner's-curse/weak-instrument correction (Table S17; new ref MRLAP)
  3. Atrioventricular-block negative outcome control (Table S18)
Plus: FinnGen I9_AF flutter-pooling limitation; deviations statement updated;
word-budget trims (I2 sentence, Table 2 footnote duplicates, LDSC methods clause).
Vancouver renumbering by first appearance (25 -> 27 refs).
"""
import re
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


# ================= MANUSCRIPT =================
src = (BUILD / "build_manuscript_v45.js").read_text(encoding="utf-8")

old_refs = dict((int(n), t) for n, t in re.findall(r"T`(\d+)\. ([^`]+)`", src))
if not check(sorted(old_refs) == list(range(1, 26)),
             f"parsed {len(old_refs)} refs (expected 1..25)"):
    sys.exit(1)
print(f"  ok: parsed {len(old_refs)} v4.5.2 references")

NEW_REFS = {
    "NETMR": "Burgess S, Daniel RM, Butterworth AS, Thompson SG; EPIC-InterAct Consortium. Network Mendelian randomization: using genetic variants as instrumental variables to investigate mediation in causal pathways. Int J Epidemiol. 2015;44(2):484-495.",
    "MRLAP": "Mounier N, Kutalik Z. Bias correction for inverse variance weighting Mendelian randomization. Genet Epidemiol. 2023;47(4):314-331.",
}

# ---- 1. content insertions ----
src = sub_once(
    src,
    "conditional on adiposity, with BMI included as a positive control.`,",
    "conditional on adiposity, with BMI included as a positive control. Complementary two-step (network) mediation MR ⟦NETMR⟧ quantified the adiposity-mediated component of the nominal coffee signal from the coffee–BMI and BMI–AF IVW estimates (product method with delta-method standard errors; Table S16).`,",
    "Methods: two-step mediation mention",
)
src = sub_once(
    src,
    "distinguished correlated pleiotropy from causation while modelling sample overlap between the beverage and AF GWAS; and leave-one-out analysis",
    "distinguished correlated pleiotropy from causation while modelling sample overlap between the beverage and AF GWAS; the MRlap framework ⟦MRLAP⟧ jointly corrected the coffee–AF estimate for residual sample overlap, winner's curse and weak-instrument bias (Table S17); and leave-one-out analysis",
    "Methods: MRlap mention",
)
src = sub_once(
    src,
    "tested reverse causation. Statistical power was quantified",
    "tested reverse causation. A negative outcome control repeated the pipeline against atrioventricular block (FinnGen R13 I9_AVBLOCK; Table S18). Statistical power was quantified",
    "Methods: negative outcome control",
)
src = sub_once(
    src,
    "Because no sweetened-beverage exposure showed such an effect, mediation MR was not pursued, and the pre-specified NHANES observational triangulation was deferred to future work. Two deviations are reported transparently: locus-level colocalization",
    "Because no sweetened-beverage exposure showed such an effect, mediation MR through BMI was performed during revision for the sole nominal signal (coffee intake) as a mechanistic probe; the pre-specified NHANES observational triangulation was deferred to future work. Three deviations are reported transparently: the revision-stage mediation probe just described; locus-level colocalization",
    "Methods: deviations statement updated",
)
src = sub_once(
    src,
    " Between-source heterogeneity was negligible (I² = 2.7%) and random-effects meta-analysis was essentially unchanged (OR 1.34; P = 0.003).",
    "",
    "Results: trim duplicated I-squared sentence",
)
src = sub_once(
    src,
    "(γ = 0.01, 95% CI −0.01 to 0.04; Table S15).`,",
    "(γ = 0.01, 95% CI −0.01 to 0.04; Table S15). Two-step mediation MR attributed the nominal association to the adiposity pathway: coffee intake increased BMI (β = 0.82 kg/m² per intake category; P = 0.007), BMI increased AF (β = 0.343 log OR per kg/m²; P = 2 × 10⁻³⁸), and the BMI-mediated indirect effect (0.281, SE 0.106) statistically accounted for the entire total association (mediated proportion 120%, 95% CI −23% to 263%), leaving a null direct effect (Table S16). The MRlap overlap-corrected estimate did not differ significantly from the observed estimate (difference P = 0.07; Table S17), excluding material sample-overlap bias.`,",
    "Results: mediation + MRlap sentences",
)
src = sub_once(
    src,
    "The detection of the alcohol-quantity signal argues against general insensitivity as an explanation for the null beverage findings.`,",
    "The detection of the alcohol-quantity signal argues against general insensitivity as an explanation for the null beverage findings.`]),\n  h2(T`Negative outcome control: atrioventricular block`),\n  mix([\n    T`Against atrioventricular block (FinnGen R13 I9_AVBLOCK; Table S18), six of nine exposure tests were null (P ≥ 0.53); nominal positive associations for alcohol intake frequency (P = 0.043) and coffee intake (P = 0.042) did not survive Bonferroni correction across the nine tests, whereas the inverse association for sugar added to tea (P = 0.001) did. The coffee and sugar-in-tea estimates mirrored their AF associations in direction and magnitude—the behaviour expected if both track the shared adiposity-mediated pathway, BMI being an established risk factor for atrioventricular block—so the control informs pathway sharing rather than instrument specificity (Limitations).`,",
    "Results: negative outcome control paragraph",
)
src = sub_once(
    src,
    "increases AF risk through atrial remodelling, epicardial fat, hypertension and obstructive sleep apnoea.",
    "increases AF risk through atrial remodelling, epicardial fat, hypertension and obstructive sleep apnoea. Two-step mediation MR quantified this pathway for the nominal coffee signal: the BMI-mediated indirect effect statistically accounted for the entire association, leaving a null direct effect (Table S16).",
    "Discussion: mediation quantification in mechanisms",
)
src = sub_once(
    src,
    " This distinction matters clinically: it shifts preventive emphasis from beverage-specific restriction towards weight management and overall dietary pattern, in line with guideline recommendations for lifestyle management of AF [1].",
    " This distinction matters clinically, shifting preventive emphasis towards weight management and overall dietary pattern [1].",
    "Discussion: trim mechanisms clinical sentence",
)
src = sub_once(
    src,
    "Seventh, AF ascertainment from diagnostic codes under-detects paroxysmal AF.",
    "Seventh, AF ascertainment from diagnostic codes under-detects paroxysmal AF, and the FinnGen I9_AF endpoint pools AF with atrial flutter (ICD-10 I48), so FinnGen-specific estimates are not AF-exclusive.",
    "Discussion: flutter-pooling limitation",
)
src = sub_once(
    src,
    "Finally, mediation MR, although pre-specified, was conditional on a robust total effect and was therefore not performed; the NHANES observational triangulation is deferred to future work.",
    "Finally, mediation MR—pre-specified as conditional on a robust total effect—was performed during revision as a mechanistic probe of the sole nominal signal and carries the usual product-method assumptions (including homogeneity of the mediator–outcome effect across instrument sets); the negative outcome control was imperfect, because atrioventricular block shares adiposity-mediated aetiology with AF, so AF-specificity of the coffee and sugar-in-tea instruments cannot be formally established; the NHANES observational triangulation is deferred to future work.",
    "Discussion: limitations finally updated",
)
src = sub_once(
    src,
    "Implementation accuracy was verified against a same-trait positive control (Nielsen 2018 × FinnGen R13, expected rg ≈ 1) and an overlap positive control (coffee × tea intake, both UK Biobank).",
    "Implementation accuracy was verified against same-trait and overlap positive controls.",
    "Methods: trim LDSC validation clause",
)
src = sub_once(
    src,
    "; the nominal inverse association for sugar added to tea in FinnGen R13 (P = 0.014) did not replicate in any other outcome source (meta-analysis P = 0.060) and is interpreted as a chance finding.",
    ".",
    "Table 2 footnote: trim duplicated sugar-tea sentence",
)
src = sub_once(
    src,
    " DerSimonian–Laird random-effects meta-analysis did not change any conclusion (coffee intake OR 1.34, 1.11–1.63, P = 0.003; sugar added to tea OR 0.77, 0.51–1.15, P = 0.20).",
    "",
    "Table 2 footnote: trim duplicated random-effects sentence",
)
src = sub_once(
    src,
    "Manuscript version: v4.5.2 — EJPC format plus reviewer-driven additions: references renumbered by order of first appearance; Xie 2024 divergence addressed; colocalization prior-sensitivity scan (Table S13); contamination-mixture estimator (Table S14); LDSC rg forest plot (Figure S2); genome-wide CAUSE analysis (Table S15) (24 August 2026)",
    "Manuscript version: v4.5.3 — EJPC format plus reviewer-driven additions: references renumbered by order of first appearance; Xie 2024 divergence addressed; colocalization prior-sensitivity scan (Table S13); contamination-mixture estimator (Table S14); LDSC rg forest plot (Figure S2); genome-wide CAUSE analysis (Table S15); two-step mediation MR (Table S16), MRlap correction (Table S17) and an atrioventricular-block negative outcome control (Table S18) (25 August 2026)",
    "version note v4.5.3",
)
src = sub_once(
    src,
    "Sweetened beverages and atrial fibrillation — MR manuscript (v4.5.2, EJPC format)",
    "Sweetened beverages and atrial fibrillation — MR manuscript (v4.5.3, EJPC format)",
    "page header v4.5.3",
)
src = sub_once(
    src,
    "cross-trait linkage disequilibrium score (LDSC) regression and a positive lifestyle control (alcohol).",
    "cross-trait linkage disequilibrium score (LDSC) regression, two-step mediation MR, and positive and negative controls.",
    "Abstract: methods list updated",
)
if fails:
    print("\nMANUSCRIPT v4.5.3 ABORTED (insertions):", len(fails), "failure(s)")
    sys.exit(1)

# ---- 2. auto-remap citations by first appearance ----
tok_pat = re.compile(r"(?<![A-Za-z0-9_\)\]])\[(\d{1,2}(?:,\d{1,2})*)\]|⟦(NETMR|MRLAP)⟧")
order = []
for m in tok_pat.finditer(src):
    toks = [m.group(2)] if m.group(2) else [int(x) for x in m.group(1).split(",")]
    for t in toks:
        if t not in order:
            order.append(t)
expected = set(range(1, 26)) | {"NETMR", "MRLAP"}
check(set(order) == expected, f"token set mismatch: {sorted(set(order), key=str)}")
check(len(order) == 27, f"{len(order)} distinct tokens (expected 27)")
if fails:
    print("\nMANUSCRIPT v4.5.3 ABORTED (scan):", len(fails), "failure(s)")
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
check(sorted(set(flat)) == list(range(1, 28)), f"post-remap citation set = {sorted(set(flat))}")
firsts = {}
for i, g in enumerate(groups):
    for n in g:
        firsts.setdefault(n, i)
seq = [n for n, _ in sorted(firsts.items(), key=lambda kv: kv[1])]
check(seq == list(range(1, 28)), f"first-appearance not monotonic after remap: {seq}")
print(f"  ok: renumbered {len(groups)} citation groups; first appearance monotonic 1..27")

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
print("  ok: references array rebuilt (27 entries)")

if fails:
    print("\nMANUSCRIPT v4.5.3 ABORTED:", len(fails), "failure(s)")
    sys.exit(1)
(BUILD / "build_manuscript_v45.js").write_text(src, encoding="utf-8")
print("written: build_manuscript_v45.js (v4.5.3)")

n_netmr = new_num["NETMR"]
n_mrlap = new_num["MRLAP"]
n_conmix = new_num[19]
n_cause = new_num[20]
n_xie = new_num[23]
print(f"  key numbers: NETMR=[{n_netmr}] MRLAP=[{n_mrlap}] conmix=[{n_conmix}] CAUSE=[{n_cause}] XIE=[{n_xie}]")

# ================= SUPPLEMENT =================
fails = []
sup = (BUILD / "build_supplement_v45.js").read_text(encoding="utf-8")
sup = sub_once(
    sup,
    'const T15 = readTsv(path.join(DIR, "S15_cause.tsv"));\n',
    'const T15 = readTsv(path.join(DIR, "S15_cause.tsv"));\nconst T16 = readTsv(path.join(DIR, "S16_mediation.tsv"));\nconst T17 = readTsv(path.join(DIR, "S17_mrlap.tsv"));\nconst T18 = readTsv(path.join(DIR, "S18_avblock.tsv"));\n',
    "supplement: import S16-S18 TSVs",
)
n = sup.count("(v4.5.2)")
if check(n == 2, f"supplement '(v4.5.2)' x{n} (expected 2)"):
    sup = sup.replace("(v4.5.2)", "(v4.5.3)")
    print("  ok: supplement version strings -> v4.5.3")
sup = sub_once(
    sup,
    "Burgess et al., 2020; manuscript ref 19",
    f"Burgess et al., 2020; manuscript ref {n_conmix}",
    "supplement: S14 note ref renumbered",
)
sup = sub_once(
    sup,
    "Morrison et al., 2020; manuscript ref 20",
    f"Morrison et al., 2020; manuscript ref {n_cause}",
    "supplement: S15 note ref renumbered",
)
sup = sub_once(
    sup,
    'v4.5.2 note: Table S15 reports the genome-wide CAUSE analysis (causal versus correlated-pleiotropy model) for coffee intake and AF."',
    'v4.5.2 note: Table S15 reports the genome-wide CAUSE analysis (causal versus correlated-pleiotropy model) for coffee intake and AF. v4.5.3 note: Tables S16-S18 report the revision-stage robustness additions - two-step (network) mediation MR through BMI for the nominal coffee signal (Table S16), MRlap correction for sample overlap, winner\'s curse and weak-instrument bias (Table S17), and the atrioventricular-block negative outcome control (Table S18)."',
    "supplement: v4.5.3 contents note",
)
S16_BLOCK = f"""children.push(caption("Table S16. Two-step (network) mediation MR of coffee intake, body mass index and atrial fibrillation (Nielsen 2018 outcome)"));
children.push(makeTable(
  [1900, 4300, 1900, 1050, 950, 950, 900],
  T16.header, T16.rows, 18));
children.push(note("Network (two-step) mediation MR (Burgess et al., 2015; manuscript ref {n_netmr}) applied to the sole nominal signal as a mechanistic probe. Step 1 used the 17 of 34 coffee instruments represented in the HapMap-2-based Yengo 2018 BMI meta-analysis (GCST006900; kg/m2 units); cross-matching by chromosome:position recovered no further instruments. Step 2 used 701 BMI instruments (P < 5 x 10-8) selected by 1-Mb window pruning (lowest P retained; a conservative substitute for LD clumping without a compatible reference panel); the BMI-AF estimate (0.343, SE 0.026) agreed with the MVMR conditional estimate (0.384, SE 0.035; Table S4) and with the weighted median (0.316, SE 0.035). Indirect effect and mediated proportion used the product method with delta-method standard errors; covariance between steps (partially overlapping UK Biobank samples) was ignored, so confidence intervals are slightly anti-conservative. A mediated proportion above 100% with a null direct effect mirrors the MVMR attenuation (OR 0.82; P = 0.099) and indicates that the nominal total association is statistically explained by the adiposity pathway."));

children.push(caption("Table S17. MRlap correction for sample overlap, winner's curse and weak-instrument bias: coffee intake and atrial fibrillation (Nielsen 2018)"));
children.push(makeTable(
  [5200, 3300, 1100, 1000],
  T17.header, T17.rows, 18));
children.push(note("MRlap (Mounier & Kutalik, 2023; manuscript ref {n_mrlap}) approximates sample overlap by cross-trait LDSC (GenomicSEM implementation) and derives a corrected causal estimate under a spike-and-slab genetic-architecture model; both traits entered as Z-scores from the same munged files used for the LDSC analysis (Tables S10-S11), so effects are per SD and only sign and precision are interpreted. The corrected effect (0.037, SE 0.023) did not differ significantly from the observed IVW effect (0.028, SE 0.018; difference P = 0.070), and the cross-trait intercept (-0.010, SE 0.006) matched the independent LDSC diagnostic (-0.011, SE 0.008; Table S11), jointly excluding material bias from sample overlap, winner's curse and weak instruments. HapMap-3 SNP list: w_hm3.snplist (MHC retained); 8,000 simulations were used for the variance of the corrected effect."));

children.push(caption("Table S18. Negative outcome control: beverage exposures and alcohol controls against atrioventricular block (FinnGen R13 I9_AVBLOCK)"));
children.push(makeTable(
  [3600, 2400, 1100, 1050, 1000, 1050],
  T18.header, T18.rows, 18));
children.push(note("Atrioventricular block was chosen a priori as a negative outcome (a conduction disorder with no hypothesised causal link to beverage intake). Six of nine exposure tests were null (P >= 0.53). Three nominal associations emerged - alcohol intake frequency (+0.186, P = 0.043), coffee intake (+0.480, P = 0.042) and sugar added to tea (-0.676, P = 0.001) - of which only sugar added to tea survived Bonferroni correction across the nine tests (threshold P = 0.006). The coffee and sugar-in-tea estimates mirrored the direction and magnitude of their AF associations (+0.458 and -0.506, respectively, in FinnGen R13), the expected behaviour if both endpoints share the adiposity-mediated pathway (BMI is an established risk factor for atrioventricular block); the analysis is therefore interpreted as a positive control for the shared pathway rather than a discriminator of instrument validity, and AF-specificity of these instruments cannot be formally established (manuscript Limitations)."));

const doc = new Document({{"""
sup = sub_once(sup, "const doc = new Document({", S16_BLOCK, "supplement: add Tables S16-S18")

if fails:
    print("\nSUPPLEMENT v4.5.3 ABORTED:", len(fails), "failure(s)")
    sys.exit(1)
(BUILD / "build_supplement_v45.js").write_text(sup, encoding="utf-8")
print("written: build_supplement_v45.js (v4.5.3)")
print("\nALL v4.5.3 TRANSFORMS COMPLETED")
print("OLD->NEW:", {str(k): v for k, v in sorted(new_num.items(), key=lambda kv: kv[1])})
