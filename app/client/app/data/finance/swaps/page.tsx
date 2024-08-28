
import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard"; // Make sure the path is correct

const FinanceSwapsDataPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <h1 className={title()}>Financial Data</h1>
      <h1 className={subtitle()}>Swap Contract Data</h1>
  
      <p>
        Note: Derivatives contracts are extremely easy to misinterpret as they are high dimensional and can take so many different shapes and forms. Use this data with caution. It is still in the process of being aggregated and normalized. Notional sums by date without the proper filtering are inaccurate, as swap records are ADDED (not modified) whenever a modification is made to the agreement, resulting in inflated notional sums for a given contract. 
      </p>

      <SupersetDashboard
        dashboardTitle="Historical Regulation SHO Threshold Lists"
        supersetUrl="https://superset.spotlight-us.com"
        dashboardId="3d239b12-ea2d-40bd-8f3b-c9c123fccf44"
        username="admin"
        password="admin"
        guestUsername="superstonker"
        guestFirstName="Great"
        guestLastName="Ape"
      />
    </div>
  );
};

export default FinanceSwapsDataPage;