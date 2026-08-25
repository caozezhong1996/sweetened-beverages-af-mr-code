suppressMessages(library(readr))
coffee <- read_tsv("neale_ldsc/1498.ldsc.imputed_v3.both_sexes.tsv.bgz",
                   col_types = cols(SNP = "c", A1 = "c", A2 = "c", N = "d", Z = "d"), progress = FALSE)
af <- read_tsv("results/ldsc_Nielsen2018.sumstats.gz",
               col_types = cols(SNP = "c", A1 = "c", A2 = "c", N = "d", Z = "d"), progress = FALSE)
cat("coffee:", nrow(coffee), " AF:", nrow(af), " shared:", length(intersect(coffee$SNP, af$SNP)), "\n")
