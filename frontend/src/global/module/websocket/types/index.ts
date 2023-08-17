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

interface CommandMessage {
  msg: 'shell'
  data: {
    command: string
    shell_id: 1 | 2
  }
}

export type PublishMessage = {
  level?: 'debug' | 'info' | 'warning' | 'error' | 'critical' | 'fatal'
  time?: number
} & (RunScenarioMessage | StopScenarioMessage | OnOffControlMessage | RemoteControlMessage | CommandMessage)

export type SubscribeMessage<T> = {
  level: 'debug' | 'info' | 'warning' | 'error' | 'critical' | 'fatal'
  time: number
  msg: string
  data: T
  service: string
}
