import API from '@global/api'
import { AxiosError } from 'axios'
import { Response } from '@global/api/entity'
import apiUrls from './url'
import { Logcat, Network } from './entity'

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
