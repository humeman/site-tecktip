/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/**/*.{html,js,svelte,ts}',
    "./node_modules/flowbite-svelte/**/*.{html,js,svelte,ts}",
  ],
  theme: {
    fontFamily: {
      'sans': ['Secular One', 'sans-serif'],
      'serif': ['Secular One', 'sans-serif'],
      'mono': ['Chivo Mono', 'monospace']
    },
    extend: {
      dropShadow: {
        'dark3xl': '15px 15px 20px rgba(255, 255, 255, 0.25)',
        '3xl': '15px 15px 20px rgba(0, 0, 0, 0.4)',
      },
      boxShadow: {
        '3xl': '0 35px 60px -15px rgba(0, 0, 0, 1)',
      }
    },
  },
  variants: {
    fill: ['hover', 'focus'], // this line does the trick
  },
  plugins: [
    require('flowbite/plugin')
  ],
  darkMode: "class"
}
