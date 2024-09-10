                        # KAFKA PRODUCER FUNCTION 


def transform_df(
    df: pd.DataFrame, 
    url: Required[str], 
    market: Required[str], 
    data_source: Required[str]) -> pd.DataFrame:
    '''
    Field definitions:  
    Nasdaq: https://www.nasdaqtrader.com/Trader.aspx?id=RegShoDefs
    NYSE: follows the same schema :) (also I can't find a data dict for it)
    FINRA: https://api.finra.org/metadata/group/otcMarket/name/thresholdListMock
    '''
    print(df)
    df = df.iloc[:-1]   # Remove the last line which is only datestring
    df['Source URL'] = url
    df['Market'] = market.replace('%20', ' ')
    # df['Date'] = pd.to_datetime(datestring, format='%Y%m%d') #.strptime('%Y-%m-%d').   

    acceptable_sources = ['nyse', 'nasdaq', 'finra']
    if data_source.lower() == 'nyse':
        df['Data_Provider'] = 'NYSE'
        # Make fields only provided by FINRA satisfy SQL dimension requirements
        df['FINRA_Rule_4320_Flag'] = ''
        df['Rule_3210'] = ' '
        df['Threshold_List_Flag'] = ' '
    elif data_source.lower() == 'cboe':
        df['Data_Provider'] = 'Cboe'
        df['Threshold_List_Flag'] = ' '
        df['Reg_SHO_Threshold_Flag'] = ' '
        df['Rule_3210'] = ' '
        df['FINRA_Rule_4320_Flag'] = ' '
        df['Market'] = 'BZX'
        df['Market_Category'] = ''
        df.rename(columns={'CompanyName':'Security Name'}, inplace=True)
        print("Changed cboe df ", df)
    elif data_source.lower() == 'nasdaq':
        df['Market'] = 'Nasdaq'
        df['Data_Provider'] = 'Nasdaq'
        df['Threshold_List_Flag'] = ' '
        df['FINRA_Rule_4320 Flag'] = ' '
    elif data_source.lower() == 'finra':    # Convert FINRA field names to NASDAQ/NYSE equivalents
        df['Data Provider'] = 'FINRA'
        df['Rule 3210'] = ' '
        column_map = {
            'tradeDate': 'Date',
            'issueSymbolIdentifier': 'Symbol',
            'issueName': 'Security Name',
            'marketClassCode': 'Market Category',
            'marketCategoryDescription': 'Market',
            'thresholdListFlag': 'Threshold List Flag',
            'regShoThresholdFlag': 'Reg SHO Threshold Flag',
            'rule4320Flag': 'FINRA Rule 4320 Flag'
        }

        print(f"\nRenaming column names of df: {df.columns} \n according to this map: {column_map}")
        df.rename(columns=column_map, inplace=True)
        print(f"\nRename successful - new column names: {df.columns}")
    else: 
        print(f"\nReceived unknown data source value: {data_source}. Please use one of {acceptable_sources}")
    

    drop_cols = [col for col in ['Filler', 'Filler.1'] if col in df.columns]    # NYSE/NASDAQ put in 'Filler' columns but don't use them. I haven't learned why yet, but we don't need to carry them over rn.
    df.drop(drop_cols, axis=1, inplace=True)    

    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)   # Remove spaces to the right and left of all values

    # Generate unique row ID programatically to avoid duplicate insertions
    print("\nGenerating ID string from data_source + Symbol + Date + Market Category")
    if len(df['Market_Category'][0]) > 0:
        market_tag = df['Market_Category'].str.replace(' ', '').str.lower()
    elif len(df['Market'][0])  > 0:
        market_tag = df['Market'].str.replace(' ', '').str.lower()
    else:
        print('No market identifier for ID formatting, need more unique points to make ID')
        return

    datestring = df['Date'].dt.strftime('%Y%m%d')

    df['ID'] = (data_source.lower() + df['Symbol'] + datestring + market_tag)

    df.reset_index(drop=True, inplace=True)    # drop the unecessary pandas index (which doesn't get inserted to duckdb)

    schema_mapping = {
        "ID": "str",
        "Date": "datetime64[ns]",
        "Symbol": "str",
        "Security_Name": "str",
        "Market_Category": "str",
        "Market": "str",
        "Reg_SHO_Threshold_Flag": "str",
        "Threshold_List_Flag": "str",
        "FINRA_Rule_4320_Flag": "str",
        "Rule_3210": "str",
        "Data_Provider": "str",
        "Source_Url": "str"
    }

    df = df.astype({col: dtype for col, dtype in schema_mapping.items() if col in df.columns})     # Assert data types for any df columns that exist in schema_mapping
    print("cleaned df:", df)

    return df
