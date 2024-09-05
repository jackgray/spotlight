import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard"; // Make sure the path is correct
import { supersetConfig } from "@/lib/envConfig";
import ScrollingTabBar from '@/components/scrollingTabBar';
import { tabs } from './tabs';

const CrowContributionsPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>  
      <h1 className={subtitle()}>Crow Fund Contributions</h1>
      <ScrollingTabBar tabs={tabs} />
      <SupersetDashboard
        dashboardTitle="Crow Family Donations provided by OpenSecrets"
        supersetUrl={supersetConfig.supersetUrl}
        dashboardId="7c324fec-ed90-4cb0-a764-a276282a575c"
        username={supersetConfig.username}
        password={supersetConfig.password}
        guestUsername={supersetConfig.guestUsername}
        guestFirstName={supersetConfig.guestFirstName}
        guestLastName={supersetConfig.guestLastName}
      />
    </div>
  );

};

export default CrowContributionsPage;