import fs from "node:fs";
import path from "node:path";
import {
  AlignmentType, Document, Footer, Header, HeadingLevel, Packer, PageNumber,
  Paragraph, ShadingType, Table, TableCell, TableRow, TextRun, WidthType,
} from "docx";

const outputPath = process.argv[2];
if (!outputPath) throw new Error("Usage: node build_supplement_v4.js /abs/out.docx");
fs.mkdirSync(path.dirname(outputPath), { recursive: true });

const palette = { dark: "263238", primary: "37474F", light: "78909C", fill: "EEF3F6" };
const font = { ascii: "Times New Roman", hAnsi: "Times New Roman", cs: "Times New Roman", eastAsia: "SimSun" };
const run = (text, o = {}) => new TextRun({ text, font, size: 24, ...o });
const para = (children, o = {}) =>
  new Paragraph({ spacing: { after: 120, line: 360 }, ...o, children: Array.isArray(children) ? children : [children] });
const h1 = (t) => para(run(t, { bold: true, size: 28, color: palette.dark }), { heading: HeadingLevel.HEADING_1, spacing: { before: 280, after: 120 } });
const caption = (t) => para(run(t, { bold: true, size: 22, color: palette.primary }), { spacing: { before: 200, after: 80 } });
const note = (t) => para(run(t, { size: 18, color: palette.light }), { spacing: { after: 200 } });

const cell = (text, width, size, o = {}) =>
  new TableCell({
    children: [new Paragraph({ spacing: { after: 10, line: 240 }, children: [run(String(text), { size })] })],
    margins: { top: 60, bottom: 60, left: 80, right: 80 },
    width: { size: width, type: WidthType.DXA },
    ...o,
  });
const makeTable = (widths, headerRow, bodyRows, size = 20) =>
  new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, children: headerRow.map((t, i) => cell(t, widths[i], size, { shading: { type: ShadingType.CLEAR, fill: palette.fill } })) }),
      ...bodyRows.map((r) => new TableRow({ children: r.map((t, i) => cell(t, widths[i], size)) })),
    ],
  });

const readTsv = (p) => {
  const lines = fs.readFileSync(p, "utf8").trim().split(/\r?\n/);
  return { header: lines[0].split("\t"), rows: lines.slice(1).map((l) => l.split("\t")) };
};

const DIR = String.raw`C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\06_升级分析_v4\supplement_tables`;
const S1 = readTsv(path.join(DIR, "S1_instruments.tsv"));
const S2 = readTsv(path.join(DIR, "S2_uvmr_full.tsv"));
const S3 = readTsv(path.join(DIR, "S3_het_pleio.tsv"));
const S5 = readTsv(path.join(DIR, "S5_alcohol_control.tsv"));
const S6 = readTsv(path.join(DIR, "S6_steiger.tsv"));
const S7 = readTsv(path.join(DIR, "S7_radial_reverse.tsv"));
const S8 = readTsv(path.join(DIR, "S8_coloc.tsv"));
const T5 = readTsv(path.join(DIR, "T5_power.tsv"));
const T13 = readTsv(path.join(DIR, "S13_coloc_priorscan.tsv"));
const T14 = readTsv(path.join(DIR, "S14_conmix.tsv"));
const T15 = readTsv(path.join(DIR, "S15_cause.tsv"));
const T16 = readTsv(path.join(DIR, "S16_mediation.tsv"));
const T17 = readTsv(path.join(DIR, "S17_mrlap.tsv"));
const T18 = readTsv(path.join(DIR, "S18_avblock.tsv"));
const T19 = readTsv(path.join(DIR, "S19_neale1498_replication.tsv"));
const T20 = readTsv(path.join(DIR, "S20_earlyonset_af_sensitivity.tsv"));
const T21 = readTsv(path.join(DIR, "S21_coloc_tea.tsv"));
const T17B = readTsv(path.join(DIR, "S17b_mrlap_tea.tsv"));
const T22 = readTsv(path.join(DIR, "S22_instrument_strength.tsv"));
const T23 = readTsv(path.join(DIR, "S23_mrraps.tsv"));
const T24 = readTsv(path.join(DIR, "S24_conditional_F.tsv"));

// display formatters for Tables S13/S14 (superscript scientific notation, 3-dp rounding)
const SUPC = { "0": "⁰", "1": "¹", "2": "²", "3": "³", "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹", "-": "⁻" };
const supNum = (s) => String(s).split("").map((c) => SUPC[c] || c).join("");
const fmtSci = (v) => { const [m, e] = v.toExponential(1).split("e"); return `${m} × 10${supNum(e)}`; };
const fmtPP = (x) => { const v = Number(x); if (!isFinite(v)) return String(x); return (v !== 0 && Math.abs(v) < 0.001) ? fmtSci(v) : v.toFixed(3); };
const fmtP = (x) => { const v = Number(x); if (!isFinite(v)) return String(x); return (v !== 0 && v < 0.001) ? fmtSci(v) : v.toFixed(3); };
const P12_LABEL = { "1e-06": "10⁻⁶", "5e-06": "5 × 10⁻⁶", "1e-05": "10⁻⁵", "2.5e-05": "2.5 × 10⁻⁵", "5e-05": "5 × 10⁻⁵" };

