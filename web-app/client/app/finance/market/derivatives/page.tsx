
import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard"; // Make sure the path is correct
import { supersetConfig } from "@/lib/envConfig";
import ScrollingTabBar from '@/components/scrollingTabBar';
import { tabs } from './tabs';

const DerivativesDataPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <h1 className={subtitle()}>Derivatives Trading Data</h1>
      <ScrollingTabBar tabs={tabs} />
      <SupersetDashboard
        dashboardTitle="Equity Based Swap Data"
        supersetUrl={supersetConfig.supersetUrl}
        dashboardId="3d239b12-ea2d-40bd-8f3b-c9c123fccf44"
        username={supersetConfig.username}
        password={supersetConfig.password}
        guestUsername={supersetConfig.guestUsername}
        guestFirstName={supersetConfig.guestFirstName}
        guestLastName={supersetConfig.guestLastName}
      />
    </div>
  );
};

export default DerivativesDataPage;