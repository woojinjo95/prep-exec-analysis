/**
 * API Response
 */
export interface Response<T> {
  items: T
}

/**
 * API 페이지네이션 Response
 *
 * @param items 페이징처리된 데이터
 * @param jumpNext 10페이지 건너뛴 다음 페이지
 * @param jumpPrev 10페이지 건너뛴 이전 페이지
 * @param next 다음 페이지
 * @param pages 전체 페이지 개수
 * @param prev 이전 페이지
 * @param total 데이터 총 개수
 */
export interface PaginationResponse<T> extends Response<T> {
  jumpNext: number
  jumpPrev: number
  next: number
  pages: number
  prev: number
  total: number
}

/**
 * 시나리오 리스트 아이템
 */
export interface ScenarioSummary {
  id: string
  name: string
  tags: string[]
  updated_at: number
}

/**
 * 하드웨어 설정 - IP 제한
 */
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
  remote_control_type: 'ir' | 'bt'
  enable_dut_power: boolean
  enable_hdmi: boolean
  enable_dut_wan: boolean
  enable_network_emulation: boolean
  packet_bandwidth: number
  packet_delay: number
  packet_loss: number
  stb_connection?: {
    mode: 'adb' | 'ssh'
    host: string | null
    port: string | null
    username?: string | null
    password?: string | null
  }
  ip_limit?: IPLimit[]
}
