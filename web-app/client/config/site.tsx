import {
  ChevronDown, 
  Lock, 
  Activity, 
  Flash, 
  Server, 
  TagUser, 
  Scale
} from '@/components/navIcons';

const icons: { [key: string]: () => JSX.Element } = {
  chevron: () => <ChevronDown fill="currentColor" size={16} height={16} width={16} />,
  scale: () => <Scale className="text-warning" fill="currentColor" size={30} height={30} width={30} />,
  lock: () => <Lock className="text-success" fill="currentColor" size={30} height={30} width={30} />,
  activity: () => <Activity className="text-secondary" fill="currentColor" size={30} height={30} width={30} />,
  flash: () => <Flash className="text-primary" fill="currentColor" size={30} height={30} width={30} />,
  server: () => <Server className="text-success" fill="currentColor" size={30} height={30} width={30} />,
  user: () => <TagUser className="text-danger" fill="currentColor" size={30} height={30} width={30} />,
};

type NavItem = {
  label: string;
  href: string;
  icon?: () => JSX.Element;
};
type DropdownNavItem = NavItem & {
  dropdown?: DropdownNavItem[];
};


export type SiteConfig = typeof siteConfig;

export const siteConfig: { name: string; description: string; navItems: DropdownNavItem[]; links: { github: string } } = {
  name: "Spotlight",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Finance",
      href: "/finance",
      icon: icons.chevron,
      dropdown: [
        {
          label: "Wall St.",
          href: "/finance/market",
          icon: icons.activity
        },
        {
          label: "Campaign Finance",
          href: "/finance/campaign",
          icon: icons.scale
        }
      ]
    },
    {
      label: "Policy",
      href: "/policy",
      icon: icons.chevron,
      dropdown: [
        {
          label: "Crow Family Donations",
          href: "/policy/contributions/crow",
          icon: icons.scale
        },
        {
          label: "Defense Industry Lobbying",
          href: "/policy/lobbying/defense",
          icon: icons.flash
        },
      ]
    },
    {
      label: "Info",
      href: "/info",
      icon: icons.chevron,
      dropdown: [
        {
          label: "Creator",
          href: "/info/creator",
          icon: icons.scale 
        }
      ]
    },
  ],
  links: {
    github: "https://github.com/jackgray/spotlight",
  },
};

export type FinanceConfig = typeof financeConfig;

export const financeConfig = {
  name: "Spotlight",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Wall St.",
      href: "/finance/market",
      icon: icons.chevron,
      dropdown: [
        {
          label: "CAT",
          href: "/finance/market/cat",
          icon: icons.activity
        },
        {
          label: "Derivatives",
          href: "/finance/market/derivatives",
          icon: icons.scale,
        },
        {
          label: "FTD",
          href: "/finance/market/ftd",
          icon: icons.activity,
        }
      ]
    },
    {
      label: "Campaign Finance",
      href: "/finance/campaign",
      icon: icons.server
    },
  ],
  links: {
    github: "https://github.com/jackgray/spotlight",
  },
}

export type InfoConfig = typeof infoConfig;

export const infoConfig = {
  name: "Spotlight",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Creator",
      href: "/info/creator",
      icon: icons.chevron,
      dropdown: [
        {
          label: "Resume",
          href: "/info/creator/resume",
          icon: icons.activity
        }
      ]
    },
    {
      label: "Donate",
      href: "/info/donate",
      icon: icons.activity
    },
  ],
  links: {
    github: "https://github.com/jackgray/spotlight",
  },
}

export type PoliticsConfig = typeof politicsConfig;

export const politicsConfig = siteConfig;
