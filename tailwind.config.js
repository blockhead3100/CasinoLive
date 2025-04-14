module.exports = {
  content: [
    './src/**/*.{html,js,jsx,ts,tsx}', // Adjust paths to match your project structure
    './src/styles/index.css',
  ],
  theme: {
    extend: {
      fontFamily: {
        inter: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
