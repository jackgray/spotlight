// import { Html, Head, Main, NextScript } from "next/document";

// export default function Document() {
//   return (
//     <Html>
//       <Head>
//         <script
//           dangerouslySetInnerHTML={{
//             __html: `
//               (function() {
//                 let theme = localStorage.getItem('theme');
//                 if (theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
//                   document.documentElement.setAttribute('data-theme', 'dark');
//                   document.documentElement.classList.add('dark');
//                 } else {
//                   document.documentElement.setAttribute('data-theme', 'light');
//                   document.documentElement.classList.remove('dark');
//                 }
//               })();
//             `,
//           }}
//         />
//       </Head>
//       <body>
//         <Main />
//         <NextScript />
//       </body>
//     </Html>
//   );
// }
