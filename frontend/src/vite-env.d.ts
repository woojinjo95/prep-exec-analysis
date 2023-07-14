/// <reference types="vite/client" />
/// <reference types="vite-plugin-svgr/client" />

declare global {
  interface ImportMetaEnv {
    readonly VITE_BACKEND_URL: string
  }

  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
}
