
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
Fails to deliver and Reg SHO threshold list appearances`,
    },
    {
      key: "source",
      title: "Source",
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
  