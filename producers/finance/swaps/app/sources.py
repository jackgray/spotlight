sources = [
    {
        "name": "ice",
        "url_string": "https://tradevault.ice.com/tvsec/ticker/webpi/exportTicks?date={url_datestring}",
        "date_fmt": "%Y-%m-%d"
    },
    {
        "name": "cboe",
        "url_string": "https://www.cboe.com/us/equities/market_statistics/reg_sho_threshold/{url_datestring}/csv",
        "date_format": "%Y-%m-%d"
    }
]