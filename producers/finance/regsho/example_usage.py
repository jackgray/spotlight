import pandas as pd
# import seaborn as sns
# import matplotlib.pyplot as plt
from main import pull_all


# data_sources = ['nasdaq', 'finra', 'nyse', 'cboe']
data_sources = ['nasdaq', 'nyse', 'cboe']

###################
# GATHER ZEE DATA
###################

pull_all(start_date='20080101', end_date='20100101', data_sources=data_sources)

# merge_tables()

###################
# EXPOLORE ZEE DATA
###################

# def load_select(ticker_list, db_path='./stonk.duckdb'):
#     con = duckdb.connect(database=db_path, read_only=False)
#     ticker_list_str = ', '.join(f"'{ticker}'" for ticker in ticker_fam)
#     df = con.execute(f"""
#         SELECT Date, Symbol FROM regsho_daily

#         WHERE Symbol IN ({ticker_list_str})
#     """).fetchdf()
#     con.close()
#     return df

# def load_all_date_only(db_path='./stonk.duckdb'):
#     con = duckdb.connect(database=db_path, read_only=False)
#     df = con.execute(f"""
#         SELECT Date, Symbol FROM regsho_daily
#     """).fetchdf()
#     con.close()
#     return df

# def monthly_total(db_path='./stonk.duckdb'):
#     con = duckdb.connect(database=db_path, read_only=False)
#     df = con.execute(f"""
#         SELECT Month, Symbol, Market FROM monthly_totals
#     """).fetchdf()
#     con.close()
#     return df

# def weekly_total(db_path='./stonk.duckdb'):
#     con = duckdb.connect(database=db_path, read_only=False)
#     df = con.execute(f"""
#         SELECT Week, Symbol, Market FROM weekly_totals
#     """).fetchdf()
#     con.close()
#     return df


# ticker_fam = ['GME', 'KOSS', 'CHWY', 'AMC', 'BYON', 'OSTK', 'BBBY', 'TSLA', 'BNGE', 'XRT', 'RETL', 'IVOV', 'IJJ', 'MDYV', 'ISCV', 'XJH', 'IVOO', 'SPMD', 'IJH', 'MDY', 'VBR', 'ISCB', 'MVV', 'RWK', 'MIDU', 'VCR', 'SMLF', 'ISCG', 'VB', 'ESML', 'IYC', 'VXF','FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF']

# # df = monthly_total(db_path='./stonk.duckdb')
# # df = weekly_total(db_path='./stonk.duckdb')
# # df = load_all_date_only()

# ###################
# # TRANSFORM ZEE DATA
# ###################

# def heatmap_df(df):
#     # Ensure Date column is of datetime type
#     df['Month'] = pd.to_datetime(df['Month'], format='%Y-%m')
#     print('DataFrame after date conversion:')
#     print(df.head())
    
#     # Create a binary presence/absence matrix
#     pivot_df = pd.crosstab(df['Symbol'], df['Month'])
#     print('Pivot table (binary presence/absence):')
#     print(pivot_df.head())
    
#     # Create a cumulative sum for each company
#     cumsum_df = pivot_df.cumsum(axis=1)
    
#     # Replace values where there is no change with NaN
#     diff_df = cumsum_df.diff(axis=1).fillna(0)
#     heatmap_df = cumsum_df.where(diff_df > 0, '')
    
#     print('Pivot table after cumulative sum with empty cells for unchanged values:')
#     print(heatmap_df.head())
    
#     return heatmap_df


# def monthly_heatmap_df(df):
#     # Ensure Date column is of datetime type
#     df['Month'] = pd.to_datetime(df['Month'], format='%Y-%m')
#     print('DataFrame after date conversion:')
#     print(df.head())
    
#     # Create a binary presence/absence matrix
#     pivot_df = pd.crosstab(df['Symbol'], df['Month'])
#     print('Pivot table (binary presence/absence):')
#     print(pivot_df.head())
    
#     # Create a cumulative sum for each company
#     # cumsum_df = pivot_df.cumsum(axis=1)
    
#     # Replace values where there is no change with NaN
#     # diff_df = cumsum_df.diff(axis=1).fillna(0)
#     # heatmap_df = cumsum_df.where(diff_df > 0, '')
    
#     print('Pivot table after cumulative sum with empty cells for unchanged values:')
#     print(heatmap_df.head())
    
#     return heatmap_df


# def weekly_heatmap_df(df):
#     # Ensure Date column is of datetime type
#     df['Week'] = pd.to_datetime(df['Week'], format='%Y-%W')
#     print('DataFrame after date conversion:')
#     print(df.head())
    
#     # Create a binary presence/absence matrix
#     pivot_df = pd.crosstab(df['Symbol'], df['Week'])
#     print('Pivot table (binary presence/absence):')
#     print(pivot_df.head())
    
#     # Create a cumulative sum for each company
#     # cumsum_df = pivot_df.cumsum(axis=1)
    
#     # Replace values where there is no change with NaN
#     # diff_df = cumsum_df.diff(axis=1).fillna(0)
#     # heatmap_df = cumsum_df.where(diff_df > 0, '')
    
#     print('Pivot table after cumulative sum with empty cells for unchanged values:')
#     print(heatmap_df.head())
    
#     return heatmap_df

# # print('loaded data: ', df)
# # transformed_df = weekly_heatmap_df(df)
# # print(transformed_df)
# # transformed_df.to_csv('weekly_heatmap.csv')

# def insert_duckdb(df, table_name):    
#     con = duckdb.connect(database='./stonk.duckdb', read_only=False)
#     con.execute(f'''
#         CREATE OR REPLACE TABLE {table_name} AS (
#         SELECT * FROM df)
#     ''')

# # insert_duckdb(transformed_df, 'weekly_heatmap')