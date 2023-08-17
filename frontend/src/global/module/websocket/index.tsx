import AppURL from '@global/constant/appURL'
import { useCallback, useEffect, useMemo } from 'react'
import { PublishMessage, SubscribeMessage } from './types'

const ws = new WebSocket(AppURL.websocketURL.client)
ws.onmessage = (message: MessageEvent<string>) => {
  const payload = JSON.parse(message.data) as SubscribeMessage<object>
  console.info({ 보내온_모듈_URL: (message.target as WebSocket)?.url, ...payload, time: payload.time * 1000 })
}

// FIXME: 모듈화!!!, 예외처리 등등등
const useWebsocket = <T extends object>({ onMessage }: { onMessage?: (message: SubscribeMessage<T>) => void } = {}) => {
  const ws = useMemo(() => new WebSocket(AppURL.websocketURL.client), [])

  /**
   * websocket 메시지 전송 함수
   *
   * @default level 'info'
   * @default service 'frontend'
   * @default time new Date().getTime() / 1000
   */
  const sendMessage = useCallback(
    (message: PublishMessage) => {
      ws.send(JSON.stringify({ level: 'info', service: 'frontend', time: new Date().getTime() / 1000, ...message }))
    },
    [ws],
  )

  useEffect(() => {
    ws.onmessage = (message: MessageEvent<string>) => {
      const payload = JSON.parse(message.data) as SubscribeMessage<T>
      onMessage?.(payload)
    }
  }, [onMessage])

  return { ws, sendMessage }
}

export default useWebsocket
