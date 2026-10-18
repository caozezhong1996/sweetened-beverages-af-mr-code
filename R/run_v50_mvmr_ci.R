# v5.0 (PB4/5, rev 2 - 第三轮仲裁版) - 直接/间接/总效应 CI + 工具重叠统计
# 数据源：经 v457 投稿前数据审计的原 pipeline 中间文件（mediation_bmi_v46.tsv 等）。
# rev1 的手写 harmonisation 与原 TwoSampleMR action=2 实现不一致（0.0139 vs 0.820），已废弃。
suppressMessages({library(data.table)})

base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
out <- "C:/Users/64915/Desktop/EHJOpen投稿包_奶茶房颤MR_v5.0_20261006/06_新增分析_B级"
args <- commandArgs(trailingOnly = TRUE); tag <- if (length(args) >= 1) args[1] else "run1"

med <- fread(file.path(base, "results", "mediation_bmi_v46.tsv"))
gv <- function(k) med[quantity == k, estimate]

b_tot <- gv("beta_total_coffee_to_AF_IVN"); se_tot <- 0.11195560044895  # scalars file (audited)
b_xm  <- gv("beta_XM_coffee_to_BMI");  se_xm <- gv("se_XM")
b_my  <- gv("beta_MY_BMI_to_AF");     se_my <- gv("se_MY")
b_ind <- gv("indirect_effect");       se_ind <- gv("se_indirect")
prop  <- gv("proportion_mediated")

mv <- fread(file.path(base, "results", "mvmr_coffee_sugartea_bmi_Nielsen.csv"))
dc <- mv[exposure_label == "Coffee intake"]; b_dir <- dc$b; se_dir <- dc$se
db <- mv[exposure_label == "BMI"]; b_bmi <- db$b; se_bmi <- db$se
st <- mv[exposure_label == "Sugar added to tea"]

# 工具重叠（本地可验部分）
dat_coffee <- fread(file.path(base, "results", "dat_Coffee_intake_ebi_a_GCST006414.csv"))
dat_st <- fread(file.path(base, "results", "dat_Sugar_added_to_tea_ebi_a_GCST006414.csv"))
bmi <- fread(file.path(base, "yengo2018_bmi_gcst006900.txt.gz"), select = c("SNP","P"))
bmi_iv <- bmi[P < 5e-8, toupper(SNP)]
res <- data.frame(
  quantity = c(
    "total effect, coffee->AF (IVW, 34 SNPs)",
    "step 1, coffee->BMI (IVW, 17 SNPs after action=2 harmonisation)",
    "step 2, BMI->AF (IVW, 701 SNPs)",
    "INDIRECT effect (product method)",
    "DIRECT effect, coffee|BMI,sugar-tea (MVMR, 14 joint SNPs)",
    "MVMR BMI positive control",
    "MVMR sugar-added-to-tea (single joint instrument)",
    "mediated proportion",
    "instrument overlap: coffee(n=34) & BMI(5e-8) SNPs",
    "instrument overlap: sugar-tea(n=17) & BMI(5e-8) SNPs",
    "instrument overlap: coffee(n=34) & sugar-tea(n=17) SNPs"),
  estimate = round(c(b_tot, b_xm, b_my, b_ind, b_dir, b_bmi, st$b, prop,
                     length(intersect(toupper(dat_coffee$SNP), bmi_iv)),
                     length(intersect(toupper(dat_st$SNP), bmi_iv)),
                     length(intersect(dat_coffee$SNP, dat_st$SNP))), 4),
  ci95_low = round(c(b_tot-1.96*se_tot, b_xm-1.96*se_xm, b_my-1.96*se_my, b_ind-1.96*se_ind,
                     b_dir-1.96*se_dir, b_bmi-1.96*se_bmi, st$b-1.96*st$se, -0.231150963749309,
                     NA, NA, NA), 4),
  ci95_high = round(c(b_tot+1.96*se_tot, b_xm+1.96*se_xm, b_my+1.96*se_my, b_ind+1.96*se_ind,
                      b_dir+1.96*se_dir, b_bmi+1.96*se_bmi, st$b+1.96*st$se, 2.62668192234036,
                      NA, NA, NA), 4),
  or_display = c("1.26 (1.02-1.57)", "per category, SD units", "-", sprintf("%.3f (%.3f-%.3f)", exp(b_ind), exp(b_ind-1.96*se_ind), exp(b_ind+1.96*se_ind)),
                 sprintf("%.2f (%.2f-%.2f)", exp(b_dir), exp(b_dir-1.96*se_dir), exp(b_dir+1.96*se_dir)),
                 sprintf("%.2f (%.2f-%.2f)", exp(b_bmi), exp(b_bmi-1.96*se_bmi), exp(b_bmi+1.96*se_bmi)),
                 sprintf("%.2f", exp(st$b)), "120% (-23% to 263%)", "-", "-", "-")
)
print(res)
fwrite(res, file.path(out, sprintf("MVMR_mediation_CI_v50_%s.csv", tag)))
cat("written:", file.path(out, sprintf("MVMR_mediation_CI_v50_%s.csv", tag)), "\n")
