import {nextui} from '@nextui-org/theme'

/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
    './node_modules/@nextui-org/theme/dist/**/*.{js,ts,jsx,tsx}'
  ],
  theme: {
    extend: {
      colors: {
        gunmetal: '#2a3439',
      },
    },
  },
  darkMode: "class",
  plugins: [nextui()],
}

// module.exports = {
//   theme: {
//     extend: {
//       colors: {
//         // Define your black and white theme
//         primary: '#000000',
//         secondary: '#ffffff',
//       }
//     }
//   },
//   plugins: [
//     require('@tailwindcss/typography'), // To apply the `prose` class
//   ]
// }