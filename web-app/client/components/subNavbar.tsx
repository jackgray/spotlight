import React from 'react';
import { usePathname } from 'next/navigation';
import { Tabs, Tab } from '@nextui-org/tabs';
import { Card, CardBody } from '@nextui-org/card';
import { NavItem } from './navbar';
import NextLink from 'next/link';

interface SubNavbarProps {
  navItems: NavItem[];
}

export const SubNavbar = ({ navItems }: SubNavbarProps) => {
  const pathname = usePathname();
  const activeNavItem = navItems.find(item => pathname.startsWith(item.href));

  if (!activeNavItem || !activeNavItem.dropdown) {
    return null;
  }

  return (
    <div className="container flex justify-center mt-4">
      <Tabs aria-label="Navigation tabs" selectedKey={pathname}>
        {activeNavItem.dropdown.map((subItem) => (
          <Tab
            key={subItem.href}
            title={
              <NextLink href={subItem.href} passHref>
                {subItem.label}
              </NextLink>
            }
          >
            <Card>
              <CardBody>
                {subItem.dropdown ? (
                  <Tabs aria-label={`${subItem.label} subtabs`}>
                    {subItem.dropdown.map((subSubItem) => (
                      <Tab
                        key={subSubItem.href}
                        title={
                          <NextLink href={subSubItem.href} passHref>
                            {subSubItem.label}
                          </NextLink>
                        }
                      >
                        <Card>
                          <CardBody>
                            Content for {subSubItem.label}
                          </CardBody>
                        </Card>
                      </Tab>
                    ))}
                  </Tabs>
                ) : (
                  <p>Content for {subItem.label}</p>
                )}
              </CardBody>
            </Card>
          </Tab>
        ))}
      </Tabs>
    </div>
  );
};
