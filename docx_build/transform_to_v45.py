# -*- coding: utf-8 -*-
"""
transform_to_v45.py — Convert build_manuscript_v4.js / build_supplement_v4.js /
build_cover_letter.js into v4.5 EJPC-format build scripts.

Every replacement is asserted: if an anchor is not found exactly the expected
number of times the script aborts without writing anything.
"""
import re
import sys
from pathlib import Path

BUILD_DIR = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本")

failures = []


def check(cond, msg):
    if not cond:
        failures.append(msg)
        print("FAIL:", msg)
    return cond


def sub_once(text, old, new, label):
    n = text.count(old)
    if not check(n == 1, f"{label}: anchor found {n} times (expected 1)"):
        return text
    print(f"  ok: {label}")
    return text.replace(old, new, 1)


# =========================================================================
# 1. MANUSCRIPT
# =========================================================================
src = (BUILD_DIR / "build_manuscript_v4.js").read_text(encoding="utf-8")

# ---- 1a. Abstract block -> structured abstract + keywords + lay summary ----
ABSTRACT_NEW = r"""// ---------- Abstract ----------
children.push(
  h1(T`Abstract`),
  mix([
    T`Aim: Milk tea—a composite beverage containing 35–50 g of added sugar and 100–200 mg of caffeine per serving—has never been prospectively studied for atrial fibrillation (AF). We tested whether sweetened-beverage components are causally associated with AF using two-sample Mendelian randomization (MR).`,
  ]),
  mix([
    T`Methods: Seven beverage exposures were instrumented in UK Biobank genome-wide association studies (GWAS; N = 64,949–447,485). AF summary statistics came from Nielsen 2018 (60,620 cases; primary), FinnGen release R13 (67,783 cases), AFGen 2018 and BioBank Japan (East Asian replication). Inverse-variance-weighted estimates were complemented by sensitivity estimators, multivariable MR with body mass index, locus-level colocalization, cross-trait linkage disequilibrium score (LDSC) regression and a positive lifestyle control (alcohol).`,
  ]),
  mix([
    T`Results: No sweetened-beverage exposure was causally associated with AF (European meta-analytic odds ratios 0.82–0.97; all P ≥ 0.06). A nominal coffee association (OR 1.34, 1.11–1.62; P = 0.002) failed all consistency criteria: null weighted-median estimates, source-dependent outlier robustness, attenuation after body-mass-index adjustment (OR 0.82; P = 0.099), and colocalization with AF only at the adiposity locus FTO (PP.H4 ≥ 0.894), not at caffeine-metabolism loci (PP.H4 ≤ 0.008). Sugar-sweetened and artificially sweetened beverage intake showed positive genetic correlations with AF (rg = 0.24–0.31; FDR q < 0.05) despite null causal estimates; LDSC intercepts excluded material sample-overlap bias. The alcohol control behaved as expected (P = 0.035).`,
  ]),
  mix([
    T`Conclusions: Sweetened-beverage intake is not causally associated with AF; the modest observational association likely reflects confounding, including by adiposity. Prevention should target established cardiometabolic risk factors; direct study of milk tea in East Asian cohorts remains needed.`,
  ]),
  mix([
    T`Keywords: Mendelian randomization; atrial fibrillation; sugar-sweetened beverages; coffee; genetic correlation; causal inference`,
  ])
);

// ---------- Lay summary ----------
children.push(
  h1(T`Lay summary`),
  mix([
    T`Genetic evidence does not support a direct causal effect of sweetened beverages—including the sugar added to tea or coffee that best proxies milk tea—on atrial fibrillation (AF).`,
  ]),
  mix([
    T`• Sweetened drinks have been linked to AF in observational studies, but when genetic variants were used as unconfounded proxies for lifelong intake, no sweetened-beverage exposure showed a causal association with AF across four cohorts and two ancestries.`,
  ]),
  mix([
    T`• The modest observational association is best explained by confounding, particularly body weight: the only nominally significant genetic signal (coffee) disappeared after accounting for body mass index and co-localized with AF only at the obesity gene FTO. Prevention is better aimed at established cardiometabolic risk factors; milk tea itself still needs direct study in East Asian cohorts.`,
  ])
);
"""

pat = re.compile(
    r"// ---------- Abstract ----------\nchildren\.push\(\n  h1\(T`Abstract`\),\n[\s\S]*?\n\);\n"
)
m = pat.findall(src)
check(len(m) == 1, f"abstract block matched {len(m)} times (expected 1)")
src = pat.sub(lambda _: ABSTRACT_NEW, src, count=1)
print("  ok: abstract block -> EJPC structured abstract + keywords + lay summary")

