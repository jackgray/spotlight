

# Swaps pipeline

Pulls zipped csv files for a range of dates from multiple Swap Data Repositories (SDRs). Traditionally, a single zip file containing a single csv must be downloaded each day. This package aims to automate that task and allow automated retreival of new data 



## SWAP DATA REPOSITORIES

https://www.sec.gov/swaps-chart/swaps-chart.pdf

https://www.sec.gov/about/divisions-offices/division-trading-markets/list-registered-security-based-swap-dealers-major-security-based-swap-participants

https://www.clarusft.com/sec-security-based-swap-repositories-are-now-live/

When a swap agreement is made, the transaction must be filed with qualifying swap data repository (SDR)

The nature of the swap and underlying assets determine which agencies a party has the option of filing with. 

### Schema management / Field Name changes
Schema for all data sources are managed in ./app/config.py

Any time there is a change from the source, a new updated schema is used


#### 20230129
Call amount -> Call amount-Leg 1 
+ Unique Product Identifier
+ UPI FISN
+ UPI Underlier Name


#### Custom fields
some custom fields are added to all records and are indicated as custom by a preceding "_"

1. _Report_Date: the date used to request the report, used a a sanity check for all other reported date fields. 
2. _Source_URL: url of the public record the data was pulled from
3. _RecordID: a unique ID (and primary key for clickhouse) for the row, made from Dissemination Identifier + Event Timestamp, used to prevent duplicates if the record is pulled and inserted when it already exists

#### Other field name transformations
All fields are automatically modified to replace spaces, dashes, and slashes with underscores for database compatibility. 

In a secondary staging script, they are further modified to map to common names accross sources with varying schema

This includes capitalization, and in some instances, adding '_Leg-n' to the end of a field name to match other records so that they can be merged as a single table.

Varying data repositories change their schema from time to time, so the staging process aims to keep them all the same



## DTCC Data

The DTCC offers datasets submitted to both SEC and CFTC

https://pddata.dtcc.com/ppd/

https://kgc0418-tdw-data-3.s3.amazonaws.com/gtr/static/gtr/docs/RT_PPD_quick_ref_guide.pdf



## ICE Trade Vault

https://ir.theice.com/press/news-details/2021/ICE-Announces-that-ICE-Trade-Vault-is-Approved-by-the-SEC-as-a-Security-Based-Swap-Data-Repository/default.aspx

https://www.ice.com/swap-trade/regulation


##  CME Group 
repository for CFTC-based OTC swap agreements

https://www.cmegroup.com/market-data/repository/data.html#tab_QbsT5Qi=cmdty



##### CFTC

https://www.cftc.gov/sites/default/files/idc/groups/public/@newsroom/documents/file/fd_factsheet_final.pdf

https://www.cftc.gov/sites/default/files/About/Economic%20Analysis/Introducing%20ENNs%20v4.pdf



##### More reading
https://www.sec.gov/comments/s7-10-21/s71021-9177172-248310.pdf


https://www.reddit.com/r/Superstonk/comments/1d2l85e/all_equity_swaps_data_since_21422_source_download/?share_id=9H4_VaON_J2TRJyj57w5-&utm_content=2&utm_medium=ios_app&utm_name=ioscss&utm_source=share&utm_term=1


## Useful Query Patterns

Any time a swap agreement is modified, a record is ADDED to the ledger, creating duplicates. To view only the active state of all contracts, you must filter out duplicated "Original Dissemination Identifier" field values. The record which has the most recent corresponding Event Timestamp prevails as the current state of the agreement. 

```
SELECT
    Dissemination_Identifier,
    Event_timestamp,
    Expiration_Date,
    Original_Dissemination_Identifier, 
    Notional_amount_Leg_1, 
    Underlier_ID_Leg_1,
    Underlier_ID_Leg_2
FROM
(
    SELECT
        Dissemination_Identifier,
        Event_timestamp,
        Expiration_Date,
        Original_Dissemination_Identifier, 
        Notional_amount_Leg_1, 
        Underlier_ID_Leg_1,
        Underlier_ID_Leg_2,
        row_number() OVER (PARTITION BY Original_Dissemination_Identifier ORDER BY Event_timestamp DESC) AS rn
    FROM Swaps_DTCC_source
)
WHERE rn = 1 AND Underlier_ID_Leg_1 LIKE '%36467W109%' OR Underlier_ID_Leg_1 LIKE '%GME'
```