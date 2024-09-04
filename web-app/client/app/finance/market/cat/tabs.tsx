
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
The CAT reports on errors in electronic market transactions monthly, released as tables embedded in a PDF. Raw data is not publicly accessible, so Spotlight scans for new releases of monthly PDF reports daily (report releases are not on a fixed schedule) and scrapes the tables from the PDFs and loads them to the database.

\n\nThe reports are downloadable by URLs like this: \n\n <Code size="sm">https://www.catnmsplan.com/sites/default/files/2022-07/07.28.22-Monthly-CAT-Update.pdf</Code>.

\n\nYou may use the column <Code>Source_URL</Code> to verify any given data point by checking the orinating report it was pulled from.
      </div>`,
    },
    {
      key: "source",
      title: "Source",
      content: `<div>
          <p>You can view the code used to scrape the CAT monthly reports here: </p>
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

            <li>Export the data to Excel or CSV by clicking the menue at the top right of any of the charts </li>
          </ul>
        </div>
      `
    }
  ];
  