# ---- 1b. Full-line paragraph replacements (prefix -> new paragraph text) ----
LINE_REPL = [

("Atrial fibrillation (AF) is the most common",
 "Atrial fibrillation (AF) is the most common sustained cardiac arrhythmia and a major cause of ischaemic stroke, heart failure and premature death worldwide. Its global prevalence is rising with population ageing and the growing burden of metabolic risk factors, making the identification of modifiable lifestyle determinants a public-health priority [6]."),

("Over the past decade, bubble (milk) tea",
 "Over the past decade, bubble (milk) tea has become one of the most widely consumed prepared beverages among young people in East Asia and, increasingly, worldwide. A typical serving contains 35–50 g of added sugar, 100–200 mg of caffeine, and frequently non-dairy creamer or high-fat toppings—a composite exposure poorly captured by conventional food-frequency questionnaires. No prospective cohort has ever measured milk tea consumption directly."),

("The closest available evidence concerns sugar-sweetened",
 "The closest available evidence concerns sugar-sweetened beverages (SSBs). In a prospective analysis of 201,856 UK Biobank participants followed for a median of 9.9 years, consumption of more than 2 L/week of SSBs or artificially sweetened beverages (ASBs) was associated with 10% and 20% higher risks of incident AF, respectively, with the highest risk (HR 3.51) among participants with high genetic susceptibility and high ASB intake [1]. A subsequent UK Biobank analysis in individuals with prediabetes or diabetes confirmed linear positive associations for both [2]. These studies are observational, however; residual confounding and reverse causation cannot be excluded, and the modest effect sizes (HR 1.1–1.2) warrant cautious interpretation."),

("Evidence for caffeine, the second major",
 "Evidence for caffeine, the second major bioactive component of milk tea, points towards the null. Habitual coffee consumption was inversely associated with incident arrhythmias, including AF, in a large healthcare-system cohort [3]; an MR analysis found no causal association between habitual coffee consumption and AF [4]; and the randomized DECAF trial [5] found that daily caffeinated coffee did not increase AF recurrence. Whether the sugar or the caffeine component of composite sweetened beverages drives any true effect on AF therefore remains unresolved."),

("MR uses germline genetic variants",
 "Milk tea itself has never been studied as an exposure, the SSB–AF association lacks causal evidence, virtually all evidence derives from middle-aged European populations, and sugar and caffeine have rarely been evaluated within a single causal framework. MR uses germline genetic variants as instrumental variables for an exposure, thereby minimizing confounding and reverse causation. Leveraging UK Biobank beverage-consumption GWAS [18], the largest available AF GWAS in European and East Asian populations, and open summary-statistics repositories, we conducted an MR study of sweetened beverage consumption and AF with the following aims: (i) to estimate the causal effect of sweetened beverage intake—particularly sugar added to tea or coffee, the closest available genetic proxy for milk-tea-type beverages—on AF; (ii) to disentangle the contributions of sugar-related and caffeine-related behaviours using multivariable MR with body mass index (BMI) as a benchmark confounder; (iii) to test cross-ancestry consistency in an East Asian population; and (iv) to benchmark analytical sensitivity using alcohol consumption, an established modifiable risk factor for AF, as a positive lifestyle control. Mediation MR, Bayesian colocalization and observational triangulation in NHANES were pre-specified as conditional or secondary analyses, to be pursued only where a robust total effect was identified."),

("This study is reported in accordance",
 "This study is reported in accordance with the STROBE-MR checklist [17]. The design rests on the three core MR assumptions: (1) the genetic instruments are robustly associated with the exposure; (2) they share no common cause with the outcome; and (3) they affect the outcome only through the exposure. All analyses use publicly available, de-identified GWAS summary statistics; no individual-level data were accessed. A written analysis plan was finalized before the outcome data were analysed."),

("Exposure data. Instruments for seven",
 "Exposure data. Instruments for seven beverage phenotypes were obtained from the UK Biobank GWAS pipeline of the MRC Integrative Epidemiology Unit (University of Bristol), distributed through OpenGWAS (dataset identifiers in Table 1): intake of sugar added to tea, sugar added to coffee, fizzy drink intake (representing SSB consumption), low-calorie drink intake (representing ASB consumption) and artificial sweetener added to tea (each N = 64,949), coffee intake (N = 428,860) and tea intake (N = 447,485). All participants were of European ancestry. Sugar added to tea or coffee captures sweetening behaviour for tea/coffee-based drinks and is conceptually the closest available proxy for milk-tea-type composite beverages."),

("Outcome data. Primary analyses used",
 "Outcome data. Primary analyses used the largest available European-ancestry AF GWAS, the biobank-driven meta-analysis of Nielsen et al. [7] (60,620 cases and 970,216 controls; ebi-a-GCST006414). Two further European sources were analysed: the AFGen consortium 2018 release (55,114 cases and 482,295 controls; Roselli et al. [8]), which shares participating cohorts with Nielsen 2018 and was therefore treated as a sensitivity source, and FinnGen release R13 [9] (phenotype I9_AF; 67,783 cases and 241,269 controls), which is independent of both. A larger cross-population AF meta-analysis was recently published [13], but its per-variant summary statistics are not publicly available (GWAS Catalog GCST90624413); the sources analysed here therefore represent the largest publicly usable European-ancestry resources. East Asian replication used BioBank Japan statistics (bbj-a-71; 8,180 cases and 28,612 controls; Ishigaki et al. [10])."),

("Covariate and positive-control data.",
 "Covariate and positive-control data. Summary statistics for BMI were obtained from the GIANT consortium (681,275 European-ancestry individuals; ieu-b-40; Yengo et al. [11]) and used in multivariable models, where the well-established BMI→AF effect also served as a positive control. As a positive lifestyle control, alcohol consumption was instrumented using the GSCAN consortium GWAS of alcoholic drinks per week (335,394 European-ancestry participants; ieu-b-73; Liu et al. [12]) and, as an alternative specification, UK Biobank alcohol intake frequency (N = 462,346; ukb-b-5779). Alcohol consumption is an established modifiable risk factor for AF [6]; these analyses verify that the pipeline detects a known lifestyle causal effect."),

("For each exposure, single-nucleotide",
 "For each exposure, single-nucleotide polymorphisms (SNPs) were clumped to independence (r² < 0.001 within 10,000 kb) using ancestry-matched linkage-disequilibrium references. For coffee and tea intake, instruments were selected at genome-wide significance (P < 5 × 10⁻⁸). For the five beverage sub-phenotypes, fewer than three independent variants reached P < 5 × 10⁻⁸; per the pre-specified rule, instruments for these exposures were selected at a relaxed threshold (P < 5 × 10⁻⁶), which is addressed as a limitation. Palindromic variants with intermediate allele frequencies were excluded during harmonization. Instrument strength was assessed with per-variant F statistics, with F > 10 required. Identical instrument lists were used across outcome sources, so estimates differ only in the outcome data queried."),

("Univariable MR. Random-effects",
 "Univariable MR. Random-effects inverse-variance-weighted (IVW) regression was the primary method, complemented by MR-Egger, weighted-median and weighted-mode estimators. Heterogeneity was assessed with Cochran's Q statistic and directional pleiotropy with the MR-Egger intercept. For exposures showing a nominal IVW association (P < 0.05) against the primary outcome, MR-PRESSO was applied to detect horizontal pleiotropy and outlier instruments. European estimates from Nielsen 2018 and FinnGen R13 were combined by fixed-effect meta-analysis, with DerSimonian–Laird random-effects meta-analysis as a sensitivity analysis; AFGen 2018 estimates are reported as sensitivity analyses and were not meta-analysed with Nielsen 2018 because the two GWAS share participating cohorts. BioBank Japan estimates served as cross-ancestry replication. Positive-control analyses applied the identical pipeline to alcohol consumption."),

("Multivariable MR. Coffee intake",
 "Multivariable MR [16]. Coffee intake, sugar added to tea and BMI were entered jointly (MVMR-IVW) to estimate the direct effect of caffeine-related behaviour and of sweetening behaviour conditional on adiposity, with BMI included as a positive control."),

("Multiplicity. The seven European",
 "Multiplicity. The seven European meta-analytic IVW tests were treated as the primary family and controlled by the Benjamini–Hochberg false discovery rate (q = 0.05); all other analyses were considered supportive or exploratory. Analyses used R 4.6.0 with the TwoSampleMR [14], MRPRESSO [15] and coloc packages; dataset identifiers are listed in Table 1 and analysis code is available from the corresponding author on request."),

("Robustness, directionality and power.",
 "Robustness, directionality and power. Causal direction was verified with the Steiger directionality test and per-variant Steiger filtering. For exposures with nominal associations, radial IVW regression (modified second-order weights) served as an additional heterogeneity-robust estimator, and leave-one-out analysis and funnel plots assessed influential instruments and small-study bias. Reverse MR (AF → beverage intake, using 111 independent AF-associated SNPs from the primary outcome GWAS) tested reverse causation. Statistical power was quantified from the realized standard error of each IVW estimate (minimum detectable odds ratio at 80% power, two-sided α = 0.05). Locus-level colocalization. To interrogate the nominal coffee signal, Bayesian colocalization (coloc.abf, default priors) was performed in 500-kb windows centred on the three loci harbouring the strongest coffee instruments—CYP1A1–CYP1A2 (rs2472297) and AHR (rs4410790), which encode the caffeine-metabolism pathway, and FTO (rs1421085), an adiposity locus—with PP.H4 (shared causal variant) > 0.8 considered evidence of colocalization and PP.H1 indicating a coffee-specific signal with no AF counterpart."),

("As a pleiotropy-sensitive complement",
 "As a pleiotropy-sensitive complement to MR and a quantitative diagnostic of sample overlap, cross-trait linkage disequilibrium score (LDSC) regression was implemented following Bulik-Sullivan et al. [19,20], using 1000 Genomes European HapMap 3 LD scores (eur_w_ld_chr; M = 1,290,027 SNPs with MAF > 5%). Full per-variant summary statistics were obtained for coffee intake, tea intake, sugar added to coffee, fizzy drink intake and low-calorie drink intake from the Neale lab UK Biobank round-2 release (UK Biobank fields 1498, 1488, 100370, 100170 and 100160), and for AF from the harmonized Nielsen 2018 statistics (GCST006414) and FinnGen R13; effects were aligned by effect allele and palindromic variants excluded. Single-trait observed-scale SNP heritability and cross-trait genetic correlations (rg) were estimated by two-step weighted least squares, with standard errors by 200-block jackknife; the cross-trait intercept served as a quantitative diagnostic of overlap-driven bias. Implementation accuracy was verified against a same-trait positive control (Nielsen 2018 × FinnGen R13, expected rg ≈ 1) and an overlap positive control (coffee × tea intake, both UK Biobank). Full per-variant summary statistics for sugar added to tea and artificial sweetener added to tea are not publicly distributed, precluding LDSC for these two exposures. Benjamini–Hochberg correction (q = 0.05) was applied across the ten beverage–AF rg tests."),

("Two-step mediation MR through metabolic",
 "Two-step mediation MR through metabolic traits (BMI, type 2 diabetes, blood pressure, obstructive sleep apnoea) and Bayesian colocalization at key loci were pre-specified as conditional analyses, to be performed only where a robust total causal effect was detected. Because no sweetened-beverage exposure showed such an effect, mediation MR was not pursued, and the pre-specified NHANES observational triangulation was deferred to future work. Two deviations are reported transparently: locus-level colocalization was performed at the three loci harbouring the strongest coffee instruments as a mechanistic probe of the sole nominal signal; and during revision the primary outcome was upgraded from AFGen 2018 to the nearly twice-larger Nielsen 2018 GWAS, with every pre-specified analysis repeated and AFGen 2018 results retained as sensitivity analyses."),

("None of the five sweetened-beverage exposures",
 "None of the five sweetened-beverage exposures was causally associated with AF in the primary outcome source or in the European meta-analyses (Table 2; Figure 2). IVW odds ratios (ORs) per unit higher instrumented intake in Nielsen 2018 were 0.91 (95% CI 0.72–1.17) for sugar added to tea, 0.91 (0.67–1.22) for fizzy drink intake (SSBs), 0.99 (0.86–1.13) for low-calorie drink intake (ASBs) and 0.91 (0.72–1.14) for artificial sweetener added to tea (all P ≥ 0.40). AFGen 2018 estimates and fixed-effect European meta-analyses combining Nielsen 2018 and FinnGen R13 were concordantly null (all P ≥ 0.060; Table 2), and weighted-median, MR-Egger and weighted-mode estimates were directionally consistent and non-significant throughout (Table 3; Table S2). Between-source heterogeneity was negligible except for sugar added to tea (I² = 67%; 0–3% for the other six exposures), for which random-effects meta-analysis moved the estimate further from significance (OR 0.77, 0.51–1.15; P = 0.20). The upper confidence bounds of the meta-analyses (1.01–1.17) exclude causal effects of the magnitude suggested by observational cohorts (relative risks 1.1–1.2). One isolated exception emerged: in FinnGen R13, sugar added to tea showed a nominal inverse association (OR 0.60, 0.40–0.90; P = 0.014). This signal was unsupported by the weighted median (P = 0.061), was absent from the other three outcome sources (all P > 0.21), displayed significant heterogeneity (Q P = 8 × 10⁻⁶) with a null MR-Egger intercept (P = 0.68), and was attenuated in the meta-analysis (P = 0.060); we interpret it as a chance finding."),

("Sugar added to coffee showed a nominal",
 "Sugar added to coffee showed a nominal inverse association with AF in AFGen 2018 (IVW OR 0.81, 0.66–0.98; P = 0.030). This signal did not replicate in the nearly twice-larger primary outcome (OR 0.89, 0.70–1.13; P = 0.33) or in FinnGen R13 (OR 0.88, 0.59–1.31; P = 0.53), was null under the weighted median and MR-Egger, and yielded a null European meta-analysis (OR 0.88, 0.72–1.09; P = 0.25); we interpret it as a chance finding attributable to winner's curse."),

("Coffee intake was nominally associated",
 "Coffee intake was nominally associated with higher AF odds in the primary outcome (Nielsen 2018 IVW OR 1.26, 1.02–1.57; P = 0.036), with an almost identical estimate in AFGen 2018 (OR 1.26, 1.02–1.55; P = 0.031), a significant estimate in FinnGen R13 (OR 1.58, 1.09–2.29; P = 0.016), and a European meta-analytic OR of 1.34 (1.11–1.62; P = 0.002) that survived Benjamini–Hochberg correction (threshold P = 0.007). The association nevertheless failed every pre-specified consistency criterion: significant between-instrument heterogeneity in both European sources (Cochran's Q P = 9 × 10⁻⁴ and P = 4 × 10⁻¹⁰); null weighted-median estimates (OR 1.16, P = 0.26 and OR 1.29, P = 0.14) and MR-Egger (OR 1.12; P = 0.60); and MR-PRESSO global heterogeneity in both sources (P = 0.002 and P < 0.001), with outlier correction resolving the estimate to the null in Nielsen 2018 (P = 0.20) but not in FinnGen R13 (β = 0.345; P = 0.007)—robustness to outlier correction is therefore source-dependent. MR-Egger intercepts were null throughout (P ≥ 0.54). Between-source heterogeneity was negligible (I² = 2.7%) and random-effects meta-analysis was essentially unchanged (OR 1.34; P = 0.003). The signal does not satisfy the criteria required for a credible causal interpretation; we nevertheless note that the largest single source retained a nominal association after outlier correction, so a small genuine effect cannot be formally excluded."),

("In MVMR including coffee intake",
 "In MVMR including coffee intake, sugar added to tea and BMI against the primary outcome (Table 4), BMI retained a robust direct effect on AF (OR 1.47 per SD, 1.37–1.57; P = 2.0 × 10⁻²⁷; 467 jointly independent SNPs), serving as a positive control. The nominal coffee–AF association attenuated to the null (OR 0.82, 0.65–1.04; P = 0.099), indicating confounding through adiposity-related pathways rather than a direct effect of coffee. Conditional estimation for sugar added to tea remained uninformative (single joint instrument; OR 0.99; P = 0.96)."),

("In BioBank Japan (8,180 AF cases)",
 "In BioBank Japan (8,180 AF cases), all sweetened-beverage exposures were null with wide confidence intervals (e.g., sugar added to tea OR 0.66, 0.21–2.11; Table 2, Figure 2). Coffee intake was nominally associated with AF (OR 2.34, 1.17–4.68; P = 0.016) but with null weighted-median (P = 0.20) and MR-Egger (P = 0.35) estimates, mirroring the European pattern of a fragile IVW-only signal. Because the instruments derive from European-ancestry GWAS, these estimates are interpreted as supportive context rather than independent evidence."),

("Reverse MR found no evidence",
 "Reverse MR found no evidence that AF liability influences beverage consumption: using 111 independent AF-associated SNPs from the primary outcome GWAS, IVW estimates for all seven beverage outcomes were null (P ≥ 0.054; Table S7). A nominal reverse association with sugar added to tea in an earlier AFGen-based analysis did not replicate with the upgraded instruments (P = 0.17)."),

("Statistical power was limited",
 "Statistical power was limited for small effects (Table S12): minimum detectable odds ratios at 80% power ranged from 1.15 (low-calorie drinks, European meta-analysis) to 1.53 (sugar-sweetened fizzy drinks, primary outcome), and power to detect the observational effect size (OR 1.10) was 9–47%. The null findings therefore exclude moderate-to-large causal effects but cannot exclude effects of the magnitude reported by observational cohorts."),

("As a mechanistic probe of the nominal",
 "As a mechanistic probe of the nominal coffee signal, Bayesian colocalization against the primary outcome was performed around the three loci harbouring the strongest coffee instruments (Table S8). At the caffeine-metabolism loci CYP1A1–CYP1A2 and AHR, the posterior probability overwhelmingly supported an association with coffee intake only (PP.H1 = 0.957 and 0.931), with negligible support for a shared causal variant with AF (PP.H4 = 0.005 and 0.008): coffee-specific genetic variation at these canonical caffeine-handling loci has no AF counterpart. At the FTO locus, the larger outcome GWAS resolved previously split support into strong evidence of a shared causal variant (PP.H4 = 0.894), independently corroborated against FinnGen R13 (PP.H4 = 0.906), directly implicating adiposity-linked pleiotropy as a source of the nominal coffee–AF association—consistent with the attenuation of the coffee estimate after BMI adjustment. A subgroup analysis restricted to the three instruments within the caffeine-metabolism windows was likewise null in both European sources (Nielsen 2018 OR 1.03, 0.76–1.38, P = 0.86; FinnGen R13 OR 1.23, 0.73–2.07, P = 0.44), whereas the remaining 31 instruments carried the entire signal (OR 1.50, 1.12–2.01, P = 0.006 and OR 1.96, 1.18–3.24, P = 0.009): genetic proxies of coffee intake acting through caffeine-handling pathways have no detectable effect on AF."),

("Cross-trait LDSC provided an exposure-wide",
 "Cross-trait LDSC provided an exposure-wide view of shared genetic architecture between beverage intake and AF (Table S10; Table S11). All five beverage traits showed detectable SNP heritability (observed-scale h² = 0.020–0.063; intercepts 0.99–1.01), as did both AF sources (Nielsen 2018 h² = 0.025; FinnGen R13 h² = 0.089). Against FinnGen R13, positive genetic correlations with AF survived false-discovery-rate correction for fizzy drink intake (rg = 0.239, SE 0.089, P = 0.007, q = 0.035) and low-calorie drink intake (rg = 0.313, SE 0.103, P = 0.002, q = 0.025), with directionally concordant but non-significant estimates against Nielsen 2018 (rg = 0.218, P = 0.050 and rg = 0.152, P = 0.088); coffee intake showed a weak trend that did not survive correction (rg ≤ 0.075), and tea intake and sugar added to coffee were null throughout (|rg| ≤ 0.06). Because genetic correlation also captures non-causal pleiotropy, the positive rg values for SSBs and ASBs alongside robustly null MR estimates reinforce the interpretation that shared genetic architecture—for example, adiposity-related biology—rather than a causal effect links sweetened-drink intake to AF. Cross-trait intercepts were indistinguishable from zero for all ten beverage–AF pairs (|intercept| ≤ 0.018), indicating negligible sample-overlap bias; the same diagnostic readily detected the known within-cohort overlap of the coffee and tea intake GWAS (intercept = −0.318, SE 0.011), and the same-trait positive control returned rg = 0.923 (P = 6 × 10⁻²⁰), validating the implementation."),

("To verify that the design is capable",
 "To verify that the design can detect an established lifestyle causal effect, the identical pipeline was applied to alcohol consumption (Table S5). Genetically instrumented alcoholic drinks per week (GSCAN; 35 SNPs) were directionally associated with higher AF odds in all four cohorts (ORs 1.12–2.25), with a nominally significant European meta-analysis (OR 1.19, 1.01–1.40; P = 0.035), consistent with the established causal contribution of alcohol to AF. Alcohol intake frequency per se (UK Biobank; 99 SNPs) was not associated with AF in any cohort (all P > 0.15), in line with evidence that cumulative quantity rather than frequency drives AF risk. The detection of the alcohol-quantity signal argues against general insensitivity as an explanation for the null beverage findings."),

("In this two-sample and multivariable",
 "In this two-sample and multivariable Mendelian randomization study using the largest available European-ancestry AF GWAS, genetically proxied consumption of sweetened beverages was not causally associated with atrial fibrillation. The null was consistent across five conceptually distinct exposures—including sugar added to tea or coffee, the closest available genetic proxy for milk-tea-type composite beverages—across three European outcome sources, and across all complementary estimators. Three nominal IVW signals emerged, but none survived scrutiny: the inverse association for sugar added to coffee failed to replicate in the nearly twice-larger primary outcome; a nominal inverse association for sugar added to tea in FinnGen R13 was absent from the other three sources and attenuated in the meta-analysis; and the positive association for coffee intake, although it survived Benjamini–Hochberg correction (meta-analytic OR 1.34; P = 0.002), exhibited significant heterogeneity with null weighted-median estimates, source-dependent robustness to outlier correction, attenuation after BMI adjustment, and colocalization with AF only at the adiposity locus FTO—not at caffeine-metabolism loci. East Asian replication estimates were imprecise but directionally consistent. The positive lifestyle control (alcoholic drinks per week) was directionally associated with AF in all four cohorts and nominally significant in the European meta-analysis, demonstrating adequate analytical sensitivity."),

("Our findings diverge from the two",
 "Our findings diverge from the two UK Biobank cohort analyses that reported 10–20% higher incident AF risk among high consumers of SSBs or ASBs [1,2]. Three considerations help reconcile this divergence. First, the observational hazard ratios were modest and are compatible with residual confounding: sweetened-beverage consumers differ systematically from non-consumers in adiposity, diet quality and lifestyle, and our multivariable and colocalization results demonstrate directly that adiposity-related pathways account for the only nominally significant genetic signal we observed. Second, MR estimates reflect lifelong average exposure, whereas cohort analyses capture mid-life intake over roughly a decade; if any true effect requires cumulative exposure beyond what instrumented intake proxies, MR would be biased towards the null. Third, our confidence bounds exclude causal effects larger than approximately 9–20% relative increase per unit of instrumented intake for most exposures, so any small true effect lies below the range detectable with current instruments."),

("For coffee, the literature is genuinely",
 "For coffee, the literature is genuinely mixed. A previous MR study reported no causal association between coffee consumption and AF [4], using fewer instruments and earlier outcome data; observational, acute-exposure randomized and recent genetic evidence similarly points to no harm [3,5,21,22]. Our nominal IVW association does not overturn that consensus: although the European meta-analytic association survived false-discovery-rate correction, it was not robust to any sensitivity estimator, displayed substantial heterogeneity whose outlier correction resolved to the null in Nielsen 2018 but not in FinnGen R13, and vanished once BMI was modelled jointly. Colocalization reinforced this reading: the coffee signal had no AF counterpart at the CYP1A1–CYP1A2 and AHR caffeine-metabolism loci (PP.H4 ≤ 0.008) but shared a causal variant with AF at the adiposity locus FTO (PP.H4 = 0.894; replicated at 0.906), and instruments restricted to the caffeine-metabolism loci were null in both European sources while the remaining instruments carried the entire signal—consistent with pleiotropy through adiposity rather than a caffeine-specific mechanism. Genome-wide genetic correlation told a consistent story (coffee–AF rg ≤ 0.075, not surviving correction). The most defensible reading is that habitual coffee intake has no established causal effect on AF in either direction."),

("The positive-control finding for BMI",
 "The positive-control finding for BMI (OR 1.47 per SD) reaffirms adiposity as a central causal determinant of AF and offers a parsimonious explanation for the observational sweetened-beverage literature: habitual SSB intake promotes weight gain, and the resulting adiposity—rather than the beverage per se—increases AF risk through atrial remodelling, epicardial fat, hypertension and obstructive sleep apnoea. The strong colocalization of the coffee signal with AF at FTO and its absence at caffeine-metabolism loci provide locus-level corroboration, and the significant positive genetic correlations of SSB and ASB intake with AF (rg = 0.24–0.31, FDR q < 0.05) alongside robustly null MR estimates exemplify the distinction empirically: sweetened-drink intake shares heritable architecture with AF without a detectable causal effect of the beverages themselves. This distinction matters clinically: it shifts preventive emphasis from beverage-specific restriction towards weight management and overall dietary pattern, in line with guideline recommendations for lifestyle management of AF [6]."),

("Current genetic evidence does not support",
 "Current genetic evidence does not support sweetened beverage intake as a direct causal determinant of AF; within the limits of instruments that proxy sweetening behaviour rather than milk tea itself, it offers no direct evidence implicating milk-tea-type beverages in AF aetiology, but equally cannot exclude effects of the modest magnitude reported by observational cohorts. This conclusion is not a verdict of safety: the instruments proxy intake categories rather than the acute sugar and caffeine bolus characteristic of milk tea, and the cardiometabolic case for limiting added sugar rests on evidence far beyond AF. For young East Asian consumers of milk tea, the relevant AF-prevention message remains the established one: maintain healthy body weight, limit alcohol, and control cardiometabolic risk factors [6]. Prospective studies that measure milk tea consumption directly, particularly in East Asian cohorts, remain a research priority."),

("Strengths include a causal-inference design",
 "Strengths include a causal-inference design with multiple complementary estimators, use of the largest available European-ancestry AF GWAS (over one million participants), prespecified multiplicity control, multivariable modelling and locus-level colocalization, a positive lifestyle control validating analytical sensitivity, and cross-ancestry replication. Several limitations merit emphasis. First, no GWAS measures milk tea itself; our component-proxy strategy assumes that instrumented sweetening behaviour for tea/coffee approximates the exposure of interest and cannot capture the acute sugar–caffeine bolus of a single serving. Second, instruments for the five beverage sub-phenotypes were selected at a relaxed threshold (P < 5 × 10⁻⁶) because few variants reached genome-wide significance; although all per-variant F statistics exceeded 20, this weakens protection against winner's curse, and the exposure GWAS sample sizes limit power to detect small effects (Table S12): our null estimates exclude moderate-to-large causal effects but cannot exclude small ones. Third, the exposure phenotypes are ordinal or single-questionnaire intake measures, so estimates are scaled per instrumented intake category rather than per gram or millilitre. Fourth, the instruments derive from European-ancestry adults, whereas the target consumer population is young and East Asian; the BioBank Japan replication is therefore subject to cross-ancestry linkage-disequilibrium and allele-frequency mismatch, and its wide confidence intervals make it supportive context rather than definitive replication. Fifth, AFGen 2018 shares participating cohorts with Nielsen 2018 and was therefore retained only as a sensitivity source, not meta-analysed with it. Sixth, UK Biobank participants contribute to both the exposure GWAS and the Nielsen 2018 outcome meta-analysis, so sample overlap could in principle bias estimates; with per-variant F statistics of 21–79 this bias is expected to be minimal, the nominal coffee association was at least as strong in the non-overlapping FinnGen R13 (OR 1.58) as in Nielsen 2018 (OR 1.26), and the cross-trait LDSC intercept for coffee × Nielsen 2018 (−0.011, SE 0.008) was indistinguishable from zero, whereas the same diagnostic readily detected the known overlap of the coffee and tea intake GWAS (−0.318, SE 0.011). Seventh, AF ascertainment from diagnostic codes under-detects paroxysmal AF. Eighth, MR estimates lifelong average exposure and cannot model acute triggering. Finally, mediation MR, although pre-specified, was conditional on a robust total effect and was therefore not performed; the NHANES observational triangulation is deferred to future work."),
]

