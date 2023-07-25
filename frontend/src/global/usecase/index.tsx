type DateToken =
  | 'YYYYMMDD'
  | 'YYYY-MM-DD'
  | 'YYYY.MM.DD'
  | 'YY.MM.DD'
  | 'HH:MM'
  | 'HH:MM:SS'
  | 'AA HH:MM'
  | 'YYYY-MM-DD HH:MM'
  | 'YYYY-MM-DD HH:MM:SS'
  | 'YYYY-MM-DD HH:MM:SS:MS'
  | 'YYYY_MM_DD_HH_MM_SS_MS'

/**
 * date format 함수
 */
export const formatDateTo = (type: DateToken, dateObject = new Date()): string => {
  const year = dateObject.getFullYear()
  const month = `0${dateObject.getMonth() + 1}`.slice(-2)
  const date = `0${dateObject.getDate()}`.slice(-2)
  const hour = dateObject.getHours() < 10 ? `0${dateObject.getHours()}` : dateObject.getHours()
  const minute = dateObject.getMinutes() < 10 ? `0${dateObject.getMinutes()}` : dateObject.getMinutes()
  const second = dateObject.getSeconds() < 10 ? `0${dateObject.getSeconds()}` : dateObject.getSeconds()
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
    default:
      return `${year}${month}${date}`
  }
}
