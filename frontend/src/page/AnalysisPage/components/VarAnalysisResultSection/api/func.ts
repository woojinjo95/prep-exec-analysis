import { AxiosError } from 'axios'
import API from '@global/api'
import { AnalysisConfig } from '@page/AnalysisPage/api/entity'
import { AnalysisType } from '@global/constant'
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
 * 분석 설정 삭제 api
 */
export const deleteAnalysisConfig = async ({
  scenario_id,
  testrun_id,
  analysis_type,
}: {
  scenario_id: string
  testrun_id: string
  analysis_type: keyof typeof AnalysisType
}) => {
  try {
    await API.delete(`${apiUrls.analysis_config}/${scenario_id}/${testrun_id}/${analysis_type}`)
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 로그 패턴 정규표현식 체크 api
 */
export const postValidateRegex = async ({ regex }: { regex: string }) => {
  try {
    const result = await API.post<{
      is_valid: boolean
      msg: string
    }>(apiUrls.validate_regex, { regex })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}
