#!/usr/bin/env Rscript
# v4.5.1: contamination-mixture estimator for the nominal coffee -> AF signal
# (34 instruments), Nielsen 2018 and FinnGen R13 outcomes.
# Complements IVW / weighted-median / MR-Egger / MR-PRESSO / radial IVW.
suppressMessages({library(data.table); library(MendelianRandomization)})
root   <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
outdir <- file.path(root, "06_升级分析_v4/results")

run_one <- function(f, label) {
  d <- fread(f)
  d <- d[d$mr_keep == TRUE & !is.na(d$beta.exposure) & !is.na(d$beta.outcome), ]
  cat(label, "instruments:", nrow(d), "\n")
  inp <- mr_input(bx = d$beta.exposure, bxse = d$se.exposure,
                  by = d$beta.outcome, byse = d$se.outcome)
  cx <- mr_conmix(inp, CIMin = -1, CIMax = 1, CIStep = 0.001)
  data.frame(analysis = label, n_snp = nrow(d),
             conmix_beta = cx@Estimate, conmix_ci_lo = cx@CILower,
             conmix_ci_hi = cx@CIUpper, conmix_p = cx@Pvalue)
}

rows <- list(
  run_one(file.path(outdir, "dat_Coffee_intake_ebi_a_GCST006414.csv"), "conmix: coffee -> AF (Nielsen 2018)"),
  run_one(file.path(outdir, "dat_Coffee_intake_finngen_R13.csv"),      "conmix: coffee -> AF (FinnGen R13)")
)
out <- rbindlist(rows)
fwrite(out, file.path(outdir, "conmix_coffee_v45.tsv"), sep = "\t")
print(out, digits = 4)
cat("CONMIX DONE\n")
