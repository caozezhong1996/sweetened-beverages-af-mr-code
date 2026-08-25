# v4.5.4 Task B - Neale 21001 (BMI, raw kg/m2) two-step mediation sensitivity
# Goal: recover step-1 (coffee->BMI) with up to 34/34 instrument SNPs (Yengo main had 17/34)
# Also: cross-exposure-GWAS IVW meta-analysis (main ukb-b-5237 + Neale 1498)
suppressMessages({library(data.table); library(TwoSampleMR)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
dl <- file.path(base, "downloads"); res_dir <- file.path(base, "results")
KG_PER_SD <- 4.8  # Yengo anchor: FTO rs1558902 0.078 SD ~ 0.39 kg/m2

## ---- 1. 34 coffee instruments (ukb-b-5237 betas, same exposure scale as main IVW)
main <- fread(file.path(res_dir, "dat_Coffee_intake_ebi_a_GCST006414.csv"))

## ---- 2. Neale 21001 BMI rows matched by chr:pos
bmi <- fread(file.path(dl, "neale21001_iv34.tsv"),
             header = FALSE,
             col.names = c("variant","minor_allele","minor_AF","low_conf",
                           "n","AC","ytx","beta","se","tstat","pval"))
vp <- tstrsplit(bmi$variant, ":", fixed = TRUE)
bmi[, `:=`(chr = as.integer(vp[[1]]), pos = as.integer(vp[[2]]),
           ref = vp[[3]], alt = vp[[4]])]
m <- merge(main, bmi, by = c("chr", "pos"))
cat(sprintf("Instruments matched in Neale 21001: %d / %d\n", nrow(m), nrow(main)))
miss <- main[!paste(main$chr, main$pos) %in% paste(m$chr, m$pos), ]
if (nrow(miss)) cat("Missing:", paste(miss$SNP, miss$chr, miss$pos, sep = ":"), "\n")

## ---- 3. Harmonize BMI beta to coffee-instrument effect allele
m[, ea_x := toupper(effect_allele.exposure)][, oa_x := toupper(other_allele.exposure)]
harm <- m[(alt == ea_x & ref == oa_x) | (alt == oa_x & ref == ea_x)]
harm[, b_bmi := ifelse(alt == ea_x, beta, -beta)]
harm[, se_bmi := se]
cat(sprintf("Allele-matched for step1: %d\n", nrow(harm)))

## ---- 4. Step-1 IVW: coffee -> BMI (kg/m2)
exp_df <- data.frame(SNP = harm$SNP, beta = harm$beta.exposure, se = harm$se.exposure,
                     eaf = harm$eaf.exposure, effect_allele = harm$ea_x,
                     other_allele = harm$oa_x, pval = harm$pval.exposure,
                     samplesize = harm$samplesize.exposure, id = "ukb-b-5237",
                     exposure = "Coffee intake", stringsAsFactors = FALSE)
out_df <- data.frame(SNP = harm$SNP, beta = harm$b_bmi, se = harm$se_bmi,
                     eaf = harm$minor_AF, effect_allele = harm$ea_x,
                     other_allele = harm$oa_x, pval = harm$pval,
                     samplesize = harm$n, id = "Neale21001",
                     outcome = "BMI (Neale 21001, kg/m2)", stringsAsFactors = FALSE)
exp_f <- format_data(exp_df, type = "exposure")
out_f <- format_data(out_df, type = "outcome")
dat_xm <- harmonise_data(exp_f, out_f, action = 1)
dat_xm <- dat_xm[dat_xm$mr_keep, ]
fwrite(dat_xm, file.path(res_dir, "mediation_step1_dat_coffee_bmi21001_v47.csv"))
mr_xm <- mr(dat_xm, method_list = c("mr_ivw", "mr_weighted_median", "mr_egger_regression"))
fwrite(as.data.frame(mr_xm), file.path(res_dir, "mediation_step1_coffee_to_bmi21001_v47.csv"))
print(mr_xm[, c("method", "nsnp", "b", "se", "pval")])
ivw <- mr_xm[mr_xm$method == "Inverse variance weighted", ]
b_XM <- ivw$b; se_XM <- ivw$se; nsnp_XM <- ivw$nsnp; p_XM <- ivw$pval

## unit sanity: FTO-locus instrument 16:53800954 should be ~0.36-0.39 kg/m2 per C
fto <- bmi[chr == 16 & abs(pos - 53800954) < 5000]
cat(sprintf("Unit sanity FTO 16:53800954: beta=%.3f kg/m2 (expect ~0.36-0.39)\n", fto$beta[1]))

## ---- 5. Mediation quantification (delta method, same as v46)
sc <- fread(file.path(res_dir, "tmp_mediation_scalars_v46.csv"))
getv <- function(k) sc[item == k, value]
b_total <- getv("b_total"); se_total <- getv("se_total")
v46 <- fread(file.path(res_dir, "mediation_bmi_v46.tsv"))
b_MY_SD <- v46[quantity == "beta_MY_BMI_to_AF", estimate]
se_MY_SD <- v46[quantity == "se_MY", estimate]
b_MY <- b_MY_SD / KG_PER_SD; se_MY <- se_MY_SD / KG_PER_SD   # per kg/m2

b_ind <- b_XM * b_MY
se_ind <- sqrt(b_MY^2 * se_XM^2 + b_XM^2 * se_MY^2)
prop <- b_ind / b_total
d1 <- b_MY / b_total; d2 <- b_XM / b_total; d3 <- -b_XM * b_MY / b_total^2
se_prop <- sqrt(d1^2 * se_XM^2 + d2^2 * se_MY^2 + d3^2 * se_total^2)
p_prop <- 2 * pnorm(-abs(prop / se_prop))

res <- data.frame(
  quantity = c("beta_XM_coffee_to_BMI_kgm2", "se_XM", "p_XM", "nsnp_XM",
               "beta_XM_perSD", "beta_MY_per_kgm2", "b_total",
               "indirect_effect", "se_indirect",
               "proportion_mediated", "se_proportion",
               "prop_CI_lower", "prop_CI_upper", "p_proportion"),
  estimate = c(b_XM, se_XM, p_XM, nsnp_XM, b_XM / KG_PER_SD, b_MY, b_total,
               b_ind, se_ind, prop, se_prop,
               prop - 1.96 * se_prop, prop + 1.96 * se_prop, p_prop))
fwrite(res, file.path(res_dir, "mediation_bmi_neale21001_v47.tsv"), sep = "\t")

cat(sprintf("\n==== MEDIATION (Neale 21001) ====\n"))
cat(sprintf("beta_XM: %.4f kg/m2 per coffee-unit (SE %.4f, P=%.3g, nsnp=%d) = %.4f SD\n",
            b_XM, se_XM, p_XM, nsnp_XM, b_XM / KG_PER_SD))
cat(sprintf("Indirect via BMI: %.4f (SE %.4f)\n", b_ind, se_ind))
cat(sprintf("Proportion mediated: %.1f%% (95%%CI %.1f%% to %.1f%%), P=%.3g\n",
            100 * prop, 100 * (prop - 1.96 * se_prop), 100 * (prop + 1.96 * se_prop), p_prop))

## ---- 6. Cross-exposure-GWAS IVW meta-analysis (fixed effects)
b1 <- 0.234718580377584; s1 <- 0.11195560044895            # main ukb-b-5237 IVW
a <- fread(file.path(res_dir, "mr_neale1498_nielsen_v47.csv"))
b2 <- a[method == "Inverse variance weighted", b]; s2 <- a[method == "Inverse variance weighted", se]
w1 <- 1 / s1^2; w2 <- 1 / s2^2
b_meta <- sum(w1 * b1 + w2 * b2) / (w1 + w2); se_meta <- sqrt(1 / (w1 + w2))
z <- b_meta / se_meta; p_meta <- 2 * pnorm(-abs(z))
meta <- data.frame(source = c("ukb-b-5237 (main)", "Neale 1498 (replication)", "Fixed-effect meta"),
                   b = c(b1, b2, b_meta), se = c(s1, s2, se_meta),
                   OR = exp(c(b1, b2, b_meta)),
                   CI_lo = exp(c(b1, b2, b_meta) - 1.96 * c(s1, s2, se_meta)),
                   CI_hi = exp(c(b1, b2, b_meta) + 1.96 * c(s1, s2, se_meta)),
                   pval = c(0.0360349598459479, a[method == "Inverse variance weighted", pval], p_meta))
fwrite(meta, file.path(res_dir, "mr_coffee_ivw_crossgwas_meta_v47.csv"))
print(meta)
cat("Task B done.\n")
