export type SiteConfig = typeof siteConfig;

export const siteConfig = {
  name: "Spotlight",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Home",
      href: "/",
      dropdown: [
        {
          label: "Finance",
          href: "/finance"
        },
        {
          label: "Policy",
          href: "/policy"
        },
      ]
    },
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
      label: "Political Data",
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
          label: "Hire Me",
          href: "/info/hireme",
          dropdown: [
            {
              label: "Resume",
              href: "/info/hireme/resume"
            }
          ]
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
          label: "Consolidated Audit Trail",
          href: "/finance/market/cat",
        },
        {
          label: "Derivatives Trading",
          href: "/finance/market/derivatives",
        },
        {
          label: "Regulation SHO",
          href: "/finance/market/ftd"
        }
      ]
    },
    {
      label: "Campaign Finance Data",
      href: "/finance/campaign"
    },
    {
      label: "<",
      href: "/"
    }
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
