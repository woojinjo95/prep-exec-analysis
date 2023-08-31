// pubsub type을 기준으로 작성
export type RemoconTransmit = {
  msg: 'remocon_transmit'
  data: {
    key: string
    type: 'bt' | 'ir'
    press_time: number
    name: string
  }
}
// customKey는 data 배열을 전달받을 예정
export type CustomKeyTransmit = {
  msg: 'remocon_transmit'
  data: {
    key: string
    type: 'bt' | 'ir'
    press_time: number
    name: string
  }[]
}
