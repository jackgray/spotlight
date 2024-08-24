// app/financial-data/page.tsx

import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard"; // Make sure the path is correct

const FinanceCatDataPage: FC = () => {
    console.log(process.env.NEXT_PUBLIC_SUPERSET_URL)
    return (
        <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>

            <h1 className={title()}>Financial Data</h1>
            <h1 className={subtitle()}>Consolidated Auditing Trail</h1>
            
            <SupersetDashboard
                dashboardTitle="Consolidated Auditing Trail"
                supersetUrl="https://superset.spotlight-us.com"
                dashboardId="9d4bd71d-6c04-4c1d-a49a-f9d811b2ab88"
                username="admin"
                password="admin"
                guestUsername="superstonker"
                guestFirstName="Great"
                guestLastName="Ape"
            />
        </div>
    );
};

export default FinanceCatDataPage;