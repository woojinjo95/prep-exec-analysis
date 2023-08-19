interface RunScenarioMessage {
  msg: 'run_scenario'
  data: { scenario_id: string }
}

interface StopScenarioMessage {
  msg: 'stop_scenario'
}

interface OnOffControlMessage {
  msg: 'on_off_control'
  data: { [key in 'enable_dut_power' | 'enable_hdmi' | 'enable_dut_wan']?: boolean }
}

interface RemoteControlMessage {
  msg: 'remocon_properties'
  data: { name?: string; type: 'ir' | 'bt' }
}

interface RemoconTransmitMessage {
  msg: 'remocon_transmit'
  data: {
    key: string
    type: 'ir' | 'bt'
    press_time: number
    name: string
  }
}

interface CommandMessage {
  msg: 'shell'
  data: {
    command: string
    shell_id: 1 | 2
  }
}

interface AnalysisMessage {
  msg: 'analysis'
  data: {
    measurement: (
      | 'freeze'
      | 'boot'
      | 'channel_change_time'
      | 'log_level_finder'
      | 'log_pattern_matching'
      | 'loudness'
      | 'macroblock'
      | 'network_filter'
      | 'process_lifecycle_analysis'
      | 'resume'
    )[]
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
)

export type SubscribeMessage<T> = {
  level: 'debug' | 'info' | 'warning' | 'error' | 'critical' | 'fatal'
  time: number
  msg: string
  data: T
  service: string
}
