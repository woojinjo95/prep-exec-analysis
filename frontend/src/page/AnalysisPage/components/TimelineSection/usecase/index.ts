import { DefaultChartDataType } from '@global/types'

/**
 * 차트 데이터 배열에서 원하는 숫자와 가장 가까운 숫자의 인덱스를 구하는 함수
 *
 * @param array duration - ms단위
 */
export const findNearIndex = (array: DefaultChartDataType[], target: number) => {
  let abs = array[array.length - 1].datetime
  let index = 0

  array.forEach(({ datetime: startDatetime, duration }, idx) => {
    const startDatetimeAbs = Math.abs(startDatetime - target)
    if (startDatetimeAbs < abs) {
      abs = startDatetimeAbs
      index = idx
    }

    if (!duration) return

    const endDatetimeAbs = Math.abs(startDatetime + duration - target)
    if (endDatetimeAbs < abs) {
      abs = endDatetimeAbs
      index = idx
    }
  })

  return index
}
