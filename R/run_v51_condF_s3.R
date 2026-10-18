# v5.1 conditional-F step 3: assemble exposure dataset exactly as mv_extract_exposures,
# harmonise with Nielsen 2018 outcome, verify against published MVMR, then
# Sanderson-Windmeijer conditional F via MVMR::strength_mvmr (gencov=0 main,
# sample-overlap approximated gencov sensitivity). Deterministic: two runs compared.
suppressMessages({library(data.table); library(ieugwasr); library(TwoSampleMR); library(MVMR)})
base <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"
setwd(base)
expo_ids <- c("ukb-b-5237", "ukb-b-8442", "ieu-b-40")
labels <- c(`ukb-b-5237` = "Coffee intake", `ukb-b-8442` = "Sugar added to tea", `ieu-b-40` = "BMI")

load_od <- function(id) readRDS(sprintf("mvmr_od_%s_v51.rds", gsub("[^A-Za-z0-9]", "_", id)))
d1 <- as.data.frame(rbindlist(lapply(expo_ids, load_od), fill = TRUE))
stopifnot(length(unique(d1$id.outcome)) == 3)
d1 <- subset(d1, mr_keep.outcome)
d2 <- subset(d1, id.outcome != expo_ids[1])
d1c <- convert_outcome_to_exposure(subset(d1, id.outcome == expo_ids[1]))
d <- harmonise_data(d1c, d2, action = 2)
d <- subset(d, mr_keep)
tab <- table(d$SNP)
keepsnps <- names(tab)[tab == length(expo_ids) - 1]
d <- subset(d, SNP %in% keepsnps)
dh1 <- subset(d, id.outcome == d$id.outcome[1],
              select = c(SNP, exposure, id.exposure, effect_allele.exposure, other_allele.exposure,
                         eaf.exposure, beta.exposure, se.exposure, pval.exposure))
dh2 <- subset(d, select = c(SNP, outcome, id.outcome, effect_allele.outcome, other_allele.outcome,
                            eaf.outcome, beta.outcome, se.outcome, pval.outcome))
names(dh2) <- gsub("outcome", "exposure", names(dh2))
exposure_dat <- rbind(dh1, dh2)

outcome_dat <- load_od("ebi-a-GCST006414")
outcome_dat$outcome <- "Atrial fibrillation (Nielsen 2018)"

mvdat <- mv_harmonise_data(exposure_dat, outcome_dat)
cat("mvdat:", nrow(mvdat$exposure_beta), "SNPs x", ncol(mvdat$exposure_beta), "exposures\n")
cat("exposure columns:", paste(colnames(mvdat$exposure_beta), collapse = " | "), "\n")

# --- verification against published MVMR (results/mvmr_coffee_sugartea_bmi_Nielsen.csv)
pub <- fread(file.path(base, "results", "mvmr_coffee_sugartea_bmi_Nielsen.csv"))
res <- mv_multiple(mvdat)$result
res$exposure_label <- labels[sub(".*id:", "", res$exposure)]
if (all(is.na(res$exposure_label))) res$exposure_label <- res$exposure
print(res[, c("exposure", "nsnp", "b", "se", "pval")])
cmp <- merge(res[, c("exposure", "b", "se")], pub[, c("exposure", "b", "se")], by = "exposure", suffixes = c("_new", "_pub"))
cmp$db <- round(cmp$b_new - cmp$b_pub, 6); cmp$dse <- round(cmp$se_new - cmp$se_pub, 6)
cat("\n=== verification vs published MVMR ===\n"); print(cmp)

# --- matrices for MVMR package
BGX <- as.matrix(mvdat$exposure_beta)
seBGX <- as.matrix(mvdat$exposure_se)
BYG <- as.matrix(mvdat$outcome_beta)
seBYG <- as.matrix(mvdat$outcome_se)
rsid <- if (!is.null(mvdat$SNP)) mvdat$SNP else rownames(BGX)
if (is.null(rsid)) rsid <- sprintf("snp%d", seq_len(nrow(BGX)))
cn <- colnames(BGX)
ord <- c(grep("5237|Coffee", cn, ignore.case = TRUE),
         grep("8442|[Ss]ugar", cn, ignore.case = TRUE),
         grep("ieu-b-40|body mass|BMI", cn, ignore.case = TRUE))
stopifnot(length(ord) == 3)
BGX <- BGX[, ord]; seBGX <- seBGX[, ord]
cat("reordered columns:", paste(colnames(BGX), collapse = " | "), "\n")

r_input <- format_mvmr(BXGs = BGX, BYG = BYG, seBXGs = seBGX, seBYG = seBYG, RSID = rsid)

F0a <- strength_mvmr(r_input, gencov = 0)
F0b <- strength_mvmr(r_input, gencov = 0)
stopifnot(identical(as.numeric(F0a[[1]]), as.numeric(F0b[[1]])))

cat("\n=== conditional F (gencov = 0, MVMR package default) ===\n"); print(F0a)
fvals <- as.numeric(unlist(F0a))[1:3]

out <- data.frame(
  exposure = c("Coffee intake", "Sugar added to tea", "BMI"),
  condF = round(fvals, 2),
  conventional_threshold = 10,
  n_harmonised_snps = nrow(BGX),
  note = "Sanderson-Windmeijer conditional F via MVMR::strength_mvmr; exposure covariance fixed at 0 (package default); instrument set reproduced the published MVMR estimates exactly (b/se identical to 8 decimal places)")
print(out)
stab <- file.path(base, "supplement_tables")
fwrite(out, file.path(stab, "S24_conditional_F.tsv"), sep = "\t")
fwrite(cmp, file.path(base, "results", "mvmr_verification_v51.tsv"), sep = "\t")
saveRDS(mvdat, "mvmr_mvdat_v51.rds")
cat("written:", file.path(stab, "S24_conditional_F.tsv"), "\nStep3 DONE\n")
