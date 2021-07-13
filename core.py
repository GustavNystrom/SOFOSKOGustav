import os.path, logging, csv
import settings, db_commands, Mutation
import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
from xlsxwriter.workbook import Workbook

def gene_list(genes, filename):
   # Create a file containing each unique item from a list
   with open(filename, 'w') as file:
      for gene in genes:
         file.write(gene + '\n')
   print('SUccessfully created ', filename)

def mutations_per_gene(dataframe, filename, base_path):
    # Supply the base_path to create the file in that directory
    file_name = os.path.join(base_path, filename)
    value_counts = dataframe['Hugo_Symbol'].value_counts()
    value_counts.to_csv(file_name, sep='\t', header=['Count'], index_label='Hugo_Symbol')
    logging.info(f'Wrote the mutations per gene to file: {file_name}')
    plt.scatter(value_counts.index[0:settings.n_mutations], value_counts[0:settings.n_mutations])
    #plt.figure(figsize=(10.0,10.0))
    plt.title(f'The {settings.n_mutations} most mutated genes')
    plt.ylabel('Number of mutations')
    plt.xlabel('Gene name')
    for n in range(len(value_counts)):
        plt.annotate(f"({value_counts.index[n]}, {value_counts[n]})", (value_counts.index[n], value_counts[n]))

    logging.info('Created plot with mutations per gene')
    plt.savefig(os.path.join(settings.dir_loc, settings.mutations_per_gene_name))
    plt.show()
   
def create_dataframe(data, filename, base_path):
    # Creates a dataframe and dumps it onto a csv with \t as separator. Returns the dataframe.
    dataf = pd.DataFrame(data, columns=settings.df_labels)
    file_name = os.path.join(base_path, filename)
    dataf.to_csv(file_name, sep='\t')
    logging.info(f'Created new dataframe at: {file_name}')
    return dataf

def get_gene_list(dataframe):
    genes = []
    for rown in range(len(dataframe)):
        gene = dataframe.iloc[rown]['Hugo_Symbol']
        if gene in genes:
            continue
        genes.append(gene)
    return genes

def matched_mutations_per_gene(df, dir_loc=settings.dir_loc):
    plt.bar(df['Hugo_Symbol'].value_counts()[0:settings.n_mutations].index,
    df['Hugo_Symbol'].value_counts()[0:settings.n_mutations])
    plt.title('Number of mutations matched to an annotated domain per gene')
    plt.ylabel('Number of mutations')
    plt.xlabel('Gene name')    
    plt.savefig(os.path.join(dir_loc, settings.matched_mut_per_gene_name))
    plt.show()

def features_affected(df, conn, dir_loc=settings.dir_loc):
    regions, sites, aa_modifications, domain_ids = [], [], [], []
    with open(os.path.join(dir_loc, settings.features_affected), 'w') as file:
        for i in df['Matched_ID']:
            i = i.split(',')
            for id in i:
                feature = db_commands.get_feature(conn, id)
                if feature in settings.uniprot_regions:
                    regions.append(feature)
                    if feature == "Domain":
                        domain_ids.append(id)
                elif feature in settings.uniprot_sites:
                    sites.append(feature)
                elif feature in settings.unprot_aa_modifications:
                    aa_modifications.append(feature)
        writer = csv.writer(file, delimiter='\t')
        file.write('##The most common regions affected:\n\n')
        counter = Counter(regions).most_common()
        for key, item in counter:
            writer.writerow([key, item])
        
        file.write('\n\n##The most common sites affected:\n\n')
        counter = Counter(sites).most_common()
        for key, item in counter:
            writer.writerow([key, item])
        
        file.write('\n\n##The most common amino acid modifications affected:\n\n')
        counter = Counter(aa_modifications).most_common()
        for key, item in counter:
            writer.writerow([key, item])
        
        file.write('\n\n##The 10 most common domain descriptions:\n\n')
        domain_descs = []
        for id in domain_ids:
            note = Mutation.get_note(id, conn)
            domain_descs.append(note)
        counter = Counter(domain_descs).most_common()[:10]
        for key, item in counter:
            writer.writerow([key, item])

        features_counter(df, conn, writer, file)
    
    features_affected_to_xl(os.path.join(dir_loc, settings.features_affected))

def features_counter(df, conn, writer, file):
    """Writer is a csv writer, file is an opened file to write to"""
    matched_ids = []
    for matched_id in df['Matched_ID']:
        matched_ids_current = matched_id.split(',')
        matched_ids += matched_ids_current
    matched_ids = Counter(matched_ids).most_common()
    file.write('\n\n##Regions that have multiple mutations:\nID\tGENE\tREGION\tNOTE\tRECURRENCES \n\n')
    for id, recurrences in matched_ids:       
        if recurrences >= 2:
            row = db_commands.get_row_from_ID(conn, id)
            gene = db_commands.uniprotid_to_gene_name(conn, row[1])
            try:
                note = Mutation.get_note(id, conn)
            except AttributeError as e:
                note = ''
            writer.writerow([id, gene, row[3], note, recurrences])

    
    #ID GENE REGION NOTE(POSSIBLE) RECURRENCES
    #id gene row[3] note recurrences

def features_affected_to_xl(file):
    workbook = Workbook(file[:-4] + '.xlsx')
    worksheet = workbook.add_worksheet()
    with open(file, 'rt', encoding='utf8') as f:
        reader = csv.reader(f, delimiter='\t')
        for r, row in enumerate(reader):
            for c, col in enumerate(row):
                worksheet.write(r, c, col)
    workbook.close()