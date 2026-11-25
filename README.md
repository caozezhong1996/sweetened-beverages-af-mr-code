# Sweetened Beverages and Atrial Fibrillation — MR Analysis Code

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22099675.svg)](https://doi.org/10.5281/zenodo.22099675)

## Current JAHA submission archive

The complete statistically reconciled and editor-refined archive for the current manuscript is
[`sweetened-beverages-af-mr-code-v6.2.0.zip`](sweetened-beverages-af-mr-code-v6.2.0.zip).
See [`CURRENT_ARCHIVE.md`](CURRENT_ARCHIVE.md) for its contents and
[`RELEASE_NOTES.md`](RELEASE_NOTES.md) for the v6.2.0 release summary.
The archive contains current analysis code, harmonized per-variant data,
submission files, figures, result tables and verification outputs.
Its SHA256 checksum is recorded in [`SHA256SUMS.txt`](SHA256SUMS.txt).

Analysis and manuscript-build code for:

> **Sweetened Beverage Consumption and Risk of Atrial Fibrillation: A Two-Sample and Multivariable Mendelian Randomization Study With Cross-Ancestry Replication**
> Manuscript v4.5.6 (formatted for the *European Journal of Preventive Cardiology*), 27 August 2026.

## Overview

Two-sample Mendelian randomization (MR) of genetically proxied intake of sugar-sweetened beverages (SSBs), artificially sweetened beverages (ASBs), natural juices, coffee, tea, and added sugar against atrial fibrillation (AF), with:

- univariable IVW / weighted-median / MR-Egger / MR-PRESSO / radial-IVW estimators across four AF outcome sources (primary: Nielsen 2018; replication: FinnGen R13, AFGen 2018 legacy, BBJ cross-ancestry);
- multivariable MR adjusting for adiposity (BMI), smoking and alcohol;
- Steiger directionality, reverse MR, alcohol positive lifestyle control, caffeine-pathway subgroup MR;
- Bayesian colocalization (coloc.abf) at CYP1A1–CYP1A2, AHR and FTO, including a prior-sensitivity (p12) scan (v4.5.1); the v4.5.8 extension repeats the analysis for tea intake (Neale field 1488, offline Z-derived effects; `R/run_v458_coloc_tea_offline.R`, results in `results/upgrade_coloc_tea_loci_Nielsen.csv`; Table S21);
- contamination-mixture (conmix) robust estimator (v4.5.1);
- genome-wide CAUSE analysis (causal vs correlated-pleiotropy model; v4.5.2);
- two-step (network) mediation MR through BMI, incl. a full-coverage Neale-21001 BMI sensitivity (Table S16; v4.5.3/v4.5.4);
- MRlap correction for sample overlap, winner's curse and weak instruments (Table S17; v4.5.3);
- atrioventricular-block negative outcome control (Table S18; v4.5.3);
- independent coffee-exposure GWAS replication (Neale field 1498) with cross-GWAS meta-analysis (Table S19; v4.5.4);
- early-onset AF sensitivity analysis (Choi et al., JAMA 2018; GWAS Catalog GCST010636, TOPMed freeze 4 WGS; score-test statistics converted to effect estimates, beta = Score/Var; Table S20; v4.5.6);
- cross-trait LD Score regression (LDSC) genetic correlations with same-trait validation controls;
- statistical power from realized IVW standard errors.

## Data sources (all public)

| Dataset | Source / accession |
|---|---|
| Beverage-intake GWAS | Zhong VW et al., Hum Mol Genet 2019 (manuscript ref 8) |
| AF primary outcome | Nielsen JB et al., Nat Genet 2018 (60,620 cases / 970,216 controls) |
| AF replication | FinnGen release R13 (67,783 cases / 241,269 controls) |
| AF legacy sensitivity | Roselli C et al., Nat Genet 2018 (AFGen) |
| AF cross-ancestry | Ishigaki K et al. (BBJ), Nat Genet 2020; Yuan S et al., Nat Commun 2025 (GWAS Catalog GCST90624413; per-variant statistics not public) |
| AF early-onset sensitivity | Choi SH et al., JAMA 2018 (GWAS Catalog GCST010636; TOPMed freeze 4 WGS; 2,781 cases / 4,959 controls, European ancestry) |
| Adiposity / smoking / alcohol covariates | Yengo L et al. 2018 (GIANT BMI); Liu M et al. 2019 (GSCAN) |
| LDSC reference | Bulik-Sullivan BK et al., Nat Genet 2015 (1000 Genomes European LD scores) |

Full GWAS summary-statistics files are **not redistributed** in this repository (size and licence); download from the sources above. Harmonized per-variant datasets underlying each table are in the manuscript's `Supplementary_Data_Files.zip`.

## Repository layout

```
R/                  R analysis scripts (chronological v4.0 -> v4.5.1)
python/             aggregation, LDSC munging, figure scripts (Python 3)
docx_build/         manuscript/supplement/cover-letter docx-js build scripts,
                    v4.5 and v4.5.1 transform scripts, and verify_v45.py
supplement_tables/  TSV tables rendered into the supplement (S1-S21, T2-T5)
```

## Reproduction pipeline

1. **Primary univariable MR** — `R/run_v4_nielsen.R` (TwoSampleMR; Nielsen 2018 primary), `R/run_v4_local_sens.R` (AFGen legacy sensitivity).
2. **Robustness** — `R/run_v4_reverse.R` (reverse MR), `R/run_v4_alcohol.R` (alcohol positive control), `R/run_v4_re.R` (random-effects / between-source heterogeneity), `R/run_v4_meta_compare.R`.
3. **Multivariable MR** — `R/run_v4_mvmr.R` (BMI / smoking / alcohol adjustment; MR-PRESSO).
4. **Replication upgrade** — `R/run_v41_finngen_r13.R` (FinnGen R5 → R13).
5. **Colocalization** — `R/run_v4_coloc.R` (CYP1A1/AHR/FTO vs AFGen + Nielsen), `R/run_v42_coloc_fto_r13.R` (FTO vs FinnGen R13), `R/run_v45_coloc_priorscan.R` (p12 prior scan; Nielsen region rebuilt locally via `python/extract_coloc_FTO_nielsen_v45.py`), `R/run_v458_coloc_tea_offline.R` (tea intake, fully offline from local Neale 1488 + Nielsen 2018 files).
6. **Caffeine-pathway subgroup** — `R/run_v43_caffeine_subgroup.R`; Figure S1 via `R/run_v43_figureS1.R`.
7. **conmix robust estimator** — `R/run_v45_conmix.R` (MendelianRandomization::mr_conmix).
7b. **CAUSE** — `R/run_v46_cause.R` (causal vs correlated-pleiotropy model on the same munged HM3 inputs used for LDSC). CAUSE (jean997/cause@master, v1.2.0.0335) is not on CRAN; obtain the source, apply the two compatibility patches in `cause/` (readr `write_tsv(file=)` in `gwas_format.R`; loo ≥ 2.5 `loo_compare()` data.frame API in `in_sample_elpd_loo.R`), then load with `devtools::load_all()`. See `cause/cause_summary_coffee_v46.txt` for the expected output.
8. **LDSC** — `python/munge_for_ldsc.py` then `R/run_v44_ldsc.R`; forest plot via `python/figureS2_ldsc_rg_v45.py`.
9. **Tables / figures** — `python/aggregate_supplement_v4.py` (supplement TSVs), `python/figure1_design_v4.py`, `python/forest_figure2_v4.py`, `python/forest_v4.py`, `python/graphical_abstract_v45.py`.
9b. **Early-onset AF sensitivity** — `python/eoaf_sensitivity.py` (instrument lookup in the GCST010636 score-test summary statistics by chromosome:position; effect estimates recovered as beta = Score/Var, SE = Var^-1/2; IVW / bootstrap weighted median / MR-Egger; results in `python/eoaf_sensitivity_results.csv`, SNP-level data in `eoaf_harmonised_snps.csv`).
10. **Manuscript build** — `docx_build/transform_to_v45.py` → `transform_to_v451.py` → `transform_to_v452.py` (edit docx-js sources with asserted anchors and Vancouver auto-renumbering), then build each `build_*_v45.js` with a docx-js toolchain, then `python verify_v45.py` (machine checks: word limits, citation order 1–37 in document flow, key numbers, table counts). All 37 references are verified against PubMed with `python/check_refs_pubmed.py` (E-utilities; DOI-aware for epub-ahead-of-print items); the v4.5.6 insertion of the AHA 2026 scientific statement as ref 7 used the one-shot renumbering script `python/renumber_refs_v456.py`, and the v4.5.7/v4.5.8 additions of eight references (Casiglia 2018, Chieng 2022, Krittanawong 2021, Woolf 2024, Larsson 2023, Liu 2016, Mattioli 2018, Joglar 2024; refs 5-7, 32-33, 34-36) were applied with asserted-anchor renumbering in the same style.

## Software requirements

- R ≥ 4.4 with `TwoSampleMR`, `MendelianRandomization` (conmix; requires `mixsqp`), `MRPRESSO`, `coloc`, `ggplot2`, `remotes`; `cause` (GitHub: jean997/cause) with the patches in `cause/` and an Rtools toolchain for its C++ code.
- Python 3 with `pandas`, `numpy`, `matplotlib`, `seaborn`, `python-docx`.
- LDSC (munge_sumstats / ldsc.py) for cross-trait rg, with 1000 Genomes European LD scores.
- Node.js + docx-js only for rebuilding the manuscript `.docx` files.

Known environment notes (documented in the revision record): CAUSE was added in v4.5.2 after installing an Rtools toolchain (see step 7b for the two source patches needed with current readr/loo versions). `mr.raps` failed to install from CRAN — radial IVW + conmix cover the same robustness questions. An OpenGWAS JWT is required only if re-fetching CYP1A1/AHR regional statistics via the API; the FTO prior scan uses local files.

## Suggested licence & archiving

- Code: MIT licence. Tables/figures: CC BY 4.0 (or CC0).
- To archive with a DOI: push this folder to GitHub, then link the repository to Zenodo (Settings → GitHub → flip the repo switch) and create a release; Zenodo mints a DOI automatically. Add the DOI to the manuscript's data-availability statement.

## Citation

If you use this code, cite the manuscript (details to be added upon publication) and the archived code:

Cao Z, Chen R. sweetened-beverages-af-mr-code: analysis code for "Sweetened Beverage Consumption and Risk of Atrial Fibrillation: A Two-Sample and Multivariable Mendelian Randomization Study With Cross-Ancestry Replication" [Computer software]. Zenodo. 2026. https://doi.org/10.5281/zenodo.22099675

## v5.1 update (NMCD submission, 2026-10)

- New analyses: instrument-strength metrics (S22), corrected MR-RAPS against FinnGen R13 (S23), Sanderson–Windmeijer conditional F (S24); scripts `R/run_v51_raps_strength.R`, `R/run_v51_condF_s1-s3.R`.
- MVMR rebuild verification: `results/mvmr_verification_v51.tsv` (published values reproduced to 8 decimals).
- Manuscript compressed to NMCD format (<=4000 countable words; three-part abstract <=250 words; title 108 chars) via `python/patch_v51_nmcd_compress*.py` applied to `docx_build/build_manuscript_v51.js`; machine checks in `python/verify_v51.py` (all PASS).
- Current manuscript title: "Sweetened Beverage Consumption and Atrial Fibrillation: Two-Sample and Multivariable Mendelian Randomization".

- `python/make_jaha_build.py`, `python/verify_jaha.py`, `docx_build/build_*_v51_JAHA.js` — JAHA edition (v5.1): JAHA abstract labels, Nonstandard Abbreviations and Acronyms + Clinical Perspective sections, Sources of Funding/Disclosures headings; verification: abstract 223 words, body 5872 words, all KEY figures retained (2026-10-13).
- JAHA edition update (2026-10-13): defensive paragraph on behavioural-instrument pleiotropy added to Strengths and limitations (estimates framed as bounds on total beverage-component-pathway effects; debate acknowledged as unsettled), with new reference 43 (Hemani G, Bowden J, Davey Smith G. Hum Mol Genet. 2018;27(R2):R195-R208); citations now cover 1..43.

- v5.2 biomarker-MR arm (2026-10-13): plasma caffeine/paraxanthine/theobromine (Chen 2023 Nat Genet; GCST90200436/90199654/90199644) vs Nielsen 2018 + FinnGen R13 — null for caffeine (meta OR 0.993, 0.922-1.069) and paraxanthine (0.976, 0.930-1.023); nominal theobromine inverse (0.843, P=0.029) does not survive Bonferroni. Scripts: python/fast_dl.py, python/extract_biomarker_outcomes*.py, R/run_v52_biomarker_*.R

- v5.2 integrated (2026-10-13): biomarker-MR arm added to manuscript (Methods data sources, Results subsection, Discussion convergence sentence, limitation #6, ref 44 Chen et al. 2023 Nat Genet 55(1):44-53), supplement Table S25, cover letter; compensating trims keep body at exactly 6000 words, abstract 236; verify_jaha.py: 1..44 citations, 44 refs, 112 KEY strings, S25 check. Patch: python/patch_v52_biomarker.py.

- v5.2.1 (2026-10-13, pre-submission review fixes): Larsson 2023 (ref 33) AF-null disclosed and biomarker arm delineated in Discussion + cover letter; minimum detectable ORs (1.07-1.25) reported; GTF2I-excluded theobromine = cis CYP2A6 estimates noted in Table S25; ref 45 added (Liu et al., JAHA 2025;14(9):e035978, SSB-CVD burden) for East Asian motivation; steady-state estimand limitation added. Body 5999 words; citations 1..45; 117 KEY strings. Patch: python/patch_v521_fixes.py.

- v5.2.2 (2026-10-16, narrative hardening per external top-journal strategy review): DECAF description corrected to 39% fewer AF recurrences (JAMA 2026;335(4):317-325; HR 0.61) in Introduction and Discussion; three-design convergence sentence added to the coffee Discussion paragraph (genetic susceptibility nulls [8,33,44] x acute randomized triggering null [30] x randomized recurrence HR 0.61 [9]); ref 46 added (Dewland TA, van Dam RM, Marcus GM. Coffee and cardiovascular disease. Eur Heart J. 2025;46(36):3546-3554); abstract convergence sentence (246 words); cover letter quantified-workload sentence. Compensating trims net -3 words: body 5996; citations 1..46; 46 refs; 121 KEY strings. Patch: python/patch_v522_narrative.py.

- v5.2.3 (2026-10-18, pre-submission final review): US spelling unified for JAHA (AHA journal convention) — 34 manuscript + 3 cover-letter + 7 supplement British spellings replaced 1:1 (behaviour/analysed/modelled/towards/centred/harbouring/aetiology/ischaemic/ageing/millilitre/colour); word counts and all 121 KEY strings unchanged. Patch: python/patch_v523_spelling.py.

- v5.2.4 (2026-10-18, external 3-reviewer report adoption): abstract "not robust" list parallelized + weak-conditional-instrument qualifier on the BMI attenuation item (R1-M1/R3-1, funded by abstract trims, 249 words); Table S16 note flags mediated proportion as not estimable (R1-M2); HR 3.51 flagged as interaction estimate (R2-m1); "no exception" referent, entails->involves, estimand active-voice, "its weight remains" clarified, objective (iv) recast, Table 2 footnote phrasing (R3-2..7). Declined with reasons: R2-m2, R1-M3/M4, R3-8 (stale; no "likewise" in highlights), full estimand gloss. Body 5997; all checks pass. Patch: python/patch_v524_review.py.