lines = src.split("\n")
used = set()
for prefix, newtext in LINE_REPL:
    hits = [i for i, ln in enumerate(lines)
            if ln.lstrip().startswith("T`") and ln.lstrip()[2:].startswith(prefix)]
    if not check(len(hits) == 1, f"line prefix '{prefix[:40]}...' matched {len(hits)} lines"):
        continue
    i = hits[0]
    check(i not in used, f"line {i} reused")
    used.add(i)
    if not check("`" not in newtext and "${" not in newtext, f"unsafe chars in replacement for '{prefix[:30]}'"):
        continue
    lines[i] = "    T`" + newtext + "`,"
print(f"  ok: {len(used)} paragraph lines replaced")

# ---- 1c. Delete the 'Four gaps follow' mix block ----
hits = [i for i, ln in enumerate(lines) if ln.lstrip().startswith("T`Four gaps follow")]
if check(len(hits) == 1, f"'Four gaps' line matched {len(hits)}"):
    i = hits[0]
    if check(lines[i - 1].strip() == "mix([" and lines[i + 1].strip() == "]),",
             "'Four gaps' wrapper structure"):
        del lines[i - 1:i + 2]
        print("  ok: deleted 'Four gaps follow' intro paragraph (merged into aims)")

# ---- 1d. Delete the Results 'Analyses not performed' subsection ----
src = "\n".join(lines)
OLD_ANP = ("  ]),\n"
           "  h2(T`Analyses not performed`),\n"
           "  mix([\n"
           "    T`Mediation MR, pre-specified as a conditional analysis, was not performed because no sweetened-beverage exposure showed a robust total causal effect on AF; the NHANES observational triangulation was deferred to future work.`,\n"
           "  ])\n"
           ");")
