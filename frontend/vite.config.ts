import { defineConfig } from 'vite'
import { resolve } from 'path'

import react from '@vitejs/plugin-react-swc'
import eslint from 'vite-plugin-eslint'
import tsconfigPaths from 'vite-tsconfig-paths'
import svgr from 'vite-plugin-svgr'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    eslint({
      include: './src/**/*.{ts,tsx,js,jsx}',
    }),
    tsconfigPaths(),
    svgr(),
  ],
  resolve: {
    alias: [
      { find: '@src', replacement: resolve(__dirname, 'src') },
      { find: '@assets', replacement: resolve(__dirname, 'src/assets') },
    ],
  },
  server: {
    host: '0.0.0.0',
    port: 3000,
    watch: {
      usePolling: true,
    },
  },
  preview: {
    port: 3000,
  },
})
//
