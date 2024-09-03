// app/financial-data/page.tsx

import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard"; // Make sure the path is correct
import { supersetConfig } from "@/lib/envConfig";
import InfoPopover from '@/components/InfoPopover';
import DescriptionBox from '@/components/DescriptionBox';

const MarketPage: FC = () => {
    return (
        <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
            <h1 className={title()}>Market Data</h1>

            <DescriptionBox
                label="More about the data"
                text="More here later"
            />
            <SupersetDashboard
                dashboardTitle="Consolidated Auditing Trail"
                supersetUrl={supersetConfig.supersetUrl}
                dashboardId="fcc3fd0a-64f5-4d13-a564-1d04939094a3"
                username={supersetConfig.username}
                password={supersetConfig.password}
                guestUsername={supersetConfig.guestUsername}
                guestFirstName={supersetConfig.guestFirstName}
                guestLastName={supersetConfig.guestLastName}
            />
        </div>
    );
};

export default MarketPage;