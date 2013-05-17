#!/usr/bin/python
"""Read chea-background.csv, output human adj list.
WARNING: chea mixes symbols and aliases and does not seem to have a standardized naming scheme!

python parse_chea.py > ../chea_adj.csv
"""
import sys
FNAME = "chea-background.csv"

def main(fname=FNAME):
  adj_d = parse(fname)
  genes = set()
  for tf, targs in adj_d.items():
    print "%s,%s" % (tf, ",".join(targs))
    genes.add(tf)
    genes.update(targs)
  print >>sys.stderr, "# transcription factors: %d" % len(adj_d)
  print >>sys.stderr, "# unique genes (including tfs): %d" % len(genes)

def parse(fname):
  adj_d = {}
  for line in open(fname):
    row = line.strip().split(',')
    tf, targ, spec = row[1], row[3], row[7].lower()
    if spec != "human":
      continue
    adj_d.setdefault(tf,set()).add(targ)
  return adj_d

if __name__ == "__main__":
  main()