const children = [];
children.push(
  para(run("Supplementary Materials", { bold: true, size: 36, color: palette.dark }), { alignment: AlignmentType.CENTER, spacing: { after: 160 } }),
  para(run("Sweetened Beverage Consumption and Atrial Fibrillation: Two-Sample and Multivariable Mendelian Randomization", { size: 24, color: palette.primary }), { alignment: AlignmentType.CENTER, spacing: { after: 120 } }),
  para(run("Contents: Table S1 exposure GWAS, instrument selection thresholds and instrument strength; Table S2 complete univariable MR estimates (all exposures, outcome sources and methods); Table S3 heterogeneity and directional pleiotropy; Table S4 multivariable MR, MR-PRESSO and caffeine-pathway-restricted subgroup MR; Table S5 alcohol positive lifestyle control; Table S6 Steiger directionality tests; Table S7 radial IVW and reverse MR; Table S8 Bayesian colocalization at coffee-associated loci (AFGen 2018 vs Nielsen 2018); Table S9 STROBE-MR checklist; Table S10 single-trait SNP heritability and LDSC intercepts; Table S11 cross-trait LDSC genetic correlations between beverage intake and AF; Table S12 statistical power; Table S13 colocalization prior-sensitivity scan at the FTO locus; Table S14 contamination-mixture estimates for the nominal coffee signal; Table S15 CAUSE analysis of coffee intake and AF; Table S16 two-step (network) mediation MR through BMI; Table S17 MRlap correction for sample overlap, winner's curse and weak-instrument bias (coffee), continued for tea intake; Table S18 atrioventricular-block negative outcome control; Table S19 independent coffee-exposure GWAS replication and cross-GWAS meta-analysis; Table S20 early-onset AF sensitivity analysis; Table S21 Bayesian colocalization of tea intake at caffeine-metabolism and FTO loci (Nielsen 2018 outcome); Table S22 instrument-strength metrics for all beverage exposures; Table S23 MR-RAPS robust adjusted profile score estimates for all exposures against both co-primary outcomes; Table S24 Sanderson–Windmeijer conditional F statistics for the multivariable MR instrument set; Figure S1 leave-one-out and funnel plots (separate PNG); Figure S2 LDSC genetic-correlation forest plot (separate PNG). Per-SNP harmonized datasets are provided as CSV files in Supplementary_Data_Files.zip within the Zenodo archive (https://doi.org/10.5281/zenodo.22099675).", { size: 20, color: palette.light }), { spacing: { after: 300 } })
);

children.push(caption("Table S1. Exposure GWAS, instrument selection thresholds and instrument strength"));
children.push(makeTable([2150, 1350, 1100, 1350, 1750, 1050, 950], S1.header, S1.rows, 18));
children.push(note("F statistics are per-variant (beta²/se²) on the exposure side and are therefore identical across outcome sources. SSB, sugar-sweetened beverage; ASB, artificially sweetened beverage. Instruments for coffee and tea intake reached genome-wide significance (P < 5 × 10⁻⁸); the five beverage sub-phenotypes used the pre-specified relaxed threshold (P < 5 × 10⁻⁶) because fewer than three independent variants reached P < 5 × 10⁻⁸."));

children.push(caption("Table S2. Complete univariable Mendelian randomization estimates for all exposures, outcome sources and methods"));
children.push(makeTable([1900, 1750, 1850, 850, 1900, 950], S2.header, S2.rows, 16));
children.push(note("IVW estimates are random-effects. OR, odds ratio per unit higher genetically instrumented intake. EUR, European; EAS, East Asian. Nielsen 2018 is the primary outcome; AFGen 2018 is a sensitivity source that shares cohorts with Nielsen 2018."));

children.push(caption("Table S3. Heterogeneity (Cochran Q, IVW) and directional pleiotropy (MR-Egger intercept)"));
children.push(makeTable([2000, 1800, 1300, 1100, 1900, 1300], S3.header, S3.rows, 18));
children.push(note("Significant heterogeneity was observed for tea intake (all four sources), coffee intake (Nielsen 2018, AFGen 2018, FinnGen R13), sugar added to tea (Nielsen 2018, FinnGen R13, BioBank Japan) and sugar added to coffee (Nielsen 2018, FinnGen R13, BioBank Japan); no Egger intercept was significant."));

