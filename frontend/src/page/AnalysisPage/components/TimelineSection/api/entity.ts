/**
 * CPU, Memory
 */
export interface CPUAndMemory {
  timestamp: string
  cpu_usage: number
  memory_usage: number
}

export interface EventLog {
  timestamp: string
  service: string
  msg: string
  data: object
}
