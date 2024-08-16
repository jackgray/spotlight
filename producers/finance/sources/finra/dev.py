from api import fetch_finra
from io import StringIO
# import polars as pl
import pandas as pd
import json
import duckdb

res = fetch_finra('data', 'otcmarket', 'regshodaily')
json = json.dumps(res, indent=2)
# print(json)
df = pd.read_json(json)
print(df)

def load_df_to_duckdb(df, table_name, db_path):
    con = duckdb.connect(database=db_path, read_only=False)
    # Check if the table exists
    table_exists = con.execute(f"""
        SELECT count(*)
        FROM information_schema.tables
        WHERE table_name = '{table_name}'
    """).fetchone()[0] == 1
    
    if table_exists:
        # Insert data into the existing table
        con.execute(f"INSERT INTO {table_name} SELECT * FROM df")
    else:
        # Create a new table and insert data
        con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")

load_df_to_duckdb(df, 'finra_regsho_daily', '../gme.duckdb')