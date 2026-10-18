# -*- coding: utf-8 -*-
"""patch_v521_fixes.py — address pre-submission review findings on v5.2 JAHA files:
Finding 1 (disclose Larsson 2023 AF null + delineate biomarker arm),
Finding 2 (minimum detectable ORs + GTF2I-exclusion note),
Finding 3 (cite JAHA 2025 SSB-CVD burden, ref 45),
Reviewer 1-4 (single-measurement steady-state estimand in Limitations),
cover-letter delineation; compensating trims keep body <= 6000."""
import io, sys

M = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本\build_manuscript_v51_JAHA.js"
S = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本\build_supplement_v51_JAHA.js"
C = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本\build_cover_letter_v51_JAHA.js"
V = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\06_升级分析_v4\scripts\verify_jaha.py"

EDITS = [
# --- Finding 1a: disclose [33] includes AF (Discussion coffee paragraph) ---
(M, "plasma-caffeine MR links caffeine itself to lower adiposity [33], reinforcing that the adiposity pathway captured here reflects beverage-drinking patterning, not caffeine pharmacology.",
"plasma-caffeine MR links caffeine itself to lower adiposity and returned null associations with major cardiovascular diseases, AF included [33], reinforcing that the adiposity pathway captured here reflects beverage-drinking patterning, not caffeine pharmacology."),

# --- Finding 1b: delineate biomarker arm vs Larsson 2023 (Discussion biomarker sentence) ---
(M, "and cis estimation at CYP2A6 was null, converging with the absent colocalization at caffeine-metabolism loci [44]. It offers no direct evidence implicating",
"and cis estimation at CYP2A6 was null, converging with the absent colocalization at caffeine-metabolism loci [44]; relative to that two-variant plasma-caffeine analysis [33], this arm adds independent multi-locus instruments, cis estimation at CYP2A6 and extension to paraxanthine and theobromine. It offers no direct evidence implicating"),

# --- Finding 3: East Asian motivation with JAHA GBD citation ---
(M, "For young East Asian consumers, the AF-prevention message remains the established one: healthy weight, limited alcohol, cardiometabolic risk control [1].",
"For young East Asian consumers—where global estimates place a rising SSB-attributable cardiovascular burden [45]—the AF-prevention message remains the established one: healthy weight, limited alcohol, cardiometabolic risk control [1]."),

# --- Finding 2: minimum detectable ORs in biomarker Results ---
(M, "the only genome-wide-significant caffeine-metabolism enzyme locus, was non-significant in both co-primary sources (P ≥ 0.075).",
"the only genome-wide-significant caffeine-metabolism enzyme locus, was non-significant in both co-primary sources (P ≥ 0.075); minimum detectable odds ratios were 1.07–1.25 (Table S25)."),

# --- Reviewer 1-4: steady-state estimand in Limitations Sixth ---
(M, "Sixth, the biomarker arm carried two to seven instruments per analyte, and FinnGen coverage of rare metabolite-associated variants was incomplete (1 of 5 caffeine loci; 2 of 7 paraxanthine loci), so metabolite estimates are supportive rather than definitive.",
"Sixth, the biomarker arm carried two to seven instruments per analyte, captured steady-state plasma levels from single measurements rather than habitual intake, and suffered incomplete FinnGen coverage of rare metabolite-associated variants (1 of 5 caffeine loci; 2 of 7 paraxanthine loci), so metabolite estimates are supportive rather than definitive."),

# --- compensating trims ---
(M, "On balance, the genetic evidence does not establish a causal effect of habitual coffee intake on AF in either direction, although the heterogeneous, partly source-dependent estimates preclude a definitive null.",
"On balance, the genetic evidence does not establish a causal effect of habitual coffee intake on AF in either direction."),
(M, "This reading aligns with the 2026 American Heart Association statement that habitual caffeinated coffee does not increase AF risk and left caffeine-metabolism effect modification unresolved [10];",
"This reading aligns with the 2026 American Heart Association statement [10], which left caffeine-metabolism effect modification unresolved;"),
(M, "For coffee, the literature is mixed. A previous, smaller MR study reported no causal coffee–AF association [8];",
"For coffee, the literature is mixed: a smaller MR study reported no causal coffee–AF association [8];"),
(M, "and the cardiometabolic case for limiting added sugar and sweeteners rests on evidence far beyond AF, including genetic analyses linking artificial sweeteners to cardiometabolic disease [38].",
"and the case for limiting added sugar and sweeteners rests on evidence far beyond AF [38]."),
(M, "We read our estimates as bounds on total beverage-component-pathway effects, not proof of zero effect; a null conclusion carries little risk of clinical misdirection.",
"Our estimates are bounds on total beverage-component-pathway effects, not proof of zero effect."),
(M, "Here it is bounded by concordance across estimators with distinct pleiotropy assumptions, participant-disjoint replication and null metabolite-instrument estimates.",
"Here it is bounded by cross-estimator concordance, participant-disjoint replication and null metabolite-instrument estimates."),
(M, "Metabolite instruments (2–7 locus-lead variants per analyte; per-variant F 30–49; Table S25)",
"Metabolite instruments (2–7 locus-lead variants; per-variant F 30–49; Table S25)"),
(M, "Three deviations are reported transparently: the revision-stage mediation probe; locus-level colocalization at the three loci harbouring the strongest coffee instruments; and during revision the primary outcome was upgraded from AFGen 2018 to the nearly twice-larger Nielsen 2018 GWAS, with all analyses repeated and AFGen 2018 retained as sensitivity.",
"Three deviations are reported transparently: the revision-stage mediation probe; locus-level colocalization at the three strongest coffee-instrument loci; and the revision-stage upgrade of the primary outcome from AFGen 2018 to the nearly twice-larger Nielsen 2018 GWAS, with all analyses repeated and AFGen 2018 retained as sensitivity."),

# --- ref 45 ---
(M, """    T`44. Chen Y, Lu T, Pettersson-Kymmer U, Stewart ID, Butler-Laporte G, Nakanishi T, et al. Genomic atlas of the plasma metabolome prioritizes metabolites implicated in human diseases. Nat Genet. 2023;55(1):44-53.`,""",
"""    T`44. Chen Y, Lu T, Pettersson-Kymmer U, Stewart ID, Butler-Laporte G, Nakanishi T, et al. Genomic atlas of the plasma metabolome prioritizes metabolites implicated in human diseases. Nat Genet. 2023;55(1):44-53.`,
    T`45. Liu X, Bai J, Qi X, Wu Y, Ling J, Liu X, et al. Global burden of cardiovascular disease attributable to sugar-sweetened beverages in middle-aged adults: an age-period-cohort modelling study. J Am Heart Assoc. 2025;14(9):e035978.`,"""),

# --- Finding 2 supplement: GTF2I-exclusion + MDO + Larsson delineation in S25 note ---
(S, "cis estimation used rs56113850 (CYP2A6), the only caffeine-metabolism enzyme locus reaching genome-wide significance in these metabolite GWAS.",
"cis estimation used rs56113850 (CYP2A6), the only caffeine-metabolism enzyme locus reaching genome-wide significance in these metabolite GWAS; excluding the GTF2I instrument therefore leaves these single-SNP CYP2A6 estimates, which are likewise non-significant. Minimum detectable odds ratios (80% power, alpha = 0.05) for the European meta-analyses were 1.11 (caffeine), 1.07 (paraxanthine) and 1.25 (theobromine): the caffeine and paraxanthine nulls exclude effects of the magnitude reported observationally, whereas the two-instrument theobromine estimate is uninformative beyond small effects. Larsson et al. (manuscript ref 33) reported null associations between plasma caffeine and major cardiovascular diseases, atrial fibrillation included, using a two-variant (CYP1A2/AHR) instrument set; the present arm extends that analysis with independent multi-locus instruments from an independent metabolome GWAS."),

# --- Finding 4: cover-letter delineation ---
(C, "Biomarker-level MR of plasma caffeine, paraxanthine and theobromine—whose instruments are anchored in caffeine-metabolism biology rather than self-reported behaviour—likewise returned null estimates.",
"Biomarker-level MR of plasma caffeine, paraxanthine and theobromine—whose instruments are anchored in caffeine-metabolism biology rather than self-reported behaviour—likewise returned null estimates; this arm extends the two-variant plasma-caffeine analysis of Larsson et al. (BMJ Med 2023), which reported null cardiovascular associations including atrial fibrillation, with independent multi-locus instruments and adds the first MR tests of paraxanthine and theobromine."),

# --- verify updates ---
(V, 'check(cites == list(range(1, 45)), f"numbered citations cover 1..44 (got {cites})")',
 'check(cites == list(range(1, 46)), f"numbered citations cover 1..45 (got {cites})")'),
(V, 'check(len(refs) == 44, f"references: {len(refs)} numbered entries")',
 'check(len(refs) == 45, f"references: {len(refs)} numbered entries")'),
(V, '"0.84, 0.72–0.98; P = 0.029", "Wald-ratio estimation", "P ≥ 0.31"]',
 '"0.84, 0.72–0.98; P = 0.029", "Wald-ratio estimation", "P ≥ 0.31",\n       "minimum detectable odds ratios were 1.07–1.25",\n       "SSB-attributable cardiovascular burden", "independent multi-locus instruments",\n       "AF included [33]", "e035978"]'),
]

for path, old, new in EDITS:
    with io.open(path, encoding="utf-8") as f:
        t = f.read()
    n = t.count(old)
    if n != 1:
        print(f"FAIL ({n}x): {path.split(chr(92))[-1]} :: {old[:70]}...")
        sys.exit(1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(t.replace(old, new))
    print(f"OK  {path.split(chr(92))[-1]} :: {old[:55]}...")
print("ALL v5.2.1 PATCHES APPLIED")
