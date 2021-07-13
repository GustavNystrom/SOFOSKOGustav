import sqlite3, os.path, logging
from sqlite3 import Error
import settings, GFFParser

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

def create_db(file_gff=os.path.join(settings.dir_loc, settings.gff_name), 
            file_mapping=os.path.join(settings.dir_loc, settings.mapping_name),
            db_file=settings.db_name,
            dir_loc=settings.dir_loc):
    logging.basicConfig(level=logging.INFO, filename=os.path.join(dir_loc,settings.logging_db_name))
    db_file = os.path.join(dir_loc, db_file)
    conn = create_connection(db_file)
    logging.info("created connection")
    create_table(conn,create_table_data)
    create_table(conn,create_table_mapping)
    logging.info("Created tables")
    for i in enumerate(GFFParser.GFFParse(file_gff)):
        data_tuple = (i[0],) + tuple(i[1])
        logging.debug(f"Attempting to insert data:\n{data_tuple}")
        create_data(conn, data_tuple)
        if (i[0]+1) % 1000 == 0:
            logging.info("Inserted 1000 rows into data table")
            print('Inserted 1000 rows into data table')
    logging.info("Inserted data")
    print("Inserted data")

    for i in enumerate(GFFParser.map_parse(file_mapping)):
        map_data = (i[0]-1,) + tuple(i[1])
        if i[0] == 0:
            continue
        create_mapping(conn, map_data)
        if (i[0]+1) % 1000 == 0:
            logging.info("Inserted 1000 rows into mapping table")
            print("Inserted 1000 rows into mapping table")
    logging.info("Inserted mapping")
    print("Inserted mapping")

    logging.info("Finished creating database")
    print('Finished creating database')



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