import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          DEFAULT: "#0F1729", // dark navy used across the AthliQ mockups
          light: "#1B2542",
        },
      },
    },
  },
  plugins: [],
};

export default config;
