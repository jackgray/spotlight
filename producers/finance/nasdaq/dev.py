from api import regsho_by_range
import duckdb

df = regsho_by_range('20240701', 'yesterday')

# Filter out the tickers you want to save
symbols = ['GME', 'XRT', 'KOSS']
def filter_symbols(df, symbols):
    return df[df['Symbol'].isin(symbols)]

df = filter_symbols(df, symbols)
df.to_csv('gme_regsho.csv')



# DuckDB is super lightweight and easy to download.
# It's an easy way to work with data that may be too large for a CSV, and 
# doesn't require the setup that most databases require. You can save tables as
# .duckdb files, CSV, parquet, json, or just about any filetype you wish and 
# query with the same syntax for all of them


def load_df_to_duckdb(df, table_name, db_path):
    con = duckdb.connect(database=db_path, read_only=False)
    # Check if the table exists
    table_exists = con.execute(f"""
        SELECT count(*)
        FROM information_schema.tables
        WHERE table_name = '{table_name}'
    """).fetchone()[0] == 1
    
    if table_exists:
        try:
            con.execute(f"""ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS "Unique product identifier" VARCHAR""")
        except Exception as e:
            print(e)
        # Insert data into the existing table
        con.execute(f"INSERT INTO {table_name} SELECT * FROM df")
    else:
        # Create a new table and insert data
        con.execute(f"CREATE TABLE {table_name} AS SELECT * FROM df")


load_df_to_duckdb(df, 'gme_regsho', './gme.duckdb')

# Now to query, download duckdb binary and run ./duckdb gme.ducksb from your terminal

# Run 'SELECT * FROM gme_regsho;' to see the entire table
# Use normal SQL queries to filter data like any other SQL database