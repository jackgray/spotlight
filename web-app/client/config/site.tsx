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
          icon: "stocks"
        },
        {
          label: "Major Donors",
          href: "/finance/donations",
          icon: "donation"
        },
      ]
    },
    {
      label: "Policy",
      href: "/policy",
      icon: "policy",
      dropdown: [
        {
          label: "Elections",
          href: "/policy/elections",
          icon: "ballot"
        },
        {
          label: "Lobbying",
          href: "/policy/lobbying",
          icon: "wscale"
        },
        {
          label: "Appropriations",
          href: "/policy/spending",
          icon: "moneyreport"
        },
        {
          label: "Guns",
          href: "/policy/guns",
          icon: "pistol"
        },
        {
          label: "People",
          href: "/policy/people",
          icon: "activity"
        },
        {
          label: "Bills",
          href: "/policy/bills",
          icon: "activity"
        }
      ]
    },
    {
      label: "Info",
      href: "/info",
      icon: "info",
      dropdown: [
        {
          label: "Road Map",
          href: "/info/roadmap",
          icon: "todo"
        },
        {
          label: "Who Made This",
          href: "/info/creator",
          icon: "lightbulb" 
        },
        {
          label: "Donate",
          href: "/info/donate",
          icon: "donation"
        },
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
      icon: "stocks",
      dropdown: [
        {
          label: "CAT",
          href: "/finance/market/cat",
          icon: "cat"
        },
        {
          label: "Swaps",
          href: "/finance/market/derivatives",
          icon: "swap",
        },
        {
          label: "FTD",
          href: "/finance/market/ftd",
          icon: "late",
        }
      ]
    },
    {
      label: "Appropriations",
      href: "/finance/gov",
      icon: "moneyreport"
    },
    {
      label: "Campaign Finance",
      href: "/finance/campaign",
      icon: "ballot"
    },
    {
      label: "Major Donors",
      href: "/finance/donations",
      icon: "shadow",
      dropdown: [
        {
          label: "Crow Family",
          href: "/finance/donations/crow",
          icon: "donation"
        },
        {
          label: "Elon Musk",
          href: "/finance/donations/elon",
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
          label: "Info",
          href: "/info",
          icon: "info"
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
      href: "/info/roadmap",
      icon: "todo"
    },
    {
      label: "Created By",
      href: "/info/creator",
      icon: "lightbulb",
      dropdown: [
        {
          label: "Resume",
          href: "/info/creator/resume",
          icon: "resume"
        }
      ]
    },
    {
      label: "Donate",
      href: "/info/donate",
      icon: "donation"
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
          label: "Info",
          href: "/info",
          icon: "info"
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
      label: "Elections",
      href: "/policy/elections",
      icon: "ballot",
      dropdown: [
        {
          label: "Local",
          href: "/policy/elections/local"
        }
      ]
    },
    {
      label: "Lobbying",
      href: "/policy/lobbying",
      icon: "wscale",
      dropdown: [
        {
          label: "Defense Industry",
          href: "/policy/lobbying/defense",
          icon: "active"
        }
      ]
    },
    {
      label: "Appropriations",
      href: "/policy/spending",
      icon: "moneyreport"
    },
    {
      label: "Guns",
      href: "/policy/guns",
      icon: "pistol"
    },
    {
      label: "People",
      href: "/policy/people",
      icon: "activity"
    },
    {
      label: "Bills",
      href: "/policy/bills",
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
          label: "Information",
          href: "/info",
          icon: "info"
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