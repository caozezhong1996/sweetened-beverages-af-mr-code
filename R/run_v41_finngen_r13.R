#!/usr/bin/env Rscript
# v4.1: beverage + alcohol instruments vs FinnGen R13 I9_AF (67,783 cases / 241,269 controls)
# fully local: outcome summary stats already filtered to instrument rsIDs
suppressMessages({library(data.table); library(dplyr); library(TwoSampleMR)})
root   <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
outdir <- file.path(root, "06_升级分析_v4/results")

fg <- fread(file.path(outdir, "finngen_R13_I9_AF_instruments.tsv"))
cat("R13 rows:", nrow(fg), "\n")

# long -> one row per rsid (a variant line can carry multiple rsids; expand then match)
fg_long <- fg[, .(rsid = unlist(strsplit(rsids, ",", fixed = TRUE))), by = .(beta, sebeta, af_alt, pval, ref, alt)]
fg_long <- fg_long[!duplicated(rsid)]

expo_specs <- list(
  c("Artificial_sweetener_added_to_tea", "dat_Artificial_sweetener_added_to_tea_ebi_a_GCST006414.csv"),
  c("Coffee_intake",                   "dat_Coffee_intake_ebi_a_GCST006414.csv"),
  c("Fizzy_drink_intake_SSB",          "dat_Fizzy_drink_intake_SSB_ebi_a_GCST006414.csv"),
  c("Low_calorie_drink_intake_ASB",    "dat_Low_calorie_drink_intake_ASB_ebi_a_GCST006414.csv"),
  c("Sugar_added_to_coffee",           "dat_Sugar_added_to_coffee_ebi_a_GCST006414.csv"),
  c("Sugar_added_to_tea",              "dat_Sugar_added_to_tea_ebi_a_GCST006414.csv"),
  c("Tea_intake",                      "dat_Tea_intake_ebi_a_GCST006414.csv"),
  c("Alcohol_intake_frequency",        "dat_Alcohol_intake_frequency_ebi_a_GCST006414.csv"),
  c("Alcoholic_drinks_per_week_GSCAN", "dat_Alcoholic_drinks_per_week_GSCAN_ebi_a_GCST006414.csv")
)

run_one <- function(tag, datfile) {
  d <- fread(file.path(outdir, datfile))
  exp_dat <- data.frame(
    SNP = d$SNP, beta.exposure = d$beta.exposure, se.exposure = d$se.exposure,
    effect_allele.exposure = d$effect_allele.exposure, other_allele.exposure = d$other_allele.exposure,
    eaf.exposure = d$eaf.exposure, pval.exposure = d$pval.exposure,
    samplesize.exposure = d$samplesize.exposure, exposure = d$exposure, id.exposure = d$id.exposure,
    stringsAsFactors = FALSE)
  sub <- fg_long[rsid %in% exp_dat$SNP]
  cat(sprintf("\n=== %s: %d instruments, %d matched in R13\n", tag, nrow(exp_dat), nrow(sub)))
  out_dat <- data.frame(
    SNP = sub$rsid, beta.outcome = sub$beta, se.outcome = sub$sebeta,
    effect_allele.outcome = sub$alt, other_allele.outcome = sub$ref,
    eaf.outcome = sub$af_alt, pval.outcome = sub$pval,
    samplesize.outcome = 309052, outcome = "Atrial fibrillation (FinnGen R13)",
    id.outcome = "finngen_R13_I9_AF", stringsAsFactors = FALSE)
  dat <- harmonise_data(exp_dat, out_dat, action = 2)
  dat <- dat[dat$mr_keep, ]
  cat("  SNPs after harmonisation:", nrow(dat), "\n")
  if (nrow(dat) < 3) { cat("  SKIP\n"); return(NULL) }
  res   <- mr(dat, method_list = c("mr_ivw", "mr_egger_regression", "mr_weighted_median", "mr_weighted_mode"))
  het   <- mr_heterogeneity(dat)
  pleio <- tryCatch(mr_pleiotropy_test(dat), error = function(e) NULL)
  rad   <- tryCatch(mr(dat, method_list = "mr_ivw_radial"), error = function(e) NULL)
  fwrite(as.data.table(dat), file.path(outdir, paste0("dat_", tag, "_finngen_R13.csv")))
  fwrite(res,  file.path(outdir, paste0("mr_", tag, "_finngen_R13.csv")))
  fwrite(het,  file.path(outdir, paste0("het_", tag, "_finngen_R13.csv")))
  if (!is.null(pleio)) fwrite(pleio, file.path(outdir, paste0("pleio_", tag, "_finngen_R13.csv")))
  if (!is.null(rad))   fwrite(as.data.table(rad), file.path(outdir, paste0("radial_", tag, "_finngen_R13.csv")))
  ivw <- res[res$method == "Inverse variance weighted", ]
  cat(sprintf("  IVW: OR=%.3f (%.3f-%.3f), P=%.4g, nsnp=%d\n",
              exp(ivw$b), exp(ivw$b - 1.96 * ivw$se), exp(ivw$b + 1.96 * ivw$se), ivw$pval, ivw$nsnp))
  invisible(list(res = res, ivw = ivw))
}

