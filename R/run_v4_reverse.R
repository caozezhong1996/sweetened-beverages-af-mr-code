#!/usr/bin/env Rscript
# v4: reverse MR — AF liability (Nielsen 2018 instruments) -> beverage intake
suppressMessages({library(data.table); library(ieugwasr); library(TwoSampleMR)})
if (Sys.getenv("OPENGWAS_JWT") == "") stop("OPENGWAS_JWT not set")
root   <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
outdir <- file.path(root, "06_升级分析_v4/results")

cat("Extracting AF instruments (ebi-a-GCST006414, Nielsen 2018) ...\n")
af_exp <- extract_instruments("ebi-a-GCST006414", p1 = 5e-8, clump = TRUE, r2 = 0.001, kb = 10000)
cat("AF instruments:", nrow(af_exp), "\n")
af_exp$exposure <- "Atrial fibrillation (Nielsen 2018)"

beverages <- list(
  c("ukb-b-8442",  "Sugar added to tea"),
  c("ukb-b-243",   "Sugar added to coffee"),
  c("ukb-b-2832",  "Fizzy drink intake SSB"),
  c("ukb-b-19703", "Low-calorie drink intake ASB"),
  c("ukb-b-5867",  "Artificial sweetener added to tea"),
  c("ukb-b-5237",  "Coffee intake"),
  c("ukb-b-6066",  "Tea intake")
)
rows <- list()
for (b in beverages) {
  oid <- b[1]; olab <- b[2]
  cat("\n--- AF(Nielsen) ->", olab, "\n")
  out <- tryCatch(extract_outcome_data(af_exp$SNP, oid), error = function(e) { cat("outcome err:", conditionMessage(e), "\n"); NULL })
  if (is.null(out)) next
  out$outcome <- olab
  dat <- harmonise_data(af_exp, out, action = 2)
  dat <- dat[dat$mr_keep, ]
  cat("SNPs after harmonisation:", nrow(dat), "\n")
  if (nrow(dat) < 3) { cat("skip (<3)\n"); next }
  res <- mr(dat, method_list = c("mr_ivw", "mr_weighted_median", "mr_egger_regression"))
  df <- as.data.frame(res); df$outcome_label <- olab
  rows[[length(rows)+1]] <- df
  ivw <- df[df$method == "Inverse variance weighted", ]
  cat(sprintf("IVW: b=%.4f se=%.4f P=%.4f (nsnp=%d)\n", ivw$b, ivw$se, ivw$pval, ivw$nsnp))
  fwrite(as.data.table(dat), file.path(outdir, paste0("revdat_AFNielsen_", gsub("[^A-Za-z0-9]+", "_", olab), ".csv")))
  Sys.sleep(2)
}
if (length(rows)) fwrite(rbindlist(rows, fill = TRUE), file.path(outdir, "upgrade_reverse_mr_nielsen.csv"))
cat("REVERSE MR DONE\n")
