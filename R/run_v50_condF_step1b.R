# v5.0 条件F Step1B (近似版, API clump 服务故障期间):
# 联合工具 = coffee(34, 本地5e-8) ∪ sugarTea(2, 本地5e-8) ∪ BMI(724, 本地1-Mb窗口)
# 暴露交叉效应经 associations 端点查询; 结局 Nielsen (GCST006414) 同样经 associations。
# 注: BMI 工具为 1-Mb 窗口剪枝版 (原 MVMR 为 r2<0.001 clump 的 467 个), 属近似, 结果表注明。
suppressMessages({library(data.table); library(ieugwasr)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
setwd(base)

dat_coffee <- fread("results/dat_Coffee_intake_ebi_a_GCST006414.csv")
dat_st     <- fread("results/dat_Sugar_added_to_tea_ebi_a_GCST006414.csv")
bmi_rsids  <- readLines("results/tmp_bmi_iv_rsids_v46.txt")

coffee_iv <- dat_coffee[pval.exposure < 5e-8, SNP]
st_iv <- dat_st[pval.exposure < 5e-8, SNP]
all_snps <- unique(c(coffee_iv, st_iv, bmi_rsids))
cat(sprintf("joint instruments: %d (coffee %d, sugarTea %d, BMI %d)\n",
            length(all_snps), length(coffee_iv), length(st_iv), length(bmi_rsids)))
flush.console()

# 分批 associations
batch_assoc <- function(snps, id, size = 200) {
  chunks <- split(snps, ceiling(seq_along(snps) / size))
  out <- lapply(chunks, function(ch) {
    for (att in 1:5) {
      r <- tryCatch(associations(ch, id), error = function(e) NULL)
      if (!is.null(r)) return(r)
      cat(sprintf("  retry %s (%d snps) attempt %d...\n", id, length(ch), att)); flush.console()
      Sys.sleep(20)
    }
    stop(paste("failed:", id))
  })
  rbindlist(out, fill = TRUE)
}

cat("querying coffee (ukb-b-5237)...\n"); flush.console()
a_coffee <- batch_assoc(all_snps, "ukb-b-5237")
cat("querying sugarTea (ukb-b-8442)...\n"); flush.console()
a_st <- batch_assoc(all_snps, "ukb-b-8442")
cat("querying outcome Nielsen (ebi-a-GCST006414)...\n"); flush.console()
a_af <- batch_assoc(all_snps, "ebi-a-GCST006414")

# BMI 列: Yengo 本地
bmi <- fread("yengo2018_bmi_gcst006900.txt.gz",
             select = c("SNP","Tested_Allele","Other_Allele","BETA","SE","P"))
setnames(bmi, c("rsid","ea","oa","beta","se","p"))
bmi[, ea := toupper(ea)][, oa := toupper(oa)]
setorder(bmi, p); bmi <- bmi[!duplicated(rsid)]

saveRDS(list(a_coffee = a_coffee, a_st = a_st, a_af = a_af, bmi = bmi,
             coffee_iv = coffee_iv, st_iv = st_iv, bmi_rsids = bmi_rsids),
        "mvmr_step1b_raw.rds")
fwrite(a_coffee, "mvmr_assoc_coffee_v50.csv")
fwrite(a_st, "mvmr_assoc_sugartea_v50.csv")
fwrite(a_af, "mvmr_assoc_af_v50.csv")
cat("Step1B DONE\n")
