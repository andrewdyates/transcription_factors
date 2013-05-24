#!/usr/bin/python
"""Load GSEA msigdb, nature methods list, output adj matrix.
Use new symbol mapped lists. Use only "high quality" TF list.
Also output csv of target to putative mappings.

python create_tf_adjm.py
# genes total: 12692
# transcription factors: 1370
# transcription factors with targets: 234
Printing list of transcription factors with putative targets to all_tf_with_targs_may_21_2013.csv
# interactions: 133764
# genesXtf size: (12692, 1370)
"""
import numpy as np
import matrix_io as mio
import sys

TARGS_FNAME = "gsea_msigdb/tf2targs.may-21-2013.csv"
TFLIST_FNAME = "nature_census/nature_tf_list_high_may21_2013.txt"
LIT_FNAME = "lit/lit_factors_may23_2013.csv"
MERGED_LIST_OUT_FNAME = "all_tf_with_targs_may_21_2013.csv"
# Warning: the adj matrix is a huge file. Move it out of the local directory once created.
ADJM_OUT_FNAME = "all_tf_with_targs_may_21_2013_adjm.tab"


def main(write_adj=False):
  all_genes = set()
  tf_targs = {}
  for line in open(TARGS_FNAME):
    row = line.strip('\n\r').split(',')
    tf_targs[row[0]] = set(row[1:])
    all_genes.update(row[1:])
   
  tfs = set(tf_targs.keys())
  for line in open(TFLIST_FNAME):
    tfs.add(line.strip('\n\r'))
  all_genes.update(tfs)

  for line in open(LIT_FNAME):
    row = line.strip().split(',')
    tf, targs = row[0], row[1:]
    tfs.add(tf)
    all_genes.update(row)
    tf_targs.setdefault(tf,set()).update(targs)

  # STATS
  print "# genes total:", len(all_genes)
  print "# transcription factors:", len(tfs)
  print "# transcription factors with targets:", len(tf_targs)
  # Text adj list
  print "Printing list of transcription factors with putative targets to %s" % MERGED_LIST_OUT_FNAME
  fp_out = open(MERGED_LIST_OUT_FNAME,"w")
  for tf in sorted(tfs):
    if tf in tf_targs:
      print >>fp_out, "%s,%s" % (tf,",".join(tf_targs))
    else:
      print >>fp_out, tf
      
  # Text adj matrix, columns TF, rows TF targets
  if not write_adj: return 0
  rownames = sorted(all_genes)
  colnames = sorted(tfs)
  row_idx = dict(((s,i) for i,s in enumerate(rownames)))
  A = np.zeros((len(rownames), len(colnames)))

  for j,tf in enumerate(colnames):
    for g in tf_targs.get(tf,[]):
      i = row_idx[g]
      A[i,j] = 1
      
  print >>sys.stderr, "# interactions: %d" % np.sum(A)
  print >>sys.stderr, "# genesXtf size:", A.shape
  mio.save(A, fp=ADJM_OUT_FNAME, row_ids=['"%s"'%s for s in rownames], col_ids=['"%s"'%s for s in colnames], fmt="%d")


if __name__ == "__main__":
  main(**dict((s.split('=') for s in sys.argv[1:])))