src = sub_once(src, OLD_ANP, "  ])\n);", "delete 'Analyses not performed' subsection")

# ---- 1e. Remove Table 5 block (moved to supplement as S12) ----
OLD_T5 = """  caption(T`Table 5. Statistical power of the Mendelian randomization analyses`),
  makeTable(
    [2500, 1100, 2300, 1900, 2000],
    [T5.header[0], T5.header[1], T5.header[2], T5.header[3], T5.header[4]],
    T5.rows
  ),
  para(run(T`Minimum detectable odds ratios at 80% power (two-sided α = 0.05) were computed from the realized standard error of each IVW estimate as exp[(z₀.₉₇₅ + z₀.₈₀) × SE]; power to detect OR 1.10 (the magnitude reported by observational cohorts) used the same realized precision. SNP counts refer to the primary (Nielsen 2018) analysis.`, { size: 18, color: palette.light }), { spacing: { after: 200 } }),
"""
src = sub_once(src, OLD_T5, "", "remove Table 5 block from manuscript tables")
src = sub_once(src, 'const T5 = readTsv(path.join(TBLDIR, "T5_power.tsv"));\n', "",
               "remove T5 TSV import from manuscript script")

# ---- 1f. References: Vancouver, first-six authors, new numbering ----
REFS_NEW = """    T`1. Sun Y, Yu B, Yu Y, Wang B, Tan X, Lu Y, et al. Sweetened beverages, genetic susceptibility, and incident atrial fibrillation: a prospective cohort study. Circ Arrhythm Electrophysiol. 2024;17(3):e012145.`,
    T`2. Gan X, Ye Z, Zhang Y, He P, Liu M, Zhou C, et al. Sweetened beverages and atrial fibrillation in people with prediabetes or diabetes. Diabetes Obes Metab. 2024;26(11):5147-5156.`,
    T`3. Kim EJ, Hoffmann TJ, Nah G, Vittinghoff E, Delling F, Marcus GM. Coffee consumption and incident tachyarrhythmias: reported behavior, Mendelian randomization, and their interactions. JAMA Intern Med. 2021;181(9):1185-1193.`,
    T`4. Yuan S, Larsson SC. No association between coffee consumption and risk of atrial fibrillation: a Mendelian randomization study. Nutr Metab Cardiovasc Dis. 2019;29(11):1185-1188.`,
    T`5. Wong CX, Cheung CC, Montenegro G, Oo HH, Peña IJ, Tang JJ, et al. Caffeinated coffee consumption or abstinence to reduce atrial fibrillation: the DECAF randomized clinical trial. JAMA. 2026;335(4):317-325.`,
    T`6. Van Gelder IC, Rienstra M, Bunting KV, Casado-Arroyo R, Caso V, Crijns HJGM, et al. 2024 ESC Guidelines for the management of atrial fibrillation developed in collaboration with the European Association for Cardio-Thoracic Surgery (EACTS). Eur Heart J. 2024;45(36):3314-3414.`,
    T`7. Nielsen JB, Thorolfsdottir RB, Fritsche LG, Zhou W, Skov MW, Graham SE, et al. Biobank-driven genomic discovery yields new insight into atrial fibrillation biology. Nat Genet. 2018;50(9):1234-1239.`,
    T`8. Roselli C, Chaffin MD, Weng LC, Aeschbacher S, Ahlberg G, Albert CM, et al. Multi-ethnic genome-wide association study for atrial fibrillation. Nat Genet. 2018;50(9):1225-1233.`,
    T`9. Kurki MI, Karjalainen J, Palta P, Sipilä TP, Kristiansson K, Donner KM, et al. FinnGen provides genetic insights from a well-phenotyped isolated population. Nature. 2023;613(7944):508-518.`,
    T`10. Ishigaki K, Akiyama M, Kanai M, Takahashi A, Kawakami E, Sugishita H, et al. Large-scale genome-wide association study in a Japanese population identifies novel susceptibility loci across different diseases. Nat Genet. 2020;52(7):669-679.`,
    T`11. Yengo L, Sidorenko J, Kemper KE, Zheng Z, Wood AR, Weedon MN, et al. Meta-analysis of genome-wide association studies for height and body mass index in ~700,000 individuals of European ancestry. Hum Mol Genet. 2018;27(20):3641-3649.`,
    T`12. Liu M, Jiang Y, Wedow R, Li Y, Brazel DM, Chen F, et al. Association studies of up to 1.2 million individuals yield new insights into the genetic etiology of tobacco and alcohol use. Nat Genet. 2019;51(2):237-244.`,
    T`13. Yuan S, Chen J, Ruan X, Li Y, Abramowitz SA, Wang L, et al. Cross-population GWAS and proteomics improve risk prediction and reveal mechanisms in atrial fibrillation. Nat Commun. 2025;16(1):6426. (Per-variant summary statistics not publicly available; GWAS Catalog GCST90624413, checked 22 August 2026.)`,
    T`14. Hemani G, Zheng J, Elsworth B, Wade KH, Haberland V, Baird D, et al. The MR-Base platform supports systematic causal inference across the human phenome. eLife. 2018;7:e34408.`,
    T`15. Verbanck M, Chen CY, Neale B, Do R. Detection of widespread horizontal pleiotropy in causal relationships inferred from Mendelian randomization between complex traits and diseases (MR-PRESSO). Nat Genet. 2018;50(5):693-698.`,
    T`16. Burgess S, Thompson SG. Multivariable Mendelian randomization: the use of pleiotropic genetic variants to estimate causal effects. Am J Epidemiol. 2015;181(4):251-260.`,
    T`17. Skrivankova VW, Richmond RC, Woolf BAR, Yarmolinsky J, Davies NM, Swanson SA, et al. Strengthening the reporting of observational studies in epidemiology using Mendelian randomization: the STROBE-MR statement. JAMA. 2021;326(16):1614-1621.`,
    T`18. Zhong VW, Kuang A, Danning RD, Kraft P, van Dam RM, Chasman DI, et al. A genome-wide association study of bitter and sweet beverage consumption. Hum Mol Genet. 2019;28(14):2449-2457.`,
    T`19. Bulik-Sullivan BK, Loh PR, Finucane HK, Ripke S, Yang J, et al. LD Score regression distinguishes confounding from polygenicity in genome-wide association studies. Nat Genet. 2015;47(3):291-295.`,
    T`20. Bulik-Sullivan B, Finucane HK, Anttila V, Gusev A, Day FR, Loh PR, et al. An atlas of genetic correlations across human diseases and traits. Nat Genet. 2015;47(11):1236-1241.`,
    T`21. Marcus GM, Rosenthal DG, Nah G, Vittinghoff E, Fang C, Ogomori K, et al. Acute effects of coffee consumption on health among ambulatory adults (CRAVE trial). N Engl J Med. 2023;388(12):1092-1100.`,
    T`22. Zheng J, Chen H, Yang Q, Zhou Z, Yang C, Huang J, et al. Association of coffee consumption and caffeine metabolism with arrhythmias and cardiac morphology: an observational, genetic, and Mendelian randomization study. Heart Rhythm. 2025;22(9):e618-e630.`,"""

