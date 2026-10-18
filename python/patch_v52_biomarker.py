# -*- coding: utf-8 -*-
"""patch_v52_biomarker.py — v5.2: add biomarker-MR arm (Chen 2023 plasma caffeine metabolites)
to JAHA manuscript/supplement/cover-letter builders + verify_jaha.py; with compensating trims
to keep body <= 6000 words. Every replacement asserts exactly one occurrence."""
import io, sys

M = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本\build_manuscript_v51_JAHA.js"
S = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本\build_supplement_v51_JAHA.js"
C = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本\build_cover_letter_v51_JAHA.js"
V = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\06_升级分析_v4\scripts\verify_jaha.py"

EDITS = [
# ---------- manuscript ----------
(M, "these analyses verify that the pipeline detects a known causal effect.`,\n  ]),\n  h2(T`Instrument selection`)",
"""these analyses verify that the pipeline detects a known causal effect.`,
  ]),
  mix([
    T`Biomarker exposure data. Plasma caffeine, paraxanthine and theobromine levels were instrumented from the genomic atlas of the plasma metabolome (Chen et al. [44]; N = 8,005, 7,840 and 8,137 European-ancestry participants; GCST90200436, GCST90199654, GCST90199644), anchoring caffeine biology in variants of unambiguous biological specificity. Per-locus lead variants (P < 5 × 10⁻⁸; 10-Mb windows) recoverable in each outcome source served as instruments, analysed with the identical pipeline (Wald ratio for single-instrument tests).`,
  ]),
  h2(T`Instrument selection`)"""),

(M, """  ]),
  h2(T`Genetic correlation with AF`),""",
"""  ]),
  h2(T`Biomarker MR of plasma caffeine metabolites`),
  mix([
    T`Metabolite instruments (2–7 locus-lead variants per analyte; per-variant F 30–49; Table S25) gave no evidence that caffeine biology contributes to AF: European meta-analytic ORs per genetically higher SD were 0.99 (0.92–1.07; P = 0.85) for plasma caffeine and 0.98 (0.93–1.02; P = 0.31) for paraxanthine, with no significant heterogeneity (all Cochran's Q P > 0.05) and null MR-Egger intercepts. A nominal inverse association for theobromine (OR 0.84, 0.72–0.98; P = 0.029) did not survive Bonferroni correction across the three metabolites and rested on two instruments, one at the taste-behaviour locus GTF2I; it is not interpreted as protective. Wald-ratio estimation at CYP2A6 (rs56113850), the only caffeine-metabolism enzyme locus reaching genome-wide significance in the metabolite GWAS, was non-significant in both co-primary sources (P ≥ 0.075).`,
  ]),
  h2(T`Genetic correlation with AF`),"""),

(M, "as a direct causal determinant of AF; it offers no direct evidence implicating",
"as a direct causal determinant of AF. Plasma metabolite instruments extended this inference from behaviour to biology: genetically higher caffeine and paraxanthine levels were unassociated with AF, and cis estimation at CYP2A6 was null, converging with the absent colocalization at caffeine-metabolism loci [44]. It offers no direct evidence implicating"),

(M, " Finally, multivariable estimates rest on conditionally modest instruments",
" Sixth, the biomarker arm carried two to seven instruments per analyte, and FinnGen coverage of rare metabolite-associated variants was incomplete (1 of 5 caffeine loci; 2 of 7 paraxanthine loci), so metabolite estimates are supportive rather than definitive. Finally, multivariable estimates rest on conditionally modest instruments"),

(M, """T`A more fundamental concern applies to behavioural-exposure instruments generally, ours included: variants associated with beverage preferences may influence AF through correlated behavioural, socioeconomic or metabolic pathways rather than through the beverages themselves, and no sensitivity analysis can establish the biological specificity of such instruments. This limitation is not unique to the present study—it applies equally to published alcohol, coffee and smoking MR analyses, our positive control included—and its weight remains a matter of active methodological debate rather than settled consensus [43]. Three features nonetheless bound the plausible bias here: estimates were concordant across estimators built on mutually distinct pleiotropy assumptions; participant-disjoint replication in FinnGen reproduced the nulls; and mechanistic probes located the residual coffee signal at an adiposity locus (FTO) rather than at caffeine-metabolism loci, with null LDSC intercepts. We therefore interpret our estimates as bounds on the total effect of beverage-component pathways, not as proof of zero effect—and note that a null conclusion carries little risk of clinical misdirection.`,""",
"""T`A concern common to all behavioural-exposure instruments—including published alcohol, coffee and smoking MR analyses and our positive control—is that preference-associated variants may act through correlated behavioural, socioeconomic or metabolic pathways, and no sensitivity analysis can establish biological specificity; the weight assigned to this limitation remains an unsettled methodological debate [43]. Here it is bounded by concordance across estimators with distinct pleiotropy assumptions, participant-disjoint replication and null metabolite-instrument estimates. We read our estimates as bounds on total beverage-component-pathway effects, not proof of zero effect; a null conclusion carries little risk of clinical misdirection.`,"""),

(M, """T`As a pleiotropy-sensitive complement to MR and a quantitative diagnostic of sample overlap, cross-trait linkage disequilibrium score (LDSC) regression was implemented following Bulik-Sullivan et al. [27,28], using 1000 Genomes European HapMap 3 LD scores (eur_w_ld_chr; M = 1,290,027 SNPs with MAF > 5%). Full summary statistics were obtained for five beverage traits from the Neale lab UK Biobank round-2 release (fields 1498, 1488, 100370, 100170, 100160) and for AF from the harmonized Nielsen 2018 statistics (GCST006414) and FinnGen R13; effects were aligned by effect allele and palindromic variants excluded. Single-trait observed-scale SNP heritability and cross-trait genetic correlations (rg) were estimated by two-step weighted least squares, with standard errors by 200-block jackknife; the cross-trait intercept diagnosed overlap-driven bias. Implementation accuracy was verified against same-trait and overlap positive controls. Full summary statistics for sugar and artificial sweetener added to tea are not public, precluding their LDSC. Benjamini–Hochberg correction (q = 0.05) was applied across the ten beverage–AF rg tests.`,""",
"""T`As a pleiotropy-sensitive complement to MR and a diagnostic of sample overlap, cross-trait LD score regression [27,28] used 1000 Genomes European HapMap 3 LD scores (eur_w_ld_chr; M = 1,290,027 SNPs with MAF > 5%). Full statistics came from the Neale lab UK Biobank round-2 release (fields 1498, 1488, 100370, 100170, 100160) and from harmonized Nielsen 2018 (GCST006414) and FinnGen R13; palindromic variants were excluded. Heritability and genetic correlations (rg) were estimated by two-step weighted least squares (200-block jackknife SEs), the cross-trait intercept diagnosing overlap bias; implementation was verified against same-trait and overlap positive controls. Sugar- and sweetener-added-to-tea statistics are not public, precluding their LDSC. Benjamini–Hochberg correction (q = 0.05) covered the ten beverage–AF rg tests.`,"""),

(M, "reached the same conclusion for habitual coffee, cautioning against high-dose caffeinated products and sugar-sweetened coffee drinks, and prioritized disentangling",
"reached the same conclusion for habitual coffee and prioritized disentangling"),

(M, "rather than a beverage-specific effect; the corresponding AF nulls are therefore evidence against a beverage-specific effect, though adiposity-pleiotropic contributions cannot be excluded (Limitations).",
"rather than a beverage-specific effect, though adiposity-pleiotropic contributions cannot be excluded (Limitations)."),

(M, "Between 8 and 34 independent SNPs per exposure were available for analysis against the primary outcome (median 17; Table 2); identical instrument lists were carried into all outcome sources.",
"Between 8 and 34 independent SNPs per exposure were analysed against the primary outcome (median 17; Table 2), with identical instrument lists across outcome sources."),

(M, "(rg = 0.24–0.31; FDR q < 0.05).`",
"(rg = 0.24–0.31; FDR q < 0.05). Plasma caffeine and paraxanthine instruments were likewise unassociated with AF (P ≥ 0.31).`"),

(M, """      [T`Exposure: tea intake`, T`UK Biobank, MRC IEU pipeline (ukb-b-6066)`, T`447,485`, T`European`, T`OpenGWAS`],""",
"""      [T`Exposure: tea intake`, T`UK Biobank, MRC IEU pipeline (ukb-b-6066)`, T`447,485`, T`European`, T`OpenGWAS`],
      [T`Exposure: plasma caffeine metabolites`, T`Chen et al. 2023 metabolome atlas (GCST90200436, GCST90199654, GCST90199644)`, T`7,840–8,137`, T`European`, T`GWAS Catalog`],"""),

(M, """    T`43. Hemani G, Bowden J, Davey Smith G. Evaluating the potential role of pleiotropy in Mendelian randomization studies. Hum Mol Genet. 2018;27(R2):R195-R208.`,""",
"""    T`43. Hemani G, Bowden J, Davey Smith G. Evaluating the potential role of pleiotropy in Mendelian randomization studies. Hum Mol Genet. 2018;27(R2):R195-R208.`,
    T`44. Chen Y, Lu T, Pettersson-Kymmer U, Stewart ID, Butler-Laporte G, Nakanishi T, et al. Genomic atlas of the plasma metabolome prioritizes metabolites implicated in human diseases. Nat Genet. 2023;55(1):44-53.`,"""),

# ---------- supplement ----------
(S, "const doc = new Document({",
"""children.push(caption("Table S25. Biomarker Mendelian randomization: plasma caffeine metabolites (Chen et al. 2023) and atrial fibrillation"));
children.push(makeTable(
  [2500, 1800, 1600, 2100, 900],
  ["Exposure", "Outcome source", "Instruments (n)", "OR (95% CI)", "P"],
  [
    ["Plasma caffeine", "Nielsen 2018", "5", "0.99 (0.91-1.06)", "0.72"],
    ["Plasma caffeine", "FinnGen R13", "1 (Wald ratio)", "1.10 (0.82-1.48)", "0.53"],
    ["Plasma caffeine", "European meta-analysis", "-", "0.99 (0.92-1.07)", "0.85"],
    ["Plasma paraxanthine", "Nielsen 2018", "7", "0.98 (0.93-1.03)", "0.45"],
    ["Plasma paraxanthine", "FinnGen R13", "2", "0.90 (0.75-1.08)", "0.26"],
    ["Plasma paraxanthine", "European meta-analysis", "-", "0.98 (0.93-1.02)", "0.31"],
    ["Plasma theobromine", "Nielsen 2018", "2", "0.85 (0.69-1.04)", "0.11"],
    ["Plasma theobromine", "FinnGen R13", "2", "0.84 (0.67-1.06)", "0.14"],
    ["Plasma theobromine", "European meta-analysis", "-", "0.84 (0.72-0.98)", "0.029"],
    ["cis CYP2A6 (rs56113850), paraxanthine", "Nielsen 2018", "1 (Wald ratio)", "0.89 (0.79-1.01)", "0.075"],
    ["cis CYP2A6 (rs56113850), paraxanthine", "FinnGen R13", "1 (Wald ratio)", "0.93 (0.79-1.08)", "0.33"],
    ["cis CYP2A6 (rs56113850), theobromine", "Nielsen 2018", "1 (Wald ratio)", "0.89 (0.78-1.01)", "0.075"],
    ["cis CYP2A6 (rs56113850), theobromine", "FinnGen R13", "1 (Wald ratio)", "0.92 (0.78-1.09)", "0.33"],
  ], 18));
children.push(note("Exposures were plasma caffeine, paraxanthine and theobromine levels from the genomic atlas of the plasma metabolome (Chen et al., 2023; manuscript ref 44; GCST90200436, GCST90199654, GCST90199644; N = 8,005, 7,840 and 8,137 European-ancestry participants; genome build GRCh38). Instruments were per-locus lead variants (P < 5 x 10-8; 10-Mb windows) recoverable in each outcome source (per-variant F 30-49); FinnGen R13 lacked many rare metabolite-associated variants (1 of 5 caffeine loci and 2 of 7 paraxanthine loci covered), so metabolite estimates are supportive rather than definitive. ORs are per genetically higher SD of metabolite level. No significant heterogeneity was detected (all Cochran's Q P > 0.05); MR-Egger intercepts were null where computable (caffeine P = 0.40; paraxanthine P = 0.26). The nominal inverse theobromine association did not survive Bonferroni correction across the three metabolites (threshold P = 0.017) and rested on two instruments, one at the taste-behaviour locus GTF2I (a recurrent beverage-preference GWAS locus); it is not interpreted as protective. cis estimation used rs56113850 (CYP2A6), the only caffeine-metabolism enzyme locus reaching genome-wide significance in these metabolite GWAS."));

const doc = new Document({"""),

# ---------- cover letter ----------
(C, "and was compatible with correlated pleiotropy in genome-wide CAUSE analysis. Cross-trait LD score regression",
"and was compatible with correlated pleiotropy in genome-wide CAUSE analysis. Biomarker-level MR of plasma caffeine, paraxanthine and theobromine—whose instruments are anchored in caffeine-metabolism biology rather than self-reported behaviour—likewise returned null estimates. Cross-trait LD score regression"),

(C, "adds multivariable modelling of adiposity, locus-level colocalization, robust profile-score (MR-RAPS) and weak-instrument (conditional F) diagnostics",
"adds multivariable modelling of adiposity, locus-level colocalization, biomarker-level MR of plasma caffeine metabolites, robust profile-score (MR-RAPS) and weak-instrument (conditional F) diagnostics"),

# ---------- verify ----------
(V, 'check(cites == list(range(1, 44)), f"numbered citations cover 1..43 (got {cites})")',
 'check(cites == list(range(1, 45)), f"numbered citations cover 1..44 (got {cites})")'),
(V, 'check(len(refs) == 43, f"references: {len(refs)} numbered entries")',
 'check(len(refs) == 44, f"references: {len(refs)} numbered entries")'),
(V, '"moderate-to-large effects are excluded, but small effects"]',
 '"moderate-to-large effects are excluded, but small effects",\n       "Table S25", "GTF2I", "CYP2A6", "rs56113850", "GCST90200436",\n       "0.99 (0.92–1.07; P = 0.85)", "0.98 (0.93–1.02; P = 0.31)",\n       "0.84, 0.72–0.98; P = 0.029", "Wald-ratio estimation", "P ≥ 0.31"]'),
(V, 'BASE + r"\\manuscript_v51_JAHA.docx"', 'BASE + r"\\manuscript_v52_JAHA.docx"'),
(V, 'BASE + r"\\supplement_v51_JAHA.docx"', 'BASE + r"\\supplement_v52_JAHA.docx"'),
(V, 'check("Table S24" in sfull and "Table S23. MR-RAPS" in sfull and "Table S22. Instrument-strength" in sfull,\n      "supplement contains S22/S23/S24")',
 'check("Table S24" in sfull and "Table S23. MR-RAPS" in sfull and "Table S22. Instrument-strength" in sfull and "Table S25" in sfull,\n      "supplement contains S22/S23/S24/S25")'),
]

for path, old, new in EDITS:
    with io.open(path, encoding="utf-8") as f:
        t = f.read()
    n = t.count(old)
    if n != 1:
        print(f"FAIL ({n}x): {path} :: {old[:70]}...")
        sys.exit(1)
    with io.open(path, "w", encoding="utf-8") as f:
        f.write(t.replace(old, new))
    print(f"OK  {path.split(chr(92))[-1]} :: {old[:60]}...")
print("ALL PATCHES APPLIED")
