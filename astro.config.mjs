import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
export default defineConfig({
  base: '/tochka-auto-demo/',
  vite: { plugins: [tailwindcss()] },
  server: { port: 4321 },
  devToolbar: { enabled: false }
});
