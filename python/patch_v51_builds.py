# v5.1 patch: manuscript + supplement build scripts (v50 -> v51)
# Each replacement carries a unique-occurrence assertion.
import io, os, sys

DIR = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本"
M = os.path.join(DIR, "build_manuscript_v51.js")
S = os.path.join(DIR, "build_supplement_v51.js")

def patch(path, pairs, label):
    t = io.open(path, encoding="utf-8").read()
    for i, (old, new) in enumerate(pairs, 1):
        n = t.count(old)
        assert n == 1, f"[{label} #{i}] anchor occurs {n} times (need 1): {old[:80]}..."
        t = t.replace(old, new)
    io.open(path, "w", encoding="utf-8").write(t)
    print(f"[{label}] {len(pairs)} patches applied OK")

# ---------------- manuscript ----------------
mp = []

mp.append((
 "conditional on adiposity, with BMI as a positive control. Complementary two-step",
 "conditional on adiposity, with BMI as a positive control; conditional instrument strength was quantified with Sanderson\u2013Windmeijer conditional F statistics (MVMR package) [42]. Complementary two-step"))

mp.append((
 "All per-variant F statistics exceeded 20, indicating strong instruments and limited weak-instrument bias.",
 "All per-variant F statistics exceeded 20 (Table S22), indicating strong instruments and limited weak-instrument bias at the univariable stage."))

mp.append((
 "it should not be considered informative (OR 0.99; P = 0.96).",
 "it should not be considered informative (OR 0.99; P = 0.96). Conditional F statistics were below the conventional threshold of 10 for all three exposures (coffee 5.2; sugar added to tea 1.3; BMI 7.5; Table S24); because weak conditional instruments bias multivariable estimates towards the null, these estimates are interpreted as supportive rather than definitive."))

mp.append((
 "T`MR-RAPS estimates, robust to many weak and pleiotropic instruments, were null for every exposure against both co-primary outcomes (Table S23), including coffee (Nielsen 2018 log-odds ratio 0.17, P = 0.11; FinnGen R13 0.47, P = 0.13; all other exposures P \u2265 0.39).",
 "T`MR-RAPS estimates, robust to many weak and pleiotropic instruments, were directionally consistent with the primary IVW analysis for all 14 exposure\u2013outcome pairs (Table S23): every exposure was null against Nielsen 2018, including coffee (log-odds ratio 0.17, P = 0.11), whereas against FinnGen R13 the nominal coffee (log-odds ratio 0.41, P = 0.045) and inverse sugar-added-to-tea (\u22120.37, P = 0.032) associations persisted at nominal significance, mirroring that source's primary estimates (Table 2); all other tests were null (P \u2265 0.51). Neither nominal signal survived correction for the 14 MR-RAPS tests, reinforcing the source-dependent interpretation of both."))

mp.append((
 "Previous Mendelian randomization analyses examined individual beverages in smaller outcome resources, without adiposity modelling or East Asian context.",
 "Previous Mendelian randomization analyses examined individual beverages in smaller outcome resources, without adiposity modelling or East Asian context [8,29,40]."))

mp.append((
 "Beyond previous single-beverage MR analyses [8,29], the present study contributes",
 "Beyond previous single-beverage and dietary-exposure MR analyses [8,29,40,41], the present study contributes"))

new_section = (
 "  h2(T`Instrument specificity and horizontal pleiotropy`),\n"
 "  mix([\n"
 "    T`Genetic instruments for self-reported beverage intake are not molecule-specific: they index intake behaviour together with its adiposity, dietary-quality and socioeconomic correlates, so horizontal pleiotropy is the expectation rather than the exception for traits of this kind [32,33]. Three features of the design mitigate this concern. First, pleiotropy of this type manufactures false-positive signals, not precise false negatives: the headline estimates are null with confidence bounds that exclude the observational effect sizes, a pattern that would be improbable were a moderate causal effect present. Second, the single nominal signal that did arise was dissected rather than accepted at face value\u2014source-dependent outlier sensitivity, attenuation once BMI was modelled jointly, and colocalization confined to the adiposity locus FTO jointly show the framework detecting and isolating pleiotropy rather than concealing it. Third, all exposures were re-estimated under estimators with orthogonal robustness assumptions (weighted median, contamination mixture, MR-RAPS, CAUSE, MRlap), with concordant results. We nonetheless interpret these estimates as effects of the behaviour cluster the instruments index, not of a molecularly isolated exposure, and frame our conclusions accordingly.`,\n"
 "  ]),\n"
 "  mix([\n"
 "    T`For coffee, the literature is mixed.")
mp.append(("  mix([\n    T`For coffee, the literature is mixed.", new_section))

mp.append((
 "our null tea estimates extend that literature causally.",
 "our null tea estimates extend that literature causally and concur with a previous null MR of tea intake against cardiovascular outcomes [41]."))

mp.append((
 "MR-RAPS was null for all seven exposures against both co-primary outcomes, and MRlap-based joint correction",
 "MR-RAPS estimates were concordant with the primary analysis throughout\u2014null for all seven exposures against Nielsen 2018 and tracking the two nominal FinnGen R13 signals (Table S23)\u2014and MRlap-based joint correction"))

