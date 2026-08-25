#!/usr/bin/env Rscript
# v4 upgrade step 2: re-run 7 beverage exposures against Nielsen 2018 AF GWAS
# (ebi-a-GCST006414, N=1,030,836; 60,620 cases) reusing v3.1 instrument SNP lists
# saved from the AFGen (GCST006061) harmonised data.
suppressMessages({library(data.table); library(dplyr); library(ieugwasr); library(TwoSampleMR)})
if (Sys.getenv("OPENGWAS_JWT") == "") stop("OPENGWAS_JWT not set")

root    <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
olddir  <- file.path(root, "03_结果数据_mr_results")
outdir  <- file.path(root, "06_升级分析_v4/results")
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

new_outcome <- "ebi-a-GCST006414"   # Nielsen 2018, EUR, N=1,030,836

tags <- c("Artificial_sweetener_added_to_tea","Coffee_intake","Fizzy_drink_intake_SSB",
          "Low_calorie_drink_intake_ASB","Sugar_added_to_coffee","Sugar_added_to_tea","Tea_intake")
args <- commandArgs(trailingOnly = TRUE)
if (length(args) > 0) tags <- intersect(tags, args)

run_one <- function(tag) {
  f <- file.path(olddir, paste0("dat_", tag, "_ebi_a_GCST006061.csv"))
  if (!file.exists(f)) { cat("missing", f, "\n"); return(NULL) }
  d <- fread(f)
  cat("\n=== ", tag, ": ", nrow(d), " instrument SNPs (reused from v3.1)\n")
  exp_dat <- data.frame(
    SNP = d$SNP,
    beta.exposure = d$beta.exposure,
    se.exposure = d$se.exposure,
    effect_allele.exposure = d$effect_allele.exposure,
    other_allele.exposure = d$other_allele.exposure,
    eaf.exposure = d$eaf.exposure,
    pval.exposure = d$pval.exposure,
    samplesize.exposure = d$samplesize.exposure,
    exposure = d$exposure,
    id.exposure = d$id.exposure,
    stringsAsFactors = FALSE)

  out_dat <- tryCatch(
    extract_outcome_data(exp_dat$SNP, new_outcome),
    error = function(e) { cat("  outcome fail:", conditionMessage(e), "\n"); NULL })
  if (is.null(out_dat) || nrow(out_dat) == 0) { cat("  SKIP: no outcome data\n"); return(NULL) }
  out_dat$outcome <- "Atrial fibrillation (Nielsen 2018, EUR, N=1.03M)"

  dat <- harmonise_data(exp_dat, out_dat, action = 2)
  dat <- dat[dat$mr_keep, ]
  cat("  SNPs after harmonisation:", nrow(dat), "\n")
  if (nrow(dat) < 3) { cat("  SKIP: <3 after harmonisation\n"); return(NULL) }
  dat$F_stat <- (dat$beta.exposure / dat$se.exposure)^2
  cat("  min F:", round(min(dat$F_stat), 1), "\n")

  res   <- mr(dat, method_list = c("mr_ivw", "mr_egger_regression", "mr_weighted_median", "mr_weighted_mode"))
  het   <- mr_heterogeneity(dat)
  pleio <- tryCatch(mr_pleiotropy_test(dat), error = function(e) NULL)

  fwrite(as.data.table(dat), file.path(outdir, paste0("dat_", tag, "_ebi_a_GCST006414.csv")))
  fwrite(res,  file.path(outdir, paste0("mr_", tag, "_ebi_a_GCST006414.csv")))
  fwrite(het,  file.path(outdir, paste0("het_", tag, "_ebi_a_GCST006414.csv")))
  if (!is.null(pleio)) fwrite(pleio, file.path(outdir, paste0("pleio_", tag, "_ebi_a_GCST006414.csv")))

  ivw <- res[res$method == "Inverse variance weighted", ]
  cat(sprintf("  IVW: OR=%.3f (%.3f-%.3f), P=%.4g, nsnp=%d\n",
              exp(ivw$b), exp(ivw$b - 1.96 * ivw$se), exp(ivw$b + 1.96 * ivw$se), ivw$pval, ivw$nsnp))
  invisible(res)
}

all_res <- list()
for (tg in tags) {
  r <- tryCatch(run_one(tg), error = function(e) { cat("ERROR:", conditionMessage(e), "\n"); NULL })
  if (!is.null(r)) all_res[[tg]] <- r
  Sys.sleep(2)
}
cat("\n=== DONE ===\n")
