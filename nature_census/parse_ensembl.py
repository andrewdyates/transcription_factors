#!/usr/bin/python
"""Parse list of transcription factors, output list of symbols.
python parse_ensembl.py > ensembl.txt
"""
import sys
FNAME = "nrg2538-s3.txt"
fp = open(FNAME)
for line in fp:
  if "--Table start--" in line: break #skip header
fp.next() # skip column headers
for line in fp:
  row = line.strip().split('\t')
  if len(row) >= 2:
    print row[1]
