
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
        This section will first focus on equity swap agreements, and then eventually provide other kinds of derivatives data.
        \n\n
        They are sourced from several swap data repositories, which are used by institutions based on a combination of preference and SEC regulation on the type of security being traded. 
        \n\n
        Equities data from the DTCC alone dating back to 2017 encompasses ~35 million records, which is only a small fraction of publicly disseminated derivatives trading data. Spotlight will need to upgrade its servers in order to host these datasets in their entirety. Stay tuned.
        \n\n
        Until then, these records are unverified and for demonstration purposes only. 
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
  