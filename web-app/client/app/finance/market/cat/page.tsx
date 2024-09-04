import { FC } from 'react';
import { subtitle } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard";
import { supersetConfig } from "@/lib/envConfig";
import ScrollingTabBar from '@/components/scrollingTabBar';
import { tabs } from './tabs';

const MarketCatPage: FC = () => {
    return (
        <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
            <h1 className={subtitle()}>Consolidated Audit Trail</h1>
            <ScrollingTabBar tabs={tabs} />
            <SupersetDashboard
                dashboardTitle="Historical Consolidated Audit Trail Reports"
                supersetUrl={supersetConfig.supersetUrl}
                dashboardId="9d4bd71d-6c04-4c1d-a49a-f9d811b2ab88"
                username={supersetConfig.username}
                password={supersetConfig.password}
                guestUsername={supersetConfig.guestUsername}
                guestFirstName={supersetConfig.guestFirstName}
                guestLastName={supersetConfig.guestLastName}
            />
        </div>
    );
};

export default MarketCatPage;
