#!/usr/bin/env Rscript
# v4.5.8 offline: coloc tea intake (Neale 1488, Z-derived) vs AF Nielsen 2018 (local full stats)
suppressMessages({library(data.table); library(coloc)})
root <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4/results"

regions <- c("CYP1A1-CYP1A2", "AHR", "FTO")
rows <- list()
for (rg in regions) {
  m <- fread(file.path(root, sprintf("tea_coloc_merged_%s.tsv", rg)))
  m <- m[!is.na(beta_tea) & !is.na(beta_af) & se_af > 0 & var_tea > 0]
  cat("\n=== ", rg, " merged SNPs:", nrow(m), "===\n")
  if (nrow(m) < 50) { cat("  too few, skip\n"); next }
  ds1 <- list(snp = m$rsid, beta = m$beta_tea, varbeta = m$var_tea,
              N = as.integer(median(m$n)), type = "quant", sdY = 1)
  ds2 <- list(snp = m$rsid, beta = m$beta_af, varbeta = m$se_af^2,
              N = 1030836, type = "cc", s = 60620/1030836)
  eaf <- suppressWarnings(as.numeric(m$eaf_af))
  if (!all(is.na(eaf))) ds2$MAF <- pmin(eaf, 1 - eaf)
  res <- coloc.abf(dataset1 = ds1, dataset2 = ds2)
  pp <- res$summary
  cat(sprintf("  PP.H0=%.3g H1=%.3f H2=%.3g H3=%.3f H4=%.3f (nsnp=%d)\n",
      pp["PP.H0.abf"], pp["PP.H1.abf"], pp["PP.H2.abf"], pp["PP.H3.abf"], pp["PP.H4.abf"], pp["nsnps"]))
  rows[[rg]] <- data.frame(region = rg, nsnp = pp["nsnps"],
    PP.H0 = pp["PP.H0.abf"], PP.H1 = pp["PP.H1.abf"], PP.H2 = pp["PP.H2.abf"],
    PP.H3 = pp["PP.H3.abf"], PP.H4 = pp["PP.H4.abf"])
}
if (length(rows)) {
  out <- rbindlist(rows)
  fwrite(out, file.path(root, "upgrade_coloc_tea_loci_Nielsen.csv"))
  print(out)
}
cat("COLOC TEA DONE\n")
