import { FC } from 'react';
import { subtitle } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard";
import { supersetConfig } from "@/lib/envConfig";
import ScrollingTabBar from '@/components/scrollingTabBar';
import { tabs } from './tabs';

const Rule605Page: FC = () => {
    return (
        <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
            <h1 className={subtitle()}>Rule 605</h1>
            <ScrollingTabBar tabs={tabs} />
            <SupersetDashboard
                dashboardTitle="Rule 605"
                supersetUrl={supersetConfig.supersetUrl}
                dashboardId="3b6e47e6-4c38-4bba-bfb9-761e794abcab"
                username={supersetConfig.username}
                password={supersetConfig.password}
                guestUsername={supersetConfig.guestUsername}
                guestFirstName={supersetConfig.guestFirstName}
                guestLastName={supersetConfig.guestLastName}
            />
        </div>
    );
};

export default Rule605Page;
