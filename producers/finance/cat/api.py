from datetime import datetime
import requests
import pdfplumber
import pandas as pd
import duckdb
from io import BytesIO

def fetch_pdf_to_list(datestring):
    """Fetch PDF from URL and extract text from the last 8 pages as a list of strings."""
    monthstring = datetime.strptime(datestring, '%Y%m%d').strftime('%Y-%m')
    datestring_fmt = datetime.strptime(datestring, '%Y%m%d').strftime('%m.%d.%y')

    url = f'https://www.catnmsplan.com/sites/default/files/{monthstring}/{datestring_fmt}-Monthly-CAT-Update.pdf'

    print("\nRequesting data from ", url)
    response = requests.get(url)
    pdf_bytes = BytesIO(response.content)

    text = []
    with pdfplumber.open(pdf_bytes) as pdf:
        for page in pdf.pages[-8:]:
            text.append(page.extract_text().split('\n'))
    return text


def clean_list(raw_data, params):
    """Clean raw data by slicing and flattening it into a single list."""
    all_data = [raw_data[i][params['slice']] for i in range(len(raw_data))]
    combined_list = [item for sublist in all_data for item in sublist]
    return combined_list


def clean_to_df(data, params):
    """Convert cleaned list data into a DataFrame and format the Date column."""
    df = pd.DataFrame([row.split() for row in data], columns=params['columns'])
    df['Date'] = pd.to_datetime(df['Date'], format=params['date format']).dt.strftime('%Y-%m-%d')
    df = df.replace('%', '', regex=True).reset_index(drop=True)
    return df


def load_to_duckdb(df, report, trade_type, connection):
    """Load the DataFrame into a DuckDB table named by the report and trade_type."""
    table_name = f"{report.replace(' ','')}_{trade_type.replace(' ', '')}"
    print("Generating table name: ", table_name)
    connection.execute(f"CREATE TABLE IF NOT EXISTS {table_name} AS SELECT * FROM df")
    print(f"Loaded data into table: {table_name}")


def process_and_load(datestring, params, db_path=':memory:'):
    """Main function to fetch, process, and load data into DuckDB."""
    text = fetch_pdf_to_list(datestring)
    connection = duckdb.connect(db_path)

    for report in params:
        print('\n\n\nReport: ', report)
        for trade_type in params[report]['pages']:
            print('\nTrade Type: ', trade_type)
            rawdata = text[params[report]['pages'][trade_type]]
            cleaned = clean_list(rawdata, params=params[report])
            df = clean_to_df(data=cleaned, params=params[report])
            load_to_duckdb(df, report, trade_type, connection)

    connection.close()


params = { 
    'rolling': {
        'columns': [
            'Date', 'Late', 'Rejection Initial', 'Rejection Adjusted', 
            'Intrafirm Initial', 'Intrafirm Adjusted', 'Interfirm Sent Initial', 
            'Interfirm Sent Adjusted', 'Interfirm Received Initial', 
            'Interfirm Received Adjusted', 'Exchange Initial', 'Exchange Adjusted', 
            'Trade Initial', 'Trade Adjusted', 'Overall Error Rate Initial', 
            'Overall Error Rate Adjusted'
        ],
        'date format': '%m/%d/%Y',
        'slice': slice(5, -1),
        'pages': {
            'equities': slice(0, 2),
            'options': slice(2, 4)
        } 
    },
    'trade stats': {
        'columns': ['Date', 'Processed', 'Accepted', 'Late', 'Overall Errors Count'],
        'date format': '%Y-%m-%d',
        'slice': slice(3, -1),
        'pages': {
            'equities': slice(4, 6),
            'options': slice(6, 8)
        }
    }
}

# Example usage
process_and_load('20240418', params, db_path='../../../data/stonk.duckdb')
