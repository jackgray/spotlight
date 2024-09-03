// app/financial-data/page.tsx

import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard"; // Make sure the path is correct
import { supersetConfig } from "@/lib/envConfig";

const FtdPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <h1 className={title()}>Financial Market Data</h1>
      <h1 className={subtitle()}>Fails To Deliver</h1>
      
      <SupersetDashboard
        dashboardTitle="Historical Regulation SHO Threshold Lists"
        supersetUrl={supersetConfig.supersetUrl}
        dashboardId="b6d818b2-e884-49c2-8e88-e43230394f97"
        username={supersetConfig.username}
        password={supersetConfig.password}
        guestUsername={supersetConfig.guestUsername}
        guestFirstName={supersetConfig.guestFirstName}
        guestLastName={supersetConfig.guestLastName}
      />
    </div>
  );
};

export default FtdPage;