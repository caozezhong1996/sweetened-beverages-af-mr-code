# v4.5.3 - Two-step MR mediation Stage C: BMI -> AF (beta_MY) + mediation quantification
suppressMessages({library(data.table); library(TwoSampleMR)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
res_dir <- file.path(base, "results")

sc <- fread(file.path(res_dir, "tmp_mediation_scalars_v46.csv"))
getv <- function(k) sc[item == k, value]
b_total <- getv("b_total"); se_total <- getv("se_total")
b_XM <- getv("b_XM"); se_XM <- getv("se_XM"); nsnp_XM <- getv("nsnp_XM")

## ---- BMI instruments (Yengo, window-pruned)
bmi_iv <- fread(file.path(res_dir, "tmp_bmi_instruments_v46.csv"))

## ---- Nielsen AF rows for those instruments (exact rsid match after splitting ";")
af <- fread(file.path(res_dir, "tmp_nielsen_bmiiv.tsv"))
# NOTE: in this GCST006414 harmonised file the first two header labels are swapped
# relative to content: col "rs_dbsnp147" holds chr:pos_ref/alt, col "variant_id" holds rsids.
af_long <- af[, .(rsid = unlist(strsplit(variant_id, ";", fixed = TRUE))),
              by = .(variant_id, chromosome, base_pair_location, other_allele,
                     effect_allele, effect_allele_frequency, beta, standard_error, p_value)]
af_sub <- af_long[rsid %in% bmi_iv$rsid]
setorder(af_sub, p_value); af_sub <- af_sub[!duplicated(af_sub$rsid)]
cat(sprintf("BMI instruments matched in Nielsen AF: %d / %d\n", nrow(af_sub), nrow(bmi_iv)))

exp_df <- data.frame(SNP = bmi_iv$rsid,
                     beta = bmi_iv$beta, se = bmi_iv$se, eaf = bmi_iv$eaf,
                     effect_allele = bmi_iv$ea, other_allele = bmi_iv$oa,
                     pval = bmi_iv$p, samplesize = bmi_iv$n,
                     id = "GCST006900", exposure = "BMI (Yengo 2018)",
                     stringsAsFactors = FALSE)
out_df <- data.frame(SNP = af_sub$rsid,
                     beta = af_sub$beta, se = af_sub$standard_error,
                     eaf = af_sub$effect_allele_frequency,
                     effect_allele = toupper(af_sub$effect_allele),
                     other_allele = toupper(af_sub$other_allele),
                     pval = af_sub$p_value, samplesize = 1030836,
                     id = "ebi-a-GCST006414", outcome = "Atrial fibrillation (Nielsen 2018)",
                     stringsAsFactors = FALSE)
exp_f <- format_data(exp_df, type = "exposure")
out_f <- format_data(out_df, type = "outcome")
dat_my <- harmonise_data(exp_f, out_f, action = 2)
mr_my <- mr(dat_my)
fwrite(as.data.frame(mr_my), file.path(res_dir, "mediation_step2_bmi_to_af_v46.csv"))
fwrite(dat_my, file.path(res_dir, "mediation_step2_dat_bmi_af_v46.csv"))
print(mr_my[, c("method", "nsnp", "b", "se", "pval")])

ivw_my <- mr_my[mr_my$method == "Inverse variance weighted", ]
b_MY <- ivw_my$b; se_MY <- ivw_my$se; nsnp_MY <- ivw_my$nsnp

## ---- mediation quantification (delta method)
b_ind <- b_XM * b_MY
se_ind <- sqrt(b_MY^2 * se_XM^2 + b_XM^2 * se_MY^2)
prop <- b_ind / b_total
d1 <- b_MY / b_total; d2 <- b_XM / b_total; d3 <- -b_XM * b_MY / b_total^2
se_prop <- sqrt(d1^2 * se_XM^2 + d2^2 * se_MY^2 + d3^2 * se_total^2)
z_prop <- prop / se_prop; p_prop <- 2 * pnorm(-abs(z_prop))

res <- data.frame(
  quantity = c("beta_total_coffee_to_AF_IVN",
               "beta_XM_coffee_to_BMI", "se_XM", "p_XM", "nsnp_XM",
               "beta_MY_BMI_to_AF", "se_MY", "p_MY", "nsnp_MY",
               "indirect_effect", "se_indirect",
               "proportion_mediated", "se_proportion",
               "prop_CI_lower", "prop_CI_upper", "p_proportion"),
  estimate = c(b_total, b_XM, se_XM, getv("p_XM"), nsnp_XM,
               b_MY, se_MY, ivw_my$pval, nsnp_MY,
               b_ind, se_ind, prop, se_prop,
               prop - 1.96 * se_prop, prop + 1.96 * se_prop, p_prop))
fwrite(res, file.path(res_dir, "mediation_bmi_v46.tsv"), sep = "\t")

cat(sprintf("\n==== MEDIATION SUMMARY ====\n"))
cat(sprintf("beta_total (coffee->AF): %.4f (SE %.4f)\n", b_total, se_total))
cat(sprintf("beta_XM (coffee->BMI): %.4f (SE %.4f), nsnp=%d\n", b_XM, se_XM, nsnp_XM))
cat(sprintf("beta_MY (BMI->AF): %.4f (SE %.4f), nsnp=%d\n", b_MY, se_MY, nsnp_MY))
cat(sprintf("Indirect via BMI: %.4f (SE %.4f)\n", b_ind, se_ind))
cat(sprintf("Proportion mediated: %.1f%% (95%% CI %.1f%% to %.1f%%), P=%.3g\n",
            100 * prop, 100 * (prop - 1.96 * se_prop), 100 * (prop + 1.96 * se_prop), p_prop))
cat("Stage C done.\n")
