// app/financial-data/page.tsx

import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard"; // Make sure the path is correct

const FinanceRegShoDataPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <h1 className={title()}>Financial Data</h1>
      <h1 className={subtitle()}>Regulation SHO Daily Threshold List Data</h1>
      
      <SupersetDashboard
        dashboardTitle="Historical Regulation SHO Threshold Lists"
        supersetUrl="https://superset.spotlight-us.com"
        dashboardId="b6d818b2-e884-49c2-8e88-e43230394f97"
        username="admin"
        password="admin"
        guestUsername="superstonker"
        guestFirstName="Great"
        guestLastName="Ape"
      />
    </div>
  );
};

export default FinanceRegShoDataPage;