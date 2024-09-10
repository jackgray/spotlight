"use client";

import React, { useState, useEffect } from 'react';
import { usePathname } from 'next/navigation';
import { Tabs, Tab } from '@nextui-org/tabs';
import { NavItem } from './navbar';
import NextLink from 'next/link';
import { RenderIcon } from './renderIcon';

interface SubNavbarProps {
  activeNavItem: NavItem | undefined;
}

export const SubNavbar = ({ activeNavItem }: SubNavbarProps) => {
  const pathname = usePathname();
  const [activeKey, setActiveKey] = useState<string | undefined>(undefined);

  useEffect(() => {
    // Determine which tab should be active based on pathname
    if (activeNavItem && activeNavItem.dropdown) {
      const matchingItem = activeNavItem.dropdown.find(item => item.href === pathname);
      if (matchingItem) {
        setActiveKey(matchingItem.href);
      }
    }
  }, [pathname, activeNavItem]);

  if (!activeNavItem || !activeNavItem.dropdown) {
    return null;
  }

  return (
    <div className="flex justify-center w-full">
      <Tabs 
        aria-label="Options" 
        color="primary" 
        variant="underlined"
        classNames={{
          tabList: "pl-1 gap-10 w-full relative rounded-none p-0 border-b border-divider",
          cursor: "w-full bg-[#22d3ee]",
          tab: "max-w-fit px-3 h-14",
          tabContent: "group-data-[selected=true]:text-[#06b6d4]"
        }}
        selectedKey={activeKey}
      >
        {activeNavItem.dropdown.map((subItem) => (
          <Tab key={subItem.href} title={
            <NextLink href={subItem.href} passHref>
              <div className="flex items-center space-x-4">
                {subItem.icon && <RenderIcon name={subItem.icon} />} {/* Icon */}
                <span>{subItem.label}</span> {/* Label */}
              </div>
            </NextLink>
          }/>
        ))}
      </Tabs>
    </div>
  );
};