ivw_all <- list()
for (sp in expo_specs) {
  r <- tryCatch(run_one(sp[1], sp[2]), error = function(e) { cat("ERROR", sp[1], ":", conditionMessage(e), "\n"); NULL })
  if (!is.null(r)) ivw_all[[sp[1]]] <- r$ivw
}

# ---- EUR meta v4.1: Nielsen 2018 + FinnGen R13 ----
cat("\n=== EUR meta v4.1 (Nielsen 2018 + FinnGen R13, fixed effect) ===\n")
meta_rows <- list()
for (sp in expo_specs) {
  tag <- sp[1]
  f_n <- file.path(outdir, paste0("mr_", tag, "_ebi_a_GCST006414.csv"))
  f_f <- file.path(outdir, paste0("mr_", tag, "_finngen_R13.csv"))
  if (!file.exists(f_n) || !file.exists(f_f)) next
  rn <- fread(f_n)[method == "Inverse variance weighted"]
  rf <- fread(f_f)[method == "Inverse variance weighted"]
  w1 <- 1/rn$se^2; w2 <- 1/rf$se^2
  mb <- (rn$b*w1 + rf$b*w2)/(w1+w2); mse <- sqrt(1/(w1+w2))
  mp <- 2*pnorm(-abs(mb/mse))
  meta_rows[[tag]] <- data.frame(exposure = tag, nsnp_nielsen = rn$nsnp, nsnp_r13 = rf$nsnp,
    nielsen_orci = sprintf("%.3f (%.3f-%.3f), P=%.4g", exp(rn$b), exp(rn$b-1.96*rn$se), exp(rn$b+1.96*rn$se), rn$pval),
    r13_orci     = sprintf("%.3f (%.3f-%.3f), P=%.4g", exp(rf$b), exp(rf$b-1.96*rf$se), exp(rf$b+1.96*rf$se), rf$pval),
    meta_orci    = sprintf("%.3f (%.3f-%.3f)", exp(mb), exp(mb-1.96*mse), exp(mb+1.96*mse)),
    meta_P = signif(mp, 3), meta_se = mse)
  cat(sprintf("%-38s meta OR %.3f (%.3f-%.3f) P=%.4g\n", tag, exp(mb), exp(mb-1.96*mse), exp(mb+1.96*mse), mp))
}
fwrite(rbindlist(meta_rows), file.path(outdir, "META_v41_Nielsen_FinnGenR13.csv"))

# ---- MR-PRESSO for coffee vs R13 if nominal ----
ivw_c <- ivw_all[["Coffee_intake"]]
if (!is.null(ivw_c) && ivw_c$pval < 0.10) {
  suppressMessages(library(MRPRESSO))
  dat <- as.data.frame(fread(file.path(outdir, "dat_Coffee_intake_finngen_R13.csv")))
  pr <- tryCatch(mr_presso(BetaOutcome = "beta.outcome", BetaExposure = "beta.exposure",
                           SdOutcome = "se.outcome", SdExposure = "se.exposure",
                           OUTLIERtest = TRUE, DISTORTIONtest = TRUE, data = dat,
                           NbDistribution = 3000, SignifThreshold = 0.05),
                 error = function(e) { cat("presso fail:", conditionMessage(e), "\n"); NULL })
  if (!is.null(pr)) {
    print(pr$`Main MR results`)
    cat("Coffee vs R13 — Global P:", pr$`MR-PRESSO results`$`Global Test`$Pvalue, "\n")
    capture.output(print(pr), file = file.path(outdir, "presso_Coffee_intake_finngen_R13.txt"))
  }
}
cat("\nDONE\n")
