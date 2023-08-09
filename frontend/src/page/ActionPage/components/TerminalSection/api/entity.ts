export interface IPLimit {
  id: string
  ip?: string
  port?: string
  protocol: 'all' | 'tcp' | 'udp'
}

/**
 * 하드웨어 설정
 */
export interface HardwareConfiguration {
  remote_control_type: 'ir' | 'bluetooth'
  enable_dut_power: boolean
  enable_hdmi: boolean
  enable_dut_wan: boolean
  enable_network_emulation: boolean
  packet_bandwidth: number
  packet_delay: number
  packet_loss: number
  stb_connection?: {
    type: 'adb' | 'ssh'
    ip: string
    port: string
    username?: string
    password?: string
  }
  ip_limit?: IPLimit[]
}
