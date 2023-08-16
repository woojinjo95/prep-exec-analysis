interface RunScenarioMessage {
  msg: 'run_scenario'
  data: { scenario_id: string }
}

interface StopScenarioMessage {
  msg: 'stop_scenario'
}

export type PublishMessage = {
  level: 'debug' | 'info' | 'warning' | 'error' | 'critical' | 'fatal'
  time: number
} & (RunScenarioMessage | StopScenarioMessage)

export type SubscribeMessage = {
  level: 'debug' | 'info' | 'warning' | 'error' | 'critical' | 'fatal'
  time: number
  msg: string
  data: JSON
}
