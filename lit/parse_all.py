#!/usr/bin/python
"""Parse .tab sheets of human transcription factor targets."""
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
