/**
 * API Response
 */
export interface Response<T> {
  items: T
}

/**
 * API 페이지네이션 Response
 *
 * @param items 페이징처리된 데이터
 * @param jumpNext 10페이지 건너뛴 다음 페이지
 * @param jumpPrev 10페이지 건너뛴 이전 페이지
 * @param next 다음 페이지
 * @param pages 전체 페이지 개수
 * @param prev 이전 페이지
 * @param total 데이터 총 개수
 */
export interface PaginationResponse<T> extends Response<T> {
  jumpNext: number
  jumpPrev: number
  next: number
  pages: number
  prev: number
  total: number
}

export interface ScenarioSummary {
  id: string
  name: string
  tags: string[]
  updated_at: number
}
