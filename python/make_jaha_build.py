# -*- coding: utf-8 -*-
"""make_jaha_build.py — create build_manuscript_v51_JAHA.js from the pre-NMCD-
compression build script (build_manuscript_v51.js.bak_nmcd, full-length v5.1).

Edits:
  1. Abstract -> JAHA three-label structured abstract (<=250 words), reusing
     the NMCD-compressed abstract text; old 4th paragraph deleted.
  2. Lay summary section deleted (JAHA does not use one).
  3. Insert "Nonstandard Abbreviations and Acronyms" + "Clinical Perspective"
     sections after the Abstract.
  4. Two body trims (intro aims paragraph; strengths/limitations) to bring
     body below ~6000 words; all key result strings preserved.
  5. Declarations relabelled to JAHA style ("Sources of Funding", "Disclosures").
Also creates build_supplement_v51_JAHA.js from its .bak_nmcd (long title).
"""
import re
import shutil
from pathlib import Path

BASE = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822")
BLD = BASE / "04_docx构建脚本"

src = (BLD / "build_manuscript_v51.js.bak_nmcd").read_text(encoding="utf-8")


def sub_literal(text, anchor, new_inner):
    pat = re.compile(r"T`[^`]*" + re.escape(anchor) + r"[^`]*`", re.S)
    n = len(pat.findall(text))
    if n != 1:
        raise SystemExit(f"ANCHOR NOT UNIQUE ({n}): {anchor[:70]}")
    return pat.sub(lambda m: "T`" + new_inner + "`", text, count=1)


# ---- 1. abstract: replace 4 paragraphs with JAHA 3-label version ----
src = sub_literal(src, "Aim: Milk tea",
    "Background: Milk tea (typically 35–50 g sugar and 100–200 mg caffeine "
    "per serving) has never been prospectively studied for atrial "
    "fibrillation (AF) and is not instrumented in genome-wide association "
    "studies (GWAS). We tested whether genetically proxied intake of its "
    "sweetened-beverage components is causally associated with AF.")
src = sub_literal(src, "Methods: Seven beverage exposures",
    "Methods and Results: Seven beverage exposures were instrumented in UK "
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
    "positive genetic correlations with AF (rg = 0.24–0.31; FDR q < 0.05).")
pat_res = re.compile(
    r"\s*mix\(\[\s*T`Results: No sweetened-beverage exposure[^`]*`,?\s*\]\),",
    re.S)
assert len(pat_res.findall(src)) == 1, "abstract results block not unique"
src = pat_res.sub("", src)
src = sub_literal(src, "Conclusions: Genetically proxied sweetened-beverage intake",
    "Conclusions: Genetically proxied sweetened-beverage intake showed no "
    "evidence of a causal association with AF; moderate-to-large effects are "
    "excluded, but small effects are not. The modest observational "
    "association likely reflects adiposity-related confounding; direct "
    "milk-tea studies in East Asian cohorts remain needed.")

# ---- 2. delete lay summary ----
pat_lay = re.compile(
    r"// ---------- Lay summary ----------.*?(?=// ---------- Introduction)",
    re.S)
assert len(pat_lay.findall(src)) == 1
src = pat_lay.sub("", src)

# ---- 3. insert NAA + Clinical Perspective after Abstract block ----
CP_BLOCK = """// ---------- Nonstandard Abbreviations and Clinical Perspective ----------
children.push(
  h1(T`Nonstandard Abbreviations and Acronyms`),
  mix([
    T`AF, atrial fibrillation; ASB, artificially sweetened beverage; BMI, body mass index; GWAS, genome-wide association study; IVW, inverse-variance weighted; LDSC, linkage disequilibrium score regression; MR, Mendelian randomization; MVMR, multivariable Mendelian randomization; MR-RAPS, MR robust adjusted profile score; OR, odds ratio; SNP, single-nucleotide polymorphism; SSB, sugar-sweetened beverage`,
  ])
);
children.push(
  h1(T`Clinical Perspective`),
  h2(T`What Is New?`),
  mix([
    T`• In the first unified Mendelian randomization framework of five sweetened-beverage phenotypes and their caffeinated counterparts against the largest public atrial fibrillation genome-wide association studies, genetically proxied sweetened-beverage intake showed no evidence of a causal association with atrial fibrillation across three European outcome sources and an East Asian contextual analysis.`,
  ]),
  mix([
    T`• The only nominal signal (coffee intake) was attributable to adiposity rather than caffeine pathways: it attenuated after body-mass-index adjustment and colocalized with atrial fibrillation only at the FTO locus, not at caffeine-metabolism loci.`,
  ]),
  mix([
    T`• Sweetened-beverage traits nevertheless share genetic architecture with atrial fibrillation (genetic correlations 0.24–0.31) despite null causal estimates.`,
  ]),
  h2(T`What Are the Clinical Implications?`),
  mix([
    T`• The modest observational association between sweetened beverages and atrial fibrillation most likely reflects adiposity-related confounding; prevention is better directed at established cardiometabolic risk factors, particularly weight management, than at beverage-specific avoidance.`,
  ]),
  mix([
    T`• These nulls exclude moderate-to-large effects but not small ones, and component-level nulls cannot certify the safety of composite milk-tea beverages; direct prospective studies of milk tea intake in East Asian cohorts remain needed.`,
  ])
);

// ---------- Introduction ----------"""
marker = "// ---------- Introduction ----------"
assert src.count(marker) == 1
src = src.replace(marker, CP_BLOCK)

# ---- 4. two body trims (texts already vetted in NMCD passes) ----
src = sub_literal(src, "Milk tea itself has never been studied",
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
    "sensitivity with alcohol as a positive control.")
src = sub_literal(src, "Strengths include",
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
    "triangulation would have been uninformative by design.")

# ---- 5. JAHA declaration labels ----
src = sub_literal(src, "Funding: None.",
    "Sources of Funding: None. This research received no specific grant "
    "from any funding agency in the public, commercial or not-for-profit "
    "sectors.")
src = sub_literal(src, "Conflicts of interest: The authors declare",
    "Disclosures: The authors declare no conflicts of interest.")

out = BLD / "build_manuscript_v51_JAHA.js"
out.write_text(src, encoding="utf-8")
print("written", out)

# ---- supplement: restore long-title build as JAHA variant ----
sp_src = (BLD / "build_supplement_v51.js.bak_nmcd").read_text(encoding="utf-8")
sp_out = BLD / "build_supplement_v51_JAHA.js"
sp_out.write_text(sp_src, encoding="utf-8")
print("written", sp_out)
