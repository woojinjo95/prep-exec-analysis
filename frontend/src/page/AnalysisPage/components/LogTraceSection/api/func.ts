import API from '@global/api'
import { AxiosError } from 'axios'
import { Response } from '@global/api/entity'
import apiUrls from './url'
import { Logcat, Network, Shell, ShellLog } from './entity'

/**
 * 로그캣 로그 조회 api
 */
export const getLogcat = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
}) => {
  try {
    const result = await API.get<Response<Logcat[]>>(apiUrls.logcat, {
      params,
    })

    return result.data.items
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
  end_time: string
  scenario_id?: string
  testrun_id?: string
}) => {
  try {
    const result = await API.get<Response<Network[]>>(apiUrls.network, {
      params,
    })

    return result.data.items
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
  end_time: string
  scenario_id?: string
  testrun_id?: string
}) => {
  try {
    const result = await API.get<Response<ShellLog[]>>(apiUrls.shell_log, {
      params,
    })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}
