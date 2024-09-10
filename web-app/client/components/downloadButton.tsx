// import { useState } from 'react';
// import { Button } from '@nextui-org/button';

// const DownloadButton: React.FC = () => {
//   const [format, setFormat] = useState<'csv' | 'json'>('csv'); // Explicitly type the state

//   const downloadTable = async () => {
//     const res = await fetch(`/api/download?format=${format}`);
//     if (!res.ok) {
//       console.error('Failed to fetch data');
//       return;
//     }

//     const blob = await res.blob();
//     const url = window.URL.createObjectURL(blob);

//     const a = document.createElement('a');
//     a.href = url;
//     a.download = `data.${format}`;
//     document.body.appendChild(a);
//     a.click();
//     window.URL.revokeObjectURL(url);
//   };

//   return (
//     <div>
//       <label>
//         Select format:
//         <select value={format} onChange={(e) => setFormat(e.target.value as 'csv' | 'json')}>
//           <option value="csv">CSV</option>
//           <option value="json">JSON</option>
//         </select>
//       </label>
//       <button onClick={downloadTable}>Download Table</button>
//     </div>
//   );
// };

// export default DownloadButton;
