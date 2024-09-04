export type SiteConfig = typeof siteConfig;


export type NavItem = {
  label: string;
  href: string;
  icon?: string;
  dropdown?: NavItem[];
};

export type DropdownNavItem = NavItem & {
  dropdown?: DropdownNavItem[];
};

export type Config = {
  name: string;
  description: string;
  navItems: DropdownNavItem[];
  links: {
    github: string;
  };
};

export const siteConfig: Config = {
  name: "Spotlight",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Finance",
      href: "/finance",
      icon: "chevron",
      dropdown: [
        {
          label: "Wall St.",
          href: "/finance/market",
          icon: "activity"
        },
        {
          label: "Campaign Finance",
          href: "/finance/campaign",
          icon: "scale"
        }
      ]
    },
    {
      label: "Policy",
      href: "/policy",
      icon: "chevron",
      dropdown: [
        {
          label: "Crow Family Donations",
          href: "/policy/contributions/crow",
          icon: "scale"
        },
        {
          label: "Defense Industry Lobbying",
          href: "/policy/lobbying/defense",
          icon: "flash"
        },
      ]
    },
    {
      label: "Info",
      href: "/info",
      icon: "chevron",
      dropdown: [
        {
          label: "Creator",
          href: "/info/creator",
          icon: "scale" 
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
      icon: "chevron",
      dropdown: [
        {
          label: "CAT",
          href: "/finance/market/cat",
          icon: "activity"
        },
        {
          label: "Derivatives",
          href: "/finance/market/derivatives",
          icon: "scale",
        },
        {
          label: "FTD",
          href: "/finance/market/ftd",
          icon: "activity",
        }
      ]
    },
    {
      label: "Campaign Finance",
      href: "/finance/campaign",
      icon: "server"
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
      icon: "chevron",
      dropdown: [
        {
          label: "Resume",
          href: "/info/creator/resume",
          icon: "activity"
        }
      ]
    },
    {
      label: "Donate",
      href: "/info/donate",
      icon: "activity"
    },
  ],
  links: {
    github: "https://github.com/jackgray/spotlight",
  },
}

export type PoliticsConfig = typeof politicsConfig;

export const politicsConfig = siteConfig;
