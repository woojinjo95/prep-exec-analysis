import { AxiosError } from 'axios'
import { Response } from '@global/api/entity'
import API from '@global/api'
import { AnalysisConfig } from './entity'
import apiUrls from './url'

/**
 * 분석 설정 조회 api
 */
export const getAnalysisConfig = async () => {
  try {
    const result = await API.get<Response<AnalysisConfig>>(apiUrls.analysis_config)

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 분석 설정 수정 api
 */
export const putAnalysisConfig = async (data: AnalysisConfig) => {
  try {
    await API.put(apiUrls.analysis_config, data)
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}
