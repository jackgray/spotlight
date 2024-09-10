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
import { ScrollShadow } from '@nextui-org/scroll-shadow'
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
import { politicsConfig, financeConfig, infoConfig, siteConfig, legislationConfig } from '@/config/site';
import { usePathname, useRouter } from 'next/navigation';
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
  const router = useRouter();
  const [activeNavItem, setActiveNavItem] = useState<NavItem | undefined>(undefined);

  // Change the config of the navbar based on the current page
  const getConfig = () => {
    if (pathname.startsWith('/policy/legislation/')) {
      return politicsConfig;
    } else if (pathname.startsWith('/info/')) {
      return infoConfig;
    } else if (pathname.startsWith('/finance/')) {
      return financeConfig;
    } else if (pathname.startsWith('/policy/')) {
      return legislationConfig;
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
                      <Link href={subItem.href}>{subItem.label}</Link>
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

  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 });

  // Function to handle mouse move and update position
  const handleMouseMove = (e: React.MouseEvent) => {
    const { clientX, clientY } = e;
    setMousePosition({ x: clientX, y: clientY });
  };
  

  // Custom styles for the circular mask that moves with the cursor
  const maskStyle: React.CSSProperties = {
    clipPath: `circle(100px at ${mousePosition.x}px ${mousePosition.y}px)`,
    transition: 'clip-path 0.3s ease-in-out',
    position: 'absolute', // Use 'absolute', 'relative', etc. instead of a generic string
    zIndex: 1,
  };
  
  // Render each navigation item
  const renderNavItem = (item: DropdownNavItem) => {
    // const router = useRouter();
    return (
      <Dropdown key={item.href}>
        <NavbarItem className="flex-shrink-0">
          <DropdownTrigger>
            <Button
              variant="light"
              className="flex items-center flex-shrink-0 p-0 bg-transparent data-[hover=true]:bg-transparent"
              radius="sm"
              style={{ 
                display: 'flex', 
                alignItems: 'center', 
                minWidth: '0', // Allows button to shrink below its default width
                flexShrink: 1, // Ensures button can shrink if needed
                gap: '0', // Removes gap between icon and text
                padding: '0'
              }}
              onPress={() => {if (!item.dropdown) { router.push(item.href)}}}
            >
              {item.icon && <RenderIcon name={item.icon} />}
              <span className="hidden sm:inline truncate ml-1">{item.label}</span>
            </Button>
          </DropdownTrigger>
        </NavbarItem>
        {item.dropdown && renderDropdownMenu(item.dropdown, `${item.label} Menu`)}
      </Dropdown>
    );
  };

    const renderMenuItem = (item: DropdownNavItem) => {
      // const router = useRouter();
      return (
        <Dropdown key={item.href}>
          <NavbarItem className="flex-shrink-0">
            <DropdownTrigger>
              <Button
                variant="light"
                className="flex items-center flex-shrink-0 p-0 bg-transparent data-[hover=true]:bg-transparent"
                radius="sm"
                style={{ 
                  display: 'flex', 
                  alignItems: 'center', 
                  minWidth: '0', 
                  flexShrink: 1, 
                  gap: '0', 
                  padding: '0'
                }}
                onPress={() => {if (!item.dropdown) { router.push(item.href)}}}
              >
                {item.icon && <RenderIcon name={item.icon} />}
                <span>{item.label}</span>
              </Button>
            </DropdownTrigger>
          </NavbarItem>
          {item.dropdown && renderDropdownMenu(item.dropdown, `${item.label} Menu`)}
        </Dropdown>
      );
    };

  return (
    <>
      <NextUINavbar 
        isBordered
        className="w-full"
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
        <ScrollShadow orientation="horizontal" className="w-full max-w-full pl-2 max-h-[1300px]">

          <NavbarContent className="basis-1/5 sm:basis-full flex justify-start flex-shrink-0">
            {/* <div onMouseMove={handleMouseMove} style={{ overflow: 'hidden' }}> */}
              {/* <div style={maskStyle}> */}
                <NextLink
                  className="flex justify-start items-center gap-1 mr-2"
                  href="/"
                  passHref
                >
                  <Link>
                    <h1 className={title()} style={{ margin: 0, padding: 0 }}>
                      Spotlight
                    </h1>
                    {/* <h1 className={title({ color: 'pastelYellowOrange' }) }>
                      light
                    </h1> */}
                  </Link>
                </NextLink>
              {/* </div> */}
            {/* </div> */}
              <ul className="flex gap-4 justify-start ml-4 whitespace-nowrap overflow-x-auto max-w-[1430px] sm:max-w-none overflow-y-hidden">
                {config.navItems.map((item) => renderNavItem(item as DropdownNavItem))}
              </ul>

          </NavbarContent>
        </ScrollShadow>
        {/* <NavbarContent className="basis-1" justify="end">
          <Button
            variant="light"
            className="flex items-center flex-shrink-0 p-0 bg-transparent data-[hover=true]:bg-transparent justify-end"
            radius="sm"
            onPress={() => {router.back()}}
          >
            <RenderIcon name='back'/>
          </Button>
          <Button
            variant="light"
            className="flex items-center flex-shrink-0 p-0 bg-transparent data-[hover=true]:bg-transparent"
            radius="sm"
            onPress={() => {router.forward()}}
          >
            <RenderIcon name='forward'/>
          </Button>
        </NavbarContent> */}
        <NavbarContent className="basis-1" justify="end">
          <Link isExternal aria-label="Github" href={config.links.github}>
            <GithubIcon className="text-default-500" />
          </Link>
          <ThemeSwitch />
          <NavbarMenuToggle className="block" />
        </NavbarContent>
        <NavbarMenu className="w-1/2 ml-auto flex">
          {searchInput}
          <div className="mx-4 mt-2 flex flex-col gap-2">
            {config.navItems.map((item) => (
              <NavbarMenuItem key={item.href}>
                {renderMenuItem(item)}
              </NavbarMenuItem>
            ))}
          </div>
        </NavbarMenu>
      </NextUINavbar>
      <ScrollShadow orientation="horizontal" className="w-full max-w-full pl-2 max-h-[1300px]">
        <SubNavbar activeNavItem={activeNavItem} />
      </ScrollShadow>
    </>
  );
};