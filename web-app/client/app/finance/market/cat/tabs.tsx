
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
                  <p>A branch of FINRA, the Consolidated Audit Trail reports on errors in electronic market transactions. Most of the data is not publicly disseminated, but it does publish some of it on a monthly basis, in the form of a PDF slideshow.</p>
                  <p>
                  <p>Spotlight scans for new releases of these reports, scrapes the tables from the PDFs and loads them to the database which is represented in real-time by these dashboards.</p>
                </div>
      `,
    },
    {
      key: "source",
      title: "Source",
      content: `<div>
          <p>As with all of Spotlight's curated datasets, a source URL column is available which will link you to the report that any given data point was pulled from, making the data easy to verify.
          <p>You can also view the code used to scrape the CAT monthly reports here: </p>
          <p>
            <Code size="sm">github.com/jackgray/spotlight/main/producers</Code>
          </p>
        </div>
      `,
    },
    {
      key: "usage",
      title: "Usage Tips",
      content: `<div>
          <ul>
            <li>Click on the left hand panel to filter ranges of dates which will apply to all charts.</li>

            <li>Export the data to Excel or CSV by clicking the menu at the top right of any of the charts </li>

            <li>You can also filter the data accross all charts by double clicking a column or value in the corresponding table. More filters will may be available in the left panel as well.
          </ul>
        </div>
      `
    }
  ];
  