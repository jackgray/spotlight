// app/financial-data/page.tsx

import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";

const FinanceDataPage: FC = () => {
  return (
    <div className="flex flex-col h-full">
      <h1 className={title()}>Financial Data</h1>
      <br />
      <h1 className={subtitle()}>Drop down list to data categories goes here</h1>
      
    </div>
  );
};

export default FinanceDataPage;