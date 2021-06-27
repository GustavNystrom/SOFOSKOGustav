# Location where new files are created

dir_loc = r'C:\Users\gusny\OneDrive\Dokument\SOFOSKO'

#Main_function

#Filename for the mutations_per_gene file
value_count_file_name = 'mutations_per_gene.txt'

#Filename for create_dataframe function
dataframe_filename = 'matched_mutations.txt'

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