import sqlite3, os
from sqlite3 import Error
import settings

#create a connection (new db if it doesn't exist)
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
        return conn
    except Error as e:
        print(e)
    # finally:
    #     if conn:
    #         conn.close()
    return conn

#function to create a table using a connection obj and an sql statement
def create_table(connection, table):
    try:
        c = connection.cursor()
        c.execute(table)
    except Error as e:
        print(e)


create_table_mapping = """
CREATE TABLE IF NOT EXISTS mapping (
    id integer PRIMARY KEY,
    gene_name text,
    uniprotID text REFERENCES data(uniprotID) 
)
"""

create_table_data = """
CREATE TABLE IF NOT EXISTS data (
    id integer PRIMARY KEY,
    uniprotID text,
    source text,
    feature text,
    start text, 
    end text,
    score text,
    strand text,
    phase text,
    attributes text
)
"""

def create_data(conn, data):
    sql = ''' INSERT INTO data(id,uniprotID,source,feature,start,end,score,strand,phase,attributes)
              VALUES(?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()

    return cur.lastrowid

def create_mapping(conn, mapping):
    sql = ''' INSERT INTO mapping(id,gene_name,uniprotID)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, mapping)
    conn.commit()

    return cur.lastrowid


if __name__ == '__main__':
    #create_connection(r"F:\Skolgrejer\LÄKARPROGRAMMET\SOFOSKO\Databases\pythonsqlite.db")
    db_file = os.path.join(settings.dir_loc, settings.db_name)
    create_table(create_connection(db_file), create_table_data)
    create_table(create_connection(db_file), create_table_mapping)