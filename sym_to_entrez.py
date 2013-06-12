#!/usr/bin/python
"""Remap gene symbols in csv to entrez IDs
"""
import ncbi_gene_info
import hugo_gene_symbols
import sys
H = hugo_gene_symbols.load()
R = ncbi_gene_info.load()

FNAME = "all_tf_with_targs_may_21_2013.csv"
FNAME_ENTREZ = FNAME + ".entrez.csv"
MANUAL_MAP = {'FOXM1C': '2305'}

sym_to_entrez = dict((r[1],r[0]) for r in R)
alias_to_entrez = {}
for r in R:
  entrez, sym, alias_s = r
  aliases = alias_s.split('|')
  for a in aliases:
    if a and a != '-':
      alias_to_entrez.setdefault(a,set()).add(entrez)

def get_entrez(s):
  hugo = H.find_sym(s)
  if s in MANUAL_MAP:
    return MANUAL_MAP[s]
  elif s in sym_to_entrez:
    return sym_to_entrez[s]
  elif hugo in sym_to_entrez:
    return sym_to_entrez[hugo]
  elif s in alias_to_entrez and len(alias_to_entrez[s]) == 1:
    z = alias_to_entrez[s].pop()
    alias_to_entrez[s].add(z)
    return z
  elif hugo in alias_to_entrez and len(alias_to_entrez[hugo]) == 1:
    return alias_to_entrez[hugo]
  else:
    return None
    

no_entrez = set()
fp_out = open(FNAME_ENTREZ, 'w')
for line in open(FNAME):
  row = line.strip('\n\r').split(',')
  tf, targs = row[0], row[1:]
  tfe = get_entrez(tf)
  rowe = [tfe]
  if not tfe:
    print >>sys.stderr, "Cannot find entrez ID for TF symbol %s" % tf
    no_entrez.add(tf)
    continue

  for ss in targs:
    sse = get_entrez(ss)
    if not sse:
      print >>sys.stderr, "Cannot find entrez ID for tf %s target symbol %s" % (tf, ss)
      no_entrez.add(ss)
    else:
      rowe.append(sse)
  print >>fp_out, ",".join(rowe)
  
