import type { Config } from "tailwindcss";


const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      colors: {
        primary: "#F1F3F2",
        secondary: "#4C4E4D",
        complementary: "#FFF200"
      },
      fontFamily: {
        "lato": ["Lato", "sans-serif"],
        "rubik": ["Rubik", "sans-serif"],
        "kanit": ["Kanit", "sans-serif"],
        "sans": ["Open Sans", "sans-serif"],
        "cabin": ["Cabin", "sans-serif"]
      }
    },
  },
  plugins: [],
};
export default config;
