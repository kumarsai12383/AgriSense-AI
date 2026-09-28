import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: false,
    proxy: {
      '/health': 'http://localhost:8000',
      '/farm': 'http://localhost:8000',
      '/crop': 'http://localhost:8000',
      '/ai': 'http://localhost:8000',
      '/sensor': 'http://localhost:8000',
      '/disease': 'http://localhost:8000',
      '/farmer': 'http://localhost:8000',
      '/farmers': 'http://localhost:8000',
      '/live': {
        target: 'ws://localhost:8000',
        ws: true
      }
    }
  }
})
