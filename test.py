# import pprint
# from BCBio.GFF import GFFExaminer

# in_file = "uniprot-yourlist chr1p36.gff"
# examiner = GFFExaminer()
# in_handle = open(in_file)
# pprint.pprint(examiner.parent_child_map(in_handle))
# in_handle.close()

import urllib.parse
import urllib.request
#from bs4 import BeautifulSoup

url = 'https://www.uniprot.org/uniprot'

params = {
'query': 'gene:AADACL3 organism:"Homo sapiens (Human) [9606]"',
'format': 'gff',
}
# 'from': 'GENENAME',
# 'to': 'ID',
#'organism': 'Homo sapiens (Human)9606'
#https://www.uniprot.org/uniprot/?query=gene:AADACL3%20organism:%22Homo%20sapiens%20(Human)%20[9606]%22&format=gff&limit=10&sort=score

###https://www.uniprot.org/uniprot/?query=insulin&sort=score&columns=id,entry name,reviewed,protein names,genes,organism,length&format=tab

data = urllib.parse.urlencode(params)
print(data)
data = data.encode('utf-8')
print(data)
req = urllib.request.Request(url, data)
req = urllib.request.Request("https://www.uniprot.org/uniprot/?query=gene:AADACL3%20organism:%22Homo%20sapiens%20(Human)%20[9606]%22&format=gff")
print(str(req))
with urllib.request.urlopen(req) as f:
   response = f.read()
text = response.decode('utf-8')
with open('text.txt', 'w') as file:
    file.write(text)
