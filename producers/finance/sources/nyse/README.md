# NYSE Data

## Regulation SHO Daily Threshold Data

### Requirements

DuckDB - crazy light and fast to install, no configuration needed
python3
pip packages
### Usage



### Queries

Enter the database with `duckdb gme.duckdb` or whatever you named the db

To query the top 5 most occurring stocks on Reg SHO Daily Threshold list and display their rate of occurence

```
SELECT
    Symbol,
    COUNT(*) AS count
FROM
    nyse_regsho
WHERE
    "Reg SHO Threshold Flag" = 'Y'
    AND "Date" < "2024-01-01"
GROUP BY
    Symbol
ORDER BY
    count DESC
LIMIT 5;
```