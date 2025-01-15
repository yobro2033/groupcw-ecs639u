import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import path from 'path';

// https://vitejs.dev/config/
export default defineConfig(({ mode }) => ({
    base:
        mode == "development"
            ? "http://localhost:5173/"
            : "/static/api/spa/",
    build: {
        emptyOutDir: true,
        outDir: "../api/static/api/spa",
    },
    server: {
        proxy: {
            '/Login': {
                target: 'http://127.0.0.1:8000', 
                changeOrigin: true,
            },
            '/Signup': {
                target: 'http://127.0.0.1:8000', 
                changeOrigin: true,
            },
        },
    },
    plugins: [vue()],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
}));
