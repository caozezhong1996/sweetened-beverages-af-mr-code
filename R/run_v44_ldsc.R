#!/usr/bin/env Rscript
# =============================================================================
# v4.4 / E3: Cross-trait LD score regression (Bulik-Sullivan 2015), R re-impl.
# LD scores: 1000G EUR HM3 eur_w_ld_chr (Zenodo 8182036 copy of Alkes Group).
# Two-step WLS; 200-block jackknife via block sufficient statistics (fast).
# =============================================================================
suppressMessages(library(data.table))
setwd("C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4")
NB <- 200

ld <- rbindlist(lapply(1:22, function(ch)
  fread(sprintf("ld_ref/eur_w_ld_chr/%d.l2.ldscore.gz", ch))))
setnames(ld, c("CHR","SNP","BP","CM","MAF","L2"))
ld <- ld[!duplicated(SNP)][L2 > 0]
M <- nrow(ld)
cat("LD-score SNPs (M):", M, "\n")

traits <- list(
  coffee   = "neale_ldsc/1498.ldsc.imputed_v3.both_sexes.tsv.bgz",
  tea      = "neale_ldsc/1488_raw.ldsc.imputed_v3.both_sexes.tsv.bgz",
  sugarCof = "neale_ldsc/100370.ldsc.imputed_v3.both_sexes.tsv.bgz",
  fizzy    = "neale_ldsc/100170.ldsc.imputed_v3.both_sexes.tsv.bgz",
  lowcal   = "neale_ldsc/100160.ldsc.imputed_v3.both_sexes.tsv.bgz",
  Nielsen  = "results/ldsc_Nielsen2018.sumstats.gz",
  R13      = "results/ldsc_FinnGenR13.sumstats.gz"
)
T <- lapply(traits, function(f){ t <- fread(f); t[!duplicated(SNP)] })

# WLS from sufficient statistics
wls_ss <- function(sw, swx, swy, swxx, swxy){
  mx <- swx/sw; my <- swy/sw
  b <- (swxy - mx*swy - my*swx + sw*mx*my) / (swxx - 2*mx*swx + sw*mx^2)
  a <- my - b*mx
  c(a, b)
}
ss <- function(y, x, w){ c(sum(w), sum(w*x), sum(w*y), sum(w*x*x), sum(w*x*y)) }

# two-step WLS returning final weights + estimates
ldsc_twostep <- function(y, x, l2){
  w1 <- 1/l2
  f1 <- do.call(wls_ss, as.list(ss(y, x, w1)))
  fit <- f1[1] + f1[2]*x
  w2 <- 1/(l2*pmax(fit,1))
  f2 <- do.call(wls_ss, as.list(ss(y, x, w2)))
  list(est=f2, w=w2)
}
# jackknife with FIXED weights, via per-block sufficient stats
jk_se <- function(y, x, w, blk){
  tot <- ss(y, x, w)
  bs <- matrix(0, NB, 5)
  for (j in 1:5) bs[,j] <- tapply(cbind(w, w*x, w*y, w*x*x, w*x*y)[,j], blk, sum)
  th <- t(sapply(1:NB, function(b) wls_ss(tot[1]-bs[b,1], tot[2]-bs[b,2], tot[3]-bs[b,3],
                                          tot[4]-bs[b,4], tot[5]-bs[b,5])))
  ctr <- sweep(th, 2, colMeans(th))
  list(se=sqrt((NB-1)/NB * colSums(ctr^2)), th=th)
}

