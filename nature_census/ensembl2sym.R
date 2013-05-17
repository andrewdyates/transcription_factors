library(biomaRt)
tf.ensem <- as.character(read.table("ensembl.txt")[,1])


mart <- useMart("ENSEMBL_MART_ENSEMBL","hsapiens_gene_ensembl",host="www.ensembl.org")
tf.syms <- getBM(c('ensembl_gene_id','hgnc_symbol'), filters = c('ensembl_gene_id'), values=tf.ensem, mart=mart)

length(unique(tf.syms[,2]))
length((tf.syms[,2]))
#1906
length(unique(tf.syms[,2]))
#1867
syms <- tf.syms[,2][tf.syms[,2]!=""]
length(syms)
#[1] 1876
writeLines(syms, "../nature.tfsyms.txt")
