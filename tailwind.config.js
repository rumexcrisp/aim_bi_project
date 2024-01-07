module.exports = {
  content: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
  theme: {
    extend: {},
    darkMode: 'class',
    fontFamily: {
      Roboto: ["Roboto, sans-serif"],
      Nabla: ["Nabla, system-ui"],
    },
    container: {
      padding: "2rem",
      center: true,
    },
    screens: {
      sm: "640px",
      md: "768px",
    },
  },
  plugins: [],
};
