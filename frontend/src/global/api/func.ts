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
  BlockGroup,
  VideoSummary,
  TestRun,
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
 * 비디오 정보 조회 api
 */
export const getVideoSummary = async (params: { scenario_id: string; testrun_id: string }) => {
  try {
    const result = await API.get<Response<VideoSummary>>(apiUrls.video_summary, {
      params,
    })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * tag 조회
 */

export const getTag = async () => {
  try {
    const result = await API.get<Response<{ tags: string[] }>>(apiUrls.tag)

    return result.data.items.tags
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * tag 추가
 * @param tag 태그
 */
export const postTag = async (tag: string) => {
  try {
    await API.post<{ msg: string }>(apiUrls.tag, {
      tag,
    })
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * tag 수정
 * @param targetTag 바꿀 목표 태그
 * @param newTag 새로운 태그값
 */
export const putTag = async ({ targetTag, newTag }: { targetTag: string; newTag: string }) => {
  try {
    await API.put<{ msg: string }>(`${apiUrls.tag}/${targetTag}`, {
      tag: newTag,
    })
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * tag 삭제
 */
export const deleteTag = async (tag: string) => {
  try {
    await API.delete<{ msg: string }>(`${apiUrls.tag}/${tag}`)
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 테스트런 추가
 */
export const postTestrun = async (scenaroId: string) => {
  try {
    const result = await API.post<{ msg: string; id: string }>(`${apiUrls.testrun}/${scenaroId}`)

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 테스트런 조회
 */
export const getTestrun = async (params: { scenaroId: string }) => {
  try {
    const result = await API.get<Response<TestRun[]>>(`${apiUrls.testrun}`, {
      params,
    })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

interface postCopyScenarioParams {
  src_scenario_id: string
  name: string
  tags: string[]
  block_group: BlockGroup[]
}

/**
 * scenario copy
 */
export const postCopyScenario = async ({ copy_scenario }: { copy_scenario: postCopyScenarioParams }) => {
  try {
    await API.post<{ msg: string; id: string }>(`${apiUrls.copy_scenario}`, copy_scenario)
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * post scenario
 */
export const postScenario = async ({
  is_active,
  name,
  tags,
}: {
  is_active: boolean
  name?: string
  tags?: string[]
}) => {
  try {
    const result = await API.post<{ msg: string; id: string; testrun_id: string }>(`${apiUrls.scenario}`, {
      params: {
        is_active,
        name,
        tags,
      },
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}
