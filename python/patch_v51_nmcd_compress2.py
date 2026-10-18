# -*- coding: utf-8 -*-
"""patch_v51_nmcd_compress2.py — second-pass compression of manuscript v5.1.

Applies to the already pass-1-compressed build_manuscript_v51.js.
Anchors match the pass-1 replacement texts. Backup: *.bak_nmcd2.
"""
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
    # ---------------- introduction ----------------
    ("Milk tea itself has never been studied",
     "Milk tea itself has never been studied as an exposure; the SSB–AF "
     "association lacks causal evidence; and sugar and caffeine have rarely "
     "been examined within one causal framework. Leveraging UK Biobank "
     "beverage-consumption GWAS [11] and the largest public AF GWAS, we "
     "conducted two-sample and multivariable MR of sweetened beverage "
     "consumption (not milk tea itself) and AF, aiming (i) to estimate "
     "causal effects of sweetened-beverage intake, particularly sugar added "
     "to tea or coffee (the closest genetic proxy for milk-tea-type "
     "beverages); (ii) to disentangle sugar- and caffeine-related behaviour "
     "with body mass index (BMI) modelled jointly; (iii) to examine "
     "consistency in an East Asian population; and (iv) to benchmark "
     "sensitivity with alcohol as a positive control."),
    # ---------------- methods ----------------
    ("This study is reported in accordance with the STROBE-MR",
     "This study follows the STROBE-MR checklist [12] and the three core MR "
     "assumptions (robust instrument–exposure association; no common cause "
     "with the outcome; effect on the outcome only through the exposure). "
     "All analyses use publicly available, de-identified GWAS summary "
     "statistics; the analysis plan was finalized before outcome data were "
     "analysed."),
    ("Exposure data.",
     "Exposure data. Instruments for seven beverage phenotypes were obtained "
     "from UK Biobank GWAS (MRC Integrative Epidemiology Unit pipeline, via "
     "OpenGWAS; identifiers in Table 1): sugar added to tea, sugar added to "
     "coffee, fizzy drink intake (sugar-sweetened beverages, SSBs), "
     "low-calorie drink intake (artificially sweetened beverages, ASBs) and "
     "artificial sweetener added to tea (each N = 64,949), coffee intake "
     "(N = 428,860) and tea intake (N = 447,485), all European-ancestry. "
     "Sugar added to tea or coffee is conceptually the closest proxy for "
     "milk-tea-type composite beverages."),
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
     "4,959 controls; GCST010636) served as sensitivity, with score "
     "statistics converted to effect estimates."),
    ("Covariate and positive-control data.",
     "Covariate and positive-control data. BMI statistics came from GIANT "
     "(N = 681,275; ieu-b-40) [18]. Alcohol consumption, an established AF "
     "risk factor [1], served as positive lifestyle control, instrumented "
     "through GSCAN drinks per week (N = 335,394; ieu-b-73) [19] and UK "
     "Biobank alcohol intake frequency (N = 462,346; ukb-b-5779)."),
    ("For each exposure, single-nucleotide",
     "For each exposure, single-nucleotide polymorphisms (SNPs) were clumped "
     "to independence (r² < 0.001, 10,000 kb) with ancestry-matched "
     "linkage-disequilibrium references. Coffee and tea instruments were "
     "genome-wide significant (P < 5 × 10⁻⁸); for the five sub-phenotypes, "
     "fewer than three variants reached that threshold, so the pre-specified "
     "relaxed threshold (P < 5 × 10⁻⁶) was used (revisited in Limitations). "
     "Palindromic variants with intermediate allele frequencies were "
     "excluded; per-variant F statistics above 10 were required; identical "
     "instrument lists were used across outcome sources. Because phenotypes "
     "are ordinal categories, estimates scale per one-category increment in "
     "instrumented intake."),
    ("Univariable MR.",
     "Univariable MR. Random-effects inverse-variance-weighted (IVW) "
     "regression was primary, complemented by MR-Egger, weighted-median and "
     "weighted-mode estimators, Cochran's Q and the MR-Egger intercept; "
     "MR-PRESSO was applied to exposures with a nominal primary-outcome "
     "association. Nielsen 2018 and FinnGen R13 estimates were combined by "
     "fixed-effect meta-analysis (DerSimonian–Laird sensitivity); AFGen 2018 "
     "was not meta-analysed (shared cohorts with Nielsen 2018). BioBank "
     "Japan estimates are contextual, not independent replication "
     "(European-ancestry instruments)."),
    ("Multiplicity.",
     "Multiplicity. The seven European meta-analytic IVW tests formed the "
     "primary family (Benjamini–Hochberg q = 0.05); all other analyses were "
     "supportive. Analyses used R 4.6.0 with TwoSampleMR [22], MRPRESSO [23] "
     "and coloc; code is archived at https://doi.org/10.5281/zenodo.22099675."),
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
     "minimum detectable odds ratio at 80% power. Locus-level colocalization "
     "(coloc.abf, default priors; PP.H4 > 0.8 = shared variant) covered "
     "500-kb windows around CYP1A1–CYP1A2, AHR and FTO—the "
     "caffeine-metabolism and adiposity loci—with prior p12 varied from 10⁻⁶ "
     "to 5 × 10⁻⁵."),
    ("As a pleiotropy-sensitive complement",
     "As a pleiotropy-sensitive complement to MR and a diagnostic of sample "
     "overlap, cross-trait linkage disequilibrium score (LDSC) regression "
     "[27,28] used 1000 Genomes European HapMap 3 LD scores (M = 1,290,027 "
     "SNPs), Neale lab UK Biobank round-2 full summary statistics for five "
     "beverage traits (fields 1498, 1488, 100370, 100170, 100160) and AF "
     "statistics from Nielsen 2018 and FinnGen R13. Cross-trait intercepts "
     "diagnosed overlap-driven bias; Benjamini–Hochberg correction (q = "
     "0.05) covered the ten beverage–AF rg tests; same-trait and overlap "
     "controls validated the implementation. Full statistics for sugar and "
     "artificial sweetener added to tea are not public, precluding their "
     "LDSC."),
    ("Two-step mediation MR through metabolic traits",
     "Two-step mediation MR through metabolic traits and locus-level "
     "colocalization were pre-specified as conditional on a robust total "
     "effect; because only coffee showed a nominal signal, they were "
     "performed for coffee during revision as mechanistic probes, and the "
     "pre-specified NHANES triangulation was deferred. A further deviation "
     "was the revision-stage upgrade of the primary outcome from AFGen 2018 "
     "to the nearly twice-larger Nielsen 2018 GWAS, with all analyses "
     "repeated."),
    ("All data are de-identified",
     "All data are de-identified public summary statistics, exempt from "
     "ethics review per the Chinese Measures for Ethical Review of Life "
     "Science and Medical Research Involving Human Subjects (Article 32, "
     "2023); FinnGen, BioBank Japan and OpenGWAS data were used under their "
     "terms."),
    # ---------------- results ----------------
    ("Between 8 and 34",
     "Between 8 and 34 independent SNPs per exposure were available (median "
     "17; Table 2), with identical lists across outcome sources; all "
     "per-variant F statistics exceeded 20 (Table S22)."),
    ("None of the five",
     "None of the five sweetened-beverage exposures showed evidence of a "
     "causal association with AF in any European source or in the "
     "meta-analyses (Table 2; Figure 2). Nielsen 2018 IVW odds ratios (ORs) "
     "were 0.91 (95% CI 0.72–1.17) for sugar added to tea, 0.91 (0.67–1.22) "
     "for fizzy drinks, 0.99 (0.86–1.13) for low-calorie drinks and 0.91 "
     "(0.72–1.14) for artificial sweetener (all P ≥ 0.40); fixed-effect "
     "meta-analyses were concordantly null (all P ≥ 0.060), as were all "
     "sensitivity estimators (Table 3; Table S2), and upper meta-analytic "
     "confidence bounds (≤1.17) exclude the effect sizes reported "
     "observationally (1.1–1.2). One exception emerged: sugar added to tea "
     "showed a nominal inverse association in FinnGen R13 (OR 0.60; P = "
     "0.014) that was unsupported by the weighted median (P = 0.061), absent "
     "from the other sources (P > 0.21), significantly heterogeneous (Q P = "
     "8 × 10⁻⁶; between-source I² = 67%) and attenuated in the meta-analysis "
     "(OR 0.77; P = 0.20); we attribute it to chance."),
    ("Sugar added to coffee showed",
     "Sugar added to coffee showed a nominal inverse association in AFGen "
     "2018 (OR 0.81, 0.66–0.98; P = 0.030) that did not replicate in the "
     "nearly twice-larger primary outcome (P = 0.33) or FinnGen R13 (P = "
     "0.53), was null under weighted-median and MR-Egger estimators, and "
     "yielded a null meta-analysis (OR 0.88; P = 0.25)—a chance finding "
     "consistent with winner's curse."),
    ("Coffee intake was nominally associated with higher AF odds",
     "Coffee intake was nominally associated with higher AF odds (Nielsen "
     "2018 OR 1.26; P = 0.036; AFGen 2018 OR 1.26, P = 0.031; FinnGen R13 "
     "OR 1.58; P = 0.016; European meta-analysis OR 1.34, 1.11–1.62; P = "
     "0.002, surviving Benjamini–Hochberg correction). It nevertheless "
     "failed every pre-specified consistency criterion: significant "
     "heterogeneity (Cochran's Q P = 9 × 10⁻⁴ and 4 × 10⁻¹⁰), null "
     "weighted-median and MR-Egger estimates, and significant MR-PRESSO "
     "global tests, with outlier correction resolving to the null in Nielsen "
     "2018 (P = 0.20) but not FinnGen R13 (β = 0.345; P = 0.007). The "
     "contamination-mixture estimator gave the same source-dependent pattern "
     "(Nielsen 2018 β = 0.068, −0.136 to 0.564; FinnGen R13 β = 0.689, "
     "0.257–0.958; Table S14), and genome-wide CAUSE (1,081,418 shared "
     "variants) found correlated pleiotropy explained the overlap as well as "
     "a causal model (P = 0.53; causal effect γ = 0.01, −0.01 to 0.04; Table "
     "S15). A small genuine effect cannot be excluded."),
    ("Two-step mediation MR attributed",
     "Two-step mediation MR attributed the nominal signal to adiposity: "
     "coffee intake increased BMI (β = 0.82 SD; P = 0.007), BMI increased "
     "AF (β = 0.343 per SD; P = 2 × 10⁻³⁸), and the indirect effect (0.281, "
     "0.073–0.490) was similar in magnitude to the total association "
     "(mediated proportion 120%, −23% to 263%; proportions above 100% "
     "reflect an imprecise total effect), leaving a null direct effect "
     "(Table S16). The MRlap overlap-corrected estimate did not differ from "
     "the observed one (difference P = 0.07; Table S17). An independent "
     "coffee GWAS (field 1498) gave a concordant non-significant estimate "
     "(OR 1.18, 0.93–1.50; P = 0.166), with a cross-GWAS meta-analytic OR of "
     "1.23 (1.04–1.44; P = 0.013; Table S19); BMI re-instrumented in the "
     "Neale GWAS (33 of 34 instruments; β = 0.75 SD) reproduced the "
     "mediation (109%; Table S16)."),
    ("In MVMR including",
     "In MVMR including coffee intake, sugar added to tea and BMI (Table "
     "4), BMI retained a robust direct effect (OR 1.47 per SD, 1.37–1.57; P "
     "= 2.0 × 10⁻²⁷), a positive control, whereas the nominal coffee "
     "association attenuated (OR 0.82, 0.65–1.04; P = 0.099), consistent "
     "with adiposity confounding; the single-instrument estimate for sugar "
     "added to tea is uninformative (OR 0.99; P = 0.96). Conditional F "
     "statistics were below the conventional threshold of 10 (coffee 5.2; "
     "sugar added to tea 1.3; BMI 7.5; Table S24); weak conditional "
     "instruments bias multivariable estimates towards the null, so these "
     "estimates are supportive rather than definitive."),
    ("Steiger directionality testing supported",
     "Steiger directionality testing supported the exposure-to-outcome "
     "direction for all exposures (P < 10⁻³⁴; Table S6), and radial IVW "
     "reproduced the primary estimates (Table S7)."),
    ("MR-RAPS estimates, robust to many weak",
     "MR-RAPS estimates, robust to many weak and pleiotropic instruments, "
     "were directionally consistent with the primary analysis for all 14 "
     "exposure–outcome pairs (Table S23): every exposure was null against "
     "Nielsen 2018, including coffee (0.17, P = 0.11), whereas the nominal "
     "coffee (0.41, P = 0.045) and inverse sugar-added-to-tea (−0.37, P = "
     "0.032) signals persisted only in FinnGen R13; all other tests were "
     "null (P ≥ 0.51). Reverse MR found no evidence that AF liability "
     "influences beverage consumption (111 SNPs; all P ≥ 0.054; Table S7)."),
    ("Statistical power was limited",
     "Statistical power was limited for small effects (Table S12): minimum "
     "detectable odds ratios at 80% power ranged from 1.15 to 1.53, and "
     "power to detect the observational effect size (OR 1.10) was 9–47%. The "
     "nulls therefore exclude moderate-to-large but not small effects."),
    ("As a locus-level probe",
     "As a locus-level probe of the nominal coffee signal, colocalization "
     "was performed around its three strongest-instrument loci (Table S8). "
     "At CYP1A1–CYP1A2 and AHR, posterior probabilities supported a "
     "coffee-only association (PP.H1 = 0.957 and 0.931; PP.H4 ≤ 0.008): "
     "coffee-specific variation at these caffeine-handling loci has no AF "
     "counterpart. At FTO, there was strong evidence of a shared causal "
     "variant with AF (PP.H4 = 0.894; FinnGen R13 0.906), robust to the "
     "prior (PP.H4 > 0.8 for p12 ≥ 5 × 10⁻⁶; Table S13), directly "
     "implicating adiposity-linked pleiotropy. Tea intake showed the "
     "identical dissociation (PP.H1 = 0.993 and 0.988; FTO PP.H4 = 0.896; "
     "Table S21). Instruments restricted to the caffeine-metabolism windows "
     "were null in both European sources (P ≥ 0.44), whereas the remaining "
     "31 instruments carried the signal (OR 1.50–1.96; P ≤ 0.009)."),
    ("Cross-trait LDSC provided",
     "Cross-trait LDSC provided an exposure-wide view of shared genetic "
     "architecture (Table S10; Table S11; Figure S2). All five beverage "
     "traits showed detectable SNP heritability (h² = 0.020–0.063). Against "
     "FinnGen R13, positive genetic correlations with AF survived FDR "
     "correction for fizzy drink intake (rg = 0.239, SE 0.089; q = 0.035) "
     "and low-calorie drink intake (rg = 0.313, SE 0.103; q = 0.025), with "
     "directionally similar non-significant estimates against Nielsen 2018; "
     "coffee intake showed a weak trend (rg ≤ 0.075), and tea intake and "
     "sugar added to coffee were null. Positive rg alongside null MR "
     "estimates indicates shared architecture—such as adiposity-related "
     "biology—rather than causation. Cross-trait intercepts were null for "
     "all ten pairs (|intercept| ≤ 0.018); the diagnostic detected the known "
     "coffee–tea overlap (−0.318, SE 0.011; coffee × Nielsen 2018 −0.011), "
     "and the same-trait control returned rg = 0.923."),
    ("As a positive control",
     "As a positive control, the identical pipeline was applied to alcohol "
     "(Table S5). Genetically instrumented drinks per week (GSCAN; 33 SNPs) "
     "were directionally associated with higher AF odds in all four cohorts "
     "(ORs 1.12–2.25), with a nominally significant European meta-analysis "
     "(OR 1.19; P = 0.035); intake frequency (97 SNPs) was null throughout "
     "(P ≥ 0.12). Detecting the alcohol signal argues against general "
     "insensitivity explaining the null beverage findings."),
    ("Against atrioventricular block (Table S18)",
     "Against atrioventricular block (Table S18), six of nine exposure "
     "tests were null (P ≥ 0.53); nominal associations for alcohol intake "
     "frequency (P = 0.043) and coffee (P = 0.042) did not survive "
     "Bonferroni correction, whereas the inverse sugar-added-to-tea "
     "association (P = 0.001) did. Because atrioventricular block shares "
     "adiposity-mediated aetiology with AF, this pattern most plausibly "
     "reflects shared adiposity pleiotropy rather than beverage-specific "
     "effects (Limitations)."),
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
     "signals emerged, but none survived scrutiny. The positive lifestyle "
     "control confirmed analytical sensitivity."),
    ("Beyond previous single-beverage and dietary-exposure",
     "Beyond previous single-beverage and dietary-exposure MR analyses "
     "[8,29,40,41], this study provides a unified multi-exposure framework: "
     "five sweetened-beverage phenotypes and their caffeinated counterparts "
     "against the largest public AF GWAS, with adiposity modelled jointly, "
     "locus-level colocalization and an East Asian contextual arm. Our nulls "
     "diverge from UK Biobank cohort estimates of 10–20% higher incident AF "
     "risk among high SSB/ASB consumers [2,3], and from a smaller MR "
     "reporting a positive SSB–AF association (OR 1.023; P = 0.0039) [29] "
     "using an outcome GWAS one-sixteenth the size of ours (3,818 cases), a "
     "relaxed instrument threshold and no adiposity modelling; our "
     "multivariable, colocalization and CAUSE analyses argue against a "
     "causal interpretation of that signal. The divergence is plausibly "
     "reconciled by residual confounding—our analyses show adiposity "
     "accounting for the only nominal signal—by MR's lifelong-average "
     "estimand versus mid-life cohort exposure, and by limited power for "
     "small effects."),
    ("Genetic instruments for self-reported",
     "Genetic instruments for self-reported beverage intake are not "
     "molecule-specific: they index intake behaviour together with its "
     "adiposity, dietary-quality and socioeconomic correlates, so horizontal "
     "pleiotropy is the expectation rather than the exception for traits of "
     "this kind [32,33]. Three features of the design mitigate this concern. "
     "First, such pleiotropy manufactures false-positive signals, not "
     "precise false negatives: the headline estimates are null with "
     "confidence bounds that exclude the observational effect sizes, an "
     "improbable pattern were a moderate causal effect present. Second, the "
     "single nominal signal that did arise was dissected rather than "
     "accepted—source-dependent outlier sensitivity, attenuation once BMI "
     "was modelled jointly, and colocalization confined to the adiposity "
     "locus FTO show the framework detecting and isolating pleiotropy rather "
     "than concealing it. Third, all exposures were re-estimated under "
     "estimators with orthogonal robustness assumptions (weighted median, "
     "contamination mixture, MR-RAPS, CAUSE, MRlap), with concordant "
     "results. We therefore interpret these estimates as effects of the "
     "behaviour cluster the instruments index, not of a molecularly "
     "isolated exposure."),
    ("For coffee, the literature is mixed.",
     "For coffee, the literature is mixed. A previous, smaller MR study "
     "reported no causal coffee–AF association [8]; observational, "
     "acute-exposure randomized and recent genetic evidence points to no "
     "harm [4,9,30,31], although healthy-user bias may colour inverse "
     "estimates [10]. Our nominal IVW association does not overturn that "
     "consensus: it was heterogeneous, non-robust to sensitivity estimators, "
     "attenuated once BMI was modelled jointly and source-dependent. "
     "Colocalization reinforced this reading: the coffee signal had no AF "
     "counterpart at the CYP1A1–CYP1A2 and AHR loci (PP.H4 ≤ 0.008) but "
     "shared a causal variant with AF at FTO, and caffeine-metabolism-locus "
     "instruments were null while the remainder carried the signal. "
     "Consumption-based instruments index intake behaviour rather than "
     "circulating caffeine [32], and plasma-caffeine MR links caffeine "
     "itself to lower adiposity [33]; the adiposity pathway captured here "
     "therefore reflects beverage-drinking patterning, not caffeine "
     "pharmacology. On balance, the genetic evidence establishes no causal "
     "coffee–AF effect in either direction, although heterogeneity precludes "
     "a definitive null. This aligns with the 2026 American Heart "
     "Association statement, which left caffeine-metabolism effect "
     "modification unresolved [10]; our locus-level analyses speak to that "
     "gap."),
    ("The BMI positive control",
     "The BMI positive control (OR 1.47 per SD) reaffirms adiposity as a "
     "central causal determinant of AF and offers a parsimonious explanation "
     "for the observational literature: habitual SSB intake promotes weight "
     "gain, and the resulting adiposity, rather than the beverage per se, "
     "increases AF risk via atrial remodelling, epicardial fat and "
     "hypertension. Mediation MR quantified this pathway, FTO colocalization "
     "corroborated it at locus level, and the positive genetic correlations "
     "of SSB and ASB intake with AF (rg = 0.24–0.31, q < 0.05) alongside "
     "null MR estimates exemplify shared architecture without a causal "
     "beverage effect. Preventive emphasis therefore shifts towards weight "
     "management and dietary pattern [1]."),
    ("Most fundamentally",
     "Most fundamentally, the component-proxy design estimates the marginal, "
     "lifelong effects of individual ingredients rather than the composite "
     "beverage: a null for sugar, caffeine and tea does not entail a null "
     "for milk tea, which additionally entails possible sugar–caffeine "
     "interaction, non-instrumented constituents (non-dairy creamer; "
     "high-glycaemic-index toppings) and an acute per-serving character "
     "outside the lifelong estimand. The acute window and dose–response "
     "shape are questions for randomized ambulatory-monitoring designs "
     "[30]."),
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
     "control [1]. Prospective studies measuring milk tea intake directly in "
     "East Asian cohorts remain a priority."),
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
     "(conditional F 1.3–7.5; Table S24) and are biased towards the null "
     "under weak identification, mediation MR was a mechanistic probe under "
     "product-method assumptions, and the deferred NHANES triangulation "
     "would have been uninformative by design."),
    ("Genetically proxied consumption of sweetened beverages—including",
     "Genetically proxied consumption of sweetened beverages—including the "
     "sugar component of tea- and coffee-based drinks, the closest available "
     "proxy for milk-tea-type beverages—showed no evidence of a causal "
     "association with atrial fibrillation in European or East Asian "
     "populations: moderate-to-large effects are excluded, but small "
     "effects, and milk-tea exposure itself, remain untested. The modest "
     "observational association is more plausibly explained by residual "
     "confounding, including adiposity, than by a direct causal effect of "
     "beverage sugar. Prevention is better directed at established "
     "cardiometabolic risk factors; direct investigation of milk tea "
     "consumption in prospective East Asian cohorts is needed."),
    # ---------------- declarations ----------------
    ("Acknowledgements: We thank",
     "Acknowledgements: We thank the participants and investigators of UK "
     "Biobank, AFGen, FinnGen, BioBank Japan, GIANT, GSCAN, and the MRC "
     "Integrative Epidemiology Unit and OpenGWAS platform for making summary "
     "statistics publicly available."),
    ("Data availability: All GWAS summary statistics analysed",
     "Data availability: All GWAS summary statistics are publicly available "
     "via OpenGWAS (https://gwas.mrcieu.ac.uk; identifiers in Table 1), the "
     "Neale lab UK Biobank round-2 release "
     "(http://www.nealelab.is/uk-biobank), GWAS Catalog (GCST006414, "
     "GCST010636) and FinnGen (release R13). Analysis code, harmonized "
     "datasets and complete result tables are archived at Zenodo "
     "(https://doi.org/10.5281/zenodo.22099675)."),
]


def main():
    mp = BLD / "build_manuscript_v51.js"
    shutil.copy(mp, str(mp) + ".bak_nmcd2")
    src = mp.read_text(encoding="utf-8")
    for anchor, new in REPL:
        src = sub_literal(src, anchor, new)
    mp.write_text(src, encoding="utf-8")
    print(f"pass-2 applied: {len(REPL)} replacements")


if __name__ == "__main__":
    main()