pat_refs = re.compile(r"  \.\.\.\[\n[\s\S]*?\n  \]\.map")
m = pat_refs.findall(src)
check(len(m) == 1, f"references array matched {len(m)} times (expected 1)")
src = pat_refs.sub(lambda _: "  ...[\n" + REFS_NEW + "\n  ].map", src, count=1)
print("  ok: references -> 22 Vancouver entries (first-six authors)")

# ---- 1g. Version note + page header ----
src = sub_once(
    src,
    "Manuscript version: v4 — primary AF outcome upgraded to Nielsen 2018 (N ≈ 1.03 M); alcohol positive lifestyle control added; all robustness analyses repeated against the upgraded outcome (22 August 2026)",
    "Manuscript version: v4.5 — formatted for the European Journal of Preventive Cardiology (structured abstract, numbered references, six display items; Table 5 moved to Table S12); primary AF outcome Nielsen 2018; alcohol positive lifestyle control; cross-trait LDSC (23 August 2026)",
    "title-page version note",
)
src = sub_once(
    src,
    "Sweetened beverages and atrial fibrillation — MR manuscript (v4, Nielsen 2018 primary outcome)",
    "Sweetened beverages and atrial fibrillation — MR manuscript (v4.5, EJPC format)",
    "page header version string",
)

