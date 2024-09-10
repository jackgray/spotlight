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
      icon: "cash",
      dropdown: [
        {
          label: "Dashboard",
          href: "/finance",
          icon: "cash",
        },
        {
          label: "Wall St.",
          href: "/finance/market",
          icon: "bank"
        },
        {
          label: "Ultra Wealthy",
          href: "/finance/donations",
          icon: "exclusive"
        },
      ]
    },
    {
      label: "Policy",
      href: "/policy",
      icon: "policy",
      dropdown: [
        {
          label: "Dashboard",
          href: "/policy",
          icon: "policy",
        },
        {
          label: "Elections",
          href: "/policy/elections",
          icon: "ballot"
        },
        {
          label: "People",
          href: "/policy/people",
          icon: "activity"
        },
        {
          label: "Legislation",
          href: "/policy/legislation",
          icon: "legislation"
        }
      ]
    },
    // {
    //   label: "Info",
    //   href: "/info",
    //   icon: "info",
    //   dropdown: [
    //     {
    //       label: "Info",
    //       href: "/info",
    //       icon: "info",
    //     },
    //     {
    //       label: "Road Map",
    //       href: "/info/roadmap",
    //       icon: "todo"
    //     },
        // {
        //   label: "Who Made This",
        //   href: "/info/creator",
        //   icon: "lightbulb" 
        // },
        // {
        //   label: "Donate",
        //   href: "/info/donate",
        //   icon: "donation"
        // },
    //   ]
    // },
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
      icon: "bank",
      dropdown: [
        {
          label: "Dashboard",
          href: "/finance/market",
          icon: "bank"
        },
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
        },
        {
          label: "Rule 605",
          href: "/finance/market/rule605"
        }
      ]
    },
    {
      label: "Ultra Wealthy",
      href: "/finance/donations",
      icon: "exclusive",
      dropdown: [
        {
          label: "Crow Family",
          href: "/finance/donations/crow",
          icon: "realestate"
        },
        {
          label: "Elon Musk",
          href: "/finance/donations/elon",
          icon: "bolt"
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
        // {
        //   label: "Info",
        //   href: "/info",
        //   icon: "info"
        // },
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
      label: "Gov. Officials",
      href: "/policy/people",
      icon: "activity",
    },
    {
      label: "Legislation",
      href: "/policy/legislation",
      icon: "activity",
      dropdown: [
        {
          label: "Dashboard",
          href: "/policy/legislation",
        },
        {
          label: "Bills",
          href: "/policy/legislation/bills",
          icon: "legislation"
        },
        {
          label: "Lobbying",
          href: "/policy/legislation/lobbying",
          icon: "wscale",
        },
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
        // {
        //   label: "Info",
        //   href: "/info",
        //   icon: "info"
        // },
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

export type LegislationConfig = typeof legislationConfig;

export const legislationConfig = {
  name: "Spotlight Politics",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Bills",
      href: "/policy/legislation/bills",
      icon: "activity"
    },
    {
      label: "Lobbying",
      href: "/policy/legislation/lobbying",
      icon: "wscale",
      dropdown: [
        {
          label: "Defense Industry",
          href: "/policy/legislation/lobbying/defense",
          icon: "jet"
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
          href: "/policy/legislation",
          icon: "legislation"
        },
        // {
        //   label: "Info",
        //   href: "/info",
        //   icon: "info"
        // },
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


export type LobbyingConfig = typeof lobbyingConfig;

export const lobbyingConfig = {
  name: "Spotlight Politics",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Bills",
      href: "/policy/legislation/bills",
      icon: "activity"
    },
    {
      label: "Lobbying",
      href: "/policy/legislation/lobbying",
      icon: "wscale",
      dropdown: [
        {
          label: "Defense Industry",
          href: "/policy/legislation/lobbying/defense",
          icon: "jet"
        },
        {
          label: "Gun & Rifle",
          href: "/policy/legislation/lobbying/gunrifle",
          icon: "pistol"
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
          href: "/policy/legislation",
          icon: "legislation"
        },
        // {
        //   label: "Info",
        //   href: "/info",
        //   icon: "info"
        // },
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
    // {
    //   label: "Created By",
    //   href: "/info/creator",
    //   icon: "lightbulb",
    //   dropdown: [
    //     {
    //       label: "Bio",
    //       href: "/info/creator",
    //       icon: "lightbulb",
    //     },
    //     {
    //       label: "Resume",
    //       href: "/info/creator/resume",
    //       icon: "resume"
    //     }
    //   ]
    // },
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
