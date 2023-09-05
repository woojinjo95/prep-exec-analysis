import { AxiosError } from 'axios'
import { Response } from '@global/api/entity'
import API from '@global/api'
import { AnalysisConfig } from '@page/AnalysisPage/api/entity'
import { AnalysisResultSummary } from './entity'
import apiUrls from './url'

/**
 * 분석 설정 수정 api
 */
export const putAnalysisConfig = async ({
  scenario_id,
  testrun_id,
  ...data
}: { scenario_id: string; testrun_id: string } & AnalysisConfig) => {
  try {
    await API.put(`${apiUrls.analysis_config}/${scenario_id}/${testrun_id}`, data)
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