mp.append((
 "the conditional analyses carry caveats of their own: mediation MR was performed",
 "the conditional analyses carry caveats of their own: the multivariable estimates rest on conditionally modest instruments (conditional F 1.3\u20137.5; Table S24) and are biased towards the null under weak identification; mediation MR was performed"))

mp.append((
 "Estimates are MVMR-IVW odds ratios per unit of each exposure conditional on the others.",
 "Estimates are MVMR-IVW odds ratios per unit of each exposure conditional on the others. Conditional F statistics (Table S24) were 5.2 (coffee intake), 1.3 (sugar added to tea) and 7.5 (BMI), below the conventional threshold of 10."))

mp.append((
 "T`39. Zhao Q, Wang J, Hemani G, Bowden J, Small DS. Statistical inference in two-sample summary-data Mendelian randomization using robust adjusted profile score. Ann Stat. 2020;48(3):1742-1769.`,",
 "T`39. Zhao Q, Wang J, Hemani G, Bowden J, Small DS. Statistical inference in two-sample summary-data Mendelian randomization using robust adjusted profile score. Ann Stat. 2020;48(3):1742-1769.`,\n"
 "    T`40. Li H, Xu J. Multifaceted dietary exposures and atrial fibrillation: bidirectional causal evidence from two-sample Mendelian randomization. Medicine (Baltimore). 2025;104(38):e44722.`,\n"
 "    T`41. Chen L, Sun X, Zheng L. No causal effect of tea consumption on cardiovascular diseases: a two-sample Mendelian randomization study. Front Cardiovasc Med. 2022;9:870972.`,\n"
 "    T`42. Sanderson E, Davey Smith G, Windmeijer F, Bowden J. An examination of multivariable Mendelian randomization in the single-sample and two-sample summary data settings. Int J Epidemiol. 2019;48(3):713-727.`,"))

mp.append(("co-localized with AF only at the obesity gene FTO", "colocalized with AF only at the obesity gene FTO"))

patch(M, mp, "manuscript")

# ---------------- supplement ----------------
sp = []

sp.append((
 'Study With Cross-Ancestry Replication", { size: 24',
 'Study With East Asian Contextual Analysis", { size: 24'))

sp.append((
 "Table S23 MR-RAPS robust adjusted profile score estimates for all exposures against both co-primary outcomes; Figure S1",
 "Table S23 MR-RAPS robust adjusted profile score estimates for all exposures against both co-primary outcomes; Table S24 Sanderson\u2013Windmeijer conditional F statistics for the multivariable MR instrument set; Figure S1"))

sp.append((
 'const T23 = readTsv(path.join(DIR, "S23_mrraps.tsv"));',
 'const T23 = readTsv(path.join(DIR, "S23_mrraps.tsv"));\nconst T24 = readTsv(path.join(DIR, "S24_conditional_F.tsv"));'))

sp.append((
 "Every exposure was null against both co-primary outcomes, including coffee (Nielsen 2018 log-OR 0.17, P = 0.11; FinnGen R13 0.47, P = 0.13), further supporting the interpretation that the nominal IVW coffee signal is not robust.",
 "Estimates were directionally consistent with the primary IVW analysis for all 14 exposure\u2013outcome pairs: every exposure was null against Nielsen 2018, including coffee (log-OR 0.17, P = 0.11); against FinnGen R13 the nominal coffee (log-OR 0.41, P = 0.045) and inverse sugar-added-to-tea (log-OR \u22120.37, P = 0.032) associations persisted at nominal significance, mirroring that source's primary estimates, and neither survived correction for the 14 tests. MR-RAPS thus corroborates, rather than overturns, the source-dependent reading of both nominal signals."))

s24_block = (
 'children.push(caption("Table S24. Sanderson\u2013Windmeijer conditional F statistics for the multivariable MR instrument set (471 harmonized SNPs)"));\n'
 "children.push(makeTable(\n"
 "  [2800, 1400, 1900, 1900],\n"
 '  ["Exposure", "Conditional F", "Conventional threshold", "Harmonized SNPs (n)"],\n'
 "  T24.rows.map((r) => [r[0], r[1], r[2], r[3]]), 18));\n"
 'children.push(note("Conditional F statistics quantify each exposure\'s instrument strength conditional on the other exposures in the multivariable model (Sanderson et al., 2019; manuscript ref 42); values below the conventional threshold of 10 indicate limited conditional strength, biasing multivariable estimates towards the null. Computed with MVMR::strength_mvmr (exposure covariance fixed at 0, the package default). The re-derived joint instrument set reproduced the multivariable MR estimates in Table 4 exactly (regression coefficients and standard errors identical to 8 decimal places), confirming fidelity to the primary analysis."));\n'
 "\n"
 "const doc = new Document({")
sp.append(("const doc = new Document({", s24_block))

patch(S, sp, "supplement")
print("ALL PATCHES OK")
