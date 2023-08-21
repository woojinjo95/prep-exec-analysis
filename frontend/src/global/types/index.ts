/**
 * 포인트 차트 데이터
 */
export type PointChartData = Date[]

/**
 * 영역 차트 데이터
 */
export type AreaChartData = {
  date: Date
  value: number
}[]

export interface Terminal {
  id: string
  mode: 'adb' | 'ssh'
}

export interface History {
  type: 'command' | 'response'
  message: string
}

export interface ShellMessage {
  shell_id: 1 | 2
  mode: 'adb' | 'ssh'
  data: { timestamp: string; module: 'stdin' | 'stdout' | 'stderr'; message: string }
}
