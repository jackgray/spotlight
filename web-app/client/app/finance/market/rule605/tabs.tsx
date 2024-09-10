
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
      content: `<div>
                  <p>Rule 605 requires broker-dealers to release monthly statistical reports on trade transations, like the amount of time between an order was place and when it was executed, and how much the price of the stock changed within that time.</p>
                  <p>
                  <p>Spotlight scans for new releases of these reports and loads them into its database which is represented in real-time by these dashboards.</p>
                </div>
      `,
    },
    {
      key: "source",
      title: "Source",
      content: `<div>
          <p>
            You can view the code used to scrape the Rule 605 monthly reports here: <a href='github.com/jackgray/spotlight/main/producers'>here</a>
          </p>
        </div>
      `,
    },
    {
      key: "usage",
      title: "Usage Tips",
      content: `<div>
          <ul>
            <li>Click on the left-hand panel to filter ranges of dates which will apply to all charts.</li>

            <li>Export the data to Excel or CSV by clicking the menu at the top right of any of the charts </li>

            <li>You can also filter the data accross all charts by double clicking a column or value in the corresponding table. More filters will may be available in the left panel as well.
          </ul>
        </div>
      `
    }
  ];
  