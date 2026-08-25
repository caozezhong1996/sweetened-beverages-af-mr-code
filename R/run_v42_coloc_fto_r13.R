#!/usr/bin/env Rscript
# v4.2: colocalization coffee intake (ukb-b-5237) vs AF FinnGen R13 (I9_AF)
# Region: FTO only (chr16:53550954-54050954, hg19 for the coffee GWAS).
# R13 summary stats are hg38 -> variants are matched by rsID, not position.
suppressMessages({library(data.table); library(ieugwasr); library(coloc)})
if (Sys.getenv("OPENGWAS_JWT") == "") stop("OPENGWAS_JWT not set")
root   <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
outdir <- file.path(root, "06_升级分析_v4/results")

# 1. coffee region from OpenGWAS (hg19 window, same as v4)
d1 <- as.data.frame(associations(variants = "16:53550954-54050954", id = "ukb-b-5237"))
cat("coffee SNPs in FTO window:", nrow(d1), "\n")
d1 <- d1[!is.na(d1$beta) & d1$se > 0 & !is.na(d1$rsid) & d1$rsid != "", ]
d1 <- d1[!duplicated(d1$rsid), ]
fwrite(d1, file.path(outdir, "coloc_FTO_coffee_region_v42.csv"))

# 2. extract those rsIDs from the local R13 file (808MB gz, hg38) via python
rsfile <- file.path(outdir, "coloc_FTO_rsids_v42.txt")
writeLines(d1$rsid, rsfile)
gz <- file.path(root, "06_升级分析_v4/finngen_R13_I9_AF.gz")
tmp <- file.path(outdir, "coloc_FTO_R13_raw_v42.tsv")
py <- sprintf(paste0(
  "import gzip\n",
  "ids = set(l.strip() for l in open(r'%s') if l.strip())\n",
  "with gzip.open(r'%s','rt') as f, open(r'%s','w') as o:\n",
  "    hdr = f.readline(); o.write(hdr)\n",
  "    for line in f:\n",
  "        rs = line.split('\\t')[4]\n",
  "        if any(x in ids for x in rs.split(',')): o.write(line)\n"), rsfile, gz, tmp)
pyfile <- file.path(outdir, "coloc_FTO_extract_v42.py")
writeLines(py, pyfile)
system2("python", shQuote(pyfile))
r13 <- fread(tmp)
cat("R13 rows matched by rsid:", nrow(r13), "\n")
setnames(r13, c("chr","pos","ref","alt","rsids","nearest_genes","pval","mlogp","beta","sebeta","af_alt","af_alt_cases","af_alt_controls"))

# 3. merge by rsid (R13 rows may carry comma-separated rsids; expand first)
r13 <- r13[, .(rsid = unlist(strsplit(rsids, ","))), by = .(pos, ref, alt, beta, sebeta, af_alt)]
m <- merge(d1, r13, by = "rsid")
cat("merged SNPs:", nrow(m), "\n")
# allele harmonization: coffee ea/nea vs R13 alt/ref (beta is alt-allele effect)
ok <- (m$ea == m$alt & m$nea == m$ref) | (m$ea == m$ref & m$nea == m$alt)
m <- m[ok, ]
flip <- m$ea == m$ref & m$nea == m$alt   # coffee beta is ea-effect; R13 beta is alt-effect
m$beta.y[flip] <- -m$beta.y[flip]
m <- m[m$sebeta > 0 & !duplicated(m$rsid), ]
cat("harmonized SNPs:", nrow(m), "\n")
if (nrow(m) < 50) stop("too few SNPs")

ds1 <- list(snp = m$rsid, beta = m$beta.x, varbeta = m$se^2,
            N = 428860, type = "quant", MAF = pmin(m$eaf, 1 - m$eaf))
ds2 <- list(snp = m$rsid, beta = m$beta.y, varbeta = m$sebeta^2,
            N = 309052, type = "cc", s = 67783/309052,
            MAF = pmin(m$af_alt, 1 - m$af_alt))
res <- coloc.abf(dataset1 = ds1, dataset2 = ds2)
pp <- res$summary
cat(sprintf("FTO (coffee vs FinnGen R13): PP.H0=%.3g H1=%.3f H2=%.3g H3=%.3f H4=%.3f (nsnp=%d)\n",
    pp["PP.H0.abf"], pp["PP.H1.abf"], pp["PP.H2.abf"], pp["PP.H3.abf"], pp["PP.H4.abf"], pp["nsnps"]))
out <- data.frame(region = "FTO", outcome = "FinnGen R13", nsnp = pp["nsnps"],
                  PP.H0 = pp["PP.H0.abf"], PP.H1 = pp["PP.H1.abf"], PP.H2 = pp["PP.H2.abf"],
                  PP.H3 = pp["PP.H3.abf"], PP.H4 = pp["PP.H4.abf"])
fwrite(out, file.path(outdir, "upgrade_coloc_FTO_FinnGenR13.csv"))
print(out)
cat("COLOC R13 DONE\n")
