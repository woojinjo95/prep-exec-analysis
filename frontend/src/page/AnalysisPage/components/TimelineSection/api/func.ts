import API from '@global/api'
import { Response } from '@global/api/entity'
import { AxiosError } from 'axios'
import { CPUAndMemory } from './entity'
import apiUrls from './url'

/**
 * CPU, Memory 사용률 리스트 조회 api
 */
export const getCPUAndMemory = async (params: { scenario_id?: string; start_time: string; end_time: string }) => {
  try {
    const result = await API.get<Response<CPUAndMemory[]>>(apiUrls.cpu_and_memory, { params })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}
