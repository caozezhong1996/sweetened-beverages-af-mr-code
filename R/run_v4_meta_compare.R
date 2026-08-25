#!/usr/bin/env Rscript
# v4 upgrade step 4: assemble comparison master table (old AFGen vs new Nielsen 2018),
# fixed-effects EUR meta (Nielsen + FinnGen), updated power, and alcohol control summary.
suppressMessages({library(data.table); library(dplyr)})

root   <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
olddir <- file.path(root, "03_结果数据_mr_results")
outdir <- file.path(root, "06_升级分析_v4/results")

get_ivw <- function(f) {
  if (!file.exists(f)) return(NULL)
  r <- fread(f)
  ivw <- r[method == "Inverse variance weighted"]
  if (nrow(ivw) == 0) return(NULL)
  list(b = ivw$b, se = ivw$se, p = ivw$pval, nsnp = ivw$nsnp,
       orci = sprintf("%.3f (%.3f-%.3f)", exp(ivw$b), exp(ivw$b-1.96*ivw$se), exp(ivw$b+1.96*ivw$se)))
}
# v3.1 Sugar_added_to_tea AFGen files were saved without outcome suffix
get_ivw_fallback <- function(dir, tag, suffix_with, suffix_plain) {
  f <- file.path(dir, paste0("mr_", tag, suffix_with))
  if (!file.exists(f)) f <- file.path(dir, paste0("mr_", tag, suffix_plain))
  get_ivw(f)
}
meta_fe <- function(est_list) {
  est_list <- est_list[!sapply(est_list, is.null)]
  if (length(est_list) < 2) return(NULL)
  b <- sapply(est_list, `[[`, "b"); se <- sapply(est_list, `[[`, "se")
  w <- 1/se^2
  mb <- sum(w*b)/sum(w); mse <- sqrt(1/sum(w))
  mp <- 2*pnorm(-abs(mb/mse))
  list(b = mb, se = mse, p = mp, nsnp = NA,
       orci = sprintf("%.3f (%.3f-%.3f)", exp(mb), exp(mb-1.96*mse), exp(mb+1.96*mse)))
}

tags <- c("Artificial_sweetener_added_to_tea","Coffee_intake","Fizzy_drink_intake_SSB",
          "Low_calorie_drink_intake_ASB","Sugar_added_to_coffee","Sugar_added_to_tea","Tea_intake")
labels <- c("Artificial sweetener added to tea","Coffee intake","Fizzy drink intake (SSB)",
            "Low-calorie drink intake (ASB)","Sugar added to coffee","Sugar added to tea","Tea intake")

rows <- list()
for (i in seq_along(tags)) {
  tg <- tags[i]
  afg <- get_ivw_fallback(olddir, tg, "_ebi_a_GCST006061.csv", ".csv")
  niel <- get_ivw(file.path(outdir, paste0("mr_", tg, "_ebi_a_GCST006414.csv")))
  finn <- get_ivw(file.path(olddir, paste0("mr_", tg, "_finn_b_I9_AF.csv")))
  bbj  <- get_ivw(file.path(olddir, paste0("mr_", tg, "_bbj_a_71.csv")))
  meta_old <- meta_fe(list(afg, finn))
  meta_new <- meta_fe(list(niel, finn))
  het_new_f <- file.path(outdir, paste0("het_", tg, "_ebi_a_GCST006414.csv"))
  qp <- NA
  if (file.exists(het_new_f)) { h <- fread(het_new_f); qp <- h[method=="Inverse variance weighted"]$Q_pval[1] }
  rows[[tg]] <- data.frame(
    exposure = labels[i],
    AFGen_nsnp = afg$nsnp,   AFGen_OR = afg$orci,   AFGen_P = signif(afg$p, 3),
    Nielsen_nsnp = niel$nsnp, Nielsen_OR = niel$orci, Nielsen_P = signif(niel$p, 3),
    Nielsen_hetQ_P = signif(qp, 3),
    FinnGen_OR = finn$orci,  FinnGen_P = signif(finn$p, 3),
    BBJ_OR = bbj$orci,       BBJ_P = signif(bbj$p, 3),
    EURmeta_v31_OR = meta_old$orci, EURmeta_v31_P = signif(meta_old$p, 4),
    EURmeta_v4_OR  = meta_new$orci, EURmeta_v4_P  = signif(meta_new$p, 4),
    se_ivw_Nielsen = niel$se,
    MDE80_OR_Nielsen = exp(2.8 * niel$se),
    power_OR1.10_Nielsen = pnorm(log(1.10)/niel$se - 1.96),
    stringsAsFactors = FALSE)
}
master <- rbindlist(rows)
fwrite(master, file.path(outdir, "MASTER_v4_compare.csv"))
cat("=== MASTER v4 comparison ===\n")
print(master[, .(exposure, AFGen_OR, AFGen_P, Nielsen_OR, Nielsen_P, EURmeta_v31_OR, EURmeta_v31_P, EURmeta_v4_OR, EURmeta_v4_P)])

# ---- alcohol positive control summary ----
alc_rows <- list()
for (cfg in list(c("Alcohol_intake_frequency","Alcohol intake frequency (UKB)"),
                 c("Alcoholic_drinks_per_week_GSCAN","Alcoholic drinks per week (GSCAN)"))) {
  tg <- cfg[1]
  for (oc in c("ebi_a_GCST006414","ebi_a_GCST006061","finn_b_I9_AF","bbj_a_71")) {
    ivw <- get_ivw(file.path(outdir, paste0("mr_", tg, "_", oc, ".csv")))
    if (!is.null(ivw))
      alc_rows[[paste(tg, oc)]] <- data.frame(exposure = cfg[2], outcome = oc, nsnp = ivw$nsnp,
                                              OR = ivw$orci, P = signif(ivw$p, 3))
  }
}
alc <- rbindlist(alc_rows)
# EUR meta for GSCAN DPW: Nielsen + FinnGen (independent cohorts)
g_niel <- get_ivw(file.path(outdir, "mr_Alcoholic_drinks_per_week_GSCAN_ebi_a_GCST006414.csv"))
g_finn <- get_ivw(file.path(outdir, "mr_Alcoholic_drinks_per_week_GSCAN_finn_b_I9_AF.csv"))
g_meta <- meta_fe(list(g_niel, g_finn))
if (!is.null(g_meta))
  alc <- rbind(alc, data.frame(exposure = "Alcoholic drinks per week (GSCAN)", outcome = "EUR_meta_v4",
                               nsnp = NA, OR = g_meta$orci, P = signif(g_meta$p, 3)))
fwrite(alc, file.path(outdir, "SUMMARY_v4_alcohol_control.csv"))
cat("\n=== Alcohol positive control ===\n")
print(alc)
cat("\nDONE\n")
