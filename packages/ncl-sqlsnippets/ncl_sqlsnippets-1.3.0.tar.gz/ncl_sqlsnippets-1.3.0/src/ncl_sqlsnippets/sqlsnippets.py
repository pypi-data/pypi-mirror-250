from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import pandas as pd

#Builds connect string, given database details
def get_connection_string (server_address, database, server_type="mssql", driver="SQL+Server"):
    #In most cases only the address needs to be passed. While this is largely fixed, hardcoding this means it will appear if published publicly anywhere. 

    #server_type: 'mssql' unless NCL switches away from using Microsoft SQL
    #sever_address: for Microsoft SQL this is the Server Name when connecting to the server through Microsoft SQL Server Management Studio
    #driver: 'SQL+Server' unless NCL switches away from using Microsoft SQL
    conn_str = f"{server_type}://{server_address}/{database}?trusted_connection=yes&driver={driver}"

    return conn_str

#Connect to the database 
def connect_to_sql (conn_str):

    #Connect to DB Server using the connection string
    engine = create_engine(conn_str, use_setinputsizes=False)

    return engine

#Function that wraps the basic connection functions and returns the engine
def connect (server_address, database):

    #Get the connection string
    conn_str = get_connection_string (server_address, database)

    #Create the engine and return it
    return connect_to_sql (conn_str)

#Take provided data and upload it to MSSQL
def upload_to_sql (data, engine, table, schema, replace, chunks=100, dtypes={}):

    #Determine if the data is appending or replacing
    if replace:
        if_exists = "replace"
    else:
        if_exists = "append"

    #the to_sql function commits
    data.to_sql(table, engine, schema=schema, if_exists=if_exists, index=False, chunksize=chunks, method='multi', dtype=dtypes)

#List all tables in the given database
def list_all_tables (engine):

    #Connect to engine
    with engine.connect() as connection:
        # Execute a query and fetch the result
        query = "SELECT s.name AS SchemaName, t.name AS TableName FROM sys.schemas AS s INNER JOIN sys.tables AS t ON s.schema_id = t.schema_id ORDER BY s.name, t.name;"
        result = connection.execute(text(query))
        
        # Fetch all rows from the result into a list of tuples
        rows = result.fetchall()

        # Get column names from the result's keys
        columns = result.keys()

    # Create a pandas DataFrame from the rows and columns
    return pd.DataFrame(rows, columns=columns)

#Returns a boolean value saying if the supplied schema and table exists in the database
def table_exists(engine, table, schema):

    all_tables = list_all_tables(engine)

    return all_tables.isin([schema, table]).all(axis=1).any()

#Creates a back of the named table
#Back up the table specified (Backup name for TABLE: TABLE_Backup)
def backup_table (engine, table, schema):
    
    #Full table name
    full_table = "[" + schema + "].[" + table + "]"

    #Backup table name
    backup_table = "[" + schema + "].[" + table + "_backup]"

    #Drop the existing backup
    drop_query = "DROP TABLE IF EXISTS " + backup_table + ";"

    #Create the new backup
    backup_query = "SELECT * INTO " + backup_table + "FROM " + full_table + ";"

    #Execute queries
    with engine.connect() as connection:
        print("Begin backup")

        #Drop table query
        connection.execute(text(drop_query))

        #Backup query
        connection.execute(text(backup_query))

        #Commit changes
        connection.commit()

        print("Backup complete")

#Restore the table specified
def restore_table(engine, table, schema):

    #Check backup exists
    if table_exists(engine, table + "_backup", schema):

        #Full table name
        full_table = "[" + schema + "].[" + table + "]"

        #Backup table name
        backup_table = "[" + schema + "].[" + table + "_backup]"

        #Drop the existing table
        drop_query = "DROP TABLE IF EXISTS " + full_table + ";"

        #Restore from the existing backup
        restore_query = "SELECT * INTO " + full_table + "FROM " + backup_table + ";"

        #Execute queries
        with engine.connect() as connection:
            
            print("Begin restore from backup")

            #Drop table query
            connection.execute(text(drop_query))

            #Backup query
            connection.execute(text(restore_query))

            #Commit changes
            connection.commit()

            print("Table restored from backup")
    
    else:
        print(f"Backup table not found: {backup_table}")

#Returns a list of columns for a given table
def list_all_columns (engine, table, schema):
    with engine.connect() as connection:
        # Execute a query and fetch the result
        query = f"SELECT c.name FROM sys.tables AS t INNER JOIN sys.schemas s ON s.schema_id = t.schema_id INNER JOIN sys.all_columns AS c  ON t.object_id = c.object_id WHERE t.name = '{table}' AND s.name = '{schema}'"

        result = connection.execute(text(query))
        
        # Fetch all rows from the result into a list of tuples
        columns = [column[0] for column in result.fetchall()]

    # Create a pandas DataFrame from the rows and columns
    return pd.Series(columns)

#Given an array of columns, do they all exist in a given table
def columns_exist(engine, table, schema, columns):

    #Get columns from target table
    table_columns = list_all_columns(engine, table, schema)

    #track list of missing columns
    missing_columns = []

    #For each provided column
    for col in columns:
        #If it does not exist in the table, add it to the missing list
        if not table_columns.isin([col]).any():
            missing_columns.append(col)

    #Return the list of columns. If all columns are in the table the return is an empty list [] which can logically be treated as False
    return missing_columns

#Execute a generic sql query with no results
def execute_query (engine, query):
    
    #Establish connection
    with engine.connect() as connection:

        # Execute a query
        connection.execute(text(query))

        
        #Commit to reflect changes
        connection.commit()

#Execute a generic sql query with results
def execute_sfw (engine, query):
    #Establish connection
    with engine.connect() as connection:
        # Execute a query and fetch the result

        result = connection.execute(text(query))
        
        # Fetch all rows from the result into a list of tuples
        rows = result.fetchall()

        # Get column names from the result's keys
        columns = result.keys()

    # Create a pandas DataFrame from the rows and columns
    return pd.DataFrame(rows, columns=columns)

#Create a session (for manual commits)
def generate_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session, session.begin()

#Execute a non-sfw query for a given session
def execute_query_session (query, session):
    session.execute(text(query))

#Force commit after batch changes
def commit_changes(transaction):
    transaction.commit()