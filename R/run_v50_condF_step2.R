# v5.0 条件F Step 2: MVMR 条件 F 统计量（双轮复核版）
# 主分析 gencov=0（MVMR 默认独立假设）；敏感性: 样本量近似暴露相关矩阵（假设性，标注用）
# 运行两次 (run1/run2) 比对; 条件 F 为确定性计算, 应逐位一致。
suppressMessages({library(data.table); library(MVMR)})

base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
out <- "C:/Users/64915/Desktop/EHJOpen投稿包_奶茶房颤MR_v5.0_20261006/06_新增分析_B级"
args <- commandArgs(trailingOnly = TRUE); tag <- if (length(args) >= 1) args[1] else "run1"
setwd(base)

BGX <- as.matrix(fread("mvmr_bgx_v50.csv"))   # SNP x 3 (coffee, sugar-tea, BMI)
seBGX <- as.matrix(fread("mvmr_sebgx_v50.csv"))
BYG <- as.matrix(fread("mvmr_ao_v50.csv"))    # SNP x 1
seBYG <- as.matrix(fread("mvmr_seao_v50.csv"))

# 列名对齐: mvdat 列顺序 = expo_ids 顺序 (coffee, sugar-tea, BMI)
colnames(BGX); colnames(seBGX)
stopifnot(ncol(BGX) == 3)

rsid <- if (file.exists("mvmr_rsids_v50.csv")) fread("mvmr_rsids_v50.csv")$x else sprintf("rs%d", seq_len(nrow(BGX)))

r_input <- format_mvmr(BXGs = BGX, BYG = BYG, seBXGs = seBGX, seBYG = seBYG, RSID = rsid)

# 主分析: gencov = 0
F0 <- strength_mvmr(r_input, gencov = 0)
cat("=== conditional F (gencov = 0) ===\n")
print(F0)

# 敏感性: 样本量近似 gencov（单位矩阵 + off-diag rho_ij = N_overlap/sqrt(N_i*N_j)）
# coffee=334659 (neale 1498 imputed), sugar-tea=51427 (neale ukb-b-8442 ldsc版), BMI=681275 (Yengo)
# coffee–sugartea: UKB 完全嵌套 rho≈0.39; coffee–BMI: Yengo 含 UKB≈336k rho≈0.70; sugartea–BMI rho≈0.27
N <- c(334659, 51427, 681275)
ov12 <- 51427; ov13 <- 336000; ov23 <- 51427 * (336000 / 681275)
gcov <- diag(3)
gcov[1,2] <- gcov[2,1] <- ov12 / sqrt(N[1] * N[2])
gcov[1,3] <- gcov[3,1] <- ov13 / sqrt(N[1] * N[3])
gcov[2,3] <- gcov[3,2] <- ov23 / sqrt(N[2] * N[3])
cat("\napproximate gencov matrix:\n"); print(round(gcov, 3))
Fs <- strength_mvmr(r_input, gencov = gcov)
cat("\n=== conditional F (sample-size-approximated gencov, sensitivity) ===\n")
print(Fs)

# 输出
res <- data.frame(
  run = tag,
  exposure = c("Coffee intake", "Sugar added to tea", "BMI"),
  condF_gencov0 = round(as.numeric(F0[[1]]), 2),
  condF_gencovApprox = round(as.numeric(Fs[[1]]), 2),
  n_joint_instruments = nrow(BGX),
  note = "MVMR::strength_mvmr; gencov0 = independent-GWAS assumption; approx = sample-overlap rho: coffee-sugarTea 0.39, coffee-BMI 0.70, sugarTea-BMI 0.27 (assumptions documented)"
)
print(res)
fwrite(res, file.path(out, sprintf("conditional_F_v50_%s.csv", tag)))
cat("written:", file.path(out, sprintf("conditional_F_v50_%s.csv", tag)), "\n")
