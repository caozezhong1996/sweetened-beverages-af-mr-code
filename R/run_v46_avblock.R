# v4.5.3 - Negative outcome control: 9 beverage exposures -> AV block (FinnGen R13 I9_AVBLOCK)
suppressMessages({library(data.table); library(TwoSampleMR)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
res_dir <- file.path(base, "results")

av <- fread(file.path(res_dir, "tmp_avblock_extract.tsv"))
av_long <- av[, .(rsid = unlist(strsplit(rsids, ",", fixed = TRUE))),
              by = .(`#chrom`, pos, ref, alt, pval, beta, sebeta, af_alt)]
av_long[, ref := toupper(ref)][, alt := toupper(alt)]
setorder(av_long, pval); av_long <- av_long[!duplicated(av_long$rsid)]
cat(sprintf("AVBLOCK extracted unique rsids: %d\n", nrow(av_long)))

files <- list.files(res_dir, pattern = "^dat_.*_finngen_R13\\.csv$", full.names = TRUE)
out_all <- list()
for (f in files) {
  dat <- fread(f)
  expo_name <- gsub("^dat_|_finngen_R13\\.csv$", "", basename(f))
  sub <- av_long[rsid %in% dat$SNP]
  if (nrow(sub) < 3) { cat(sprintf("%s: only %d SNPs matched, skipped\n", expo_name, nrow(sub))); next }
  exp_df <- data.frame(SNP = dat$SNP, beta = dat$beta.exposure, se = dat$se.exposure,
                       eaf = dat$eaf.exposure,
                       effect_allele = dat$effect_allele.exposure,
                       other_allele = dat$other_allele.exposure,
                       pval = dat$pval.exposure,
                       id = expo_name, exposure = expo_name, stringsAsFactors = FALSE)
  out_df <- data.frame(SNP = sub$rsid, beta = sub$beta, se = sub$sebeta, eaf = sub$af_alt,
                       effect_allele = sub$alt, other_allele = sub$ref, pval = sub$pval,
                       id = "I9_AVBLOCK", outcome = "Atrioventricular block (FinnGen R13)",
                       stringsAsFactors = FALSE)
  exp_f <- format_data(exp_df, type = "exposure")
  out_f <- format_data(out_df, type = "outcome")
  harm <- harmonise_data(exp_f, out_f, action = 2)
  harm <- harm[harm$mr_keep, ]
  if (nrow(harm) < 3) { cat(sprintf("%s: only %d SNPs after harmonise, skipped\n", expo_name, nrow(harm))); next }
  r <- mr(harm, method_list = c("mr_ivw", "mr_weighted_median", "mr_egger_regression"))
  r$exposure <- expo_name
  out_all[[expo_name]] <- as.data.frame(r)
  ivw <- r[r$method == "Inverse variance weighted", ]
  cat(sprintf("%-40s nsnp=%2d  IVW b=%+.4f (SE %.4f) P=%.3g\n",
              expo_name, ivw$nsnp, ivw$b, ivw$se, ivw$pval))
}
res <- rbindlist(out_all, fill = TRUE)
fwrite(res, file.path(res_dir, "mr_avblock_v46.csv"))
cat("saved results/mr_avblock_v46.csv\n")
