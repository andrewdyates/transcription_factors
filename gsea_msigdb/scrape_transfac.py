#!/usr/bin/python
"""Scrape transcription factor gene from each TRANSFAC ID"""
import sys, re, urllib2

FNAME = "c3.tft.v3.1.entrez.gmt"
#http://www.broadinstitute.org/gsea/msigdb/geneset_page.jsp?geneSetName=V$E47_01
URL_PTN = "http://www.broadinstitute.org/gsea/msigdb/geneset_page.jsp?geneSetName=%s"
RX_BRIEF = re.compile("<th>Brief description(.+?)</td>", re.I|re.M)

def main():
  tids = {}
  for line in open(FNAME):
    row = line.split('\t')
    tid = row[0]
    if "_UNKNOWN" in tid:
      sym = None
    else:
      sym = get_sym(tid)
      tids[tid] = sym
  print tids

def get_sym(tid):
  url = URL_PTN%tid
  print "Fetching url %s..." % url
  page = urllib2.urlopen(url).read()
  fp_out = open(tid+".html","w")
  fp_out.write(page)
  fp_out.close()
  return ""
  # rip description
  # rip gene
#http://www.broadinstitute.org/gsea/msigdb/geneset_page.jsp?geneSetName=V$E47_01
  
if __name__ == "__main__":
  main()
