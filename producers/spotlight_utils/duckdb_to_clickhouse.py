import duckdb
from clickhouse_connect import get_client as ch

db_path = '../../../data/stonk.duckdb'
# ddb_conn = duckdb.connect(db_path)



# Mapping DuckDB data types to ClickHouse data types
duckdb_to_clickhouse_type_mapping = {
    'INTEGER': 'Int32',
    'BIGINT': 'Int64',
    'VARCHAR': 'String',
    'FLOAT': 'Float32',
    'DOUBLE': 'Float64',
    # Add more mappings as needed
}

def map_duckdb_type_to_clickhouse(duckdb_type):
    return duckdb_to_clickhouse_type_mapping.get(duckdb_type, duckdb_type)


def duckdb_table_to_clickhouse(table, db_path='./default.duckdb'):
    """
    Load a DuckDB table into ClickHouse using Quackpipe for data transfer.

    Parameters:
    - duckdb_table_name: The name of the DuckDB table to transfer.
    - clickhouse_table_name: The name of the ClickHouse table to insert data into.
    - clickhouse_client: ClickHouse client instance.
    - quackpipe_command: Path to the Quackpipe binary (default 'quackpipe').
    """

    ddb_conn  = duckdb.connect(db_path)
    ch_conn = ch(host='192.168.8.246', user='default', database='default')
    
    # Get schema from DuckDB
    schema_info = ddb_conn.execute(f"DESCRIBE {table}").fetchall()
    
    # Construct schema string for ClickHouse
    schema_string = ', '.join([f"{col[0].replace(' ','_')} {map_duckdb_type_to_clickhouse(col[1])}" for col in schema_info])
    print("Schema String: ", schema_string)
    ch_conn.command(f"DROP TABLE IF EXISTS {table}")

    # Prepare the data transfer query for ClickHouse
    clickhouse_query = f"""
    CREATE TABLE IF NOT EXISTS {table} (
        {schema_string}
    ) ENGINE = Executable('quackpipe -stdin -format TSV', TSV, {schema_string}, (
        SELECT * FROM {table}
    ));
    """

    print("\nusing query: ", clickhouse_query, "\n\n")
    
    # Execute the query on ClickHouse
    ch_conn.query(clickhouse_query)
    

def load_all(db_path='./default.duckdb'):
    ddb_conn  = duckdb.connect(db_path)
    tables = ddb_conn.execute("SHOW TABLES").fetchall()
    ddb_conn.close()
    for table in tables:
        table_name = table[0]
        print(table_name)

        duckdb_table_to_clickhouse(table=table_name, db_path=db_path)


load_all(db_path=db_path)

# # Example usage
# if __name__ == "__main__":
#     # Initialize ClickHouse client
# Get the list of tables in DuckDB




