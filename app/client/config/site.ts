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
      label: "CAT Data",
      href: "/data/finance/cat",
    },
    {
      label: "Reg SHO Data",
      href: "/data/finance/regsho",
    },
    {
      label: "Swap Contracts",
      href: "/data/finance/swaps",
    },
    {
      label: "About",
      href: "/about",
    },
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
