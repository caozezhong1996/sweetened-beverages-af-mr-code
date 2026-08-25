# run_v46_cause.R — CAUSE (Causal Analysis Using Summary Effect Estimates)
# Trait 1: coffee intake (Neale UKB 1498, LDSC-munged: SNP A1 A2 N Z)
# Trait 2: atrial fibrillation (Nielsen 2018, same LDSC-munged format)
#
# Both traits enter as Z-scores with seb = 1 (CAUSE z-score practice: the
# gamma/eta scales absorb the trait-specific constants; identical treatment
# of both traits keeps the sharing-vs-causal model comparison valid).
# Same munged inputs as the LDSC analysis (Table S10/S11, Figure S2).
#
# Formal install of CAUSE fails on this machine (Rscript segfault inside
# makeLazyLoadDB); devtools::load_all provides the identical package.

suppressMessages({
  devtools::load_all("cause_src", quiet = TRUE)
  library(dplyr)
  library(readr)
})

set.seed(20260824)

read_ldsc <- function(f, n_max = Inf) {
  read_tsv(f, col_types = cols(SNP = "c", A1 = "c", A2 = "c", N = "d", Z = "d"),
           n_max = n_max, progress = FALSE)
}

cat("reading exposures/outcome ...\n")
coffee <- read_ldsc("neale_ldsc/1498.ldsc.imputed_v3.both_sexes.tsv.bgz")
af     <- read_ldsc("results/ldsc_Nielsen2018.sumstats.gz")
cat("coffee variants:", nrow(coffee), " AF variants:", nrow(af), "\n")

coffee <- coffee %>% mutate(beta_hat = Z, seb = 1)
af     <- af %>% mutate(beta_hat = Z, seb = 1)

X <- gwas_merge(
  coffee, af,
  snp_name_cols = c("SNP", "SNP"),
  beta_hat_cols = c("beta_hat", "beta_hat"),
  se_cols       = c("seb", "seb"),
  A1_cols       = c("A1", "A1"),
  A2_cols       = c("A2", "A2")
)
cat("merged variants:", nrow(X), "\n")

# ---- nuisance parameters (cached) ----
if (file.exists("results/cause_params_v46.rds")) {
  params <- readRDS("results/cause_params_v46.rds")
  cat("params loaded from cache\n")
} else {
  n_par <- min(200000, nrow(X))
  cat("estimating nuisance parameters on", n_par, "sampled variants ...\n")
  t0 <- Sys.time()
  params <- est_cause_params(X, variants = sample(X$snp, n_par))
  cat("param estimation mins:", round(difftime(Sys.time(), t0, units = "mins"), 2), "\n")
  saveRDS(params, "results/cause_params_v46.rds")
}
print(params)

# ---- model fit: sharing vs causal ----
top <- X %>% filter(p1 < 1e-3) %>% arrange(p1)
if (nrow(top) > 5000) top <- top[seq_len(5000), ]
cat("variants entering CAUSE fit (exposure p < 1e-3):", nrow(top), "\n")

t0 <- Sys.time()
res <- cause(X = X, variants = top$snp, param_ests = params, force = TRUE)
cat("fit mins:", round(difftime(Sys.time(), t0, units = "mins"), 2), "\n")
saveRDS(res, "results/cause_fit_coffee_v46.rds")

s <- summary(res)
print(s)

# ---- extract key numbers ----
el <- as.data.frame(res$elpd)
print(el)
# CAUSE summary: compare causal vs sharing via ELPD z-test
out <- capture.output(print(s))
writeLines(out, "results/cause_summary_coffee_v46.txt")
write.csv(el, "results/cause_elpd_coffee_v46.csv", row.names = FALSE)

# causal-model posterior of gamma (causal effect of trait1 on trait2)
pm <- res$causal$posterior_means
pc <- tryCatch(res$causal$posterior_ci, error = function(e) NULL)
cat("causal model gamma posterior mean(s):\n"); print(pm)
if (!is.null(pc)) { cat("causal model gamma CI:\n"); print(pc) }
cat("DONE\n")
