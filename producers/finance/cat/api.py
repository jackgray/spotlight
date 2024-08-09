from datetime import datetime
import requests
import camelot
from io import BytesIO
import pdfplumber
import pandas as pd
import re

def fetch_pdf_to_list(datestring):
    ''' 
    '''
    # 2 dates formats need to be supplied in the URL: YYYY-mm format and mm.dd.YY
    monthstring = datetime.strptime(datestring, '%Y%m%d').strftime('%Y-%m')  #'20240621' to '2024-06'
    datestring_fmt = datetime.strptime(datestring, '%Y%m%d').strftime('%m.%d.%y')
# i.e. '20240621' to '06.21.24'

    url = f'https://www.catnmsplan.com/sites/default/files/{monthstring}/{datestring_fmt}-Monthly-CAT-Update.pdf'

    print("\nRequesting data from ", url)
    response = requests.get(url)
    pdf_bytes = BytesIO(response.content)

    # Extract text using pdfplumber
    text = []
    with pdfplumber.open(pdf_bytes) as pdf:
        # print("pages: ", pdf.pages)
        for page in pdf.pages[-8:]:
            text.append(page.extract_text().split('\n'))
        return text


def clean_list(raw_data, params):
    all_data=[]
    i=0
    while i < len(raw_data):
        all_data.append(raw_data[i][params['slice']])
        i+=1
    # print('\n\nall data: ', all_data)
    combined_list = [item for sublist in all_data for item in sublist]
    return combined_list

def clean_to_df(data, params):
    print("Using params: ", params)
    df = pd.DataFrame([row.split() for row in data], columns=params['columns'])
    print(params['date format'])
    df['Date'] = pd.to_datetime(df['Date'], format=params['date format']).dt.strftime('%Y-%m-%d')
    df = df.replace('%', '', regex=True).reset_index(drop=True)

    return df

'''
    Data is pulled from tables in the last 8 pages of these pdf reports:
    https://www.catnmsplan.com/sites/default/files/2024-04/04.18.24-Monthly-CAT-Update.pd
    There are 2 report types with different formatting and schema: rolling 5-day error rates, and industry aggregate trade statistics
    Each are divided into equities and options, making 4 tables.
    This pipeline will create two tables and combine options and equities, with a new column to designate
'''

params = { 
    'rolling': {
        'columns': [
                'Date', 'Late', 'Rejection Initial', 
                'Rejection Adjusted', 'Intrafirm Initial', 'Intrafirm Adjusted', 
                'Interfirm Sent Initial', 'Interfirm Sent Adjusted', 'Interfirm Received Initial', 
                'Interfirm Received Adjusted', 'Exchange Initial', 'Exchange Adjusted', 
                'Trade Initial', 'Trade Adjusted', 'Overall Error Rate Initial', 'Overall Error Rate Adjusted'
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
            'options': slice(6,8)
        }
    }
}



text = fetch_pdf_to_list('20240418')


for report in params:
    print('\n\n\nReport: ', report)
    for trade_type in params[report]['pages']:
        print('\nTrade Type: ', trade_type)
        rawdata = text[params[report]['pages'][trade_type]]
        cleaned = clean_list(rawdata, params=params[report])
        df = clean_to_df(data=cleaned, params=params[report])
        print(df)



