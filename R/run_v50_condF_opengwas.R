# v5.0 (PB4 拓展, 待 OpenGWAS token 更新后运行) - 三暴露 MVMR 条件 F 统计量
# 依赖: OpenGWAS API (OPENGWAS_JWT), 因 sugar-added-to-tea 无公开全统计,
#       482 个联合工具 SNP 的 sugar-tea 侧效应只能经 API 提取。
# 用法: 更新 ~/.Renviron 的 OPENGWAS_JWT 后运行本脚本两次 (run1/run2) 比对。
suppressMessages({library(data.table); library(ieugwasr); library(TwoSampleMR); library(MVMR)})

expo_ids <- c("ukb-b-5237", "ukb-b-8442", "ieu-b-40")  # coffee, sugar-in-tea, BMI
cat("extracting joint instruments (may take a few minutes)...\n")
exposure_dat <- mv_extract_exposures(expo_ids, pval_threshold = 5e-8, clump_r2 = 0.001, clump_kb = 10000)
outcome_dat <- extract_outcome_data(exposure_dat$SNP, "ebi-a-GCST006414")
mvdat <- mv_harmonise_data(exposure_dat, outcome_dat)

# MVMR 输入格式: BGX (SNP x exposure beta), seBGX, outcome beta/se
mvmr_in <- as.data.frame(mvdat[["exposure_beta"]])          # 视 mvdat 结构调整
# 用 MVMR 包:
#   formatted <- format_mvmr(BGX = ..., seBGX = ..., Ao = ..., ...)
#   res <- strength_mvmr(...)
#   q <- q_estimate(...)  # 样本重叠协方差
# 按 MVMR 包 vignette 调整字段名后运行 strength_mvmr 输出每暴露条件 F
saveRDS(mvdat, "mvmr_mvdat_v50.rds")
cat("mvdat saved; run strength_mvmr per MVMR package vignette after inspecting structure.\n")
