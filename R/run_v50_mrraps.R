# v5.0 (PB3) - MR-RAPS for all exposures x Nielsen 2018 + FinnGen R13
# Reviewer 1.2: supplementary robust estimator for relaxed-threshold exposures.
suppressMessages({library(data.table); library(mr.raps)})

base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
out <- "C:/Users/64915/Desktop/EHJOpen投稿包_奶茶房颤MR_v5.0_20261006/06_新增分析_B级"

args <- commandArgs(trailingOnly = TRUE)
tag <- if (length(args) >= 1) args[1] else "run1"

exposures <- c("Artificial_sweetener_added_to_tea", "Coffee_intake", "Fizzy_drink_intake_SSB",
               "Low_calorie_drink_intake_ASB", "Sugar_added_to_coffee", "Sugar_added_to_tea", "Tea_intake")

run_pair <- function(dat) {
  k <- complete.cases(dat$beta.exposure, dat$se.exposure, dat$beta.outcome, dat$se.outcome)
  d <- dat[k, ]
  if (nrow(d) < 3) return(list(nsnp = nrow(d), b = NA, se = NA, p = NA, note = "too few SNPs"))
  fit <- tryCatch(
    mr.raps.mle(b_exp = d$beta.exposure, se_exp = d$se.exposure,
            b_out = d$beta.outcome, se_out = d$se.outcome,
            over.dispersion = TRUE, loss.function = "tukey"),
    error = function(e) NULL)
  if (is.null(fit)) return(list(nsnp = nrow(d), b = NA, se = NA, p = NA, note = "fit failed"))
  list(nsnp = nrow(d), b = fit$beta.hat, se = fit$beta.se, p = fit$beta.p.value, note = "")
}

rows <- list()
src_map <- c("GCST006414" = "Nielsen2018", "finn_b_I9_AF" = "FinnGenR13")
for (e in exposures) {
  for (sid in names(src_map)) {
    src <- src_map[[sid]]
    if (sid == "GCST006414") {
      f <- file.path(out, "mrraps_input", sprintf("dat_%s_ebi_a_%s.csv", e, sid))
    } else {
      f <- file.path("C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/03_结果数据_mr_results",
                     sprintf("dat_%s_finn_b_I9_AF.csv", e))
    }
    if (!file.exists(f)) { rows[[length(rows)+1]] <- list(exposure = e, outcome = src, note = "file missing"); next }
    dat <- fread(f)
    r <- run_pair(dat)
    rows[[length(rows)+1]] <- list(exposure = e, outcome = src, nsnp = r$nsnp,
                                   b_raps = round(r$b, 4), se_raps = round(r$se, 4),
                                   p_raps = signif(r$p, 3), note = r$note)
    cat(sprintf("%s x %s: n=%d b=%.4f se=%.4f p=%.3g %s\n", e, src, r$nsnp, r$b, r$se, r$p, r$note))
  }
}

df <- rbindlist(rows, fill = TRUE)
fwrite(df, file.path(out, sprintf("MR_RAPS_v50_%s.csv", tag)))
cat("written:", file.path(out, sprintf("MR_RAPS_v50_%s.csv", tag)), "\n")
