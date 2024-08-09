# Consolidated Auditing Trail

CAT reports on errors in the transaction chain for buy and sell orders.

[image]('./graph.png')

## Earliest Availability
These reports started being published on June 22, 2022. It is unknown whether earlier reports were ever published elsewhere.

Here's a link to the google sheets containing everything so far.


The url (i.e. https://www.catnmsplan.com/sites/default/files/2022-07/07.28.22-Monthly-CAT-Update.pdf) follows a standard format, so this component just loops through a formated list of dates amd reqiests the reports, converts the pdf to text, then parses the raw text and inserts the resulting data frames into duckdb tables.