children.push(caption("Table S4. Multivariable MR, MR-PRESSO and caffeine-pathway-restricted subgroup MR results"));
children.push(makeTable(
  [3000, 2300, 1300, 1100, 2100],
  ["Analysis", "Estimate, OR (95% CI) or beta", "P value", "No. SNPs", "Note"],
  [
    ["MVMR: body mass index (conditional)", "1.47 (1.37–1.57)", "2.0 × 10⁻²⁷", "467", "Positive control (Nielsen 2018 outcome)"],
    ["MVMR: coffee intake (conditional on BMI and sugar added to tea)", "0.82 (0.65–1.04)", "0.099", "14", "Univariable nominal signal attenuated to null"],
    ["MVMR: sugar added to tea (conditional)", "0.99 (0.81–1.22)", "0.96", "1", "Uninformative: single joint instrument"],
    ["MR-PRESSO: coffee intake → AF (Nielsen 2018)", "raw beta 0.235; outlier-corrected beta 0.116", "raw 0.044; corrected 0.20", "34", "Global heterogeneity P = 0.002; 2 outlier variants identified; outlier-corrected estimate null"],
    ["MR-PRESSO: coffee intake → AF (FinnGen R13)", "raw beta 0.458; outlier-corrected beta 0.345", "raw 0.021; corrected 0.007", "34", "Global heterogeneity P < 0.001; outlier-corrected estimate remained nominal — robustness to outlier correction is source-dependent"],
    ["Subgroup MR: caffeine-metabolism instruments only → AF (Nielsen 2018)", "OR 1.03 (0.76–1.38)", "0.86", "3", "rs2472297 (CYP1A1–CYP1A2), rs4410790 (AHR), rs117968677; caffeine-pathway proxies have no detectable AF effect"],
    ["Subgroup MR: caffeine-metabolism instruments only → AF (FinnGen R13)", "OR 1.23 (0.73–2.07)", "0.44", "3", "Same three instruments; consistent null in the larger source"],
    ["Subgroup MR: remaining coffee instruments → AF (Nielsen 2018)", "OR 1.50 (1.12–2.01)", "0.006", "31", "Signal carried entirely by non-caffeine-pathway instruments"],
    ["Subgroup MR: remaining coffee instruments → AF (FinnGen R13)", "OR 1.96 (1.18–3.24)", "0.009", "31", "Replicated in FinnGen R13; weighted median OR 2.16 (1.37–3.38), P = 0.0008"],
  ], 18
));
children.push(note("MVMR, multivariable Mendelian randomization (IVW); outcome is atrial fibrillation (Nielsen 2018, European ancestry). MR-PRESSO was applied to coffee intake, the only exposure with a nominal IVW association against the primary outcome."));

children.push(caption("Table S5. Positive lifestyle control: alcohol consumption and atrial fibrillation (IVW)"));
children.push(makeTable([2600, 2100, 1000, 2100, 1100], S5.header, S5.rows, 18));
children.push(note("Alcohol intake frequency: UK Biobank ukb-b-5779 (N = 462,346; ordinal frequency categories; 99 genome-wide-significant instruments, 97 retained after harmonization against Nielsen 2018). Alcoholic drinks per week: GSCAN consortium ieu-b-73 (N = 335,394; 35 instruments). The European meta-analysis combines Nielsen 2018 and FinnGen release R13 by fixed-effect meta-analysis. Genetically instrumented drinks per week were directionally associated with higher AF odds in all four cohorts and nominally significant in the European meta-analysis (P = 0.035), confirming that the analytical pipeline detects an established lifestyle causal effect; intake frequency per se was null throughout, consistent with cumulative quantity rather than frequency driving AF risk."));

const strobe = [
  ["1. Title and abstract", "Indicate MR as the study design", "Title; Abstract (Methods)"],
  ["2. Background", "Scientific background and rationale", "Introduction, paragraphs 1–4"],
  ["3. Objectives", "Pre-specified hypotheses stated", "Introduction, final paragraph"],
  ["4. Study design and data sources", "Design, data sources, time periods", "Methods — Study design; Data sources; Table 1"],
  ["5. Participants / setting", "Eligibility and setting of contributing studies", "Methods — Data sources; Table 1"],
  ["6. Variables", "Exposures, outcomes, covariates", "Methods — Data sources; Instrument selection"],
  ["7. Data sources / measurement", "Measurement of exposures and outcomes", "Methods — Data sources; Table 1"],
  ["8. Bias", "MR assumptions and their assessment", "Methods — Study design; Instrument selection; Statistical analysis"],
  ["9. Study size", "Sample sizes of all GWAS", "Table 1; Table S1"],
  ["10. Quantitative variables", "Scaling of estimates", "Methods — Statistical analysis; Table 2 footnote"],
  ["11a. Statistical methods", "Main methods", "Methods — Statistical analysis"],
  ["11b. Assumptions", "Assessment of MR assumptions", "Methods; Tables 3, S3 (heterogeneity, intercepts, F statistics)"],
  ["11c. Sensitivity analyses", "MR-Egger, weighted median/mode, MR-PRESSO, MVMR", "Methods; Tables 3–4, S2–S4"],
  ["12a. Descriptive data", "Genetic variants at each stage", "Results — Genetic instruments; Table S1"],
  ["12b. Flow of variants", "Numbers retained after each step", "Results; Table S1"],
  ["13. Outcome data", "Case/control numbers", "Table 1"],
  ["14. Main results", "Primary IVW estimates", "Results; Table 2; Figure 2"],
  ["15. Other analyses", "Sensitivity, MVMR, replication, positive control", "Results; Tables 3–4, S5"],
  ["16. Key results", "Summary with reference to objectives", "Discussion — Principal findings"],
  ["17. Limitations", "Direction/magnitude of potential bias", "Discussion — Strengths and limitations"],
  ["18. Interpretation", "Comparison with prior work, mechanisms, implications", "Discussion"],
  ["19. Generalisability", "External validity across ancestries/populations", "Discussion — Clinical and public-health implications; Limitations"],
  ["20. Funding", "Funding sources", "Declarations (none)"],
  ["21. Data availability", "Public data and code access", "Declarations — Data availability; Table 1 identifiers"],
];

