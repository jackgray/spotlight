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
          label: "Gov. Officials",
          href: "/policy/people",
          icon: "politician"
        },
        {
          label: "Legislation",
          href: "/policy/legislation",
          icon: "gavel"
        }
      ]
    },
    {
      label: "Info",
      href: "/info",
      icon: "info",
      dropdown: [
        {
          label: "Dashboard",
          href: "/info",
          icon: "info",
        },
        {
          label: "Data",
          href: "/info/data",
          icon: "activity"
        },
        {
          label: "Design",
          href: "/info/design",
          icon: "activity"
        }
      //   },
      //   {
      //     label: "Road Map",
      //     href: "/info/roadmap",
      //     icon: "todo"
      //   },
      //   {
      //     label: "Who Made This",
      //     href: "/info/creator",
      //     icon: "lightbulb" 
      //   },
      //   {
      //     label: "Donate",
      //     href: "/info/donate",
      //     icon: "donation"
        // },
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
          label: "Derivatives",
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
          href: "/finance/market/rule605",
          icon: "receipt"
        }
      ]
    },
    {
      label: "Ultra Wealthy",
      href: "/finance/donations",
      icon: "exclusive",
      dropdown: [
        {
          label: "Dashboard",
          href: "/finance/donations",
          icon: "exclusive",
        },
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
      label: "",
      href: "/",
      icon: "back",
      dropdown:[
        {
          label: "Finance",
          href: "/finance",
          icon: "cash"
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
          icon: "home"
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
      icon: "politician",
    },
    {
      label: "Legislation",
      href: "/policy/legislation",
      icon: "gavel",
      dropdown: [
        {
          label: "Dashboard",
          href: "/policy/legislation",
          icon: "gavel"
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
      label: "",
      href: "/",
      icon: "back",
      dropdown:[
        {
          label: "Finance",
          href: "/finance",
          icon: "cash"
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
          icon: "home"
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
      icon: "legislation"
    },
    {
      label: "Lobbying",
      href: "/policy/legislation/lobbying",
      icon: "wscale",
      dropdown: [
        {
          label: "Lobbying Dashboard",
          href: "/policy/legislation/lobbying",
          icon: "wscale"
        },
        {
          label: "Defense Industry",
          href: "/policy/legislation/lobbying/defense",
          icon: "jet"
        }
      ]
    },
    {
      label: "Gov. Officials",
      href: "/policy/people",
      icon: "politician"
    },
    {
      label: "",
      href: "/",
      icon: "back",
      dropdown:[
        {
          label: "Finance",
          href: "/finance",
          icon: "cash"
        },
        {
          label: "Legislation",
          href: "/policy/legislation",
          icon: "gavel"
        },
        {
          label: "Elections",
          href: "/policy/elections",
          icon: "ballot"
        },
        {
          label: "Gov. Officials",
          href: "/policy/people",
          icon: "politician"
        },
        // {
        //   label: "Info",
        //   href: "/info",
        //   icon: "info"
        // },
        {
          label: "Home",
          href: "/",
          icon: "home"
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
      icon: "legislation"
    },
    {
      label: "Lobbying",
      href: "/policy/legislation/lobbying",
      icon: "wscale",
      dropdown: [
        {
          label: "Dashboard",
          href: "/policy/legislation/lobbying",
          icon: "wscale"
        },
        {
          label: "Defense Industry",
          href: "/policy/legislation/lobbying/defense",
          icon: "jet"
        },
        {
          label: "NRA",
          href: "/policy/legislation/lobbying/nra",
          icon: "pistol"
        },
        {
          label: "Finance",
          href: "/policy/legislation/lobbying/finance",
          icon: "cash"
        }
      ]
    },
    {
      label: "",
      href: "/",
      icon: "back",
      dropdown:[
        {
          label: "Gov. Officials",
          href: "/policy/people",
          icon: "cash"
        },
        {
          label: "Legislation",
          href: "/policy/legislation",
          icon: "policy"
        },
        {
          label: "Elections",
          href: "/policy/elections",
          icon: "ballot"
        },
        {
          label: "Info",
          href: "/info",
          icon: "info"
        },
        {
          label: "Home",
          href: "/",
          icon: "home"
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
      icon: "map"
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
      label: "",
      href: "/",
      icon: "back",
      dropdown:[
        {
          label: "Finance",
          href: "/finance",
          icon: "cash"
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
          icon: "home"
        }
      ]
    },
  ],
  links: {
    github: "https://github.com/jackgray/spotlight",
  },
}
