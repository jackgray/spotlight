import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";


const BillsPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <h1 className={subtitle()}>Bill On the Floor</h1>
    </div>
  );
};

export default BillsPage;