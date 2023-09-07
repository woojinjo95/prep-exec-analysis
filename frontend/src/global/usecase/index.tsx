import { MILLISECONDS_PER_MINUTE, MILLISECONDS_PER_SECOND, MONTH_NAMES } from '@global/constant'

type DateToken =
  | 'YYYYMMDD'
  | 'YYYY-MM-DD'
  | 'YYYY.MM.DD'
  | 'YY.MM.DD'
  | 'HH:MM'
  | 'HH:MM:SS'
  | 'HH:MM:SS:MS'
  | 'AA HH:MM'
  | 'YYYY-MM-DD HH:MM'
  | 'YYYY-MM-DD HH:MM:SS'
  | 'YYYY-MM-DD HH:MM:SS:MS'
  | 'YYYY_MM_DD_HH_MM_SS_MS'
  | 'M DD YYYY, HH:MM AA'

/**
 * date format 함수
 */
export const formatDateTo = (type: DateToken, dateObject = new Date()): string => {
  const year = dateObject.getFullYear()
  const month = `0${dateObject.getMonth() + 1}`.slice(-2)
  const date = `0${dateObject.getDate()}`.slice(-2)
  const hour = String(dateObject.getHours()).padStart(2, '0')
  const minute = String(dateObject.getMinutes()).padStart(2, '0')
  const second = String(dateObject.getSeconds()).padStart(2, '0')
  const milliSec = dateObject.getMilliseconds()

  switch (type) {
    case 'YYYYMMDD':
      return `${year}${month}${date}`
    case 'YYYY-MM-DD':
      return `${year}-${month}-${date}`
    case 'YYYY.MM.DD':
      return `${year}.${month}.${date}`
    case 'YY.MM.DD':
      return `${year.toString().slice(2, 4)}.${month}.${date}`
    case 'HH:MM':
      return `${hour}:${minute}`
    case 'HH:MM:SS':
      return `${hour}:${minute}:${second}`
    case 'HH:MM:SS:MS':
      return `${hour}:${minute}:${second}:${String(milliSec).slice(0, 2).padStart(2, '0')}`
    case 'AA HH:MM': {
      if (dateObject.getHours() < 12) {
        return `오전 ${dateObject.getHours() === 0 ? '12' : dateObject.getHours()}:${minute}`
      }
      return `오후 ${dateObject.getHours() === 12 ? '12' : dateObject.getHours() - 12}:${minute}`
    }
    case 'YYYY-MM-DD HH:MM':
      return `${year}-${month}-${date} ${hour}:${minute}`
    case 'YYYY-MM-DD HH:MM:SS':
      return `${year}-${month}-${date} ${hour}:${minute}:${second}`
    case 'YYYY-MM-DD HH:MM:SS:MS':
      return `${year}-${month}-${date} ${hour}:${minute}:${second}.${milliSec}`
    case 'YYYY_MM_DD_HH_MM_SS_MS':
      return `${year}_${month}_${date}_${hour}_${minute}_${second}_${milliSec}`
    case 'M DD YYYY, HH:MM AA': {
      const monthName = MONTH_NAMES[dateObject.getMonth()]
      const currentDate = new Date()
      const isToday = !!(
        currentDate.getFullYear() === year ||
        currentDate.getMonth() === dateObject.getMonth() ||
        currentDate.getDate() === dateObject.getDate()
      )
      const AMPM = dateObject.getHours() < 12 ? 'AM' : 'PM'

      return `${isToday ? 'Today' : `${monthName} ${dateObject.getDate()} ${year}`}, ${hour}:${minute} ${AMPM}`
    }
    default:
      return `${year}${month}${date}`
  }
}
/**
 * 100단위로 ms를 끊어주는 함수
 */
export const formMsToHundred = (ms: number) => {
  if (ms < 100) return ms

  if (ms < 150) return 100

  if (ms >= 900) return 900

  return Math.round(ms / 100) * 100
}

/**
 * ms를 분, 초, ms로 끊어주는 함수
 */
export const changeMsToMinSecMs = (_ms: number) => {
  const m = Math.floor(_ms / MILLISECONDS_PER_MINUTE)
  const s = Math.floor((_ms % MILLISECONDS_PER_MINUTE) / MILLISECONDS_PER_SECOND)
  const ms = (_ms % MILLISECONDS_PER_MINUTE) % MILLISECONDS_PER_SECOND
  return {
    m,
    s,
    ms,
  }
}

/**
 * 분, 초, ms를 ms로 변환해주는 함수
 */
export const changeMinSecMsToMs = (m: number, s: number, ms: number) => {
  return m * MILLISECONDS_PER_MINUTE + s * MILLISECONDS_PER_SECOND + ms
}

/**
 * 숫자를 3자리씩 끊어서 comma를 찍어주는 함수
 *
 * @param x comma를 찍을 숫자
 */
export const numberWithCommas = (x: number): string => {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

/**
 * Portal 엘리먼트의 기본적인 스타일을 생성하는 함수
 *
 * @param wrapperRef createPortal을 사용하는 엘리먼트의 상위 엘리먼트
 * @param spaceX 상위 엘리먼트와 createPortal로 생성된 엘리먼트 사이의 가로 간격
 * @param spaceY 상위 엘리먼트와 createPortal로 생성된 엘리먼트 사이의 세로 간격
 * @returns createPortal 엘리먼트의 style
 */
export const createPortalStyle = ({
  wrapperRef,
  spaceX = 0,
  spaceY = 4,
}: {
  wrapperRef: React.MutableRefObject<HTMLDivElement | null>
  spaceX?: number
  spaceY?: number
}) => {
  if (!wrapperRef.current) return {}

  const styles: React.CSSProperties = {}
  const dimensions = wrapperRef.current.getBoundingClientRect()

  styles.left = dimensions.left + spaceX
  styles.marginRight = 16
  // TODO: 오른쪽이 기준일 경우 -> marginLeft
  if (dimensions.top < window.innerHeight / 2) {
    styles.top = dimensions.top + dimensions.height + spaceY
  } else {
    styles.bottom = window.innerHeight - dimensions.top + spaceY
  }

  return styles
}

/**
 * 소수점이 .0일 땐 정수만 표시, 소수점이 있을 땐 소수점 1번째 자리까지 표시
 */
export const dropDecimalPoint = (number: number, point?: number) =>
  numberWithCommas(Number(Number.isInteger(number) ? number.toFixed() : number.toFixed(point || 1)))

/**
 * byte 단위의 숫자를 적절한 단위와 함께 변환하여 표시해주는 함수
 *
 * @example
 * byteToSize(5870372) // return '5.6 MB'
 */
export const bytesToSize = (bytes: number) => {
  const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB']

  if (bytes === 0) return ''

  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  if (i === 0) return `${dropDecimalPoint(bytes)} ${sizes[i]}`
  return `${dropDecimalPoint(bytes / 1024 ** i)} ${sizes[i]}`
}

/**
 * Promise를 반환하는 시간 대기 함수
 */
export const delay = (sec: number): Promise<void> => {
  return new Promise((resolve) => {
    setTimeout(resolve, sec * 1000)
  })
}
