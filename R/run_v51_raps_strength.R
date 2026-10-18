# v5.1 - MR-RAPS (Nielsen 2018 + FinnGen R13) + instrument strength, rebuild S22/S23
# Change vs v5.0: FinnGen side now uses results/dat_*_finngen_R13.csv
# (v5.0 S23 "FinnGen R13" rows were computed from R12-era finn_b_I9_AF files and
#  had SNP counts inconsistent with the R13 harmonised data; this run fixes that.)
suppressMessages({library(data.table); library(mr.raps)})

base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
stab <- file.path(base, "supplement_tables")

exposures <- c("Artificial_sweetener_added_to_tea", "Coffee_intake", "Fizzy_drink_intake_SSB",
               "Low_calorie_drink_intake_ASB", "Sugar_added_to_coffee", "Sugar_added_to_tea", "Tea_intake")
labels <- c(Artificial_sweetener_added_to_tea = "Artificial sweetener added to tea",
            Coffee_intake = "Coffee intake",
            Fizzy_drink_intake_SSB = "Fizzy drink intake (SSB)",
            Low_calorie_drink_intake_ASB = "Low-calorie drink intake (ASB)",
            Sugar_added_to_coffee = "Sugar added to coffee",
            Sugar_added_to_tea = "Sugar added to tea",
            Tea_intake = "Tea intake")

load_dat <- function(e, src) {
  f <- file.path(base, "results", sprintf("dat_%s_%s.csv", e, src))
  if (!file.exists(f)) return(NULL)
  d <- fread(f)
  if ("mr_keep" %in% names(d)) d <- d[mr_keep == TRUE]
  d[complete.cases(d[, .(beta.exposure, se.exposure, beta.outcome, se.outcome)])]
}

run_raps <- function(d) {
  if (is.null(d) || nrow(d) < 3) return(list(b = NA_real_, se = NA_real_, p = NA_real_))
  fit <- tryCatch(
    mr.raps.mle(b_exp = d$beta.exposure, se_exp = d$se.exposure,
                b_out = d$beta.outcome, se_out = d$se.outcome,
                over.dispersion = TRUE, loss.function = "tukey"),
    error = function(e) NULL)
  if (is.null(fit)) return(list(b = NA_real_, se = NA_real_, p = NA_real_))
  list(b = fit$beta.hat, se = fit$beta.se, p = fit$beta.p.value)
}

s23 <- list(); s22 <- list()
for (e in exposures) {
  dn <- load_dat(e, "ebi_a_GCST006414")
  dr <- load_dat(e, "finngen_R13")
  for (dd in list(list(d = dn, nm = "Nielsen 2018"), list(d = dr, nm = "FinnGen R13"))) {
    if (is.null(dd$d)) { cat("MISSING:", e, dd$nm, "\n"); next }
    r <- run_raps(dd$d)
    s23[[length(s23) + 1]] <- data.table(
      Exposure = labels[[e]], Outcome = dd$nm, `SNPs (n)` = nrow(dd$d),
      `MR-RAPS log-OR` = round(r$b, 4), SE = round(r$se, 4), P = signif(r$p, 3))
    cat(sprintf("%-35s %-12s n=%3d  b=%8.4f  se=%7.4f  p=%.3g\n",
                labels[[e]], dd$nm, nrow(dd$d), r$b, r$se, r$p))
  }
  d <- dn
  r2 <- with(d[!is.na(eaf.exposure)], sum(2 * eaf.exposure * (1 - eaf.exposure) * beta.exposure^2)) * 100
  thr <- if (max(d$pval.exposure, na.rm = TRUE) > 5e-8) "P < 5 \u00d7 10\u207b\u2076" else "P < 5 \u00d7 10\u207b\u2078"
  s22[[length(s22) + 1]] <- data.table(
    Exposure = labels[[e]], Instrument_threshold = thr, SNPs_n = nrow(d),
    F_minimum = round(min(d$F_stat), 1), F_median = round(median(d$F_stat), 1),
    F_maximum = round(max(d$F_stat), 1), R2_pct = round(r2, 3))
}

S22 <- rbindlist(s22); S23 <- rbindlist(s23)
setnames(S22, c("Exposure", "Instrument threshold", "SNPs (n)", "F, minimum", "F, median",
                "F, maximum", "Cumulative R\u00b2 (%)"))
fwrite(S22, file.path(stab, "S22_instrument_strength.tsv"), sep = "\t")
fwrite(S23, file.path(stab, "S23_mrraps.tsv"), sep = "\t")
cat("\n=== S22 ===\n"); print(S22)
cat("written:", file.path(stab, "S22_instrument_strength.tsv"), "and S23_mrraps.tsv\n")
