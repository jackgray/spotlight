// app/financial-data/page.tsx

import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";
import SupersetDashboard from "@/components/superset-dashboard";
import { supersetConfig } from "@/lib/envConfig";
import InfoPopover from '@/components/InfoPopover';
import DescriptionBox from '@/components/DescriptionBox';

const MarketPage: FC = () => {
    return (
        <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
            <h1 className={title()}>Market Data</h1>

            <DescriptionBox
                label="Currently offered datasets"
                text="Here you can explore data released by FINRA for the Consolidated Audit Trail (CAT) system, equity swap contracts, and fails to deliver/regulation SHO threshold lists. Use these datasets with caution as this project is still in infancy and has not fully validated the data. Each row includes a link to the original report it was scraped from, so that should make your verification efforts easier. "
            />
        </div>
    );
};

export default MarketPage;