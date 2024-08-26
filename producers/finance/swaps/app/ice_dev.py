import pandas as pd
from io import StringIO
import csv
import requests
import time
from clickhouse_connect import get_client as ch

from sources import sources

print(sources)


def get_ice_token():
    # Initialize a session
    session = requests.Session()

    # URL to access the portal or obtain the initial cookie
    initial_url = "https://tradevault.ice.com/tvsec/ticker/webpi/getToken"

    # Optional: Provide headers if required (replicate browser headers as needed)
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15"
    }

    # Make the initial request to establish a session and get cookies
    response = session.post(initial_url, headers=headers)

    if response.status_code == 200:
        # Extract token if needed
        token = response.json().get('token')
        print("Token obtained:", token)
        return token
    else:
        print(f"Failed to obtain the token. Status code: {response.status_code}")
        exit()
    

def pull_csv_from_url(url, token):
    retries = 0
    max_retries=1
    backoff_factor=1

    while retries < max_retries:
        try:
            session = requests.Session()
            # Update headers to include Authorization if required
            session.headers.update({
                "Authorization": f"Bearer {token}"
            })
            response = session.get(url)
            if response.status_code == 200:
                data = StringIO(response.text)
                csvreader = csv.reader(data)
                # nested = [row for row in csvreader]
                df = pd.read_csv(data, sep=',')                
                return df
                # return nested
             
            elif response.status_code == 404:
                print(f"Error 404: Data not found for {datestring}.")
                return None  # Exit if data is not found
            else:
                print(f"Received status code {response.status_code}. Retrying...")
        except requests.RequestException as e:
            print(f"Error fetching data from {url}: {e}")
        retries += 1
        time.sleep(backoff_factor * retries)  # Exponential backoff
    print("Max retries reached. Failed to fetch data.")


def prep_origin_df(df, url, datestring):
    df.columns = df.columns.str.strip().str.replace(' ', '_').str.replace('_-_','_').str.replace('-','_').str.replace('/','_')  # Remove spaces from column names
    df = df.astype(str)
    df.replace('nan', None, inplace=True)

    df['Report_Date'] = datestring
    df['Source_URL'] = url
    return df

def prep_origin_list(table_name, rows, url, datestring, schema_dict, settings):
    '''Expects rows to be a list of lists, which are each a row'''
    flattened_values = tuple(item for row in rows for item in row)
    num_columns = len(rows[0])
    placeholders = ', '.join(['%s'] * num_columns)
    values_placeholders = ', '.join([f'({placeholders})'] * len(rows))

    # Flatten lists to string
    # values = ', '.join([
    #                         f"""(
    #                             {
    #                                 ', '.join([
    #                                     "NULL" if value is None else f'{value}' for value in row
    #                                 ])
    #                             }
    #                         )""" 
    #                     for row in rows[1:]
    #                 ])

    # Generate VALUES string
    values = ', '.join(
        f"""({', '.join(['NULL' if value == '' else f"'{value.replace('(','').replace(')','')}'"
                for value in row])})"""
        for row in rows[1:]
    )

    columns = ", ".join([f"`{col_name.replace(' ', '_').replace('_-_','_').replace('-','_').replace('/','_')}` {col_type}" for col_name, col_type in schema_dict.items()])

    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])
    
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns}
        ) ENGINE = MergeTree()
        ORDER BY tuple()
    """
    print("\nRunning query: \n ", create_table_query)
    ch_conn.command(create_table_query)

    insert_query = f"""
            INSERT INTO {table_name} ({columns}) VALUES {values}
        """
    print("\nRunning insert query: ", insert_query)
    ch_conn.command(insert_query)


def create_table_from_dict(schema_dict, table_name, settings):
    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])
    columns_str = ", ".join([f"`{col.replace(' ', '_').replace('_-_','_').replace('-','_').replace('/','_')}` {coltype}" for col, coltype in schema_dict.items()])
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns_str}
        ) ENGINE = MergeTree()
        ORDER BY (Event_timestamp);
    """
    print("\nRunning query: \n", create_table_query)

    ch_conn.command(create_table_query)

