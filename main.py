import DBCreator, settings, test2, test_script
import Mutation
import pandas as pd
import numpy as np
import os, logging, csv
import matplotlib.pyplot as plt



def main(maf):
    logging.basicConfig(level=logging.INFO, filename=os.path.join(settings.dir_loc,settings.logging_name))
    df = pd.read_csv(maf, sep="\t")
    logging.info('Created dataframe from MAF-file')

    # Get database filepath
    db_file = os.path.join(settings.dir_loc, settings.db_name)
    # get genenames
    #pass genenames to uniprot, get gff and mapping table
    # import to sqlite db
    # get location of mutation and see if it is in an annotated domain
    # if it is, add to new

    gene_list = test2.get_gene_list(df)
    logging.info('Successfully created a gene list')
    test2.gene_list(gene_list, settings.gene_list_name)
    logging.info(f'Successfully created a gene list file: {settings.gene_list_name}')

    conn = DBCreator.create_connection(db_file)
    logging.info(f'Connected to database: {db_file}')

    test2.mutations_per_gene(df,settings.value_count_file_name, base_path=settings.dir_loc)
    logging.info('Finished running mutations per gene')

    #Contains the matched rows with the id from the database match appended at the end
    matched_rows, missing_genes = Mutation.compare_mutations(df, conn)

    # Count of genes in the MAF-file missing from database


            #TODO: what to do with annotated_withinid??
    logging.info('Finished working through the dataframe')
    new_df = test2.create_dataframe(matched_rows, settings.dataframe_filename, settings.dir_loc)
    logging.info('Finished creating new dataframe')
    print(f"Identified {len(df)-missing_genes}/{len(df)} entries")
    print(f"Matched {len(new_df)} entries to new file")

    plt.bar(new_df['Hugo_Symbol'].value_counts()[0:settings.n_mutations].index,
    new_df['Hugo_Symbol'].value_counts()[0:settings.n_mutations])
    plt.title('Number of mutations matched to an annotated domain per gene')
    plt.ylabel('Number of mutations')
    plt.xlabel('Gene name')
    plt.show()
    features = []
    with open(os.path.join(settings.dir_loc, settings.features_affected), 'w') as file:
        for i in new_df['Matched_ID']:
            feature = test_script.get_feature(conn, i)
            # print(feature)
            # if feature in features:
            #     print('in')
            #     #dict = {feature: features[feature] + 1}
            #     #features.update(dict)
            #     features[feature] += 1
            #     print(features[feature])
            # else:
            #     features[feature] = 1
            features.append(feature)
        d = pd.Series(features)
        d.value_counts().to_csv(file,sep='\t')
        print(len(d))
        print(len(new_df))
            
        # writer = csv.writer(file, delimiter='\t')
        # for i in features.items():
        #     writer.writerow([i[0], i[1]])

if __name__ == "__main__":
    value_count_file_name = 'mutations_per_gene.txt'
    maf_location = r'C:\Users\gusny\OneDrive\Dokument\SOFOSKO\test_maf.txt'
    main(maf_location)
    #mutations_per_gene(pd.read_csv(maf_location, sep="\t"), value_count_file_name, base_path=os.path.dirname(maf_location))