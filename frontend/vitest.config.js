import { fileURLToPath } from 'node:url'
import { mergeConfig } from 'vite'
import { configDefaults, defineConfig } from 'vitest/config'
import viteConfig from './vite.config'

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: 'jsdom',
      exclude: [...configDefaults.exclude, 'e2e/*'],
      root: fileURLToPath(new URL('./src', import.meta.url)),
      transformMode: {
        web: [/\.[jt]sx$/]
      },
      silent : true,
      coverage: {
        include: ['**/*.ts'],
        exclude: ['**/*.d.ts'],
      }
    }
  })
)
