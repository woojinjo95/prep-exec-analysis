/**
 * CPU, Memory
 */
export interface CPUAndMemory {
  /**
   * @format timestamp
   */
  timestamp: string
  cpu_usage: number
  memory_usage: number
}

export interface EventLog {
  /**
   * @format timestamp
   */
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

export interface Freeze {
  /**
   * @format timestamp
   */
  timestamp: string
}
