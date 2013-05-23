#!/usr/bin/python
"""From web dump, scrape TRANSFACT IDs and corresponding genes, save to file.
Intended for use after executing "scrape_transfac.py" to download all relevant .html files.
Outputs a map from TRANSFACT ID to putative transcription factor gene symbol names.
  Multiple gene names separated with ';'
  Declared missing gene names represented as string 'None'.

$ python parse_transfac.py > transfac_id_to_genes_raw.tab
"""
import sys, re, urllib2

FNAME = "c3.tft.v3.1.entrez.gmt"
#http://www.broadinstitute.org/gsea/msigdb/geneset_page.jsp?geneSetName=V$E47_01
FNAME_PTN = "gsea_html/%s.html"
RX_BRIEF = re.compile("Brief description</th>(.+?)</td>", flags=re.I|re.M|re.S)
# http://en.wikipedia.org/wiki/TBP-associated_factor
TATA = ["TBP","TAF1","TAF2","TAF3","TAF4","TAF4B","TAF5","TAF6","TAF7","TAF8","TAF9","TAF9B","TAF10","TAF11","TAF12","TAF13","TAF15"]
# http://en.wikipedia.org/wiki/NFAT
NFAT = ["NFATC1", "NFATC2", "NFATC3", "NFATC4", "NFATC5"]

def main():
  tids = {}
  for line in open(FNAME):
    row = line.split('\t')
    tid = row[0]
    if "_UNKNOWN" in tid:
      sym = None
    else:
      sym = get_sym_file(tid)
      tids[tid] = sym
  # output list
  for tid, syms in tids.items():
    if syms is None:
      syms_s = "None"
    else:
      syms_s = ";".join(syms)
    print "%s\t%s" % (tid, syms_s)
  

def get_sym_file(tid):
  fname = FNAME_PTN % tid
  page = open(fname).read()
  m = RX_BRIEF.search(page)
  if not m:
    print >>sys.stderr, "Cannot parse file %s" % fname
    raise Exception
  line = m.group(1)
  words = line.split(' ')
  syms = [s[:-1] for s in words if len(s) and s[-1] == ":"]
  if not syms:
    if "Motif does not match any known transcription factor" in line:
      return None
    else:
      # handle exceptions manually
      if tid == "V$TATA_C":
        return TATA
      elif tid == "V$TATA_01":
        return TATA
      elif tid == "V$NFAT_Q6":
        return NFAT
      elif tid == "V$NFAT_Q4_01":
        return NFAT
      elif tid == "TGGAAA_V$NFAT_Q4_01":
        return NFAT
      elif tid == "TATAAA_V$TATA_01":
        return TATA
      else:
        print >>sys.stderr, "Cannot find gene in file %s" % fname
        print >>sys.stderr, "LINE:", line
        raise Exception
  return syms


  # rip description
  # rip gene
#http://www.broadinstitute.org/gsea/msigdb/geneset_page.jsp?geneSetName=V$E47_01
  
if __name__ == "__main__":
  main()
