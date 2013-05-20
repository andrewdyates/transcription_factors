#!/usr/bin/python
"""
python all.tfnames.to.sym.list.py > all.tf.targ.syms.aliases.txt
"""
import sys
FNAME_GSEA = "gsea_tftargs.csv"
FNAME_GSEA_TAB = "gsea_msigdb/tf2targs.tab"
FNAME_NATURE = "nature.tfsyms.txt"
FNAME_HGNC = "hgnc_alias_list.txt"

# parse HGNC alias list
syms = {}
problems = {}
official = set()
fp = open(FNAME_HGNC)
fp.next()

bad = 0
for line in fp:
  row = line.strip().split('\t')
  if len(row) < 6:
    continue
  sym, aliases = row[1], filter(None, row[4].split(', ')+row[5].split(', '))
  syms[sym] = sym
  official.add(sym)
  for s in aliases:
    if s in syms:
      bad += 1
    syms[s] = sym # will override dupes... oh well
print len(syms)
print bad
    

# remap FNAME_GSEA
gsea_remap_fname = FNAME_GSEA+".aliasmap.txt"
n_changed, n_same = 0,0
fp_out = open(gsea_remap_fname, "w")
for line in open(FNAME_GSEA):
  newline = []
  for s in line.strip().split(','):
    if s not in official and s in syms:
      newline.append(syms[s])
      n_changed += 1
    else:
      newline.append(s)
      n_same += 1
  fp_out.write(",".join(newline)+"\n")
fp_out.close()
print n_changed, n_same

nature_remap_fname = FNAME_NATURE+".aliasmap.txt"
n_changed, n_same = 0,0
fp_out = open(nature_remap_fname, "w")
for line in open(FNAME_NATURE):
  s = line.strip()
  if s not in official and s in syms:
    print s, syms[s]
    s = syms[s]
    n_changed += 1
  else:
    n_same += 1
  fp_out.write("%s\n"%s)
fp_out.close()
print n_changed, n_same

nature_tab_remap_fname = FNAME_GSEA_TAB+".aliasmap.tab"
fp_out = open(nature_tab_remap_fname, "w")
for line in open(FNAME_GSEA_TAB):
  tfs, targs = [s.split(',') for s in line.strip().split('\t')]
  new_tfs, new_targs = [],[]
  for s in tfs:
    if s not in official and s in syms:
      new_tfs.append(syms[s])
    else:
      new_tfs.append(s)
  for s in targs:
    if s not in official and s in syms:
      new_targs.append(syms[s])
    else:
      new_targs.append(s)
  fp_out.write(",".join(new_tfs)+"\t"+",".join(new_targs)+"\n")
fp_out.close()
  
