'use client';

import React, { useState, useEffect } from 'react';
import {
  Navbar as NextUINavbar,
  NavbarContent,
  NavbarMenu,
  NavbarMenuToggle,
  NavbarBrand,
  NavbarItem,
  NavbarMenuItem,
} from '@nextui-org/navbar';
import { Button } from '@nextui-org/button';
import { Kbd } from '@nextui-org/kbd';
import { Link } from '@nextui-org/link';
import { Input } from '@nextui-org/input';
import { link as linkStyles } from '@nextui-org/theme';
import NextLink from 'next/link';
import clsx from 'clsx';
import {
  Dropdown,
  DropdownTrigger,
  DropdownMenu,
  DropdownItem,
} from '@nextui-org/dropdown';
import { ThemeSwitch } from '@/components/theme-switch';
import {
  TwitterIcon,
  GithubIcon,
  DiscordIcon,
  HeartFilledIcon,
  SearchIcon,
  Logo,
} from '@/components/icons';
import { politicsConfig, financeConfig, infoConfig, siteConfig } from '@/config/site';
import { usePathname } from 'next/navigation';
import { SubNavbar } from '@/components/subNavbar';
import { title } from '@/components/primitives';
import { RenderIcon } from '@/components/renderIcon';

export type NavItem = {
  label: string;
  href: string;
  icon?: string;
  dropdown?: DropdownNavItem[];
};

type DropdownNavItem = NavItem & {
  dropdown?: DropdownNavItem[];
};

const isDropdownNavItem = (item: NavItem): item is DropdownNavItem => {
  return (item as DropdownNavItem).dropdown !== undefined;
};

export const Navbar = () => {
  const pathname = usePathname();
  const [activeNavItem, setActiveNavItem] = useState<NavItem | undefined>(undefined);

  const getConfig = () => {
    if (pathname.startsWith('/finance')) {
      return financeConfig;
    } else if (pathname.startsWith('/policy')) {
      return politicsConfig;
    } else if (pathname.startsWith('/info')) {
      return infoConfig;
    } else {
      return siteConfig;
    }
  };

  const config = getConfig();

  useEffect(() => {
    const active = (config.navItems as DropdownNavItem[]).find(item => pathname.startsWith(item.href));
    setActiveNavItem(active);
  }, [pathname, config.navItems]);

  const searchInput = (
    <Input
      aria-label="Search"
      classNames={{
        inputWrapper: 'bg-default-100',
        input: 'text-sm',
      }}
      endContent={
        <Kbd className="hidden lg:inline-block" keys={['command']}>
          K
        </Kbd>
      }
      labelPlacement="outside"
      placeholder="Search..."
      startContent={
        <SearchIcon className="text-base text-default-400 pointer-events-none flex-shrink-0" />
      }
      type="search"
    />
  );

  // Render the dropdown menu for items
  const renderDropdownMenu = (items: DropdownNavItem[], ariaLabel: string) => (
    <DropdownMenu
      aria-label={ariaLabel}
      className="w-[340px]"
      itemClasses={{ base: "gap-4" }}
    >
      {items.map((item) => (
        <DropdownItem
          key={item.href}
          startContent={item.icon ? <RenderIcon name={item.icon} /> : null}
        >
          {item.dropdown ? (
            <Dropdown>
              <DropdownTrigger>
                <Button
                  variant="light"
                  disableRipple
                  className="p-0 bg-transparent data-[hover=true]:bg-transparent"
                  endContent={item.icon ? <RenderIcon name={item.icon} /> : null}
                  radius="sm"
                >
                  {item.label}
                </Button>
              </DropdownTrigger>
              <DropdownMenu
                aria-label={`${item.label} Submenu`}
                className="w-[340px]"
                itemClasses={{ base: "gap-4" }}
              >
                {item.dropdown?.map(subItem => (
                  <DropdownItem
                    key={subItem.href}
                    startContent={subItem.icon ? <RenderIcon name={subItem.icon} /> : null}
                  >
                    {subItem.dropdown ? (
                      <Dropdown>
                        <DropdownTrigger>
                          <Button>
                            {subItem.label}
                          </Button>
                        </DropdownTrigger>
                        <DropdownMenu>
                          {renderDropdownMenu(subItem.dropdown, `${subItem.label} Submenu`)}
                        </DropdownMenu>
                      </Dropdown>
                    ) : (
                      <span>{subItem.label}</span>
                    )}
                  </DropdownItem>
                ))}
              </DropdownMenu>
            </Dropdown>
          ) : (
            <NextLink href={item.href} passHref>
              <Link>{item.label}</Link>
            </NextLink>
          )}
        </DropdownItem>
      ))}
    </DropdownMenu>
  );

  // Render each navigation item
  const renderNavItem = (item: DropdownNavItem) => {
    return (
      <Dropdown key={item.href}>
        <DropdownTrigger>
          <Button variant="light" className="flex items-center flex-shrink-0">
            {item.icon && <RenderIcon name={item.icon} className="mr-2" />}
            <span className="hidden sm:inline truncate">{item.label}</span>
          </Button>
        </DropdownTrigger>
        {item.dropdown && renderDropdownMenu(item.dropdown, `${item.label} Menu`)}
      </Dropdown>
    );
  };

  return (
    <>
      <NextUINavbar 
        isBordered
        className="flex-nowrap"
        classNames={{
          item: [
            "flex",
            "relative",
            "h-full",
            "items-center",
            "data-[active=true]:after:content-['']",
            "data-[active=true]:after:absolute",
            "data-[active=true]:after:bottom-0",
            "data-[active=true]:after:left-0",
            "data-[active=true]:after:right-0",
            "data-[active=true]:after:h-[2px]",
            "data-[active=true]:after:rounded-[2px]",
            "data-[active=true]:after:bg-primary",
            "maxWidth:xl",
            "position:sticky"
          ],
        }}
      >
        <NavbarContent className="basis-1/5 sm:basis-full flex justify-start flex-shrink-0">
          <NavbarBrand as="li" className="gap-3 max-w-fit">
            <NextLink
              className="flex justify-start items-center gap-1"
              href="/"
              passHref
            >
              <Link>
                <h1 className={title({color: 'goldToPurple'})} style={{ margin: 0, padding: 0 }}>
                  Sp&nbsp;
                </h1>
                <Logo />
                <h1 className={title({color: 'purpleToGold'})} style={{ margin: 0, padding: 0 }}>
                  &nbsp;t
                </h1>
                <h1 className={title({color: 'pastelOrangeYellow'})}>
                  &nbsp;Light
                </h1>
              </Link>
            </NextLink>
          </NavbarBrand>
          <ul className="flex gap-4 justify-start ml-2 whitespace-nowrap overflow-x-auto flex-nowrap">
            {config.navItems.map((item) => renderNavItem(item as DropdownNavItem))}
          </ul>
        </NavbarContent>
        <NavbarContent className="basis-1 pl-1" justify="end">
          <Link isExternal aria-label="Github" href={config.links.github}>
            <GithubIcon className="text-default-500" />
          </Link>
          <ThemeSwitch />
          <NavbarMenuToggle className="block" />
        </NavbarContent>
        <NavbarMenu>
          {searchInput}
          <div className="mx-4 mt-2 flex flex-col gap-2">
            {config.navItems.map((item) => (
              <NavbarMenuItem key={item.href}>
                {renderNavItem(item)}
              </NavbarMenuItem>
            ))}
          </div>
        </NavbarMenu>
      </NextUINavbar>
      <SubNavbar activeNavItem={activeNavItem} />
    </>
  );
};
