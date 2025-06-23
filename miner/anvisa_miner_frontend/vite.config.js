import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(),tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    host: true,
    port: 5173,
    strictPort: true,
    hmr: {
      port: 5173,
    },
    watch: {
      usePolling: true,
    },
    allowedHosts: [
      '5173-ijc7gnx0ckiyiifuadaoj-a1790518.manusvm.computer'
    ]
  }
})
