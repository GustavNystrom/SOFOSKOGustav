# Location where new files are created if not specified otherwise when calling functions

dir_loc = r'C:\Users\gusny\OneDrive\Dokument\SOFOSKO'


# Names for the files being created:
# Database name
db_name = 'testdb.db'

#GFF file name
gff_name = 'uniprot-test-list.gff'

# Mapping table name
mapping_name = 'uniprot-mpngtbl-1p36.tab'

#Filename for the mutations_per_gene file
value_count_file_name = 'mutations_per_gene.txt'

#Filename for create_dataframe function
dataframe_filename = 'matched_mutations.txt'

#Filename for genelist
gene_list_name = 'gene_list.txt'

# plot names
mutations_per_gene_name = 'mutations_per_gene.png'
matched_mut_per_gene_name = 'matched_mutations_per_gene.png'

#Logging filename
logging_name = 'Runtime_log.log'

#Logging database creation
logging_db_name = 'DB_log.log'

#Features affected name
features_affected = 'features_affected.txt'



# mutations per gene shown in graph
n_mutations = 10

#DataFrame labels = the columns for the new dataframe/Maf-file that is generated.
df_labels = [
'Hugo_Symbol',
'Chromosome',
'Start_Position',
'End_Position',
'Variant_Classification',
'Variant_Type',
'Reference_Allele',
'Tumor_Seq_Allele2',
'HGVSc',
'HGVSp',
'HGVSp_Short',
'Transcript_ID',
'Gene',
'RefSeq',
'NVAF',
'NDP',
'TVAF',
'TDP',
'TAL',
'Matched_ID' # The ID in the database it matched
]




#Domains to skip: won't try to match domains with these labels
domains_skip = [
'Chain',
'Natural variant',
'Sequence conflict',
'Alternative sequence',
'Helix',
'Beta strand',
'Turn']


#Regions
uniprot_regions = [
'Topological domain',	#Location of non-membrane regions of membrane-spanning proteins
'Transmembrane',	#Extent of a membrane-spanning region
'Intramembrane',	#Extent of a region located in a membrane without crossing it
'Domain',	#Position and type of each modular protein domain
'Repeat',	#Positions of repeated sequence motifs or repeated domains
'Calcium binding',	#Position(s) of calcium binding region(s) within the protein
'Zinc finger',	#Position(s) and type(s) of zinc fingers within the protein
'DNA binding',	#Position and type of a DNA-binding domain
'Nucleotide binding',	#Nucleotide phosphate binding region
'Region',	#Region of interest in the sequence
'Coiled coil',	#Positions of regions of coiled coil within the protein
'Motif',	#Short (up to 20 amino acids) sequence motif of biological interest
'Compositional bias',  #Region of compositional bias in the protein
]

#Sites
uniprot_sites = [
'Active site',	#Amino acid(s) directly involved in the activity of an enzyme
'Metal binding',	#Binding site for a metal ion
'Binding site',	#Binding site for any chemical group (co-enzyme, prosthetic group, etc.)
'Site',	#Any interesting single amino acid site on the sequence
]

#amino acid modifications
unprot_aa_modifications = [
'Non-standard residue',	#Occurence of non-standard amino acids (selenocysteine and pyrrolysine) in the protein sequence
'Modified residue',	#Modified residues excluding lipids, glycans and protein cross-links
'Lipidation',	#Covalently attached lipid group(s)
'Glycosylation',	#Covalently attached glycan group(s)
'Disulfide bond',	#Cysteine residues participating in disulfide bonds
'Cross-link',	#Residues participating in covalent linkage(s) between proteins
]