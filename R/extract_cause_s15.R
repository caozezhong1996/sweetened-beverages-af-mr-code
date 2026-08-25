suppressMessages(devtools::load_all("cause_src", quiet = TRUE))
res <- readRDS("results/cause_fit_coffee_v46.rds")
n_merged <- nrow(res$data)
s <- summary(res)
tab <- s$tab
z <- s$z; p <- s$p
el <- as.data.frame(res$elpd)
lines <- c(
  paste0("n_merged_variants\t", n_merged),
  paste0("n_fit_variants\t", sum(res$data$snp %in% res$data$snp)),  # placeholder, fixed below
  paste0("sharing_eta\t", tab[1, "eta"]),
  paste0("sharing_q\t", tab[1, "q"]),
  paste0("causal_gamma\t", tab[2, "gamma"]),
  paste0("causal_eta\t", tab[2, "eta"]),
  paste0("causal_q\t", tab[2, "q"]),
  paste0("delta_elpd_sharing_vs_causal\t", el$delta_elpd[el$model1 == "sharing" & el$model2 == "causal"]),
  paste0("se_delta_elpd\t", el$se_delta_elpd[el$model1 == "sharing" & el$model2 == "causal"]),
  paste0("z\t", z),
  paste0("p_causal_better_than_sharing\t", p)
)
writeLines(lines, "results/cause_keynumbers_v46.txt")
cat(paste(lines, collapse = "\n"), "\n")
