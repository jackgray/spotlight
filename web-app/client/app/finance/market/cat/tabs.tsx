
import React from 'react';

interface TabContent {
    key: string;
    title: string;
    content: React.ReactNode;
  }
  
  export const tabs: TabContent[] = [
    {
      key: "tab1",
      title: "Tab 1",
      content: "Tab 1 Content",
    },
    {
      key: "tab2",
      title: "Tab 2",
      content: "Tab 2 Content",
    },
  ];
  