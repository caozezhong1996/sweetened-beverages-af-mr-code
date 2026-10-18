# 条件F Step1 重试版: 对 mv_extract_exposures 做 5 次退避重试
suppressMessages({library(data.table); library(ieugwasr); library(TwoSampleMR)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
setwd(base)
expo_ids <- c("ukb-b-5237", "ukb-b-8442", "ieu-b-40")

exposure_dat <- NULL
for (attempt in 1:5) {
  cat(sprintf("attempt %d...\n", attempt)); flush.console()
  exposure_dat <- tryCatch(
    mv_extract_exposures(expo_ids, pval_threshold = 5e-8, clump_r2 = 0.001, clump_kb = 10000),
    error = function(e) { cat("  err:", conditionMessage(e), "\n"); flush.console(); NULL })
  if (!is.null(exposure_dat)) break
  Sys.sleep(90)
}
if (is.null(exposure_dat)) stop("mv_extract_exposures failed after 5 attempts")

cat("joint instruments:", nrow(exposure_dat), "\n"); flush.console()
print(table(exposure_dat$exposure))
fwrite(exposure_dat, "mvmr_exposure_dat_v50.csv")

cat("extracting outcome (Nielsen 2018)...\n"); flush.console()
outcome_dat <- tryCatch(extract_outcome_data(exposure_dat$SNP, "ebi-a-GCST006414"),
                        error = function(e) { cat("outcome err:", conditionMessage(e), "\n"); NULL })
if (is.null(outcome_dat)) {
  cat("API outcome failed, falling back to local Nielsen full stats...\n"); flush.console()
  nz <- fread("nielsen2018_AF_full.tsv.gz")
  # 本地查结局效应（列名自适应）
  cat("local cols:", paste(names(nz), collapse=","), "\n")
  saveRDS(list(exposure_dat = exposure_dat, local_nz = TRUE), "mvmr_step1_partial.rds")
  quit(save = "no", status = 0)
}
outcome_dat$outcome <- "Atrial fibrillation (Nielsen 2018)"
mvdat <- mv_harmonise_data(exposure_dat, outcome_dat)
cat("harmonised:", nrow(mvdat$exposure_beta), "SNPs x", ncol(mvdat$exposure_beta), "exposures\n")
saveRDS(mvdat, "mvmr_mvdat_v50.rds")
fwrite(as.data.frame(mvdat$exposure_beta), "mvmr_bgx_v50.csv")
fwrite(as.data.frame(mvdat$exposure_se), "mvmr_sebgx_v50.csv")
fwrite(as.data.frame(mvdat$outcome_beta), "mvmr_ao_v50.csv")
fwrite(as.data.frame(mvdat$outcome_se), "mvmr_seao_v50.csv")
cat("Step 1 DONE\n")
