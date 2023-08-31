/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        // grey palette
        black: '#222222',
        'light-black': '#323339',
        charcoal: '#3E4048',
        'light-charcoal': '#4E525A',
        grey: '#8F949E',
        'light-grey': '#DFE0EE',
        'dark-grey': '#707070',

        // palette
        pink: '#D89B9B',
        red: '#E93535',
        orange: '#FF9900',
        'light-orange': '#FFBB00',
        yellow: '#FFDD00',
        navy: '#3A547D',
        green: '#97A442',
        'light-red': '#EB0050',

        // default active 색상
        primary: '#00B1FF',
      },
    },
  },
  plugins: [],
}
