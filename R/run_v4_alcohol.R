#!/usr/bin/env Rscript
# v4 upgrade step 3: positive lifestyle control — alcohol intake frequency -> AF
# Exposure: ukb-b-5779 (Alcohol intake frequency, UKB, EUR, N=462,346)
# Outcomes: Nielsen 2018 (new primary EUR), AFGen 2018 (old primary), FinnGen R5, BBJ (EAS)
suppressMessages({library(data.table); library(dplyr); library(ieugwasr); library(TwoSampleMR)})
if (Sys.getenv("OPENGWAS_JWT") == "") stop("OPENGWAS_JWT not set")

root   <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
outdir <- file.path(root, "06_升级分析_v4/results")
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

expo_id    <- "ukb-b-5779"
expo_label <- "Alcohol intake frequency"
args <- commandArgs(trailingOnly = TRUE)
if (length(args) >= 2) { expo_id <- args[1]; expo_label <- args[2] }

cat("Extracting instruments for", expo_label, "(", expo_id, ")\n")
exp_dat <- extract_instruments(expo_id, p1 = 5e-8, clump = TRUE, r2 = 0.001, kb = 10000)
if (is.null(exp_dat) || nrow(exp_dat) < 3) {
  cat("5e-8 yielded <3; relaxing to 5e-6\n")
  exp_dat <- extract_instruments(expo_id, p1 = 5e-6, clump = TRUE, r2 = 0.001, kb = 10000)
}
stopifnot(!is.null(exp_dat), nrow(exp_dat) >= 3)
exp_dat$exposure <- expo_label
cat("instruments:", nrow(exp_dat), "\n")

outcomes <- list(
  c("ebi-a-GCST006414", "AF Nielsen 2018 EUR N1.03M", "ebi_a_GCST006414"),
  c("ebi-a-GCST006061", "AF AFGen 2018 EUR",         "ebi_a_GCST006061"),
  c("finn-b-I9_AF",     "AF FinnGen R5 EUR",         "finn_b_I9_AF"),
  c("bbj-a-71",         "AF BBJ EAS",                "bbj_a_71")
)

for (oc in outcomes) {
  oid <- oc[1]; olabel <- oc[2]; otag <- oc[3]
  cat("\n=== ", expo_label, " -> ", olabel, "\n")
  out_dat <- tryCatch(extract_outcome_data(exp_dat$SNP, oid),
                      error = function(e) { cat("  outcome fail:", conditionMessage(e), "\n"); NULL })
  if (is.null(out_dat) || nrow(out_dat) == 0) { cat("  SKIP: no outcome data\n"); next }
  out_dat$outcome <- olabel
  dat <- harmonise_data(exp_dat, out_dat, action = 2)
  dat <- dat[dat$mr_keep, ]
  cat("  SNPs after harmonisation:", nrow(dat), "\n")
  if (nrow(dat) < 3) { cat("  SKIP: <3\n"); next }
  dat$F_stat <- (dat$beta.exposure / dat$se.exposure)^2
  cat("  min F:", round(min(dat$F_stat), 1), "\n")

  res   <- mr(dat, method_list = c("mr_ivw", "mr_egger_regression", "mr_weighted_median", "mr_weighted_mode"))
  het   <- mr_heterogeneity(dat)
  pleio <- tryCatch(mr_pleiotropy_test(dat), error = function(e) NULL)

  tag <- gsub("[^A-Za-z0-9]+", "_", expo_label)
  fwrite(as.data.table(dat), file.path(outdir, paste0("dat_", tag, "_", otag, ".csv")))
  fwrite(res,  file.path(outdir, paste0("mr_", tag, "_", otag, ".csv")))
  fwrite(het,  file.path(outdir, paste0("het_", tag, "_", otag, ".csv")))
  if (!is.null(pleio)) fwrite(pleio, file.path(outdir, paste0("pleio_", tag, "_", otag, ".csv")))

  ivw <- res[res$method == "Inverse variance weighted", ]
  cat(sprintf("  IVW: OR=%.3f (%.3f-%.3f), P=%.4g, nsnp=%d\n",
              exp(ivw$b), exp(ivw$b - 1.96 * ivw$se), exp(ivw$b + 1.96 * ivw$se), ivw$pval, ivw$nsnp))
  Sys.sleep(2)
}
cat("\n=== DONE ===\n")
