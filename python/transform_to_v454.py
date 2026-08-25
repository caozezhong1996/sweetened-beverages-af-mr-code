# -*- coding: utf-8 -*-
"""transform_to_v454.py — upgrade manuscript/supplement build scripts to v4.5.4.

v4.5.4 additions:
  A. Independent coffee-exposure GWAS replication (Neale lab UKB field 1498;
     24 instruments) + cross-GWAS fixed-effect meta-analysis  -> new Table S19
  B. Full-coverage BMI mediation sensitivity (Neale lab field 21001, raw kg/m2;
     33/34 instruments recovered)                             -> Table S16 rows
Body-word budget: additions offset by surgical trims (EJPC <= 5,100 words).
"""
import io, os, sys

ROOT = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822"
MS = os.path.join(ROOT, "04_docx构建脚本", "build_manuscript_v45.js")
SUP = os.path.join(ROOT, "04_docx构建脚本", "build_supplement_v45.js")
TABDIR = os.path.join(ROOT, "06_升级分析_v4", "supplement_tables")


def sub_once(text, old, new, tag):
    n = text.count(old)
    if n != 1:
        print(f"FAIL  anchor not unique ({n}x): {tag}")
        sys.exit(1)
    print(f"  ok  {tag}")
    return text.replace(old, new, 1)


# ---------------- manuscript ----------------
ms = io.open(MS, encoding="utf-8").read()

ms = sub_once(ms,
    "Manuscript version: v4.5.3 — EJPC format plus reviewer-driven additions: ",
    "Manuscript version: v4.5.4 — EJPC format plus reviewer-driven additions: ",
    "version string v4.5.4")
ms = sub_once(ms,
    "and an atrioventricular-block negative outcome control (Table S18) (25 August 2026)",
    "and an atrioventricular-block negative outcome control (Table S18); "
    "independent coffee-exposure GWAS replication with cross-GWAS meta-analysis (Table S19) "
    "and a full-coverage BMI mediation sensitivity (25 August 2026)",
    "version string additions")

# --- Results: replication + mediation sensitivity (after MRlap sentence; also trims it)
ms = sub_once(ms,
    "The MRlap overlap-corrected estimate did not differ significantly from the observed estimate "
    "(difference P = 0.07; Table S17), excluding material sample-overlap bias.`",
    "The MRlap overlap-corrected estimate did not differ from the observed estimate "
    "(difference P = 0.07; Table S17), excluding material overlap bias. An independent coffee GWAS "
    "(Neale lab field 1498; 24 instruments) gave a concordant, non-significant estimate (OR 1.18, "
    "0.93–1.50; P = 0.166); cross-GWAS fixed-effect meta-analysis gave OR 1.23 (1.04–1.44; "
    "P = 0.013; Table S19). BMI re-instrumented in the full-coverage Neale GWAS (33 of 34 "
    "instruments) reproduced the mediation (β = 0.75 SD; 109%, −9% to 227%; Table S16).`",
    "results: replication + mediation sensitivity")

# --- Methods: robustness clause
ms = sub_once(ms,
    "(product method; Table S16).`",
    "(product method; Table S16); robustness used the full-coverage Neale BMI GWAS (field 21001) "
    "and an independent coffee GWAS (field 1498).`",
    "methods: robustness data sources")

