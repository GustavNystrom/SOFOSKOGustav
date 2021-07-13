import re, logging
import numpy as np
import test_script
import settings
import pandas as pd

class Mutation:
    # Should initialize from a DataFrame wit the correct column labels to get the __init__ to work
    def __init__(self, row):
        self.gene = row['Hugo_Symbol']
        self.varclass = row['Variant_Classification']    
        self.hgvspshort = row['HGVSp_Short']
        self.mut_site = self.mut_site()
        self.row = row
    
    def parse_row(self):
        self.chr = self.row['Chromosome']
        self.startpos = self.row['Start_Position']
        self.endpos = self.row['End_Position']
        self.vartype = self.row['Variant_Type']
        self.refallele = self.row['Reference_Allele']
        self.mutallele = self.row['Tumor_Seq_Allele2']
        self.hgvsc = self.row['HGVSc']
        self.hgvsp = self.row['HGVSp']
    
    def mut_site(self):
        """returns (start,stop) of the mutation on protein level"""
        logging.debug(f"Varclass: {self.varclass}")
        exp = '(\D*)(\d*)'
        if self.varclass == "Missense_Mutation" or self.varclass == "Silent":
            try:
                site = int(self.hgvspshort[3:-1])
                site = (site, site)
            except:
                logging.warning(f"Failed to identify mut_site for {self.gene}\nhgvspshort = {self.hgvspshort}")
                #Missing data!
                site = np.NaN

        elif self.varclass == "RNA" or self.varclass == "Splice_Region" or self.varclass == "Splice_Site":
            site = np.NaN

        #TODO: Define the site better. Perhaps the entire protein, perhaps from the start to the end of the protein?
        elif self.varclass == "Nonsense_Mutation":
            try:
                matches = re.findall(exp, self.hgvspshort)
                site = (int(matches[0][1]),np.NaN)
            except Exception as e:
                logging.warning(f"Failed to identify mut_site for {self.gene}\nhgvspshort = {self.hgvspshort}\n Error: {e}")
                site = np.NaN
        
        #TODO: Define the site better. Perhaps the entire protein, perhaps from the start to the end of the protein?
        elif self.varclass == "Frame_Shift_Del" or self.varclass == "Frame_Shift_Ins":   
            try:
                matches = re.findall(exp, self.hgvspshort)
                site = (int(matches[0][1]), int(matches[1][1])+int(matches[0][1]))
            except (TypeError) as e:
                logging.warning(f'Missing data for {self.gene}\nHGVSpshort = {self.hgvspshort}')
                print('Missing data')
                site = np.NaN
            except:
                logging.debug(f'Created an early termination, hgvspshort={self.hgvspshort}')
                # If it creates an early termination!
                site = (int(matches[0][1]), np.NaN)
        
        elif self.varclass == "In_Frame_Del":
            try:
                matches = re.findall(exp, self.hgvspshort)
                site = (int(matches[0][1]), int(matches[0][1]))
            except (TypeError) as e:
                logging.warning(f'Missing data for {self.gene}\nHGVSpshort = {self.hgvspshort}')
                print('Missing data')
                site = np.NaN


        elif self.varclass == "In_Frame_Ins":
            
            try:
                matches = re.findall(exp, self.hgvspshort)
                if matches[1][1] == '':
                    site = (int(matches[0][1]), int(matches[0][1]))
                else:
                    site = (int(matches[0][1]), int(matches[1][1]))
            except (TypeError) as e:
                logging.warning(f'Missing data for {self.gene}\nHGVSpshort = {self.hgvspshort}')
                print('Missing data')
                site = np.NaN
        
        #TODO: Try to understand what to do with these better...
        elif self.varclass == "Translation_Start_Site" or self.varclass == "Nonstop_Mutation":
             site = np.NaN
        else:
            print('Unknown mutation type')
            site = np.NaN
        logging.debug(f'Finished identifying mut_site, mut_site={site}')
        return site


