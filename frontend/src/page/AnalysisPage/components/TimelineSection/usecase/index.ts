/**
 * 배열에서 원하는 숫자와 가장 가까운 숫자의 인덱스를 구하는 함수
 */
export const findNearIndex = (array: { datetime: number }[], target: number) => {
  let abs = array[array.length - 1].datetime
  let index = 0

  array.forEach(({ datetime: value }, idx) => {
    const valueAbs = Math.abs(value - target)
    if (valueAbs < abs) {
      abs = valueAbs
      index = idx
    }
  })

  return index
}
