import DBCreator, GFFParser
import logging

logging.basicConfig(level=logging.INFO)

file_gff = "uniprot-yourlist chr1p36.gff"
file_mapping = "uniprot-mpngtbl-1p36.tab"
db_file = r"F:\Skolgrejer\LÄKARPROGRAMMET\SOFOSKO\Databases\pythonsqlite.db"

conn = DBCreator.create_connection(db_file)
logging.info("created connection")
DBCreator.create_table(conn,DBCreator.create_table_data)
DBCreator.create_table(conn,DBCreator.create_table_mapping)
logging.info("Created tables")

for i in enumerate(GFFParser.GFFParse(file_gff)):
    data_tuple = (i[0],) + i[1][1]
    logging.debug("Attempting to insert data:\n%s", data_tuple)
    DBCreator.create_data(conn, data_tuple)
    if (i[0]+1) % 1000 == 0:
        logging.info("Inserted 1000 rows into data table")
logging.info("Inserted data")

for i in enumerate(GFFParser.map_parse(file_mapping)):
    map_data = (i[0]-1,) + tuple(i[1])
    if i[0] == 0:
        continue
    DBCreator.create_mapping(conn, map_data)
    if (i[0]+1) % 1000 == 0:
        logging.info("Inserted 1000 rows into mapping table")
logging.info("Inserted mapping")

logging.info("Finished the code")