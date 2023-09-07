import { defineConfig } from 'vite';
import laravel, { refreshPaths } from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: [
                'resources/css/app.css',
                'resources/js/app.js',
            ],
            refresh: [
                ...refreshPaths,
                'app/Livewire/**',
            ],
        }),
    ],
    resolve: {
        alias: {
          'buffer': 'buffer' // This ensures that any import of 'buffer' points to the installed package
        }
      },
      build: {
        rollupOptions: {
          external: ['buffer'], // This tells Vite to treat 'buffer' as an external dependency
        }
      }
});
