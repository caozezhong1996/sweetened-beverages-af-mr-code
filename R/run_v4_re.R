#!/usr/bin/env Rscript
# v4 step 5: multiplicative random-effects IVW sensitivity for Nielsen 2018 outcome
# (local computation on saved harmonised data; no API calls)
suppressMessages({library(data.table); library(TwoSampleMR)})
root   <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
outdir <- file.path(root, "06_升级分析_v4/results")

tags <- c("Artificial_sweetener_added_to_tea","Coffee_intake","Fizzy_drink_intake_SSB",
          "Low_calorie_drink_intake_ASB","Sugar_added_to_coffee","Sugar_added_to_tea","Tea_intake")
rows <- list()
for (tg in tags) {
  f <- file.path(outdir, paste0("dat_", tg, "_ebi_a_GCST006414.csv"))
  d <- as.data.frame(fread(f))
  res <- mr(d, method_list = c("mr_ivw_mre"))
  fwrite(as.data.table(res), file.path(outdir, paste0("mrre_", tg, "_ebi_a_GCST006414.csv")))
  r <- res[1, ]
  rows[[tg]] <- data.frame(exposure = tg, nsnp = r$nsnp, b = r$b, se = r$se, pval = r$pval,
                           OR = sprintf("%.3f (%.3f-%.3f)", exp(r$b), exp(r$b-1.96*r$se), exp(r$b+1.96*r$se)))
}
out <- rbindlist(rows)
fwrite(out, file.path(outdir, "SUMMARY_v4_nielsen_random_effects.csv"))
cat("=== Nielsen 2018 IVW (multiplicative random effects) ===\n")
print(out[, .(exposure, nsnp, OR, pval = signif(pval, 3))])
