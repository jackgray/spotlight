// app/financial-data/page.tsx

import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";

const PoliticsPage: FC = () => {
  return (
    <div className="flex flex-col h-full">
      <h1 className={title()}>Policy Dashboard</h1>
      <br />
      <h1 className={subtitle()}>Explore data related to policy and elections</h1>
      
    </div>
  );
};

export default PoliticsPage;