def create_table_from_df(df, table_name, schema_dict, settings):
    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])
    
    columns = []
    print(f"Creating clickhouse table for {table_name}, and generating schema from pandas dtypes")
    for col_name, dtype in zip(df.columns, df.dtypes):
        if "int" in str(dtype):
            ch_type = "Int64"
        elif "float" in str(dtype):
            ch_type = "Float64"
        elif "datetime64" in str(dtype):
            ch_type = "DateTime"
        elif "object" in str(dtype):
            ch_type = "String"
        elif "bool" in str(dtype):
            ch_type = "Bool"
        else:
            ch_type = "String"  # Default to String for other types
        columns.append(f"`{col_name}` {ch_type}")
    print("Generated schema: ", columns)            # Skipping schema generation on first load to ensure all data is inserted
    # columns_str = ", ".join(columns)

    columns_str = ", ".join([f"'{col}' {coltype}" for col, coltype in schema_dict.items()])
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns_str}
        ) ENGINE = MergeTree()
        ORDER BY tuple()
    """
    print("\nRunning query: \n", create_table_query)
    ch_conn.command(create_table_query)
    print("\nTable created")

def df_to_clickhouse(df, table_name, settings):
    print(f"\nConnecting to {settings['host']} table: {table_name} with settings\n{settings}")
    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])

    if df.empty:
        print("DataFrame is empty. Skipping insertion.")
        return

    # create_table_from_df(df, table_name=table_name, settings=settings)
    print("\n\nInserting from df: ", df)
    ch_conn.insert_df(table_name, df)
    print("\nSuccess")


def drop_tables(table_names, settings):
    print(f"\nConnecting to {settings['host']} with settings\n{settings}")
    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])

    for table in table_names:
        ch_conn.command(f""" DROP TABLE {table};""")


### Now the data is in a table, but needs to be typecast

def ch_typecast(og_table, new_table, settings, desired_schema):
    print(f"\nConnecting to {settings['host']} with settings\n{settings}")
    ch_conn = ch(host=settings['host'], port=settings['port'], username=settings['username'], database=settings['database'])

    current_schema_query = f"DESCRIBE TABLE {og_table}"

    current_schema = ch_conn.query(current_schema_query).result_rows

    # Create a dictionary from the current schema
    current_schema_dict = {row[0]: row[1] for row in current_schema}
    print('\n current schema:\n', current_schema_dict)

    columns_str = ", ".join([f"`{col_name.replace(' ', '_').replace('_-_','_').replace('-','_').replace('/','_')}` {col_type}" for col_name, col_type in desired_schema.items()])

    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {new_table} (
            {columns_str}
        ) ENGINE = MergeTree()
        ORDER BY tuple()
    """

    print("\nRunning query: \n ", create_table_query)
    ch_conn.command(create_table_query)

    print("\nSuccessfully created table")
    # Modify the copy data query to include the necessary transformation
    select_columns = []
    for col_name, col_type in current_schema_dict.items():
        print(col_name)
        col_name = col_name.replace(' ', '_').replace('_-_','_').replace('-','_')
        if 'timestamp' in col_name:
            print("\n\n\n\n\n",col_name)
            select_columns.append(f"toDateTime64(replace(`{col_name}`, 'Z', ''), 3) AS `{col_name}`")
        else:
            select_columns.append(f"`{col_name}`")

    copy_data_query = f"""
        INSERT INTO {new_table} ({", ".join([f"{col.replace('_-_','_').replace('-','_').replace('/','_').replace(' ', '_')}" for col in desired_schema.keys()])})
        SELECT {", ".join(select_columns)} FROM {og_table}
    """
    print("\nRunning copy query: ", copy_data_query)
    ch_conn.command(copy_data_query)

    print("\nSuccess")



