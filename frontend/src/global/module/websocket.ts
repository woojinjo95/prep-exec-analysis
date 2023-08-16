import AppURL from '@global/constant/appURL'

// FIXME: 모듈화!!!, 예외처리 등등등
const ws = new WebSocket(AppURL.websocketURL.client)

export default ws
