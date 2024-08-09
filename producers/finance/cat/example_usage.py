from api import cat_by_range, duckdb_to_clickhouse

db_path = '../../../data/stonk.duckdb'
clickhouse_host='192.168.8.246'
# Pull tables from the ends of these pdf reports and load into duckdb
# https://www.catnmsplan.com/sites/default/files/2022-07/07.28.22-Monthly-CAT-Update.pdf
# cat_by_range('2020701', 'yesterday', db_path=db_path)

duckdb_to_clickhouse(db_path=db_path, ch_host=clickhouse_host, ch_user='default', ch_port=8123, ch_db='default')

