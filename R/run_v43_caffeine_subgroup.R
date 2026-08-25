#!/usr/bin/env Rscript
# v4.3 E1: caffeine-pathway-restricted subgroup MR for coffee intake.
# Split the 34 coffee instruments into SNPs inside the caffeine-metabolism
# windows (AHR chr7:17,034,577-17,534,577; CYP1A1-CYP1A2 chr15:74,777,880-75,277,880)
# vs all remaining instruments; IVW per subgroup vs Nielsen 2018 and FinnGen R13.
suppressMessages({library(data.table); library(TwoSampleMR)})
outdir <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4/results"

in_window <- function(chr, pos) {
  (chr == 7  & pos >= 17034577 & pos <= 17534577) |
  (chr == 15 & pos >= 74777880 & pos <= 75277880)
}

caf_rsids <- c("rs117968677", "rs2472297", "rs4410790")  # tagged from Nielsen positions (hg19 windows); identical instrument list in both sources

rows <- list()
for (oc in c("ebi_a_GCST006414", "finngen_R13")) {
  d <- as.data.frame(fread(file.path(outdir, paste0("dat_Coffee_intake_", oc, ".csv"))))
  d <- d[d$mr_keep == TRUE, ]
  d$caf <- d$SNP %in% caf_rsids
  cat(oc, ": caffeine-window SNPs =", sum(d$caf), " of ", nrow(d), "\n")
  print(d[d$caf, intersect(c("SNP", "chr", "pos", "beta.exposure", "beta.outcome", "se.outcome"), names(d))])
  for (grp in c(TRUE, FALSE)) {
    s <- d[d$caf == grp, ]
    if (nrow(s) < 2) next
    r <- mr(s, method_list = c("mr_ivw", "mr_wald_ratio", "mr_weighted_median"))
    r <- r[r$method %in% c("Inverse variance weighted", "Wald ratio", "Weighted median"), ]
    for (i in seq_len(nrow(r))) {
      rows[[length(rows) + 1]] <- data.frame(
        outcome_source = oc,
        subgroup = ifelse(grp, "Caffeine-metabolism loci (AHR + CYP1A1-CYP1A2 windows)", "All other coffee instruments"),
        method = r$method[i], nsnp = r$nsnp[i], b = r$b[i], se = r$se[i], pval = r$pval[i])
    }
  }
}
out <- rbindlist(rows)
out$OR <- sprintf("%.2f (%.2f-%.2f)", exp(out$b), exp(out$b - 1.96 * out$se), exp(out$b + 1.96 * out$se))
fwrite(out, file.path(outdir, "upgrade_v43_caffeine_subgroup_mr.csv"))
print(out[, .(outcome_source, subgroup, method, nsnp, OR, pval)])
cat("SUBGROUP MR DONE\n")
