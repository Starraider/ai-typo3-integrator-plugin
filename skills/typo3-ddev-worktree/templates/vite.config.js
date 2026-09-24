import { defineConfig } from "vite";
import typo3 from "vite-plugin-typo3";
import liveReload from 'vite-plugin-live-reload';

// In DDEV worktrees, VITE_SERVER_URI is provided via web_environment in config.vite.yaml:
// e.g. https://vite.<project_name>.ddev.site
const serverUri = process.env.VITE_SERVER_URI ? new URL(process.env.VITE_SERVER_URI) : null;

export default defineConfig({
    plugins: [
        typo3(),
        liveReload('packages/**/*.php', 'packages/**/*.html')
    ],
    // IMPORTANT: Do NOT set resolve.preserveSymlinks: true if your local packages use
    // relative imports (e.g. @import "../../../../../vendor/...") to reach the project root.
    // Preserving symlinks keeps the vendor/ symlink path depth instead of packages/* depth,
    // causing SCSS/CSS imports to fail with HTTP 500.
    server: {
        host: '0.0.0.0',
        port: 5173,
        strictPort: true,
        cors: true,
        origin: serverUri ? serverUri.origin : undefined,
        hmr: serverUri ? {
            host: serverUri.hostname,
            protocol: serverUri.protocol === 'https:' ? 'wss' : 'ws',
            clientPort: serverUri.port ? parseInt(serverUri.port, 10) : (serverUri.protocol === 'https:' ? 443 : 80),
        } : true,
    },
    build: {
        rollupOptions: {
            output: {
                generatedCode: {
                    preset: 'es2015',
                    symbols: true
                },
            }
        },
        minify: 'terser',
        target: 'es2015',
        terserOptions: {
            compress: {
                keep_fnames: true,
                drop_console: false,
                drop_debugger: false
            },
            mangle: {
                keep_fnames: true,
                keep_classnames: true
            }
        }
    }
});
