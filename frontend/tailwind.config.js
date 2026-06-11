export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  darkMode: "class",
  theme: {
    extend: {
      colors: {
        ink: "#101828",
        signal: "#14b8a6",
        ember: "#f97316",
        violet: "#7c3aed"
      },
      boxShadow: {
        panel: "0 18px 45px rgba(15, 23, 42, 0.12)"
      }
    }
  },
  plugins: []
};

