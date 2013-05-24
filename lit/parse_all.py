#!/usr/bin/python
"""Parse .tab sheets of human transcription factor targets.

Per May 23, 2013:

+++ PARSING E2f.txt +++
n_all 1092
n_human 641
good_pairs 452
missed_pairs 189

+++ PARSING Fox.txt +++
n_all 475
n_human 331
good_pairs 320
missed_pairs 23

+++ PARSING Myc.txt +++
n_all 337
n_human 150
good_pairs 110
missed_pairs 40

+++ PARSING NfKb.txt +++
n_all 204
n_human 50
good_pairs 47
missed_pairs 3

+++ PARSING Stat.txt +++
n_all 434
n_human 222
good_pairs 135
missed_pairs 87
"""
FNAMES = ["E2f.txt", "Fox.txt", "Myc.txt", "NfKb.txt", "Stat.txt"]
FNAME_OUT = "lit_factors_may23_2013.csv"

import hugo_gene_symbols
from lib import *
H = hugo_gene_symbols.load()

def main():
  tfs = {}
  for fname in FNAMES:
    print "\n+++ PARSING %s +++" % fname
    tfs.update(parse(fname))

  # write to file
  print "WRITING TO", FNAME_OUT
  fp = open(FNAME_OUT,'w')
  for tf in sorted(tfs):
    print>>fp, "%s,%s" % (tf, ",".join(sorted(tfs[tf])))
  fp.close()

if __name__ == "__main__":
  main()
