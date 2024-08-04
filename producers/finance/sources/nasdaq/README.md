# RegSHO Daily Threshold Data Pipeline For Non-OTC / Pre- 2014 OTC Trades

FTDs as a result of OTC trades are no longer reported by NASDAQ as of 2014. See the finra directory for utilizing the FINRA Query API to pull regsho daily threshold lists.

## Usage

Use `regsho_by_range` function to pull a dataframe of data by a range of dates from the nasdaq website

Functions that call the data and return a dataframe are in api.py

See `dev.py` for usage like calling the function, filtering the response down to tickers you care about, and exporting them to a csv or DuckDB table

General usage:

Try simply cloning the two files, run pip install on the packages, then

`python3 dev.py` -- you will probably like to edit the dev.py file