# ---- 1h. Sanity: no author-year citations remain ----
for leftover in ["et al., 20", "et al. (20"]:
    n = src.count(leftover)
    check(n == 0, f"leftover author-year citation pattern '{leftover}' x{n}")
check("(Table 5)" not in src, "leftover '(Table 5)' reference")
check("T`Table 5." not in src, "leftover Table 5 caption")

if failures:
    print("\nMANUSCRIPT TRANSFORM ABORTED:", len(failures), "failure(s)")
    sys.exit(1)

(BUILD_DIR / "build_manuscript_v45.js").write_text(src, encoding="utf-8")
print("written:", BUILD_DIR / "build_manuscript_v45.js")

# =========================================================================
# 2. SUPPLEMENT
# =========================================================================
failures = []
sup = (BUILD_DIR / "build_supplement_v4.js").read_text(encoding="utf-8")

sup = sub_once(
    sup,
    'const S8 = readTsv(path.join(DIR, "S8_coloc.tsv"));\n',
    'const S8 = readTsv(path.join(DIR, "S8_coloc.tsv"));\nconst T5 = readTsv(path.join(DIR, "T5_power.tsv"));\n',
    "supplement: import T5_power.tsv",
)
n = sup.count("(v4.4)")
if check(n == 2, f"supplement '(v4.4)' found {n} times (expected 2)"):
    sup = sup.replace("(v4.4)", "(v4.5)")
    print("  ok: supplement version strings -> v4.5")
