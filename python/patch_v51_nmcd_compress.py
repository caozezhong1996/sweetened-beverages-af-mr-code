# -*- coding: utf-8 -*-
"""patch_v51_nmcd_compress.py — compress manuscript v5.1 to NMCD <=4000-word format.

One-shot patch (asserts each anchor matches exactly once; backups written as
*.bak_nmcd beside the targets). Applies to:
  - 04_docx构建脚本/build_manuscript_v51.js   (title, abstract, lay summary, body, legends)
  - 04_docx构建脚本/build_supplement_v51.js   (title only)
  - 04_docx构建脚本/build_cover_letter_v51.js (title only)
"""
import re
import shutil
import sys
from pathlib import Path

BASE = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822")
BLD = BASE / "04_docx构建脚本"

NEW_TITLE = ("Sweetened Beverage Consumption and Atrial Fibrillation: "
             "Two-Sample and Multivariable Mendelian Randomization")
OLD_TITLE = ("Sweetened Beverage Consumption and Risk of Atrial Fibrillation: "
             "A Two-Sample and Multivariable Mendelian Randomization Study "
             "With East Asian Contextual Analysis")
assert len(NEW_TITLE) <= 120, len(NEW_TITLE)


def sub_literal(text, anchor, new_inner):
    pat = re.compile(r"T`[^`]*" + re.escape(anchor) + r"[^`]*`", re.S)
    n = len(pat.findall(text))
    if n != 1:
        raise SystemExit(f"ANCHOR NOT UNIQUE ({n}): {anchor[:70]}")
    return pat.sub(lambda m: "T`" + new_inner + "`", text, count=1)


