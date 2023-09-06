import { AxiosError } from 'axios'
import API from '@global/api'
import { Response } from '@global/api/entity'
import { AnalysisConfig, AnalysisResultSummary } from './entity'
import apiUrls from './url'

/**
 * 분석 설정 조회 api
 */
export const getAnalysisConfig = async (params: { scenario_id: string; testrun_id: string }) => {
  try {
    const result = await API.get<Response<AnalysisConfig>>(apiUrls.analysis_config, { params })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 분석 결과(요약 데이터) 조회 api
 */
export const getAnalysisResultSummary = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
}) => {
  try {
    const result = await API.get<Response<AnalysisResultSummary>>(apiUrls.analysis_result_summary, { params })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}
