# Location where new files are created

dir_loc = r'C:\Users\gusny\OneDrive\Dokument\SOFOSKO'

#Main_function

# Database name
db_name = 'testdb.db'

#GFF file name
gff_name = 'uniprot-test-list.gff'

# Mapping table name
mapping_name = 'uniprot-tes-mapping.tab'

#Filename for the mutations_per_gene file
value_count_file_name = 'mutations_per_gene.txt'

#Filename for create_dataframe function
dataframe_filename = 'matched_mutations.txt'

#Filename for genelist
gene_list_name = 'gene_list.txt'

# mutations per gene shown in graph
n_mutations = 10

#DataFrame labels
df_labels = ['Hugo_Symbol',
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

#Logging filename
logging_name = 'Runtime_log.log'

#Features affected name
features_affected = 'features_affected.txt'