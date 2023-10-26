import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/

// vite.config.js or vite.config.ts
export default defineConfig({
  build: {
    outDir: 'build', // Specify the output directory
  },
   server: {
    port: 3000,
    proxy: {
      '/bouquets/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
   },
  plugins: [react()],
})