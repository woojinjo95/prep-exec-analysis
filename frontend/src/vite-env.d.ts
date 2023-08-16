import React from 'react'

/// <reference types="vite/client" />
/// <reference types="vite-plugin-svgr/client" />

declare global {
  declare module '*.scss' {
    const styles: {
      [key: string]: string
    }
    export default styles
  }
  declare module '*.css' {
    const styles: {
      [key: string]: string
    }
    export default styles
  }
  declare module '*.png' {
    const value: string
    export = value
  }
  declare module '*.jpg' {
    const value: string
    export = value
  }
  declare module '*.svg' {
    export const ReactComponent: React.FC<React.SVGProps<SVGSVGElement>>
    const src: string
    export default src
  }
  declare module '*.mp4' {
    const value: string
    export = value
  }
  interface ImportMetaEnv {
    readonly VITE_BACKEND_PROTOCOL?: string
    readonly VITE_BACKEND_HOSTNAME?: string
    readonly VITE_BACKEND_PORT: string

    readonly VITE_STREAMING_PROTOCOL?: string
    readonly VITE_STREAMING_HOSTNAME?: string
    readonly VITE_STREAMING_PORT: string
    readonly VITE_STREAMING_PATHNAME: string
  }
  interface ImportMeta {
    readonly env: ImportMetaEnv
  }
}
