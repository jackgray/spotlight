# sources = [
#     {
#         "name": "citadel",
#         "urlstr": f"https://www.citadelsecurities.com/wp-content/uploads/sites/2/{year1}/{month_num}/{monthstr}-{year}_TCDRG-{year}{month_num}.txt"
#     }
# ]
    #     https://www.citadelsecurities.com/wp-content/uploads/sites/2/2024/07/June-2024_TCDRG-202406.txt
    #    july: https://www.citadelsecurities.com/wp-content/uploads/sites/2/2022/07/July-2024_TCDRG-202407.txt
    #     may: https://www.citadelsecurities.com/wp-content/uploads/sites/2/2024/06/May-2024_TCDRG-202405.txt
    #     april: https://www.citadelsecurities.com/wp-content/uploads/sites/2/2024/05/April-2024_TCDRG-202404.txt

clickhouse_schema_source = {
    "participant_code": "Nullable(String)",  # Code for Designated Participant (Amex: A, BSE: B, etc.)
    "market_center_code": "Nullable(String)",  # Code identifying the market center
    "report_month": "   String",  # Date in 'yyyymm' format
    "security_symbol": "Nullable(String)",  # Symbol assigned to the security
    "order_type": "Nullable(Enum8('market_orders' = 11, 'marketable_limit_orders' = 12, 'inside_the_quote_limit_orders' = 13, 'at_the_quote_limit_orders' = 14, 'near_the_quote_limit_orders' = 15))",  # Order type code
    "order_size_bucket": "Nullable(Enum8('100_499' = 21, '500_1999' = 22, '2000_4999' = 23, '5000_or_more' = 24))",  # Order size codes
    "num_covered_orders": "Nullable(Float32)",  # Number of covered orders
    "cumulative_shares_covered": "Nullable(UInt64)",  # Cumulative number of covered shares
    "shares_cancelled_before_execution": "Nullable(UInt64)",  # Cumulative number of shares canceled before execution
    "shares_executed_market_center": "Nullable(UInt64)",  # Cumulative number of shares executed at market center
    "shares_executed_other_venues": "Nullable(UInt64)",  # Cumulative number of shares executed at other venues
    "shares_executed_0_9_sec": "Nullable(UInt64)",  # Shares executed 0-9 seconds after order receipt
    "shares_executed_10_29_sec": "Nullable(UInt64)",  # Shares executed 10-29 seconds after order receipt
    "shares_executed_30_59_sec": "Nullable(UInt64)",  # Shares executed 30-59 seconds after order receipt
    "shares_executed_60_299_sec": "Nullable(UInt64)",  # Shares executed 60-299 seconds after order receipt
    "shares_executed_5_30_min": "Nullable(UInt64)",  # Shares executed 5-30 minutes after order receipt
    "avg_realized_spread": "Nullable(String)",  # Average realized spread in dollars (4 decimal places)
    "avg_effective_spread": "Nullable(String)",  # Average effective spread in dollars (4 decimal places)
    "shares_price_improvement": "Nullable(String)",  # Shares executed with price improvement
    "avg_price_improvement_per_share": "Nullable(String)",  # Average price improvement per share (4 decimal places)
    "avg_execution_time_price_improvement": "Nullable(String)",  # Average execution time with price improvement (seconds, 1 decimal place)
    "shares_executed_at_quote": "Nullable(String)",  # Shares executed at the quote
    "avg_execution_time_at_quote": "Nullable(String)",  # Average execution time at the quote (seconds, 1 decimal place)
    "shares_executed_outside_quote": "Nullable(String)",  # Shares executed outside the quote
    "avg_price_outside_quote_per_share": "Nullable(String)",  # Average price outside the quote per share (4 decimal places)
    "avg_execution_time_outside_quote": "Nullable(String)",  # Average execution time outside the quote (seconds, 1 decimal place)
    # "_source_url": "Nullable(String)",
    # "_record_id": "String",
    # "_broker": "Nullable(String)"
}

clickhouse_schema_staging = {
    "participant_code": "Nullable(String)",  # Code for Designated Participant (Amex: A, BSE: B, etc.)
    "market_center_code": "Nullable(String)",  # Code identifying the market center
    "report_month": "   String",  # Date in 'yyyymm' format
    "security_symbol": "Nullable(String)",  # Symbol assigned to the security
    "order_type": "Nullable(Enum8('market_orders' = 11, 'marketable_limit_orders' = 12, 'inside_the_quote_limit_orders' = 13, 'at_the_quote_limit_orders' = 14, 'near_the_quote_limit_orders' = 15))",  # Order type code
    "order_size_bucket": "Nullable(Enum8('100_499' = 21, '500_1999' = 22, '2000_4999' = 23, '5000_or_more' = 24))",  # Order size codes
    "num_covered_orders": "Nullable(Float32)",  # Number of covered orders
    "cumulative_shares_covered": "Nullable(UInt64)",  # Cumulative number of covered shares
    "shares_cancelled_before_execution": "Nullable(UInt64)",  # Cumulative number of shares canceled before execution
    "shares_executed_market_center": "Nullable(UInt64)",  # Cumulative number of shares executed at market center
    "shares_executed_other_venues": "Nullable(UInt64)",  # Cumulative number of shares executed at other venues
    "shares_executed_0_9_sec": "Nullable(UInt64)",  # Shares executed 0-9 seconds after order receipt
    "shares_executed_10_29_sec": "Nullable(UInt64)",  # Shares executed 10-29 seconds after order receipt
    "shares_executed_30_59_sec": "Nullable(UInt64)",  # Shares executed 30-59 seconds after order receipt
    "shares_executed_60_299_sec": "Nullable(UInt64)",  # Shares executed 60-299 seconds after order receipt
    "shares_executed_5_30_min": "Nullable(UInt64)",  # Shares executed 5-30 minutes after order receipt
    "avg_realized_spread": "Nullable(String)",  # Average realized spread in dollars (4 decimal places)
    "avg_effective_spread": "Nullable(String)",  # Average effective spread in dollars (4 decimal places)
    "shares_price_improvement": "Nullable(Int16)",  # Shares executed with price improvement
    "avg_price_improvement_per_share": "Nullable(String)",  # Average price improvement per share (4 decimal places)
    "avg_execution_time_price_improvement": "Nullable(String)",  # Average execution time with price improvement (seconds, 1 decimal place)
    "shares_executed_at_quote": "Nullable(Int16)",  # Shares executed at the quote
    "avg_execution_time_at_quote": "Nullable(String)",  # Average execution time at the quote (seconds, 1 decimal place)
    "shares_executed_outside_quote": "Nullable(Float64)",  # Shares executed outside the quote
    "avg_price_outside_quote_per_share": "Nullable(String)",  # Average price outside the quote per share (4 decimal places)
    "avg_execution_time_outside_quote": "Nullable(String)",  # Average execution time outside the quote (seconds, 1 decimal place)
    # "_source_url": "Nullable(String)",
    # "_record_id": "String",
    # "_broker": "Nullable(String)"
}


designated_participants = {
    "Amex": "A",
    "BSE": "B",
    "CHX": "M",
    "CSE": "C",
    "NASD": "T",
    "NYSE": "N",
    "PCX": "P",
    "Phlx": "X"
}

order_types = {
    "market_orders": "11",
    "marketable_limit_orders": "12",
    "inside_the_quote_limit_orders": "13",
    "at_the_quote_limit_orders": "14",
    "near_the_quote_limit_orders": "15"
}
