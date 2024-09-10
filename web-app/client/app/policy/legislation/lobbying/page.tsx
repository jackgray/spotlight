// app/financial-data/page.tsx

import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";

const LobbyingPage: FC = () => {
  return (
    <div className="flex flex-col h-full">
      <h1 className={title()}>Lobbying</h1>
      <br />
      {/* <h1 className={subtitle()}>Explore lobbying interests</h1> */}
      
    </div>
  );
};

export default LobbyingPage;