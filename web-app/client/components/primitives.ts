import { tv } from "tailwind-variants";

export const title = tv({
  base: "tracking-tight inline font-semibold",
  variants: {
    color: {
      violet: "from-[#FF00FF] to-[#4B0082]",
      yellow: "from-[#FF705B] to-[#FFB457]",
      blue: "from-[#5EA2EF] to-[#0072F5]",
      cyan: "from-[#00b7fa] to-[#01cfea]",
      green: "from-[#6FEE8D] to-[#17c964]",
      pink: "from-[#FF72E1] to-[#F54C7A]",
      purple: "#6a0dad",
      pastelOrangeYellow: "from-[#FAD6AA] to-[#FFFAC9]",
      pastelYellowOrange: "from-[#FFFAC9] to-[#FAD6AA]",
      foreground: "dark:from-[#FFFFFF] dark:to-[#4B4B4B]",
      purpleToGold: "from-[#6a0dad] to-yellow-400",
      goldToPurple: "from-yellow-400 to-[#6a0dad]",
    },
    size: {
      xs: "text-xl lg:text-.5xl", 
      sm: "text-2xl lg:text-1xl",
      md: "text-[1.3rem] lg:text-2xl leading-9",
      lg: "text-3xl lg:text-3xl",
    },
    fullWidth: {
      true: "w-full block",
    },
  },
  defaultVariants: {
    size: "md",
  },
  compoundVariants: [
    {
      color: [
        "violet",
        "yellow",
        "blue",
        "cyan",
        "green",
        "pink",
        "pastelOrangeYellow",
        "pastelYellowOrange",
        "foreground",
        "purpleToGold",
        "goldToPurple",
      ],
      class: "bg-clip-text text-transparent bg-gradient-to-r",
    },
  ],
});

export const subtitle = tv({
  base: "w-auto md:w-auto text-lg lg:text-xl text-default-600 block max-w-full",
  // variants: {
  //   fullWidth: {
  //     true: "!w-full",
  //   },
  // },
  // defaultVariants: {
  //   fullWidth: true,
  // },
});
