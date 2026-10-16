import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// 移动端优先的纯前端原型：本地存储，无后端
export default defineConfig({
  plugins: [react()],
  server: { host: true, port: 5173 },
});
