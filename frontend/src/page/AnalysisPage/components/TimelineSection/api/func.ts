import API from '@global/api'
import { Response } from '@global/api/entity'
import { AxiosError } from 'axios'
import { FreezeType, LogLevel } from '@global/constant'
import { CPU, ColorReference, EventLog, Freeze, LogLevelFinder, Memory } from './entity'
import apiUrls from './url'

/**
 * CPU 사용률 리스트 조회 api
 */
export const getCPU = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
}) => {
  try {
    const result = await API.get<Response<CPU[]>>(apiUrls.cpu, { params })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * Memory 사용률 리스트 조회 api
 */
export const getMemory = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
}) => {
  try {
    const result = await API.get<Response<Memory[]>>(apiUrls.memory, { params })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * Event log 리스트 조회 api
 */
export const getEventLogs = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
}) => {
  try {
    const result = await API.get<Response<EventLog[]>>(apiUrls.event_log, { params })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * Color reference 리스트 조회 api
 */
export const getColorReferences = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
}) => {
  try {
    const result = await API.get<Response<ColorReference[]>>(apiUrls.color_reference, { params })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * Freeze 리스트 조회 api
 */
export const getFreeze = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
  freeze_type?: (keyof typeof FreezeType)[]
}) => {
  try {
    const result = await API.get<Response<Freeze[]>>(apiUrls.freeze, {
      params: {
        ...params,
        freeze_type: params.freeze_type ? params.freeze_type.join(',') : undefined,
      },
    })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * Log level finder 리스트 조회 api
 *
 * @param scenario_id 시나리오 id
 * @param testrun_id 테스트런 id
 * @param log_level 로그레벨 필터. ex: "V,D,I,W,E,F,S"
 */
export const getLogLevelFinders = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
  log_level?: (keyof typeof LogLevel)[]
}) => {
  try {
    const result = await API.get<Response<LogLevelFinder[]>>(apiUrls.log_level_finder, {
      params: {
        ...params,
        log_level: params.log_level ? params.log_level.join(',') : undefined,
      },
    })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}
