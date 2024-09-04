'use client';

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
import {title} from '@/components/primitives'

export interface NavItem {
  label: string;
  href: string;
  dropdown?: NavItem[];
}

export const Navbar = () => {
  const pathname = usePathname();

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

  const renderDropdownMenu = (items: NavItem[], ariaLabel: string) => (
    <DropdownMenu aria-label={ariaLabel}>
      {items.map((item) => (
        <DropdownItem key={item.href}>
          {item.dropdown ? (
            <Dropdown>
              <DropdownTrigger>
                <Button variant="light">
                  {item.label}
                </Button>
              </DropdownTrigger>
              <DropdownMenu aria-label={`${item.label} Submenu`}>
                {item.dropdown.map(subItem => (
                  <DropdownItem key={subItem.href}>
                    {subItem.dropdown ? (
                      <Dropdown>
                        <DropdownTrigger>
                          <Button variant="light">
                            {subItem.label}
                          </Button>
                        </DropdownTrigger>
                        {renderDropdownMenu(subItem.dropdown, `${subItem.label} Submenu`)}
                      </Dropdown>
                    ) : (
                      <NextLink href={subItem.href} passHref>
                        <Link>{subItem.label}</Link>
                      </NextLink>
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

  const renderNavItem = (item: NavItem) => {
    return (
      <Dropdown key={item.href}>
        <DropdownTrigger>
          <Button variant="light">
            {item.label}
          </Button>
        </DropdownTrigger>
        {item.dropdown && renderDropdownMenu(item.dropdown, `${item.label} Menu`)}
      </Dropdown>
    );
  };

  return (
    <>
      <NextUINavbar maxWidth="xl" position="sticky">
        <NavbarContent className="basis-1/5 sm:basis-full flex justify-start">
          <NavbarBrand as="li" className="gap-3 max-w-fit">
            <NextLink
              className="flex justify-start items-center gap-1"
              href="/"
              passHref
            >
              <Link>
                <h1 className={title()} style={{ margin: 0, padding: 0 }}>
                  Sp
                </h1>
                <Logo />
                <h1 className={title()} style={{ margin: 0, padding: 0 }}>
                  t
                </h1>
                <h1 className={title({color: 'violet'})}>
                  Light
                </h1>
              </Link>
            </NextLink>
          </NavbarBrand>
          <ul className="hidden lg:flex gap-4 justify-start ml-2">
            {config.navItems.map(renderNavItem)}
          </ul>
        </NavbarContent>

        <NavbarContent className="basis-1 pl-4" justify="end">
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
      <SubNavbar navItems={config.navItems}/>
    </>
  );
};
