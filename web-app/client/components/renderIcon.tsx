import React from 'react';
import {
  ChevronDown,
  Lock,
  Activity,
  Flash,
  Server,
  TagUser,
  Scale
} from '@/components/navIcons';

import {
  Bank,
  Piggy,
  Info,
  Cat,
  Back,
  Policy,
  MoneyReport,
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
  Map,
  ShadowMan
} from '@/components/icons';

interface IconProps {
  name: string;
  className?: string;
}

export const RenderIcon: React.FC<IconProps> = ({ name, className = '' }) => {
  const iconProps = {
    fill: "currentColor",
    size: 16,
    height: 16,
    width: 16,
    className
  };

  switch (name) {
    case 'chevron':
      return <ChevronDown {...iconProps} />;
    case 'scale':
      return <Scale {...iconProps} className={`text-warning ${className}`} />;
    case 'lock':
      return <Lock {...iconProps} className={`text-success ${className}`} />;
    case 'activity':
      return <Activity {...iconProps} className={`text-secondary ${className}`} />;
    case 'flash':
      return <Flash {...iconProps} className={`text-primary ${className}`} />;
    case 'server':
      return <Server {...iconProps} className={`text-success ${className}`} />;
    case 'user':
      return <TagUser {...iconProps} className={`text-danger ${className}`} />;
    case 'bank':
      return <Bank {...iconProps} className={`text-danger ${className}`} />;
    case 'piggy':
      return <Piggy {...iconProps} className={`text-danger ${className}`} />;
    case 'info':
      return <Info {...iconProps} className={`text-danger ${className}`} />;
    case 'cat':
      return <Cat {...iconProps} className={`text-danger ${className}`} />;
    case 'back':
      return <Back {...iconProps} className={`text-danger ${className}`} />;
    case 'policy':
      return <Policy {...iconProps} className={`text-danger ${className}`} />;
    case 'moneyreport':
      return <MoneyReport {...iconProps} className={`text-danger ${className}`} />;
    case 'swap':
      return <Swap {...iconProps} className={`text-danger ${className}`} />;
    case 'late':
      return <Late {...iconProps} className={`text-danger ${className}`} />;
    case 'campaign':
      return <Campaign {...iconProps} className={`text-danger ${className}`} />;
    case 'donation':
      return <Donation {...iconProps} className={`text-danger ${className}`} />;
    case 'stocks':
      return <Stocks {...iconProps} className={`text-danger ${className}`} />;
    case 'stockguy':
      return <StockGuy {...iconProps} className={`text-danger ${className}`} />;
    case 'wscale':
      return <WeightScale {...iconProps} className={`text-danger ${className}`} />;
    case 'lightbulb':
      return <Lightbulb {...iconProps} className={`text-danger ${className}`} />;
    case 'ballot':
      return <Ballot {...iconProps} className={`text-danger ${className}`} />;
    case 'resume':
      return <Resume {...iconProps} className={`text-danger ${className}`} />;
    case 'map':
      return <Map {...iconProps} className={`text-danger ${className}`} />;
    case 'shadow':
      return <ShadowMan {...iconProps} className={`text-danger ${className}`} />;
    default:
      return null;
  }
};