children.push(caption("Table S6. Steiger directionality tests (primary outcome: Nielsen 2018)"));
children.push(makeTable([2300, 900, 1500, 1500, 1300, 1300, 1200], S6.header, S6.rows, 18));
children.push(note("R² values are aggregate variance-explained approximations computed from effect estimates, allele frequencies and sample sizes; the exposure-to-outcome direction was supported for every exposure, with no per-variant Steiger violations. The Steiger P for coffee intake was below the smallest representable value and is reported as 1.0 × 10⁻³⁰⁰."));

children.push(caption("Table S7. Radial IVW sensitivity estimates and reverse MR (AF → beverage intake), Nielsen 2018"));
children.push(makeTable([2300, 2400, 1100, 2700, 1100, 1300], S7.header, S7.rows, 18));
children.push(note("Radial IVW used modified second-order weights against the Nielsen 2018 outcome; estimates were unchanged from standard IVW. Reverse MR instruments: 111 independent AF-associated SNPs (P < 5 × 10⁻⁸) from Nielsen 2018; betas are per log-OR higher AF liability. No reverse association reached nominal significance (all P ≥ 0.054); the nominal reverse association with sugar added to tea seen in the earlier AFGen-based analysis (P = 0.030) did not replicate with the upgraded instruments (P = 0.17)."));

children.push(caption("Table S8. Bayesian colocalization (coloc.abf) of coffee intake and atrial fibrillation at the three loci harbouring the strongest coffee instruments: AFGen 2018 vs Nielsen 2018 outcome; FTO additionally vs FinnGen R13 (variants matched by rsID across genome builds)"));
children.push(makeTable([2100, 2100, 1000, 1250, 1250, 1200, 1200, 1450, 1250], S8.header, S8.rows, 16));
children.push(note("Coffee intake: UK Biobank ukb-b-5237 (N = 428,860). AF outcomes: AFGen 2018 ebi-a-GCST006061 (55,114 cases / 482,295 controls), Nielsen 2018 ebi-a-GCST006414 (60,620 cases / 970,216 controls) and FinnGen release R13 (I9_AF; 67,783 cases / 241,269 controls). coloc.abf with default priors; PP.H4 > 0.8 indicates a shared causal variant. At the caffeine-metabolism loci (CYP1A1–CYP1A2, AHR) the signal is coffee-specific (PP.H1 ≥ 0.93) with no AF counterpart in either outcome. At the adiposity locus FTO, the larger Nielsen 2018 outcome resolved previously split support (PP.H4 = 0.362) into strong evidence of a shared causal variant (PP.H4 = 0.894), independently replicated in FinnGen R13 (PP.H4 = 0.906; 1,675 harmonized SNPs), corroborating adiposity-linked pleiotropy as the source of the nominal coffee–AF signal. Per-region summary statistics: 03_结果数据_mr_results/upgrade_coloc_*.csv (AFGen), 06_升级分析_v4/results/upgrade_coloc_coffee_loci_Nielsen.csv (Nielsen) and upgrade_coloc_FTO_FinnGenR13.csv (R13)."));

children.push(caption("Table S9. STROBE-MR checklist (condensed)"));
children.push(makeTable([2500, 4200, 3600], ["Item", "Requirement", "Location in manuscript"], strobe, 18));
children.push(note("Checklist condensed from Skrivankova et al., JAMA 2021;326:1614-1621. The study was not formally pre-registered; a written analysis plan was finalized before analysis."));

children.push(caption("Table S10. Single-trait observed-scale SNP heritability and LDSC intercepts (1000 Genomes EUR HapMap 3 LD scores; two-step weighted least squares; 200-block jackknife standard errors)"));
children.push(makeTable(
  [2400, 2200, 1300, 1500, 1500, 1500, 1400],
  ["Trait", "GWAS source", "No. SNPs", "h² (observed)", "h² SE", "Intercept", "Intercept SE"],
  [
    ["Coffee intake", "Neale lab UKB r2 (field 1498)", "1,078,763", "0.0556", "0.0046", "1.003", "0.011"],
    ["Tea intake", "Neale lab UKB r2 (field 1488, raw)", "1,078,767", "0.0627", "0.0043", "0.994", "0.011"],
    ["Sugar added to coffee", "Neale lab UKB r2 (field 100370)", "1,078,768", "0.0465", "0.0111", "0.994", "0.007"],
    ["Fizzy drink intake (SSB)", "Neale lab UKB r2 (field 100170)", "1,078,768", "0.0201", "0.0101", "0.999", "0.006"],
    ["Low-calorie drink intake (ASB)", "Neale lab UKB r2 (field 100160)", "1,078,768", "0.0221", "0.0108", "1.005", "0.007"],
    ["Atrial fibrillation", "Nielsen 2018 (GCST006414)", "1,289,722", "0.0252", "0.0020", "1.051", "0.023"],
    ["Atrial fibrillation", "FinnGen R13 (I9_AF)", "1,278,261", "0.0894", "0.0054", "1.214", "0.031"],
  ], 18
));
children.push(note("Analyses restricted to HapMap 3 SNPs with 1000 Genomes EUR LD scores (eur_w_ld_chr; M = 1,290,027) after χ² outlier filtering (per Bulik-Sullivan et al., 2015). Estimates are on the observed scale; heritability of the binary AF outcome is not liability-transformed. Intercepts near 1 indicate little residual stratification or unmodelled overlap; the FinnGen R13 intercept (1.214) is typical of registry-based biobank GWAS. Full per-variant summary statistics for sugar added to tea and artificial sweetener added to tea (IEU PHESANT subsets, N = 64,949) are not publicly distributed and are therefore absent."));