REPL = [
    # ---------------- title ----------------
    ("Sweetened Beverage Consumption and Risk of Atrial Fibrillation: A Two-Sample",
     NEW_TITLE),
    # ---------------- abstract (NMCD three-part) ----------------
    ("Aim: Milk tea",
     "Background and aims: Milk tea (typically 35–50 g sugar and 100–200 mg "
     "caffeine per serving) has never been prospectively studied for atrial "
     "fibrillation (AF) and is not instrumented in genome-wide association "
     "studies (GWAS). We tested whether genetically proxied intake of its "
     "sweetened-beverage components is causally associated with AF."),
    ("Methods: Seven beverage exposures",
     "Methods and results: Seven beverage exposures were instrumented in UK "
     "Biobank GWAS (N = 64,949–447,485); AF statistics came from Nielsen 2018 "
     "(60,620 cases; primary), non-overlapping FinnGen R13 (67,783 cases; "
     "co-primary), AFGen 2018 (sensitivity) and BioBank Japan (East Asian "
     "context). Inverse-variance-weighted estimates were complemented by "
     "robust estimators, multivariable MR, locus-level colocalization and "
     "cross-trait LD-score regression. No sweetened-beverage exposure showed "
     "evidence of a causal association with AF (European meta-analytic odds "
     "ratios 0.82–0.97; P ≥ 0.06). A nominal coffee association (OR 1.34, "
     "1.11–1.62; P = 0.002) was not robust: null weighted-median estimates, "
     "source-dependent outlier robustness, attenuation after body-mass-index "
     "adjustment (OR 0.82; P = 0.099) and colocalization only at the "
     "adiposity locus FTO. Sweetened-beverage traits nonetheless showed "
     "positive genetic correlations with AF (rg = 0.24–0.31; FDR q < 0.05)."),
    ("Conclusions: Genetically proxied sweetened-beverage intake",
     "Conclusion: Genetically proxied sweetened-beverage intake showed no "
     "evidence of a causal association with AF; moderate-to-large effects are "
     "excluded, but small effects are not. The modest observational "
     "association likely reflects adiposity-related confounding; direct "
     "milk-tea studies in East Asian cohorts remain needed."),
    # ---------------- introduction ----------------
    ("Atrial fibrillation (AF) is the most common sustained",
     "Atrial fibrillation (AF) is the most common sustained cardiac "
     "arrhythmia and a major cause of ischaemic stroke, heart failure and "
     "premature death; identifying modifiable lifestyle determinants, "
     "including dietary factors, is a public-health priority [1]."),
    ("Over the past decade, bubble (milk) tea",
     "Bubble (milk) tea—typically 35–50 g of added sugar and 100–200 mg of "
     "caffeine per serving, often with non-dairy creamer or high-fat "
     "toppings—has become one of the most widely consumed prepared beverages "
     "among young people in East Asia and increasingly worldwide. No "
     "prospective cohort has measured milk tea consumption directly, and no "
     "GWAS instruments it; milk-tea-type beverages motivated, but were not "
     "directly evaluated in, the present analysis."),
    ("The closest available evidence concerns",
     "The closest available evidence concerns sugar-sweetened beverages "
     "(SSBs): in 201,856 UK Biobank participants, consumption of more than "
     "2 L/week of SSBs or artificially sweetened beverages (ASBs) was "
     "associated with 10% and 20% higher incident AF risk, respectively [2], "
     "with linear associations confirmed in prediabetes and diabetes [3]; "
     "residual confounding cannot be excluded. Previous Mendelian "
     "randomization (MR) analyses examined single beverages in smaller "
     "outcome resources, without adiposity modelling or East Asian context "
     "[8,29,40]."),
    ("Evidence for caffeine, the second major",
     "For caffeine, the second major bioactive component of milk tea, "
     "habitual coffee was inversely associated with incident AF in large "
     "cohorts [4,5,6] and a meta-analysis [7]; an MR analysis found no causal "
     "coffee–AF association [8]; and the randomized DECAF trial found that "
     "daily caffeinated coffee did not increase AF recurrence [9]. A 2026 "
     "American Heart Association scientific statement reached the same "
     "conclusion and prioritized disentangling caffeine from beverage "
     "co-ingredients [10]."),
    ("Milk tea itself has never been studied",
     "Milk tea itself has never been studied as an exposure; the SSB–AF "
     "association lacks causal evidence; and sugar and caffeine have rarely "
     "been examined within a single causal framework. Leveraging UK Biobank "
     "beverage-consumption GWAS [11] and the largest publicly available AF "
     "GWAS in European and East Asian populations, we conducted a two-sample "
     "and multivariable MR study of sweetened beverage consumption (not milk "
     "tea itself) and AF, aiming (i) to estimate causal effects of "
     "sweetened-beverage intake, particularly sugar added to tea or coffee "
     "(the closest genetic proxy for milk-tea-type beverages); (ii) to "
     "disentangle sugar-related and caffeine-related behaviour with body mass "
     "index (BMI) modelled jointly; (iii) to examine contextual consistency "
     "in an East Asian population; and (iv) to benchmark analytical "
     "sensitivity using alcohol consumption as a positive lifestyle control."),
    # ---------------- methods ----------------
    ("This study is reported in accordance with the STROBE-MR",
     "This study is reported in accordance with the STROBE-MR checklist [12] "
     "and rests on the three core MR assumptions: the instruments are "
     "robustly associated with the exposure, share no common cause with the "
     "outcome, and affect the outcome only through the exposure. All analyses "
     "use publicly available, de-identified GWAS summary statistics; the "
     "analysis plan was finalized before outcome data were analysed."),
    ("Exposure data.",
     "Exposure data. Instruments for seven beverage phenotypes were obtained "
     "from UK Biobank GWAS (MRC Integrative Epidemiology Unit pipeline, "
     "distributed through OpenGWAS; identifiers in Table 1): sugar added to "
     "tea, sugar added to coffee, fizzy drink intake (sugar-sweetened "
     "beverages, SSBs), low-calorie drink intake (artificially sweetened "
     "beverages, ASBs) and artificial sweetener added to tea (each "
     "N = 64,949), coffee intake (N = 428,860) and tea intake (N = 447,485), "
     "all in European-ancestry participants. Sugar added to tea or coffee "
     "captures sweetening behaviour for tea/coffee-based drinks and is "
     "conceptually the closest available proxy for milk-tea-type composite "
     "beverages."),
    ("Outcome data.",
     "Outcome data. The primary outcome was the largest public "
     "European-ancestry AF GWAS (Nielsen et al. [13]; 60,620 cases, 970,216 "
     "controls; ebi-a-GCST006414); a larger cross-population meta-analysis is "
     "not publicly available (GCST90624413) [16]. FinnGen release R13 [15] "
     "(I9_AF; 67,783 cases, 241,269 controls) shares no participants with UK "
     "Biobank and served as a co-primary outcome; AFGen 2018 (55,114 cases) "
     "[14], which shares cohorts with Nielsen 2018, was a sensitivity source. "
     "BioBank Japan (bbj-a-71; 8,180 cases, 28,612 controls) [17] provided "
     "East Asian context. An early-onset AF outcome (onset before age 66; "
     "2,781 cases, 4,959 controls; GCST010636) served as a sensitivity "
     "source, with score statistics converted to effect estimates "
     "(β = Score/Var; SE = 1/√Var)."),
    ("Covariate and positive-control data.",
     "Covariate and positive-control data. BMI statistics came from the "
     "GIANT consortium (N = 681,275; ieu-b-40) [18]. Alcohol consumption, an "
     "established modifiable AF risk factor [1], served as a positive "
     "lifestyle control, instrumented through GSCAN alcoholic drinks per week "
     "(N = 335,394; ieu-b-73) [19] and, alternatively, UK Biobank alcohol "
     "intake frequency (N = 462,346; ukb-b-5779)."),
    ("For each exposure, single-nucleotide",
     "For each exposure, single-nucleotide polymorphisms (SNPs) were clumped "
     "to independence (r² < 0.001 within 10,000 kb) using ancestry-matched "
     "linkage-disequilibrium references. Coffee and tea instruments were "
     "genome-wide significant (P < 5 × 10⁻⁸); for the five beverage "
     "sub-phenotypes, fewer than three variants reached that threshold, so "
     "instruments were selected at the pre-specified relaxed threshold "
     "(P < 5 × 10⁻⁶), a choice revisited in the Limitations. Palindromic "
     "variants with intermediate allele frequencies were excluded, "
     "per-variant F statistics above 10 were required, and identical "
     "instrument lists were used across outcome sources. Because the "
     "phenotypes are ordinal questionnaire categories, estimates are scaled "
     "per one-category increment in genetically instrumented intake."),
    ("Univariable MR.",
     "Univariable MR. Random-effects inverse-variance-weighted (IVW) "
     "regression was primary, complemented by MR-Egger, weighted-median and "
     "weighted-mode estimators, Cochran's Q and the MR-Egger intercept; "
     "MR-PRESSO was applied to exposures with a nominal association against "
     "the primary outcome. Nielsen 2018 and FinnGen R13 estimates were "
     "combined by fixed-effect meta-analysis (DerSimonian–Laird sensitivity); "
     "AFGen 2018 was not meta-analysed, because it shares cohorts with "
     "Nielsen 2018. BioBank Japan estimates are contextual rather than "
     "independent replication, because the instruments derive from "
     "European-ancestry GWAS."),
    ("Multivariable MR [20].",
     "Multivariable MR [20]. Coffee intake, sugar added to tea and BMI were "
     "modelled jointly (MVMR-IVW) to estimate direct effects conditional on "
     "adiposity, with BMI as a positive control and Sanderson–Windmeijer "
     "conditional F statistics quantifying conditional instrument strength "
     "[42]. Complementary two-step (network) mediation MR [21] quantified the "
     "adiposity-mediated component of the nominal coffee signal (product "
     "method; Table S16), with robustness using the full-coverage Neale BMI "
     "GWAS (field 21001) and an independent coffee GWAS (field 1498)."),
    ("Multiplicity.",
     "Multiplicity. The seven European meta-analytic IVW tests formed the "
     "primary family (Benjamini–Hochberg q = 0.05); all other analyses were "
     "supportive or exploratory. Analyses used R 4.6.0 with the TwoSampleMR "
     "[22], MRPRESSO [23] and coloc packages; analysis code is archived at "
     "https://doi.org/10.5281/zenodo.22099675."),
    ("Robustness, directionality and power.",
     "Robustness, directionality and power. Causal direction was verified by "
     "Steiger testing and per-variant filtering. Additional robust estimators "
     "comprised radial IVW, the contamination-mixture estimator [24] and "
     "MR-RAPS [39], the last applied to all seven exposures against both "
     "co-primary outcomes; genome-wide CAUSE [25] distinguished correlated "
     "pleiotropy from causation while modelling sample overlap; and MRlap "
     "[26] jointly corrected the coffee and tea estimates for overlap, "
     "winner's curse and weak-instrument bias (Table S17). Leave-one-out and "
     "funnel plots assessed influential instruments; reverse MR (111 "
     "AF-associated SNPs) tested reverse causation; atrioventricular block "
     "(I9_AVBLOCK) was the negative outcome control (Table S18). Power was "
     "quantified as the minimum detectable odds ratio at 80% power. "
     "Locus-level colocalization (coloc.abf, default priors; PP.H4 > 0.8 "
     "indicating a shared variant) covered 500-kb windows around CYP1A1–"
     "CYP1A2 (rs2472297), AHR (rs4410790) and FTO (rs1421085)—the "
     "caffeine-metabolism and adiposity loci—with prior p12 varied from 10⁻⁶ "
     "to 5 × 10⁻⁵."),
    ("As a pleiotropy-sensitive complement",
     "As a pleiotropy-sensitive complement to MR and a diagnostic of sample "
     "overlap, cross-trait linkage disequilibrium score (LDSC) regression "
     "[27,28] used 1000 Genomes European HapMap 3 LD scores (M = 1,290,027 "
     "SNPs), Neale lab UK Biobank round-2 full summary statistics for five "
     "beverage traits (fields 1498, 1488, 100370, 100170, 100160) and AF "
     "statistics from Nielsen 2018 and FinnGen R13. Cross-trait intercepts "
     "diagnosed overlap-driven bias; Benjamini–Hochberg correction (q = 0.05) "
     "covered the ten beverage–AF rg tests; same-trait and overlap controls "
     "validated the implementation. Full statistics for sugar and artificial "
     "sweetener added to tea are not public, precluding their LDSC."),
    ("Two-step mediation MR (product-of-coefficients",
     "Two-step mediation MR through metabolic traits and locus-level "
     "colocalization were pre-specified as conditional analyses, to be "
     "performed only where a robust total effect was detected; because only "
     "coffee intake showed a nominal signal, they were performed for coffee "
     "during revision as mechanistic probes, and the pre-specified NHANES "
     "triangulation was deferred. A further deviation was the revision-stage "
     "upgrade of the primary outcome from AFGen 2018 to the nearly "
     "twice-larger Nielsen 2018 GWAS, with all analyses repeated."),
    ("All data are de-identified, publicly available summary statistics; per the Chinese",
     "All data are de-identified, publicly available summary statistics; per "
     "the Chinese Measures for Ethical Review of Life Science and Medical "
     "Research Involving Human Subjects (Article 32, 2023), such studies are "
     "exempt from ethics review. FinnGen, BioBank Japan and OpenGWAS data "
     "were used under their respective terms."),
    # ---------------- results ----------------
    ("Between 8 and 34",
     "Between 8 and 34 independent SNPs per exposure were available against "
     "the primary outcome (median 17; Table 2), with identical lists carried "
     "into all outcome sources. All per-variant F statistics exceeded 20 "
     "(Table S22), indicating strong instruments; coffee and tea instruments "
     "were genome-wide significant, and the five sub-phenotypes used the "
     "pre-specified relaxed threshold (P < 5 × 10⁻⁶)."),
    ("Sweetened beverages and AF: no evidence of a causal association in European populations",
     "Sweetened beverages and AF in European populations"),
    ("None of the five",
     "None of the five sweetened-beverage exposures showed evidence of a "
     "causal association with AF in any European source or in the "
     "meta-analyses (Table 2; Figure 2). Nielsen 2018 IVW odds ratios (ORs) "
     "per unit higher instrumented intake were 0.91 (95% CI 0.72–1.17) for "
     "sugar added to tea, 0.91 (0.67–1.22) for fizzy drink intake, 0.99 "
     "(0.86–1.13) for low-calorie drink intake and 0.91 (0.72–1.14) for "
     "artificial sweetener added to tea (all P ≥ 0.40); fixed-effect "
     "meta-analyses were concordantly null (all P ≥ 0.060), as were "
     "weighted-median, MR-Egger and weighted-mode estimates (Table 3; Table "
     "S2). Upper meta-analytic confidence bounds (≤1.17) exclude the effect "
     "sizes reported observationally (1.1–1.2). One exception emerged: sugar "
     "added to tea showed a nominal inverse association in FinnGen R13 (OR "
     "0.60, 0.40–0.90; P = 0.014) that was not supported by the weighted "
     "median (P = 0.061), was absent from the other sources (P > 0.21), was "
     "significantly heterogeneous (Q P = 8 × 10⁻⁶; between-source I² = 67%) "
     "and attenuated in the meta-analysis (OR 0.77, 0.51–1.15; P = 0.20); we "
     "attribute it to chance."),
    ("Sugar added to coffee showed",
     "Sugar added to coffee showed a nominal inverse association in AFGen "
     "2018 (OR 0.81, 0.66–0.98; P = 0.030) that did not replicate in the "
     "nearly twice-larger primary outcome (OR 0.89; P = 0.33) or FinnGen R13 "
     "(P = 0.53), was null under weighted-median and MR-Egger estimators, and "
     "yielded a null European meta-analysis (OR 0.88, 0.72–1.09; P = 0.25); "
     "we interpret it as a chance finding attributable to winner's curse."),
    ("Coffee intake was nominally associated with higher AF odds in the primary outcome",
     "Coffee intake was nominally associated with higher AF odds (Nielsen "
     "2018 OR 1.26, 1.02–1.57; P = 0.036; AFGen 2018 OR 1.26, P = 0.031; "
     "FinnGen R13 OR 1.58, 1.09–2.29; P = 0.016; European meta-analysis OR "
     "1.34, 1.11–1.62; P = 0.002, surviving Benjamini–Hochberg correction). "
     "It nevertheless failed every pre-specified consistency criterion: "
     "significant heterogeneity (Cochran's Q P = 9 × 10⁻⁴ and 4 × 10⁻¹⁰), "
     "null weighted-median and MR-Egger estimates, and significant MR-PRESSO "
     "global tests (P = 0.002 and P < 0.001), with outlier correction "
     "resolving to the null in Nielsen 2018 (P = 0.20) but not FinnGen R13 "
     "(β = 0.345; P = 0.007). The contamination-mixture estimator gave the "
     "same source-dependent pattern (Nielsen 2018 β = 0.068, −0.136 to 0.564; "
     "P = 0.45; FinnGen R13 β = 0.689, 0.257–0.958; P = 0.001; Table S14), "
     "and genome-wide CAUSE (1,081,418 shared variants) found that correlated "
     "pleiotropy explained the coffee–AF overlap as well as a causal model "
     "(P = 0.53; posterior causal effect γ = 0.01, −0.01 to 0.04; Table S15). "
     "The signal does not meet criteria for credible causal interpretation, "
     "although a small genuine effect cannot be excluded."),
    ("Two-step mediation MR attributed",
     "Two-step mediation MR attributed the nominal signal to the adiposity "
     "pathway: coffee intake increased BMI (β = 0.82 SD; P = 0.007), BMI "
     "increased AF (β = 0.343 per SD; P = 2 × 10⁻³⁸), and the BMI-mediated "
     "indirect effect (0.281, 95% CI 0.073–0.490) was similar in magnitude to "
     "the total association (mediated proportion 120%, −23% to 263%; "
     "proportions above 100% reflect an imprecise total effect, not complete "
     "mediation), leaving a null direct effect (Table S16). The MRlap "
     "overlap-corrected estimate did not differ from the observed estimate "
     "(difference P = 0.07; Table S17). An independent coffee GWAS (field "
     "1498; 24 instruments) gave a concordant, non-significant estimate (OR "
     "1.18, 0.93–1.50; P = 0.166), with a cross-GWAS meta-analytic OR of 1.23 "
     "(1.04–1.44; P = 0.013; Table S19); BMI re-instrumented in the "
     "full-coverage Neale GWAS (33 of 34 instruments; β = 0.75 SD) reproduced "
     "the mediation (109%, −9% to 227%; Table S16)."),
    ("In MVMR including",
     "In MVMR including coffee intake, sugar added to tea and BMI (Table 4), "
     "BMI retained a robust direct effect (OR 1.47 per SD, 1.37–1.57; P = 2.0 "
     "× 10⁻²⁷; 467 SNPs), serving as a positive control, whereas the nominal "
     "coffee association attenuated (OR 0.82, 0.65–1.04; P = 0.099), "
     "consistent with confounding through adiposity. The single-instrument "
     "conditional estimate for sugar added to tea is retained for "
     "completeness only (OR 0.99; P = 0.96). Conditional F statistics were "
     "below the conventional threshold of 10 for all three exposures (coffee "
     "5.2; sugar added to tea 1.3; BMI 7.5; Table S24); because weak "
     "conditional instruments bias multivariable estimates towards the null, "
     "these estimates are supportive rather than definitive."),
    ("In BioBank Japan",
     "In BioBank Japan (8,180 cases), all sweetened-beverage exposures were "
     "null with wide confidence intervals (sugar added to tea OR 0.66, "
     "0.21–2.11; Table 2; Figure 2). Coffee intake was nominally associated "
     "with AF (OR 2.34, 1.17–4.68; P = 0.016) with null weighted-median and "
     "MR-Egger estimates, mirroring the fragile European pattern; given "
     "European-ancestry instruments, these estimates are context, not "
     "independent evidence."),
    ("All seven phenotypes were null against early-onset",
     "All seven phenotypes were null against early-onset AF (2,781 cases; IVW "
     "P ≥ 0.11; null Egger intercepts), and the nominal coffee association "
     "did not persist (weighted-median OR 1.39; MR-Egger OR 0.86; Table S20)."),
    ("Steiger directionality testing supported",
     "Steiger directionality testing supported the exposure-to-outcome "
     "direction for all exposures (all P < 10⁻³⁴; Table S6), and radial IVW "
     "reproduced the primary estimates (Table S7)."),
    ("MR-RAPS estimates, robust to many weak",
     "MR-RAPS estimates, robust to many weak and pleiotropic instruments, "
     "were directionally consistent with the primary analysis for all 14 "
     "exposure–outcome pairs (Table S23): every exposure was null against "
     "Nielsen 2018, including coffee (log-odds ratio 0.17, P = 0.11), whereas "
     "the nominal coffee (0.41, P = 0.045) and inverse sugar-added-to-tea "
     "(−0.37, P = 0.032) associations persisted only in FinnGen R13; all "
     "other tests were null (P ≥ 0.51). Neither nominal signal survived "
     "correction for the 14 tests. Reverse MR found no evidence that AF "
     "liability influences beverage consumption (111 SNPs; all P ≥ 0.054; "
     "Table S7)."),
    ("Statistical power was limited",
     "Statistical power was limited for small effects (Table S12): minimum "
     "detectable odds ratios at 80% power ranged from 1.15 (low-calorie "
     "drinks, meta-analysis) to 1.53 (fizzy drinks, primary outcome), and "
     "power to detect the observational effect size (OR 1.10) was 9–47%. The "
     "null findings therefore exclude moderate-to-large causal effects but "
     "cannot exclude effects of the magnitude reported observationally."),
    ("As a locus-level probe",
     "As a locus-level probe of the nominal coffee signal, colocalization was "
     "performed around the three loci harbouring its strongest instruments "
     "(Table S8). At CYP1A1–CYP1A2 and AHR, posterior probabilities supported "
     "a coffee-only association (PP.H1 = 0.957 and 0.931; PP.H4 ≤ 0.008): "
     "coffee-specific variation at these caffeine-handling loci has no AF "
     "counterpart. At FTO, there was strong evidence of a shared causal "
     "variant with AF (PP.H4 = 0.894; FinnGen R13 0.906), directly "
     "implicating adiposity-linked pleiotropy; the conclusion was robust to "
     "the prior (PP.H4 > 0.8 for p12 ≥ 5 × 10⁻⁶ in both sources; Table S13). "
     "Tea intake showed the identical dissociation (CYP1A1–CYP1A2/AHR PP.H1 = "
     "0.993 and 0.988, PP.H4 ≤ 0.009; FTO PP.H4 = 0.896; Table S21). "
     "Instruments restricted to the caffeine-metabolism windows were null in "
     "both European sources (P ≥ 0.44), whereas the remaining 31 instruments "
     "carried the entire signal (OR 1.50; P = 0.006 and OR 1.96; P = 0.009)."),
    ("Cross-trait LDSC—possible",
     "Cross-trait LDSC provided an exposure-wide view of shared genetic "
     "architecture (Table S10; Table S11; Figure S2). All five beverage "
     "traits showed detectable SNP heritability (h² = 0.020–0.063), as did "
     "both AF sources. Against FinnGen R13, positive genetic correlations "
     "with AF survived FDR correction for fizzy drink intake (rg = 0.239, SE "
     "0.089; q = 0.035) and low-calorie drink intake (rg = 0.313, SE 0.103; "
     "q = 0.025), with directionally similar non-significant estimates "
     "against Nielsen 2018; coffee intake showed a weak trend (rg ≤ 0.075), "
     "and tea intake and sugar added to coffee were null. Positive rg "
     "alongside null MR estimates indicates shared architecture—such as "
     "adiposity-related biology—rather than causation. Cross-trait intercepts "
     "were null for all ten pairs (|intercept| ≤ 0.018), indicating "
     "negligible overlap bias; the diagnostic detected the known coffee–tea "
     "overlap (−0.318, SE 0.011; coffee × Nielsen 2018 −0.011), and the "
     "same-trait control returned rg = 0.923."),
    ("As a positive control",
     "As a positive control, the identical pipeline was applied to alcohol "
     "consumption (Table S5). Genetically instrumented alcoholic drinks per "
     "week (GSCAN; 33 SNPs) were directionally associated with higher AF odds "
     "in all four cohorts (ORs 1.12–2.25), with a nominally significant "
     "European meta-analysis (OR 1.19, 1.01–1.40; P = 0.035), consistent with "
     "the established causal contribution of alcohol to AF; intake frequency "
     "per se (97 SNPs) was null in all cohorts (P ≥ 0.12). Detection of the "
     "alcohol-quantity signal argues against general insensitivity explaining "
     "the null beverage findings."),
    ("Against atrioventricular block (Table S18)",
     "Against atrioventricular block (Table S18), six of nine exposure tests "
     "were null (P ≥ 0.53); nominal associations for alcohol intake frequency "
     "(P = 0.043) and coffee intake (P = 0.042) did not survive Bonferroni "
     "correction, whereas the inverse association for sugar added to tea "
     "(P = 0.001) did. Because atrioventricular block shares "
     "adiposity-mediated aetiology with AF and the beverage estimates "
     "mirrored their AF directions, this pattern most plausibly reflects "
     "shared adiposity pleiotropy rather than beverage-specific effects "
     "(Limitations)."),
    # ---------------- discussion ----------------
    ("In this two-sample and multivariable",
     "In this two-sample and multivariable Mendelian randomization study "
     "using the largest publicly available European-ancestry AF GWAS, "
     "genetically proxied consumption of sweetened beverages showed no "
     "evidence of a causal association with atrial fibrillation, and the null "
     "estimates exclude moderate-to-large but not small effects. The null "
     "held across five conceptually distinct exposures—including sugar added "
     "to tea or coffee, the closest genetic proxy for milk-tea-type "
     "beverages—three European outcome sources and all complementary "
     "estimators. Three nominal IVW signals emerged, but none survived "
     "scrutiny. East Asian estimates were imprecise but directionally "
     "consistent, and the positive lifestyle control confirmed analytical "
     "sensitivity."),
    ("Beyond previous single-beverage and dietary-exposure",
     "Beyond previous single-beverage and dietary-exposure MR analyses "
     "[8,29,40,41], the present study contributes a unified multi-exposure "
     "framework: five sweetened-beverage phenotypes and their caffeinated "
     "counterparts against the largest public AF GWAS, with adiposity "
     "modelled jointly, locus-level colocalization and an East Asian "
     "contextual arm. Our findings diverge from the two UK Biobank cohort "
     "analyses reporting 10–20% higher incident AF risk among high consumers "
     "of SSBs or ASBs [2,3], and from a smaller MR study reporting a positive "
     "SSB–AF association (OR 1.023, 1.007–1.038; P = 0.0039) [29] that used "
     "an outcome GWAS one-sixteenth the size of ours (3,818 cases), a relaxed "
     "instrument threshold (P < 10⁻⁵) and no adiposity modelling; our "
     "multivariable, colocalization and CAUSE analyses argue against a causal "
     "interpretation of that signal. The divergence is plausibly reconciled "
     "by residual confounding—sweetened-beverage consumers differ "
     "systematically in adiposity, diet quality and lifestyle, and our "
     "analyses show adiposity-related pathways accounting for the only "
     "nominal genetic signal—by MR's lifelong-average estimand versus the "
     "mid-life exposure window of cohorts, and by limited power for small "
     "effects."),
    ("For coffee, the literature is mixed.",
     "For coffee, the literature is mixed. A previous, smaller MR study "
     "reported no causal coffee–AF association [8]; observational, "
     "acute-exposure randomized and recent genetic evidence points to no harm "
     "[4,9,30,31], although healthy-user bias may colour inverse estimates "
     "[10]. Our nominal IVW association does not overturn that consensus: it "
     "was heterogeneous, non-robust to sensitivity estimators, attenuated "
     "once BMI was modelled jointly and source-dependent—null after outlier "
     "correction in Nielsen 2018 but retained in FinnGen R13. Colocalization "
     "reinforced this reading: the coffee signal had no AF counterpart at the "
     "CYP1A1–CYP1A2 and AHR loci (PP.H4 ≤ 0.008) but shared a causal variant "
     "with AF at FTO (PP.H4 = 0.894; replicated at 0.906); tea showed the "
     "same dissociation (Table S21), and caffeine-metabolism-locus "
     "instruments were null while the remainder carried the signal. "
     "Consumption-based instruments index intake behaviour and its correlates "
     "rather than circulating caffeine [32], and plasma-caffeine MR links "
     "caffeine itself to lower adiposity [33], reinforcing that the adiposity "
     "pathway captured here reflects beverage-drinking patterning, not "
     "caffeine pharmacology. On balance, the genetic evidence does not "
     "establish a causal effect of habitual coffee intake on AF in either "
     "direction, although the heterogeneous estimates preclude a definitive "
     "null. This reading aligns with the 2026 American Heart Association "
     "statement, which left caffeine-metabolism effect modification "
     "unresolved [10]; our locus-level analyses speak directly to that gap."),
    ("The BMI positive control",
     "The BMI positive control (OR 1.47 per SD) reaffirms adiposity as a "
     "central causal determinant of AF and offers a parsimonious explanation "
     "for the observational literature: habitual SSB intake promotes weight "
     "gain, and the resulting adiposity, rather than the beverage per se, "
     "increases AF risk via atrial remodelling, epicardial fat and "
     "hypertension. Two-step mediation MR quantified this pathway (Table "
     "S16), FTO colocalization provided locus-level corroboration, and the "
     "positive genetic correlations of SSB and ASB intake with AF (rg = "
     "0.24–0.31, q < 0.05) alongside null MR estimates exemplify the "
     "distinction between shared architecture and causation. This distinction "
     "shifts preventive emphasis towards weight management and dietary "
     "pattern [1]."),
    ("Most fundamentally",
     "Most fundamentally, the component-proxy design estimates the marginal, "
     "lifelong effects of individual ingredients rather than the effect of "
     "the composite beverage: a null for sugar, caffeine and tea does not "
     "entail a null for milk tea, which additionally entails possible "
     "sugar–caffeine interaction, non-instrumented constituents (non-dairy "
     "creamer; high-glycaemic-index toppings) and an acute per-serving "
     "character that lies outside a per-category lifelong estimand. The acute "
     "time window and dose–response shape are questions for randomized "
     "ambulatory-monitoring designs [30]."),
    ("Current genetic evidence",
     "Current genetic evidence does not support sweetened beverage intake as "
     "a direct causal determinant of AF; it offers no direct evidence "
     "implicating milk-tea-type beverages, but cannot exclude effects of the "
     "magnitude reported observationally. At the trigger level, randomized "
     "acute coffee exposure found no excess of atrial arrhythmias [30], "
     "although case reports link high-dose energy drinks to acute AF in "
     "young, low-risk individuals [35]. Our null accords with US guideline "
     "advice against recommending caffeine avoidance to prevent AF [36]. "
     "This conclusion is not a verdict of safety: the cardiometabolic case "
     "for limiting added sugar and sweeteners rests on evidence far beyond "
     "AF, including genetic analyses linking artificial sweeteners to "
     "cardiometabolic disease [38]. For young East Asian consumers, the "
     "AF-prevention message remains the established one—healthy weight, "
     "limited alcohol, cardiometabolic risk control [1]—and prospective "
     "studies measuring milk tea intake directly in East Asian cohorts remain "
     "a priority."),
    ("Strengths include",
     "Strengths include a causal-inference design with multiple complementary "
     "estimators, the largest public European-ancestry AF GWAS, pre-specified "
     "multiplicity control, multivariable modelling and locus-level "
     "colocalization, a positive lifestyle control and an East Asian "
     "contextual arm. Several limitations merit emphasis. First, no GWAS "
     "measures milk tea itself: the component-proxy strategy assumes that "
     "instrumented sweetening behaviour approximates the exposure of "
     "interest, ordinal phenotypes scale estimates per intake category rather "
     "than per gram, and MR indexes lifelong average exposure, so acute "
     "triggering, post-ablation recurrence and any J-shaped dose–response lie "
     "outside the estimand [10]. Second, instruments for the five "
     "sub-phenotypes were selected at a relaxed threshold (P < 5 × 10⁻⁶); "
     "although all F statistics exceeded 20 (Table S22), F captures neither "
     "winner's curse nor correlated pleiotropy, and two sub-phenotypes lack "
     "public full summary statistics, so residual weak-instrument bias cannot "
     "be formally excluded; the concordant MR-RAPS (Table S23) and MRlap "
     "estimates (difference P > 0.05; Table S17) mitigate this concern. "
     "Third, the instruments derive from European-ancestry adults, whereas "
     "the target consumers are young East Asians; the BioBank Japan analysis "
     "is subject to cross-ancestry mismatch and its wide intervals make it "
     "supportive context only, and the early-onset AF analysis was "
     "underpowered to exclude moderate effects [37]. Fourth, diagnostic codes "
     "under-detect paroxysmal AF, and the FinnGen I9_AF endpoint pools AF "
     "with atrial flutter (ICD-10 I48), so FinnGen-specific estimates are not "
     "AF-exclusive. Fifth, UK Biobank participants contribute to both the "
     "exposure GWAS and Nielsen 2018; with all F statistics above 20 this "
     "bias should be minimal, and the cross-trait LDSC intercept for coffee × "
     "Nielsen 2018 (−0.011, SE 0.008) was indistinguishable from zero whereas "
     "it readily detected the known coffee–tea overlap (−0.318, SE 0.011). "
     "Finally, the multivariable estimates rest on conditionally modest "
     "instruments (conditional F 1.3–7.5; Table S24) and are biased towards "
     "the null under weak identification, mediation MR was a mechanistic "
     "probe under the usual product-method assumptions, and the deferred "
     "NHANES triangulation would have been uninformative by design "
     "(public-use NHANES lacks validated AF ascertainment)."),
    ("Genetically proxied consumption of sweetened beverages—including",
     "Genetically proxied consumption of sweetened beverages—including the "
     "sugar component of tea- and coffee-based drinks, the closest available "
     "proxy for milk-tea-type beverages—showed no evidence of a causal "
     "association with atrial fibrillation in European or East Asian "
     "populations: moderate-to-large effects are excluded, but small effects, "
     "and milk-tea exposure itself, remain untested. A positive lifestyle "
     "control confirmed that the design detects established causal effects. "
     "The modest observational association between sweetened beverages and "
     "incident AF is more plausibly explained by residual confounding, "
     "including adiposity, than by a direct causal effect of beverage sugar. "
     "Prevention is better directed at established cardiometabolic risk "
     "factors; direct investigation of milk tea consumption in prospective "
     "East Asian cohorts is needed to close the remaining evidence gap."),
    # ---------------- figure legends ----------------
    ("Figure 1. Study design flowchart: exposure GWAS",
     "Figure 1. Study design: exposure and outcome GWAS, instrument selection "
     "and analytic layers."),
    ("Figure 2. Forest plot of IVW estimates",
     "Figure 2. Forest plot of IVW estimates for each beverage exposure "
     "against atrial fibrillation, by outcome source, with European "
     "fixed-effect meta-analysis (Nielsen 2018 + FinnGen R13)."),
    ("Figure S1. Leave-one-out and funnel plots for every exposure",
     "Figure S1. Leave-one-out and funnel plots for exposure–source "
     "combinations with a nominal IVW association."),
    ("Figure S2. Forest plot of cross-trait LDSC",
     "Figure S2. Cross-trait LDSC genetic correlations (rg) between beverage "
     "intake and atrial fibrillation, with validation controls."),
]

