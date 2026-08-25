# v4.5.3 - Stage A2: recover missing coffee SNPs in Yengo BMI by chr:pos (hg19), recompute beta_XM
suppressMessages({library(data.table); library(TwoSampleMR)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
res_dir <- file.path(base, "results")

dat_tot <- fread(file.path(res_dir, "dat_Coffee_intake_ebi_a_GCST006414.csv"))
dat_xm_old <- fread(file.path(res_dir, "mediation_step1_dat_coffee_bmi_v46.csv"))
matched <- unique(dat_xm_old$SNP)
missing <- dat_tot[!SNP %in% matched]
cat(sprintf("Already matched by rsid: %d; missing: %d\n", length(matched), nrow(missing)))

bmi <- fread(file.path(base, "yengo2018_bmi_gcst006900.txt.gz"),
             select = c("CHR","POS","SNP","Tested_Allele","Other_Allele",
                        "Freq_Tested_Allele_in_HRS","BETA","SE","P","N"))
setnames(bmi, c("chr","pos","rsid","ea","oa","eaf","beta","se","p","n"))
bmi[, ea := toupper(ea)][, oa := toupper(oa)]
setorder(bmi, p); bmi <- bmi[!duplicated(bmi$rsid)]

m2 <- merge(missing[, .(SNP, chr, pos)], bmi[, .(chr, pos, rsid)], by = c("chr","pos"))
cat(sprintf("Recovered by chr:pos exact match: %d / %d\n", nrow(m2), nrow(missing)))
if (nrow(m2) > 0) print(m2)

# final SNP set: old matched rsids + recovered Yengo rsids
final_rsids <- unique(c(matched, m2$rsid))
sub <- bmi[rsid %in% final_rsids]
cat(sprintf("Final coffee-instrument set in Yengo: %d / %d\n", nrow(sub), nrow(dat_tot)))

exp_df <- data.frame(SNP = dat_tot$SNP,
                     beta = dat_tot$beta.exposure, se = dat_tot$se.exposure,
                     eaf = dat_tot$eaf.exposure,
                     effect_allele = dat_tot$effect_allele.exposure,
                     other_allele = dat_tot$other_allele.exposure,
                     pval = dat_tot$pval.exposure,
                     samplesize = dat_tot$samplesize.exposure,
                     id = "ukb-b-5237", exposure = "Coffee intake",
                     stringsAsFactors = FALSE)
# exposure rows keyed by original rsid; for recovered SNPs need dat rows matched by chr:pos
# build map: Yengo rsid -> original coffee SNP (via chr:pos for recovered, identity otherwise)
key <- data.table(yengo_rsid = sub$rsid)
key[, orig := yengo_rsid]
rec_map <- m2[, .(rsid, SNP)]
key <- merge(key, rec_map, by.x = "yengo_rsid", by.y = "rsid", all.x = TRUE)
key[!is.na(SNP), orig := SNP][, SNP := NULL]
exp_use <- merge(key, exp_df, by.x = "orig", by.y = "SNP")
exp_use$SNP <- exp_use$yengo_rsid

out_df <- data.frame(SNP = sub$rsid,
                     beta = sub$beta, se = sub$se, eaf = sub$eaf,
                     effect_allele = sub$ea, other_allele = sub$oa,
                     pval = sub$p, samplesize = sub$n,
                     id = "GCST006900", outcome = "BMI (Yengo 2018)",
                     stringsAsFactors = FALSE)
exp_f <- format_data(as.data.frame(exp_use[, setdiff(names(exp_use), c("orig","yengo_rsid")), with = FALSE]), type = "exposure")
out_f <- format_data(out_df, type = "outcome")
dat_xm <- harmonise_data(exp_f, out_f, action = 2)
mr_xm <- mr(dat_xm)
ivw_xm <- mr_xm[mr_xm$method == "Inverse variance weighted", ]
cat(sprintf("beta_XM (recovered set) IVW: %.5f (SE %.5f), P=%.3g, nsnp=%d\n",
            ivw_xm$b, ivw_xm$se, ivw_xm$pval, ivw_xm$nsnp))
fwrite(as.data.frame(mr_xm), file.path(res_dir, "mediation_step1_coffee_to_bmi_v46.csv"))
fwrite(dat_xm, file.path(res_dir, "mediation_step1_dat_coffee_bmi_v46.csv"))

# update scalars
sc <- fread(file.path(res_dir, "tmp_mediation_scalars_v46.csv"))
sc[item == "b_XM", value := ivw_xm$b][item == "se_XM", value := ivw_xm$se]
sc[item == "p_XM", value := ivw_xm$pval][item == "nsnp_XM", value := ivw_xm$nsnp]
fwrite(sc, file.path(res_dir, "tmp_mediation_scalars_v46.csv"))
cat("Stage A2 done.\n")
