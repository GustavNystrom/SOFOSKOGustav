import re
import numpy as np

class Mutation:

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

        exp = '(\D*)(\d*)'
        if self.varclass == "Missense_Mutation" or self.varclass == "Silent":
            try:
                site = int(self.hgvspshort[3:-1])
                site = (site, site)
            except:
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
                site = np.NaN
        
        #TODO: Define the site better. Perhaps the entire protein, perhaps from the start to the end of the protein?
        elif self.varclass == "Frame_Shift_Del" or self.varclass == "Frame_Shift_Ins":   
            try:
                matches = re.findall(exp, self.hgvspshort)
                site = (int(matches[0][1]), int(matches[1][1])+int(matches[0][1]))
            except (TypeError) as e:
                print('Missing data')
                site = np.NaN
            except:
                # If it creates an early termination!
                site = (int(matches[0][1]), np.NaN)
        
        elif self.varclass == "In_Frame_Del":
            matches = re.findall(exp, self.hgvspshort)
            site = (int(matches[0][1]), int(matches[0][1]))

        elif self.varclass == "In_Frame_Ins":
            matches = re.findall(exp, self.hgvspshort)
            if matches[1][1] == '':
                site = (int(matches[0][1]), int(matches[0][1]))
            else:
                site = (int(matches[0][1]), int(matches[1][1]))
        
        #TODO: Try to understand what to do with these better...
        elif self.varclass == "Translation_Start_Site" or self.varclass == "Nonstop_Mutation":
             site = np.NaN
        else:
            print('Unknown mutation type')
            site = np.NaN
        
        return site