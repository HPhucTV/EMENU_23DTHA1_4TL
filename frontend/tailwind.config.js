/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: '#1E4332',
          dark: '#163325',
          soft: '#E9EFEA',
          muted: '#DCE5DE',
        },
        cream: {
          DEFAULT: '#F8F7F3',
          subtle: '#F1EFE9',
        },
        hold: {
          bg: '#F3E8D2',
          text: '#6E4B1F',
        },
        cancel: {
          bg: '#F6E4E1',
          text: '#8F3A2E',
        },
      },
      fontFamily: {
        serif: ['"Cormorant Garamond"', '"Playfair Display"', 'Georgia', 'serif'],
        sans: ['"Be Vietnam Pro"', 'Inter', 'system-ui', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
