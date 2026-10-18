# v5.1 conditional-F step 2: per-GWAS extraction of the joint instrument SNPs.
# Usage: Rscript run_v51_condF_s2.R <gwas_id>
# Called once per exposure id and once for the outcome (ebi-a-GCST006414).
suppressMessages({library(data.table); library(ieugwasr); library(TwoSampleMR)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
setwd(base)
args <- commandArgs(trailingOnly = TRUE)
id <- args[1]

with_retry <- function(f, n = 4, wait = 20) {
  for (i in seq_len(n)) {
    r <- tryCatch(f(), error = function(e) { message("attempt ", i, " failed: ", conditionMessage(e)); NULL })
    if (!is.null(r)) return(r)
    Sys.sleep(wait)
  }
  stop("all attempts failed for ", id)
}

exposure_dat <- readRDS("mvmr_instruments_v51.rds")
snps <- unique(exposure_dat$SNP)
cat("extracting", length(snps), "SNPs from", id, "...\n"); flush.console()
od <- with_retry(function() extract_outcome_data(snps, id, proxies = TRUE))
tag <- gsub("[^A-Za-z0-9]", "_", id)
saveRDS(od, sprintf("mvmr_od_%s_v51.rds", tag))
cat("saved", sprintf("mvmr_od_%s_v51.rds", tag), "rows:", nrow(od), "\n")
