import { IPLimitProtocol } from '@global/api/entity'
import { AnalysisType } from '@global/constant'

/**
 * 블럭 재생 시작 publish 메시지
 */
interface RunScenarioMessage {
  msg: 'start_playblock'
  data: { scenario_id: string }
}

/**
 * 블럭 재생 중단 publish 메시지
 */
interface StopScenarioMessage {
  msg: 'stop_playblock'
}

/**
 * 환경설정 - on/off control 변경 publish 메시지
 */
interface OnOffControlMessage {
  msg: 'on_off_control'
  data: { [key in 'enable_dut_power' | 'enable_hdmi' | 'enable_dut_wan']?: boolean }
}

/**
 * 환경설정 - 캡처보드 초기화(Screen) 메시지
 */
interface CaptureBoardMessage {
  msg: 'capture_board'
  data: { action: 'refresh' }
}

/**
 * 환경설정 - Network Emulation On 메시지 Body
 */
interface NetworkEmulationOnMessageBody {
  action: 'start'
}

/**
 * 환경설정 - Network Emulation Off 메시지 Body
 */
interface NetworkEmulationOffMessageBody {
  action: 'stop'
}

interface NetworkEmulationResetMessageBody {
  action: 'reset'
}

/**
 * 환경설정 - Network Emulation - Packet Control 변경 메시지 Body
 */
interface PacketControlMessageBody {
  action: 'update'
  packet_bandwidth?: number
  packet_delay?: number
  packet_loss?: number
}

/**
 * 환경설정 - Network Emulation - IP 제한 변경 메시지 Body
 */
interface ConfiguringIPLimitMessageBody {
  action: 'create' | 'update' | 'delete'
  packet_block?: {
    id?: string
    ip?: string
    port?: string | number
    protocol?: IPLimitProtocol
  }
}

/**
 * 환경설정 - network emulation 변경 publish 메시지
 */
interface NetworkEmulationMessage {
  msg: 'network_emulation'
  data:
    | NetworkEmulationOnMessageBody
    | NetworkEmulationOffMessageBody
    | NetworkEmulationResetMessageBody
    | PacketControlMessageBody
    | ConfiguringIPLimitMessageBody
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
    measurement: (keyof typeof AnalysisType)[]
  }
}

type MessageLevel = 'debug' | 'info' | 'warning' | 'error' | 'critical' | 'fatal'

export type PublishMessage = {
  level?: MessageLevel
  time?: number
} & (
  | RunScenarioMessage
  | StopScenarioMessage
  | OnOffControlMessage
  | CaptureBoardMessage
  | RemoteControlMessage
  | RemoconTransmitMessage
  | CommandMessage
  | AnalysisMessage
  | NetworkEmulationMessage
)

type SubscribeCommandMessage<T> = {
  level: MessageLevel
  time: number
  msg: string
  data: T
  service: string
}

type SubscribeLoudnessMessage = {
  service: string
  level: MessageLevel
  time: number
  t: number
  M: number
  I: number
  inactive: boolean
}

export type SubscribeMessage<T> = SubscribeCommandMessage<T> & SubscribeLoudnessMessage