children.push(caption("Table S11. Cross-trait LDSC genetic correlations (rg) between beverage intake and atrial fibrillation, with cross-trait intercepts as a sample-overlap diagnostic"));
children.push(makeTable(
  [2150, 1500, 1300, 1300, 1200, 1200, 1500, 1500, 1200],
  ["Exposure", "AF outcome", "No. SNPs", "rg", "rg SE", "P", "FDR q", "Cross-trait intercept", "Intercept SE"],
  [
    ["Coffee intake", "Nielsen 2018", "1,076,960", "+0.038", "0.037", "0.295", "0.491", "−0.011", "0.008"],
    ["Coffee intake", "FinnGen R13", "1,068,079", "+0.075", "0.037", "0.042", "0.126", "−0.018", "0.008"],
    ["Tea intake", "Nielsen 2018", "1,076,960", "+0.015", "0.034", "0.656", "0.821", "+0.009", "0.007"],
    ["Tea intake", "FinnGen R13", "1,068,079", "−0.007", "0.033", "0.843", "0.873", "+0.014", "0.008"],
    ["Sugar added to coffee", "Nielsen 2018", "1,076,960", "−0.012", "0.072", "0.873", "0.873", "−0.002", "0.006"],
    ["Sugar added to coffee", "FinnGen R13", "1,068,079", "−0.060", "0.063", "0.344", "0.491", "−0.004", "0.006"],
    ["Fizzy drink intake (SSB)", "Nielsen 2018", "1,076,960", "+0.218", "0.111", "0.050", "0.126", "−0.001", "0.006"],
    ["Fizzy drink intake (SSB)", "FinnGen R13", "1,068,079", "+0.239", "0.089", "0.007", "0.035", "−0.006", "0.006"],
    ["Low-calorie drink intake (ASB)", "Nielsen 2018", "1,076,960", "+0.152", "0.089", "0.088", "0.177", "+0.010", "0.005"],
    ["Low-calorie drink intake (ASB)", "FinnGen R13", "1,068,079", "+0.313", "0.103", "0.002", "0.025", "+0.003", "0.006"],
    ["Nielsen 2018 (positive control)", "FinnGen R13", "1,170,277", "+0.923", "0.101", "5.8 × 10⁻²⁰", "—", "+0.042", "0.020"],
    ["Coffee intake (overlap control)", "Tea intake", "1,078,768", "+0.005", "0.077", "0.952", "—", "−0.318", "0.011"],
  ], 16
));
children.push(note("Effect alleles were aligned across sources and palindromic variants excluded; rg standard errors and cross-trait intercepts were estimated by 200-block jackknife. FDR q values apply Benjamini–Hochberg correction across the ten beverage–AF tests; the two control rows are outside the correction family. The cross-trait intercept indexes the product of sample overlap and phenotypic correlation: all beverage–AF intercepts were indistinguishable from zero (|intercept| ≤ 0.018), quantitatively excluding material sample-overlap bias, whereas the overlap control (coffee × tea intake, both UK Biobank) showed the expected large intercept (−0.318, consistent with their inverse phenotypic correlation), and the same-trait control (two independent AF GWAS) returned rg = 0.923, validating the implementation. SSB, sugar-sweetened beverage; ASB, artificially sweetened beverage."));

children.push(caption("Table S12. Statistical power of the Mendelian randomization analyses"));
children.push(makeTable([2500, 1100, 2300, 1900, 2000], T5.header, T5.rows, 18));
children.push(note("Minimum detectable odds ratios at 80% power (two-sided α = 0.05) were computed from the realized standard error of each IVW estimate as exp[(z₀.₉₇₅ + z₀.₈₀) × SE]; power to detect OR 1.10 (the magnitude reported by observational cohorts) used the same realized precision. SNP counts refer to the primary (Nielsen 2018) analysis."));

children.push(caption("Table S13. Colocalization prior-sensitivity scan at the FTO locus (coffee intake vs atrial fibrillation): posterior probabilities as the coloc.abf prior p12 is varied"));
children.push(makeTable(
  [1400, 1700, 1100, 1000, 1400, 1400, 1400],
  ["Locus", "Outcome", "p12", "No. SNPs", "PP.H1", "PP.H3", "PP.H4"],
  T13.rows.map((r) => [r[0], r[1], P12_LABEL[r[2]] || r[2], r[3], fmtPP(r[4]), fmtPP(r[5]), fmtPP(r[6])]), 18));
children.push(note("The coloc.abf default prior is p12 = 10⁻⁵. The shared-causal-variant conclusion at FTO held for p12 ≥ 5 × 10⁻⁶ in both outcome sources (PP.H4 ≥ 0.81) and weakened only under the most stringent prior (p12 = 10⁻⁶; PP.H4 = 0.46–0.49), which a priori disfavours colocalization; higher priors increased PP.H4 to ≥ 0.95. The Nielsen 2018 region dataset was rebuilt from the local full summary statistics for this scan (1,740 harmonized SNPs; PP.H4 = 0.894 at the default prior, exactly reproducing the primary analysis). Prior scans at CYP1A1–CYP1A2 and AHR were not repeated: those loci supported a coffee-specific signal (PP.H1 ≥ 0.93), a conclusion driven by the absence of an AF association and insensitive to p12, and their caffeine-pathway instruments were additionally null in subgroup MR (Table S4)."));

