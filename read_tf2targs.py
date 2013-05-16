#!/usr/bin/python
"""Load tf2targs.tab into adjacency dict

python read_tf2targs.py tf2targs.tab > tftargs.csv
output is: transcription factor gene, list of target genes

# Transcription factors: 235
# Unique Genes (plus transcription factor genes): 12280
"""
import sys

def main(fname=sys.argv[1]):
  n_tfs = 0
  genes = set()
  for tf, targs in parse(fname).items():
    n_tfs += 1
    genes.add(tf); genes.update(targs)
    print "%s,%s" % (tf, ",".join(targs))
  print >>sys.stderr, "# Transcription factors: %d" % n_tfs
  print >>sys.stderr, "# Unique Genes (plus transcription factor genes): %d" % len(genes)

def parse(fname):
  tfadj = {}
  for line in open(fname):
    tfs, targs = [s.split(',') for s in line.strip('\n\r').split('\t')]
    for tf in tfs:
      tfadj.setdefault(tf, set()).update(targs)
  return tfadj

if __name__ == "__main__":
  main()
