#!/usr/bin/python
"""Parse list of transcription factors, output list of symbols.
Checks for official HUGO symbol.

From the publicationsupplemental:

Genes classified as 'a' or 'b' are probable TFs for which there is experimental evidence of regulatory function in any mammalian organism ('a') or have an equivalent protein domain arrangement ('b'); those classified as 'c' are possible TFs that contain non-promiscuous Interpro DNa-binding domains (i.e. Interpro domains that are only ever found in TFs), but for which we do not have further functional evidence. Finally, we removed from the list unlikely TFs (classified as 'x') that comprise predicted genes, contain promiscuous Interpro DNa-binding domains (i.e. DNa-binding domains that are also found in non-TFs) or have an established molecular function outside transcription (such as nucleoporins, threonine phosphatases or splicing factors). Finally, we also included 27 curated probable TFs from other sources ('other'), such as Gene Ontology (GO)8 or TraNSFaC9 containing undefined DNa-binding domains, and were therefore missed using the above procedure.

For the analysis we focused on 1,391 TFs that were classified as 'a', 'b' or 'other'.

Writes list to file.

python parse_ensembl.py
"""
import sys
import hugo_gene_symbols

FNAME = "nrg2538-s3.txt"
FNAME_OUT_ALL = "nature_tf_list_all_may21_2013.txt"
FNAME_OUT_HIGH = "nature_tf_list_high_may21_2013.txt"
FNAME_OUT_LOW = "nature_tf_list_low_may21_2013.txt"

fp = open(FNAME)

H = hugo_gene_symbols.load()
for line in fp:
  if "--Table start--" in line: break #skip header
fp.next() # skip column headers

bad_ensemble = set()
bad = set()
good_lines = 0
remapped_sym = 0
ambigious_sym = 0
used_sym = 0
tfs_abo = set()
tfs_cx = set()

for line in fp:
  row = line.strip().split('\t')
  if len(row) >= 6:
    ensembl_id = row[1]
    cls = row[0]
    if not ensembl_id:
      print "No ensembl ID on line?", line
      continue
      
    offical = H.ensembl.get(ensembl_id, None)
    if offical is None:
      bad_ensemble.add(ensembl_id)
      # try to get gene symbol
      sym = row[5]
      if sym:
        offical_sym = H.find_sym(sym, allow_dupe=True)
        if sym == offical_sym:
          used_sym += 1
          if cls in ('a','b','other'):
            tfs_abo.add(sym)
          else:
            tfs_cx.add(sym)
          print "!%s => %s" % (ensembl_id, sym)
        elif offical_sym and isinstance(offical_sym, basestring):
          remapped_sym += 1
          if cls in ('a','b','other'):
            tfs_abo.add(offical_sym)
          else:
            tfs_cx.add(offical_sym)
          print "!!%s => %s => %s" % (ensembl_id, sym, offical_sym)
        elif offical_sym and isinstance(offical_sym, set):
          ambigious_sym += 1
          print "Ambigious !!!%s => %s => %s" % (ensembl_id, sym, offical_sym)
        else:
          bad.add(ensembl_id)
    else:
      if cls in ('a','b','other'):
        tfs_abo.add(offical)
      else:
        tfs_cx.add(offical)
      good_lines += 1
fp.close()

print "Bad ensembl IDs", len(bad_ensemble)
print "Good lines:", good_lines
print "# Unrecognized lines:", len(bad)
print "used_syms", used_sym
print "remapped_syms", remapped_sym
print "ambigious_syms", ambigious_sym
print "# recognized tfs", len(tfs_abo) + len(tfs_cx)
print "# high quality tf", len(tfs_abo)
print "# low quality tf", len(tfs_cx)

print "Writing all tf list to file %s..." % FNAME_OUT_ALL
open(FNAME_OUT_ALL, "w").write("\n".join(sorted(tfs_abo|tfs_cx)))
print "Writing high quality tf list to file %s..." % FNAME_OUT_HIGH
open(FNAME_OUT_HIGH, "w").write("\n".join(sorted(tfs_abo)))
print "Writing low quality tf list to file %s..." % FNAME_OUT_LOW
open(FNAME_OUT_LOW, "w").write("\n".join(sorted(tfs_cx)))
