// app/financial-data/page.tsx

import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard"; // Make sure the path is correct
import { supersetConfig } from "@/lib/envConfig";
import InfoPopover from '@/components/InfoPopover';
import DescriptionBox from '@/components/DescriptionBox';

const MarketCatDataPage: FC = () => {
    return (
        <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
            <h1 className={title()}>Market Data</h1>
            <div>
                <InfoPopover 
                    button_text="Dataset Info"
                    popover_header="Header"
                    popover_text="Info about this dataset here."
                />                
                <InfoPopover 
                    button_text="Code"
                    popover_header="Inspect the code that generated these datasets"
                    popover_text="https://github.com/jackgray/spotlight/main/producers/finance/cat"
                />
            </div>
            <DescriptionBox
                label="More about the data"
                text="More here later"
            />
            <SupersetDashboard
                dashboardTitle="Consolidated Auditing Trail"
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

export default MarketCatDataPage;