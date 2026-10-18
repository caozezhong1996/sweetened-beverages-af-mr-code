# -*- coding: utf-8 -*-
import io, sys

# ---------- supplement builder ----------
p = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本\build_supplement_v45.js"
s = io.open(p, encoding="utf-8").read()
REPS = [
('const T20 = readTsv(path.join(DIR, "S20_earlyonset_af_sensitivity.tsv"));',
 'const T20 = readTsv(path.join(DIR, "S20_earlyonset_af_sensitivity.tsv"));\nconst T21 = readTsv(path.join(DIR, "S21_coloc_tea.tsv"));'),
("Table S20 early-onset AF sensitivity analysis; Figure S1 leave-one-out",
 "Table S20 early-onset AF sensitivity analysis; Table S21 Bayesian colocalization of tea intake at caffeine-metabolism and FTO loci (Nielsen 2018 outcome); Figure S1 leave-one-out"),
]
for old, new in REPS:
    n = s.count(old)
    if n != 1:
        print("MISS/DUP supplement (%d): %s" % (n, old[:70])); sys.exit(1)
    s = s.replace(old, new)

s21_block = '''
children.push(caption("Table S21. Bayesian colocalization of tea intake at the caffeine-metabolism loci (CYP1A1-CYP1A2, AHR) and FTO against atrial fibrillation (Nielsen 2018)"));
children.push(makeTable(
  [2600, 2600, 1900, 1300, 1400],
  T21.header, T21.rows, 18));
children.push(note("Tea-intake region statistics came from the Neale lab UK Biobank round-2 release (field 1488, cups of tea per day; n = 349,376; LDSC-imputed v3 release) because per-variant summary statistics for the primary tea exposure GWAS (ukb-b-6066) were not retrievable at analysis time; per-variant effects were derived as beta = Z/sqrt(N) with varbeta = 1/N (standardised units, sdY = 1), the same Z-score convention used for the CAUSE and MRlap analyses. Variants were matched to the harmonized Nielsen 2018 statistics by rsid with exact allele-set alignment (3 allele mismatches excluded; palindromic variants excluded where the Nielsen effect-allele frequency lay between 0.42 and 0.58); SNP density follows the HapMap-3-based LDSC release (156-252 variants per 500-kb window versus 1,160-1,738 in the primary coffee analysis, Table S8), so tea posterior probabilities are slightly conservative. coloc.abf used default priors; PP.H1 denotes a tea-only association and PP.H4 a shared causal variant with AF. The identical 500-kb windows as the coffee analysis were interrogated."));

const doc = new Document({'''
old_tail = '''
const doc = new Document({'''
assert s.count(old_tail) == 1
s = s.replace(old_tail, s21_block)
io.open(p, "w", encoding="utf-8", newline="\n").write(s)
print("supplement builder: S21 added")

# ---------- manuscript builder ----------
p2 = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本\build_manuscript_v45.js"
m = io.open(p2, encoding="utf-8").read()
REPS2 = [
# methods trim (L197)
("Palindromic variants with intermediate allele frequencies were excluded during harmonization. Instrument strength was assessed with per-variant F statistics, with F > 10 required.",
 "Palindromic variants with intermediate allele frequencies were excluded. Instrument strength used per-variant F statistics (F > 10 required)."),
# coloc results: compress + tea sentence
("At the caffeine-metabolism loci CYP1A1\u2013CYP1A2 and AHR, the posterior probability overwhelmingly supported an association with coffee intake only (PP.H1 = 0.957 and 0.931), with negligible support for a shared causal variant with AF (PP.H4 = 0.005 and 0.008): coffee-specific genetic variation at these canonical caffeine-handling loci has no AF counterpart. At the FTO locus, the larger outcome GWAS turned previously split support into strong evidence for a shared causal variant (PP.H4 = 0.894), independently corroborated against FinnGen R13 (PP.H4 = 0.906), directly implicating adiposity-linked pleiotropy\u2014consistent with the attenuation of the coffee estimate after BMI adjustment.",
 "At CYP1A1\u2013CYP1A2 and AHR, posterior probabilities supported an association with coffee intake only (PP.H1 = 0.957 and 0.931), with negligible support for a shared causal variant with AF (PP.H4 = 0.005 and 0.008): coffee-specific variation at these caffeine-handling loci has no AF counterpart. At FTO, the larger outcome GWAS yielded strong evidence of a shared causal variant (PP.H4 = 0.894; FinnGen R13 0.906), directly implicating adiposity-linked pleiotropy\u2014consistent with the attenuation of the coffee estimate after BMI adjustment. Tea intake showed the identical dissociation in the same windows (Table S21): tea-only associations at CYP1A1\u2013CYP1A2 and AHR (PP.H1 = 0.993 and 0.988; PP.H4 \u2264 0.009) but a shared variant with AF at FTO (PP.H4 = 0.896)."),
("The shared-variant conclusion at FTO was robust to the colocalization prior: PP.H4 exceeded 0.8 for p12 \u2265 5 \u00d7 10\u207b\u2076 in both outcome sources and weakened only under the most stringent prior tested (p12 = 10\u207b\u2076; PP.H4 = 0.46\u20130.49; Table S13).",
 "The FTO shared-variant conclusion was robust to the colocalization prior (PP.H4 > 0.8 for p12 \u2265 5 \u00d7 10\u207b\u2076 in both sources; Table S13)."),
# discussion: tea clause after coffee coloc recap
("but shared a causal variant with AF at FTO (PP.H4 = 0.894; replicated at 0.906), and caffeine-metabolism-locus instruments were null while the remainder carried the signal.",
 "but shared a causal variant with AF at FTO (PP.H4 = 0.894; replicated at 0.906); tea showed the same dissociation (Table S21), and caffeine-metabolism-locus instruments were null while the remainder carried the signal."),
# small extra trims to hold word budget
("The signal does not satisfy the criteria for a credible causal interpretation;",
 "The signal does not meet our criteria for credible causal interpretation;"),
("At the trigger level, the one randomized trial of acute coffee exposure likewise found no excess of atrial arrhythmias [30], although case reports link high-dose caffeinated energy drinks to acute AF in young, low-risk individuals [35].",
 "At the trigger level, randomized acute coffee exposure found no excess of atrial arrhythmias [30], although case reports link high-dose energy drinks to acute AF in young, low-risk individuals [35]."),
("and leave-one-out analysis and funnel plots assessed influential instruments",
 "leave-one-out analysis and funnel plots assessed influential instruments"),
]
for old, new in REPS2:
    n = m.count(old)
    if n != 1:
        print("MISS/DUP manuscript (%d): %s" % (n, old[:80])); sys.exit(1)
    m = m.replace(old, new)
io.open(p2, "w", encoding="utf-8", newline="\n").write(m)
print("manuscript builder: tea coloc woven in")
