#!/usr/bin/python
"""Remap gene symbols in csv to entrez IDs
"""
import ncbi_gene_info
import hugo_gene_symbols
import sys
H = hugo_gene_symbols.load()
R = ncbi_gene_info.load_list()

FNAME = "all_tf_with_targs_may_21_2013.csv"
FNAME_ENTREZ = FNAME + ".entrez.csv"
MANUAL_MAP = {'FOXM1C': set(['2305'])}

sym_to_entrez, alias_to_entrez = ncbi_gene_info.sym_to_entrez_dicts(R)

multi_sym = [(k,v) for k,v in sym_to_entrez.items() if len(v) > 1]
multi_alias = [(k,v) for k,v in alias_to_entrez.items() if len(v) > 1]
print "symbols with multiple entrez IDs", len(multi_sym)
print multi_sym
print "---"
print "aliases with multiple entrez IDs", len(multi_alias)

def get_entrezes(s):
  hugo = H.find_sym(s)
  if s in MANUAL_MAP:
    return MANUAL_MAP[s]
  elif s in sym_to_entrez:
    return sym_to_entrez[s]
  elif hugo in sym_to_entrez:
    return sym_to_entrez[hugo]
  elif s in alias_to_entrez:
    return alias_to_entrez[s]
  elif hugo in alias_to_entrez:
    return alias_to_entrez[hugo]
  else:
    return None
    

no_entrez = set()
tf_entrezes = {}

for line in open(FNAME):
  row = line.strip('\n\r').split(',')
  tf, targs = row[0], row[1:]
  tfe = get_entrezes(tf)
  if not tfe:
    print >>sys.stderr, "Cannot find any entrez ID for TF symbol %s" % tf
    no_entrez.add(tf)
    continue

  if len(tfe) > 1:
    print >>sys.stderr, "TF %s has %d entrez IDs: %s" % (tf, len(tfe), ", ".join(tfe))
  for tfei in tfe:
    etargs = set()
    for ss in targs:
      sse = get_entrezes(ss)
      if not sse:
        print >>sys.stderr, "Cannot find any entrez ID for tf %s target symbol %s" % (tf, ss)
        no_entrez.add(ss)
      else:
        for sss in sse:
          etargs.add(sss)
    tf_entrezes.setdefault(tfei,set()).update(etargs)

# print results
fp_out = open(FNAME_ENTREZ, 'w')
for tfe in sorted(tf_entrezes):
  print >>fp_out, ",".join([tfe]+sorted(tf_entrezes[tfe]))
fp_out.close()
  
