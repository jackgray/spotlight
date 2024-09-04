"use client"

import React from 'react';
import { Tabs, Tab } from "@nextui-org/tabs";
import { ScrollShadow } from "@nextui-org/scroll-shadow";
import {Card, CardBody, CardHeader } from "@nextui-org/card";

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
    <div className="flex w-full flex-col">
      <Tabs aria-label="Dynamic tabs" items={tabs} color="secondary">
        {(item) => (
          <Tab key={item.key} title={item.title}>
            <Card>
              <CardBody>
                {item.content}
              </CardBody>
            </Card>  
          </Tab>
        )}
      </Tabs>
    </div>  
  );
};

