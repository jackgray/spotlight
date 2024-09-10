// app/financial-data/page.tsx

import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";

const LegislationPage: FC = () => {
  return (
    <div className="flex flex-col h-full">
      <h1 className={title()}>Legislation</h1>
      <br />
      {/* <h1 className={subtitle()}></h1> */}
      
    </div>
  );
};

export default LegislationPage;