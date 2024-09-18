import pandas as pd
import argparse
import asyncio
from datetime import datetime

from spotlight_utils.main import get_token, create_table_from_dict, generate_datestrings, fetch_with_adaptive_concurrency
from config import clickhouse_schema_source as schema_dict

''' 
Usage:

python3.11 main.py. --start_date '20200101' --end_date 'today' --table_name 'Swaps_ICE_source_sept1'

'''



def get_unique_months(datestrings):
    # Strip the day and keep only year and month (YYYYmm)
    months = [datestring[:6] for datestring in datestrings]
    # Remove duplicates
    unique_months = sorted(set(months))
    return unique_months

def generate_urls(unique_months):
    urls = []
    
    for month_str in unique_months:
        # Parse date components from the month string (YYYYmm format)
        year = int(month_str[:4])
        month_num = int(month_str[4:6])
        monthstr = datetime(year, month_num, 1).strftime('%B')  # Full month name

        # Helper function to adjust month and year
        def adjust_month_year(month, year):
            if month > 12:
                month = 1
                year += 1
            elif month < 1:
                month = 12
                year -= 1
            return month, year

        # Citadel consistently mislabels their data outputs, so this generates URLs for the next, current year and the 3 preceding years
        for year1 in range(year+1, year - 4, -1):  # Current year and 3 preceding years
            for month_num1 in range(1, 13):  # Months from 1 to 12
                # Adjust year if necessary
                month_num1_adjusted, year1_adjusted = adjust_month_year(month_num1, year1)
                month_num1_str = f"{month_num1_adjusted:02d}"

                # Construct the URL
                # if str(year) == '2021':
                url = f'https://www.citadelsecurities.com/wp-content/uploads/sites/2/{year1_adjusted}/{month_num1_str}/TCDRG{year}{month_num:02d}.txt'
                urls.append(url)

                # elif str(year) == '2024':
                url = f'https://www.citadelsecurities.com/wp-content/uploads/sites/2/{year1_adjusted}/{month_num1_str}/{monthstr}-{year}_TCDRG-{year}{month_num:02d}.txt'                                    
                urls.append(url)
                url = f'https://www.citadelsecurities.com/wp-content/uploads/sites/2/{year1_adjusted}/{month_num1_str}/{monthstr}-{year}_TCDRG-{year}{month_num:02d}_Corrected.txt'                                    
                urls.append(url)
                # Brute forcing possible URL strings because inconsistent file formatting (sometimes month is left off the prefix of 'TCDRG')
                url = f'https://www.citadelsecurities.com/wp-content/uploads/sites/2/{year1_adjusted}/{month_num1_str}/TCDRG-{year}{month_num:02d}.txt'      
                urls.append(url)                              
                # else:
                #     print('Citadel changes their file naming format format, and url formatting has not yet added for this year.')

    unique_urls = list(set(urls))
    return sorted(unique_urls)


async def main(start_date='yesterday', end_date='today', schema_dict=schema_dict, table_name='Rule605', sep='|', **kwargs):
    datestrings = generate_datestrings(start_date=start_date, end_date=end_date)
    unique_months = get_unique_months(datestrings)
    urls = generate_urls(unique_months)
    
    print('\n\n\n\n', urls)
    create_table_from_dict(schema_dict=schema_dict, table_name=table_name, key_col='report_month')
    
    
    await fetch_with_adaptive_concurrency(
        urls=urls,
        sep=sep,
        table_name=table_name,
        chunk_size=100000,
        transform_func=transform_df
    )



import pandas as pd

def transform_df(df: pd.DataFrame, url: str) -> pd.DataFrame:
    ''' Pass this into fetch pipeline to transform dataframes mid-stream '''
    print("Transforming df ", len(df.columns), df)

    # Reset index and convert all columns to strings to avoid type conflicts
    df.reset_index(drop=True, inplace=True)
    try:
        df.columns = list(schema_dict.keys())
    except Exception as e:
        print(f"Error adjusting columns to schema: {e}")
        exit()

    df = df.astype(str)
    df.replace('nan', None, inplace=True)   # Ensure clickhouse handles null values properly

    print("Transformed DataFrame:\n", df.head())
    return df



def retry_callback():
    print("retry callback placeholder")

def success_callback():
    print("success callback placeholder")



def parse_args():
    parser = argparse.ArgumentParser(description="Fetch and process CSV data from ICE US SDR.")
    parser.add_argument('--start_date', type=str, default='20240101', help='Start date in YYYYMMDD format')
    parser.add_argument('--end_date', type=str, default='today', help='End date in YYYYMMDD format (or "today")')
    parser.add_argument('--table_name', type=str, default='Rule605', help='Table name for ClickHouse')

    return parser.parse_args()



if __name__ == "__main__":
    args = parse_args()
    asyncio.run(main(start_date=args.start_date, end_date=args.end_date, table_name=args.table_name))