children.push(caption("Table S14. Contamination-mixture (conmix) estimates for the nominal coffee–atrial fibrillation signal"));
children.push(makeTable(
  [3400, 1100, 2700, 1300],
  ["Analysis", "No. SNPs", "conmix estimate, beta (95% CI)", "P value"],
  T14.rows.map((r) => [r[0].replace(" -> ", " → "), r[1], `${Number(r[2]).toFixed(3)} (${r[3]} to ${r[4]})`, fmtP(r[5])]), 18));
children.push(note("The contamination-mixture estimator (Burgess et al., 2020; manuscript ref 24) remains consistent when only a subset of instruments is valid. Estimates mirror the source-dependent robustness pattern seen in the weighted-median and MR-PRESSO analyses: null in Nielsen 2018 but positive in FinnGen R13, so the nominal coffee signal cannot be credibly interpreted as causal, although a small genuine effect cannot be excluded."));

children.push(caption("Table S15. CAUSE analysis of coffee intake and atrial fibrillation (Nielsen 2018): causal versus correlated-pleiotropy (sharing) model"));
children.push(makeTable(
  [5200, 4200],
  T15.header, T15.rows, 18));
children.push(note("CAUSE (Morrison et al., 2020; manuscript ref 25) compares a causal model with a correlated-pleiotropy (sharing) model using genome-wide summary statistics and explicitly models sample overlap (estimated rho ≈ 0.001). Both traits entered as Z-scores with unit standard errors (the same munged files used for the LDSC analysis, Tables S10–S11); gamma and eta are therefore in Z units and only their sign and precision are interpreted. The causal model did not fit significantly better than the sharing model (P = 0.534) and the posterior causal effect gamma was centred on zero, consistent with the weighted-median, contamination-mixture and colocalization analyses: the coffee–AF genetic overlap is adequately explained by correlated pleiotropy, including the adiposity-mediated component colocalizing at FTO (Tables S8 and S13)."));

children.push(caption("Table S16. Two-step (network) mediation MR of coffee intake, body mass index and atrial fibrillation (Nielsen 2018 outcome)"));
children.push(makeTable(
  [1900, 4300, 1900, 1050, 950, 950, 900],
  T16.header, T16.rows, 18));
children.push(note("Network (two-step) mediation MR (Burgess et al., 2015; manuscript ref 21) applied to the sole nominal signal as a mechanistic probe. Step 1 used the 17 of 34 coffee instruments represented in the HapMap-2-based Yengo 2018 BMI meta-analysis (GCST006900; SD-standardised units, verified against FTO anchor variants); cross-matching by chromosome:position recovered no further instruments. Step 2 used 701 BMI instruments (P < 5 x 10-8) selected by 1-Mb window pruning (lowest P retained; a conservative substitute for LD clumping without a compatible reference panel); the BMI-AF estimate (0.343, SE 0.026) agreed with the MVMR conditional estimate (0.384, SE 0.035; Table S4) and with the weighted median (0.316, SE 0.035). Indirect effect and mediated proportion used the product method with delta-method standard errors; covariance between steps (partially overlapping UK Biobank samples) was ignored, so confidence intervals are slightly anti-conservative. A mediated proportion above 100% with a null direct effect mirrors the MVMR attenuation (OR 0.82; P = 0.099) and indicates that the nominal total association is statistically explained by the adiposity pathway. A pre-specified sensitivity analysis repeated step 1 against the full-coverage Neale lab UK Biobank BMI GWAS (field 21001; raw kg/m2 units; n = 359,983), recovering 33 of 34 coffee instruments (only rs117810762 unmatched); beta_XM = 3.587 kg/m2 (0.747 SD at 4.8 kg/m2 per SD) and the mediated proportion was 109% (95% CI -9% to 227%), concordant with the primary Yengo estimate; 21001 units were verified at the FTO locus anchor (beta = 0.359 kg/m2)."));

children.push(caption("Table S17. MRlap correction for sample overlap, winner's curse and weak-instrument bias: coffee intake and atrial fibrillation (Nielsen 2018)"));
children.push(makeTable(
  [5200, 3300, 1100, 1000],
  T17.header, T17.rows, 18));
children.push(note("MRlap (Mounier & Kutalik, 2023; manuscript ref 26) approximates sample overlap by cross-trait LDSC (GenomicSEM implementation) and derives a corrected causal estimate under a spike-and-slab genetic-architecture model; both traits entered as Z-scores from the same munged files used for the LDSC analysis (Tables S10-S11), so effects are per SD and only sign and precision are interpreted. The corrected effect (0.037, SE 0.023) did not differ significantly from the observed IVW effect (0.028, SE 0.018; difference P = 0.070), and the cross-trait intercept (-0.010, SE 0.006) matched the independent LDSC diagnostic (-0.011, SE 0.008; Table S11), jointly excluding material bias from sample overlap, winner's curse and weak instruments. HapMap-3 SNP list: w_hm3.snplist (MHC retained); 8,000 simulations were used for the variance of the corrected effect."));

