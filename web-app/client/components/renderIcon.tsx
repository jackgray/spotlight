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
    default:
      return null;
  }
};
