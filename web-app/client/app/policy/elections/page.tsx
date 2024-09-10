
import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";

const ElectionsPage: FC = () => {
  return (
    <div className="flex flex-col h-full">
      <h1 className={title()}>Vote in your area</h1>
      <br />
      <h1 className={subtitle()}>Explore information about elections in your district</h1>
      
    </div>
  );
};

export default ElectionsPage;