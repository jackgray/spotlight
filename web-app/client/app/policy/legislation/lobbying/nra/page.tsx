import { FC } from 'react';
import { subtitle, title } from "@/components/primitives";

const NRALobbyingPage: FC = () => {
  return (
    <div style={{ width: '100%', height: '100%', overflow: 'auto' }}>
      <h1 className={subtitle()}>National Rifle Association</h1>
    </div>
  );
};

export default NRALobbyingPage;