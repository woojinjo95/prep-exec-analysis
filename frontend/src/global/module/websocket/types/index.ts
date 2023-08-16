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

export type PublishMessage = {
  level?: 'debug' | 'info' | 'warning' | 'error' | 'critical' | 'fatal'
  time?: number
} & (RunScenarioMessage | StopScenarioMessage | OnOffControlMessage)

export type SubscribeMessage = {
  level: 'debug' | 'info' | 'warning' | 'error' | 'critical' | 'fatal'
  time: number
  msg: string
  data: JSON
}
