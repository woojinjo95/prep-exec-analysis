interface RunScenarioMessage {
  msg: 'run_scenario'
  data: { scenario_id: string }
}

interface StopScenarioMessage {
  msg: 'stop_scenario'
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
} & (RunScenarioMessage | StopScenarioMessage | CommandMessage)

export type SubscribeMessage<T> = {
  level: 'debug' | 'info' | 'warning' | 'error' | 'critical' | 'fatal'
  time: number
  msg: string
  data: T
}
