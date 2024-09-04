
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
        About deriivatives trading data.
      `,
    },
    {
      key: "source",
      title: "Source",
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
  