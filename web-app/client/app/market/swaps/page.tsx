
import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard"; // Make sure the path is correct
import { supersetConfig } from "@/lib/envConfig";

const FinanceSwapsDataPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <h1 className={title()}>Financial Data</h1>
      <h1 className={subtitle()}>Derivatives Trading Data</h1>
      <p>
        Note: Derivatives data are incredibly complex and these charts may not present meaningful metrics without careful filtering. For example, a new record is made any time an existing swap contract is modified, so querying notational sums or other aggregated values must take this into effect. 
      </p>
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

export default FinanceSwapsDataPage;