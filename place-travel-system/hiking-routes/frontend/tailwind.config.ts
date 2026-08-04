import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#060a08",
        surface: "#0f1713",
        card: "#121c16",
        border: "#1c2e22",
        "border-l": "#253a2c",
        accent: "#c9a24e",
        "accent-2": "#e0b85c",
        "accent-3": "#5a9e7a",
        "accent-4": "#b86b4a",
        "accent-5": "#6888cc",
        text: "#e2ddd4",
        "text-dim": "#8a9a8e",
        "text-muted": "#4a5a4e",
      },
      fontFamily: {
        display: ["Cormorant Garamond", "Noto Serif SC", "serif"],
        body: ["Noto Serif SC", "Noto Sans SC", "serif"],
        mono: ["DM Mono", "monospace"],
        sans: ["Noto Sans SC", "sans-serif"],
      },
      borderRadius: {
        DEFAULT: "14px",
        sm: "8px",
      },
    },
  },
  plugins: [],
};
export default config;
