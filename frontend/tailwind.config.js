/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // palette
        black: '#222222',
        'light-black': '#323339',
        charcoal: '#3E4048',
        'light-charcoal': '#4E525A',
        grey: '#8F949E',
        'light-grey': '#DFE0EE',

        // default active 색상
        primary: '#00B1FF',
      },
    },
  },
  plugins: [],
}
