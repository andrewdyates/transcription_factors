from Bio import Entrez
Entrez.email = "user@osu.edu"

def retrieve_one_annotation(entrezid):
  return retrieve_annotation([entrezid])[0]

def retrieve_annotation(id_list):
  """Annotates Entrez Gene IDs using Bio.Entrez, in particular epost (to
  submit the data to NCBI) and esummary to retrieve the information. 
  Returns a list of dictionaries with the annotations."""
  
  request = Entrez.epost("gene",id=",".join(id_list))
  try:
    result = Entrez.read(request)
  except RuntimeError as e:
    print "An error occurred while retrieving the annotations."
    print "The error returned was %s" % e
    raise
 
  webEnv = result["WebEnv"]
  queryKey = result["QueryKey"]
  data = Entrez.esummary(db="gene", webenv=webEnv, query_key=queryKey)
  annotations = Entrez.read(data)
 
  print "Retrieved %d annotations for %d genes" % (len(annotations), len(id_list))
  return annotations
  
def generate_dict(annotation):
  idmap = {}
  for gene_data in annotation:
    gene_id = gene_data["Id"]
    gene_symbol = gene_data["NomenclatureSymbol"]
    idmap[gene_id] = gene_symbol
  return idmap

def print_data(annotation):
  for gene_data in annotation:
    gene_id = gene_data["Id"]
    gene_symbol = gene_data["NomenclatureSymbol"]
    gene_name = gene_data["Description"]
    print "ID: %s - Gene Symbol: %s - Gene Name: %s" % (gene_id, gene_symbol, gene_name)
