import sqlite3

def gene_name_to_uniprotID(conn, name):
    """
    :name: tuple
    :return: tuple
    """

    statement = '''
    SELECT uniprotID FROM mapping WHERE gene_name=?
    '''
    cur = conn.cursor()
    cur.execute(statement, (name,))
    return cur.fetchall()

if __name__ == "__main__":
    import DBCreator as db
    genes = ("AADACL3", "AADACL4", "ACAP3")
    conn = db.create_connection(r'F:\Skolgrejer\LÄKARPROGRAMMET\SOFOSKO\Databases\pythonsqlite.db')
    
    for gene in genes:
        print(gene)
        uni_id = gene_name_to_uniprotID(conn, gene)
        print(uni_id)
    conn.close()