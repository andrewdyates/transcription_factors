#!/usr/bin/python
"""Load GSEA msigdb, nature methods list, output adj matrix

# Transcription factors: 235
# Unique Genes (plus transcription factor genes): 12280
# 1876 transcription factors
---
# interactions: 135831
# genesXtf size: (12955, 1917)
"""
import sys
import gsea_msigdb.read_tf2targs as gsea
import numpy as np
import matrix_io as mio

#GSEA_FNAME = "gsea_msigdb/tf2targs.tab"
GSEA_FNAME = "gsea_msigdb/tf2targs.tab.aliasmap.tab"
#NATURE_FNAME = "nature.tfsyms.txt"
NATURE_FNAME = "nature.tfsyms.txt.aliasmap.txt"

#FNAME_OUT = "/nfs/01/osu6683/tftargets/tf_adj_matrix.tab"
FNAME_OUT = "/nfs/01/osu6683/tftargets/tf_adj_matrix_aliasmapped.tab"

def main():
  genes, tfs = set(), set()
  adj_d = gsea.parse(GSEA_FNAME)
  nature_g = [s.strip() for s in open(NATURE_FNAME)]
  genes.update(nature_g)
  tfs.update(nature_g)
  
  for tf, targs in adj_d.items():
    genes.add(tf); tfs.add(tf); genes.update(targs); 

  rownames = sorted(['"%s"'%s for s in genes])
  colnames = sorted(['"%s"'%s for s in tfs])
  row_idx = dict(((s,i) for i,s in enumerate(rownames)))
  A = np.zeros((len(rownames), len(colnames)))
  
  for j,tf in enumerate(colnames):
    for g in adj_d.get(tf,[]):
      i = row_idx[g]
      A[i,j] = 1

  print >>sys.stderr, "# interactions: %d" % np.sum(A)
  print >>sys.stderr, "# genesXtf size:", A.shape
  mio.save(A, fp=FNAME_OUT, row_ids=rownames, col_ids=colnames, fmt="%d")

if __name__ == "__main__":
  main()
