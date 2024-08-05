from api import load_df_to_duckdb
from producers.finance.sources.utils import regsho_by_range
from porducers.finance.sources.nyse.api import gen_nyse_regsho_url, load_df_to_duckdb
import duckdb

# If any data fails to load into duckdb, it will return as a dataframe
# note that large date ranges may consume exessive memory
df = regsho_by_range('20190101', '20240801', urlgen_func=gen_nyse_regsho_url, from_date_format='%Y%m%d', to_date_format='%d-%b-%Y', table_name='nyse_regsho', db_path='../gme.duckdb')

print(df)
df.to_csv('gme_regsho.csv')