WC_BLOCK = """children.push(
  para(run(T`Word count (title page, main text, keywords, declarations and figure legends; excluding abstract, tables and references): 0000`, { size: 18, color: palette.light }), {
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 }
  })
);

"""


def main():
    # ---- manuscript ----
    mp = BLD / "build_manuscript_v51.js"
    shutil.copy(mp, str(mp) + ".bak_nmcd")
    src = mp.read_text(encoding="utf-8")

    pat_lay = re.compile(
        r"// ---------- Lay summary ----------.*?(?=// ---------- Introduction)",
        re.S)
    assert len(pat_lay.findall(src)) == 1, "lay summary block not unique"
    src = pat_lay.sub("", src)

    pat_res = re.compile(
        r"\s*mix\(\[\s*T`Results: No sweetened-beverage exposure[^`]*`,?\s*\]\),",
        re.S)
    assert len(pat_res.findall(src)) == 1, "abstract results block not unique"
    src = pat_res.sub("", src)

    for anchor, new in REPL:
        src = sub_literal(src, anchor, new)

    marker = "// ---------- Abstract ----------"
    assert src.count(marker) == 1
    src = src.replace(marker, WC_BLOCK + marker)

    mp.write_text(src, encoding="utf-8")
    print("manuscript build script patched")

    # ---- supplement title ----
    sp = BLD / "build_supplement_v51.js"
    shutil.copy(sp, str(sp) + ".bak_nmcd")
    s = sp.read_text(encoding="utf-8")
    assert s.count(OLD_TITLE) == 1, "supplement title not unique"
    s = s.replace(OLD_TITLE, NEW_TITLE)
    sp.write_text(s, encoding="utf-8")
    print("supplement title patched")

    # ---- cover letter title ----
    cp = BLD / "build_cover_letter_v51.js"
    shutil.copy(cp, str(cp) + ".bak_nmcd")
    c = cp.read_text(encoding="utf-8")
    assert c.count(OLD_TITLE) == 1, "cover-letter title not unique"
    c = c.replace(OLD_TITLE, NEW_TITLE)
    cp.write_text(c, encoding="utf-8")
    print("cover letter title patched")

    print("ALL PATCHES APPLIED")


if __name__ == "__main__":
    main()
