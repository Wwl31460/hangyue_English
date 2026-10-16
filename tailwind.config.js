/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      // 主色：深蓝 / 青绿，学生友好、清爽专注
      colors: {
        brand: {
          50: '#eef6fb', 100: '#d6e9f5', 200: '#abd2ea', 300: '#79b5da',
          400: '#3f93c6', 500: '#1f6fae', 600: '#155488', 700: '#114268',
          800: '#0f3857', 900: '#0b2c46',
        },
        accent: {
          50: '#eafaf7', 100: '#c7f1ea', 200: '#92e3d6', 300: '#54cdbc',
          400: '#23b09c', 500: '#0e9c8b', 600: '#0a7e70', 700: '#0a655b',
          800: '#0b514a', 900: '#0a443e',
        },
      },
      fontFamily: {
        sans: [
          '-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', '"PingFang SC"',
          '"Microsoft YaHei"', 'system-ui', 'sans-serif',
        ],
      },
      boxShadow: {
        soft: '0 10px 30px -12px rgba(11,44,70,0.22)',
        card: '0 6px 20px -10px rgba(11,44,70,0.18)',
        glow: '0 12px 28px -10px rgba(14,108,102,0.45)',
      },
      borderRadius: { '3xl': '1.5rem' },
      keyframes: {
        fadeup: {
          '0%': { opacity: '0', transform: 'translateY(8px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
        pop: {
          '0%': { transform: 'scale(0.96)' },
          '100%': { transform: 'scale(1)' },
        },
      },
      animation: {
        fadeup: 'fadeup .35s ease both',
        pop: 'pop .2s ease both',
      },
    },
  },
  plugins: [],
};
