import test_script, DBCreator, GFFParser, settings
from Mutation import Mutation
import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt


def main(maf):
    df = pd.read_csv(maf, sep="\t")
    # get genenames
    #pass genenames to uniprot, get gff and mapping table
    # import to sqlite db
    # get location of mutation and see if it is in an annotated domain
    # if it is, add to new

    conn = DBCreator.create_connection(db_file)

    mutations_per_gene(df,settings.value_count_file_name, base_path=settings.dir_loc)
    # This variable contains all the mutations that is within an annotated domain
    #annotated_withinid = []

    #Contains the matched rows with the id from the database match appended at the end
    matched_rows = []
    for rown in range(len(df)):
        if rown % 1000 == 0:
            print(rown)
        #Create a mutation object for the current row
        row = Mutation(df.iloc[rown])

        #Get all the annotated rows from the database which maps to this gene
        uniprot_annotated = test_script.get_rows_from_gene_name(conn, row.gene)

        # iterate over the rows to find if the mutation is within an annotated domain
        for i in uniprot_annotated:
            
            
            #Get the start and end of the annotated region
            annotated_region = (int(i[4]),int(i[5]))

            #These conditions are setup to find if mutation is within an annotated domain
            # TODO: what to do if (int, np.NaN)??

            if row.mut_site is np.NaN:
                continue
            # TODO: define how to calculate if the mut_site is within the annotated region, see readme
            elif row.mut_site[0] <= annotated_region[0] and row.mut_site[1] >= annotated_region[0]: #1
                #annotated_withinid.append(i[0])
                match = df.iloc[rown].tolist()
                match.append(i[0])
                matched_rows.append(match)
            elif row.mut_site[0] <= annotated_region[1] and row.mut_site[1] >= annotated_region[1]: #2
                #annotated_withinid.append(i[0])
                match = df.iloc[rown].tolist()
                match.append(i[0])
                matched_rows.append(match)
            elif row.mut_site[0] <= annotated_region[1] and row.mut_site[0] is np.NaN: #3
                #annotated_withinid.append(i[0])
                match = df.iloc[rown].tolist()
                match.append(i[0])
                matched_rows.append(match)
            #TODO: what to do with annotated_withinid??
    new_df = create_dataframe(matched_rows, settings.dataframe_filename, settings.dir_loc)
    print(new_df.head())

def mutations_per_gene(dataframe, filename, base_path):
    # Supply the base_path to create the file in that directory
    file_name = os.path.join(base_path, filename)
    value_counts = dataframe['Hugo_Symbol'].value_counts()
    value_counts.to_csv(file_name, sep='\t', header=['Count'], index_label='Hugo_Symbol')
    plt.plot(value_counts.index.tolist()[0:settings.n_mutations], value_counts.tolist()[0:settings.n_mutations])
    plt.show()

def create_dataframe(data, filename, base_path):
    # Creates a dataframe and dumps it onto a csv with \t as separator. Returns the dataframe.
    dataf = pd.DataFrame(data, columns=settings.df_labels)
    file_name = os.path.join(base_path, filename)
    dataf.to_csv(file_name, sep='\t')
    return dataf

if __name__ == "__main__":
    value_count_file_name = 'mutations_per_gene.txt'
    maf_location = r'C:\Users\gusny\OneDrive\Dokument\SOFOSKO\test_maf.txt'
    db_file = r'C:\Users\gusny\OneDrive\Dokument\SOFOSKO\pythonsqlite.db'
    main(maf_location)
    #mutations_per_gene(pd.read_csv(maf_location, sep="\t"), value_count_file_name, base_path=os.path.dirname(maf_location))