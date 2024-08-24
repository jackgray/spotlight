import { subtitle, title } from "@/components/primitives";

export default function DataPage() {
  return (
    <div>
      <h1 className={title()}>Data</h1>
      <h1 className={subtitle()}>Finance Data</h1>
      <h1 className={subtitle()}>Lobbying Data</h1>
      <h1 className={subtitle()}>Congressional Data</h1>
    </div>
  );
}
