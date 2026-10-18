# v5.0 条件 F Step 1: OpenGWAS 提取三暴露联合工具 + Nielsen 结局, 保存 mvdat
suppressMessages({library(data.table); library(ieugwasr); library(TwoSampleMR)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
setwd(base)

expo_ids <- c("ukb-b-5237", "ukb-b-8442", "ieu-b-40")
cat("extracting joint instruments (API)...\n"); flush.console()
exposure_dat <- mv_extract_exposures(expo_ids, pval_threshold = 5e-8, clump_r2 = 0.001, clump_kb = 10000)
cat("joint instruments:", nrow(exposure_dat), "\n"); flush.console()
print(table(exposure_dat$exposure))

cat("extracting outcome (Nielsen 2018)...\n"); flush.console()
outcome_dat <- extract_outcome_data(exposure_dat$SNP, "ebi-a-GCST006414")
outcome_dat$outcome <- "Atrial fibrillation (Nielsen 2018)"

mvdat <- mv_harmonise_data(exposure_dat, outcome_dat)
cat("harmonised mvdat:", nrow(mvdat$exposure_beta), "SNPs x", ncol(mvdat$exposure_beta), "exposures\n")
saveRDS(mvdat, "mvmr_mvdat_v50.rds")
fwrite(as.data.frame(mvdat$exposure_beta), "mvmr_bgx_v50.csv")
fwrite(as.data.frame(mvdat$exposure_se), "mvmr_sebgx_v50.csv")
fwrite(as.data.frame(mvdat$outcome_beta), "mvmr_ao_v50.csv")
cat("Step 1 DONE\n")
