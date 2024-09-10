import { FC } from 'react';
import { subtitle } from "@/components/primitives";

const PersonPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <h1 className={subtitle()}>Things you can vote on in your district</h1>
    </div>
  );
};

export default PersonPage;