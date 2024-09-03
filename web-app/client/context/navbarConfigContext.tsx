'use client'

import React, { createContext, useState, ReactNode, useContext } from 'react';

interface NavbarConfig {
  name: string;
  description: string;
  navItems: { href: string; label: string }[]; 
  links: {
    github: string;
  };
}

interface NavbarConfigContextProps {
  config: NavbarConfig;
  setConfig: (config: NavbarConfig) => void;
}

const NavbarConfigContext = createContext<NavbarConfigContextProps | undefined>(undefined);

export const NavbarConfigProvider: React.FC<{ initialConfig: NavbarConfig; children: ReactNode }> = ({ initialConfig, children }) => {
  const [config, setConfig] = useState<NavbarConfig>(initialConfig);

  return (
    <NavbarConfigContext.Provider value={{ config, setConfig }}>
      {children}
    </NavbarConfigContext.Provider>
  );
};

export const useNavbarConfig = (): NavbarConfigContextProps => {
  const context = useContext(NavbarConfigContext);
  if (context === undefined) {
    throw new Error('useNavbarConfig must be used within a NavbarConfigProvider');
  }
  return context;
};
