""" Accepts a GFF-file and creates a generator to iterate through each line.
returns a tuple with a dictionary and a tuple with the following keys:
'uniprotID'
'source'
'feature'
'start'
'end'
'score'
'strand'
'phase'
'attributes'
Note: to access the tuple: type GFFParse(filename)[0]
"""
import csv

filenametest = 'testfile.gff'
dict_keys = ['uniprotID',
'source',
'feature',
'start',
'end',
'score',
'strand',
'phase',
'attributes']

def GFFParse(filename):
    '''
    A generator parsing the GFF-file using the csv module. 
    Returns a dictionary with all its values as strings.
    '''
    with open(filename, 'r') as file:
        file_gen = csv.reader(file, delimiter='\t')
        for i in file_gen:
            if len(i) < 9:
                continue
            i_dict = dict(zip(dict_keys, i[0:9]))
            yield (i_dict, tuple(i[0:9]))

def map_parse(filename):
        with open(filename, 'r') as file:
            file_gen = csv.reader(file, delimiter='\t')
            for i in file_gen:
                yield i

def maf_parse(filename):
    with open(filename) as file:
        file_gen = csv.reader(file, delimiter="\t")
        for i in range(5):
            print(next(file_gen))

if __name__ == '__main__':
    # for i in GFFParse(filenametest):
    #     print(i)
    #     print('ok')
    map_parse(filenametest)