# --- Trims (word budget) ---
trims = [
    (", with a concordant estimate in AFGen 2018 (OR 1.26; P = 0.031), a significant estimate in FinnGen R13",
     ", concordant in AFGen 2018 (OR 1.26; P = 0.031), significant in FinnGen R13"),
    ("but not in FinnGen R13 (β = 0.345; P = 0.007)—robustness to outlier correction is therefore source-dependent.",
     "but not FinnGen R13 (β = 0.345; P = 0.007)—robustness to outlier correction is thus source-dependent."),
    ("The signal does not satisfy the criteria required for a credible causal interpretation; we nevertheless note that the largest single source retained",
     "The signal does not satisfy the criteria for a credible causal interpretation; we note, however, that the largest source retained"),
    ("so a small genuine effect cannot be formally excluded. The contamination-mixture",
     "so a small genuine effect cannot be excluded. The contamination-mixture"),
    ("(P = 0.53 for the causal-model improvement)", "(P = 0.53 for causal-model improvement)"),
    ("accounted for the entire total association", "accounted for the full total association"),
    ("to estimate the direct effect of caffeine-related behaviour and of sweetening behaviour conditional on adiposity, with BMI included as a positive control",
     "to estimate direct effects of caffeine-related and sweetening behaviour conditional on adiposity, with BMI as a positive control"),
    ("Full per-variant summary statistics for sugar added to tea and artificial sweetener added to tea are not publicly distributed, precluding LDSC for these two exposures.",
     "Full summary statistics for sugar and artificial sweetener added to tea are not public, precluding their LDSC."),
    ("with standard errors by 200-block jackknife; the cross-trait intercept served as a quantitative diagnostic of overlap-driven bias",
     "with standard errors by 200-block jackknife; the cross-trait intercept diagnosed overlap-driven bias"),
    ("Full per-variant summary statistics were obtained for five beverage traits",
     "Full summary statistics were obtained for five beverage traits"),
    ("increases AF risk through atrial remodelling, epicardial fat, hypertension and obstructive sleep apnoea",
     "increases AF risk via atrial remodelling, epicardial fat, hypertension and sleep apnoea"),
    ("with AF without a detectable causal effect of the beverages themselves",
     "with AF without a detectable causal beverage effect"),
    ("and the exposure GWAS sample sizes limit power to detect small effects (Table S12): our null estimates exclude moderate-to-large causal effects but cannot exclude small ones",
     "and the exposure GWAS sample sizes limit power (Table S12): the null estimates exclude moderate-to-large but not small effects"),
    ("and cannot capture the acute sugar–caffeine bolus of a single serving",
     "and misses the acute sugar–caffeine bolus of one serving"),
    ("to be performed only where a robust total causal effect was detected",
     "to be performed only where a robust total effect was detected"),
    ("the pre-specified NHANES observational triangulation was deferred to future work",
     "the pre-specified NHANES triangulation was deferred"),
    ("The strong colocalization of the coffee signal with AF at FTO and its absence at caffeine-metabolism loci provide locus-level corroboration",
     "Strong colocalization of the coffee signal with AF at FTO, and its absence at caffeine-metabolism loci, provides locus-level corroboration"),
    ("Fifth, AFGen 2018 shares participating cohorts with Nielsen 2018 and was therefore retained only as a sensitivity source, not meta-analysed with it.",
     "Fifth, AFGen 2018 shares cohorts with Nielsen 2018 and was retained as a sensitivity source, not meta-analysed with it."),
    ("so sample overlap could in principle bias estimates; with per-variant F statistics of 21–79 this bias is expected to be minimal, the coffee association was at least as strong in the non-overlapping FinnGen R13",
     "so sample overlap could bias estimates; with per-variant F statistics of 21–79 this bias should be minimal, the coffee association was at least as strong in non-overlapping FinnGen R13"),
    ("whereas the same diagnostic readily detected the known overlap of the coffee and tea intake GWAS (−0.318, SE 0.011)",
     "whereas the same diagnostic readily detected the known coffee–tea GWAS overlap (−0.318, SE 0.011)"),
    ("was performed during revision as a mechanistic probe of the sole nominal signal and carries the usual product-method assumptions",
     "was performed during revision as a mechanistic probe and carries the usual product-method assumptions"),
    ("the NHANES observational triangulation is deferred to future work",
     "the NHANES triangulation is deferred"),
]
for old, new in trims:
    ms = sub_once(ms, old, new, "trim: " + old[:48] + "...")

io.open(MS, "w", encoding="utf-8", newline="").write(ms)
print("manuscript build script updated")

# ---------------- supplement ----------------
sup = io.open(SUP, encoding="utf-8").read()

sup = sub_once(sup,
    "Mendelian Randomization Study With Cross-Ancestry Replication (v4.5.3)",
    "Mendelian Randomization Study With Cross-Ancestry Replication (v4.5.4)",
    "supplement title v4.5.4")
sup = sub_once(sup,
    "Sweetened beverages and atrial fibrillation — Supplementary Materials (v4.5.3)",
    "Sweetened beverages and atrial fibrillation — Supplementary Materials (v4.5.4)",
    "supplement header v4.5.4")
sup = sub_once(sup,
    'const T18 = readTsv(path.join(DIR, "S18_avblock.tsv"));',
    'const T18 = readTsv(path.join(DIR, "S18_avblock.tsv"));\n'
    'const T19 = readTsv(path.join(DIR, "S19_neale1498_replication.tsv"));',
    "read T19")
sup = sub_once(sup,
    "and the atrioventricular-block negative outcome control (Table S18).\",",
    "and the atrioventricular-block negative outcome control (Table S18). v4.5.4 note: Table S19 reports an independent coffee-exposure GWAS replication (Neale lab UK Biobank field 1498) with cross-GWAS fixed-effect meta-analysis, and Table S16 adds a full-coverage BMI mediation sensitivity (Neale lab field 21001, 33 of 34 instruments).\",",
    "contents v4.5.4 note")
