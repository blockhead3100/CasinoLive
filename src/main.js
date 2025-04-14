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

// Ensure that your `index.css` file is correctly imported into your main entry file (e.g., `main.js`, `index.js`, or `App.jsx`). Add the following line at the top of your entry file:
import './styles/index.css'; // Ensure this import is present