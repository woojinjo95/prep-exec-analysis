/**
 * 페이지네이션 데이터
 *
 * @param results 페이징처리된 데이터
 * @param jumpNext 10페이지 건너뛴 다음 페이지
 * @param jumpPrev 10페이지 건너뛴 이전 페이지
 * @param next 다음 페이지
 * @param pages 전체 페이지 개수
 * @param prev 이전 페이지
 * @param total 데이터 총 개수
 */
export interface PaginationResult<T> {
  jumpNext: number
  jumpPrev: number
  next: number
  pages: number
  prev: number
  total: number
  results: T
}
