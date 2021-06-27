import sqlite3, pprint

def gene_name_to_uniprotID(conn, name):
    """
    :name: string
    :return: list(tuple)
    """

    statement = '''
    SELECT uniprotID FROM mapping WHERE gene_name=?
    '''
    cur = conn.cursor()
    cur.execute(statement, (name,))
    return cur.fetchall()

def retrieve_gene(conn,name):
    statement = '''
    SELECT * FROM data WHERE uniprotID=?
    '''
    cur = conn.cursor()
    cur.execute(statement, (name,))
    return cur.fetchall()

def get_rows_from_gene_name(conn, name):
    uniID = gene_name_to_uniprotID(conn, name)
    rows = []
    for i in uniID:
        rows.append(retrieve_gene(conn,i[0]))
    
    try:
        return rows[0]
    except:
        #print("Can't find match for gene: ", name)
        return []

def get_row_from_ID(conn, id):
    statement = '''
    SELECT * FROM data WHERE id=?
    '''
    cur = conn.cursor()
    cur.execute(statement, (str(id),))
    return cur.fetchall()[0]

if __name__ == "__main__":
    import DBCreator as db
    gene = "AADACL3"
    conn = db.create_connection(r'C:\Users\gusny\OneDrive\Dokument\SOFOSKO\pythonsqlite.db')
    
    # for gene in genes:
    #     print(gene)
    #     uni_id = gene_name_to_uniprotID(conn, gene)
    #     print(uni_id)
    # conn.close()

    # uniprotid = gene_name_to_uniprotID(conn, gene)
    # print(uniprotid[0][0])
    # items = retrieve_gene(conn,uniprotid[0][0])
    # pprint.pprint(items)
    print(get_rows_from_gene_name(conn, 'PLCH2'))
    print(get_row_from_ID(conn, 5))