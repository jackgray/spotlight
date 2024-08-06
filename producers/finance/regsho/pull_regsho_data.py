from api import regsho_by_range


related_tickers = ['GME', 'KOSS', 'CHWY', 'XRT', 'MDY', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF']



data_sources = ['nasdaq', 'finra', 'nyse']
# data_sources = ['finra']
def pull_all(data_sources):
    for data_source in data_sources:
       
        df = regsho_by_range(start_date='20140101', end_date='20190101', data_source=data_source, db_path='./gme.duckdb')
        if df:
            print("Some rows were not added to duckdb")
            print(df)
        else:
            print("All downloaded data was inserted successfully")



def merge_tables(tables):
    merge_tables_sql = f"""
            CREATE TABLE regsho_daily AS
            SELECT * FROM nasdaq_regsho_daily
            UNION ALL
            SELECT * FROM nyse_regsho_daily
            UNION ALL
            SELECT * FROM finra_regsho_daily
            ORDER BY Date;
        """
    con = duckdb()

# df = load_finra_regsho()
pull_all(data_sources)

# CREATE TABLE regsho_daily AS
# SELECT * FROM nasdaq_regsho_daily
# UNION ALL
# SELECT * FROM nyse_regsho_daily
# UNION ALL
# SELECT * FROM finra_regsho_daily
# ORDER BY Date;