from api import regsho_by_range
import duckdb

# If any data fails to load into duckdb, it will return as a dataframe
# note that large date ranges may consume exessive memory
df = regsho_by_range('20190101', '20240801', 'nyse_regsho', './gme.duckdb')
print(df)
# Filter out the tickers you want to save
# symbols = ['GME', 'KOSS', 'CHWY', 'XRT', 'MDY', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF']
# def filter_symbols(df, symbols):
#     return df[df['Symbol'].isin(symbols)]


# df = filter_symbols(df, symbols)
df.to_csv('gme_regsho.csv')