children.push(caption("Table S17 (continued). MRlap correction for sample overlap, winner's curse and weak-instrument bias: tea intake and atrial fibrillation (both co-primary outcomes)"));
children.push(makeTable(
  [1400, 4000, 2200, 1000, 1000],
  ["Outcome", "Quantity", "Estimate", "SE", "P"],
  T17B.rows.map((r) => [r[0] === "Nielsen2018" ? "Nielsen 2018" : (r[0] === "FinnGenR13" ? "FinnGen R13" : r[0]), r[1], r[2], r[3], r[4]]), 18));
children.push(note("Extension of the MRlap analysis from coffee to tea (the only other exposure with genome-wide-significant instruments and public full summary statistics), requested in revision. Corrected and observed tea estimates were closely similar against both co-primary outcomes; across three independent runs the difference test gave P = 0.057-0.097 (Nielsen 2018) and P = 0.18-0.24 (FinnGen R13), the residual variability reflecting the 8,000-simulation variance estimation. MRlap is not applicable to the five relaxed-threshold sub-phenotypes, whose instruments (P < 5 × 10⁻⁶) do not survive the genome-wide-significance threshold MRlap requires; for those exposures, MR-RAPS (Table S23) and the contamination-mixture estimator (Table S14) serve as the weak-instrument-robust alternatives."));

children.push(caption("Table S18. Negative outcome control: beverage exposures and alcohol controls against atrioventricular block (FinnGen R13 I9_AVBLOCK)"));
children.push(makeTable(
  [3600, 2400, 1100, 1050, 1000, 1050],
  T18.header, T18.rows, 18));
children.push(note("Atrioventricular block was chosen a priori as a negative outcome (a conduction disorder with no hypothesised causal link to beverage intake). Six of nine exposure tests were null (P >= 0.53). Three nominal associations emerged - alcohol intake frequency (+0.186, P = 0.043), coffee intake (+0.480, P = 0.042) and sugar added to tea (-0.676, P = 0.001) - of which only sugar added to tea survived Bonferroni correction across the nine tests (threshold P = 0.006). The coffee and sugar-in-tea estimates mirrored the direction and magnitude of their AF associations (+0.458 and -0.506, respectively, in FinnGen R13), the expected behaviour if both endpoints share the adiposity-mediated pathway (BMI is an established risk factor for atrioventricular block); the analysis is therefore interpreted as a positive control for the shared pathway rather than a discriminator of instrument validity, and AF-specificity of these instruments cannot be formally established (manuscript Limitations)."));


children.push(caption("Table S19. Independent coffee-exposure GWAS replication (Neale lab UK Biobank field 1498) and cross-GWAS fixed-effect meta-analysis (Nielsen 2018 outcome)"));
children.push(makeTable(
  [3000, 1900, 1050, 950, 950, 1650, 900],
  T19.header, T19.rows, 18));
children.push(note("Replication instruments came from the Neale lab UK Biobank round-2 GWAS of coffee intake (field 1498; n = 334,659; effects per ALT allele, validated by 9/9 sign concordance with the primary instruments at shared loci): 3,147 variants at P < 5 x 10-8 after excluding low-confidence calls, pruned to 27 independent loci by 1-Mb window pruning (lowest P retained); 24 were recoverable in the harmonized Nielsen 2018 statistics by chromosome:position with exact ref/alt allele matching (three palindromic SNPs retained on exact plus-strand match; excluding them gave IVW OR 1.22, 0.95-1.56; P = 0.117). Per-variant F statistics: minimum 29.7, median 45.2. 19 of 24 replication instruments lay within 1 Mb of a primary-analysis locus. MR-Egger intercept 0.002 (P = 0.757); Cochran's Q P = 0.002. The replication point estimate is directionally concordant but the smaller instrument set limits power; the fixed-effect cross-GWAS meta-analysis (OR 1.23, 1.04-1.44; P = 0.013) is more precise than either source alone."));

children.push(caption("Table S20. Early-onset atrial fibrillation sensitivity analysis (Choi et al. 2018, GWAS Catalog GCST010636; TOPMed freeze 4 whole-genome sequencing)"));
children.push(makeTable(
  [2400, 700, 1700, 800, 900, 1700, 800, 1100, 900],
  T20.header, T20.rows, 18));
children.push(note("Early-onset AF (onset before age 66) summary statistics were from Choi et al., 2018 (manuscript ref 37; GWAS Catalog GCST010636; NHLBI TOPMed freeze 4 whole-genome sequencing; 2,781 European-ancestry cases and 4,959 controls from nine studies; no UK Biobank participation, hence no sample overlap with the exposure GWAS). The release provides score-test statistics only; per-variant effect estimates were recovered as beta = Score/Var with SE = Var^-1/2 (the z-to-p identity was verified against the reported Score.pval to <1 x 10-12). Instruments were matched by chromosome:position (hg19) with exact allele alignment: 126 of 137 instrument-outcome pairs (92%) were recovered, with zero allele mismatches and zero allele-frequency discordances. IVW used multiplicative random effects; weighted-median standard errors used 1,000 bootstrap draws. No exposure approached significance (all IVW P >= 0.11), point estimates were directionally inconsistent, and no MR-Egger intercept indicated directional pleiotropy (all P >= 0.13). Confidence intervals are wide, so the analysis is a consistency check rather than an exclusion of moderate effects; the nominal coffee association did not persist (weighted-median OR 1.39; MR-Egger OR 0.86)."));

