import base64
import requests
import json
import csv
from io import StringIO
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import os
import nasdaqdatalink
import pandas as pd

load_dotenv()
# Load environment variables
api_key = os.getenv('NASDAQ_API_KEY')


def search_datasets(db_code='CFTC'):
    '''
        Returns dataframes of search results on specified NASDAQ datasets

        Args:

        db_code: Eg. 'CFTC'
    '''

    # Define the URL endpoint for searching datasets
    search_url = 'https://data.nasdaq.com/api/v3/datasets'

    # Define parameters for the search
    params = {
        'api_key': api_key,
        'database_code': db_code,  # Example database code for CFTC datasets
        'per_page': 100,  # Number of datasets to retrieve per request
        'page': 1         # Start from the first page
    }

    all_datasets = []

    while True:
        response = requests.get(search_url, params=params)

        if response.status_code == 200:
            data = response.json()
            datasets = data['datasets']
            
            # Append the retrieved datasets to the list
            all_datasets.extend(datasets)
            
            # Check if there is another page of results
            if len(datasets) < params['per_page']:
                break
            else:
                params['page'] += 1
        else:
            print(f"Failed to fetch data: {response.status_code}")
            break


    # Convert the list of datasets to a DataFrame
    df = pd.DataFrame(all_datasets)

    return df
