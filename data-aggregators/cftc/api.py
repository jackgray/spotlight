'''
CFTC releases new reports every Friday at 3:30pm Eastern Time
'''

import base64
import requests
import json
import csv
from io import StringIO
from typing import Optional, Dict, Any
from dotenv import load_dotenv
import os
from tabulate import tabulate
import nasdaqdatalink


legacy_futures = cot("legacy_fut")
# print(tabulate(legacy_futures))
legacy_futures_contracts = legacy_futures.list_available_contracts()
print(legacy_futures_contracts)

reports = {
    "legacy_fut",
    "disaggregated_futopt",
    "traders_in_financial_futures_fut"
}
def fetch_report(report):
    '''
    Returns: report as dataframe
    '''

    return cot(report)

def fetch_all_reports(reports):
    data = {}
    for report in reports:
        res = fetch_report(report)
        print(res)
        data.append(res)
    return data

# fetch_report('disaggregated_futopt').style

# def fetch_cftc(type: str, group: str, dataset:str) -> Optional[str]:
#     return CommitmentOfTraders(dataset)