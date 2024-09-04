import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard"; // Make sure the path is correct
import { supersetConfig } from "@/lib/envConfig";
import ScrollingTabBar from '@/components/scrollingTabBar';
import { tabs } from './tabs';

const DefenseLobbyingPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <h1 className={subtitle()}>Defense Industry Lobbying</h1>
      <ScrollingTabBar tabs={tabs} />
      <SupersetDashboard
        dashboardTitle="Defense Contracting Companies and Lobbying Spending"
        supersetUrl={supersetConfig.supersetUrl}
        dashboardId="4d6f1a76-e48e-4066-8279-d622a700a417"
        username={supersetConfig.username}
        password={supersetConfig.password}
        guestUsername={supersetConfig.guestUsername}
        guestFirstName={supersetConfig.guestFirstName}
        guestLastName={supersetConfig.guestLastName}
      />
    </div>
  );
};

export default DefenseLobbyingPage;