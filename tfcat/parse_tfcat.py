#!/usr/bin/python
"""Parse tfcat export, output entrez gene id list.

python parse_tfcat.py > ../tfcat.entrez.txt
# tfs: 1437
"""
import sys
FNAME = "tfcat.txt"

def main(fname=FNAME):
  tfs = parse(fname)
  print "\n".join(sorted(tfs))
  print >>sys.stderr, "# tfs: %d" % len(tfs)

def parse(fname):
  fp = open(fname)
  fp.next()
  tfs = []
  for line in fp:
    row = line.strip().split('\t')
    eid = row[0]
    if eid:
      try:
        int(eid)
      except ValueError:
        continue
      else:
        tfs.append(eid)
  return tfs

if __name__ == "__main__":
  main()
