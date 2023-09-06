import { AxiosError } from 'axios'
import API from '@global/api'
import { Response } from '@global/api/entity'
import { AnalysisConfig } from './entity'
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
