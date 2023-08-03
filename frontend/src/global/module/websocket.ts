// FIXME: 모듈화!!!, 예외처리 등등등
const ws = new WebSocket(
  import.meta.env.VITE_BACKEND_WEBSOCKET_URL || `ws://${window.location.hostname}:5000/api/v1/client/ws`,
)

export default ws