sup = sub_once(sup,
    "indicates that the nominal total association is statistically explained by the adiposity pathway.\"",
    "indicates that the nominal total association is statistically explained by the adiposity pathway. Revision sensitivity (v4.5.4): step 1 was repeated against the full-coverage Neale lab UK Biobank BMI GWAS (field 21001; raw kg/m2 units; n = 359,983), recovering 33 of 34 coffee instruments (only rs117810762 unmatched); beta_XM = 3.587 kg/m2 (0.747 SD at 4.8 kg/m2 per SD) and the mediated proportion was 109% (95% CI -9% to 227%), concordant with the primary Yengo estimate; 21001 units were verified at the FTO locus anchor (beta = 0.359 kg/m2).\"",
    "S16 note: Neale 21001 sensitivity")

s19_block = '''
children.push(caption("Table S19. Independent coffee-exposure GWAS replication (Neale lab UK Biobank field 1498) and cross-GWAS fixed-effect meta-analysis (Nielsen 2018 outcome)"));
children.push(makeTable(
  [3000, 1900, 1050, 950, 950, 1650, 900],
  T19.header, T19.rows, 18));
children.push(note("Replication instruments came from the Neale lab UK Biobank round-2 GWAS of coffee intake (field 1498; n = 334,659; effects per ALT allele, validated by 9/9 sign concordance with the primary instruments at shared loci): 3,147 variants at P < 5 x 10-8 after excluding low-confidence calls, pruned to 27 independent loci by 1-Mb window pruning (lowest P retained); 24 were recoverable in the harmonized Nielsen 2018 statistics by chromosome:position with exact ref/alt allele matching (three palindromic SNPs retained on exact plus-strand match; excluding them gave IVW OR 1.22, 0.95-1.56; P = 0.117). Per-variant F statistics: minimum 29.7, median 45.2. 19 of 24 replication instruments lay within 1 Mb of a primary-analysis locus. MR-Egger intercept 0.002 (P = 0.757); Cochran's Q P = 0.002. The replication point estimate is directionally concordant but the smaller instrument set limits power; the fixed-effect cross-GWAS meta-analysis (OR 1.23, 1.04-1.44; P = 0.013) is more precise than either source alone."));

const doc = new Document({'''
sup = sub_once(sup, "const doc = new Document({", s19_block, "S19 block")

io.open(SUP, "w", encoding="utf-8", newline="").write(sup)
print("supplement build script updated")

# ---------------- staged TSVs ----------------
s16 = io.open(os.path.join(TABDIR, "S16_mediation.tsv"), encoding="utf-8").read().rstrip("\n")
s16 += (
    "\nStep 1 sensitivity (X->M)\tCoffee intake -> BMI (Neale UKB 21001, kg/m2)\tIVW\t33\t3.5873\t0.9522\t1.6e-04"
    "\nStep 1 sensitivity (X->M, SD)\tCoffee intake -> BMI (Neale 21001, per 4.8 kg/m2 SD)\tIVW\t33\t0.7473\t0.1984\t1.6e-04"
    "\nIndirect effect sensitivity\tproduct beta_XM x beta_MY (Neale 21001)\tdelta method\t-\t0.2562\t0.0708\t-"
    "\nProportion mediated sensitivity\tindirect / total (95% CI -0.088 to 2.271)\tdelta method\t-\t1.091\t0.602\t0.0697"
)
io.open(os.path.join(TABDIR, "S16_mediation.tsv"), "w", encoding="utf-8", newline="").write(s16 + "\n")
print("S16_mediation.tsv updated")

s19 = "\n".join([
    "Analysis\tMethod\tNo. SNPs\tBeta\tSE\tOR (95% CI)\tP",
    "Neale 1498 replication\tInverse variance weighted\t24\t0.1682\t0.1215\t1.18 (0.93-1.50)\t0.166",
    "Neale 1498 replication\tWeighted median\t24\t0.1113\t0.1253\t1.12 (0.87-1.43)\t0.375",
    "Neale 1498 replication\tMR Egger\t24\t0.0973\t0.2582\t1.10 (0.66-1.83)\t0.710",
    "Neale 1498 replication\tWeighted mode\t24\t0.0386\t0.1205\t1.04 (0.82-1.32)\t0.752",
    "Neale 1498, palindromic SNPs excluded\tInverse variance weighted\t21\t0.1965\t0.1253\t1.22 (0.95-1.56)\t0.117",
    "Primary analysis (ukb-b-5237)\tInverse variance weighted\t34\t0.2347\t0.1120\t1.26 (1.02-1.57)\t0.036",
    "Cross-GWAS meta-analysis\tFixed effect\t-\t0.2042\t0.0823\t1.23 (1.04-1.44)\t0.013",
])
io.open(os.path.join(TABDIR, "S19_neale1498_replication.tsv"), "w", encoding="utf-8", newline="").write(s19 + "\n")
print("S19_neale1498_replication.tsv written")

print("\nTRANSFORM v4.5.4 COMPLETE")