## ---- single-trait h2 -------------------------------------------------------
h2_tab <- list(); trait_dat <- list()
for (nm in names(T)){
  d <- merge(T[[nm]], ld[, .(SNP, CHR, BP, L2)], by="SNP")
  setorder(d, CHR, BP)
  d$blk <- as.integer(cut(seq_len(nrow(d)), NB, labels=FALSE))
  chisq <- d$Z^2
  keep <- chisq <= max(0.001*median(d$N), 80)
  dd <- d[keep]
  x <- dd$N * dd$L2 / M; y <- dd$Z^2
  f <- ldsc_twostep(y, x, dd$L2)
  j <- jk_se(y, x, f$w, dd$blk)
  h2_tab[[nm]] <- data.table(trait=nm, n_snp=nrow(dd), h2_obs=f$est[2], h2_se=j$se[2],
    intercept=f$est[1], int_se=j$se[1], lambda_gc=median(chisq)/0.4549364,
    mean_chisq=mean(chisq))
  cat(sprintf("%-8s h2=%.4f(%.4f) int=%.3f(%.3f) lamGC=%.3f n=%d\n",
              nm, f$est[2], j$se[2], f$est[1], j$se[1], median(chisq)/0.4549364, nrow(dd)))
  trait_dat[[nm]] <- d
}
h2_tab <- rbindlist(h2_tab)
fwrite(h2_tab, "results/ldsc_h2_v44.csv")

## ---- cross-trait rg --------------------------------------------------------
pairs <- expand.grid(expo=c("coffee","tea","sugarCof","fizzy","lowcal"),
                     outc=c("Nielsen","R13"), stringsAsFactors=FALSE)
pairs <- rbind(pairs, data.frame(expo="coffee", outc="tea"))
pairs <- rbind(pairs, data.frame(expo="Nielsen", outc="R13"))  # same-trait validation (expect rg~1)
h2v <- setNames(h2_tab$h2_obs, h2_tab$trait)
rg_tab <- list()
for (i in seq_len(nrow(pairs))){
  e <- pairs$expo[i]; o <- pairs$outc[i]
  d1 <- trait_dat[[e]][, .(SNP, A1.1=A1, A2.1=A2, N1=N, Z1=Z, CHR, BP, L2, blk)]
  d2 <- trait_dat[[o]][, .(SNP, A1.2=A1, A2.2=A2, N2=N, Z2=Z)]
  d <- merge(d1, d2, by="SNP")
  pal <- paste0(d$A1.1, d$A2.1) %in% c("AT","TA","CG","GC")
  same <- d$A1.1==d$A1.2 & d$A2.1==d$A2.2
  flip <- d$A1.1==d$A2.2 & d$A2.1==d$A1.2
  d <- d[!pal & (same|flip)]
  flip_now <- d$A1.1==d$A2.2 & d$A2.1==d$A1.2
  d[, Z2a := Z2]; d$Z2a[flip_now] <- -d$Z2a[flip_now]
  setorder(d, CHR, BP)
  x <- sqrt(as.numeric(d$N1)*as.numeric(d$N2)) * d$L2 / M; y <- d$Z1 * d$Z2a
  f <- ldsc_twostep(y, x, d$L2)
  j <- jk_se(y, x, f$w, d$blk)
  gcov <- f$est[2]   # x already includes /M, so slope IS the genetic covariance
  rg <- gcov/sqrt(h2v[e]*h2v[o])
  rg_jk <- j$th[,2]/sqrt(h2v[e]*h2v[o])
  rg_se <- sqrt((NB-1)/NB * sum((rg_jk-mean(rg_jk))^2))
  z <- rg/rg_se; p <- 2*pnorm(-abs(z))
  rg_tab[[i]] <- data.table(exposure=e, outcome=o, n_snp=nrow(d), rg=rg, rg_se=rg_se,
    rg_z=z, rg_p=p, xtrait_intercept=f$est[1], xtrait_int_se=j$se[1], gcov=gcov)
  cat(sprintf("%-8sx %-7s rg=%+.3f(%.3f) P=%.2e int=%.4f(%.4f) n=%d\n",
              e, o, rg, rg_se, p, f$est[1], j$se[1], nrow(d)))
}
rg_tab <- rbindlist(rg_tab)
# BH-FDR across the 10 beverage x AF tests
main_idx <- rg_tab$exposure %in% c("coffee","tea","sugarCof","fizzy","lowcal") &
            rg_tab$outcome %in% c("Nielsen","R13")
rg_tab$rg_fdr <- NA_real_
rg_tab$rg_fdr[main_idx] <- p.adjust(rg_tab$rg_p[main_idx], method="BH")
fwrite(rg_tab, "results/ldsc_rg_v44.csv")
cat("DONE\n")
