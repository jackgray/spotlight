import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard"; // Make sure the path is correct
import { supersetConfig } from "@/lib/envConfig";
import ScrollingTabBar from '@/components/scrollingTabBar';
import { tabs } from './tabs';

const FinanceLobbyingPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <h1 className={subtitle()}>Financial Institute Lobbying</h1>
      <ScrollingTabBar tabs={tabs} />
      <SupersetDashboard
        dashboardTitle="Financial Institutions and Lobbying Spending"
        supersetUrl={supersetConfig.supersetUrl}
        dashboardId=""
        username={supersetConfig.username}
        password={supersetConfig.password}
        guestUsername={supersetConfig.guestUsername}
        guestFirstName={supersetConfig.guestFirstName}
        guestLastName={supersetConfig.guestLastName}
      />
    </div>
  );
};

export default FinanceLobbyingPage;