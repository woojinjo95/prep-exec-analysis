import { useQuery } from 'react-query'
import { useWebsocket } from '@global/hook'
import {
  getBoot,
  getCPU,
  getColorReferences,
  getEventLogs,
  getFreeze,
  getLogLevelFinders,
  getLogPatternMatching,
  getLoudness,
  getMemory,
  getResume,
} from './func'
import { AnalysisResponseMessageBody } from '../types'

/**
 * Log Level Finder 리스트 조회 hook
 */
export const useLogLevelFinders = (params: Parameters<typeof getLogLevelFinders>[0]) => {
  const { data, isLoading, refetch } = useQuery(['log_level_finder', params], () => getLogLevelFinders(params))

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'analysis_response' && message.data.measurement === 'log_level_finder') {
        refetch()
      }
    },
  })

  return { logLevelFinders: data, isLoading, refetch }
}

/**
 * CPU 사용률 리스트 조회 hook
 */
export const useCPU = (params: Parameters<typeof getCPU>[0]) => {
  // TODO: 서비스 상태가 analysis이면 -> enabled: false
  const { data, isLoading, refetch } = useQuery(['cpu', params], () => getCPU(params))

  return { cpu: data, isLoading, refetch }
}

/**
 * Memory 사용률 리스트 조회 hook
 */
export const useMemory = (params: Parameters<typeof getMemory>[0]) => {
  const { data, isLoading, refetch } = useQuery(['memory', params], () => getMemory(params))

  return { memory: data, isLoading, refetch }
}

/**
 * 이벤트 로그 리스트 조회 hook
 */
export const useEventLogs = (params: Parameters<typeof getEventLogs>[0]) => {
  const { data, isLoading, refetch } = useQuery(['event_log', params], () => getEventLogs(params))

  return { eventLogs: data, isLoading, refetch }
}

/**
 * Color Reference 리스트 조회 hook
 */
export const useColorReferences = (params: Parameters<typeof getColorReferences>[0]) => {
  const { data, isLoading, refetch } = useQuery(['color_reference', params], () => getColorReferences(params))

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'analysis_response' && message.data.measurement === 'color_reference') {
        refetch()
      }
    },
  })

  return { colorReferences: data, isLoading, refetch }
}

/**
 * Freeze 리스트 조회 hook
 */
export const useFreeze = (params: Parameters<typeof getFreeze>[0]) => {
  const { data, isLoading, refetch } = useQuery(['freeze', params], () => getFreeze(params))

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'analysis_response' && message.data.measurement === 'freeze') {
        refetch()
      }
    },
  })

  return { freeze: data, isLoading, refetch }
}

/**
 * Loudness 리스트 조회 hook
 */
export const useLoudness = (params: Parameters<typeof getLoudness>[0]) => {
  const { data, isLoading, refetch } = useQuery(['loudness', params], () => getLoudness(params))

  return { loudness: data, isLoading, refetch }
}

/**
 * Resume 리스트 조회 hook
 */
export const useResume = (params: Parameters<typeof getResume>[0]) => {
  const { data, isLoading, refetch } = useQuery(['resume', params], () => getResume(params))

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'analysis_response' && message.data.measurement === 'resume') {
        refetch()
      }
    },
  })

  return { resume: data, isLoading, refetch }
}

/**
 * Boot 리스트 조회 hook
 */
export const useBoot = (params: Parameters<typeof getBoot>[0]) => {
  const { data, isLoading, refetch } = useQuery(['boot', params], () => getBoot(params))

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'analysis_response' && message.data.measurement === 'boot') {
        refetch()
      }
    },
  })

  return { boot: data, isLoading, refetch }
}

/**
 * Log Pattern Matching 리스트 조회 hook
 */
export const useLogPatternMatching = (params: Parameters<typeof getLogPatternMatching>[0]) => {
  const { data, isLoading, refetch } = useQuery(['log_pattern_matching', params], () => getLogPatternMatching(params))

  useWebsocket<AnalysisResponseMessageBody>({
    onMessage: (message) => {
      if (message.msg === 'analysis_response' && message.data.measurement === 'log_pattern_matching') {
        refetch()
      }
    },
  })

  return { logPatternMatching: data, isLoading, refetch }
}
