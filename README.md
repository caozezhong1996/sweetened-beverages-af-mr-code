# Sweetened Beverages and Atrial Fibrillation — MR Analysis Code

Analysis and manuscript-build code for:

> **Sweetened Beverage Consumption and Risk of Atrial Fibrillation: A Two-Sample and Multivariable Mendelian Randomization Study With Cross-Ancestry Replication**
> Manuscript v4.5.6 (formatted for the *European Journal of Preventive Cardiology*), 25 August 2026.

## Overview

Two-sample Mendelian randomization (MR) of genetically proxied intake of sugar-sweetened beverages (SSBs), artificially sweetened beverages (ASBs), natural juices, coffee, tea, and added sugar against atrial fibrillation (AF), with:

- univariable IVW / weighted-median / MR-Egger / MR-PRESSO / radial-IVW estimators across four AF outcome sources (primary: Nielsen 2018; replication: FinnGen R13, AFGen 2018 legacy, BBJ cross-ancestry);
- multivariable MR adjusting for adiposity (BMI), smoking and alcohol;
- Steiger directionality, reverse MR, alcohol positive lifestyle control, caffeine-pathway subgroup MR;
- Bayesian colocalization (coloc.abf) at CYP1A1–CYP1A2, AHR and FTO, including a prior-sensitivity (p12) scan (v4.5.1);
- contamination-mixture (conmix) robust estimator (v4.5.1);
- genome-wide CAUSE analysis (causal vs correlated-pleiotropy model; v4.5.2);
- two-step (network) mediation MR through BMI, incl. a full-coverage Neale-21001 BMI sensitivity (Table S16; v4.5.3/v4.5.4);
- MRlap correction for sample overlap, winner's curse and weak instruments (Table S17; v4.5.3);
- atrioventricular-block negative outcome control (Table S18; v4.5.3);
- independent coffee-exposure GWAS replication (Neale field 1498) with cross-GWAS meta-analysis (Table S19; v4.5.4);
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
| Adiposity / smoking / alcohol covariates | Yengo L et al. 2018 (GIANT BMI); Liu M et al. 2019 (GSCAN) |
| LDSC reference | Bulik-Sullivan BK et al., Nat Genet 2015 (1000 Genomes European LD scores) |

Full GWAS summary-statistics files are **not redistributed** in this repository (size and licence); download from the sources above. Harmonized per-variant datasets underlying each table are in the manuscript's `Supplementary_Data_Files.zip`.

## Repository layout

```
R/                  R analysis scripts (chronological v4.0 -> v4.5.1)
python/             aggregation, LDSC munging, figure scripts (Python 3)
docx_build/         manuscript/supplement/cover-letter docx-js build scripts,
                    v4.5 and v4.5.1 transform scripts, and verify_v45.py
supplement_tables/  TSV tables rendered into the supplement (S1-S14, T2-T5)
```

## Reproduction pipeline

1. **Primary univariable MR** — `R/run_v4_nielsen.R` (TwoSampleMR; Nielsen 2018 primary), `R/run_v4_local_sens.R` (AFGen legacy sensitivity).
2. **Robustness** — `R/run_v4_reverse.R` (reverse MR), `R/run_v4_alcohol.R` (alcohol positive control), `R/run_v4_re.R` (random-effects / between-source heterogeneity), `R/run_v4_meta_compare.R`.
3. **Multivariable MR** — `R/run_v4_mvmr.R` (BMI / smoking / alcohol adjustment; MR-PRESSO).
4. **Replication upgrade** — `R/run_v41_finngen_r13.R` (FinnGen R5 → R13).
5. **Colocalization** — `R/run_v4_coloc.R` (CYP1A1/AHR/FTO vs AFGen + Nielsen), `R/run_v42_coloc_fto_r13.R` (FTO vs FinnGen R13), `R/run_v45_coloc_priorscan.R` (p12 prior scan; Nielsen region rebuilt locally via `python/extract_coloc_FTO_nielsen_v45.py`).
6. **Caffeine-pathway subgroup** — `R/run_v43_caffeine_subgroup.R`; Figure S1 via `R/run_v43_figureS1.R`.
7. **conmix robust estimator** — `R/run_v45_conmix.R` (MendelianRandomization::mr_conmix).
7b. **CAUSE** — `R/run_v46_cause.R` (causal vs correlated-pleiotropy model on the same munged HM3 inputs used for LDSC). CAUSE (jean997/cause@master, v1.2.0.0335) is not on CRAN; obtain the source, apply the two compatibility patches in `cause/` (readr `write_tsv(file=)` in `gwas_format.R`; loo ≥ 2.5 `loo_compare()` data.frame API in `in_sample_elpd_loo.R`), then load with `devtools::load_all()`. See `cause/cause_summary_coffee_v46.txt` for the expected output.
8. **LDSC** — `python/munge_for_ldsc.py` then `R/run_v44_ldsc.R`; forest plot via `python/figureS2_ldsc_rg_v45.py`.
9. **Tables / figures** — `python/aggregate_supplement_v4.py` (supplement TSVs), `python/figure1_design_v4.py`, `python/forest_figure2_v4.py`, `python/forest_v4.py`, `python/graphical_abstract_v45.py`.
10. **Manuscript build** — `docx_build/transform_to_v45.py` → `transform_to_v451.py` → `transform_to_v452.py` (edit docx-js sources with asserted anchors and Vancouver auto-renumbering), then build each `build_*_v45.js` with a docx-js toolchain, then `python verify_v45.py` (machine checks: word limits, citation order 1–28 in document flow, key numbers, table counts). All 28 references are verified against PubMed with `python/check_refs_pubmed.py` (E-utilities; DOI-aware for epub-ahead-of-print items); the v4.5.6 insertion of the AHA 2026 scientific statement as ref 7 used the one-shot renumbering script `python/renumber_refs_v456.py`.

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

If you use this code, cite the manuscript (details to be added upon publication).
