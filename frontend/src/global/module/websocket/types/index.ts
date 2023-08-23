import { IPLimitProtocol } from '@global/api/entity'

/**
 * 블럭 재생 시작 publish 메시지
 */
interface RunScenarioMessage {
  msg: 'run_scenario'
  data: { scenario_id: string }
}

/**
 * 블럭 재생 중단 publish 메시지
 */
interface StopScenarioMessage {
  msg: 'stop_scenario'
}

/**
 * 환경설정 - on/off control 변경 publish 메시지
 */
interface OnOffControlMessage {
  msg: 'on_off_control'
  data: { [key in 'enable_dut_power' | 'enable_hdmi' | 'enable_dut_wan']?: boolean }
}

/**
 * 환경설정 - network emulation 변경 publish 메시지
 */
interface NetworkEmulationMessage {
  msg: 'network_emulation'
  data: {
    action: 'start' | 'stop' | 'add' | 'del'
    packet_bandwidth?: number
    packet_delay?: number
    packet_loss?: number
    packet_block?: {
      ip?: string
      port?: string | number
      protocol?: IPLimitProtocol
    }
  }
}

/**
 * 환경설정 - remote control 변경 publish 메시지
 */
interface RemoteControlMessage {
  msg: 'remocon_properties'
  data: { name?: string; type: 'ir' | 'bt' }
}

/**
 * 리모컨 명령 publish 메시지
 */
interface RemoconTransmitMessage {
  msg: 'remocon_transmit'
  data: {
    key: string
    type: 'ir' | 'bt'
    press_time: number
    name: string
  }
}

/**
 * 터미널 - 명령어 입력 publish 메시지
 */
interface CommandMessage {
  msg: 'shell'
  data: {
    command: string
    shell_id: 1 | 2
  }
}

/**
 * 분석 시작 publish 메시지
 */
interface AnalysisMessage {
  msg: 'analysis'
  data: {
    measurement: ('freeze' | 'boot' | 'channel_change_time' | 'log_level_finder' | 'log_pattern_matching' | 'resume')[]
  }
}

export type PublishMessage = {
  level?: 'debug' | 'info' | 'warning' | 'error' | 'critical' | 'fatal'
  time?: number
} & (
  | RunScenarioMessage
  | StopScenarioMessage
  | OnOffControlMessage
  | RemoteControlMessage
  | RemoconTransmitMessage
  | CommandMessage
  | AnalysisMessage
  | NetworkEmulationMessage
)

export type SubscribeMessage<T> = {
  level: 'debug' | 'info' | 'warning' | 'error' | 'critical' | 'fatal'
  time: number
  msg: string
  data: T
  service: string
}