schema_dict = {
    'Cleared': 'Nullable(String)',
    'Custom_basket_indicator': 'Nullable(String)',
    'Action_type': 'Nullable(String)',
    'Event_type': 'Nullable(String)',
    'Amendment_indicator': 'Nullable(String)',
    'Event_timestamp': 'String',
    'Notional_amount': 'Nullable(String)',
    'Notional_currency': 'Nullable(String)',
    'Notional_amount_schedule_-_notional_amount_in_effect_on_associated_effective_date': 'Nullable(String)',
    'Notional_amount_schedule_-_unadjusted_effective_date_of_the_notional_amount': 'Nullable(String)',
    'Notional_amount_schedule_-_unadjusted_end_date_of_the_notional_amount': 'Nullable(String)',
    'Call_amount': 'Nullable(String)',
    'Call_currency': 'Nullable(String)',
    'Put_amount': 'Nullable(String)',
    'Put_currency': 'Nullable(String)',
    'Package_indicator': 'Nullable(String)',
    'Package_transaction_price': 'Nullable(String)',
    'Package_transaction_price_currency': 'Nullable(String)',
    'Package_transaction_price_notation': 'Nullable(String)',
    'Package_transaction_spread': 'Nullable(String)',
    'Package_transaction_spread_currency': 'Nullable(String)',
    'Package_transaction_spread_notation': 'Nullable(String)',
    'Day_count_convention': 'Nullable(String)',
    'Floating_rate_reset_frequency_period': 'Nullable(String)',
    'Floating_rate_reset_frequency_period_multiplier': 'Nullable(String)',
    'Other_payment_type': 'Nullable(String)',
    'Other_payment_amount': 'Nullable(String)',
    'Other_payment_currency': 'Nullable(String)',
    'Payment_frequency_period': 'Nullable(String)',
    'Payment_frequency_period_multiplier': 'Nullable(String)',
    'Fixed_rate': 'Nullable(String)',
    'Post-priced_swap_indicator': 'Nullable(String)',
    'Spread': 'Nullable(String)',
    'Spread_currency': 'Nullable(String)',
    'Spread_notation': 'Nullable(String)',
    'Strike_price': 'Nullable(String)',
    'Strike_price_currency/currency_pair': 'Nullable(String)',
    'Strike_price_notation': 'Nullable(String)',
    'Option_premium_amount': 'Nullable(String)',
    'Option_premium_currency': 'Nullable(String)',
    'First_exercise_date': 'Nullable(String)',
    'Embedded_option_type': 'Nullable(String)',
    'Settlement_currency': 'Nullable(String)',
    'Settlement_location': 'Nullable(String)',
    'Non-standardized_term_indicator': 'Nullable(String)',
    'Block_trade_election_indicator': 'Nullable(String)',
    'Effective_date': 'Nullable(String)',
    'Expiration_date': 'Nullable(String)',
    'Execution_timestamp': 'Nullable(String)',
    'Platform_identifier': 'Nullable(String)',
    'Prime_brokerage_transaction_indicator': 'Nullable(String)',
    'Classification': 'Nullable(String)',
    'Reference_Entity_Name': 'Nullable(String)',
    'Reference_Entity_Ticker': 'Nullable(String)',
    'Seniority': 'Nullable(String)',
    'Restructuring': 'Nullable(String)',
    'Scheduled_Termination_Date': 'Nullable(String)',
    'Contract_Type': 'Nullable(String)',
    'Dissemination_identifier': 'Nullable(String)',
    'Original_dissemination_identifier': 'Nullable(String)',
    'Dissemination_timestamp': 'Nullable(String)',
    'Unique_product_identifier': 'Nullable(String)',
    'Report_Date': 'Nullable(String)',
    'Source_URL': 'Nullable(String)'
}


