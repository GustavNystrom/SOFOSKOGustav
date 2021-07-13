import PySimpleGUI as sg
import main, testDB
import os.path

sg.theme('BluePurple')

layout = [[sg.Text('MAF-file location:')],
          [sg.Input(key='-MAF-'), sg.FileBrowse('Browse')],

          [sg.Text('GFF-file location:')],
          [sg.Input(key='-GFF-'), sg.FileBrowse('Browse')],

          [sg.Text('Mapping-file location:')],
          [sg.Input(key='-MAPPING-'), sg.FileBrowse('Browse')],

          [sg.Text('Database location:')],
          [sg.Input(key='-DB-'), sg.FileBrowse('Browse')],

          #[sg.Text('Gene list:')],
          #[sg.Input(key='-GENE_LIST-'), sg.FileBrowse('Browse')],

          [sg.Radio('MAF-analysis', "RADIO1", default=True, key='-MAF_analysis-'),
          sg.Radio('Create gene list', "RADIO1", key='-GENE_CREATE-'),
          sg.Radio('Create database', "RADIO1", key='-DB_CREATE-')],

          [sg.Button('Run'), sg.Button('Exit')]]

window = sg.Window('MAF analysis program', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    elif event == 'Run':
        if values['-MAF_analysis-']:
            if values['-MAF-'] == '' or values['-DB-'] == '':
                sg.popup('A MAF-file and a database has to be specified!')
                continue

            main.main(values['-MAF-'], dir_loc=os.path.dirname(values['-MAF-']),
            db_name=values['-DB-'])
        
        elif values['-GENE_CREATE-']:
            if values['-MAF-'] == '':
                sg.popup('A MAF-file has to be specified!')
                continue
            main.create_gene_list(values['-MAF-'], dir_loc=os.path.dirname(values['-MAF-']))
            sg.popup('''1. Go to:\n https://www.uniprot.org/uploadlists/ \n
            2. Upload your gene list file.
            3. FROM: Gene name (or geneID) \n TO: UniProtKB \n ORGANISM: Homo sapiens (human) [9606]. \n
            4. Download in GFF-format AND Mapping Table. \n\n
            Use these files to create the database!''')
        
        elif values['-DB_CREATE-']:
            if values['-GFF-'] == '' or values['-MAPPING-'] == '':
                sg.popup('A GFF and Mapping file has to be specified! Get them from uniprot using the gene list!')
                continue
            testDB.create_db(file_gff=values['-GFF-'],
            file_mapping=values['-MAPPING-'],
            dir_loc=os.path.dirname(values['-MAF-'])
            )
        

window.close()