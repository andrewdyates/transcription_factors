#!/usr/bin/python
"""Load GSEA msigdb, nature methods list, output adj matrix

# Transcription factors: 235
# Unique Genes (plus transcription factor genes): 12280
# 1876 transcription factors
"""
## TODO: load nature genes, expand number of columns in adj matrix
import sys
import gsea_msigdb.read_tf2targs as gsea
import numpy as np
import matrix_io as mio
FNAME_OUT = "TF.ADJ.tab"

def main(fname="tf2targs.tab"):
  genes = set()
  adj_d = gsea.parse(fname)
  for tf, targs in adj_d.items():
    genes.add(tf); genes.update(targs)
  rownames = sorted(genes)
  colnames = sorted(adj_d)
  row_idx = dict(((s,i) for i,s in enumerate(rownames)))
  A = np.zeros((len(colnames), len(rownames)))
  
  for j,tf in enumerate(colnames):
    for g in adj_d[tf]:
      i = row_idx[g]
      A[i,j] = 1

  print >>sys.stderr, "# interactions: %d" % np.sum(A)
  print >>sys.stderr, "# genesXtf size:", A.shape
  mio.save(A, fp=FNAME_OUT, row_ids=rownames, col_ids=colnames, fmt="%d")

if __name__ == "__main__":
  main()
