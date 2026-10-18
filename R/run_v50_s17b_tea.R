# v5.0: tea MRlap 完整结果提取（S17 扩展表用, 保存全套量）
suppressMessages({library(data.table); library(devtools)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
setwd(base)
ld <- rbindlist(lapply(1:22, function(cc)
  fread(sprintf("ld_ref/eur_w_ld_chr/%d.l2.ldscore.gz", cc), select = c("CHR","SNP","BP"))))
prep <- function(path) {
  d <- fread(path); d2 <- merge(d, ld, by = "SNP")
  data.frame(rsid = d2$SNP, chr = d2$CHR, pos = d2$BP, a1 = d2$A1, a2 = d2$A2, z = d2$Z, N = d2$N)
}
devtools::load_all("genomicsem_src", quiet = TRUE)
devtools::load_all("mrlap_src", quiet = TRUE)
edf <- prep("neale_ldsc/1488_raw.ldsc.imputed_v3.both_sexes.tsv.bgz")
outrows <- list()
for (oname in c("Nielsen2018", "FinnGenR13")) {
  odf <- prep(if (oname == "Nielsen2018") "results/ldsc_Nielsen2018.sumstats.gz" else "results/ldsc_FinnGenR13.sumstats.gz")
  set.seed(42)
  res <- MRlap(exposure = edf, exposure_name = "Tea", outcome = odf, outcome_name = oname,
               ld = normalizePath(file.path(base, "ld_ref/eur_w_ld_chr")),
               hm3 = normalizePath(file.path(base, "ld_ref/eur_w_ld_chr/w_hm3.snplist")),
               MR_pruning_LD = 0, save_logfiles = FALSE, verbose = FALSE)
  mr <- res$MRcorrection; ld2 <- res$LDSC; ga <- res$GeneticArchitecture
  q <- data.frame(
    outcome = oname,
    Quantity = c("Observed IVW effect (per SD)", "Corrected effect (per SD)",
                 "Test of difference (corrected - observed)", "MR-Egger intercept P",
                 "Instruments used by MRlap", "LDSC SNP heritability, exposure",
                 "LDSC intercept, exposure", "LDSC SNP heritability, outcome",
                 "LDSC intercept, outcome", "Cross-trait genetic covariance",
                 "Cross-trait rg", "Cross-trait LDSC intercept (overlap metric)",
                 "Estimated polygenicity (exposure)", "Per-SNP heritability (exposure)"),
    Estimate = c(sprintf("%.4f", mr$observed_effect), sprintf("%.4f", mr$corrected_effect),
                 sprintf("%.4f", mr$test_difference), sprintf("%.3f", mr$egger_intercept_p),
                 sprintf("%d (%d candidates P < 5e-8, 500-kb distance pruning)", mr$m_IVs, 428),
                 sprintf("%.4f", ld2$h2_exp), sprintf("%.4f", ld2$int_exp),
                 sprintf("%.4f", ld2$h2_out), sprintf("%.4f", ld2$int_out),
                 sprintf("%.4f", ld2$gcov), sprintf("%.4f", ld2$rg),
                 sprintf("%.4f", ld2$int_crosstrait), sprintf("%.4f", ga$polygenicity),
                 sprintf("%.1e", ga$perSNP_heritability)),
    SE = c(sprintf("%.4f", mr$observed_effect_se), sprintf("%.4f", mr$corrected_effect_se),
           "-", "-", "-", sprintf("%.4f", ld2$h2_exp_se), "-",
           sprintf("%.4f", ld2$h2_out_se), "-", sprintf("%.4f", ld2$gcov_se), "-",
           sprintf("%.4f", ld2$int_crosstrait_se), "-", "-"),
    P = c(sprintf("%.3f", mr$observed_effect_p), sprintf("%.3f", mr$corrected_effect_p),
          sprintf("%.3f", mr$p_difference), "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"),
    stringsAsFactors = FALSE)
  outrows[[oname]] <- q
  cat(oname, "done: obs", mr$observed_effect, "corr", mr$corrected_effect, "diffP", mr$p_difference, "\n"); flush.console()
}
alldf <- rbindlist(outrows)
fwrite(alldf, "supplement_tables/S17b_mrlap_tea.tsv", sep = "\t")
cat("written S17b_mrlap_tea.tsv\n")
