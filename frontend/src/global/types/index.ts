export type DefaultChartDataType = {
  datetime: number // millisecond
  duration?: number // millisecond
}

/**
 * 포인트 차트 데이터
 */
export type PointChartData = (Pick<DefaultChartDataType, 'datetime'> & { color: string })[]

/**
 * 영역 차트 데이터
 */
export type AreaChartData = (Pick<DefaultChartDataType, 'datetime'> & {
  value: number
})[]

/**
 * 범위 차트 데이터
 *
 * @property {number} duration 지속시간. 단위: ms
 */
export type RangeChartData = (Required<DefaultChartDataType> & { color: string })[]

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
