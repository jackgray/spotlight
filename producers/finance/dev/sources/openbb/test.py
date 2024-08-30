
from typing import Literal
import pandas as pd
from datetime import datetime
# from plotly import graph_objects as go
from openbb import obb
from os import getenv, makedirs
from dotenv import load_dotenv
load_dotenv()


# Load environment variables
pat = getenv('OPENBB_PAT')
nasdaq_api_key = getenv('NASDAQ_API_KEY')
intrinio_api_key = getenv('INTRINO_API_KEY')

# Authenticate data sources
obb.account.login(pat=pat)
obb.user.preferences.output_type = "dataframe"
obb.user.credentials.nasdaq_api_key = nasdaq_api_key
obb.user.credentials.nasdaq_api_key = nasdaq_api_key
obb.user.credentials.intrinio_api_key = intrinio_api_key

swaps = obb.regulators.cftc.cot()

# unusuals = obb.derivatives.options.unusual(symbol)

# ftds = obb.equity.shorts.fails_to_deliver(symbol='GME')

# reports = obb.regulators.cftc.cot_search()

# load('swaps', reports)
# print(swaps)
# The major US indices - S&P 500, Nasdaq 100, Dow Jones Industrial Average, Russell 1000 & 2000, VIX, Bloomberg Commodity Index, etc. - are categorized as "Index".
# reports[reports["category"] == "Index"]
# obb.plot(swaps, kind=line, title='swap data')



# def filter_options_data(options, by: Literal["expiration", "strike"] = "expiration"):
#     data = pd.DataFrame()
#     data["Total Open Interest"] = options.groupby(by)["open_interest"].sum()
#     data["Call Open Interest"] = options[options["option_type"] == "call"].groupby(by)["open_interest"].sum()
#     data["Put Open Interest"] = options[options["option_type"] == "put"].groupby(by)["open_interest"].sum()
#     data["Total Volume"] = options.groupby(by)["volume"].sum()
#     data["Call Volume"] = options[options["option_type"] == "call"].groupby(by)["volume"].sum()
#     data["Put Volume"] = options[options["option_type"] == "put"].groupby(by)["volume"].sum()

#     return data

# data = filter_options_data(options, "strike")

# data

