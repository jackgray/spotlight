from api import regsho_by_range, pull_all, merge_tables


related_tickers = ['GME', 'KOSS', 'CHWY', 'XRT', 'MDY', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF']


# df = load_finra_regsho()
data_sources = ['nasdaq', 'finra', 'nyse']
# data_sources = ['nyse']
pull_all(data_sources, start_date='20140108', end_date='20190108')

merge_tables()
