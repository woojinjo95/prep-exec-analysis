import API from '@global/api'
import { Response } from '@global/api/entity'
import { AxiosError } from 'axios'
import { CPU, ColorReference, EventLog, Freeze, LogLevelFinder, Memory } from './entity'
import apiUrls from './url'

/**
 * CPU 사용률 리스트 조회 api
 */
export const getCPU = async (params: {
  scenario_id?: string
  testrun_id?: string
  start_time: string
  end_time: string
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
  scenario_id?: string
  testrun_id?: string
  start_time: string
  end_time: string
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
export const getEventLogs = async (params: { scenario_id?: string; start_time: string; end_time: string }) => {
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
export const getColorReferences = async (params: { scenario_id?: string; start_time: string; end_time: string }) => {
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
  scenario_id?: string
  testrun_id?: string
  start_time: string
  end_time: string
}) => {
  try {
    const result = await API.get<Response<Freeze[]>>(apiUrls.freeze, { params })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * Log level finder 리스트 조회 api
 */
export const getLogLevelFinders = async (params: { scenario_id?: string; start_time: string; end_time: string }) => {
  try {
    const result = await API.get<Response<LogLevelFinder[]>>(apiUrls.log_level_finder, { params })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}
