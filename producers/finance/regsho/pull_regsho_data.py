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

def load_data(db_path='./stonk.duckdb'):
    con = duckdb.connect(database=db_path, read_only=False)
    df = con.execute(f"""
        SELECT Date, Symbol FROM regsho_daily
        WHERE Symbol IN ({ticker_fam})
    """).fetchdf()
    con.close()
    return df

def transform_data(df):
    # Ensure Date column is of datetime type
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Create a pivot table
    pivot_df = pd.pivot_table(df, 
                              values='Company', 
                              index='Symbol', 
                              columns='Date', 
                              aggfunc='count', 
                              fill_value=0)
    
    # Create a cumulative sum for each company
    pivot_df = pivot_df.cumsum(axis=1)
    
    return pivot_df



def save_to_csv(df, file_path='heatmap_data.csv'):
    df.to_csv(file_path)



# Example usage
df = load_data()
transformed_df = transform_data(df)
save_to_csv(transformed_df)


###################
# PLOT ZEE DATA
###################

def plot_heatmap(df):

    df.set_index('Symbol', inplace=True)
    # Plot the heat map
    plt.figure(figsize=(10, 6))
    ax = sns.heatmap(df, annot=True, cmap='YlGnBu', fmt='d', linewidths=0.5)

    # Customizing the plot
    ax.set_title('Heat Map of Cumulative Occurrences')
    ax.set_xlabel('Date')
    ax.set_ylabel('Company')

    plt.xticks(rotation=45)
    plt.yticks(rotation=0)

    # Show the plot
    plt.tight_layout()
    plt.show()


plot_heatmap(transformed_df)