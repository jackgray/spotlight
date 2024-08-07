import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import duckdb
from api import regsho_by_range, pull_all, merge_tables



# df = load_finra_regsho()
data_sources = ['nasdaq', 'finra', 'nyse']
# data_sources = ['nyse']

###################
# GATHER ZEE DATA
###################

pull_all(data_sources=data_sources, start_date='20130101', end_date='20140201')

merge_tables()



###################
# EXPOLORE ZEE DATA
###################

ticker_fam = ['GME', 'KOSS', 'CHWY', 'XRT', 'MDY', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF']

def load_data(ticker_list, db_path='./stonk.duckdb'):
    con = duckdb.connect(database=db_path, read_only=False)
    ticker_list_str = ', '.join(f"'{ticker}'" for ticker in ticker_fam)
    df = con.execute(f"""
        SELECT Date, Symbol FROM regsho_daily

        WHERE Symbol IN ({ticker_list_str})
    """).fetchdf()
    con.close()
    return df


ticker_fam = ['GME', 'KOSS', 'CHWY', 'XRT', 'MDY', 'FNDA', 'IWB', 'IWM', 'IJH', 'VTI', 'VBR', 'VXF']
df = load_data(ticker_fam)

###################
# TRANSFORM ZEE DATA
###################

def heatmap_df(df):
    # Ensure Date column is of datetime type
    df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
    print('DataFrame after date conversion:')
    print(df.head())
    
    # Create a binary presence/absence matrix
    pivot_df = pd.crosstab(df['Symbol'], df['Date'])
    print('Pivot table (binary presence/absence):')
    print(pivot_df.head())
    
    # Create a cumulative sum for each company
    cumsum_df = pivot_df.cumsum(axis=1)
    
    # Replace values where there is no change with NaN
    diff_df = cumsum_df.diff(axis=1).fillna(0)
    heatmap_df = cumsum_df.where(diff_df > 0, '')
    
    print('Pivot table after cumulative sum with empty cells for unchanged values:')
    print(heatmap_df.head())
    
    return heatmap_df


def save_to_csv(df, file_path='regsho_stonks_output.csv'):
    df.to_csv(file_path)


print('loaded data: ', df)
transformed_df = heatmap_df(df)
print(transformed_df)
transformed_df.to_csv('regsho_stonks_heatmap.csv')


###################
# PLOT ZEE DATA
###################

def plot_heatmap(df):
    '''
    This function needs a lot of work
    '''

    # df.set_index('Symbol', inplace=True)
    # Plot the heat map
    plt.figure(figsize=(10, 6))
    ax = sns.heatmap(df, annot=True, cmap='YlGnBu', fmt='d', linewidths=0.5)

    # Customizing the plot
    ax.set_title('Heat Map of Cumulative Occurrences')
    ax.set_xlabel('Date')
    ax.set_ylabel('Symbol')

    plt.xticks(rotation=45)
    plt.yticks(rotation=0)

    # Show the plot
    plt.tight_layout()
    plt.show()
