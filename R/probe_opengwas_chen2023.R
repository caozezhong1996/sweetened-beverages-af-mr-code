#!/usr/bin/env Rscript
# probe_opengwas_chen2023.R — check whether Chen 2023 metabolite GCSTs are in OpenGWAS
root <- "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822"
jwt <- readLines(file.path(root, "OPENGWAS_JWT.txt"), warn = FALSE)[1]
Sys.setenv(OPENGWAS_JWT = jwt)
suppressMessages(library(ieugwasr))
for (id in c("ebi-a-GCST90200436", "ebi-a-GCST90199654", "ebi-a-GCST90199644")) {
  r <- tryCatch({
    g <- gwasinfo(id)
    if (is.null(g) || nrow(g) == 0) "NOT FOUND"
    else paste("FOUND:", g$trait[1], "| nsnp:", g$nsnp[1], "| build:", g$build[1])
  }, error = function(e) paste("ERR:", conditionMessage(e)))
  cat(id, "->", r, "\n")
}
