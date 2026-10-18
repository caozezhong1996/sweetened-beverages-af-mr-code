#!/usr/bin/env Rscript
# run_v52_biomarker_mr.R — biomarker MR: Chen2023 caffeine/paraxanthine/theobromine vs Nielsen2018 + FinnGen R13
root <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
suppressMessages({library(data.table); library(TwoSampleMR)})
outdir <- file.path(root, "06_升级分析_v4/results")

N_EXP <- c(caffeine = 8005, paraxanthine = 7840, theobromine = 8137)
N_NIE <- 1030836; N_FG <- 309052

outcomes <- list(
  nielsen = list(file = "biomarker_outcome_nielsen.tsv", name = "AF (Nielsen 2018)", id = "GCST006061", N = N_NIE),
  finngen = list(file = "biomarker_outcome_finngen.tsv", name = "AF (FinnGen R13)", id = "finngen_R13_I9_AF", N = N_FG)
)

run_pair <- function(tag, okey) {
  oc <- outcomes[[okey]]
  e <- fread(file.path(outdir, paste0("biomarker_tophits_", tag, ".tsv")))
  o <- fread(file.path(outdir, oc$file))
  m <- merge(e, o, by = "rsid", suffixes = c(".e", ".o"))
  if (!nrow(m)) { cat(sprintf("%s x %s: no overlap\n", tag, okey)); return(NULL) }
  m[, locus := paste(chr.e, pos.e %/% 1e7, sep = ":")]           # 10 Mb locus window (exposure coords)
  setorder(m, p.e)
  inst <- m[, .SD[1], by = locus]                                 # per-locus min-p present SNP
  inst[, fstat := (beta.e / se.e)^2]
  cat(sprintf("%-12s x %-8s: %d/%d loci covered, F %.0f-%.0f\n",
              tag, okey, nrow(inst), uniqueN(m$locus), min(inst$fstat), max(inst$fstat)))

  exp_dat <- data.frame(SNP = inst$rsid, beta.exposure = inst$beta.e, se.exposure = inst$se.e,
                        effect_allele.exposure = toupper(inst$ea.e), other_allele.exposure = toupper(inst$oa.e),
                        eaf.exposure = inst$eaf.e, pval.exposure = inst$p.e,
                        samplesize.exposure = N_EXP[tag], exposure = paste0("Plasma ", tag, " (Chen 2023)"),
                        id.exposure = tag, stringsAsFactors = FALSE)
  out_dat <- data.frame(SNP = inst$rsid, beta.outcome = inst$beta.o, se.outcome = inst$se.o,
                        effect_allele.outcome = toupper(inst$ea.o), other_allele.outcome = toupper(inst$oa.o),
                        eaf.outcome = inst$eaf.o, pval.outcome = inst$p.o,
                        samplesize.outcome = oc$N, outcome = oc$name, id.outcome = oc$id,
                        stringsAsFactors = FALSE)
  dat <- harmonise_data(exp_dat, out_dat, action = 2)
  dat <- dat[dat$mr_keep, ]
  cat("   after harmonisation:", nrow(dat), "SNPs\n")
  if (!nrow(dat)) return(NULL)
  methods <- if (nrow(dat) >= 3) c("mr_ivw","mr_egger_regression","mr_weighted_median","mr_weighted_mode")
             else if (nrow(dat) == 2) "mr_ivw" else "mr_wald_ratio"
  res <- mr(dat, method_list = methods)
  het <- tryCatch(mr_heterogeneity(dat), error = function(e) NULL)
  ple <- tryCatch(mr_pleiotropy_test(dat), error = function(e) NULL)
  tagf <- paste0("biomarker_", tag)
  fwrite(as.data.table(dat), file.path(outdir, paste0("dat_", tagf, "_", okey, ".csv")))
  fwrite(res,  file.path(outdir, paste0("mr_", tagf, "_", okey, ".csv")))
  if (!is.null(het)) fwrite(het, file.path(outdir, paste0("het_", tagf, "_", okey, ".csv")))
  if (!is.null(ple)) fwrite(ple, file.path(outdir, paste0("pleio_", tagf, "_", okey, ".csv")))
  main <- res[res$method %in% c("Inverse variance weighted", "Wald ratio"), ][1, ]
  cat(sprintf("   %s: OR=%.3f (%.3f-%.3f), P=%.3g, nsnp=%d\n", main$method,
              exp(main$b), exp(main$b - 1.96*main$se), exp(main$b + 1.96*main$se), main$pval, main$nsnp))
  return(list(main = main, nsnp = nrow(dat)))
}

meta_rows <- list()
for (tag in c("caffeine", "paraxanthine", "theobromine")) {
  rn <- run_pair(tag, "nielsen")
  rf <- run_pair(tag, "finngen")
  if (!is.null(rn) && !is.null(rf)) {
    b1 <- rn$main$b; s1 <- rn$main$se; b2 <- rf$main$b; s2 <- rf$main$se
    w1 <- 1/s1^2; w2 <- 1/s2^2
    mb <- (b1*w1 + b2*w2)/(w1+w2); mse <- sqrt(1/(w1+w2))
    mp <- 2*pnorm(-abs(mb/mse))
    cat(sprintf("   EUR meta: OR=%.3f (%.3f-%.3f), P=%.3g\n",
                exp(mb), exp(mb-1.96*mse), exp(mb+1.96*mse), mp))
    meta_rows[[tag]] <- data.frame(exposure = tag, b = mb, se = mse, p = mp,
                                   or = exp(mb), lo = exp(mb-1.96*mse), hi = exp(mb+1.96*mse))
  }
}
if (length(meta_rows)) fwrite(rbindlist(meta_rows), file.path(outdir, "biomarker_meta_summary.csv"))
