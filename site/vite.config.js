import { defineConfig } from "vite";

export default defineConfig({
  root: "./",
  base: "/model-ops-control-plane/",
  build: {
    outDir: "dist",
    emptyOutDir: true,
  },
});
