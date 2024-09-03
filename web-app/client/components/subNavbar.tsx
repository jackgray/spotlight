// components/SubNavbar.tsx
import { usePathname } from 'next/navigation';
import { Dropdown, DropdownTrigger, DropdownMenu, DropdownItem } from '@nextui-org/dropdown';
import { Spacer } from '@nextui-org/spacer'; // Updated import to ensure usage of Button and Spacer
import { Link } from '@nextui-org/link';
import NextLink from 'next/link';
import { NavItem } from './navbar';
import { Button } from '@nextui-org/button';


interface SubNavbarProps {
  navItems: NavItem[];
}

export const SubNavbar = ({ navItems }: SubNavbarProps) => {
  const pathname = usePathname();

  const activeNavItem = navItems.find(item => pathname.startsWith(item.href));

  return (
    <div className="flex items-center">
      {activeNavItem?.dropdown && (
        activeNavItem.dropdown.map(subItem => (
          <div key={subItem.href} className="flex items-center">
            <Spacer x={2} />
            {subItem.dropdown ? (
              <Dropdown>
                <DropdownTrigger>
                  <Button variant="light">{subItem.label}</Button>
                </DropdownTrigger>
                <DropdownMenu aria-label={`${subItem.label} Menu`}>
                  {subItem.dropdown.map(subSubItem => (
                    <DropdownItem key={subSubItem.href}>
                      <NextLink href={subSubItem.href} passHref>
                        <Link>{subSubItem.label}</Link>
                      </NextLink>
                    </DropdownItem>
                  ))}
                </DropdownMenu>
              </Dropdown>
            ) : (
              <NextLink href={subItem.href} passHref>
                <Link>{subItem.label}</Link>
              </NextLink>
            )}
          </div>
        ))
      )}
    </div>
  );
};
