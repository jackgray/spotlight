import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import duckdb
from api import pull_all, merge_tables

ch_settings = {
    'host': '192.168.8.246',
    'port': 8123,
    'database': 'default',
    'username': 'default',
    'password': ''
}
db_source = 'DuckDB' # Change this to 'Clickhouse' if you have a Clickhouse endpoint to send the output to. 

# data_sources = ['nasdaq', 'finra', 'nyse', 'cboe']
data_sources = ['cboe']

###################
# GATHER ZEE DATA
###################

pull_all(data_sources=data_sources, ch_settings=ch_settings, start_date='20150902', end_date='today')
