# RegSHO Daily Threshold Data Pipeline

Use `regsho_by_range` function to pull a dataframe of data by a range of dates from the nasdaq website

Functions that call the data and return a dataframe are in api.py

See `dev.py` for usage like calling the function, filtering the response down to tickers you care about, and exporting them to a csv or DuckDB table

General usage:

Try simply cloning the two files, run pip install on the packages, then

`python3 dev.py` -- you will probably like to edit the dev.py file