schema_dict_2 = {
    'Cleared': 'Nullable(String)',
    'Custom_basket_indicator': 'Nullable(String)',
    'Action_type': 'Nullable(String)',
    'Event_type': 'Nullable(String)',
    'Amendment_indicator': 'Nullable(String)',
    'Event_timestamp': 'Datetime64',
    'Notional_amount': 'Nullable(Float64)',
    'Notional_currency': 'Nullable(String)',
    'Notional_amount_schedule_-_notional_amount_in_effect_on_associated_effective_date': 'Nullable(Float64)',
    'Notional_amount_schedule_-_unadjusted_effective_date_of_the_notional_amount': 'Nullable(Date)',
    'Notional_amount_schedule_-_unadjusted_end_date_of_the_notional_amount': 'Nullable(Date)',
    'Call_amount': 'Nullable(Float64)',
    'Call_currency': 'Nullable(String)',
    'Put_amount': 'Nullable(Float64)',
    'Put_currency': 'Nullable(String)',
    'Package_indicator': 'Nullable(String)',
    'Package_transaction_price': 'Nullable(Float64)',
    'Package_transaction_price_currency': 'Nullable(String)',
    'Package_transaction_price_notation': 'Nullable(String)',
    'Package_transaction_spread': 'Nullable(Float64)',
    'Package_transaction_spread_currency': 'Nullable(String)',
    'Package_transaction_spread_notation': 'Nullable(String)',
    'Day_count_convention': 'Nullable(String)',
    'Floating_rate_reset_frequency_period': 'Nullable(String)',
    'Floating_rate_reset_frequency_period_multiplier': 'Nullable(Float64)',
    'Other_payment_type': 'Nullable(String)',
    'Other_payment_amount': 'Nullable(Float64)',
    'Other_payment_currency': 'Nullable(String)',
    'Payment_frequency_period': 'Nullable(String)',
    'Payment_frequency_period_multiplier': 'Nullable(Int)',
    'Fixed_rate': 'Nullable(String)',
    'Post-priced_swap_indicator': 'Nullable(String)',
    'Spread': 'Nullable(Float64)',
    'Spread_currency': 'Nullable(String)',
    'Spread_notation': 'Nullable(String)',
    'Strike_price': 'Nullable(Float64)',
    'Strike_price_currency/currency_pair': 'Nullable(String)',
    'Strike_price_notation': 'Nullable(String)',
    'Option_premium_amount': 'Nullable(Float64)',
    'Option_premium_currency': 'Nullable(String)',
    'First_exercise_date': 'Nullable(Date)',
    'Embedded_option_type': 'Nullable(String)',
    'Settlement_currency': 'Nullable(String)',
    'Settlement_location': 'Nullable(String)',
    'Non-standardized_term_indicator': 'Nullable(String)',
    'Block_trade_election_indicator': 'Nullable(String)',
    'Effective_date': 'Nullable(Date)',
    'Expiration_date': 'Nullable(Date)',
    'Execution_timestamp': 'Nullable(Datetime64)',
    'Platform_identifier': 'Nullable(String)',
    'Prime_brokerage_transaction_indicator': 'Nullable(String)',
    'Classification': 'Nullable(String)',
    'Reference_Entity_Name': 'Nullable(String)',
    'Reference_Entity_Ticker': 'Nullable(String)',
    'Seniority': 'Nullable(String)',
    'Restructuring': 'Nullable(String)',
    'Scheduled_Termination_Date': 'Nullable(Date)',
    'Contract_Type': 'Nullable(String)',
    'Dissemination_identifier': 'Nullable(String)',
    'Original_dissemination_identifier': 'Nullable(String)',
    'Dissemination_timestamp': 'Nullable(String)',
    'Unique_product_identifier': 'Nullable(String)',
    'Report_Date': 'Nullable(String)',
    'Source_URL': 'Nullable(String)'
}



ch_settings = {
    'host': '192.168.8.246',
    'port': 8123,
    'database': 'default',
    'username': 'default',
    'password': ''
}

token = get_ice_token()
url_datestring = '2024-07-31'
url = f'https://tradevault.ice.com/tvsec/ticker/webpi/exportTicks?date={url_datestring}'
df = pull_csv_from_url(url=url, token=token)

origin_df = prep_origin_df(df=df, url=url, datestring=url_datestring)

print(origin_df.head(5))

# prep_origin_list(table_name='isr', rows=df, url=url, datestring=url_datestring, schema_dict=schema_dict, settings=ch_settings)
print('\n\n\nyeeeee\n\n\n')

drop_tables(table_names=['isr', 'swaps_ice'], settings=ch_settings)
# Create table and insert with all data as string type
create_table_from_dict(schema_dict=schema_dict, table_name='isr', settings=ch_settings)

df_to_clickhouse(df=origin_df, table_name='isr', settings=ch_settings)


ch_typecast('isr', 'Swaps_ICE_SEC', ch_settings, schema_dict_2)