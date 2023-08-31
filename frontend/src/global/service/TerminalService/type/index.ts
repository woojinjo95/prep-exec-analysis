export interface CommandTransmit {
  type: 'shell'
  data: {
    command: string
  }
}
