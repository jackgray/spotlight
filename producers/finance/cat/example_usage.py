from api import cat_by_range

# Pull tables from the ends of these pdf reports and load into duckdb
# https://www.catnmsplan.com/sites/default/files/2022-07/07.28.22-Monthly-CAT-Update.pdf
cat_by_range('2024401', 'yesterday', db_path='../../../data/stonk.duckdb')


