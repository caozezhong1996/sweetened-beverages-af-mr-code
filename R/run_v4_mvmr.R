#!/usr/bin/env Rscript
# v4: MVMR coffee + sugar-in-tea + BMI -> AF (Nielsen 2018, ebi-a-GCST006414)
suppressMessages({library(data.table); library(ieugwasr); library(TwoSampleMR)})
if (Sys.getenv("OPENGWAS_JWT") == "") stop("OPENGWAS_JWT not set")
root   <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
outdir <- file.path(root, "06_升级分析_v4/results")

expo_ids <- c("ukb-b-5237", "ukb-b-8442", "ieu-b-40")  # coffee, sugar-in-tea, BMI
labels <- c(`ukb-b-5237` = "Coffee intake", `ukb-b-8442` = "Sugar added to tea", `ieu-b-40` = "BMI")

cat("Extracting exposure instruments (joint) ...\n")
exposure_dat <- mv_extract_exposures(expo_ids, pval_threshold = 5e-8, clump_r2 = 0.001, clump_kb = 10000)
cat("joint instruments:", nrow(exposure_dat), "\n")
print(table(exposure_dat$exposure))

cat("Extracting outcome data (Nielsen 2018) ...\n")
outcome_dat <- extract_outcome_data(exposure_dat$SNP, "ebi-a-GCST006414")
outcome_dat$outcome <- "Atrial fibrillation (Nielsen 2018)"

mvdat <- mv_harmonise_data(exposure_dat, outcome_dat)
res <- mv_multiple(mvdat)
res$result$exposure_label <- labels[res$result$exposure]
print(res$result[, c("exposure_label", "nsnp", "b", "se", "pval")])
fwrite(res$result, file.path(outdir, "mvmr_coffee_sugartea_bmi_Nielsen.csv"))
cat("MVMR DONE\n")
