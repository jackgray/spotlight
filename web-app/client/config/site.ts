export type SiteConfig = typeof siteConfig;

export const siteConfig = {
  name: "Spotlight",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Finance",
      href: "/finance",
      dropdown: [
        {
          label: "Market Regulation",
          href: "/finance/market",
        },
        {
          label: "Campaign Finance",
          href: "/finance/campaign"
        }
      ]
    },
    {
      label: "Policy",
      href: "/policy",
      dropdown: [
        {
          label: "Crow Family Donations",
          href: "/policy/contributions/crow"
        },
        {
          label: "Defense Industry Lobbying",
          href: "/policy/lobbying/defense",
        },
      ]
    },
    {
      label: "Info",
      href: "/info",
      dropdown: [
        {
          label: "Creator",
          href: "/info/creator",
        }
      ]
    },
  ],
  // Leaving this in to eventually support alternative navigation menu for logged in user
  // navMenuItems: [
  //   {
  //     label: "Dashboard",
  //     href: "/dashboard",
  //   },
  //   {
  //     label: "Settings",
  //     href: "/settings",
  //   },
  //   {
  //     label: "Logout",
  //     href: "/logout",
  //   },
  // ],
  links: {
    github: "https://github.com/jackgray/spotlight",
    // twitter: "https://twitter.com/getnextui",
    // docs: "https://nextui.org",
    // discord: "https://discord.gg/9b6yyZKmH4",
    // sponsor: "https://patreon.com/jrgarciadev",
  },
};

// Support for dynamically changing nav meu
export type FinanceConfig = typeof financeConfig;

export const financeConfig = {
  name: "Spotlight",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Market Regulatory Data",
      href: "/finance/market",
      dropdown: [
        {
          label: "CAT",
          href: "/finance/market/cat",
        },
        {
          label: "Derivatives",
          href: "/finance/market/derivatives",
        },
        {
          label: "FTD",
          href: "/finance/market/ftd"
        }
      ]
    },
    {
      label: "Campaign Finance Data",
      href: "/finance/campaign"
    },
  ],
  links: {
    github: "https://github.com/jackgray/spotlight",
    // twitter: "https://twitter.com/getnextui",
    // docs: "https://nextui.org",
    // discord: "https://discord.gg/9b6yyZKmH4",
    // sponsor: "https://patreon.com/jrgarciadev",
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
      dropdown: [
        {
          label: "Resume",
          href: "/info/creator/resume",
        }
      ]
    },
    {
      label: "Donate",
      href: "/info/donate"
    },
  ],
  links: {
    github: "https://github.com/jackgray/spotlight",
    // twitter: "https://twitter.com/getnextui",
    // docs: "https://nextui.org",
    // discord: "https://discord.gg/9b6yyZKmH4",
    // sponsor: "https://patreon.com/jrgarciadev",
  },
}


export type PoliticsConfig = typeof politicsConfig;

export const politicsConfig = siteConfig
