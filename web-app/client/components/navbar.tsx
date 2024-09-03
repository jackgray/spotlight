'use client'

import { Navbar as NextUINavbar, NavbarContent, NavbarMenu, NavbarMenuToggle, NavbarBrand, NavbarItem, NavbarMenuItem } from "@nextui-org/navbar";
import { Button } from "@nextui-org/button";
import { Kbd } from "@nextui-org/kbd";
import { Link } from "@nextui-org/link";
import { Input } from "@nextui-org/input";
import { link as linkStyles } from "@nextui-org/theme";
import NextLink from "next/link";
import clsx from "clsx";
import { Dropdown, DropdownTrigger, DropdownMenu, DropdownItem } from "@nextui-org/dropdown";
import { ThemeSwitch } from "@/components/theme-switch";
import { TwitterIcon, GithubIcon, DiscordIcon, HeartFilledIcon, SearchIcon, Logo } from "@/components/icons";
import { politicsConfig, marketConfig, siteConfig } from "@/config/site"; // Ensure SiteConfig is imported
import { usePathname } from 'next/navigation';



interface NavItem {
  label: string;
  href: string;
  dropdown?: NavItem[]; // Optional dropdown property
}


export const Navbar = () => {
  const pathname = usePathname();

  const getConfig = () => {
    if (pathname.startsWith('/market')) {
      return marketConfig;
    } else if (pathname.startsWith('/politics')) {
      return politicsConfig;
    } else {
      return siteConfig;
    }
  }

  const config = getConfig();
  
  const searchInput = (
    <Input
      aria-label="Search"
      classNames={{
        inputWrapper: "bg-default-100",
        input: "text-sm",
      }}
      endContent={
        <Kbd className="hidden lg:inline-block" keys={["command"]}>
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

  const renderDropdown = (dropdownItems: NavItem[]) => (
    <Dropdown>
      <DropdownTrigger>
        <Button variant="light">{dropdownItems[0].label}</Button>
      </DropdownTrigger>
      {dropdownItems[0].dropdown && dropdownItems[0].dropdown.length > 0 ? (
        <DropdownMenu aria-label="Dropdown Menu">
          {dropdownItems[0].dropdown.map((item) => (
            <DropdownItem key={item.href}>
              {item.dropdown ? (
                <Dropdown>
                  <DropdownTrigger>
                    <Button variant="light">{item.label}</Button>
                  </DropdownTrigger>
                  {renderDropdown([item])}
                </Dropdown>
              ) : (
                <NextLink href={item.href} passHref>
                  <Link>{item.label}</Link>
                </NextLink>
              )}
            </DropdownItem>
          ))}
        </DropdownMenu>
      ) : null}
    </Dropdown>
  );

  const hasDropdown = (item: NavItem): item is NavItem & { dropdown: NavItem[] } => {
    return Array.isArray(item.dropdown);
  };

  return (
    <NextUINavbar maxWidth="xl" position="sticky">
      <NavbarContent className="basis-1/5 sm:basis-full" justify="start">
        <NavbarBrand as="li" className="gap-3 max-w-fit">
          <NextLink className="flex justify-start items-center gap-1" href="/" passHref>
            <Link>
              <Logo />
              <p className="font-bold text-inherit"> Spotlight</p>
            </Link>
          </NextLink>
        </NavbarBrand>
        <ul className="hidden lg:flex gap-4 justify-start ml-2">
          {config.navItems.map((item) => (
            <NavbarItem key={item.href}>
              {hasDropdown(item) ? (
                renderDropdown([item])
              ) : (
                <NextLink
                  className={clsx(
                    linkStyles({ color: "foreground" }),
                    "data-[active=true]:text-primary data-[active=true]:font-medium",
                  )}
                  color="foreground"
                  href={item.href}
                  passHref
                >
                  <Link>{item.label}</Link>
                </NextLink>
              )}
            </NavbarItem>
          ))}
        </ul>
      </NavbarContent>

      <NavbarContent className="md:hidden basis-1 pl-4" justify="end">
        <Link isExternal aria-label="Github" href={config.links.github}>
          <GithubIcon className="text-default-500" />
        </Link>
        <ThemeSwitch />
        <NavbarMenuToggle />
      </NavbarContent>

      <NavbarMenu>
        {searchInput}
        <div className="mx-4 mt-2 flex flex-col gap-2">
          {config.navItems.map((item, index) => (
            <NavbarMenuItem key={`${item.href}-${index}`}>
              {hasDropdown(item) ? (
                renderDropdown([item]) // Pass single item with dropdown
              ) : (
                <Link
                  color={
                    index === 2
                      ? "primary"
                      : index === config.navItems.length - 1
                        ? "danger"
                        : "foreground"
                  }
                  href={item.href}
                  size="lg"
                >
                  {item.label}
                </Link>
              )}
            </NavbarMenuItem>
          ))}
        </div>
      </NavbarMenu>
    </NextUINavbar>
  );
};
