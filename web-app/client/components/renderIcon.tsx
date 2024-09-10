import React from 'react';
import {
  ChevronDown,
  Lock,
  Activity,
  Flash,
  Server,
  TagUser,
  Scale,
  // Cash
} from '@/components/navIcons';

import {
  Bank,
  Piggy,
  Info,
  Cat,
  Back,
  Forward,
  Policy,
  Swap,
  Late,
  Campaign,
  Stocks,
  StockGuy,
  Donation,
  Scale as WeightScale,
  Lightbulb,
  Ballot,
  Resume,
  Todo,
  Map,
  ShadowMan,
  Pistol,
  Bolt,
  Cash,
  Exclusive,
  RealEstate,
  Jet,
  Legislation
} from '@/components/icons';

interface IconProps {
  name: string;
  className?: string;
}

const iconMap: Record<string, React.ComponentType<any>> = {
  chevron: ChevronDown,
  scale: Scale,
  lock: Lock,
  activity: Activity,
  flash: Flash,
  server: Server,
  user: TagUser,
  bank: Bank,
  piggy: Piggy,
  info: Info,
  cat: Cat,
  back: Back,
  forward: Forward,
  policy: Policy,
  cash: Cash,
  swap: Swap,
  late: Late,
  campaign: Campaign,
  stocks: Stocks,
  stockguy: StockGuy,
  donation: Donation,
  wscale: WeightScale,
  lightbulb: Lightbulb,
  ballot: Ballot,
  resume: Resume,
  todo: Todo,
  shadow: ShadowMan,
  pistol: Pistol,
  map: Map,
  bolt: Bolt,
  exclusive: Exclusive,
  realestate: RealEstate,
  jet: Jet,
  legislation: Legislation
};

export const RenderIcon: React.FC<IconProps> = ({ name, className = '' }) => {
  const IconComponent = iconMap[name];

  if (!IconComponent) return null;

  const iconProps = {
    fill: "currentColor",
    size: 16,
    height: 16,
    width: 16,
    className: `text-danger ${className}`,
  };

  return <IconComponent {...iconProps} />;
};
