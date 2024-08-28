
''' Normalizes column names accross data repositories '''
from clickhouse_connect import get_client as ch
# from ice_dtcc_staging insert

from config import ch_settings, dtcc_staging_schema, ice_staging_schema



""" ***************************************** """
"""              STAGING                      """
""" ***************************************** """

def col_txfm(col):
    ''' Converts dashes slashes and spaces to underscores and all words capitalized '''
    return '_'.join([part.capitalize() for part in col.replace(' ', '_').replace('_-_','_').replace('-','_').replace('/','_').split('_')])

def ch_typecast(og_table, new_table, ch_settings, schema):
    ''' Creates new table with proper schema using staging table with all string types '''
    
    print(f"\nConnecting to {ch_settings['host']} with settings\n{ch_settings}")
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])

    current_schema_query = f"DESCRIBE TABLE {og_table}" 
    current_schema = ch_conn.query(current_schema_query).result_rows    # Gets the current schema
    current_schema_dict = {row[0]: row[1] for row in current_schema}    # Creates a dict from the current schema
    print('\n current schema:\n', current_schema_dict)

    # Use second stage schema to make new table with proper typecasts
    columns_str = ", ".join([f"`{col_txfm(col_name)}` {col_type}" for col_name, col_type in schema.items()])
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
        # col_name = col_txfm(col_name)
        if 'timestamp' in col_name:
            print("\n\n\n\n\n",col_name)
            select_columns.append(f"toDateTime64(replace(`{col_name}`, 'Z', ''), 3) AS `{col_name}`")
        else:
            select_columns.append(f"`{col_name}`")

    copy_data_query = f"""
        INSERT INTO {new_table} ({", ".join([f"{col_txfm(col)}" for col in schema.keys()])})
        SELECT {", ".join(select_columns)} FROM {og_table}
    """
    print("\nRunning copy query: ", copy_data_query)
    ch_conn.command(copy_data_query)
    print("\nSuccess")






def diff_schema(table1, table2, ch_settings):
    ''' Shows columns in table 1 which are not in table 2, and vice-versa '''
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])

    table1_unique = ch_conn.command(f"""
            SELECT name
            FROM system.columns
            WHERE (`table` = '{table1}') AND (name NOT IN (
                SELECT name
                FROM system.columns
                WHERE `table` = '{table2}'
            ));
        """
    )
    
    table2_unique = ch_conn.command(f"""
            SELECT name
            FROM system.columns
            WHERE (`table` = '{table2}') AND (name NOT IN (
                SELECT name
                FROM system.columns
                WHERE `table` = '{table1}'
            ));
        """
    )

    return table1_unique, table2_unique

    

def drop_tables(table_names, ch_settings):
    print(f"\nConnecting to {ch_settings['host']} with settings\n{ch_settings}")
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])
    print("\nDropping tables ", table_names)
    for table in table_names:
        ch_conn.command(f""" DROP TABLE IF EXISTS {table};""")


# Make third table with ICE field names matching DTCC schema
def add_leg(src_table, dst_table, diff, ch_settings):
    ''' Create a new table with transformed column names based on the diff list and rename rules '''

    print(f"\nConnecting to {ch_settings['host']} with settings\n{ch_settings}")
    ch_conn = ch(host=ch_settings['host'], port=ch_settings['port'], username=ch_settings['username'], database=ch_settings['database'])

    # Get the current schema
    current_schema_query = f"DESCRIBE TABLE {src_table}"
    current_schema = ch_conn.query(current_schema_query).result_rows
    current_schema_dict = {row[0]: row[1] for row in current_schema}
    print('\nCurrent schema:\n', current_schema_dict)

    # ICE fields and their DTCC equivalents
    schema_map = {
        "Reference_Entity_Name": "Underlying_Asset_Name",
        "Reference_Entity_Ticker": "Underlier_Id_Leg_1",
        "Scheduled_Termination_Date": "End_Date_Of_The_Notional_Amount_Leg_1",
        "Notional_Amount_Schedule_Unadjusted_Effective_Date_Of_The_Notional_Amount": "Effective_Date_Of_The_Notional_Amount_Leg_1",
        "Dissemination_Timestamp": "Effective_Date"
    }

    # Build the columns for the new table creation
    select_clauses = []
    for col_name in current_schema_dict.keys():
        # Apply diff transformations
        base_name = col_name.replace('_Leg_1', '').replace('_Leg_2', '')
        new_col_name = col_name  # Default to the original name
        for diff_col in diff:
            if base_name in diff_col:
                new_col_name = diff_col
                break

        # Apply specific rename rules if the column matches
        if col_name in schema_map:
            new_col_name = schema_map[col_name]

        select_clauses.append(f"`{col_name}` AS `{new_col_name}`")

    # Create the new table with the transformed schema
    create_table_query = f"""
        CREATE TABLE {dst_table} 
        ENGINE=MergeTree() 
        ORDER BY Event_Timestamp AS 
        SELECT {', '.join(select_clauses)} 
        FROM {src_table} 
    """

    print("\nRunning create table query: ", create_table_query)
    ch_conn.command(create_table_query)

    print(f"\nSuccessfully created new table {dst_table} with transformed column names")



def diff_stats(table1, table2, ch_settings):
    ''' Returns columns that would be the same without _Leg_1 or _Leg_2 added '''

    t1, t2 = diff_schema(table1, table2, ch_settings)
    print(f"\nColumns in {table1} not in {table2}:\n", t1)
    print(f"\nColumns in {table2} not in {table1}:\n", t2)

    diff_noleg = list([x for x in t1.split('\n') + t2.split('\n') if 'Leg' not in x])
    diff_wleg = list([x for x in t1.split('\n') + t2.split('\n') if 'Leg' in x])

    # [print(x) for x in diff_wleg]
    # [print(x) for x in diff_noleg]
    # print("\n\nDiff wo legs:", diff_noleg)
    # print("\n\nDiff w legs:", diff_wleg)


    # for i in diff_wleg:
    #     leg1_match = i.replace('_Leg_1', '')
    #     leg2_match = i.replace('_Leg_2', '')

    #     print(leg1_match)


    return diff_wleg

print("\nStaging tables...")
# ch_typecast(og_table='Swaps_ICE_source', new_table='Swaps_ICE_staging', ch_settings=ch_settings, schema=ice_staging_schema)
# ch_typecast(og_table='Swaps_DTCC_source', new_table='Swaps_DTCC_staging', ch_settings=ch_settings, schema=dtcc_staging_schema)


# diff = diff_stats('Swaps_ICE_staging', 'Swaps_DTCC_staging', ch_settings)

# print("Normalizing tables..")
# add_leg('Swaps_ICE_staging', 'Swaps_ICE_staging2',diff, ch_settings)
# add_leg('Swaps_DTCC_staging', 'Swaps_DTCC_staging2',diff, ch_settings)

# diff2 = diff_stats('Swaps_ICE_staging2', 'Swaps_DTCC_staging2', ch_settings)

# print(diff2)

