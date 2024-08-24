
import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard"; // Make sure the path is correct

const FinanceSwapsDataPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <h1 className={title()}>Financial Data</h1>
      <h1 className={subtitle()}>Swap Contract Data</h1>
  
      <p>
        Note: the other date provided on this site are derived from open source code available in the github project linked on this site. The swap data that is currently displayed was compiled by redditor bobprice, and has not been fully verified.
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