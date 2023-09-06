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
  testrun_count: number
  has_block: boolean
}

export type IPLimitProtocol = 'all' | 'tcp' | 'udp'

/**
 * 하드웨어 설정 - IP 제한
 */
export interface IPLimit {
  id: string
  ip?: string
  port?: string
  protocol: IPLimitProtocol
}

/**
 * 하드웨어 설정
 */
export interface HardwareConfiguration {
  remote_control_type: 'ir' | 'bt'
  dut_ip: string | null
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
  packet_block?: IPLimit[]
}

/**
 * Block type
 */
type BlockType =
  | 'remocon_transmit'
  | 'on_off_control'
  | 'shell'
  | 'packet_control'
  | 'packet_block'
  | 'monkey_test'
  | 'intelligent_monkey_test'
  | 'device_info'
  | 'remocon_properties'

/**
 * 서비스 상태
 *
 * `idle` 대기 (녹화 및 로그수집 X, 스트리밍 X)
 *
 * `streaming` 녹화 (녹화 및 로그수집 O, 스트리밍 O)
 *
 * `playblock` 재생 (녹화 및 로그수집 O, 스트리밍 O)
 *
 * `analysis` 분석 (녹화 및 로그수집 X, 스트리밍 X)
 */
export type ServiceState = 'idle' | 'streaming' | 'playblock' | 'analysis'

export interface Block {
  type: BlockType
  args: { key: string; value: string | number | boolean | object | null | undefined }[]
  name: string
  delay_time: number
  id: string
}

export interface BlockGroup {
  id: string
  repeat_cnt: number
  block: Block[]
}

export interface Scenario {
  id: string
  name: string
  is_active: boolean
  tags: string[]
  block_group: BlockGroup[]
}
/**
 * 로그 연결여부
 */
export type LogConnectionStatus = 'log_disconnected' | 'log_connected'

/**
 * 비디오 정보
 *
 * @param start_time 비디오 시작시간(테스트런 시작시간)
 * @param end_time 비디오 종료시간(테스트런 종료시간)
 * @param path 비디오 저장경로
 */
export interface VideoSummary {
  start_time: string
  end_time: string
  path: string
}

/**
 * 테스트런
 */
export interface TestRun {
  id: string
  updated_at: string
  measure_targets: string[]
}
