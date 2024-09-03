import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";


const CampaignFinancePage: FC = () => {
    return (
        <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
            <h1 className={title()}>Financial Data</h1>

        </div>
    );
};

export default CampaignFinancePage;