"use client";

import React from 'react';
import { usePathname } from 'next/navigation';
import { Tabs, Tab } from '@nextui-org/tabs';
import { NavItem } from './navbar';
import NextLink from 'next/link';

interface SubNavbarProps {
  activeNavItem: NavItem | undefined;
}

export const SubNavbar = ({ activeNavItem }: SubNavbarProps) => {
  const pathname = usePathname();

  if (!activeNavItem || !activeNavItem.dropdown) {
    return null;
  }

  return (
    <div className="container flex justify-center mt-4">
      <Tabs 
        aria-label="Navigation tabs" 
        selectedKey={pathname}
        className="rounded-lg bg-gunmetal p-2"
        classNames={{
          tabList: "gap-4",
          tab: "text-white",
          cursor: "bg-white/20",
        }}
      >
        {activeNavItem.dropdown.map((subItem) => (
          <Tab
            key={subItem.href}
            title={
              <NextLink href={subItem.href} passHref>
                {subItem.label}
              </NextLink>
            }
          />
        ))}
      </Tabs>
    </div>
  );
};
