/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'judicial-cream': '#F7F4EF',
        'judicial-brown': '#1C1A18',
        'judicial-gold': '#C19A36',
        'judicial-gold-light': '#D4B460',
        'judicial-beige': '#EAE5DC',
        'judicial-beige-dark': '#DCD5CA',
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['Roboto Slab', 'serif'], // For headings if needed
      },
      animation: {
        'spin-slow': 'spin 60s linear infinite',
        'fade-in': 'fadeIn 0.5s ease-out forwards',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0', transform: 'translateY(10px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        }
      }
    },
  },
  plugins: [],
}
