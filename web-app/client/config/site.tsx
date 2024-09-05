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
      icon: "bank",
      dropdown: [
        {
          label: "Wall St.",
          href: "/finance/market",
          icon: "piggy"
        },
        {
          label: "Elections",
          href: "/finance/campaign",
          icon: "scale"
        }
      ]
    },
    {
      label: "Policy",
      href: "/policy",
      icon: "policy",
      dropdown: [
        {
          label: "Donations",
          href: "/policy/donations",
          icon: "scale"
        },
        {
          label: "Lobbying",
          href: "/policy/lobbying",
          icon: "flash"
        },
      ]
    },
    {
      label: "Info",
      href: "/info",
      icon: "info",
      dropdown: [
        {
          label: "Created By",
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
      icon: "piggy",
      dropdown: [
        {
          label: "CAT",
          href: "/finance/market/cat",
          icon: "cat"
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
      label: "Gov Spending",
      href: "/finance/gov",
      icon: "moneyreport"
    },
    {
      label: "Campagin",
      href: "/finance/campaign",
      icon: "server"
    },
    {
      label: "Back",
      href: "/",
      icon: "back",
      dropdown:[
        {
          label: "Finance",
          href: "/finance",
          icon: "bank"
        },
        {
          label: "Policy",
          href: "/policy",
          icon: "policy"
        },
        {
          label: "Home",
          href: "/",
          icon: "activity"
        }
      ]
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
      label: "Roadmap",
      href: "/info/roadmap"
    },
    {
      label: "Created By",
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
    {
      label: "Back",
      href: "/",
      icon: "back",
      dropdown:[
        {
          label: "Finance",
          href: "/finance",
          icon: "bank"
        },
        {
          label: "Policy",
          href: "/policy",
          icon: "policy"
        },
        {
          label: "Home",
          href: "/",
          icon: "activity"
        }
      ]
    },
  ],
  links: {
    github: "https://github.com/jackgray/spotlight",
  },
}

export type PoliticsConfig = typeof politicsConfig;

export const politicsConfig = {
  name: "Spotlight",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Donations",
      href: "/policy/donations",
      icon: "moneyreport",
      dropdown: [
        {
          label: "Crow Family",
          href: "/policy/donations/crow"
        }
      ]
    },
    {
      label: "Lobbying",
      href: "/policy/lobbying",
      icon: "moneyreport",
      dropdown: [
        {
          label: "Defense Industry",
          href: "/policy/lobbying/defense"
        }
      ]
    },
    {
      label: "Back",
      href: "/",
      icon: "back",
      dropdown:[
        {
          label: "Finance",
          href: "/finance",
          icon: "bank"
        },
        {
          label: "Policy",
          href: "/policy",
          icon: "policy"
        },
        {
          label: "Home",
          href: "/",
          icon: "activity"
        }
      ]
    },
  ],
  links: {
    github: "https://github.com/jackgray/spotlight",
  },
};