children.push(caption("Table S21. Bayesian colocalization of tea intake at the caffeine-metabolism loci (CYP1A1-CYP1A2, AHR) and FTO against atrial fibrillation (Nielsen 2018)"));
children.push(makeTable(
  [2600, 2600, 1900, 1300, 1400],
  T21.header, T21.rows, 18));
children.push(note("Tea-intake region statistics came from the Neale lab UK Biobank round-2 release (field 1488, cups of tea per day; n = 349,376; LDSC-imputed v3 release) because per-variant summary statistics for the primary tea exposure GWAS (ukb-b-6066) were not retrievable at analysis time; per-variant effects were derived as beta = Z/sqrt(N) with varbeta = 1/N (standardised units, sdY = 1), the same Z-score convention used for the CAUSE and MRlap analyses. Variants were matched to the harmonized Nielsen 2018 statistics by rsid with exact allele-set alignment (3 allele mismatches excluded; palindromic variants excluded where the Nielsen effect-allele frequency lay between 0.42 and 0.58); SNP density follows the HapMap-3-based LDSC release (156-252 variants per 500-kb window versus 1,160-1,738 in the primary coffee analysis, Table S8), so tea posterior probabilities are slightly conservative. coloc.abf used default priors; PP.H1 denotes a tea-only association and PP.H4 a shared causal variant with AF. The identical 500-kb windows as the coffee analysis were interrogated."));

children.push(caption("Table S22. Instrument-strength metrics for all beverage exposures (primary Nielsen 2018 outcome instrument sets)"));
children.push(makeTable(
  [2600, 1600, 900, 1100, 1100, 1100, 1200],
  T22.header, T22.rows, 18));
children.push(note("Per-variant F statistics computed as (beta/se)² from the harmonized instrument sets used against the primary outcome (identical to Table 2 SNP counts); cumulative R² as 2·EAF·(1−EAF)·beta² summed over instruments. All per-variant F statistics exceed 20; however, F statistics capture neither winner's curse nor correlated pleiotropy, which are addressed by MR-RAPS (Table S23) and MRlap (Table S17), respectively discussed in the manuscript Limitations."));

children.push(caption("Table S23. MR-RAPS (robust adjusted profile score) estimates for all beverage exposures against both co-primary outcomes"));
children.push(makeTable(
  [2800, 1700, 900, 1500, 1000, 1100],
  T23.header, T23.rows, 18));
children.push(note("MR-RAPS (Zhao et al., 2020; manuscript ref 39) provides inference robust to many weak and pleiotropic instruments; over-dispersion was allowed with the Tukey loss function (the original MR-RAPS procedure, mr.raps.mle; the weight-shrinkage variant did not converge for these short instrument sets, consistent with its documented behaviour with few weak instruments). Estimates were directionally consistent with the primary IVW analysis for all 14 exposure–outcome pairs: every exposure was null against Nielsen 2018, including coffee (log-OR 0.17, P = 0.11); against FinnGen R13 the nominal coffee (log-OR 0.41, P = 0.045) and inverse sugar-added-to-tea (log-OR −0.37, P = 0.032) associations persisted at nominal significance, mirroring that source's primary estimates, and neither survived correction for the 14 tests. MR-RAPS thus corroborates, rather than overturns, the source-dependent reading of both nominal signals."));

children.push(caption("Table S24. Sanderson–Windmeijer conditional F statistics for the multivariable MR instrument set (471 harmonized SNPs)"));
children.push(makeTable(
  [2800, 1400, 1900, 1900],
  ["Exposure", "Conditional F", "Conventional threshold", "Harmonized SNPs (n)"],
  T24.rows.map((r) => [r[0], r[1], r[2], r[3]]), 18));
children.push(note("Conditional F statistics quantify each exposure's instrument strength conditional on the other exposures in the multivariable model (Sanderson et al., 2019; manuscript ref 42); values below the conventional threshold of 10 indicate limited conditional strength, biasing multivariable estimates towards the null. Computed with MVMR::strength_mvmr (exposure covariance fixed at 0, the package default). The re-derived joint instrument set reproduced the multivariable MR estimates in Table 4 exactly (regression coefficients and standard errors identical to 8 decimal places), confirming fidelity to the primary analysis."));

const doc = new Document({
  features: { updateFields: false },
  sections: [{
    properties: { page: { margin: { top: 1200, bottom: 1200, left: 1000, right: 1000 } } },
    headers: { default: new Header({ children: [para(run("Sweetened beverages and atrial fibrillation — Supplementary Materials", { size: 18, color: palette.light }), { alignment: AlignmentType.CENTER })] }) },
    footers: { default: new Footer({ children: [para(new TextRun({ children: [PageNumber.CURRENT] }), { alignment: AlignmentType.CENTER })] }) },
    children,
  }],
});
const buffer = await Packer.toBuffer(doc);
fs.writeFileSync(outputPath, buffer);
console.log("written:", outputPath);
