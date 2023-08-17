import { AxiosError } from 'axios'
import API from '.'
import { PaginationResponse, ScenarioSummary } from './entity'
import apiUrls from './url'

/**
 * 시나리오 리스트 조회 api
 */
export const getScenarios = async ({ page, page_size }: { page: number; page_size: number }) => {
  try {
    const result = await API.get<PaginationResponse<ScenarioSummary[]>>(apiUrls.scenario, {
      params: {
        page,
        page_size,
      },
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}
