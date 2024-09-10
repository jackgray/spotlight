
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
       Swap agreements are reported to the exchange(s) that the underlying securities in the contract are traded on. The DTC holds repositories for SEC and CFTC regulated swaps. ICE also has swap data repositories with which institutions may satisfy their legal reporting requirement. For other types of contracts, Cboe, CME Group, and other exchanges host and disseminate swap aggreement records as well. 
      `,
    },
    {
      key: "source",
      title: "Provenance",
      content: `
You can view the code used to scrape the swap data repositories of the DTC, ICE, CME Group here: github.com/jackgray/spotlight/main/producers
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
  