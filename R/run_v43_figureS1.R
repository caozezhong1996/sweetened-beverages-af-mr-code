#!/usr/bin/env Rscript
# v4.3 E2: Figure S1 — leave-one-out + funnel plots for all exposures with any
# nominal IVW signal in current sources:
#   coffee x Nielsen 2018, coffee x FinnGen R13, sugar added to tea x FinnGen R13,
#   sugar added to coffee x AFGen 2018 (legacy signal).
suppressMessages({library(data.table); library(TwoSampleMR); library(ggplot2); library(patchwork)})
root <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
NEW  <- file.path(root, "06_升级分析_v4/results")
OLD  <- file.path(root, "03_结果数据_mr_results")

combos <- list(
  list(f = file.path(NEW, "dat_Coffee_intake_ebi_a_GCST006414.csv"),        lab = "Coffee intake ~ Nielsen 2018 (EUR, primary)"),
  list(f = file.path(NEW, "dat_Coffee_intake_finngen_R13.csv"),             lab = "Coffee intake ~ FinnGen R13 (EUR)"),
  list(f = file.path(NEW, "dat_Sugar_added_to_tea_finngen_R13.csv"),        lab = "Sugar added to tea ~ FinnGen R13 (EUR)"),
  list(f = file.path(OLD, "dat_Sugar_added_to_coffee_ebi_a_GCST006061.csv"), lab = "Sugar added to coffee ~ AFGen 2018 (legacy signal)")
)

loo_plot <- function(d, lab) {
  l <- mr_leaveoneout(d)
  l <- l[l$SNP != "All", ]
  a <- mr_leaveoneout(d); all <- a[a$SNP == "All", ]
  ggplot(l, aes(y = reorder(SNP, b), x = b)) +
    geom_errorbarh(aes(xmin = b - 1.96 * se, xmax = b + 1.96 * se), height = 0, linewidth = 0.3) +
    geom_point(size = 0.7) +
    geom_errorbarh(data = all, aes(xmin = b - 1.96 * se, xmax = b + 1.96 * se, y = "ALL"),
                   height = 0, color = "#B33A3A", inherit.aes = FALSE) +
    geom_point(data = all, aes(x = b, y = "ALL"), color = "#B33A3A", size = 1.6, inherit.aes = FALSE) +
    geom_vline(xintercept = 0, linetype = "dashed", color = "grey50", linewidth = 0.4) +
    labs(title = lab, x = "Leave-one-out IVW beta (log OR)", y = NULL) +
    theme_bw(base_size = 7) + theme(plot.title = element_text(size = 8, face = "bold"))
}

funnel_plot <- function(d, lab) {
  s <- mr_singlesnp(d)
  s <- s[!grepl("All", s$SNP), ]
  s$precision <- 1 / s$se
  ivw <- mr(d, method_list = "mr_ivw")
  ggplot(s, aes(x = b, y = precision)) +
    geom_point(size = 0.8, alpha = 0.7) +
    geom_vline(xintercept = ivw$b, color = "#B33A3A", linewidth = 0.5) +
    geom_vline(xintercept = 0, linetype = "dashed", color = "grey50", linewidth = 0.4) +
    labs(title = lab, x = "Per-SNP Wald ratio (log OR)", y = "Precision (1/SE)") +
    theme_bw(base_size = 7) + theme(plot.title = element_text(size = 8, face = "bold"))
}

plots <- list()
for (cmb in combos) {
  d <- as.data.frame(fread(cmb$f))
  d <- d[d$mr_keep == TRUE, ]
  plots[[length(plots) + 1]] <- loo_plot(d, paste0(cmb$lab, " — leave-one-out"))
  plots[[length(plots) + 1]] <- funnel_plot(d, paste0(cmb$lab, " — funnel"))
}
p <- wrap_plots(plots, ncol = 2, byrow = TRUE)
out <- file.path(root, "06_升级分析_v4/figures/FigureS1_LOO_Funnel_v43_300dpi.png")
ggsave(out, p, width = 11, height = 13, dpi = 300)
cat("saved:", out, "\n")
