#!/usr/bin/env Rscript
suppressMessages(library(ieugwasr))
ids <- c("ukb-b-8442","ukb-b-243","ukb-b-2832","ukb-b-19703","ukb-b-5867","ukb-b-5237","ukb-b-6066")
g <- tryCatch(gwasinfo(ids), error=function(e){cat("ERR:",conditionMessage(e),"\n"); NULL})
if(!is.null(g)){
  cols <- intersect(c("id","trait","sample_size","nsnp","note","unit","category","year","author"), names(g))
  for(i in seq_len(nrow(g))){
    cat("-----\n")
    for(cl in cols) cat(sprintf("%s: %s\n", cl, as.character(g[i,cl])))
  }
}
