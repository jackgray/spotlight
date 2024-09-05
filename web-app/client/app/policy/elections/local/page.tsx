import { FC } from 'react';
import { subtitle } from "@/components/primitives";
import ScrollingTabBar from '@/components/scrollingTabBar';
import { tabs } from './tabs';

const LocalElectionsPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <h1 className={subtitle()}>Defense Industry Lobbying</h1>
      <ScrollingTabBar tabs={tabs} />
    </div>
  );
};

export default LocalElectionsPage;