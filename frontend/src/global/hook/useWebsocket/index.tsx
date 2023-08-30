import AppURL from '@global/constant/appURL'
import { useCallback, useEffect, useRef } from 'react'
import { PublishMessage, SubscribeMessage } from './types'

const ReadyState = {
  CONNECTING: 0, // 소켓이 생성됐으나 연결은 아직 개방되지 않았습니다.
  OPEN: 1, // 연결이 개방되어 통신할 수 있습니다.
  CLOSING: 2, // 연결을 닫는 중입니다.
  CLOSED: 3, // 연결이 닫혔거나, 개방할 수 없었습니다.
} as const

const delay = (sec: number) => {
  return new Promise((resolve) => {
    setTimeout(resolve, sec * 1000)
  })
}

/**
 * 웹소켓 연결 hook
 *
 * @param onMessage 메시지 수신 callback
 * @return sendMessage 메시지 송신 function
 */
const useWebsocket = <T extends object>({ onMessage }: { onMessage?: (message: SubscribeMessage<T>) => void } = {}) => {
  const ws = useRef<WebSocket | null>(null)

  const connect = useCallback(async (): Promise<WebSocket | null> => {
    ws.current = null
    return new Promise((resolve, reject) => {
      ws.current = new WebSocket(AppURL.websocketURL.client)
      ws.current.onopen = () => {
        resolve(ws.current)
      }

      ws.current.onmessage = (message: MessageEvent<string>) => {
        const payload = JSON.parse(message.data) as SubscribeMessage<T>
        onMessage?.(payload)
      }

      ws.current.onerror = (e) => {
        console.log('websocket error: ', e)
        reject(e)
      }
    })
  }, [])

  /**
   * websocket 메시지 전송 함수
   *
   * @default level 'info'
   * @default service 'frontend'
   * @default time new Date().getTime() / 1000
   */
  const sendMessage = useCallback(async (message: PublishMessage) => {
    if (ws.current?.readyState === ReadyState.CONNECTING) {
      console.log('websocket connecting')
      await delay(1)
      await sendMessage(message)
    } else if (ws.current?.readyState === ReadyState.OPEN) {
      ws.current.send(
        JSON.stringify({ level: 'info', service: 'frontend', time: new Date().getTime() / 1000, ...message }),
      )
    } else {
      console.log('no websocket, try reconnect')
      await delay(1)
      await connect()
      await sendMessage(message)
    }
  }, [])

  useEffect(() => {
    connect()
  }, [])

  useEffect(() => {
    if (!ws.current) return

    ws.current.onmessage = (message: MessageEvent<string>) => {
      const payload = JSON.parse(message.data) as SubscribeMessage<T>
      onMessage?.(payload)
    }
  }, [onMessage])

  return { sendMessage }
}

export default useWebsocket
