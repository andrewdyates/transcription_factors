import hugo_gene_symbols
import re
H = hugo_gene_symbols.load()


def rmch(s):
  return filter(lambda x: not x in '- .,;|_"', s)

def trysym(s):
  """Just try to return any viable, credible symbol!"""
  s = s.strip(' \t\n\r;:,."')
  if not s: return None
  z = H.find_sym(s, allow_dupe=True)
  if z: return z
  s = s.upper()
  z = H.find_sym(s, allow_dupe=True)
  if z: return z
  ss = s.split(' ')[0]
  z = H.find_sym(ss, allow_dupe=True)
  if z: return z
  ss = s.split(',')[0]
  z = H.find_sym(ss, allow_dupe=True)
  if z: return z
  s = rmch(s)
  z = H.find_sym(s, allow_dupe=True)
  if z: return z
  ss = s.replace('ALPHA','A').replace('BETA','B')
  z = H.find_sym(ss, allow_dupe=True)
  if z: return z
  ss = s.replace('ALPHA','').replace('BETA','')
  z = H.find_sym(ss, allow_dupe=True)
  if z: return z
  ss = "-".join(filter(None, re.split('([0-9]+)', s)))
  z = H.find_sym(ss, allow_dupe=True)
  if z: return z
  # special cases
  if s == "P53": return "TP53"
  if s[-1] in ("AB"):
    z = H.find_sym(s[:-1])
    if z: return z
  ss = s.split('/')[0]
  z = H.find_sym(ss, allow_dupe=True)
  if z: return z
  return None

def parse(fname):
  fp = open(fname, "Ur")
  fp.next()
  n_all, n_human, good_pairs, missed_pairs = 0,0,0,0
  tfs = {}
  all_syms = {}
  problems = set()
  for i, line in enumerate(fp):
    row = line.strip('\n\r').split('\t')
    if len(row) < 4:
      print "$ TRUNCATED LINE %d:"%(i+2), line.strip('\n\r')
      continue
    n_all += 1
    
    gene, tf, spec = row[0], row[1], row[3]
    if spec != "Human": continue
    if not gene or not tf:
      print "$ MISSING GENE OR TF:", line.strip('\n\r')
      continue
    n_human += 1
    # gene
    if gene in all_syms:
      good_gene = all_syms[gene]
    else:
      good_gene = trysym(gene)
      if not good_gene or isinstance(good_gene,set):
        problems.add(gene)
      all_syms[gene] = good_gene
    # tf
    if tf in all_syms:
      good_tf = all_syms[tf]
    else:
      good_tf = trysym(tf)
      if not good_tf or isinstance(good_tf,set):
        #print "Cannot uniquely map human tf symbol %s. Got %s." % (tf, good_tf)
        problems.add(tf)
      all_syms[tf] = good_tf

    # manual custom cases
    if good_gene and isinstance(good_gene,basestring):
      if tf.lower() in ('"foxa2, foxa1"','"foxa1, foxa2"', "foxa"):
        tfs.setdefault("FOXA1",set()).add(good_gene)
        tfs.setdefault("FOXA2",set()).add(good_gene)
        if tf in problems: problems.remove(tf)
        good_pairs += 2
        continue
      if tf.upper() in ("FOXM1A","FOXM1B","FOXM1C"):
        tfs.setdefault(tf.upper(),set()).add(good_gene)
        if tf in problems: problems.remove(tf)
        good_pairs += 1
        continue
      

    # pair
    if good_gene and isinstance(good_gene,basestring) and good_tf and isinstance(good_tf,basestring):
      tfs.setdefault(good_tf,set()).add(good_gene)
      good_pairs += 1
    else:
      missed_pairs += 1
      #print "!", gene, good_gene, tf, good_tf

  print "n_all", n_all
  print "n_human", n_human
  print "good_pairs", good_pairs
  print "missed_pairs", missed_pairs
  print "# tf", len(tfs)
  print "# tf->targ pairs", sum( len(q) for q in tfs.values() )
  print "# unique symbols", len(all_syms)
  print "# problem symbols", len(problems)
  print
  print "PROBLEMS"
  for s in sorted(problems):
    print s, all_syms[s]

  return tfs
