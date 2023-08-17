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

export interface ColorReference {
  /**
   * @format timestamp
   */
  timestamp: string

  /**
   * @min 0
   * @max 8
   */
  color_reference: number
}
