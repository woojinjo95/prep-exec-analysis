import { AxiosError } from 'axios'
import API from '@global/api'
import { PaginationResponse, Response } from '@global/api/entity'
import { FreezeType, LogLevel } from '@global/constant'
import {
  AnalysisConfig,
  AnalysisResultSummary,
  Boot,
  CPU,
  ColorReference,
  EventLog,
  Freeze,
  LogLevelFinder,
  LogPatternMatching,
  Loudness,
  Memory,
  Resume,
} from './entity'
import apiUrls from './url'

/**
 * 분석 설정 조회 api
 */
export const getAnalysisConfig = async (params: { scenario_id: string; testrun_id: string }) => {
  try {
    const result = await API.get<Response<AnalysisConfig>>(apiUrls.analysis_config, { params })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * 분석 결과(요약 데이터) 조회 api
 */
export const getAnalysisResultSummary = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
}) => {
  try {
    const result = await API.get<Response<AnalysisResultSummary>>(apiUrls.analysis_result_summary, { params })

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
    const result = await API.get<PaginationResponse<LogLevelFinder[]>>(apiUrls.log_level_finder, {
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
    const result = await API.get<PaginationResponse<CPU[]>>(apiUrls.cpu, { params })

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
    const result = await API.get<PaginationResponse<Memory[]>>(apiUrls.memory, { params })

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
    const result = await API.get<PaginationResponse<EventLog[]>>(apiUrls.event_log, { params })

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
    const result = await API.get<PaginationResponse<ColorReference[]>>(apiUrls.color_reference, { params })

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
  page?: number
  page_size?: number
  sort_by?: keyof Pick<Freeze, 'timestamp' | 'freeze_type' | 'duration'>
  sort_desc?: boolean
}) => {
  try {
    const result = await API.get<PaginationResponse<Freeze[]>>(apiUrls.freeze, {
      params: {
        ...params,
        freeze_type: params.freeze_type ? params.freeze_type.join(',') : undefined,
      },
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * Loudness 리스트 조회 api
 */
export const getLoudness = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
}) => {
  try {
    const result = await API.get<PaginationResponse<Loudness[]>>(apiUrls.loudness, {
      params,
    })

    return result.data.items
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * Resume 리스트 조회 api
 */
export const getResume = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
  page?: number
  page_size?: number
  sort_by?: keyof Pick<Resume, 'timestamp' | 'target' | 'measure_time'>
  sort_desc?: boolean
}) => {
  try {
    const result = await API.get<PaginationResponse<Resume[]>>(apiUrls.resume, {
      params,
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * Boot 리스트 조회 api
 */
export const getBoot = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
  page?: number
  page_size?: number
  sort_by?: keyof Pick<Boot, 'timestamp' | 'target' | 'measure_time'>
  sort_desc?: boolean
}) => {
  try {
    const result = await API.get<PaginationResponse<Boot[]>>(apiUrls.boot, {
      params,
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}

/**
 * LogPatternMatching 리스트 조회 api
 */
export const getLogPatternMatching = async (params: {
  start_time: string
  end_time: string
  scenario_id?: string
  testrun_id?: string
  page?: number
  page_size?: number
  sort_by?: keyof Pick<LogPatternMatching, 'timestamp' | 'log_pattern_name' | 'log_level'>
  sort_desc?: boolean
}) => {
  try {
    const result = await API.get<PaginationResponse<LogPatternMatching[]>>(apiUrls.log_pattern_matching, {
      params,
    })

    return result.data
  } catch (err) {
    const er = err as AxiosError
    throw er
  }
}