sup = sub_once(
    sup,
    "so these two exposures are not covered by LDSC.\"",
    "so these two exposures are not covered by LDSC. v4.5 note (journal-format revision): the statistical-power table was moved from the main text to Table S12 so that the manuscript contains six display items; main-text citations of the power analysis now refer to Table S12.\"",
    "supplement: v4.5 contents note",
)
S12_BLOCK = """children.push(caption("Table S12. Statistical power of the Mendelian randomization analyses (moved from the main text in v4.5)"));
children.push(makeTable([2500, 1100, 2300, 1900, 2000], T5.header, T5.rows, 18));
children.push(note("Minimum detectable odds ratios at 80% power (two-sided α = 0.05) were computed from the realized standard error of each IVW estimate as exp[(z₀.₉₇₅ + z₀.₈₀) × SE]; power to detect OR 1.10 (the magnitude reported by observational cohorts) used the same realized precision. SNP counts refer to the primary (Nielsen 2018) analysis."));

const doc = new Document({"""
sup = sub_once(sup, "const doc = new Document({", S12_BLOCK, "supplement: add Table S12 block")

if failures:
    print("\nSUPPLEMENT TRANSFORM ABORTED:", len(failures), "failure(s)")
    sys.exit(1)
(BUILD_DIR / "build_supplement_v45.js").write_text(sup, encoding="utf-8")
print("written:", BUILD_DIR / "build_supplement_v45.js")

# =========================================================================
# 3. COVER LETTER
# =========================================================================
failures = []
cl = (BUILD_DIR / "build_cover_letter.js").read_text(encoding="utf-8")
cl = sub_once(
    cl,
    "analysis code and complete result files are available on request.\"",
    "analysis code and complete result files are available on request. In accordance with journal policy, we disclose that portions of the analysis workflow and drafting were assisted by an artificial-intelligence tool (Kimi, Moonshot AI); all content was independently verified and approved by the authors, who take full responsibility for the integrity of the work.\"",
    "cover letter: AI-use disclosure",
)
if failures:
    print("\nCOVER LETTER TRANSFORM ABORTED:", len(failures), "failure(s)")
    sys.exit(1)
(BUILD_DIR / "build_cover_letter_v45.js").write_text(cl, encoding="utf-8")
print("written:", BUILD_DIR / "build_cover_letter_v45.js")

print("\nALL TRANSFORMS COMPLETED SUCCESSFULLY")
