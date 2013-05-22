downloaded may 15 2013
http://www.broadinstitute.org/gsea/downloads.jsp

NOTES:
+ c3.tft.v3.1.entrez.gmt must be downloaded from GSEA website at http://www.broadinstitute.org/gsea/downloads.jsp
+ HTML file contents of directory gsea_html as required by parse_transfac.py (not included in this repository due to large size) can be downloaded from the web using scrape_transfac.py.

USE: tf2targs.may-21-2013.csv
FORMAT: TF_gene,target_gene_1,target_gene_2...
GENERATED USING: tfgene2targetgene.py

OTHER FILES:
+ transfac_id_to_genes_raw.tab: compiled transfac_id to putative transcription factor genes as parsed from the gsea website; Generated using scrape_transfac.py and parse_transfac.py
+ c3.tft.v3.1.entrez.gmt: mapping of transfac_id to target genes as downloaded from GSEA website
