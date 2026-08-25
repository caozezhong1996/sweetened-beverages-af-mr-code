# v4.5.3 - MRlap: coffee (Neale 1498) x AF (Nielsen 2018) overlap-bias quantification
suppressMessages({library(data.table); library(devtools)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
setwd(base)
dir.create("mrlap_run", showWarnings = FALSE)

## ---- prep inputs: munged files + chr/pos from LD score files
cat("loading LD score chr/pos...\n")
ld <- rbindlist(lapply(1:22, function(cc)
  fread(sprintf("ld_ref/eur_w_ld_chr/%d.l2.ldscore.gz", cc), select = c("CHR","SNP","BP"))))
prep <- function(path) {
  d <- fread(path)
  d2 <- merge(d, ld, by = "SNP")
  data.frame(rsid = d2$SNP, chr = d2$CHR, pos = d2$BP,
             a1 = d2$A1, a2 = d2$A2, z = d2$Z, N = d2$N)
}
coffee_df <- prep("neale_ldsc/1498.ldsc.imputed_v3.both_sexes.tsv.bgz")
af_df     <- prep("results/ldsc_Nielsen2018.sumstats.gz")
cat(sprintf("coffee SNPs: %d ; AF SNPs: %d\n", nrow(coffee_df), nrow(af_df)))

## ---- load packages from source
devtools::load_all("genomicsem_src", quiet = TRUE)
devtools::load_all("mrlap_src", quiet = TRUE)
cat("packages loaded\n")

setwd("mrlap_run")
res <- MRlap(exposure = coffee_df, exposure_name = "Coffee",
             outcome = af_df, outcome_name = "AF",
             ld = normalizePath(file.path(base, "ld_ref/eur_w_ld_chr")),
             hm3 = normalizePath(file.path(base, "ld_ref/eur_w_ld_chr/w_hm3.snplist")),
             MR_pruning_LD = 0,
             save_logfiles = TRUE, verbose = TRUE)
saveRDS(res, "mrlap_coffee_af_v46.rds")

mr <- res$MRcorrection; ld2 <- res$LDSC; ga <- res$GeneticArchitecture
sink("mrlap_coffee_v46.txt")
cat("==== MRlap coffee(Neale1498) -> AF(Nielsen2018) ====\n")
cat(sprintf("observed effect:  %.5f (SE %.5f), P=%.3g, m_IVs=%d\n",
            mr$observed_effect, mr$observed_effect_se, mr$observed_effect_p, mr$m_IVs))
cat(sprintf("corrected effect: %.5f (SE %.5f), P=%.3g\n",
            mr$corrected_effect, mr$corrected_effect_se, mr$corrected_effect_p))
cat(sprintf("test difference:  %.5f, P_difference=%.3g\n", mr$test_difference, mr$p_difference))
cat(sprintf("egger intercept P: %.3g\n", mr$egger_intercept_p))
cat(sprintf("LDSC: h2_exp=%.5f(%.5f) int_exp=%.5f ; h2_out=%.5f(%.5f) int_out=%.5f\n",
            ld2$h2_exp, ld2$h2_exp_se, ld2$int_exp, ld2$h2_out, ld2$h2_out_se, ld2$int_out))
cat(sprintf("LDSC cross-trait: gcov=%.5f(%.5f) rg=%.5f intercept=%.5f (SE %.5f)\n",
            ld2$gcov, ld2$gcov_se, ld2$rg, ld2$int_crosstrait, ld2$int_crosstrait_se))
cat(sprintf("GeneticArchitecture: polygenicity=%.5f perSNP_h2=%.3g\n",
            ga$polygenicity, ga$perSNP_heritability))
sink()
cat("MRlap done.\n")
