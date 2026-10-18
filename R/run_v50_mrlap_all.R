# v5.0 (PB2) - MRlap: all 5 exposures with full summary statistics x 2 outcomes
# Template: run_v46_mrlap.R. Runs with two different seeds for reproducibility check.
suppressMessages({library(data.table); library(devtools)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
setwd(base)
outdir <- file.path(base, "mrlap_run_v50")
dir.create(outdir, showWarnings = FALSE)

args <- commandArgs(trailingOnly = TRUE)
seed <- if (length(args) >= 1) as.integer(args[1]) else 42L
tag <- if (length(args) >= 2) args[2] else "run1"

cat("loading LD score chr/pos...\n")
ld <- rbindlist(lapply(1:22, function(cc)
  fread(sprintf("ld_ref/eur_w_ld_chr/%d.l2.ldscore.gz", cc), select = c("CHR","SNP","BP"))))

prep <- function(path) {
  d <- fread(path)
  d2 <- merge(d, ld, by = "SNP")
  data.frame(rsid = d2$SNP, chr = d2$CHR, pos = d2$BP,
             a1 = d2$A1, a2 = d2$A2, z = d2$Z, N = d2$N)
}

exposures <- c(
  Coffee        = "neale_ldsc/1498.ldsc.imputed_v3.both_sexes.tsv.bgz",
  Tea           = "neale_ldsc/1488_raw.ldsc.imputed_v3.both_sexes.tsv.bgz",
  Neale100370   = "neale_ldsc/100370.ldsc.imputed_v3.both_sexes.tsv.bgz",
  Neale100170   = "neale_ldsc/100170.ldsc.imputed_v3.both_sexes.tsv.bgz",
  Neale100160   = "neale_ldsc/100160.ldsc.imputed_v3.both_sexes.tsv.bgz"
)
outcomes <- c(
  Nielsen2018 = "results/ldsc_Nielsen2018.sumstats.gz",
  FinnGenR13  = "results/ldsc_FinnGenR13.sumstats.gz"
)

devtools::load_all("genomicsem_src", quiet = TRUE)
devtools::load_all("mrlap_src", quiet = TRUE)
cat("packages loaded\n")

res_all <- list()
for (ename in names(exposures)) {
  edf <- prep(exposures[[ename]])
  for (oname in names(outcomes)) {
    odf <- prep(outcomes[[oname]])
    set.seed(seed)
    key <- paste0(ename, "__", oname)
    cat(sprintf("\n>>> MRlap %s vs %s (seed %d)\n", ename, oname, seed))
    flush.console()
    tryCatch({
      res <- MRlap(exposure = edf, exposure_name = ename,
                   outcome = odf, outcome_name = oname,
                   ld = normalizePath(file.path(base, "ld_ref/eur_w_ld_chr")),
                   hm3 = normalizePath(file.path(base, "ld_ref/eur_w_ld_chr/w_hm3.snplist")),
                   MR_pruning_LD = 0,
                   save_logfiles = FALSE, verbose = FALSE)
      mr <- res$MRcorrection
      line <- sprintf("%s,%d,%d,%.5f,%.5f,%.3g,%.5f,%.5f,%.3g,%.5f,%.3g",
                      key, mr$m_IVs, NA,
                      mr$observed_effect, mr$observed_effect_se, mr$observed_effect_p,
                      mr$corrected_effect, mr$corrected_effect_se, mr$corrected_effect_p,
                      mr$test_difference, mr$p_difference)
      res_all[[key]] <- line
      cat("    ", line, "\n")
    }, error = function(e) {
      res_all[[key]] <<- paste0(key, ",ERROR,", conditionMessage(e))
      cat("    ERROR:", conditionMessage(e), "\n")
    })
  }
}

csv <- file.path(outdir, sprintf("mrlap_v50_%s_seed%d.csv", tag, seed))
hdr <- "pair,m_IVs,fill,obs,obs_se,obs_p,corr,corr_se,corr_p,diff,diff_p"
writeLines(c(hdr, unlist(res_all)), csv)
cat("\nwritten:", csv, "\n")
