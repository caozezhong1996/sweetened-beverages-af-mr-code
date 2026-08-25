# v4.5.3 - Two-step MR mediation: Coffee -> BMI -> AF (Stage A)
# beta_XM (coffee->BMI, Yengo 2018 GCST006900) + BMI instrument selection (window pruned)
suppressMessages({library(data.table); library(TwoSampleMR)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
res_dir <- file.path(base, "results")

## ---- Step 0: total effect coffee -> AF (Nielsen), recompute IVW from harmonised dat
dat_tot <- fread(file.path(res_dir, "dat_Coffee_intake_ebi_a_GCST006414.csv"))
mr_tot <- mr(dat_tot)
ivw_tot <- mr_tot[mr_tot$method == "Inverse variance weighted", ]
b_total <- ivw_tot$b; se_total <- ivw_tot$se; p_total <- ivw_tot$pval; nsnp_tot <- ivw_tot$nsnp
cat(sprintf("beta_total (coffee->AF Nielsen IVW): %.4f (SE %.4f), P=%.3g, nsnp=%d\n",
            b_total, se_total, p_total, nsnp_tot))

## ---- Load Yengo 2018 BMI (GCST006900, hg19, kg/m^2)
bmi <- fread(file.path(base, "yengo2018_bmi_gcst006900.txt.gz"),
             select = c("CHR","POS","SNP","Tested_Allele","Other_Allele",
                        "Freq_Tested_Allele_in_HRS","BETA","SE","P","N"))
setnames(bmi, c("chr","pos","rsid","ea","oa","eaf","beta","se","p","n"))
bmi[, ea := toupper(ea)][, oa := toupper(oa)]
# dedupe by rsid (keep smallest p)
setorder(bmi, p); bmi <- bmi[!duplicated(bmi$rsid)]
cat(sprintf("Yengo BMI variants loaded: %d\n", nrow(bmi)))

## ---- Step 1: coffee -> BMI (beta_XM) via IVW with the 34 coffee instruments
sub <- bmi[rsid %in% dat_tot$SNP]
cat(sprintf("Coffee instruments found in Yengo BMI: %d / %d\n", nrow(sub), nrow(dat_tot)))

exp_df <- data.frame(SNP = dat_tot$SNP,
                     beta = dat_tot$beta.exposure, se = dat_tot$se.exposure,
                     eaf = dat_tot$eaf.exposure,
                     effect_allele = dat_tot$effect_allele.exposure,
                     other_allele = dat_tot$other_allele.exposure,
                     pval = dat_tot$pval.exposure,
                     samplesize = dat_tot$samplesize.exposure,
                     id = "ukb-b-5237", exposure = "Coffee intake",
                     stringsAsFactors = FALSE)
out_df <- data.frame(SNP = sub$rsid,
                     beta = sub$beta, se = sub$se, eaf = sub$eaf,
                     effect_allele = sub$ea, other_allele = sub$oa,
                     pval = sub$p, samplesize = sub$n,
                     id = "GCST006900", outcome = "BMI (Yengo 2018)",
                     stringsAsFactors = FALSE)
exp_f <- format_data(exp_df, type = "exposure")
out_f <- format_data(out_df, type = "outcome")
dat_xm <- harmonise_data(exp_f, out_f, action = 2)
mr_xm <- mr(dat_xm)
ivw_xm <- mr_xm[mr_xm$method == "Inverse variance weighted", ]
b_XM <- ivw_xm$b; se_XM <- ivw_xm$se; p_XM <- ivw_xm$pval; nsnp_xm <- ivw_xm$nsnp
cat(sprintf("beta_XM (coffee->BMI IVW): %.5f (SE %.5f), P=%.3g, nsnp=%d\n",
            b_XM, se_XM, p_XM, nsnp_xm))
fwrite(as.data.frame(mr_xm), file.path(res_dir, "mediation_step1_coffee_to_bmi_v46.csv"))
fwrite(dat_xm, file.path(res_dir, "mediation_step1_dat_coffee_bmi_v46.csv"))

## ---- BMI instrument selection for step 2: P<5e-8 + 1-Mb window pruning
hits <- bmi[p < 5e-8]
cat(sprintf("BMI variants P<5e-8: %d\n", nrow(hits)))
setorder(hits, p)
keep <- rep(TRUE, nrow(hits))
sel_idx <- integer(0)
for (i in seq_len(nrow(hits))) {
  if (!keep[i]) next
  sel_idx <- c(sel_idx, i)
  same <- hits$chr == hits$chr[i] & abs(hits$pos - hits$pos[i]) <= 1e6
  keep[same & seq_len(nrow(hits)) > i] <- FALSE
}
bmi_iv <- hits[sel_idx]
cat(sprintf("BMI instruments after 1-Mb window pruning: %d\n", nrow(bmi_iv)))
fwrite(bmi_iv, file.path(res_dir, "tmp_bmi_instruments_v46.csv"))
writeLines(bmi_iv$rsid, file.path(res_dir, "tmp_bmi_iv_rsids_v46.txt"))

## ---- save step-0/1 scalars for stage C
scalars <- data.frame(item = c("b_total","se_total","p_total","nsnp_total",
                               "b_XM","se_XM","p_XM","nsnp_XM"),
                      value = c(b_total, se_total, p_total, nsnp_tot,
                                b_XM, se_XM, p_XM, nsnp_xm))
fwrite(scalars, file.path(res_dir, "tmp_mediation_scalars_v46.csv"))
cat("Stage A done.\n")
