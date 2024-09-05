
import React from 'react';

interface TabContent {
    key: string;
    title: string;
    content: React.ReactNode;
  }
  
  export const tabs: TabContent[] = [
    {
      key: "about",
      title: "About",
      content: `
CAT reports on errors in market transactions monthly, released as tables embedded in a PDF. Raw data is not publicly accessible. 

This pipeline scans for reports in a supplied range of dates (the exact day of the month they are released are not consistent, so it scans each date in a provided range), extracts the tables from any PDFs returned, cleans them, and loads them into a Clickhouse and/or DuckDB database.

The url (i.e. https://www.catnmsplan.com/sites/default/files/2022-07/07.28.22-Monthly-CAT-Update.pdf) follows a standard format, so this component just loops through a formated list of dates amd reqiests the reports, converts the pdf to text, then parses the raw text and inserts the resulting dataframes into the database.
      `,
    },
    {
      key: "code",
      title: "Code",
      content: `
You can view the code used to scrape the CAT monthly reports here: github.com/jackgray/spotlight/main/producers
      `,
    },
    {
      key: "usage",
      title: "Usage Tips",
      content: `
Click on the left hand panel to filter ranges of dates which will apply to all charts.

Export the data to Excel or CSV by clicking the menue at the top right of any of the charts
      `
    }
  ];
  