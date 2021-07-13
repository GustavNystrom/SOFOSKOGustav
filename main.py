import DBCreator, settings, core, db_commands
import Mutation
import pandas as pd
import numpy as np
import os, logging, csv
import matplotlib.pyplot as plt



def main(maf, dir_loc=settings.dir_loc, db_name=settings.db_name):
    logging.basicConfig(level=logging.INFO, filename=os.path.join(dir_loc,settings.logging_name))
    df = pd.read_csv(maf, sep="\t")
    logging.info('Created dataframe from MAF-file')

    # Get database filepath
    db_file = os.path.join(dir_loc, db_name)

    conn = DBCreator.create_connection(db_file)
    logging.info(f'Connected to database: {db_file}')

    core.mutations_per_gene(df,settings.value_count_file_name, base_path=dir_loc)
    logging.info('Finished running mutations per gene')
    

    #Contains the matched rows with the id from the database match appended at the end
    matched_rows, missing_genes = Mutation.compare_mutations(df, conn)

    # Count of genes in the MAF-file missing from database


            #TODO: what to do with annotated_withinid??
    logging.info('Finished working through the dataframe')
    new_df = core.create_dataframe(matched_rows, settings.dataframe_filename, dir_loc)
    logging.info('Finished creating new dataframe')
    print(f"Identified {len(df)-missing_genes}/{len(df)} entries")
    print(f"Matched {len(new_df)} entries to new file")
    core.matched_mutations_per_gene(new_df, dir_loc=dir_loc)
    
    core.features_affected(new_df, conn, dir_loc=dir_loc)
    print(len(new_df))
    print('Finished analyzing!')

def create_gene_list(df, filename=settings.gene_list_name, dir_loc=settings.dir_loc):
    if not isinstance(df, pd.DataFrame):
        df = pd.read_csv(df, sep="\t")
    filename=os.path.join(dir_loc, filename)
    gene_list = core.get_gene_list(df)
    logging.info('Successfully created a gene list')
    core.gene_list(gene_list, filename)
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