def compare_mutations(df, conn):
    missing_genes = 0
    matched_rows = []
    sep = ','
    #df = df.drop(df.loc[df['Variant_Classification'] == 'Silent'].index, 
    #inplace=False, axis=0)
    df2 = df.loc[df['Variant_Classification'] == 'Missense_Mutation']
    df3 = df.loc[df['Variant_Classification'] == 'In_Frame_Del']
    df4 = df.loc[df['Variant_Classification'] == 'In_Frame_Ins']
    df = pd.merge(df2, df3, how='outer')
    df = pd.merge(df, df4, how='outer')
    print(f"{len(df)} rows will be analyzed")
    for rown in range(len(df)):
        logging.debug(f'Started working on row number {rown}')
        if rown % 1000 == 0:
            print('Worked through row number: ', rown)
        #Create a mutation object for the current row
        row = Mutation(df.iloc[rown])
        #row_mut_site = _mut_site(row)
        logging.debug(f'Created a Mutation object from row {rown}')

        #Get all the annotated rows from the database which maps to this gene
        uniprot_annotated = test_script.get_rows_from_gene_name(conn, row.gene)
        if uniprot_annotated == []:
            missing_genes += 1
            logging.info('Missing gene appended. Continuing...')
            continue

        # iterate over the rows to find if the mutation is within an annotated domain
        logging.debug(f'Started trying to find a match for rown: {rown}')
        matches = []
        for i in uniprot_annotated:            
            if i[3] in settings.domains_skip:
                continue
                        
            #Get the start and end of the annotated region
            annotated_region = (int(i[4]),int(i[5]))
            logging.debug(f'Coordinates for annotated region mutation: {annotated_region}\nCoordinates for maf-mutation: {row.mut_site}')

            #These conditions are setup to find if mutation is within an annotated domain
            # TODO: what to do if (int, np.NaN)??

            if row.mut_site is np.NaN:
                logging.debug('mutation site for maf-mutation is undefined, continues...')
                continue
            elif i[3] == 'Disulfide bond':
                if annotated_region[0] in row.mut_site or annotated_region[1] in row.mut_site:
                    logging.debug('Disulfide bond matched')
                    matches.append(str(i[0]))
                    continue
            # TODO: define how to calculate if the mut_site is within the annotated region, see readme
            elif row.mut_site[0] <= annotated_region[0] and row.mut_site[1] >= annotated_region[1]: #1
                logging.debug('Mutation matched at condition 1')
                matches.append(str(i[0]))
                continue
            elif row.mut_site[0] <= annotated_region[1] and row.mut_site[0] >= annotated_region[0]: #2
                logging.debug('Mutation matched at condition 2')
                matches.append(str(i[0]))
                continue
            elif row.mut_site[1] <= annotated_region[1] and row.mut_site[1] >= annotated_region[0]: #3
                logging.debug('Mutation matched at condition 3')
                matches.append(str(i[0]))
                continue
            elif row.mut_site[0] <= annotated_region[1] and row.mut_site[1] is np.NaN: #4
                logging.debug('Mutation matched at condition 4')
                matches.append(str(i[0]))
                continue
            
        if matches != []:
            match = df.iloc[rown].tolist()
            matches = sep.join(matches)
            match.append(matches)
            matched_rows.append(match)
    return (matched_rows, missing_genes)


# Get the note for a domain
def get_note(id, conn):
    attrs = test_script.get_attributes(conn=conn, id=id)
    expression = 'Note=([^;]+)'
    match = re.compile(expression).match(attrs)
    return match.group(1)

# Obsolete, used if you want to get mut_site without creating a Mutation object first
def _mut_site(row):
    """returns (start,stop) of the mutation on protein level"""
    exp = '(\D*)(\d*)'
    varclass = row['Variant_Classification']
    hgvspshort = row['HGVSp_Short']
    logging.debug(f"Varclass: {varclass}")
    if varclass == "Missense_Mutation" or varclass == "Silent":
        try:
            site = int(hgvspshort[3:-1])
            site = (site, site)
        except:
            logging.warning(f"Failed to identify mut_site for {row['Hugo_Symbol']}\nhgvspshort = {hgvspshort}")
            #Missing data!
            site = np.NaN

    elif varclass == "RNA" or varclass == "Splice_Region" or varclass == "Splice_Site":
        site = np.NaN

    #TODO: Define the site better. Perhaps the entire protein, perhaps from the start to the end of the protein?
    elif varclass == "Nonsense_Mutation":
        try:
            matches = re.findall(exp, hgvspshort)
            site = (int(matches[0][1]),np.NaN)
        except Exception as e:
            logging.warning(f"Failed to identify mut_site for {row['Hugo_Symbol']}\nhgvspshort = {hgvspshort}\n Error: {e}")
            site = np.NaN

    #TODO: Define the site better. Perhaps the entire protein, perhaps from the start to the end of the protein?
    elif varclass == "Frame_Shift_Del" or varclass == "Frame_Shift_Ins":   
        try:
            matches = re.findall(exp, hgvspshort)
            site = (int(matches[0][1]), int(matches[1][1])+int(matches[0][1]))
        except (TypeError) as e:
            logging.warning(f"Missing data for {row['Hugo_Symbol']}\nHGVSpshort = {hgvspshort}")
            print('Missing data')
            site = np.NaN
        except:
            logging.debug(f'Created an early termination, hgvspshort={hgvspshort}')
            # If it creates an early termination!
            site = (int(matches[0][1]), np.NaN)

    elif varclass == "In_Frame_Del":
        matches = re.findall(exp, hgvspshort)
        site = (int(matches[0][1]), int(matches[0][1]))

    elif varclass == "In_Frame_Ins":
        matches = re.findall(exp, hgvspshort)
        if matches[1][1] == '':
            site = (int(matches[0][1]), int(matches[0][1]))
        else:
            site = (int(matches[0][1]), int(matches[1][1]))

    #TODO: Try to understand what to do with these better...
    elif varclass == "Translation_Start_Site" or varclass == "Nonstop_Mutation":
            site = np.NaN
    else:
        print('Unknown mutation type')
        site = np.NaN
    logging.debug(f'Finished identifying mut_site, mut_site={site}')
    return site