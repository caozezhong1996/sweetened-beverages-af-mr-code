# install CRAN deps for GenomicSEM (+ MRlap chain)
repos <- c(CRAN = "https://mirrors.tuna.tsinghua.edu.cn/CRAN")
need <- c("plyr","e1071","gdata","lavaan","doParallel","foreach",
          "splitstackshape","R.utils","mgsub","simsalapar","iterators")
inst <- rownames(installed.packages())
miss <- setdiff(need, inst)
cat("missing:", paste(miss, collapse=", "), "\n")
if (length(miss) > 0) {
  options(timeout = 240)
  install.packages(miss, repos = repos, dependencies = FALSE, quiet = TRUE)
}
still <- setdiff(need, rownames(installed.packages()))
cat("still missing after install:", paste(still, collapse=", "), "\n")
ok <- sapply(need, function(p) suppressMessages(require(p, character.only = TRUE)))
print(ok)
