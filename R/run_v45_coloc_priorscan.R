#!/usr/bin/env Rscript
# v4.5.1: colocalization prior sensitivity (p12 scan) at the FTO locus,
# coffee intake (ukb-b-5237, OpenGWAS region saved in v4.2) vs AF
# (Nielsen 2018 local full stats; FinnGen R13 local full stats).
suppressMessages({library(data.table); library(coloc)})
root   <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
outdir <- file.path(root, "06_升级分析_v4/results")

coffee <- fread(file.path(outdir, "coloc_FTO_coffee_region_v42.csv"))
coffee <- coffee[!is.na(beta) & se > 0 & !is.na(rsid) & rsid != "" & !duplicated(rsid)]
cat("coffee FTO SNPs:", nrow(coffee), "\n")

## ---- Nielsen FTO region (local extract by rsid) ----
niel <- fread(file.path(outdir, "coloc_FTO_Nielsen_region_v45.tsv"))
niel[, rsid := tstrsplit(variant_id, ";", keep = 1)]
# some variant_ids carry several rsids; expand
niel <- niel[, .(rsid = unlist(strsplit(variant_id, ";")),
                 ea = rep(effect_allele,  lengths(strsplit(variant_id, ";"))),
                 nea = rep(other_allele,  lengths(strsplit(variant_id, ";"))),
                 beta = rep(beta,          lengths(strsplit(variant_id, ";"))),
                 se = rep(standard_error,  lengths(strsplit(variant_id, ";"))),
                 eaf = rep(effect_allele_frequency, lengths(strsplit(variant_id, ";"))))]
m <- merge(coffee, niel, by = "rsid", suffixes = c(".c", ".n"))
ok <- (m$ea.c == m$ea.n & m$nea.c == m$nea.n) | (m$ea.c == m$nea.n & m$nea.c == m$ea.n)
m <- m[ok]
flip <- m$ea.c == m$nea.n & m$nea.c == m$ea.n
m$beta.n[flip] <- -m$beta.n[flip]
m <- m[!is.na(m$beta.c) & !is.na(m$beta.n) & m$se.c > 0 & m$se.n > 0 & !duplicated(m$rsid)]
cat("FTO x Nielsen harmonized:", nrow(m), "\n")

ds_c  <- list(snp = m$rsid, beta = m$beta.c, varbeta = m$se.c^2,
              N = 428860, type = "quant", MAF = pmin(m$eaf.c, 1 - m$eaf.c))
ds_n  <- list(snp = m$rsid, beta = m$beta.n, varbeta = m$se.n^2,
              N = 1030836, type = "cc", s = 60620/1030836,
              MAF = pmin(m$eaf.n, 1 - m$eaf.n))

## ---- FinnGen R13 FTO region (local raw extract) ----
r13 <- fread(file.path(outdir, "coloc_FTO_R13_raw_v42.tsv"))
r13 <- r13[, .(rsid = unlist(strsplit(rsids, ","))),
           by = .(ref, alt, beta, sebeta, af_alt)]
m2 <- merge(coffee, r13, by = "rsid")
ok2 <- (m2$ea == m2$alt & m2$nea == m2$ref) | (m2$ea == m2$ref & m2$nea == m2$alt)
m2 <- m2[ok2]
flip2 <- m2$ea == m2$ref & m2$nea == m2$alt
m2$beta.y[flip2] <- -m2$beta.y[flip2]
m2 <- m2[m2$sebeta > 0 & !duplicated(m2$rsid)]
cat("FTO x R13 harmonized:", nrow(m2), "\n")

ds_r  <- list(snp = m2$rsid, beta = m2$beta.y, varbeta = m2$sebeta^2,
              N = 309052, type = "cc", s = 67783/309052,
              MAF = pmin(m2$af_alt, 1 - m2$af_alt))
ds_c2 <- list(snp = m2$rsid, beta = m2$beta.x, varbeta = m2$se^2,
              N = 428860, type = "quant", MAF = pmin(m2$eaf, 1 - m2$eaf))

## ---- p12 scan ----
p12_grid <- c(1e-6, 5e-6, 1e-5, 2.5e-5, 5e-5)
rows <- list()
for (p12 in p12_grid) {
  rn <- coloc.abf(dataset1 = ds_c, dataset2 = ds_n, p12 = p12)$summary
  rows[[length(rows)+1]] <- data.frame(locus = "FTO", outcome = "Nielsen 2018",
    p12 = p12, nsnp = rn["nsnps"], PP.H1 = rn["PP.H1.abf"], PP.H3 = rn["PP.H3.abf"], PP.H4 = rn["PP.H4.abf"])
  rr <- coloc.abf(dataset1 = ds_c2, dataset2 = ds_r, p12 = p12)$summary
  rows[[length(rows)+1]] <- data.frame(locus = "FTO", outcome = "FinnGen R13",
    p12 = p12, nsnp = rr["nsnps"], PP.H1 = rr["PP.H1.abf"], PP.H3 = rr["PP.H3.abf"], PP.H4 = rr["PP.H4.abf"])
}
out <- rbindlist(rows)
fwrite(out, file.path(outdir, "coloc_priorscan_v45.tsv"), sep = "\t")
print(out, digits = 4)
cat("PRIOR SCAN DONE\n")
