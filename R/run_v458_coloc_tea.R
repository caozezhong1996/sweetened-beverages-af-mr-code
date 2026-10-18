#!/usr/bin/env Rscript
# v4.5.8: colocalization tea intake (ukb-b-6066) vs AF Nielsen 2018 (ebi-a-GCST006414)
# Same 500-kb windows as the coffee analysis: CYP1A1-CYP1A2 (chr15), AHR (chr7), FTO (chr16)
suppressMessages({library(data.table); library(ieugwasr); library(coloc)})
if (Sys.getenv("OPENGWAS_JWT") == "") stop("OPENGWAS_JWT not set")
root   <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
outdir <- file.path(root, "06_升级分析_v4/results")

regions <- list(
  list(name = "CYP1A1-CYP1A2", query = "15:74777880-75277880"),
  list(name = "AHR",           query = "7:17034577-17534577"),
  list(name = "FTO",           query = "16:53550954-54050954")
)

get_region <- function(id, q) {
  d <- tryCatch(associations(variants = q, id = id), error = function(e) { cat("ERR", id, q, ":", conditionMessage(e), "\n"); NULL })
  if (is.null(d) || nrow(d) == 0) return(NULL)
  as.data.frame(d)
}

rows <- list()
for (rg in regions) {
  cat("\n=== Region", rg$name, rg$query, "===\n")
  d1 <- get_region("ukb-b-6066", rg$query)        # tea
  Sys.sleep(1)
  d2 <- get_region("ebi-a-GCST006414", rg$query)  # AF Nielsen 2018
  if (is.null(d1) || is.null(d2)) { cat("  region data unavailable\n"); next }
  cat("  tea SNPs:", nrow(d1), "| AF SNPs:", nrow(d2), "\n")
  m <- merge(d1, d2, by = "rsid", suffixes = c(".tea", ".af"))
  ok <- (m$ea.tea == m$ea.af & m$nea.tea == m$nea.af) |
        (m$ea.tea == m$nea.af & m$nea.tea == m$ea.af)
  m <- m[ok, ]
  flip <- m$ea.tea == m$nea.af & m$nea.tea == m$ea.af
  m$beta.af[flip] <- -m$beta.af[flip]
  m <- m[!is.na(m$beta.tea) & !is.na(m$beta.af) & m$se.tea > 0 & m$se.af > 0, ]
  m <- m[!duplicated(m$rsid), ]
  cat("  merged SNPs:", nrow(m), "\n")
  if (nrow(m) < 50) { cat("  too few SNPs, skip\n"); next }

  ds1 <- list(snp = m$rsid, beta = m$beta.tea, varbeta = m$se.tea^2,
              N = 447485, type = "quant", MAF = pmin(m$eaf.tea, 1 - m$eaf.tea))
  ds2 <- list(snp = m$rsid, beta = m$beta.af, varbeta = m$se.af^2,
              N = 1030836, type = "cc", s = 60620/1030836)
  if (!all(is.na(m$eaf.af))) ds2$MAF <- pmin(m$eaf.af, 1 - m$eaf.af)

  res <- coloc.abf(dataset1 = ds1, dataset2 = ds2)
  pp <- res$summary
  cat(sprintf("  PP.H0=%.3g H1=%.3f H2=%.3g H3=%.3f H4=%.3f (nsnp=%d)\n",
      pp["PP.H0.abf"], pp["PP.H1.abf"], pp["PP.H2.abf"], pp["PP.H3.abf"], pp["PP.H4.abf"], pp["nsnps"]))
  rows[[length(rows)+1]] <- data.frame(
    region = rg$name, nsnp = pp["nsnps"],
    PP.H0 = pp["PP.H0.abf"], PP.H1 = pp["PP.H1.abf"], PP.H2 = pp["PP.H2.abf"],
    PP.H3 = pp["PP.H3.abf"], PP.H4 = pp["PP.H4.abf"])
  Sys.sleep(1)
}

if (length(rows)) {
  out <- rbindlist(rows)
  fwrite(out, file.path(outdir, "upgrade_coloc_tea_loci_Nielsen.csv"))
  print(out)
}
cat("COLOC TEA DONE\n")
