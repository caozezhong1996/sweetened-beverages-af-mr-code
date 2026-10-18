# 第三轮仲裁: Tea-only MRlap 重跑 (seed 44)
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
for (oname in c("Nielsen2018", "FinnGenR13")) {
  odf <- prep(if (oname == "Nielsen2018") "results/ldsc_Nielsen2018.sumstats.gz" else "results/ldsc_FinnGenR13.sumstats.gz")
  set.seed(44)
  res <- MRlap(exposure = edf, exposure_name = "Tea", outcome = odf, outcome_name = oname,
               ld = normalizePath(file.path(base, "ld_ref/eur_w_ld_chr")),
               hm3 = normalizePath(file.path(base, "ld_ref/eur_w_ld_chr/w_hm3.snplist")),
               MR_pruning_LD = 0, save_logfiles = FALSE, verbose = FALSE)
  mr <- res$MRcorrection
  cat(sprintf("Tea x %s (seed44): obs=%.5f corr=%.5f diff_p=%.4g\n",
              oname, mr$observed_effect, mr$corrected_effect, mr$p_difference))
}
