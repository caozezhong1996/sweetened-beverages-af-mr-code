#!/usr/bin/env Rscript
# run_v52_biomarker_stepA_clump.R — LD-clump Chen 2023 metabolite tophits (OpenGWAS ld/clump, EUR, r2<0.001, kb=10000)
root <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
Sys.setenv(OPENGWAS_JWT = readLines(file.path(root, "OPENGWAS_JWT.txt"), warn = FALSE)[1])
suppressMessages({library(data.table); library(ieugwasr)})
outdir <- file.path(root, "06_升级分析_v4/results")

for (tag in c("caffeine", "paraxanthine", "theobromine")) {
  d <- fread(file.path(outdir, paste0("biomarker_tophits_", tag, ".tsv")))
  cl <- tryCatch(
    ld_clump(dat = dplyr::tibble(rsid = d$rsid, pval = d$p, id = tag),
             clump_r2 = 0.001, clump_kb = 10000, pop = "EUR"),
    error = function(e) { cat(tag, "ld_clump ERR:", conditionMessage(e), "\n"); NULL })
  if (is.null(cl)) next
  keep <- d[rsid %in% cl$rsid]
  keep[, fstat := (beta / se)^2]
  fwrite(keep, file.path(outdir, paste0("biomarker_instruments_", tag, ".tsv")), sep = "\t")
  cat(sprintf("%s: %d hits -> %d independent instruments (F %.1f-%.1f)\n",
              tag, nrow(d), nrow(keep), min(keep$fstat), max(keep$fstat)))
}
