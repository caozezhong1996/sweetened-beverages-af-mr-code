# v4.5.4 Task A - Neale Lab UKB 1498 (coffee) -> Nielsen 2018 AF sensitivity MR
# Independent exposure GWAS replication of the main coffee IVW (ukb-b-5237, OR 1.26, P=0.036)
suppressMessages({library(data.table); library(TwoSampleMR)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
dl <- file.path(base, "downloads"); res_dir <- file.path(base, "results")

## ---- 1. Neale 1498 pruned instruments (P<5e-8, low_conf==false, +/-1Mb window)
iv <- fread(file.path(dl, "neale1498_instruments_pruned.tsv"))
iv[, ea_alt := alt]  # Neale beta is w.r.t. ALT allele (validated below by sign concordance)

## ---- 2. Nielsen AF rows matched by chr:pos
af <- fread(file.path(dl, "tmp_nielsen_neale1498.tsv"))
# NOTE: first header label pair is swapped: col rs_dbsnp147 holds chr:pos_ref/alt
parts <- tstrsplit(af$rs_dbsnp147, "[:_]")
af[, `:=`(chr = as.integer(parts[[1]]), pos = as.integer(parts[[2]]))]
key_iv <- paste(iv$chr, iv$pos); key_af <- paste(af$chr, af$pos)
iv <- iv[key_iv %in% key_af]; af <- af[key_af %in% key_iv]
cat(sprintf("Instruments with Nielsen match: %d\n", nrow(iv)))

## ---- 3. Manual harmonization: align Nielsen beta to Neale ALT allele
m <- merge(iv, af, by = c("chr", "pos"), suffixes = c(".x", ".n"))
m[, `:=`(nea_ea = toupper(effect_allele), nea_oa = toupper(other_allele))]
harm <- m[(ea_alt == nea_ea & ref == nea_oa) | (ea_alt == nea_oa & ref == nea_ea)]
harm[, b_out := ifelse(ea_alt == nea_ea, beta.n, -beta.n)]  # beta.x=Neale, beta.n=Nielsen
harm[, se_out := standard_error]
cat(sprintf("Allele-matched instruments: %d (dropped %d allele-mismatch)\n",
            nrow(harm), nrow(m) - nrow(harm)))
pal <- (paste0(harm$ref, harm$alt) %in% c("AT","TA","CG","GC"))
cat(sprintf("Palindromic instruments kept on exact plus-strand ref/alt match: %d\n", sum(pal)))

## ---- 4. Build TwoSampleMR frames (outcome pre-aligned: EA = exposure EA)
mk_id <- function(c, p, a1, a2) paste0(c, ":", p, "_", a1, "/", a2)
exp_df <- data.frame(
  SNP = mk_id(harm$chr, harm$pos, harm$ref, harm$alt),
  beta = harm$beta.x, se = harm$se, eaf = harm$minor_AF,
  effect_allele = harm$alt, other_allele = harm$ref,
  pval = harm$pval, samplesize = harm$n,
  id = "Neale1498", exposure = "Coffee intake (Neale 1498)", stringsAsFactors = FALSE)
out_df <- data.frame(
  SNP = exp_df$SNP,
  beta = harm$b_out, se = harm$se_out, eaf = NA_real_,
  effect_allele = harm$alt, other_allele = harm$ref,
  pval = harm$p_value, samplesize = 1030836,
  id = "Nielsen2018", outcome = "Atrial fibrillation (Nielsen 2018)", stringsAsFactors = FALSE)
exp_f <- format_data(exp_df, type = "exposure")
out_f <- format_data(out_df, type = "outcome")
dat <- harmonise_data(exp_f, out_f, action = 1)
dat <- dat[dat$mr_keep, ]
cat(sprintf("Harmonised mr_keep SNPs: %d\n", nrow(dat)))
fwrite(dat, file.path(res_dir, "dat_Neale1498_nielsen_v47.csv"))

## ---- 5. MR
mr_res <- mr(dat, method_list = c("mr_ivw", "mr_egger_regression",
                                  "mr_weighted_median", "mr_weighted_mode"))
het <- mr_heterogeneity(dat)
ple <- mr_pleiotropy_test(dat)
fwrite(as.data.frame(mr_res), file.path(res_dir, "mr_neale1498_nielsen_v47.csv"))
fwrite(as.data.frame(het), file.path(res_dir, "het_neale1498_nielsen_v47.csv"))
fwrite(as.data.frame(ple), file.path(res_dir, "pleio_neale1498_nielsen_v47.csv"))

## robustness: IVW without palindromic SNPs
np <- dat[!paste0(dat$other_allele.exposure, dat$effect_allele.exposure) %in%
          c("AT","TA","CG","GC"), ]
if (nrow(np) >= 3) {
  mr_np <- mr(np, method_list = c("mr_ivw", "mr_weighted_median"))
  fwrite(as.data.frame(mr_np), file.path(res_dir, "mr_neale1498_nielsen_nopal_v47.csv"))
} else mr_np <- NULL

## ---- 6. Overlap & sign concordance vs main 34 instruments (ukb-b-5237)
main <- fread(file.path(res_dir, "dat_Coffee_intake_ebi_a_GCST006414.csv"))
conc <- 0; ncomp <- 0; loci <- 0
for (i in seq_len(nrow(harm))) {
  j <- which(main$chr == harm$chr[i] & abs(main$pos - harm$pos[i]) <= 1000000)
  if (length(j) > 0) {
    loci <- loci + 1
    jj <- j[1]
    ea_main <- toupper(main$effect_allele.exposure[jj]); oa_main <- toupper(main$other_allele.exposure[jj])
    if (harm$alt[i] == ea_main && harm$ref[i] == oa_main) {
      ncomp <- ncomp + 1; if (sign(harm$beta.x[i]) == sign(main$beta.exposure[jj])) conc <- conc + 1
    } else if (harm$alt[i] == oa_main && harm$ref[i] == ea_main) {
      ncomp <- ncomp + 1; if (sign(-harm$beta.x[i]) == sign(main$beta.exposure[jj])) conc <- conc + 1
    }
  }
}
cat(sprintf("Locus overlap with main 34: %d/%d; sign-concordant (alleles matched): %d/%d\n",
            loci, nrow(harm), conc, ncomp))

## ---- 7. F stats
Fstat <- (harm$beta.x / harm$se)^2

## ---- 8. Summary
ivw <- mr_res[mr_res$method == "Inverse variance weighted", ]
sink(file.path(res_dir, "neale1498_summary_v47.txt"))
cat("v4.5.4 Task A: Neale 1498 (coffee) -> Nielsen 2018 AF\n")
cat(sprintf("Pruned instruments (P<5e-8, +/-1Mb): %d; allele-matched in Nielsen: %d (palindromic kept: %d)\n",
            nrow(iv), nrow(harm), sum(pal)))
cat(sprintf("F stats: min %.1f, median %.1f\n", min(Fstat), median(Fstat)))
cat(sprintf("Locus overlap with main 34-SNP set: %d/%d; sign concordance: %d/%d\n",
            loci, nrow(harm), conc, ncomp))
print(as.data.frame(mr_res)[, c("method", "nsnp", "b", "se", "pval")])
cat(sprintf("IVW OR=%.3f (95%%CI %.3f-%.3f), P=%.4g\n",
            exp(ivw$b), exp(ivw$b - 1.96 * ivw$se), exp(ivw$b + 1.96 * ivw$se), ivw$pval))
if (!is.null(mr_np)) { cat("\nNo-palindrome robustness:\n"); print(as.data.frame(mr_np)[, c("method","nsnp","b","se","pval")]) }
cat("\nHeterogeneity:\n"); print(as.data.frame(het))
cat("\nEgger intercept:\n"); print(as.data.frame(ple))
sink()
cat("Task A done.\n")
