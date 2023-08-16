import AppURL from '@global/constant/appURL'
import { useEffect } from 'react'
import { PublishMessage, SubscribeMessage } from './types'

// FIXME: 모듈화!!!, 예외처리 등등등
const useWebsocket = ({ onMessage }: { onMessage?: (message: SubscribeMessage) => void } = {}) => {
  const ws = new WebSocket(AppURL.websocketURL.client)

  const sendMessage = (message: PublishMessage) => {
    ws.send(JSON.stringify({ ...message, service: 'frontend' }))
  }

  useEffect(() => {
    ws.onmessage = (message: MessageEvent<string>) => {
      const payload = JSON.parse(message.data) as SubscribeMessage
      console.info({ 보내온_모듈_URL: (message.target as WebSocket)?.url, ...payload })
      onMessage?.(payload)
    }
  }, [onMessage])

  return { ws, sendMessage }
}

export default useWebsocket
