#!/usr/bin/python
"""Print transcription factor gene to target list.

python tfgene2targetgene.py > ../tf2targs.tab
"""
TF_FNAME = "../transfac.id.to.genes.tab"
TARG_FNAME = "c3.tft.v3.1.symbols.gmt"

# parse TF_FNAME
tid2tfs = {}
for line in open(TF_FNAME):
  tid, tfs = line.strip().split('\t')
  if tfs == "None":
    tid2tfs[tid] = None
  else:
    tid2tfs[tid] = tfs.split(';')

tftargs = []  
# parse TARG_FNAME
for line in open(TARG_FNAME):
  row = line.strip().split('\t')
  tfs = tid2tfs.get(row[0], None)
  if tfs is not None:
    tftargs.append((tid2tfs[row[0]], row[2:]))
  
# output
for tfs, targs in tftargs:
  print "%s\t%s" % (",".join(tfs), ",".join(targs))
