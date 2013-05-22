#!/usr/bin/python
"""Parse list of transcription factors, output list of symbols.
Check for official HUGO symbol.
python parse_ensembl.py > ensembl.txt
"""
import sys
import hugo_gene_symbols

FNAME = "nrg2538-s3.txt"
fp = open(FNAME)

H = hugo_gene_symbols.load()
for line in fp:
  if "--Table start--" in line: break #skip header
fp.next() # skip column headers
for line in fp:
  row = line.strip().split('\t')
  if len(row) >= 2:
    sym = row[1]
    offical = H.find_sym(sym, allow_dupes=True)
    if offical != sym:
      print >>sys.stderr "symbol %s != offical symbol %s" % (sym, offical)
    if offical and isinstance(offical,basestring):
      print offical
    
