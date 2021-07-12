import DBCreator, settings, test2, test_script
import Mutation
import pandas as pd
import numpy as np
import os, logging, csv
import matplotlib.pyplot as plt
from collections import Counter


def main(maf, dir_loc=settings.dir_loc, db_name=settings.db_name):
    logging.basicConfig(level=logging.INFO, filename=os.path.join(dir_loc,settings.logging_name))
    df = pd.read_csv(maf, sep="\t")
    logging.info('Created dataframe from MAF-file')

    # Get database filepath
    db_file = os.path.join(dir_loc, db_name)

    conn = DBCreator.create_connection(db_file)
    logging.info(f'Connected to database: {db_file}')

    test2.mutations_per_gene(df,settings.value_count_file_name, base_path=dir_loc)
    logging.info('Finished running mutations per gene')
    

    #Contains the matched rows with the id from the database match appended at the end
    matched_rows, missing_genes = Mutation.compare_mutations(df, conn)

    # Count of genes in the MAF-file missing from database


            #TODO: what to do with annotated_withinid??
    logging.info('Finished working through the dataframe')
    new_df = test2.create_dataframe(matched_rows, settings.dataframe_filename, dir_loc)
    logging.info('Finished creating new dataframe')
    print(f"Identified {len(df)-missing_genes}/{len(df)} entries")
    print(f"Matched {len(new_df)} entries to new file")
    plt.bar(new_df['Hugo_Symbol'].value_counts()[0:settings.n_mutations].index,
    new_df['Hugo_Symbol'].value_counts()[0:settings.n_mutations])
    plt.title('Number of mutations matched to an annotated domain per gene')
    plt.ylabel('Number of mutations')
    plt.xlabel('Gene name')
    plt.show()
    plt.savefig(os.path.join(dir_loc, settings.matched_mut_per_gene_name))
    regions, sites, aa_modifications, domain_ids = [], [], [], []
    with open(os.path.join(dir_loc, settings.features_affected), 'w') as file:
        for i in new_df['Matched_ID']:
            i = i.split(',')
            for id in i:
                feature = test_script.get_feature(conn, id)
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
        # d = pd.Series(features)
        # d.value_counts().to_csv(file,sep='\t')
        print(len(new_df))

def create_gene_list(df, filename=settings.gene_list_name, dir_loc=settings.dir_loc):
    if not isinstance(df, pd.DataFrame):
        df = pd.read_csv(df, sep="\t")
    filename=os.path.join(dir_loc, filename)
    gene_list = test2.get_gene_list(df)
    logging.info('Successfully created a gene list')
    test2.gene_list(gene_list, filename)
    logging.info(f'Successfully created a gene list file: {settings.gene_list_name}')

if __name__ == "__main__":
    from datetime import datetime
    now = datetime.now()
    maf_location = r'F:\Skolgrejer\LÄKARPROGRAMMET\SOFOSKO\MAF\BGI_MAF_1p36.txt'
    create_gene_list(maf_location)
    main(maf_location)
    now2 = datetime.now()
    print(now2 - now)
    #mutations_per_gene(pd.read_csv(maf_location, sep="\t"), value_count_file_name, base_path=os.path.dirname(maf_location))