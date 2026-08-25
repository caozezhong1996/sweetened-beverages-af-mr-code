#!/usr/bin/env Rscript
# v4 step 6: local sensitivity analyses on saved Nielsen 2018 harmonised data
# (Steiger directionality, radial IVW, MR-PRESSO for the nominal coffee signal)
suppressMessages({library(data.table); library(TwoSampleMR)})
root   <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
outdir <- file.path(root, "06_升级分析_v4/results")

tags <- c("Artificial_sweetener_added_to_tea","Coffee_intake","Fizzy_drink_intake_SSB",
          "Low_calorie_drink_intake_ASB","Sugar_added_to_coffee","Sugar_added_to_tea","Tea_intake")

# ---- radial IVW ----
rows <- list()
for (tg in tags) {
  f <- file.path(outdir, paste0("dat_", tg, "_ebi_a_GCST006414.csv"))
  dat <- as.data.frame(fread(f))
  r <- tryCatch(mr(dat, method_list = "mr_ivw_radial"), error = function(e) { cat(tg, "radial ERR:", conditionMessage(e), "\n"); NULL })
  if (!is.null(r)) {
    df <- as.data.frame(r); df$exposure <- tg
    rows[[tg]] <- df
    cat(sprintf("%-38s radial IVW: b=%.4f se=%.4f P=%.4g (nsnp=%d)\n", tg, df$b[1], df$se[1], df$pval[1], df$nsnp[1]))
  }
}
if (length(rows)) fwrite(rbindlist(rows, fill = TRUE), file.path(outdir, "upgrade_radial_ivw_nielsen.csv"))

# ---- Steiger directionality ----
srows <- list()
for (tg in tags) {
  f <- file.path(outdir, paste0("dat_", tg, "_ebi_a_GCST006414.csv"))
  dat <- as.data.frame(fread(f))
  st <- tryCatch(directionality_test(dat), error = function(e) { cat(tg, "steiger ERR:", conditionMessage(e), "\n"); NULL })
  if (!is.null(st)) {
    df <- as.data.frame(st); df$exposure <- tg
    srows[[tg]] <- df
    cat(sprintf("%-38s Steiger: correct_dir=%s P=%.3g (R2exp=%.4g R2out=%.4g)\n",
                tg, df$correct_causal_direction, df$steiger_pval, df$rsq.exposure, df$rsq.outcome))
  }
}
if (length(srows)) fwrite(rbindlist(srows, fill = TRUE), file.path(outdir, "upgrade_steiger_nielsen.csv"))

# ---- MR-PRESSO for coffee (sole nominal Nielsen signal) ----
suppressMessages(library(MRPRESSO))
dat <- as.data.frame(fread(file.path(outdir, "dat_Coffee_intake_ebi_a_GCST006414.csv")))
pr <- tryCatch(
  mr_presso(BetaOutcome = "beta.outcome", BetaExposure = "beta.exposure",
            SdOutcome = "se.outcome", SdExposure = "se.exposure",
            OUTLIERtest = TRUE, DISTORTIONtest = TRUE, data = dat,
            NbDistribution = 3000, SignifThreshold = 0.05),
  error = function(e) { cat("presso fail:", conditionMessage(e), "\n"); NULL })
if (!is.null(pr)) {
  print(pr$`Main MR results`)
  cat("Coffee vs Nielsen — Global test P:", pr$`MR-PRESSO results`$`Global Test`$Pvalue, "\n")
  ot <- pr$`MR-PRESSO results`$`Outlier Test`
  if (!is.null(ot)) cat("outliers (P<0.05):", sum(!is.na(ot$Pvalue) & ot$Pvalue < 0.05), "\n")
  capture.output(print(pr), file = file.path(outdir, "presso_Coffee_intake_ebi_a_GCST006414.txt"))
}
cat("LOCAL SENS DONE\n")
