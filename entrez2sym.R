# convert tfcat entrezids to gene symbols
library(org.Hs.eg.db)
entrezIDs <- as.character(read.table("tfcat.entrez.txt")[,1])
syms <- mget(entrezIDs, org.Hs.egSYMBOL, ifnotfound=NA)
print(sum(is.na(syms))) #1437 ok
writeLines(na.omit(syms), "tfcat.sym.txt")
