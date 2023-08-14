const config = {
  backend: {
    protocol: import.meta.env.VITE_BACKEND_PROTOCOL || window.location.protocol,
    hostname: import.meta.env.VITE_BACKEND_HOSTNAME || window.location.hostname,
    port: import.meta.env.VITE_BACKEND_PORT,
  },
  streaming: {
    protocol: import.meta.env.VITE_STREAMING_PROTOCOL || window.location.protocol,
    hostname: import.meta.env.VITE_STREAMING_HOSTNAME || window.location.hostname,
    port: import.meta.env.VITE_STREAMING_PORT,
    pathname: import.meta.env.VITE_STREAMING_PATHNAME,
  },
} as const

const AppURL = {
  baseURL: `${config.backend.protocol}://${config.backend.hostname}:${config.backend.port}`,
  websocketURL: {
    client: `ws://${config.backend.hostname}:${config.backend.port}/api/v1/client/ws`,
  },
  streamingURL: `${config.streaming.protocol}://${config.streaming.hostname}:${config.streaming.port}${config.streaming.pathname}`,
}

export default AppURL
