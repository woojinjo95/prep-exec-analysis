import { AxiosError } from 'axios'
import API from '.'
import {
  HardwareConfiguration,
  LogConnectionStatus,
  ServiceState,
  PaginationResponse,
  Response,
  ScenarioSummary,
  Scenario,
} from './entity'
import apiUrls from './url'

/**
 * 시나리오 단건 조회 api
 */

export const getScenarioById = async ({ scenario_id }: { scenario_id: string }) => {
  try {
    const result = await API.get<Response<Scenario>>(`${apiUrls.scenario}/${scenario_id}`)

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 시나리오 리스트 조회 api
 */
export const getScenarios = async ({ page, page_size }: { page?: number; page_size?: number }) => {
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

/**
 * 하드웨어 설정 조회 api
 */
export const getHardwareConfiguration = async () => {
  try {
    const result = await API.get<Response<HardwareConfiguration>>(apiUrls.hardware_configuration)

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 터미널 - 쉘 연결
 */
export const postConnect = async () => {
  try {
    const result = await API.post<{ msg: string }>(apiUrls.connect)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 터미널 - 쉘 연결 해제
 */
export const postDisconnect = async () => {
  try {
    const result = await API.post<{ msg: string }>(apiUrls.disconnect)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 서비스 상태 조회 api
 */
export const getServiceState = async () => {
  try {
    const result = await API.get<Response<{ state: ServiceState }>>(apiUrls.service_state)

    return result.data.items.state
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 로그 연결여부 조회 api
 */
export const getLogConnectionStatus = async () => {
  try {
    const result = await API.get<Response<{ status: LogConnectionStatus }>>(apiUrls.log_connection_status)

    return result.data.items.status
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 특정 시나리오의 테스트런이 수행한 시작시간 및 종료시간 조회 api
 */
export const getVideoTimestamp = async (params: { scenario_id: string; testrun_id: string }) => {
  try {
    const result = await API.get<Response<{ start_time: string; end_time: string }>>(apiUrls.video_timestamp, {
      params,
    })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}
