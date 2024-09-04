
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
        <p>Harlan Crow, the Texas real estate magnate and billionaire Republican megadonor whose friendship with U.S. Supreme Court Justice Clarence Thomas sparked an intense debate about Supreme Court ethics after ProPublica reporting, has poured millions of dollars into political contributions along with his wife, Kathy Crow.</p>
        <p></p>
        <p>The Crows’ largesse has benefitted politicians at the state and federal level.</p>
        <p></p>
      `,
    },
    {
      key: "source",
      title: "Source",
      content: `
        <p>This dataset is hosted by OpenSecrets in the form of a <Code color="secondary"><a href=https://docs.google.com/spreadsheets/d/1XbkS5EYb-KTkHwy4GK2-sdp84Mt1uZJkAKltoAq-Mxk/edit?gid=649570569#gid=649570569>Google Sheet</a></Code>. 
        <p>This pageis merely for demonstration purposes. For better views on thise dataset, head over to <Code><ahref=https://www.opensecrets.org/orgs/crow-holdings/summary?id=D000021943>OpenSecrets</a></Code></p>
            
      `,
    },
    {
      key: "usage",
      title: "Usage Tips",
      content: `
        <p>Click on the left hand panel to filter ranges of dates which will apply to all charts.</p>

        <p>Export the data to Excel or CSV by clicking the menue at the top right of any of the charts.</p>
      `
    }
  ];
  