export type RemoconTransmit = {
  msg: 'remocon_transmit'
  data: {
    key: string
    type: 'bt' | 'ir'
    press_time: number
    name: string
  }
}
