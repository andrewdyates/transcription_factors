#!/usr/bin/python
"""
python all.tfnames.to.sym.list.py > all.tf.targ.syms.aliases.txt
"""
import sys
import hugo_gene_symbols

FNAME_GSEA = "gsea_tftargs.csv"
FNAME_GSEA_TAB = "gsea_msigdb/tf2targs.tab"
FNAME_NATURE = "nature.tfsyms.txt"

# parse HGNC alias list
H = hugo_gene_symbols.load()

# remap FNAME_GSEA
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

