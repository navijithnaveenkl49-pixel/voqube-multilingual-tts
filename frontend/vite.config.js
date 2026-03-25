import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      // Proxy audio files as well if they are mapped to /static
      '/static': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    },
  },
})
