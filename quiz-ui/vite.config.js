
import {
  defineConfig,
  loadEnv 
} from 'vite'
import vue from '@vitejs/plugin-vue'

const path = require('path')

export default ({ mode }) => {
  // eslint-disable-next-line no-undef
  process.env = {...process.env, ...loadEnv(mode, process.cwd())};

  return defineConfig({
    plugins: [vue()],
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src'),
      }
    },
    build: {
      emptyOutDir: true
    }
  });
}