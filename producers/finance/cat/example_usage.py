from api import cat_by_range, duckdb_to_clickhouse

db_path = '../../../data/stonk.duckdb'

ch_settings = {
    'host': '192.168.8.246',
    'port': 8123,
    'database': 'default',
    'username': 'default',
    'password': ''
}
# Pull tables from the ends of these pdf reports and load into duckdb
# https://www.catnmsplan.com/sites/default/files/2022-07/07.28.22-Monthly-CAT-Update.pdf


cat_by_range('20240812', 'yesterday', ch_settings=ch_settings, db_path=db_path)

# duckdb_to_clickhouse(db_path=db_path, ch_host=clickhouse_host, ch_user='default', ch_port=8123, ch_db='default')



# # Mapping of DuckDB data types to ClickHouse data types
# DUCKDB_TO_CLICKHOUSE_TYPE_MAP = {
#     'INTEGER': 'Int32',
#     'BIGINT': 'Int64',
#     'SMALLINT': 'Int16',
#     'TINYINT': 'Int8',
#     'BOOLEAN': 'UInt8',
#     'FLOAT': 'Float32',
#     'DOUBLE': 'Float64',
#     'VARCHAR': 'String',
#     'DATE': 'Date',
#     'TIMESTAMP': 'DateTime',
#     'TIME': 'String',  # ClickHouse does not have a native time type
#     'BLOB': 'String'   # or use FixedString(n) if you know the size
# }

# # Connect to DuckDB & CH
# duckdb_conn = duckdb.connect('../../../data/stonk.duckdb')
# ch_conn = ch(host='192.168.8.246', user='default', database='default')


# # Mapping of DuckDB data types to ClickHouse data types
# DUCKDB_TO_CLICKHOUSE_TYPE_MAP = {
#     'INTEGER': 'Int32',
#     'BIGINT': 'Int64',
#     'SMALLINT': 'Int16',
#     'TINYINT': 'Int8',
#     'BOOLEAN': 'UInt8',
#     'FLOAT': 'Float32',
#     'DOUBLE': 'Float64',
#     'VARCHAR': 'String',
#     'DATE': 'Date',
#     'TIMESTAMP': 'DateTime',
#     'TIME': 'String',  # ClickHouse does not have a native time type
#     'BLOB': 'String'   # or use FixedString(n) if you know the size
# }


# # Get the list of tables in DuckDB
# tables = duckdb_conn.execute("SHOW TABLES").fetchall()

# for table in tables:
#     table_name = table[0]
#     sanitized_table_name = table_name.replace(' ', '_')
    
#     # Drop the table in ClickHouse if it exists
#     drop_table_query = f"DROP TABLE IF EXISTS {sanitized_table_name}"
#     ch_conn.command(drop_table_query)
    
#     # Get the schema of the DuckDB table
#     schema = duckdb_conn.execute(f"DESCRIBE {table_name}").fetchall()
    
#     # Create ClickHouse table schema
#     clickhouse_columns = []
#     for column in schema:
#         column_name, duckdb_type = column[0], column[1]
#         clickhouse_type = DUCKDB_TO_CLICKHOUSE_TYPE_MAP.get(duckdb_type.upper(), 'String')  # Default to String if type is unknown
#         clickhouse_columns.append(f"`{column_name}` {clickhouse_type}")
    
#     # Create the table in ClickHouse
#     create_table_query = f"""
#     CREATE TABLE {sanitized_table_name} (
#         {', '.join(clickhouse_columns)}
#     ) ENGINE = MergeTree()
#     ORDER BY tuple()
#     """
#     ch_conn.command(create_table_query)
    
#     # Transfer data from DuckDB to ClickHouse
#     data = duckdb_conn.execute(f"SELECT * FROM {table_name}").fetchdf()

#     # Convert all numerical data to strings (or other necessary conversions)
#     for col in data.columns:
#         if data[col].dtype in ['int64', 'int32', 'int16', 'int8', 'float64', 'float32']:
#             data[col] = data[col].astype(str)
    
#     # Convert the DataFrame to a list of tuples
#     insert_data = [tuple(row) for row in data.itertuples(index=False, name=None)]
    
#     # Insert data into ClickHouse
#     ch_conn.insert(sanitized_table_name, insert_data)

# print("Data transfer complete!")