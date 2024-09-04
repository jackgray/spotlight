"use client"

import React from 'react';
import { Tabs, Tab } from "@nextui-org/tabs";
import { ScrollShadow } from "@nextui-org/scroll-shadow";
import {Card, CardBody, CardHeader } from "@nextui-org/card";
import { Code } from "@nextui-org/code";
// import Markdown from 'react-markdown';
// import remarkGfm from 'remark-gfm'
// import Markdown from "markdown-to-jsx";

interface TabContent {
  key: string;
  title: string;
  content: React.ReactNode;
}

interface ScrollingTabBarProps {
  tabs: TabContent[];
}

export default function ScrollingTabBar({ tabs }: ScrollingTabBarProps) {
  return (
    <div className="flex w-full md:w-3/4 flex-col">
      <Tabs aria-label="Dynamic tabs" items={tabs} color="secondary">
        {(item) => (
          <Tab key={item.key} title={item.title}>
            <Card className="my-4 mx-2">
              <CardBody className="p-4">
                <ScrollShadow
                >
                  <div className="prose prose-slate">
                    {typeof item.content === 'string' ? (
                      // Check if the content seems to be Markdown or HTML
                      item.content.startsWith('<') ? (
                        <div dangerouslySetInnerHTML={{ __html: item.content }} />
                      ) : (
                        <div>
                          {item.content}
                        </div>
                      )
                    ) : (
                      item.content
                    )}
                  </div>
                </ScrollShadow>
              </CardBody>
            </Card>  
          </Tab>
        )}
      </Tabs>
    </div>  
  );
}

