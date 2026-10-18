# v5.1 conditional-F step 1: replicate mv_extract_exposures instrument selection
# (extract_instruments x3 -> joint clump), save clumped instrument set.
# Faithful to run_v4_mvmr.R parameters: pval 5e-8, clump r2 0.001, kb 10000, EUR.
suppressMessages({library(data.table); library(ieugwasr); library(TwoSampleMR)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
setwd(base)
expo_ids <- c("ukb-b-5237", "ukb-b-8442", "ieu-b-40")

with_retry <- function(f, n = 4, wait = 20) {
  for (i in seq_len(n)) {
    r <- tryCatch(f(), error = function(e) { message("attempt ", i, " failed: ", conditionMessage(e)); NULL })
    if (!is.null(r)) return(r)
    Sys.sleep(wait)
  }
  stop("all attempts failed")
}

exposure_dat <- with_retry(function() extract_instruments(expo_ids, p1 = 5e-8, r2 = 0.001, kb = 10000))
cat("per-exposure instruments (pre-joint-clump):\n"); print(table(exposure_dat$exposure)); flush.console()

temp <- exposure_dat
temp$id.exposure <- 1
temp <- temp[order(temp$pval.exposure, decreasing = FALSE), ]
temp <- subset(temp, !duplicated(SNP))
temp <- with_retry(function() clump_data(temp, clump_p1 = 5e-8, clump_r2 = 0.001, clump_kb = 10000, pop = "EUR"))
exposure_dat <- subset(exposure_dat, SNP %in% temp$SNP)

saveRDS(exposure_dat, "mvmr_instruments_v51.rds")
cat("joint instruments:", length(unique(exposure_dat$SNP)), "\n")
print(table(exposure_dat$exposure))
cat("Step1 DONE\n")
