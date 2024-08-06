from api import regsho_by_range, pull_all


related_tickers = ['GME', 'KOSS', 'CHWY', 'XRT', 'MDY', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF']





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
    # con = duckdb()

# df = load_finra_regsho()
data_sources = ['nasdaq', 'finra', 'nyse']
# data_sources = ['nyse']
pull_all(data_sources, start_date='20210725')

# CREATE TABLE regsho_daily AS
# SELECT * FROM nasdaq_regsho_daily
# UNION ALL
# SELECT * FROM nyse_regsho_daily
# UNION ALL
# SELECT * FROM finra_regsho_daily
# ORDER BY Date;