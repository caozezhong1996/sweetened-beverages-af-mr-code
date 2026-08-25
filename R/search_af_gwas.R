#!/usr/bin/env Rscript
# v4 upgrade step 1: search OpenGWAS catalog for
#  (a) large-sample atrial fibrillation GWAS (target N >= 1M)
#  (b) alcohol intake frequency GWAS (positive lifestyle control exposure)
suppressMessages({library(ieugwasr); library(data.table)})
if (Sys.getenv("OPENGWAS_JWT") == "") stop("OPENGWAS_JWT not set")

root   <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
outdir <- file.path(root, "06_升级分析_v4/results")
dir.create(outdir, showWarnings = FALSE, recursive = TRUE)

cat("Downloading full OpenGWAS catalog (this can take a minute)...\n")
info <- as.data.table(ieugwasr::gwasinfo())
cat("Catalog datasets:", nrow(info), "\n")
fwrite(info, file.path(outdir, "gwasinfo_catalog_20260822.csv"))

cols <- intersect(c("id","trait","author","consortium","year","pmid","population",
                    "sample_size","ncase","ncontrol","nsnp","build","category","subcategory"),
                  names(info))

# (a) AF GWAS
af <- info[grepl("atrial fibrillation", trait, ignore.case = TRUE)]
setorder(af, -sample_size)
cat("\n=== AF GWAS by sample size (top 25) ===\n")
print(af[, ..cols][1:min(25, .N)])
fwrite(af[, ..cols], file.path(outdir, "search_af_gwas_sorted.csv"))

# (b) alcohol intake frequency GWAS (UKB-style exposure for positive control)
alc <- info[grepl("alcohol", trait, ignore.case = TRUE)]
setorder(alc, -sample_size)
cat("\n=== Alcohol-related GWAS by sample size (top 25) ===\n")
print(alc[, ..cols][1:min(25, .N)])
fwrite(alc[, ..cols], file.path(outdir, "search_alcohol_gwas_sorted.csv"))
cat("\nDONE\n")
