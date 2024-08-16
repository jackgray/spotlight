import duckdb
import os
import subprocess

# Define paths
duckdb_path = '../../../data/stonk.duckdbb'
export_dir = '../../../data/clickhouse_staging'

# Connect to DuckDB
con = duckdb.connect(duckdb_path)

# Get all tables
tables = con.execute("SHOW TABLES").fetchall()

# Export each table to CSV
for table in tables:
    table_name = table[0]
    csv_file = os.path.join(export_dir, f"{table_name}.csv")
    con.execute(f"COPY {table_name} TO '{csv_file}' (HEADER, DELIMITER ',')")

# Load CSV files into ClickHouse
for table in tables:
    table_name = table[0]
    csv_file = os.path.join(export_dir, f"{table_name}.csv")
    subprocess.run([
        'docker', 'exec', '-i', 'clickhouse', 'clickhouse-client',
        '--query', f"INSERT INTO {table_name} FORMAT CSVWithNames",
        f'<', csv_file
    ])
