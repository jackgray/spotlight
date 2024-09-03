export type SiteConfig = typeof siteConfig;

export const siteConfig = {
  name: "Spotlight",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Home",
      href: "/",
    },
    {
      label: "Market Data",
      href: "/market"
    },
    {
      label: "Political Data",
      href: "/politics"
    },
    {
      label: "About",
      href: "/about",
    },
    {
      label: "Hire Me",
      href: "/hireme/resume"
    }
  ],
  // navMenuItems: [
  //   {
  //     label: "Profile",
  //     href: "/profile",
  //   },
  //   {
  //     label: "Dashboard",
  //     href: "/dashboard",
  //   },
  //   {
  //     label: "Projects",
  //     href: "/projects",
  //   },
  //   {
  //     label: "Team",
  //     href: "/team",
  //   },
  //   {
  //     label: "Calendar",
  //     href: "/calendar",
  //   },
  //   {
  //     label: "Settings",
  //     href: "/settings",
  //   },
  //   {
  //     label: "Help & Feedback",
  //     href: "/help-feedback",
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

export type MarketConfig = typeof marketConfig;

export const marketConfig = {
  name: "Spotlight",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Financial Market Data",
      href: "/market"
    },
    {
      label: "Derivatives",
      href: "/market/derivatives"
    },
    {
      label: "CAT",
      href: "/market/cat",
    },
    {
      label: "Reg SHO",
      href: "/market/regsho",
    },
    {
      label: "Back",
      href: "/",
    },
  ],
  links: {
    github: "https://github.com/jackgray/spotlight",
    // twitter: "https://twitter.com/getnextui",
    // docs: "https://nextui.org",
    // discord: "https://discord.gg/9b6yyZKmH4",
    // sponsor: "https://patreon.com/jrgarciadev",
  },
};


export type PoliticsConfig = typeof politicsConfig;

export const politicsConfig = {
  name: "Spotlight",
  description: "Aggregations for hard to find data -> oversight for hard to catch crime.",
  navItems: [
    {
      label: "Policy Data",
      href: "/politics"
    },
    {
      label: "Crow Family Donations",
      href: "/politics/contributions/crow"
    },
    {
      label: "Defense Industry Lobbying",
      href: "/politics/lobbying/defense",
    },
    {
      label: "Back",
      href: "/",
    },
  ],
  links: {
    github: "https://github.com/jackgray/spotlight",
    // twitter: "https://twitter.com/getnextui",
    // docs: "https://nextui.org",
    // discord: "https://discord.gg/9b6yyZKmH4",
    // sponsor: "https://patreon.com/jrgarciadev",
  },
};

