import API from '@global/api'
import { AxiosError } from 'axios'
import { PaginationResponse, Response } from '@global/api/entity'
import apiUrls from './url'
import { Logcat, Network, Shell, ShellLog } from './entity'

/**
 * 로그캣 로그 조회 api
 */
export const getLogcat = async (params: {
  start_time: string
  end_time?: string
  scenario_id?: string
  testrun_id?: string
  page?: number
  page_size?: number
  sort_by?: keyof Pick<Logcat, 'timestamp' | 'log_level' | 'message' | 'module' | 'pid' | 'process_name' | 'tid'>
  sort_desc?: boolean
}) => {
  try {
    const result = await API.get<PaginationResponse<Logcat[]>>(apiUrls.logcat, {
      params,
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 네트워크 로그 조회 api
 */
export const getNetwork = async (params: {
  start_time: string
  end_time?: string
  scenario_id?: string
  testrun_id?: string
  page?: number
  page_size?: number
  sort_by?: keyof Pick<Network, 'timestamp' | 'dst' | 'info' | 'length' | 'protocol' | 'src'>
  sort_desc?: boolean
}) => {
  try {
    const result = await API.get<PaginationResponse<Network[]>>(apiUrls.network, {
      params,
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 쉘 탭 리스트 조회 api
 */
export const getShells = async (params: { scenario_id?: string; testrun_id?: string }) => {
  try {
    const result = await API.get<Response<Shell[]>>(apiUrls.shell, {
      params,
    })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 쉘 로그 리스트 조회 api
 */
export const getShellLogs = async (params: {
  shell_mode: 'adb' | 'ssh'
  start_time: string
  end_time?: string
  scenario_id?: string
  testrun_id?: string
  page?: number
  page_size?: number
  sort_by?: keyof Pick<ShellLog, 'timestamp' | 'message' | 'module'>
  sort_desc?: boolean
}) => {
  try {
    const result = await API.get<PaginationResponse<ShellLog[]>>(apiUrls.shell_log, {
      params,
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}
