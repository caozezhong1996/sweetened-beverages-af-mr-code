# -*- coding: utf-8 -*-
"""patch_v51_nmcd_compress3.py — third-pass surgical trims (NMCD <=4000)."""
import re
import shutil
from pathlib import Path

BASE = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822")
BLD = BASE / "04_docx构建脚本"


def sub_literal(text, anchor, new_inner):
    pat = re.compile(r"T`[^`]*" + re.escape(anchor) + r"[^`]*`", re.S)
    n = len(pat.findall(text))
    if n != 1:
        raise SystemExit(f"ANCHOR NOT UNIQUE ({n}): {anchor[:70]}")
    return pat.sub(lambda m: "T`" + new_inner + "`", text, count=1)


REPL = [
    ("Word count (title page, main text, keywords",
     "Word count: 0000"),
    # ---------------- introduction ----------------
    ("Bubble (milk) tea—typically",
     "Bubble (milk) tea—typically 35–50 g of added sugar and 100–200 mg of "
     "caffeine per serving, often with non-dairy creamer or high-fat "
     "toppings—is among the most widely consumed prepared beverages of young "
     "East Asians and is spreading worldwide. No prospective cohort has "
     "measured milk tea directly and no GWAS instruments it; milk-tea-type "
     "beverages motivated, but were not directly evaluated in, this "
     "analysis."),
    ("The closest available evidence concerns",
     "The closest available evidence concerns sugar-sweetened beverages "
     "(SSBs): in 201,856 UK Biobank participants, >2 L/week of SSBs or "
     "artificially sweetened beverages (ASBs) was associated with 10% and "
     "20% higher incident AF risk [2], confirmed in prediabetes and "
     "diabetes [3]; residual confounding cannot be excluded. Previous "
     "Mendelian randomization (MR) analyses examined single beverages in "
     "smaller outcome resources, without adiposity modelling or East Asian "
     "context [8,29,40]."),
    ("For caffeine, the second major",
     "For caffeine, the second major bioactive component of milk tea, "
     "habitual coffee was inversely associated with incident AF in large "
     "cohorts [4,5,6] and a meta-analysis [7]; an MR analysis found no "
     "causal coffee–AF association [8]; and the randomized DECAF trial found "
     "no increase in AF recurrence [9]. A 2026 American Heart Association "
     "scientific statement reached the same conclusion and prioritized "
     "disentangling caffeine from beverage co-ingredients [10]."),
    # ---------------- methods ----------------
    ("Outcome data.",
     "Outcome data. The primary outcome was the largest public "
     "European-ancestry AF GWAS (Nielsen et al. [13]; 60,620 cases, 970,216 "
     "controls; ebi-a-GCST006414); a larger cross-population meta-analysis "
     "is not public (GCST90624413) [16]. FinnGen R13 [15] (I9_AF; 67,783 "
     "cases, 241,269 controls) shares no participants with UK Biobank and "
     "served as co-primary; AFGen 2018 (55,114 cases) [14], which shares "
     "cohorts with Nielsen 2018, was a sensitivity source. BioBank Japan "
     "(bbj-a-71; 8,180 cases, 28,612 controls) [17] provided East Asian "
     "context, and an early-onset AF outcome (onset <66 years; 2,781 cases, "
     "4,959 controls; GCST010636) served as sensitivity."),
    ("For each exposure, single-nucleotide",
     "Single-nucleotide polymorphisms (SNPs) were clumped to independence "
     "(r² < 0.001, 10,000 kb) with ancestry-matched linkage-disequilibrium "
     "references. Coffee and tea instruments were genome-wide significant "
     "(P < 5 × 10⁻⁸); for the five sub-phenotypes, fewer than three variants "
     "reached that threshold, so the pre-specified relaxed threshold (P < 5 "
     "× 10⁻⁶) was used (revisited in Limitations). Palindromic variants with "
     "intermediate allele frequencies were excluded; per-variant F "
     "statistics above 10 were required; identical instrument lists were "
     "used across outcome sources. Because phenotypes are ordinal "
     "categories, estimates scale per one-category increment in instrumented "
     "intake."),
    ("Robustness, directionality and power.",
     "Robustness, directionality and power. Causal direction was verified "
     "by Steiger testing and per-variant filtering. Additional robust "
     "estimators comprised radial IVW, the contamination-mixture estimator "
     "[24] and MR-RAPS [39] (all seven exposures, both co-primary outcomes); "
     "genome-wide CAUSE [25] distinguished correlated pleiotropy from "
     "causation while modelling sample overlap; and MRlap [26] jointly "
     "corrected the coffee and tea estimates for overlap, winner's curse "
     "and weak-instrument bias (Table S17). Leave-one-out and funnel plots "
     "assessed influential instruments; reverse MR (111 AF-associated SNPs) "
     "tested reverse causation; atrioventricular block (I9_AVBLOCK) was the "
     "negative outcome control (Table S18). Power was quantified as the "
     "minimum detectable odds ratio (80% power). Locus-level colocalization "
     "(coloc.abf, default priors) covered 500-kb windows around CYP1A1–"
     "CYP1A2, AHR and FTO (caffeine-metabolism and adiposity loci), with "
     "prior p12 varied from 10⁻⁶ to 5 × 10⁻⁵."),
    ("As a pleiotropy-sensitive complement",
     "As a pleiotropy-sensitive complement to MR and a diagnostic of sample "
     "overlap, cross-trait linkage disequilibrium score (LDSC) regression "
     "[27,28] used HapMap 3 European LD scores (M = 1,290,027 SNPs), Neale "
     "lab round-2 full summary statistics for five beverage traits (fields "
     "1498, 1488, 100370, 100170, 100160) and AF statistics from Nielsen "
     "2018 and FinnGen R13. Cross-trait intercepts diagnosed overlap-driven "
     "bias; Benjamini–Hochberg correction covered the ten beverage–AF rg "
     "tests; same-trait and overlap controls validated the implementation. "
     "Full statistics for sugar and artificial sweetener added to tea are "
     "not public, precluding their LDSC."),
    ("Two-step mediation MR through metabolic traits",
     "Two-step mediation MR and locus-level colocalization were "
     "pre-specified as conditional on a robust total effect; because only "
     "coffee showed a nominal signal, they were performed for coffee during "
     "revision as mechanistic probes, and the pre-specified NHANES "
     "triangulation was deferred. A further deviation was the revision-stage "
     "upgrade of the primary outcome from AFGen 2018 to Nielsen 2018, with "
     "all analyses repeated."),
    # ---------------- results ----------------
    ("None of the five",
     "None of the five sweetened-beverage exposures showed evidence of a "
     "causal association with AF in any European source or in the "
     "meta-analyses (Table 2; Figure 2). Nielsen 2018 IVW odds ratios (ORs) "
     "were 0.91 (95% CI 0.72–1.17) for sugar added to tea, 0.91 (0.67–1.22) "
     "for fizzy drinks, 0.99 (0.86–1.13) for low-calorie drinks and 0.91 "
     "(0.72–1.14) for artificial sweetener (all P ≥ 0.40); fixed-effect "
     "meta-analyses were concordantly null (all P ≥ 0.060), as were all "
     "sensitivity estimators (Table 3; Table S2); upper meta-analytic "
     "confidence bounds (≤1.17) exclude the observational effect sizes "
     "(1.1–1.2). One exception emerged: sugar added to tea showed a nominal "
     "inverse association in FinnGen R13 (OR 0.60; P = 0.014), unsupported "
     "by the weighted median (P = 0.061), absent elsewhere (P > 0.21), "
     "significantly heterogeneous (Q P = 8 × 10⁻⁶; between-source I² = 67%) "
     "and attenuated in the meta-analysis (OR 0.77; P = 0.20); we attribute "
     "it to chance."),
    ("Sugar added to coffee showed",
     "Sugar added to coffee showed a nominal inverse association in AFGen "
     "2018 (OR 0.81; P = 0.030) that did not replicate in the nearly "
     "twice-larger primary outcome (P = 0.33) or FinnGen R13 (P = 0.53), was "
     "null under weighted-median and MR-Egger estimators, and yielded a null "
     "meta-analysis (OR 0.88; P = 0.25)—a chance finding consistent with "
     "winner's curse."),
    ("Two-step mediation MR attributed",
     "Two-step mediation MR attributed the nominal signal to adiposity: "
     "coffee intake increased BMI (β = 0.82 SD; P = 0.007), BMI increased "
     "AF (β = 0.343 per SD; P = 2 × 10⁻³⁸), and the indirect effect (0.281, "
     "0.073–0.490) was similar in magnitude to the total association "
     "(mediated proportion 120%, −23% to 263%; >100% reflects an imprecise "
     "total effect), leaving a null direct effect (Table S16). The MRlap "
     "overlap-corrected estimate did not differ from the observed one "
     "(difference P = 0.07; Table S17). An independent coffee GWAS (field "
     "1498) was concordantly null (OR 1.18, 0.93–1.50; P = 0.166; "
     "cross-GWAS meta-analysis OR 1.23, 1.04–1.44; P = 0.013; Table S19), "
     "and BMI re-instrumented in the Neale GWAS (33 of 34 instruments; β = "
     "0.75 SD) reproduced the mediation (109%; Table S16)."),
    ("MR-RAPS estimates, robust to many weak",
     "MR-RAPS estimates, robust to many weak and pleiotropic instruments, "
     "were directionally consistent with the primary analysis for all 14 "
     "pairs (Table S23): every exposure was null against Nielsen 2018, "
     "including coffee (0.17, P = 0.11), whereas the nominal coffee (0.41, "
     "P = 0.045) and inverse sugar-added-to-tea (−0.37, P = 0.032) signals "
     "persisted only in FinnGen R13; all other tests were null (P ≥ 0.51). "
     "Reverse MR found no evidence that AF liability influences beverage "
     "consumption (111 SNPs; all P ≥ 0.054; Table S7)."),
    ("As a locus-level probe",
     "Around the three strongest coffee-instrument loci (Table S8), "
     "colocalization supported a coffee-only association at CYP1A1–CYP1A2 "
     "and AHR (PP.H1 = 0.957 and 0.931; PP.H4 ≤ 0.008): coffee-specific "
     "variation at these caffeine-handling loci has no AF counterpart. At "
     "FTO, there was strong evidence of a shared causal variant with AF "
     "(PP.H4 = 0.894; FinnGen R13 0.906), robust to the prior (PP.H4 > 0.8 "
     "for p12 ≥ 5 × 10⁻⁶; Table S13), directly implicating adiposity-linked "
     "pleiotropy. Tea intake showed the identical dissociation (PP.H1 = "
     "0.993 and 0.988; FTO PP.H4 = 0.896; Table S21). Instruments restricted "
     "to the caffeine-metabolism windows were null in both European sources "
     "(P ≥ 0.44), whereas the remaining 31 instruments carried the signal "
     "(OR 1.50–1.96; P ≤ 0.009)."),
    ("Cross-trait LDSC provided",
     "Cross-trait LDSC provided an exposure-wide view of shared genetic "
     "architecture (Table S10; Table S11; Figure S2). All five beverage "
     "traits showed detectable SNP heritability (h² = 0.020–0.063). Against "
     "FinnGen R13, positive genetic correlations with AF survived FDR "
     "correction for fizzy drink intake (rg = 0.239, SE 0.089; q = 0.035) "
     "and low-calorie drink intake (rg = 0.313, SE 0.103; q = 0.025), with "
     "directionally similar null estimates against Nielsen 2018; coffee "
     "intake showed a weak trend (rg ≤ 0.075), and tea intake and sugar "
     "added to coffee were null. Positive rg alongside null MR estimates "
     "indicates shared architecture—such as adiposity-related biology—rather "
     "than causation. Cross-trait intercepts were null for all ten pairs "
     "(|intercept| ≤ 0.018); the diagnostic detected the known coffee–tea "
     "overlap (−0.318, SE 0.011; coffee × Nielsen 2018 −0.011), and the "
     "same-trait control returned rg = 0.923."),
    ("In BioBank Japan",
     "In BioBank Japan (8,180 cases), all sweetened-beverage exposures were "
     "null with wide confidence intervals (Table 2; Figure 2). Coffee intake "
     "was nominally associated (OR 2.34, 1.17–4.68; P = 0.016) with null "
     "weighted-median and MR-Egger estimates, mirroring the fragile European "
     "pattern; given European-ancestry instruments, these estimates are "
     "context, not independent evidence."),
    ("All seven phenotypes were null against early-onset",
     "All seven phenotypes were null against early-onset AF (2,781 cases; "
     "IVW P ≥ 0.11; null Egger intercepts), and the nominal coffee "
     "association did not persist (Table S20)."),
    ("As a positive control",
     "As a positive control, the identical pipeline was applied to alcohol "
     "(Table S5). Genetically instrumented drinks per week (GSCAN; 33 SNPs) "
     "were directionally associated with higher AF odds in all four cohorts "
     "(ORs 1.12–2.25; European meta-analysis OR 1.19; P = 0.035); intake "
     "frequency (97 SNPs) was null (P ≥ 0.12). Detecting the alcohol signal "
     "argues against general insensitivity explaining the null beverage "
     "findings."),
    ("Against atrioventricular block (Table S18)",
     "Against atrioventricular block (Table S18), six of nine tests were "
     "null (P ≥ 0.53); nominal associations for alcohol intake frequency "
     "(P = 0.043) and coffee (P = 0.042) did not survive Bonferroni "
     "correction, whereas the inverse sugar-added-to-tea association (P = "
     "0.001) did. Because atrioventricular block shares adiposity-mediated "
     "aetiology with AF, this pattern most plausibly reflects shared "
     "adiposity pleiotropy rather than beverage-specific effects "
     "(Limitations)."),
    # ---------------- discussion ----------------
    ("In this two-sample and multivariable",
     "In this two-sample and multivariable Mendelian randomization study "
     "using the largest public European-ancestry AF GWAS, genetically "
     "proxied consumption of sweetened beverages showed no evidence of a "
     "causal association with atrial fibrillation, and the null estimates "
     "exclude moderate-to-large but not small effects. The null held across "
     "five distinct exposures—including sugar added to tea or coffee, the "
     "closest genetic proxy for milk-tea-type beverages—three European "
     "outcome sources and all complementary estimators; three nominal IVW "
     "signals emerged, but none survived scrutiny."),
    ("For coffee, the literature is mixed.",
     "For coffee, the literature is mixed. A previous, smaller MR study "
     "reported no causal coffee–AF association [8]; observational, "
     "acute-exposure randomized and recent genetic evidence points to no "
     "harm [4,9,30,31], although healthy-user bias may colour inverse "
     "estimates [10]. Our nominal IVW association does not overturn that "
     "consensus: it was heterogeneous, non-robust to sensitivity estimators, "
     "attenuated once BMI was modelled jointly and source-dependent. "
     "Colocalization reinforced this reading: no AF counterpart at the "
     "CYP1A1–CYP1A2 and AHR loci (PP.H4 ≤ 0.008), a shared causal variant "
     "with AF at FTO, and null caffeine-metabolism-locus instruments while "
     "the remainder carried the signal. Consumption-based instruments index "
     "intake behaviour rather than circulating caffeine [32], and "
     "plasma-caffeine MR links caffeine itself to lower adiposity [33]; the "
     "adiposity pathway captured here therefore reflects beverage-drinking "
     "patterning, not caffeine pharmacology. On balance, the genetic "
     "evidence establishes no causal coffee–AF effect in either direction, "
     "although heterogeneity precludes a definitive null. This aligns with "
     "the 2026 American Heart Association statement, which left "
     "caffeine-metabolism effect modification unresolved [10]; our "
     "locus-level analyses speak to that gap."),
    ("The BMI positive control",
     "The BMI positive control (OR 1.47 per SD) reaffirms adiposity as a "
     "central causal determinant of AF and offers a parsimonious explanation "
     "for the observational literature: habitual SSB intake promotes weight "
     "gain, and the resulting adiposity, rather than the beverage per se, "
     "increases AF risk via atrial remodelling, epicardial fat and "
     "hypertension. Mediation MR quantified this pathway, FTO colocalization "
     "corroborated it, and the positive genetic correlations of SSB and ASB "
     "intake with AF (rg = 0.24–0.31, q < 0.05) alongside null MR estimates "
     "exemplify shared architecture without a causal beverage effect. "
     "Preventive emphasis therefore shifts towards weight management and "
     "dietary pattern [1]."),
    ("Current genetic evidence",
     "Current genetic evidence does not support sweetened beverage intake "
     "as a direct causal determinant of AF; it offers no direct evidence "
     "implicating milk-tea-type beverages, but cannot exclude effects of "
     "the magnitude reported observationally. At the trigger level, "
     "randomized acute coffee exposure found no excess atrial arrhythmias "
     "[30], although case reports link high-dose energy drinks to acute AF "
     "in young, low-risk individuals [35]; our null accords with US "
     "guideline advice against recommending caffeine avoidance to prevent "
     "AF [36]. This is not a verdict of safety: the cardiometabolic case for "
     "limiting added sugar and sweeteners rests on evidence far beyond AF "
     "[38], and for young East Asian consumers the AF-prevention message "
     "remains healthy weight, limited alcohol and cardiometabolic risk "
     "control [1]. Prospective direct studies of milk tea in East Asian "
     "cohorts remain a priority."),
    ("Strengths include",
     "Strengths include multiple complementary estimators, the largest "
     "public European-ancestry AF GWAS, pre-specified multiplicity control, "
     "multivariable modelling and colocalization, a positive lifestyle "
     "control and an East Asian contextual arm. Several limitations merit "
     "emphasis. First, no GWAS measures milk tea itself: the component-proxy "
     "strategy assumes instrumented sweetening behaviour approximates the "
     "exposure of interest, ordinal phenotypes scale estimates per intake "
     "category, and MR indexes lifelong average exposure, so acute "
     "triggering, post-ablation recurrence and any J-shaped dose–response "
     "lie outside the estimand [10]. Second, sub-phenotype instruments used "
     "a relaxed threshold (P < 5 × 10⁻⁶); although all F statistics exceeded "
     "20 (Table S22), F captures neither winner's curse nor correlated "
     "pleiotropy, and two sub-phenotypes lack public full summary "
     "statistics; the concordant MR-RAPS (Table S23) and MRlap estimates "
     "(difference P > 0.05; Table S17) mitigate, but do not eliminate, this "
     "concern. Third, instruments derive from European-ancestry adults "
     "whereas target consumers are young East Asians; the BioBank Japan "
     "analysis is subject to cross-ancestry mismatch, and the early-onset "
     "analysis was underpowered [37]. Fourth, diagnostic codes under-detect "
     "paroxysmal AF, and the FinnGen I9_AF endpoint pools AF with atrial "
     "flutter (ICD-10 I48). Fifth, UK Biobank contributes to both the "
     "exposure GWAS and Nielsen 2018; with F > 20 overlap bias should be "
     "minimal, and the LDSC intercept for coffee × Nielsen 2018 (−0.011) was "
     "null whereas it detected known coffee–tea overlap (−0.318). Finally, "
     "multivariable estimates rest on conditionally modest instruments "
     "(conditional F 1.3–7.5; Table S24), mediation MR was a mechanistic "
     "probe under product-method assumptions, and the deferred NHANES "
     "triangulation would have been uninformative by design."),
]


def main():
    mp = BLD / "build_manuscript_v51.js"
    shutil.copy(mp, str(mp) + ".bak_nmcd3")
    src = mp.read_text(encoding="utf-8")
    for anchor, new in REPL:
        src = sub_literal(src, anchor, new)
    mp.write_text(src, encoding="utf-8")
    print(f"pass-3 applied: {len(REPL)} replacements")


if __name__ == "__main__":
    main()
