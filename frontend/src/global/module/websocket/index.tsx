import AppURL from '@global/constant/appURL'
import { useEffect } from 'react'
import { PublishMessage, SubscribeMessage } from './types'

const ws = new WebSocket(AppURL.websocketURL.client)
ws.onmessage = (message: MessageEvent<string>) => {
  const payload = JSON.parse(message.data) as SubscribeMessage<object>
  console.info({ 보내온_모듈_URL: (message.target as WebSocket)?.url, ...payload, time: payload.time * 1000 })
}

// FIXME: 모듈화!!!, 예외처리 등등등
const useWebsocket = <T extends object>({ onMessage }: { onMessage?: (message: SubscribeMessage<T>) => void } = {}) => {
  const ws = new WebSocket(AppURL.websocketURL.client)

  const sendMessage = (message: PublishMessage) => {
    ws.send(JSON.stringify({ level: 'info', service: 'frontend', time: new Date().getTime() / 1000, ...message }))
  }

  useEffect(() => {
    ws.onmessage = (message: MessageEvent<string>) => {
      const payload = JSON.parse(message.data) as SubscribeMessage<T>
      onMessage?.(payload)
    }
  }, [onMessage])

  return { ws, sendMessage }
}

export default useWebsocket
