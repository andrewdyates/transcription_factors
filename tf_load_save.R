TF.ADJ <- as.matrix(read.table("%(fname)s", sep="\t", header=TRUE, row.names=1, stringsAsFactors=FALSE, na.strings="", check.names=F))
save(TF.ADJ, file="%(fname)s.RData")
