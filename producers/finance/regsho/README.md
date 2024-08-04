# Multiple Data Sources

Just like swap contracts, there are a number of disparate entities that these events may be reported to.

# NASDAQ

Nasdaq reports on companies that reached the Reg SHO daily threshold, but stopped including securities that reached the threshold due to OTC trades in 2014. You can find KOSS on this list, but not GME or any of the ETFs it's contained in

# FINRA 

FINRA's Query API has reports on OTC RegSHO lists, but you won't find GME there, either

I have made python functions to grab this data (you must make an account and generate an API key first), but you can check the text archives of specific dates here

https://otce.finra.org/otce/RegSHOThreshold/archives


# NYSE

https://www.nyse.com/regulation/threshold-securities

If we go to this data source at NYSE, and search dates we know GME existed on the threshold list like 02/02/2021, we can finally see GME.

# Other sources?

Where else is data being reported that we simply cannot access? Are there other data sources we don't know about?

# ICE

This is a newer intermediary with their own swap data repository, where it is legal for institutions to file a swap with ICE, instead of the SEC or DTCC, and remain anonymous to everyone except the participants in the contract.

Most of the data reported here is not available to the public


